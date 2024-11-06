import pika
import os
from dotenv import load_dotenv
import sys
import json


if __name__=="__main__":
    headers,body='',''
    if len(sys.argv) > 2:
        headers,body = json.loads(sys.argv[1]),json.loads(sys.argv[2])

    load_dotenv()
    exchange_name=os.environ['EXCHANGE_NAME']
    host=os.environ['RABBITMQ_HOST']
    port=int(os.environ['RABBITMQ_PORT'])
    virtual_host=os.environ['RABBITMQ_VHOST']
    username=os.environ['RABBITMQ_USERNAME']
    password=os.environ['RABBITMQ_PASSWORD']
    if not body:
        body=os.environ["BODY"]
    if not headers:
        headers=json.loads(os.environ["HEADERS"])

    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host=virtual_host,
        credentials=pika.PlainCredentials(username, password)
    ))
    # prepares the payload content
    content = json.dumps(body).encode()  # Sends body in JSON format, but you can choose your own
    # publish event onto the exchange
    connection.channel().basic_publish(
            exchange=exchange_name,
            routing_key='',  # Headers exchange ignores routing key
            body=content,
            properties=pika.BasicProperties(
                headers=headers  # Sends labels in headers
            )
        )
    # gracefully close connection
    connection.close()