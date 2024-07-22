import json
import os

import pika
from dotenv import load_dotenv


class EventPublisher:
    """
    A class to handle publishing events to RabbitMQ Event-bus.

    Attributes:
    ----------
    __exchange_name : str
        The name of the exchange to publish events to.
    __channel : pika.adapters.blocking_connection.BlockingChannel
        The channel used for communication with RabbitMQ.
    """

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
        """
        Initializes RabbitMQ connection with the given parameters
        and declares the exchange if it doesn't exist.

        Important! For production usage you must implement connection recovery.
        See: https://pika.readthedocs.io/en/stable/modules/adapters/index.html#connection-recovery

        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=pika.PlainCredentials(username, password)
        ))
        self._channel = connection.channel()
        self.__exchange_name = exchange_name
        # Creates the exchange on startup if it does not exist yet
        self._channel.exchange_declare(exchange=exchange_name, exchange_type='headers')

    def publish_event(self, body: any, headers: dict[str, str]):
        """
        Publishes an event to the Event-bus.

        Parameters:
        ----------
        body : any
            The body of the event to publish.
        labels : dict[str, str]
            The labels is used by consumers for filtering
        """
        content = json.dumps(body).encode()  # Sends body in JSON format, but you can choose your own
        print(f"Publish event with headers '{headers}' and body '{content}'")
        self._channel.basic_publish(
            exchange=self.__exchange_name,
            routing_key='',  # Headers exchange ignores routing key
            body=content,
            properties=pika.BasicProperties(
                headers=headers  # Sends labels in headers
            )
        )


# Load configuration from .env file
load_dotenv()

event_publisher = EventPublisher(
    exchange_name=os.environ['EXCHANGE_NAME'],
    host=os.environ['RABBITMQ_HOST'],
    port=int(os.environ['RABBITMQ_PORT']),
    virtual_host=os.environ['RABBITMQ_VHOST'],
    username=os.environ['RABBITMQ_USERNAME'],
    password=os.environ['RABBITMQ_PASSWORD']
)

# Publish 3 events with different routing headers
event_publisher.publish_event({'name': 'Document 1'}, {'type': 'document', 'event': 'create'})
event_publisher.publish_event({'name': 'Document 1'}, {'type': 'document', 'event': 'update'})
event_publisher.publish_event({'filename': 'kitty.jpeg'}, {'type': 'file', 'event': 'create'})
