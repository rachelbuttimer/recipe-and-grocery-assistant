import os
from dotenv import load_dotenv
from google import genai

# load api key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables or .env file")

# ping Gemini API to test baseline connectivity
client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="respond with 'API connection successful!' and nothing else",
)

print("Status:", response.text.strip())