from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.agent_service import run_agent
from services import dashboard_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
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


# ---- 看板：原来在 Spring Boot 里，现在同一套服务提供 ----

@app.get("/api/brand/sales")
def brand_sales():
    return dashboard_service.brand_sales()


@app.get("/api/category/sales")
def category_sales():
    return dashboard_service.category_sales()


@app.get("/api/item/hot")
def item_hot():
    return dashboard_service.item_hot()


@app.get("/api/user/active")
def user_active():
    return dashboard_service.user_active()
