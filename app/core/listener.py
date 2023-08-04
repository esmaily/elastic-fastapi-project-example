import asyncio
from aio_pika import connect, IncomingMessage
import json
from .config import settings
from app.core.db import Article


async def on_message(message: IncomingMessage):
    raw_data = message.body.decode("utf-8")
    data = json.loads(raw_data)
    article = json.loads(data[0][0])
    await Article.objects.create(**article)


async def consume_messages(loop):
    connection = await connect(settings.BROKER_URL, loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue(settings.CONSUME_QUEUE)

    await queue.consume(on_message, no_ack=True)


def init_listen_queues():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # no event loop running:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(consume_messages(loop))
    if not loop.is_running():
        loop.run_until_complete(task)


if __name__ == "__main__":
    init_listen_queues()
