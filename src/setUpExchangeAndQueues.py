import pika
import os
from dotenv import load_dotenv
import sys
import json

# first argument is queue_name, second is headers-filter

if __name__=="__main__":
    queue_name,args='',''
    if len(sys.argv) > 2:
        queue_name, args = sys.argv[1], json.loads(sys.argv[2])

    load_dotenv()
    exchange_name=os.environ['EXCHANGE_NAME']
    host=os.environ['RABBITMQ_HOST']
    port=int(os.environ['RABBITMQ_PORT'])
    virtual_host=os.environ['RABBITMQ_VHOST']
    username=os.environ['RABBITMQ_USERNAME']
    password=os.environ['RABBITMQ_PASSWORD']
    if not queue_name:
        queue_name=os.environ['QUEUE_NAME']
    if not args:
        args=json.loads(os.environ['ARGS'])
    print(args,queue_name)
    # create connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host=virtual_host,
        credentials=pika.PlainCredentials(username, password)
    ))
    # declare the header exchange
    connection.channel().exchange_declare(exchange=exchange_name, exchange_type='headers')
    # create queue
    connection.channel().queue_declare(queue_name, durable=True)
    # bind queue to exchange
    connection.channel().queue_bind(queue_name, exchange_name, routing_key='', arguments=args)
    
    # gracefully close connection
    connection.close()