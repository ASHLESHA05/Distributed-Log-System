from fastapi import APIRouter
import asyncio
from datetime import datetime

router = APIRouter(prefix="/simulate", tags=["Simulation"])

SERVICES = [
    "Log Producer",
    "Kafka Queue",
    "Backend Processor",
    "AI Reporter",
    "Dashboard Uploader"
]

@router.get("/flow")
async def simulate_flow():
    sequence = []
    for service in SERVICES:
        await asyncio.sleep(0.8)  # mimic delay
        sequence.append({
            "service": service,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "status": "ok"
        })
    return {"sequence": sequence, "message": "Simulation completed!"}
