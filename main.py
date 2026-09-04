import os
import re
import math
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from threading import Lock

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import errors, types
import httpx
from pydantic import BaseModel, Field

from intents import (
    ALL_TERMS,
    GOODBYE_TERMS,
    GREETING_TERMS,
    HOW_ARE_YOU_TERMS,
    MEAL_TERMS,
    OUT_OF_SCOPE_TERMS,
    PROJECT_TERMS,
    SENSITIVE_TERMS,
    THANKS_TERMS,
)
from rag import PortfolioRetriever

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
CHAT_COOLDOWN_SECONDS = int(os.getenv("CHAT_COOLDOWN_SECONDS", "5"))
CHAT_HOURLY_LIMIT = int(os.getenv("CHAT_HOURLY_LIMIT", "30"))
MIN_RELEVANCE = 0.05
MIN_SCOPE_RELEVANCE = 0.10


class ChatRateLimiter:
    def __init__(self, cooldown_seconds: int, hourly_limit: int):
        self.cooldown_seconds = cooldown_seconds
        self.hourly_limit = hourly_limit
        self.requests: dict[str, deque[float]] = defaultdict(deque)
        self.lock = Lock()

    def check(self, client_id: str) -> None:
        now = time.monotonic()
        hour_ago = now - 3600

        with self.lock:
            timestamps = self.requests[client_id]
            while timestamps and timestamps[0] <= hour_ago:
                timestamps.popleft()

            if timestamps:
                cooldown_remaining = self.cooldown_seconds - (now - timestamps[-1])
                if cooldown_remaining > 0:
                    retry_after = math.ceil(cooldown_remaining)
                    raise HTTPException(
                        status_code=429,
                        detail=f"กรุณารออีก {retry_after} วินาทีก่อนส่งคำถามถัดไป",
                        headers={"Retry-After": str(retry_after)},
                    )

            if len(timestamps) >= self.hourly_limit:
                retry_after = math.ceil(3600 - (now - timestamps[0]))
                raise HTTPException(
                    status_code=429,
                    detail="คุณถามครบจำนวนที่กำหนดต่อชั่วโมงแล้ว กรุณาลองใหม่ภายหลัง",
                    headers={"Retry-After": str(retry_after)},
                )

            timestamps.append(now)


chat_rate_limiter = ChatRateLimiter(CHAT_COOLDOWN_SECONDS, CHAT_HOURLY_LIMIT)



class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class Source(BaseModel):
    title: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    mode: str
    model: str = MODEL_NAME


def guarded_response(question: str, contexts: list[dict] | None = None) -> str | None:
    normalized = " ".join(question.lower().split())
    exact = normalized.strip("!?., ")

    if any(term in normalized for term in SENSITIVE_TERMS):
        return "ขออภัยครับ ผมไม่สามารถเปิดเผย API key, Prompt หรือข้อมูลระบบภายในได้ แต่ถามเรื่องประวัติ ทักษะ และผลงานของไนท์ได้นะครับ"

    if any(term in normalized for term in MEAL_TERMS):
        return "ผมเป็น AI ประจำ Portfolio จึงกินข้าวไม่ได้ครับ 😄 ลองถามเกี่ยวกับประวัติ ทักษะ หรือผลงานของไนท์ได้นะครับ"

    if exact in GREETING_TERMS:
        return "สวัสดีครับ 👋 อยากรู้เรื่องประวัติ ทักษะ หรือผลงานส่วนไหนของไนท์ครับ?"

    if exact in THANKS_TERMS:
        return "ยินดีครับ 😊 หากอยากรู้เรื่องอื่นเกี่ยวกับไนท์ ถามต่อได้เลยครับ"

    if exact in GOODBYE_TERMS:
        return "ขอบคุณที่เข้ามาคุยกันครับ แล้วพบกันใหม่ 👋"

    if exact in HOW_ARE_YOU_TERMS:
        return "สบายดีครับ 😊 ผมพร้อมช่วยตอบคำถามเกี่ยวกับไนท์ มีเรื่องไหนอยากทราบเป็นพิเศษไหมครับ?"

    if any(term in normalized for term in OUT_OF_SCOPE_TERMS):
        return "คำถามนี้อยู่นอกขอบเขตของ Portfolio ครับ ผมช่วยตอบเกี่ยวกับประวัติ การศึกษา ทักษะ โปรเจกต์ กิจกรรม และการติดต่อไนท์ได้ครับ"

    if contexts and contexts[0]["score"] < MIN_SCOPE_RELEVANCE:
        return "ยังไม่พบข้อมูลเรื่องนี้ใน Portfolio ของไนท์ครับ ลองถามเกี่ยวกับประวัติ การศึกษา ทักษะ โปรเจกต์ กิจกรรม หรือช่องทางติดต่อดูนะครับ"

    return None


def wants_all_projects(question: str) -> bool:
    normalized = question.lower()
    return (
        any(term in normalized for term in PROJECT_TERMS)
        and any(term in normalized for term in ALL_TERMS)
    )


def fallback_answer(contexts: list[dict]) -> str:
    if not contexts or contexts[0]["score"] < MIN_RELEVANCE:
        return "ยังไม่พบข้อมูลเรื่องนี้ใน Portfolio ของไนท์ ลองถามเกี่ยวกับประวัติ ทักษะ โปรเจกต์ การฝึกงาน หรือช่องทางติดต่อดูนะครับ"
    text = " ".join(context["text"] for context in contexts[:2])
    return f"ขณะนี้ระบบ AI ไม่พร้อมให้บริการชั่วคราว แต่ยังค้นข้อมูลจาก Portfolio ให้ได้ครับ: {text}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.retriever = PortfolioRetriever(BASE_DIR / "knowledge")
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    app.state.gemini = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=15_000),
    ) if api_key else None
    yield
    if app.state.gemini:
        app.state.gemini.close()


app = FastAPI(title="Night Portfolio RAG", lifespan=lifespan)
origins = [item.strip() for item in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/api/health")
def health(request: Request):
    return {
        "status": "ok",
        "gemini_configured": request.app.state.gemini is not None,
        "model": MODEL_NAME,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request):
    client_id = request.client.host if request.client else "unknown"
    chat_rate_limiter.check(client_id)

    immediate_response = guarded_response(payload.question)
    if immediate_response:
        return ChatResponse(answer=immediate_response, sources=[], mode="guard")

    if wants_all_projects(payload.question):
        projects = request.app.state.retriever.project_documents()
        names = [re.sub(r"^\d+\.\s*", "", project.title) for project in projects]
        answer = "โปรเจกต์ทั้งหมดของไนท์ ได้แก่ " + ", ".join(names) + " ครับ"
        return ChatResponse(
            answer=answer,
            sources=[Source(title=project.title) for project in projects],
            mode="retrieval",
        )

    contexts = request.app.state.retriever.search(payload.question)
    scope_response = guarded_response(payload.question, contexts)
    if scope_response:
        return ChatResponse(answer=scope_response, sources=[], mode="guard")

    sources = [Source(title=item["title"]) for item in contexts if item["score"] >= MIN_RELEVANCE]
    if not request.app.state.gemini:
        return ChatResponse(answer=fallback_answer(contexts), sources=sources, mode="fallback")

    context_text = "\n\n".join(
        f"แหล่งข้อมูล: {item['title']}\n{item['text']}" for item in contexts
    )
    try:
        response = request.app.state.gemini.models.generate_content(
            model=MODEL_NAME,
            contents=f"คำถาม: {payload.question}\n\nข้อมูลจาก Portfolio:\n{context_text}",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "คุณคือ Night AI และเป็น ผู้ชาย ตอบคำถามเกี่ยวกับนนท์ธีร์ ปานะถึก "
                    "ตอบภาษาเดียวกับคำถามอย่างสุภาพและกระชับ ใช้เฉพาะข้อมูลที่ให้มา "
                    "ห้ามแต่งข้อมูล หากข้อมูลไม่พอให้บอกว่าไม่พบใน Portfolio "
                    "ตอบเป็นข้อความธรรมดา ไม่ใช้ Markdown หรือเครื่องหมายดอกจันเพื่อเน้นข้อความ"
                ),
                temperature=0.2,
                max_output_tokens=400,
            ),
        )
        answer = (response.text or "").strip()
        if not answer:
            raise ValueError("empty response")
        return ChatResponse(answer=answer, sources=sources, mode="ai")
    except (errors.APIError, httpx.HTTPError, ValueError, OSError, RuntimeError):
        return ChatResponse(answer=fallback_answer(contexts), sources=sources, mode="fallback")
