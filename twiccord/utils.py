import asyncio


async def run_periodically(period, method):
    while True:
        await method()
        await asyncio.sleep(period)

def format_quote(quote):
    return f'**Виталий цитирует**:\n_{quote}_'
