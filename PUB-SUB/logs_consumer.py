from confluent_kafka import Consumer
import json
import os
from termcolor import colored


def put_to_elasticSearch(msg):
    print("Added to elastic search: ", msg)

def classify_logs(msg):
    put_to_elasticSearch(msg)
    
    if msg['message_type'] == 'REGISTRATION':
        message = f"Node ID: {msg['node_id']} , service_name: {msg['service_name']}  REGISTERED SUCCESSFULLY"
        print(colored(message, 'green', attrs=['bold']))
        return
    if msg['message_type'] == 'LOG':
        if msg['log_level'] == 'INFO':
            print(f"\033[96mINFO: | node_id: {msg['node_id']} | log_id: {msg['log_id']} | service_name: {msg['service_name']} | message: {msg['message']}\033[0m")
        elif msg['log_level'] == 'WARN':
            print(f'\033[38;5;214m WARNING!! node_id: {msg["node_id"]} | log_id: {msg['log_id']} | service_name: {msg["service_name"]} | message: {msg["message"]} \033[0m')
        else:
            print(f'\033[91m ERROR!! node_id: {msg["node_id"]} | log_id: {msg['log_id']} | service_name: {msg["service_name"]} | message: {msg["message"]} | ERROR CODE: {msg["error_details"]["error_code"]} \033[0m')
    elif msg['message_type']=='CLOSE_LOG':
        terminal_width = os.get_terminal_size().columns
        
        # Your message
        message = f": |{msg['service_name']} SHUTDOWN Gracefully!! node_id: {msg['node_id']} | log_id: {msg['log_id']} | {msg['timestamp']}"
        centered_message = message.center(terminal_width)
        print(colored(centered_message, 'blue', attrs=['bold']))
            

def main():
    consumer_config = {
        'bootstrap.servers': 'localhost:9092', 
        'group.id': 'logs-consumer-group',
        #'auto.offset.reset': 'earliest'  ,
        'auto.offset.reset': 'latest'
    }

    consumer = Consumer(consumer_config)

    consumer.subscribe(['logs'])

    print("Consuming messages from topic 'logs'...")
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            msg = json.loads(msg.value().decode('utf-8'))
            classify_logs(msg)

    except KeyboardInterrupt:
        print("\nShutting down logs consumer...")

    finally:
        consumer.close()

if __name__ == "__main__":
    main()
