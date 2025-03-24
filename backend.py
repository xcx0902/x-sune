import random
import json
from datetime import datetime, timedelta, timezone

import sqlite3
import openai
import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = json.loads(open("config.json", "r", encoding="utf-8").read())

MODELS = config["models"]
CATEGORY = config["category"]
SYSTEM_PROMPT = config["system_prompt"]
SECRET_KEY = config["secret_key"]

class User(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    user: str
    token: str
    message: str
    history: list[dict]

class Token(BaseModel):
    username: str
    token: str

def get_db():
    """Get database connection and cursor"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    return conn, cursor

@app.get("/ping")
def ping():
    """Ping the server"""
    return {"message": "pong"}

@app.post("/register")
def register(user: User) -> dict:
    """Register a new user"""
    conn, cursor = get_db()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail="用户名已存在") from e
    finally:
        conn.close()
    return {"message": "注册成功"}

@app.post("/token")
def login(user: User) -> dict:
    """Login and return JWT token"""
    conn, cursor = get_db()
    try:
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
        if cursor.fetchone():
            payload = {
                "sub": user.username,
                "exp": (datetime.now(timezone.utc) + timedelta(days=15)).timestamp()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return {"access_token": token}
        else:
            raise HTTPException(status_code=400, detail="用户名或密码错误")
    finally:
        conn.close()

def save_chat(username: str, role: str, content: str) -> None:
    """Save user's chat history into database"""
    conn, cursor = get_db()
    try:
        cursor.execute("INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)", (username, role, content))
        conn.commit()
    finally:
        conn.close()

def decode_token(token: str) -> dict:
    """Decode JWT token and return status"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if datetime.now(timezone.utc).timestamp() > payload["exp"]:
            return {"status": "expired"}
        return {"status": "ok", "username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return {"status": "expired"}
    except jwt.InvalidTokenError:
        return {"status": "invalid"}

@app.post("/check_token")
def check_token(token: Token) -> str:
    """Check if the token is valid"""
    result = decode_token(token.token)
    if result["status"] != "ok":
        raise HTTPException(status_code=401, detail=result["status"])
    if result["username"] != token.username:
        raise HTTPException(status_code=401, detail="invalid")
    return "ok"

@app.websocket("/ws/chat")
async def chat_stream(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    try:
        while True:
            data: dict = await websocket.receive_json()
            username = data.get("username")
            token = data.get("token")
            message = data.get("message")
            history = data.get("history", [])
            model = data.get("model", "fast")
            auth = decode_token(token)
            if auth["status"] != "ok":
                await websocket.send_text("<" + auth["status"].upper() + ">")
                continue
            if auth["username"] != username:
                await websocket.send_text("<INVALID>")
                continue
            model_id = random.choice(CATEGORY[model])
            model_info: dict = MODELS[model_id]
            await websocket.send_text(model_info["name"])
            try:
                response = openai.OpenAI(
                    api_key=model_info["api_key"],
                    base_url=model_info["url"],
                    default_headers={
                        "User-Agent": model_info.get("user_agent", ""),
                        "Cookie": model_info.get("cookie", "")
                    }
                ).chat.completions.create(
                    model=model_info["name"],
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}],
                    stream=True,
                    extra_body={"incremental_output": True} # Adapted for Qwen
                )
            except Exception as e:
                await websocket.send_text(f"{type(e).__name__}: {e}")
                await websocket.send_text("<RESPONSE ENDED>")
                continue
            assistant_message = ""
            first_token = True
            for chunk in response:
                text = chunk.choices[0].delta.content
                if text:
                    if first_token and text == "\n\n": # Adapted for SiliconFlow
                        continue
                    first_token = False
                    assistant_message += text
                    await websocket.send_text(text)
            await websocket.send_text("<RESPONSE ENDED>")
            save_chat(username, "user", message)
            save_chat(username, "assistant", assistant_message)
    except WebSocketDisconnect:
        return
