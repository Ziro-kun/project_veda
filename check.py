# check.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("--- 사용 가능한 모델 목록 ---")
try:
    for m in genai.list_models():
        # 이미지를 읽을 수 있는(vision) 모델만 찾기
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"오류 발생: {e}")