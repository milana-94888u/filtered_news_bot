from typing import Callable

from pika import BlockingConnection, ConnectionParameters, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


class Consumer:
    def __init__(self, queue_name: str, callback: Callable[[bytes], None]):
        self.queue_name = queue_name
        self.connection = BlockingConnection(ConnectionParameters("localhost"))
        self.channel = self.connection.channel()

        self.real_callback = callback
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback
        )
        self.channel.start_consuming()

    def callback(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        self.real_callback(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        self.connection.close()
