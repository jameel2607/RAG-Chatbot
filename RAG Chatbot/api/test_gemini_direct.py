import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini():
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # List available models
        print("Available models:")
        for m in genai.list_models():
            print(m.name)
        
        # Test the model with correct name
        model = genai.GenerativeModel('models/gemini-1.5-pro')  # Updated model name
        response = model.generate_content("Hello, how are you?")
        print("\nResponse:", response.text)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini() 