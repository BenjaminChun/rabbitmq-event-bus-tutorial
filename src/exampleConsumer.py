import pika

# Establish a connection to RabbitMQ server (default localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue to consume messages from
queue_name = 'catchEmAll'
channel.queue_declare(queue=queue_name,durable=True)

# Callback function to process messages
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# Tell RabbitMQ to send messages from 'hello' queue to this callback
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
