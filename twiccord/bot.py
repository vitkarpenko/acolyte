import asyncio
import random

from discord.ext import commands
from .utils import (
    run_periodically,
    format_quote
)
from .twitter_fetcher import TwitterFetcher
from commands import (
    roll,
    choice
)

bot = commands.Bot(
    command_prefix='!',
    description="За Кейли, двигатель и новый способ атомного бражения!"
)

twitter = TwitterFetcher()


async def post_updates_to_discord():
    books = bot.get_channel('405339907012427779')
    updates_ids = twitter.fetch_updates_ids()
    updates = (tweet for tweet in twitter.tweets if tweet.id in updates_ids)
    for update in updates:
        quote = twitter.find_kindle_quotes(update)
        if quote:
            await bot.send_message(
                books,
                format_quote(quote)
            )


async def on_ready():
    await run_periodically(10, post_updates_to_discord)

bot.event(on_ready)

bot.command(
    description='This is how I roll... *XdY*.'
)(roll)
bot.command(
    description='Помощь нерешительным!'
)(choice)
