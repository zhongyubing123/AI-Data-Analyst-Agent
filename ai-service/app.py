from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.agent_service import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "AI Agent Running"}


@app.post("/chat")
def chat(req: ChatRequest):
    return run_agent(req.message)