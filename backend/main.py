import os
from typing import List, Optional

import google.genai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.api_core.exceptions import ResourceExhausted
from pydantic import BaseModel
from google.genai import types as genai_types

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Ideally, this should be in an .env file.
# For now, we'll try to get it from the environment or use a placeholder.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")
    # You might want to hardcode it for testing IF SAFE, or ask the user.
    # For this code to work, the user MUST provide a key.

app = FastAPI(title="Ava Chatbot Backend")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development (localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Loading ---
COMPANY_INFO = ""
try:
    with open("backend/data/company_info.txt", "r") as f:
        COMPANY_INFO = f.read()
    print("Loaded company info.")
except FileNotFoundError:
    print("WARNING: company_info.txt not found. Run scraper first.")
    COMPANY_INFO = "Tars Group is a technology company. (Default placeholder)"

# --- Gemini Setup ---
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# --- Models ---
class ChatMessage(BaseModel):
    role: str # "user" or "model"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    action: Optional[str] = None # e.g., "contact_support"

# --- System Prompt ---
SYSTEM_PROMPT = f"""
You are Ava, the AI assistant for Tars Group.
Your persona is professional, helpful, and efficient, similar to TARS from Interstellar but warmer.
You are here to help users understand Tars Group's services and offerings.

Context about Tars Group:
{COMPANY_INFO}

Guidelines:
1. Answer questions based on the context provided.
2. If you don't know the answer, politely say so and offer to connect them with support.
3. If the user expresses an intent to contact support, sales, or get in touch, provide a helpful response AND set the 'action' flag to 'contact_support' in your internal reasoning (though here you just output text, we will handle the flag logic separately or you can explicitly say "[CONTACT_PAGE]" to trigger it).
4. Be concise.

Special Instruction for Contact:
If the user asks to contact someone, output the token [CONTACT_PAGE] at the end of your message.
"""

# --- Routes ---
@app.get("/")
async def root():
    return {"message": "Ava Chatbot Backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured.")

    user_msg = request.message

    # Build conversation context for the Gemini API
    contents = [genai_types.Content(role="user", parts=[SYSTEM_PROMPT])]

    for msg in request.history:
        role = "user" if msg.role == "user" else "model"
        contents.append(genai_types.Content(role=role, parts=[msg.content]))

    contents.append(genai_types.Content(role="user", parts=[user_msg]))

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )

        text_response = response.text

        action = None
        if "[CONTACT_PAGE]" in text_response:
            action = "contact_support"
            text_response = text_response.replace("[CONTACT_PAGE]", "").strip()

        return ChatResponse(response=text_response, action=action)

    except ResourceExhausted as e:
        # Surface quota/rate limit errors clearly to the client
        raise HTTPException(status_code=429, detail="Gemini quota exceeded. Please wait and try again." ) from e
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
