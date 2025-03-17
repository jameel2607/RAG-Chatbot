import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def test_gemini():
    try:
        # Configure the library
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # List available models
        models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print("Available models:", models)
        
        # Test a simple generation
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello!")
        print("Response:", response.text)
        
        print("✅ Gemini API is working!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_gemini()