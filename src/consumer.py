import json
import os
from typing import Callable

import pika
from dotenv import load_dotenv


class EventSubscriber:
    __exchange_name = None
    __channel = None

    def __init__(
            self,
            exchange_name: str = 'events',
            host: str = 'localhost',
            port: int = 5672,
            virtual_host: str = '/',
            username: str = 'guest',
            password: str = 'guest'
    ):
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=credentials
        ))
        self._channel = connection.channel()
        self.__exchange_name = exchange_name
        self._channel.exchange_declare(exchange=exchange_name, exchange_type='headers')

    def start(self):
        self._channel.start_consuming()

    def subscribe_events(self, queue_name: str, callback: Callable, label_filter: dict[str, str], match_type: str = 'all'):
        print(f"Create queue {queue_name} with binding attributes {label_filter}")
        args = dict(label_filter)
        args['x-match'] = match_type

        self._channel.queue_declare(queue_name, durable=True)
        self._channel.queue_bind(queue_name, self.__exchange_name, routing_key='', arguments=args)
        self._channel.basic_consume(queue_name, on_message_callback=callback, auto_ack=True)


# Load configuration from .env file
load_dotenv()

event_subscriber = EventSubscriber(
    exchange_name=os.environ['EXCHANGE_NAME'],
    host=os.environ['RABBITMQ_HOST'],
    port=int(os.environ['RABBITMQ_PORT']),
    virtual_host=os.environ['RABBITMQ_VHOST'],
    username=os.environ['RABBITMQ_USERNAME'],
    password=os.environ['RABBITMQ_PASSWORD']
)


def create_handler(name):
    """
    Creates event handler function with specific name for debug purposes.
    :param name: The name of the handler.
    :return: The handler function.
    """
    def on_every_event_received(channel, method, properties, body):
        print(f"Handler '{name}' has received event with headers '{properties.headers}':", body)
        return

    return on_every_event_received


event_subscriber.subscribe_events("documents_all", create_handler("All document events"), {'type': 'document'})
event_subscriber.subscribe_events("documents_create", create_handler("'Create document' events"), {'type': 'document', 'event': 'create'})
event_subscriber.subscribe_events("all", create_handler("All events"), {})


print("Start consuming events")
event_subscriber.start()
