from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

app = FastAPI()

# Дозволити запити з фронтенду Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://matches12.netlify.app/"],  # заміни на домен Mini App для безпеки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-subscription")
async def check_subscription(request: Request):
    data = await request.json()
    user_id = data.get("user_id")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {
        "chat_id": f"@{CHANNEL_USERNAME}",
        "user_id": user_id
    }

    try:
        response = requests.get(url, params=params).json()
        status = response.get("result", {}).get("status", "")
        subscribed = status in ["member", "administrator", "creator"]
        return {"subscribed": subscribed}
    except Exception as e:
        return {"subscribed": False, "error": str(e)}
