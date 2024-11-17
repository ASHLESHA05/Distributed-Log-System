import random
import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from log_accumulator import Logger1

node_id = str(uuid.uuid4())
logs = None
heart_beat_status = ['UP', 'DOWN']

log_messages = {
    "INFO": [
        "ShippingService started successfully",
        "Order shipped successfully",
        "Tracking number generated",
        "Shipping address verified",
        "Delivery date updated",
    ],
    "WARN": [
        "Delayed shipment warning",
        "Incomplete shipping address detected",
        "Carrier response delay",
        "High shipment volume warning",
        "Unauthorized access attempt",
    ],
    "ERROR": [
        {
            "error_code": "SHIP001",
            "error_message": "Failed to generate tracking number"
        },
        {
            "error_code": "SHIP002",
            "error_message": "Carrier service unavailable"
        },
        {
            "error_code": "SHIP003",
            "error_message": "Invalid shipping address"
        },
        {
            "error_code": "SHIP004",
            "error_message": "Shipment lost in transit"
        },
        {
            "error_code": "SHIP005",
            "error_message": "Unexpected server error in ShippingService"
        }
    ]
}

async def registration():
    IST = timezone(timedelta(hours=5, minutes=30))
    data = {
        "node_id": node_id,
        "message_type": "REGISTRATION",
        "service_name": 'Shipping_Service',
        "timestamp": datetime.now(IST).isoformat()
    }
    Logger1(reg=data)

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
        Logger1(heartbeat=heartbeat_message)
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
                "service_name": "Shipping_Service",
                "timestamp": date
            }
        elif generated_log == 'WARN':
            logs = {
                "log_id": id,
                "node_id": node_id,
                "log_level": "WARN",
                "message_type": "LOG",
                "message": getmessage(generated_log),
                "service_name": "Shipping_Service",
                "response_time_ms": random.randint(50, 500),
                "threshold_limit_ms": 400,
                "timestamp": date
            }
        elif generated_log == 'ERROR':
            logs = {
                "log_id": id,
                "node_id": node_id,
                "log_level": "ERROR",
                "message_type": "LOG",
                "message": getmessage(generated_log)['error_message'],
                "service_name": "Shipping_Service",
                "error_details": {
                    "error_code": getmessage(generated_log)['error_code'],
                    "error_message": getmessage(generated_log)['error_message']
                },
                "timestamp": date
            }
        else:
            logs = None

        Logger1(logs=logs)
        await asyncio.sleep(random.uniform(0.1, 1.0))

async def main():
    await registration()
    await asyncio.gather(print_heartbeat(), generate_logs())

asyncio.run(main())
