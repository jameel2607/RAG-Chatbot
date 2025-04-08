from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def test_openai_api():
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        # Try a simple API call
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input="Hello world"
        )
        print("✅ API key is working!")
        return True
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

if __name__ == "__main__":
    test_openai_api()