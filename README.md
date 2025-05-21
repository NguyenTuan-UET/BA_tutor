# BA_tutor

## Mô tả dự án

Dự án BA_tutor là một ứng dụng hỏi đáp sử dụng Gemini và ChromaDB để cung cấp thông tin và hỗ trợ học tập trong lĩnh vực tài chính.

## Yêu cầu

- Python 3.10 trở lên
- Đã cài đặt các package cần thiết (xem bên dưới)
- Đã có API key Gemini (Google Generative AI)

## Cài đặt thư viện

Cài đặt các thư viện cần thiết bằng pip:

```bash
pip install -r requirements.txt
```

## Thiết lập API Key

Tạo file `core/.env` hoặc chỉnh sửa file `core/config.py` để chứa biến môi trường:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

Hoặc sửa trực tiếp trong code nếu cần.

## Hướng dẫn chạy các chức năng chính

### 1. Tạo database Chroma từ tài liệu (index dữ liệu)

Chạy lệnh sau để nạp dữ liệu PDF và TXT vào ChromaDB:

```bash
python core/fill_db.py
```

### 2. Chatbot Gemini CLI (hỏi đáp trực tiếp với Gemini)

Chạy chatbot CLI với Gemini:

```bash
python core/scripts/rag_qa.py
```

Sau đó nhập câu hỏi, nhấn Enter để nhận câu trả lời.

### 3. Test chatbot Gemini CLI (bản test)

```bash
python test/gemini_cli.py
```

## Lưu ý

- Thư mục `chroma_db/` sẽ được tạo tự động để lưu trữ dữ liệu đã index, không cần push lên GitHub.
- Nếu gặp lỗi về model Gemini, hãy xem tên model khả dụng khi chạy script và sửa lại tên model trong code cho phù hợp.
- Đảm bảo các file dữ liệu (PDF, TXT) nằm trong `core/data/`.

## Bỏ qua các file/thư mục không cần thiết khi push

Đã cấu hình `.gitignore` để loại trừ `chroma_db/` và `frontend/node_modules/`.

---

Nếu có vấn đề, hãy kiểm tra lại API key, đường dẫn dữ liệu, hoặc liên hệ người phát triển: nqt.code@gmail.com
