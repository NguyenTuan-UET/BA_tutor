from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import google.generativeai as genai

# === Load biến môi trường từ file .env ===
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_CHATBOT")
CHROMA_PATH = os.path.join(BASE_DIR, os.getenv("CHROMA_DIR"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
TOP_K = int(os.getenv("TOP_K"))

# === Đường dẫn đến system_prompt.txt trong core/data ===
PROMPT_PATH = os.path.join(BASE_DIR, "core", os.getenv("SYSTEM_PROMPT_FILE"))
print(f"[INFO] Đang sử dụng system_prompt: {PROMPT_PATH}")  # Debug

# === Khởi tạo Gemini ===
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL)

# === Tải prompt mẫu từ file ===
if not os.path.isfile(PROMPT_PATH):
    raise FileNotFoundError(f"⚠️ Không tìm thấy prompt: {PROMPT_PATH}")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    prompt_template = f.read()

# === Kết nối ChromaDB ===
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings())
collection = client.get_or_create_collection(
    name="knowledge_base", embedding_function=embedding_func
)

# === Tạo FastAPI app ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Endpoint hỏi/đáp ===
@app.post("/api/ask")
async def ask_api(request: Request):
    data = await request.json()
    user_query = data.get("question")
    if not user_query:
        return {"error": "Missing question"}

    results = collection.query(query_texts=[user_query], n_results=TOP_K)
    docs = results["documents"]
    flattened_docs = "\n\n".join([doc[0] for doc in docs])
    system_prompt = prompt_template.format(docs=flattened_docs)

    response = model.generate_content([system_prompt, user_query])
    return {"answer": response.text.strip()}


# === Endpoint kiểm tra tình trạng ===
@app.get("/api/health")
def health():
    return {"status": "ok"}


# === Khởi chạy server ===
if __name__ == "__main__":
    import os

    port = int(
        os.environ.get("PORT", 10000)
    )  # Lấy PORT từ môi trường do Render cung cấp
    uvicorn.run("backend.api_server:app", host="0.0.0.0", port=port)
