# test_gemini_chat.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

print("1. Starting test...")
load_dotenv()

try:
    print("2. Configuring Gemini...")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    print("3. Creating model...")
    model = genai.GenerativeModel('gemini-pro')
    
    print("4. Testing generation...")
    response = model.generate_content("Say hello!")
    
    print("5. Response from Gemini:", response.text)
    print("\n✅ Everything is working perfectly!")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")