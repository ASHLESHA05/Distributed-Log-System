import random
import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from logger_accumulator import FluentdLogger

node_id = str(uuid.uuid4())
heart_beat_status = ['UP', 'DOWN']

log_messages = {
    "INFO": [
        "OrderService started successfully",
        "Order placed successfully",
        "Order payment verified",
        "Inventory checked and updated",
        "Shipping process initiated",
    ],
    "WARN": [
        "Inventory low for product",
        "Order processing delayed",
        "Third-party shipping service timeout",
        "Slow response from inventory system",
        "Customer address verification issue",
    ],
    "ERROR": [
        {
            "error_code": "ERR101",
            "error_message": "Order placement failed"
        },
        {
            "error_code": "ERR102",
            "error_message": "Inventory check failed"
        },
        {
            "error_code": "ERR103",
            "error_message": "Payment verification failed"
        },
        {
            "error_code": "ERR104",
            "error_message": "Shipping process failed"
        },
        {
            "error_code": "ERR105",
            "error_message": "Unexpected error in order workflow"
        }
    ]
}

logger = FluentdLogger(tag="order_service")

async def registration():
    IST = timezone(timedelta(hours=5, minutes=30))
    data = {
        "node_id": node_id,
        "message_type": "REGISTRATION",
        "service_name": 'Order_Service',
        "timestamp": datetime.now(IST).isoformat()
    }
    logger.add_registration(data)

async def generate_log():
    IST = timezone(timedelta(hours=5, minutes=30))
    return random.choice(['INFO', 'WARN', 'ERROR']), str(uuid.uuid4()), datetime.now(IST).isoformat()

async def print_heartbeat():
    while True:
        IST = timezone(timedelta(hours=5, minutes=30))
        heartbeat_message = {
            "node_id": node_id,
            "message_type": "HEARTBEAT",
            "status": random.choice(heart_beat_status),
            "timestamp": datetime.now(IST).isoformat()
        }
        logger.add_heartbeat(heartbeat_message)
        await asyncio.sleep(5)  

def getmessage(log_level):
    return random.choice(log_messages[log_level])

async def generate_logs():
    while True:
        generated_log, id, date = await generate_log()
        if generated_log == 'INFO':
            logs = {
                "log_id": id,
                "node_id": node_id,
                "log_level": "INFO",
                "message_type": "LOG",
                "message": getmessage(generated_log),
                "service_name": "Order_Service",
                "timestamp": date
            }
        elif generated_log == 'WARN':
            logs = {
                "log_id": id,
                "node_id": node_id,
                "log_level": "WARN",
                "message_type": "LOG",
                "message": getmessage(generated_log),
                "service_name": "Order_Service",
                "response_time_ms": random.randint(10, 100),
                "threshold_limit_ms": 100,
                "timestamp": date
            }
        elif generated_log == 'ERROR':
            message = getmessage(generated_log)
            logs = {
                "log_id": id,
                "node_id": node_id,
                "log_level": "ERROR",
                "message_type": "LOG",
                "message": message['error_message'],
                "service_name": "Order_Service",
                "error_details": {
                    "error_code": message['error_code'],
                    "error_message": message['error_message']
                },
                "timestamp": date
            }
        else:
            logs = None

        if logs:
            logger.add_log(logs)
        await asyncio.sleep(random.uniform(0.1, 1.0))  

async def main():
    await registration()
    await asyncio.gather(print_heartbeat(), generate_logs())

asyncio.run(main())


logger.close()