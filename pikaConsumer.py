import pika, json, time

heartbeat_registry = {}

def callback(ch, method, properties, body):
    heartbeat = json.loads(body)
    service = heartbeat["service"]
    heartbeat_registry[service] = heartbeat["timestamp"]
    print(f"[x] Received heartbeat from {service}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='heartbeat_queue', durable=True)
channel.basic_consume(queue='heartbeat_queue', on_message_callback=callback, auto_ack=True)

print('[*] Waiting for heartbeats. To exit press CTRL+C')
channel.start_consuming()
