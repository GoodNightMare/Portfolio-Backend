import os
import re
import hashlib
import math
from dataclasses import dataclass
from pathlib import Path


QUERY_EXPANSIONS = (
    (("เรียนอยู่ไหน", "เรียนที่ไหน", "ศึกษาอยู่ไหน", "ศึกษาอยู่ที่ไหน", "มหาลัย", "มหาวิทยาลัย"),
     "ประวัติ มหาวิทยาลัย คณะ สาขา สถานะนักศึกษา"),
    (("เรียนอะไร", "เรียนสาขา", "สาขาอะไร", "คณะอะไร"),
     "ประวัติ คณะ สาขา วิทยาการคอมพิวเตอร์"),
    (("ฝึกงาน", "สหกิจ", "สมัครงาน", "หางาน", "ตำแหน่ง"),
     "เป้าหมายการทำงาน Cooperative Education Internship ตำแหน่งที่สนใจ"),
    (("เก่งอะไร", "ทำอะไรได้", "ทักษะ", "สกิล", "skill"),
     "ทักษะ ภาษาโปรแกรม Frontend Backend Database AI เครื่องมือ"),
    (("ผลงาน", "โปรเจกต์", "โปรเจค", "project"),
     "โปรเจกต์ ผลงาน Technologies Features บทบาทของไนท์"),
    (("ติดต่อ", "อีเมล", "email", "github", "linkedin"),
     "ช่องทางออนไลน์ ติดต่อ GitHub LinkedIn อีเมล"),
)


@dataclass(frozen=True)
class Document:
    title: str
    text: str


class PortfolioRetriever:
    def __init__(self, knowledge_dir: Path):
        self.documents = self._load_documents(knowledge_dir)
        self.dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "2048"))
        self.embeddings = [
            self._embed(f"{document.title} {document.title} {document.text}")
            for document in self.documents
        ]

    def _embed(self, text: str) -> dict[int, float]:
        normalized = re.sub(r"\s+", " ", text.lower()).strip()
        compact = normalized.replace(" ", "")
        tokens = re.findall(r"[a-z0-9+#.]+", normalized)
        features = tokens + [compact[index:index + 3] for index in range(max(0, len(compact) - 2))]
        vector: dict[int, float] = {}
        for feature in features:
            index = int.from_bytes(hashlib.blake2b(feature.encode("utf-8"), digest_size=4).digest(), "big") % self.dimensions
            vector[index] = vector.get(index, 0.0) + 1.0
        magnitude = math.sqrt(sum(value * value for value in vector.values())) or 1.0
        return {index: value / magnitude for index, value in vector.items()}

    @staticmethod
    def _similarity(left: dict[int, float], right: dict[int, float]) -> float:
        if len(left) > len(right):
            left, right = right, left
        return sum(value * right.get(index, 0.0) for index, value in left.items())

    @staticmethod
    def _expand_query(question: str) -> str:
        normalized = question.lower()
        expansions = [
            expansion
            for aliases, expansion in QUERY_EXPANSIONS
            if any(alias in normalized for alias in aliases)
        ]
        return " ".join([question, *expansions, *expansions])

    @staticmethod
    def _load_documents(knowledge_dir: Path) -> list[Document]:
        documents = []
        for path in sorted(knowledge_dir.glob("*.md")):
            sections = re.split(r"(?m)^##\s+", path.read_text(encoding="utf-8"))
            for section in sections[1:]:
                title, _, body = section.partition("\n")
                if body.strip():
                    documents.append(Document(title.strip(), body.strip()))
        if not documents:
            raise RuntimeError("ไม่พบข้อมูลในโฟลเดอร์ knowledge")
        return documents

    def search(self, question: str, limit: int = 3) -> list[dict]:
        query = self._embed(self._expand_query(question))
        scores = [self._similarity(embedding, query) for embedding in self.embeddings]
        indices = sorted(range(len(scores)), key=scores.__getitem__, reverse=True)[:limit]
        return [{
            "title": self.documents[index].title,
            "text": self.documents[index].text,
            "score": float(scores[index]),
        } for index in indices]
