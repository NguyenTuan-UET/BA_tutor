import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import google.generativeai as genai

# Load environment
load_dotenv()
BASE_DIR = os.path.dirname(__file__)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_CHATBOT")
CHROMA_PATH = os.path.abspath(os.path.join(BASE_DIR, os.getenv("CHROMA_DIR")))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
TOP_K = int(os.getenv("TOP_K", 3))
SYSTEM_PROMPT_FILE = os.path.abspath(os.path.join(BASE_DIR, os.getenv("SYSTEM_PROMPT_FILE")))

# Cấu hình Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL)

# Tải prompt từ file
def load_prompt_template():
    if not os.path.isfile(SYSTEM_PROMPT_FILE):
        raise FileNotFoundError(f"⚠️ Không tìm thấy system_prompt.txt tại: {SYSTEM_PROMPT_FILE}")
    with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

prompt_template = load_prompt_template()

# Kết nối ChromaDB
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings(allow_reset=True))
collection = client.get_or_create_collection(name="knowledge_base", embedding_function=embedding_func)

# Chat loop
print("Nhập 'exit' để kết thúc cuộc hội thoại.\n")

while True:
    user_query = input("Bạn muốn hỏi gì?\n\n")
    if user_query.strip().lower() == "exit":
        print("Kết thúc cuộc hội thoại.")
        break

    results = collection.query(query_texts=[user_query], n_results=TOP_K)
    docs = results["documents"]

    system_prompt = prompt_template.format(docs=docs)
    response = model.generate_content([system_prompt, user_query])

    print("\n\n---------------------\n")
    print(response.text)
