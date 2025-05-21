from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os

multilingual_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
CHROMA_PATH = "chroma_db"

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH,
    settings=Settings(allow_reset=True)
)
if "knowledge_base" in [c.name for c in chroma_client.list_collections()]:
    chroma_client.delete_collection("knowledge_base")

collection = chroma_client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=multilingual_ef
)

# Load PDF
pdf_loader = DirectoryLoader(
    DATA_PATH,
    glob="*.pdf",
    loader_cls=PyPDFLoader
)
pdf_documents = pdf_loader.load()
print(f"Số file PDF nạp: {len(pdf_documents)}")

# Load TXT
txt_loader = DirectoryLoader(
    DATA_PATH,
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
txt_documents = txt_loader.load()
print(f"Số file TXT nạp: {len(txt_documents)}")

if txt_documents:
    print("Nội dung file TXT đầu tiên:", txt_documents[0].page_content)

# Gộp lại
raw_documents = pdf_documents + txt_documents
print(f"Tổng số tài liệu (PDF+TXT): {len(raw_documents)}")

# KHÔNG SPLIT, chỉ upsert từng tài liệu luôn
documents = [doc.page_content for doc in raw_documents]
metadata = [doc.metadata for doc in raw_documents]
ids = [f"ID{i}" for i in range(len(raw_documents))]

collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)
print("Đã nạp dữ liệu PDF & TXT (không split) vào ChromaDB!")
