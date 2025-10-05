# backend/app/services/heartbeat_service.py
import aio_pika, asyncio, json

async def send_heartbeat():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    exchange = await channel.declare_exchange("heartbeats", aio_pika.ExchangeType.FANOUT)
    
    msg = {"service": "backend", "status": "alive"}
    await exchange.publish(aio_pika.Message(body=json.dumps(msg).encode()), routing_key="")
    await connection.close()
