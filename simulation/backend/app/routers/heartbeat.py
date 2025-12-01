from fastapi import APIRouter
import aio_pika
import asyncio

router = APIRouter()

RABBIT = "amqp://guest:guest@localhost/"
EXCHANGE = "sim-heartBeat"

async def send_interrupt():
    conn = await aio_pika.connect_robust(RABBIT)
    channel = await conn.channel()
    exch = await channel.declare_exchange(EXCHANGE, aio_pika.ExchangeType.FANOUT)

    await exch.publish(
        aio_pika.Message(body=b"HEARTBEAT_INTERRUPT"),
        routing_key=""
    )

    await conn.close()


@router.post("/heartbeat/interrupt")
async def interrupt():
    asyncio.create_task(send_interrupt())
    return {"status": "interrupt-sent"}
