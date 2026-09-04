"""Curated intent aliases used by the portfolio scope guard and retriever."""

GREETING_TERMS = (
    "สวัสดี", "สวัสดีครับ", "สวัสดีค่ะ", "หวัดดี", "หวัดดีครับ", "ฮัลโหล",
    "ทักทาย", "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
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
PROJECT_TERMS += ("โปรเจ็ค", "ชิ้นงาน", "งานที่ทำ")
ALL_TERMS = (
    "ทั้งหมด", "อะไรบ้าง", "มีอะไรบ้าง", "ทำอะไรมาบ้าง", "เคยทำอะไร", "บ้าง",
    "ทุกโปรเจกต์", "ทุกโปรเจค", "ทุกโปรเจ็ค", "รวมโปรเจกต์", "all projects", "ทุกผลงาน",
)

# The expansion text is repeated by the retriever to boost relevant headings.
QUERY_EXPANSIONS = (
    (("โปรเจกต์ที่ใช้ ai", "โปรเจคที่ใช้ ai", "โปรเจกต์ ai", "โปรเจค ai",
      "โปรเจ็ค ai", "ใช้ ai ในโปรเจกต์", "ใช้ ai ในโปรเจค", "ใช้ ai ทำอะไร",
      "ai ที่เคยทำ", "ผลงาน ai", "ai project", "project using ai", "project ที่ใช้ ai"),
     "BuddyBuilder AI BuddyBuilder AI โปรเจกต์ AI Application Computer Vision RAG "
     "YOLO-World ZoeDepth Llama ChromaDB PostgreSQL"),
    (("คือใคร", "เป็นใคร", "แนะนำตัว", "เล่าเกี่ยวกับตัวเอง", "ประวัติ", "ชื่ออะไร",
      "ชื่อจริง", "ชื่อเล่น", "อายุ", "who is", "about night", "introduce yourself"),
     "ประวัติ นนท์ธีร์ ปานะถึก ไนท์ ชื่อ สถานะปัจจุบัน นักศึกษา"),
    (("เรียนอยู่ไหน", "เรียนที่ไหน", "ศึกษาอยู่ไหน", "ศึกษาอยู่ที่ไหน", "เรียนอะไร",
      "เรียนสาขาอะไร", "คณะอะไร", "ชั้นปี", "ปีไหน", "มหาลัย", "มหาวิทยาลัย", "คณะ", "สาขา",
      "education", "study", "university"),
     "ประวัติ การศึกษา มหาวิทยาลัย คณะ สาขา ชั้นปี นักศึกษา"),
    (("อยู่ที่ไหน", "อยู่จังหวัดไหน", "อยู่กรุงเทพไหม", "ที่อยู่", "อาศัยอยู่", "location", "where do you live"),
     "ประวัติ พื้นที่อาศัย กรุงเทพมหานคร ประเทศไทย"),
    (("ติดต่อ", "อีเมล", "เมล", "email", "contact", "เบอร์โทร", "โทรศัพท์",
      "github", "linkedin", "portfolio", "ช่องทางติดต่อ",
      "ช่องทางออนไลน์", "social", "repository", "repo", "ดูโค้ด"),
     "สรุปช่องทางติดต่อ Email GitHub LinkedIn Portfolio"),
    (("ฝึกงาน", "สหกิจ", "internship", "intern", "co-op", "cooperative", "หางาน", "สมัครงาน",
      "พร้อมทำงาน", "ตำแหน่งที่สนใจ", "ตำแหน่ง", "สายงาน", "รับงานไหม"),
     "เป้าหมายการทำงาน Cooperative Education Internship ตำแหน่งที่สนใจ ระยะเวลา"),
    (("เป้าหมายในอนาคต", "อนาคตอยาก", "อยากเป็นอะไร", "เส้นทางอาชีพ", "career path",
      "future goal", "career goal"),
     "เป้าหมายในอนาคต AI Engineer Software Engineer Applied AI"),
    (("เก่งอะไร", "ทำอะไรได้", "ถนัดอะไร", "ความสามารถ", "ทักษะ", "สกิล", "skill", "skills",
      "tech stack", "technology", "เทคโนโลยีที่ใช้", "ภาษาอะไร", "ภาษาโปรแกรม"),
     "สรุปทักษะทั้งหมด ภาษาโปรแกรม Frontend Backend Database AI เครื่องมือ"),
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
    (("โปรเจกต์ที่ใช้ react", "โปรเจคที่ใช้ react", "งานที่ใช้ react", "react project"),
     "ดัชนีโปรเจกต์ตามประเภทและเทคโนโลยี React โปรเจกต์ที่ใช้ React"),
    (("โปรเจกต์ mobile", "โปรเจค mobile", "mobile project", "แอปมือถือ", "mobile application"),
     "SlideMe SlideMe React Native Expo Mobile Application Google Maps"),
    (("โปรเจกต์ full stack", "โปรเจค full stack", "full-stack project", "full stack project"),
     "ดัชนีโปรเจกต์ตามประเภทและเทคโนโลยี Full-Stack HikeCycle CourseFlow"),
    (("โปรเจกต์ที่ใช้ c#", "โปรเจคที่ใช้ c#", "c# project", ".net project"),
     "HikeCycle HikeCycle C# ASP.NET Core MVC SQL Server"),
    (("โปรเจกต์ที่ใช้ node", "โปรเจคที่ใช้ node", "node.js project", "express project"),
     "ดัชนีโปรเจกต์ตามประเภทและเทคโนโลยี Node.js Express MongoDB CourseFlow Convert Image"),
    (("โปรเจกต์เกม", "โปรเจคเกม", "เกมที่ทำ", "game project"),
     "All Game ByNight All Game ByNight Game Collection Game Logic"),
    (("buddybuilder", "buddy builder", "buddy builder ai", "ฮวงจุ้ย", "วิเคราะห์ห้อง", "จัดวางเฟอร์นิเจอร์"),
     "BuddyBuilder AI Computer Vision RAG หน้าที่ Technologies Workflow Repository"),
    (("slideme", "slide me", "รถลาก", "เรียกรถลาก", "tow truck"),
     "SlideMe Mobile Application Google Maps หน้าที่ Technologies Features Repository"),
    (("hikecycle", "hike cycle", "hike-cycle", "เช่าอุปกรณ์เดินป่า", "อุปกรณ์เดินป่า"),
     "HikeCycle Equipment Rental System หน้าที่ Technologies Features Repository"),
    (("courseflow", "course flow", "ระบบลงทะเบียน", "ลงทะเบียนเรียน"), "CourseFlow Course Registration System"),
    (("shingburishabu", "shingburi shabu", "singburi shabu", "ร้านชาบู", "ระบบร้านอาหาร"),
     "ShingburiShabu Restaurant Management หน้าที่ Technologies Features"),
    (("all game bynight", "tic tac toe", "sliding puzzle", "connect four", "kanoodle"), "All Game ByNight Game Collection"),
    (("expense tracker", "รายรับรายจ่าย", "ค่าใช้จ่าย"), "Expense Tracker Personal Finance"),
    (("convert image", "แปลงไฟล์ภาพ", "heic"), "Convert Image Image Processing"),
    (("กิจกรรม", "เข้าร่วมอะไร", "แข่งขัน", "การแข่งขัน", "hackathon", "bootcamp", "achievement",
      "รางวัล", "ผ่านรอบ", "ประสบการณ์นอกห้องเรียน"),
     "สรุปกิจกรรมและการแข่งขันทั้งหมด Hackathon Bootcamp Achievement ผลลัพธ์"),
    (("samsung", "kbtg", "cybersecurity"), "Samsung KBTG Digital Cybersecurity Hackathon 2026"),
    (("ai-preneur", "ai preneur"), "AI-Preneur Hackathon 2026 ผลลัพธ์ ผ่านรอบคัดเลือก"),
    (("gosoft", "retail tech"), "Gosoft Retail Tech Hackathon 2026 ผลลัพธ์ ผ่านรอบคัดเลือก"),
    (("electrical engineering network", "eenet"), "The 18th Electrical Engineering Network 2026"),
    (("national software contest", "nsc"), "National Software Contest 2024"),
    (("nitmx", "fintech bootcamp"), "NITMX Fintech Bootcamp 2026"),
    (("จุดแข็ง", "ข้อดี", "strength"), "จุดแข็ง การทำงาน ทักษะ"),
    (("ทำงานเป็นทีม", "teamwork", "เพื่อนร่วมทีม", "collaboration"),
     "ประสบการณ์การทำงานเป็นทีม บทบาท ความรับผิดชอบ"),
    (("แก้ปัญหา", "วิธีแก้ปัญหา", "problem solving", "เจอปัญหา", "รับมือปัญหา"),
     "แนวทางการแก้ปัญหา Documentation ทดลอง ตรวจสอบ"),
    (("กำลังเรียน", "กำลังศึกษา", "เรียนรู้อะไร", "ศึกษาอะไรเพิ่ม", "currently learning"),
     "สิ่งที่กำลังเรียนรู้ AI Engineering Software Architecture Cloud Deployment Testing"),
    (("โปรเจกต์", "โปรเจค", "โปรเจ็ค", "project", "projects", "ผลงาน", "ชิ้นงาน", "งานที่เคยทำ"),
     "โปรเจกต์ ผลงาน Technologies Features บทบาทของไนท์"),
)
