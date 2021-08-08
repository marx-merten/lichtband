import uasyncio as asyncio


def schedule(task):
    asyncio.get_event_loop().create_task(task)
