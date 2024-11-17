from aiokafka import AIOKafkaConsumer
from datetime import datetime
import json
import asyncio

EXPECTED_INTERVAL = 5

class Heartbeat:
    def __init__(self):
        self.heart_beat = {}

    async def check_heart_beat(self, msg):
        if msg['node_id'] not in self.heart_beat:
            self.heart_beat[msg['node_id']] = {'status': msg['status'], 'timestamp': msg['timestamp']}
            print(f"First Incoming from {msg['node_id']}, timestamp: {msg['timestamp']}")
            return True
        
        if msg['status'] == 'DOWN':
            print(f"ALERT!! {msg['node_id']} shut down gracefully")
            self.heart_beat[msg['node_id']]['status'] = 'DOWN'
            return True

        if msg['status'] != self.heart_beat[msg['node_id']]['status']:
            print(f"Service with node id: {msg['node_id']} Restarted")
            self.heart_beat[msg['node_id']]['status'] = 'UP'
            return True
        
        previous_time = datetime.fromisoformat(self.heart_beat[msg['node_id']]['timestamp'])
        current_time = datetime.fromisoformat(msg['timestamp'])
        actual_interval = (current_time - previous_time).total_seconds()
        actual_interval_rounded = round(actual_interval, 2)

        if actual_interval_rounded > EXPECTED_INTERVAL:
            print(f"ALERT: Delay detected! Interval: {actual_interval_rounded} seconds")
        else:
            print(f"{msg['node_id']} : UP")
            
        self.heart_beat[msg['node_id']]['timestamp'] = msg['timestamp']
        return False

    async def consume_heartbeat(self):
        consumer = AIOKafkaConsumer(
            'heartbeat',  # Topic name
            loop=asyncio.get_event_loop(),
            bootstrap_servers='localhost:9092',
            group_id='heartbeat-consumer-group',
            auto_offset_reset='earliest'
        )

        await consumer.start()

        print("Consuming messages from topic 'heartbeat'...")

        try:
            async for msg in consumer:
                msg_value = msg.value.decode('utf-8')
                msg_dict = json.loads(msg_value)
                await self.check_heart_beat(msg_dict)

        except KeyboardInterrupt:
            print("\nShutting down heartbeat consumer...")

        finally:
            await consumer.stop()

