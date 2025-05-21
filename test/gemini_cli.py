import google.generativeai as genai
import os
from dotenv import load_dotenv

def main():
    print("== List model khả dụng với key hiện tại:")
    # Nên cho list model sau khi đã configure key!
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = input("Nhập Gemini API Key: ").strip()
        if not api_key:
            print("Bạn chưa cung cấp Gemini API Key! Thoát.")
            return
    genai.configure(api_key=api_key)

    for m in genai.list_models():
        print(m.name)

    print("==== Gemini Chatbot CLI ====")
    # Model tốt hiện tại, flash cực nhanh
    model_name = "models/gemini-2.0-flash"   # Không có dấu phẩy!
    try:
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        print("Không thể khởi tạo model Gemini:", e)
        return
    # Chat loop
    while True:
        question = input("\nBạn hỏi gì? (Enter để thoát): ")
        if not question.strip():
            print("Tạm biệt!")
            break
        try:
            response = model.generate_content(question)
            print("\nGemini:", response.text.strip())
        except Exception as e:
            print("Lỗi khi gọi Gemini API:", e)
        print("-" * 40)

if __name__ == "__main__":
    main()
# Chạy thử với model Gemini 2.0 Flash
# python3 test/gemini_cli.py                                                                        