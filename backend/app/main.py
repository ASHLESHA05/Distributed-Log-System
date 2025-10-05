# backend/app/main.py
from fastapi import FastAPI
from routers import logs, anomalies, reports
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "Distributed Backend"))

app.include_router(logs.router)
app.include_router(anomalies.router)
app.include_router(reports.router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=int(os.getenv("APP_PORT", 8000)),
                reload=bool(os.getenv("DEBUG", True)))
