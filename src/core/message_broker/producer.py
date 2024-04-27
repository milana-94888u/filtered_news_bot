from pika import BlockingConnection, ConnectionParameters, DeliveryMode, BasicProperties

from .config import settings


class Producer:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = BlockingConnection(ConnectionParameters(settings.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue_name, durable=True)

    def publish(self, message: str) -> None:
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message.encode(),
            properties=BasicProperties(delivery_mode=DeliveryMode.Persistent),
        )

    def close(self):
        self.connection.close()
