import pika
import os
from dotenv import load_dotenv
import sys
import json

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

if __name__=="__main__":
    queue_name=''
    if len(sys.argv) > 1:
        queue_name = sys.argv[1]

    load_dotenv()
    exchange_name=os.environ['EXCHANGE_NAME']
    host=os.environ['RABBITMQ_HOST']
    port=int(os.environ['RABBITMQ_PORT'])
    virtual_host=os.environ['RABBITMQ_VHOST']
    username=os.environ['RABBITMQ_USERNAME']
    password=os.environ['RABBITMQ_PASSWORD']
    if not queue_name:
        queue_name=os.environ['QUEUE_NAME']

    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host=virtual_host,
        credentials=pika.PlainCredentials(username, password)
    ))
    # prepares consumer with appropriate callback
    connection.channel().basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Waiting for messages in {queue_name}. Press CTRL+C to exit.")
    try:
        # Start consuming (this will block and run the consumer loop)
        connection.channel().start_consuming()
    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
        # Close the connection properly when CTRL+C is pressed
        connection.channel().stop_consuming()
        connection.close()
    except Exception as e:
        print(e)