"""
Simple script to list all available Gemini models for your API key
Run this to see which models you can use
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found!")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("=" * 60)
print("Available Gemini Models for your API key:")
print("=" * 60)

# List all available models
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"✓ {m.name}")

print("=" * 60)