# BA_tutor - He thong tro ly AI cho sinh vien nganh Tai chinh

## Muc tieu du an

**BA_tutor** la he thong hoi dap ung dung AI (Gemini, ChromaDB, NLP) ho tro sinh vien nganh Tai chinh, dac biet la sinh vien Hoc vien Ngan hang, tra cuu thong tin hoc tap, chuong trinh dao tao, mon hoc, tai lieu chuyen nganh, ... Du an giup sinh vien tiep can triet thuc nhanh chong, chinh xac, tiet kiem thoi gian va nang cao hieu qua hoc tap.

---

## 1. Yeu cau he thong

- **Windows 10/11**
- **Python 3.10+** (https://www.python.org/downloads/)
- **Node.js & npm** (https://nodejs.org/)
- **(Khuyen nghi) Git** (https://git-scm.com/download/win)

---

## 2. Cai dat backend

### a. Cai dat thu vien Python

Tai thu muc goc du an, chay:

```sh
pip install -r requirements.txt
```

### b. Tao file cau hinh moi truong `.env`

Tao file `.env` o thu muc goc (hoac copy tu mau neu co), noi dung vi du:

```
GOOGLE_API_KEY=your_google_gemini_api_key
MODEL_CHATBOT=gemini-1.0-pro
CHROMA_DIR=chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
TOP_K=3
SYSTEM_PROMPT_FILE=system_prompt.txt
```

> **Luu y:** Thay `your_google_gemini_api_key` bang API key that cua ban.

---

## 3. Cai dat frontend

Tai thu muc goc du an, chay:

```sh
cd frontend
npm install
cd ..
```

---

## 4. Chuan bi du lieu

- Dat cac file tai lieu (PDF, TXT, ...) vao thu muc `core/data/`.

---

## 5. Tao database ChromaDB tu du lieu

Chay script:

```sh
upload_doc.bat
```

- Script nay se tu dong chay `fill_database.py` de tao database tu du lieu.

---

## 6. Khoi dong he thong

Chay script:

```sh
run_all_win.bat
```

- Script nay se tu dong mo 2 cua so:
  - Backend (http://localhost:3001)
  - Frontend (http://localhost:3000)

---

## 7. Truy cap va su dung

- Mo trinh duyet, vao: [http://localhost:3000](http://localhost:3000) de su dung ung dung hoi dap AI.

---

## 8. Mot so luu y

- Neu thay doi du lieu trong `core/data/`, hay chay lai `upload_doc.bat` de cap nhat database.
- Neu gap loi ve module hoac import, hay chac chan ban chay lenh tu dung thu muc goc du an.
- Dam bao file `.env` da dien dung thong tin va API key con hieu luc.
- De dung he thong, chi can dong cac cua so cmd da mo ra.

---

## 9. `requirements.txt` chuan cho backend

```
fastapi
uvicorn
python-dotenv
chromadb
google-generativeai
langchain-community
sentence-transformers
```

---

## 10. Thong tin lien he

Neu can ho tro, vui long lien he: nqt.code@gmail.com

---

**Chuc ban su dung he thong hieu qua!**
