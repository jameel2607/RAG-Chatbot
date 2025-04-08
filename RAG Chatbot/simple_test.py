# simple_test.py
print("Starting test...")
import os
from dotenv import load_dotenv

print("Imports successful")
load_dotenv()

print(f"Current directory: {os.getcwd()}")
print(f"API Key exists: {'GOOGLE_API_KEY' in os.environ}")
print(f"API Key value: {os.getenv('GOOGLE_API_KEY')}")
print("Test complete")