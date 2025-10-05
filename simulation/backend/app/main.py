from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import simulate

app = FastAPI(title="Simulation Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulate.router)

@app.get("/")
def root():
    return {"message": "Simulation backend is running"}
