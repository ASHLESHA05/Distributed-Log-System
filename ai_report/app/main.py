# ai_report/app/main.py
from fastapi import FastAPI
from routers import ai_api
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "AI Report Service"))

app.include_router(ai_api.router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=int(os.getenv("APP_PORT", 8500)),
                reload=True)
