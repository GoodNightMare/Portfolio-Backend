# Night Portfolio RAG API

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload
```

ใส่ `GEMINI_API_KEY` ใน `.env` ก่อนรัน ระบบทำ local hashed text embeddings โดยไม่ต้องดาวน์โหลดโมเดลเพิ่ม ข้อมูลที่ RAG ใช้อยู่ใน `knowledge/portfolio.md`
