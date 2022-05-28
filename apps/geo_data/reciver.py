import asyncio

import async_timeout

from aioredis.client import PubSub


async def reader_channel_redis(channel: PubSub):
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    # TODO: save geo
                    pass
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass
