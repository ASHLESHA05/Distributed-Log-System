import pika, json, time
import socket

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='heartbeat_queue', durable=True)

while True:
    heartbeat = {
        "service": "payment-service",
        "status": "alive",
        "host": socket.gethostname(),
        "timestamp": time.time()
    }
    channel.basic_publish(
        exchange='',
        routing_key='heartbeat_queue',
        body=json.dumps(heartbeat),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[x] Sent heartbeat: {heartbeat}")
    time.sleep(5)
