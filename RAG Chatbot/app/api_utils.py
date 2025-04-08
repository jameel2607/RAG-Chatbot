import requests
import streamlit as st
import json
from typing import List
import os

# API endpoint
API_URL = "http://127.0.0.1:8000"

def chat_with_bot(question: str, model: str, session_id: str) -> str:
    """Send a chat request to the API"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "question": question,
                "session_id": session_id,
                "model": model
            }
        )
        if response.status_code == 200:
            return response.json()["answer"]
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Error connecting to API: {str(e)}"

def upload_document(file) -> bool:
    """Upload a document to the API"""
    try:
        # Print debug information
        print(f"Uploading file: {file.name}")
        
        # Create the files dictionary with the correct format
        files = {
            "file": (
                file.name,
                file.getvalue(),
                "application/octet-stream"
            )
        }
        
        # Make the request
        response = requests.post(
            f"{API_URL}/upload-doc",
            files=files
        )
        
        # Print response for debugging
        print(f"Upload response status: {response.status_code}")
        print(f"Upload response text: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return False

def get_documents():
    """Get list of uploaded documents"""
    try:
        response = requests.get(f"{API_URL}/list-docs")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def delete_document(doc_id: int) -> bool:
    """Delete a document"""
    try:
        response = requests.post(
            f"{API_URL}/delete-doc",
            json={"file_id": doc_id}
        )
        return response.status_code == 200
    except Exception:
        return False