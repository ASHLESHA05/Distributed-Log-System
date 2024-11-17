import asyncio
from aiokafka import AIOKafkaConsumer
import json
from termcolor import colored
import os

async def put_to_elasticSearch(msg):
    # Asynchronous function to put logs to Elasticsearch
    pass

async def classify_logs(msg):
    await put_to_elasticSearch(msg)
    
    if msg['message_type'] == 'REGISTRATION':
        message = f"Node ID: {msg['node_id']} , service_name: {msg['service_name']}  REGISTERED SUCCESSFULLY"
        print(colored(message, 'green', attrs=['bold']))
        return
    if msg['message_type'] == 'LOG':
        if msg['log_level'] == 'INFO':
            print(f"\033[96mINFO: | node_id: {msg['node_id']} | log_id: {msg['log_id']} | service_name: {msg['service_name']} | message: {msg['message']}\033[0m")
        elif msg['log_level'] == 'WARN':
            print(f'\033[38;5;214m WARNING!! node_id: {msg["node_id"]} | log_id: {msg["log_id"]} | service_name: {msg["service_name"]} | message: {msg["message"]} \033[0m')
        else:
            print(f'\033[91m ERROR!! node_id: {msg["node_id"]} | log_id: {msg["log_id"]} | service_name: {msg["service_name"]} | message: {msg["message"]} | ERROR CODE: {msg["error_details"]["error_code"]} \033[0m')
    elif msg['message_type'] == 'CLOSE_LOG':
        terminal_width = os.get_terminal_size().columns
        message = f": |{msg['service_name']} SHUTDOWN Gracefully!! node_id: {msg['node_id']} | log_id: {msg['log_id']} | {msg['timestamp']}"
        centered_message = message.center(terminal_width)
        print(colored(centered_message, 'blue', attrs=['bold']))

async def main():
    consumer = AIOKafkaConsumer(
        'logs',
        bootstrap_servers='localhost:9092',
        group_id='logs-consumer-group',
        auto_offset_reset='latest'
    )
    await consumer.start()
    try:
        print("Logs consumer started... Press Ctrl+C to stop.")
        async for msg in consumer:
            if msg.value:
                msg = json.loads(msg.value.decode('utf-8'))
                await classify_logs(msg)
            else:
                print("Received empty message.")
    except KeyboardInterrupt:
        # Catching keyboard interrupt to gracefully stop the consumer
        print("Stopping logs consumer...")
    except asyncio.CancelledError:
        # Handle cancellation explicitly
        print("Consumer task was canceled.")
    finally:
        await consumer.stop()
        print("Logs consumer stopped.")

if __name__ == "__main__":
    asyncio.run(main())
