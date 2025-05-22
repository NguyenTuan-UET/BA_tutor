# BA_tutor: AI Hỗ Trợ Học Tập Ngành Tài Chính

## Giới thiệu dự án

**BA_tutor** là một hệ thống hỏi đáp ứng dụng AI, sử dụng mô hình Gemini của Google và cơ sở tri thức ChromaDB để hỗ trợ sinh viên ngành Tài chính, đặc biệt là sinh viên Học viện Ngân hàng. Dự án hướng tới việc cung cấp một trợ lý học tập thông minh, giúp giải đáp thắc mắc về chương trình đào tạo, môn học, tài liệu, cũng như đưa ra lời khuyên hữu ích cho sinh viên.

### Định hướng và vai trò của AI trong dự án

- **Cá nhân hóa học tập:** AI giúp sinh viên tiếp cận thông tin nhanh chóng, chính xác, phù hợp với nhu cầu từng cá nhân.
- **Tăng hiệu quả tự học:** Hỗ trợ giải đáp các câu hỏi về kiến thức chuyên ngành, tài liệu, quy chế, định hướng nghề nghiệp.
- **Tiết kiệm thời gian:** Tìm kiếm thông tin từ kho dữ liệu lớn chỉ trong vài giây.
- **Hỗ trợ giảng viên:** Có thể mở rộng để hỗ trợ giảng viên trong việc xây dựng tài liệu, kiểm tra kiến thức sinh viên.

---

## Hướng dẫn cài đặt và chạy dự án

### 1. Yêu cầu hệ thống

- Python >= 3.10
- Node.js & npm (để chạy frontend)

### 2. Cài đặt backend

1. Cài đặt các thư viện Python:
   ```bash
   pip install -r requirements.txt
   ```
2. Tạo file `.env` ở thư mục gốc dự án với nội dung mẫu:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   MODEL_CHATBOT=gemini-1.0-pro
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   CHROMA_DIR=chroma_db
   SYSTEM_PROMPT_FILE=system_prompt.txt
   TOP_K=3
   ```
3. Chuẩn bị dữ liệu: Đặt các file tài liệu (PDF, TXT) vào `core/data/`.
4. Khởi tạo database ChromaDB:
   ```bash
   python backend/fill_database.py
   ```
5. Chạy server API:
   ```bash
   uvicorn backend.api_server:app --reload --port 3001
   ```

### 3. Cài đặt và chạy frontend

1. Di chuyển vào thư mục frontend:
   ```bash
   cd frontend
   ```
2. Cài đặt dependencies:
   ```bash
   npm install
   ```
3. Chạy ứng dụng:
   ```bash
   npm run dev
   ```
4. Truy cập: [http://localhost:5173/](http://localhost:5173/)

### 4. Hỏi đáp trực tiếp với Gemini (CLI, tùy chọn)

```bash
python test/gemini_cli.py
```

---

## Thư mục quan trọng

- `backend/`: Chứa mã nguồn backend (API, xử lý dữ liệu, kết nối AI)
- `core/data/`: Lưu trữ tài liệu, dữ liệu đầu vào
- `chroma_db/`: Cơ sở dữ liệu vector hóa (tự động tạo, không cần push lên git)
- `frontend/`: Mã nguồn giao diện web

---

## Liên hệ & đóng góp

- Email: nqt.code@gmail.com
- Đóng góp ý tưởng, tài liệu, phản hồi đều được hoan nghênh!
