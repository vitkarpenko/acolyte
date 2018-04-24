import asyncio
import os
from pathlib import Path
import random

from discord.ext import commands
from .utils import (
    start_background_tasks,
    format_quote,
    is_night
)
from .twitter_quoter import TwitterQuoter

bot = commands.Bot(
    command_prefix='!',
    description="За Кейли, двигатель и новый способ атомного бражения!"
)

twitter = TwitterQuoter()

current_file = os.path.dirname(os.path.abspath(__file__))
with open(Path(current_file).parent / 'data' / 'quotes.txt') as quotes_file:
    QUOTES = [quote.strip() for quote in quotes_file]

BOOKS = bot.get_channel('405339907012427779')
FLOOD = bot.get_channel('405287350734815233')


"""
Events.
"""
async def post_updates_to_discord():
    updates_ids = twitter.fetch_updates_ids()
    updates = (tweet for tweet in twitter.tweets if tweet.id in updates_ids)
    for update in updates:
        quote = twitter.find_kindle_quotes(update)
        if quote:
            await bot.send_message(
                BOOKS,
                format_quote(quote)
            )


async def post_quotes():
    if is_night():
        return
    cant_hold_it = random.randint(0, 360) // 360
    if cant_hold_it:
        bot.send_message(
            FLOOD,
            f'*{random.choice(QUOTES)}*'
        )


@bot.event
async def on_ready():
    bot.send_message(
        FLOOD,
        f'***Я переродился!***'
    )
    await start_background_tasks([post_updates_to_discord, post_quotes])


"""
Commands.
"""
@bot.command(description='This is how I roll... *XdY*.')
async def roll(dice):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('**XdY**, просил же!')
        return
    if rolls > 200:
        await bot.say('У меня нет столько кубиков.')
        return
    if rolls * limit > 1000000:
        await bot.say('Так, экспериментатор, зачехляй свой коллайдер!')
        return
    rolls = [random.randint(1, limit) for r in range(rolls)]
    comma_separated_rolls = ', '.join(str(roll) for roll in rolls)
    await bot.say(f'**Выпало**: {comma_separated_rolls}\n**Сумма**: {sum(rolls)}')


@bot.command(description='Помощь нерешительным!')
async def choice(*args):
    await bot.say(f'**Выбрано**: {random.choice(args)}')


"""
Cogs.
"""
bot.load_extension('acolyte.polls')
