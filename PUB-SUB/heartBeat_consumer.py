from aiokafka import AIOKafkaConsumer
from datetime import datetime
import json
import asyncio

EXPECTED_INTERVAL = 5  # Expected interval between heartbeats in seconds

class Heartbeat:
    def __init__(self):
        self.heart_beat = {}  # Dictionary to track heartbeat statuses and timestamps
        self.consumer = None  # Kafka consumer attribute of the class

    async def start_consumer(self):
        """Initialize and start the Kafka consumer for heartbeat messages."""
        loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            'heartbeat',  # Topic name
            loop=loop,
            bootstrap_servers='localhost:9092',
            group_id='heartbeat-consumer-group',
            auto_offset_reset='earliest'  # Start reading messages from the earliest
        )
        await self.consumer.start()  # Start the Kafka consumer
        print("Heartbeat consumer started...")

    async def check_heart_beat(self, msg):
        """
        Check the incoming heartbeat message and perform actions 
        based on node status, interval, and service restarts.
        """
        node_id = msg['node_id']
        status = msg['status']
        timestamp = msg['timestamp']

        # If node is seen for the first time, store its status and timestamp
        if node_id not in self.heart_beat:
            self.heart_beat[node_id] = {'status': status, 'timestamp': timestamp}
            print(f"First Incoming heartbeat from {node_id}, timestamp: {timestamp}")
            return True

        # Handle if node shuts down gracefully
        if status == 'DOWN':
            print(f"ALERT!! {node_id} shut down gracefully")
            self.heart_beat[node_id]['status'] = 'DOWN'
            self.heart_beat[node_id]['timestamp'] = timestamp  # Update timestamp
            return True

        # Handle service restart or status change
        if status != self.heart_beat[node_id]['status']:
            print(f"Service with node id: {node_id} Restarted")
            self.heart_beat[node_id]['status'] = 'UP'  # Update status to 'UP'
            return True

        # Calculate the time interval between the previous and current heartbeat
        previous_time = datetime.fromisoformat(self.heart_beat[node_id]['timestamp'])
        current_time = datetime.fromisoformat(timestamp)
        actual_interval = (current_time - previous_time).total_seconds()
        actual_interval_rounded = round(actual_interval, 2)

        # Check if the interval exceeds the expected interval
        if actual_interval_rounded > EXPECTED_INTERVAL:
            print(f"ALERT: Delay detected for {node_id}! Interval: {actual_interval_rounded} seconds")
        else:
            print(f"{node_id} : UP")

        # Update the heartbeat timestamp for the node
        self.heart_beat[node_id]['timestamp'] = timestamp
        return False

    async def consume_heartbeat(self):
        """Consume heartbeat messages from the Kafka topic."""
        print("Consuming heartbeat messages...")
        try:
            async for msg in self.consumer:
                msg_value = msg.value.decode('utf-8')  # Decode the Kafka message
                msg_dict = json.loads(msg_value)  # Convert message to a dictionary
                await self.check_heart_beat(msg_dict)  # Check and process the heartbeat
        except KeyboardInterrupt:
            print("\nShutting down heartbeat consumer...")
        finally:
            # Ensure Kafka consumer is stopped gracefully
            await self.consumer.stop()
            print("Heartbeat consumer stopped.")



# from aiokafka import AIOKafkaConsumer
# from datetime import datetime
# import json
# import asyncio

# EXPECTED_INTERVAL = 5

# class Heartbeat:
#     def __init__(self):
#         self.heart_beat = {}

#     async def check_heart_beat(self, msg):
#         if msg['node_id'] not in self.heart_beat:
#             self.heart_beat[msg['node_id']] = {'status': msg['status'], 'timestamp': msg['timestamp']}
#             print(f"First Incoming from {msg['node_id']}, timestamp: {msg['timestamp']}")
#             return True
        
#         if msg['status'] == 'DOWN':
#             print(f"ALERT!! {msg['node_id']} shut down gracefully")
#             self.heart_beat[msg['node_id']]['status'] = 'DOWN'
#             return True

#         if msg['status'] != self.heart_beat[msg['node_id']]['status']:
#             print(f"Service with node id: {msg['node_id']} Restarted")
#             self.heart_beat[msg['node_id']]['status'] = 'UP'
#             return True
        
#         previous_time = datetime.fromisoformat(self.heart_beat[msg['node_id']]['timestamp'])
#         current_time = datetime.fromisoformat(msg['timestamp'])
#         actual_interval = (current_time - previous_time).total_seconds()
#         actual_interval_rounded = round(actual_interval, 2)

#         if actual_interval_rounded > EXPECTED_INTERVAL:
#             print(f"ALERT: Delay detected! Interval: {actual_interval_rounded} seconds")
#         else:
#             print(f"{msg['node_id']} : UP")
            
#         self.heart_beat[msg['node_id']]['timestamp'] = msg['timestamp']
#         return False

#     async def consume_heartbeat(self):
#         consumer = AIOKafkaConsumer(
#             'heartbeat',  # Topic name
#             loop=asyncio.get_event_loop(),
#             bootstrap_servers='localhost:9092',
#             group_id='heartbeat-consumer-group',
#             auto_offset_reset='earliest'
#         )

#         await consumer.start()

#         print("Consuming messages from topic 'heartbeat'...")

#         try:
#             async for msg in consumer:
#                 msg_value = msg.value.decode('utf-8')
#                 msg_dict = json.loads(msg_value)
#                 await self.check_heart_beat(msg_dict)

#         except KeyboardInterrupt:
#             print("\nShutting down heartbeat consumer...")

#         finally:
#             await consumer.stop()

