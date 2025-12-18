import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

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
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash') # Updated to available model
else:
    model = None

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
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured.")

    user_msg = request.message
    
    # Construct the full prompt with history
    # Note: Gemini 1.5 Flash supports system instructions better, but for simple use:
    # We'll prepend the system prompt to the chat session or just send it as context.
    
    chat_history = []
    # Add system prompt as the first part of the context (or use system_instruction if using that API version)
    # For simplicity with the standard generate_content, we'll just prepend context to the latest message 
    # or keep a running history.
    
    # Let's use a simple approach: Send context + history + current message.
    
    # Format history for the model
    gemini_history = []
    for msg in request.history:
        role = "user" if msg.role == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg.content]})
    
    # Start a chat session
    chat = model.start_chat(history=gemini_history)
    
    # Send the message with the system prompt context (injected into the message for this turn to ensure it's fresh)
    # Alternatively, we could have set it at the start. 
    # Let's try sending the system prompt + user message combined for the current turn if history is empty,
    # or just rely on the model's ability to handle the context if we inject it.
    
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_msg}"
    
    try:
        response = chat.send_message(full_prompt)
        text_response = response.text
        
        action = None
        if "[CONTACT_PAGE]" in text_response:
            action = "contact_support"
            text_response = text_response.replace("[CONTACT_PAGE]", "").strip()
            
        return ChatResponse(response=text_response, action=action)
        
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
