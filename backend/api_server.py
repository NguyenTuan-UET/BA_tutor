from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import google.generativeai as genai

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), "../core/.env"))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_CHATBOT")
CHROMA_PATH = os.path.abspath(os.path.join(BASE_DIR, os.getenv("CHROMA_DIR")))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
TOP_K = int(os.getenv("TOP_K"))
SYSTEM_PROMPT_FILE = os.path.abspath(
    os.path.join(BASE_DIR, "core", os.getenv("SYSTEM_PROMPT_FILE"))
)

# Gemini config
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL)

# Load prompt template
if not os.path.isfile(SYSTEM_PROMPT_FILE):
    raise FileNotFoundError(
        f"⚠️ Không tìm thấy system_prompt.txt tại: {SYSTEM_PROMPT_FILE}"
    )
with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
    prompt_template = f.read()

# ChromaDB
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
client = chromadb.PersistentClient(
    path=CHROMA_PATH, settings=Settings(allow_reset=True)
)
collection = client.get_or_create_collection(
    name="knowledge_base", embedding_function=embedding_func
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/ask")
async def ask_api(request: Request):
    data = await request.json()
    user_query = data.get("question")
    if not user_query:
        return {"error": "Missing question"}
    results = collection.query(query_texts=[user_query], n_results=TOP_K)
    docs = results["documents"]
    system_prompt = prompt_template.format(docs=docs)
    response = model.generate_content([system_prompt, user_query])
    return {"answer": response.text.strip()}


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("backend.api_server:app", host="0.0.0.0", port=3001, reload=True)
