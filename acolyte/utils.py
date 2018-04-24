import asyncio
from datetime import datetime, time


async def start_background_tasks(tasks, period=10):
    while True:
        for task in tasks:
            await task()
        await asyncio.sleep(period)


def is_night():
    now = datetime.now().time()
    return time(2, 0) <= now <= time(8, 0)


def format_quote(quote):
    return f'**Виталий цитирует**:\n_{quote}_'
