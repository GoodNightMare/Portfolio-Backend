"""Curated intent aliases used by the portfolio scope guard and retriever."""

GREETING_TERMS = (
    "สวัสดี", "สวัสดีครับ", "สวัสดีค่ะ", "หวัดดี", "หวัดดีครับ", "ฮัลโหล",
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
)

THANKS_TERMS = (
    "ขอบคุณ", "ขอบคุณครับ", "ขอบคุณค่ะ", "ขอบใจ", "thanks", "thank you", "thx",
)

GOODBYE_TERMS = (
    "บาย", "บ๊ายบาย", "ลาก่อน", "เจอกัน", "ไปก่อน", "bye", "goodbye", "see you", "see ya",
)

HOW_ARE_YOU_TERMS = (
    "เป็นไงบ้าง", "สบายดีไหม", "สบายดีหรือเปล่า", "how are you", "how's it going",
)

MEAL_TERMS = (
    "กินข้าว", "กินอะไร", "หิวไหม", "หิวหรือยัง", "ทานข้าว", "กินอะไรดี",
)

SENSITIVE_TERMS = (
    "api key", "apikey", "api_key", "gemini_api_key", "secret key",
    "client secret", "access token", "bearer token", ".env", "env file",
    "รหัสผ่าน", "password", "passwd", "credential", "credentials",
    "database password", "db password", "connection string", "private key",
    "ssh key", "jwt secret", "system prompt", "system_prompt",
    "system instruction", "system_instruction", "developer prompt",
    "เปิดเผย prompt", "บอก prompt", "ขอ prompt", "คำสั่งระบบ",
    "ignore previous instructions", "ignore all instructions",
    "forget previous instructions", "show hidden prompt", "reveal your prompt",
)

OUT_OF_SCOPE_TERMS = (
    "อากาศ", "พยากรณ์อากาศ", "ฝนตกไหม", "weather", "forecast",
    "ราคาหุ้น", "ตลาดหุ้น", "คริปโต", "bitcoin", "ethereum", "stock price",
    "หวย", "เลขเด็ด", "lottery", "ข่าววันนี้", "ข่าวล่าสุด", "การเมือง",
    "เลือกตั้ง", "politics", "ฟุตบอล", "ผลบอล", "พรีเมียร์ลีก", "soccer",
    "ดูดวง", "ดวงวันนี้", "ราศี", "horoscope", "zodiac",
    "ทำการบ้านให้", "ทำข้อสอบให้", "เฉลยข้อสอบ", "homework", "exam answer",
    "แต่งเพลง", "แต่งนิยาย", "เขียนเรื่องสั้น", "สูตรอาหาร", "recipe",
)

PROJECT_TERMS = ("โปรเจกต์", "โปรเจค", "project", "projects", "ผลงาน", "งานที่เคยทำ")
ALL_TERMS = ("ทั้งหมด", "อะไรบ้าง", "ทุกโปรเจกต์", "รวมโปรเจกต์", "all projects", "ทุกผลงาน")

# The expansion text is repeated by the retriever to boost relevant headings.
QUERY_EXPANSIONS = (
    (("คือใคร", "แนะนำตัว", "ประวัติ", "ชื่ออะไร", "who is", "about night"),
     "ประวัติ นนท์ธีร์ ปานะถึก ไนท์ ชื่อ สถานะปัจจุบัน นักศึกษา"),
    (("เรียนอยู่ไหน", "เรียนที่ไหน", "ศึกษาอยู่ไหน", "มหาลัย", "มหาวิทยาลัย", "คณะ", "สาขา"),
     "ประวัติ การศึกษา มหาวิทยาลัย คณะ สาขา ชั้นปี นักศึกษา"),
    (("อยู่ที่ไหน", "อยู่จังหวัดไหน", "location", "where do you live"),
     "ประวัติ พื้นที่อาศัย กรุงเทพมหานคร ประเทศไทย"),
    (("ติดต่อ", "อีเมล", "email", "linkedin", "ช่องทางติดต่อ"),
     "ช่องทางออนไลน์ ติดต่อ GitHub LinkedIn อีเมล Portfolio"),
    (("ฝึกงาน", "สหกิจ", "internship", "co-op", "หางาน", "ตำแหน่ง"),
     "เป้าหมายการทำงาน Cooperative Education Internship ตำแหน่งที่สนใจ ระยะเวลา"),
    (("เป้าหมายในอนาคต", "อนาคตอยาก", "future goal", "career goal"),
     "เป้าหมายในอนาคต AI Engineer Software Engineer Applied AI"),
    (("เก่งอะไร", "ทำอะไรได้", "ทักษะ", "สกิล", "skill", "tech stack"),
     "ทักษะ ภาษาโปรแกรม Frontend Backend Database AI เครื่องมือ"),
    (("frontend", "front-end", "react", "next.js", "expo", "tailwind"),
     "Frontend Development React React Native Next.js Expo Tailwind CSS"),
    (("backend", "back-end", "node.js", "express", "asp.net", "fastapi", "rest api"),
     "Backend Development Node.js Express ASP.NET Core FastAPI REST API"),
    (("database", "ฐานข้อมูล", "postgresql", "mysql", "mongodb", "sql server", "chromadb"),
     "Database PostgreSQL MySQL MongoDB SQL Server ChromaDB Vector Database"),
    (("rag", "vector search", "embedding", "llm", "nlp"),
     "AI RAG Vector Search Embedding Large Language Model NLP"),
    (("computer vision", "object detection", "yolo", "zoedepth", "depth estimation", "ocr"),
     "Computer Vision Object Detection YOLO YOLO-World ZoeDepth OCR"),
    (("buddybuilder", "buddy builder", "ฮวงจุ้ย"), "BuddyBuilder AI Computer Vision RAG"),
    (("slideme", "slide me", "รถลาก", "tow truck"), "SlideMe Mobile Application Google Maps"),
    (("hikecycle", "hike cycle", "เช่าอุปกรณ์เดินป่า"), "HikeCycle Equipment Rental System"),
    (("courseflow", "course flow", "ระบบลงทะเบียน", "ลงทะเบียนเรียน"), "CourseFlow Course Registration System"),
    (("shingburishabu", "shingburi shabu", "ร้านชาบู"), "ShingburiShabu Restaurant Management"),
    (("all game bynight", "tic tac toe", "sliding puzzle", "connect four", "kanoodle"), "All Game ByNight Game Collection"),
    (("expense tracker", "รายรับรายจ่าย", "ค่าใช้จ่าย"), "Expense Tracker Personal Finance"),
    (("convert image", "แปลงไฟล์ภาพ", "heic"), "Convert Image Image Processing"),
    (("กิจกรรม", "แข่งขัน", "hackathon", "achievement", "รางวัล", "ผ่านรอบ"),
     "กิจกรรมและผลงาน Hackathon Achievement ผลลัพธ์"),
    (("จุดแข็ง", "ข้อดี", "strength"), "จุดแข็ง การทำงาน ทักษะ"),
    (("ทำงานเป็นทีม", "teamwork", "เพื่อนร่วมทีม", "collaboration"),
     "ประสบการณ์การทำงานเป็นทีม บทบาท ความรับผิดชอบ"),
    (("แก้ปัญหา", "problem solving", "เจอปัญหา"), "แนวทางการแก้ปัญหา Documentation ทดลอง ตรวจสอบ"),
    (("โปรเจกต์", "โปรเจค", "project", "ผลงาน"),
     "โปรเจกต์ ผลงาน Technologies Features บทบาทของไนท์"),
)
