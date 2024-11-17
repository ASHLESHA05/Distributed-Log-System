from confluent_kafka import Consumer
from datetime import datetime, timedelta
import json

EXPECTED_INTERVAL = 5 
heart_beat={}

def check_heart_beat(msg):
    if msg['node_id'] not in heart_beat:
        heart_beat[msg['node_id']]={'status':msg['status'],'timestamp':msg['timestamp']}
        print(f'First Incomming from {msg['node_id']}, timestamp: {msg['timestamp']}')
        return True
    if msg['status']=='DOWN':
        print("ALERT!! ",msg['node_id'],'shutDown Gracefully')
        heart_beat[msg['node_id']]['status']='DOWN'
        return True
    if msg['status'] != heart_beat[msg['node_id']]['status']:
        print('Service with node id:',msg['node_id'],'Restarted')
        heart_beat[msg['node_id']]['status']='UP'
        return True
        
    #Here we check for the delayed time stamp
    previous_time=datetime.fromisoformat(heart_beat[msg['node_id']]['timestamp'])
    current_time = datetime.fromisoformat(msg['timestamp'])
    actual_interval = (current_time - previous_time).total_seconds()
    actual_interval_rounded = round(actual_interval, 2)
    if actual_interval_rounded > EXPECTED_INTERVAL:
        print(f"ALERT: Delay detected! Interval: {actual_interval_rounded} seconds")
    else:
        print(f"{msg['node_id']} : UP")
        
    heart_beat[msg['node_id']]['timestamp']=msg['timestamp']
    return False
    
    
        
    
def main():
    # Configuration for the Kafka Consumer
    consumer_config = {
        'bootstrap.servers': 'localhost:9092', 
        'group.id': 'heartbeat-consumer-group',
        'auto.offset.reset': 'earliest'  
    }

    # Create a Consumer instance
    consumer = Consumer(consumer_config)

    # Subscribe to the topic
    consumer.subscribe(['heartbeat'])

    print("Consuming messages from topic 'heartbeat'...")
    try:
        while True:
            # Poll for a message
            msg = consumer.poll(1.0)  # Timeout of 1 second

            if msg is None:
                # No message available yet
                continue

            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            msg=msg.value().decode('utf-8')
            msg_dict = json.loads(msg)
            check_heart_beat(dict(msg_dict))
            # Print the message value
            #print(f"Received message: {msg}")
    except KeyboardInterrupt:
        print("\nShutting down heartbeat consumer...")

    finally:
        # Close the consumer to commit offsets and clean up resources
        consumer.close()

if __name__ == "__main__":
    main()
