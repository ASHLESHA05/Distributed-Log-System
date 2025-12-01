import aio_pika
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class HeartbeatMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rabbit_url="amqp://guest:guest@localhost/"):
        super().__init__(app)
        self.rabbit_url = rabbit_url
        self.exchange_name = "sim-heartBeat"
        self.connection = None
        self.channel = None
        self.exchange = None

    async def setup(self):
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.rabbit_url)
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.FANOUT
            )

    async def dispatch(self, request: Request, call_next):
        await self.setup()

        await self.exchange.publish(
            aio_pika.Message(body=b"HEARTBEAT"),
            routing_key=""
        )

        return await call_next(request)
