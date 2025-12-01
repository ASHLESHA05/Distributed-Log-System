from fastapi import FastAPI, WebSocket
from app.components.logger.logger import MyLogger
from app.components.services.service import ServiceSimulation
from app.middleware.heartbeat_middleware import HeartbeatMiddleware
from app.routers import heartbeat
import asyncio
import uvicorn

app = FastAPI(title="Distributed Log Simulator")
logger = MyLogger("Main")

clients = set()

async def broadcast(message: str):
    for ws in list(clients):
        try:
            await ws.send_text(message)
        except:
            clients.remove(ws)


@app.on_event("startup")
async def startup():
    logger.info("Simulation backend started")


# ROUTERS
app.add_middleware(HeartbeatMiddleware)
app.include_router(heartbeat.router)


# ---------------- API ENDPOINTS ----------------
@app.post("/api/sim/success")
async def sim_success():
    msg = ServiceSimulation("ServiceA").success_log()
    await broadcast(msg)
    return {"status": "ok"}

@app.post("/api/sim/warn")
async def sim_warn():
    msg = ServiceSimulation("ServiceA").warn_logs()
    await broadcast(msg)
    return {"status": "ok"}

@app.post("/api/sim/error")
async def sim_error():
    msg = ServiceSimulation("ServiceA").error_log()
    await broadcast(msg)
    return {"status": "ok"}

@app.post("/api/sim/debug")
async def sim_debug():
    msg = ServiceSimulation("ServiceA").debug_log()
    await broadcast(msg)
    return {"status": "ok"}

@app.post("/api/sim/failover")
async def failover():
    msg = "[FAILOVER] Node switched to backup node"
    await broadcast(msg)
    return {"status": "failover-triggered"}


# ---------------- WEBSOCKET ----------------
@app.websocket("/ws/logs")
async def logs_ws(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    await ws.send_text("WebSocket connected")

    try:
        while True:
            await asyncio.sleep(1)
    except:
        pass
    finally:
        clients.remove(ws)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
