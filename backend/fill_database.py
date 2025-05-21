import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "core", "data")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Khởi tạo embedding + Chroma client
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH, settings=Settings(allow_reset=True)
)

# Xóa và tạo lại collection
if "knowledge_base" in [c.name for c in chroma_client.list_collections()]:
    chroma_client.delete_collection("knowledge_base")

collection = chroma_client.get_or_create_collection(
    name="knowledge_base", embedding_function=embedding_func
)

# Load tài liệu PDF và TXT
pdf_loader = DirectoryLoader(DATA_DIR, glob="*.pdf", loader_cls=PyPDFLoader)
txt_loader = DirectoryLoader(
    DATA_DIR, glob="*.txt", loader_cls=lambda path: TextLoader(path, encoding="utf-8")
)

documents = pdf_loader.load() + txt_loader.load()
print(f"📄 Số tài liệu đọc được: {len(documents)}")

# Chia văn bản thành các đoạn nhỏ (chunk) để xử lý embedding hiệu quả.
# - chunk_size=500: mỗi đoạn tối đa 500 ký tự, giúp giảm độ dài văn bản đầu vào model.
# - chunk_overlap=50: mỗi đoạn sẽ chồng 50 ký tự với đoạn trước đó, giữ ngữ cảnh liền mạch.
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Đưa vào Chroma
for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.page_content], metadatas=[chunk.metadata], ids=[f"chunk-{i}"]
    )

print(f"✅ Đã nạp {len(chunks)} chunk vào ChromaDB.")
