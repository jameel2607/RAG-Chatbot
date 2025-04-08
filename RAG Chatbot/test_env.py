# test_env.py
from dotenv import load_dotenv
import os
import sys

print("1. Starting script...")

# Print Python version and working directory
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Check if .env file exists
env_path = os.path.join(os.getcwd(), '.env')
print(f"2. Checking .env file at: {env_path}")
print(f"3. .env file exists: {os.path.exists(env_path)}")

# Try to load .env
print("4. Attempting to load .env...")
load_dotenv()
print("5. load_dotenv() completed")

# Check if key exists
api_key = os.getenv('OPENAI_API_KEY')
print(f"6. API Key exists: {api_key is not None}")
print(f"7. API Key length: {len(api_key) if api_key else 0}")

# Print first few characters if key exists
if api_key:
    print(f"8. API Key starts with: {api_key[:7]}...")
else:
    print("8. No API key found!")