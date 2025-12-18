# Ava Chatbot Project

This project consists of a FastAPI backend and a React frontend.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API Key

## Setup & Running

### 1. Backend (FastAPI)

Navigate to the root directory:

```bash
cd backend
```

Install dependencies (if not already done):
```bash
pip install -r requirements.txt
```

**IMPORTANT**: Set up your environment variables.

Create a `.env` file in the `backend` directory by copying the example:
```bash
cp .env.example .env
```

Then edit `.env` and add your Gemini API Key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

**Alternative**: You can also export the API key directly:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Start the server:
```bash
uvicorn main:app --reload --port 8000
```
The backend will run at `http://localhost:8000`.

### 2. Frontend (React)

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies (if not already done):
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
The frontend will run at `http://localhost:3000`.

## Features
- **Ava Persona**: Professional and helpful.
- **Knowledge Base**: Scraped from Tars Group website.
- **Contact Redirection**: Detects intents to contact support and provides a link.


The two simple commands to run the project are:
```bash
# Start the FastAPI backend (listens on http://localhost:8000)
uvicorn backend.main:app --reload --port 8000
# Start the Vite‑React frontend (listens on http://localhost:3000)
cd frontend && npm run dev
```