import os
from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader

# Load env from .env
load_dotenv()

# Đường dẫn tuyệt đối tới thư mục data
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, os.getenv("DATA_DIR")))
CHROMA_PATH = os.path.abspath(os.path.join(BASE_DIR, os.getenv("CHROMA_DIR")))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Check thư mục data tồn tại
if not os.path.isdir(DATA_PATH):
    raise FileNotFoundError(f"❌ Không tìm thấy thư mục dữ liệu: {DATA_PATH}")

# Embedding
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

# Khởi tạo client
client = PersistentClient(path=CHROMA_PATH, settings=Settings(allow_reset=True))

# Reset collection nếu đã tồn tại
if "knowledge_base" in [c.name for c in client.list_collections()]:
    client.delete_collection("knowledge_base")

collection = client.get_or_create_collection(name="knowledge_base", embedding_function=embedding_func)

# Load tài liệu
pdf_docs = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader).load()
txt_docs = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}).load()

all_docs = pdf_docs + txt_docs
documents = [doc.page_content for doc in all_docs]
metadata = [doc.metadata for doc in all_docs]
ids = [f"id{i}" for i in range(len(all_docs))]

collection.upsert(documents=documents, metadatas=metadata, ids=ids)
print(f"✅ Đã nạp {len(all_docs)} tài liệu (PDF+TXT) vào ChromaDB.")
