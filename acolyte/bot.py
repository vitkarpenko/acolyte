import os
import random
from pathlib import Path

from discord.ext import commands

from .leet_translate import translate_letter_to_leet
from .twitter_quoter import TwitterQuoter
from .utils import format_quote, is_night, start_background_tasks

bot = commands.Bot(
    command_prefix="!",
    description="За Кейли, двигатель и новый способ атомного бражения!",
)

twitter = TwitterQuoter()

current_file = os.path.dirname(os.path.abspath(__file__))
with open(Path(current_file).parent / "data" / "quotes.txt") as quotes_file:
    QUOTES = [quote.strip() for quote in quotes_file]

BOOKS_ID = 405339907012427779
FLOOD_ID = 405287350734815233


"""
Events.
"""


async def post_updates_to_discord():
    updates_ids = twitter.fetch_updates_ids()
    updates = (tweet for tweet in twitter.tweets if tweet.id in updates_ids)
    for update in updates:
        quote = twitter.find_kindle_quotes(update)
        if quote:
            channel = bot.get_channel(BOOKS_ID)
            await channel.send(format_quote(quote))


async def post_quotes():
    if is_night():
        return
    cant_hold_it = random.randint(0, 7200) // 7200
    if cant_hold_it:
        await bot.send_message(bot.get_channel(FLOOD_ID), f"*{random.choice(QUOTES)}*")


@bot.event
async def on_ready():
    await start_background_tasks([post_updates_to_discord, post_quotes])


"""
Commands.
"""


@bot.command(description="This is how I roll... *XdY*.")
async def roll(context, dice):
    try:
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await context.send("**XdY**, просил же!")
        return
    if rolls > 200:
        await context.send("У меня нет столько кубиков.")
        return
    if rolls * limit > 1_000_000:
        await context.send("Так, экспериментатор, зачехляй свой коллайдер!")
        return
    rolls = [random.randint(1, limit) for r in range(rolls)]
    comma_separated_rolls = ", ".join(str(roll) for roll in rolls)
    await context.send(f"**Выпало**: {comma_separated_rolls}\n**Сумма**: {sum(rolls)}")


@bot.command(description="Помощь нерешительным!")
async def choice(context, *args):
    await context.send(f"**Выбрано**: {random.choice(args)}")


@bot.command(description="Поможем склеротикам")
async def links(context):
    await context.send(
        "**Github**:\n\tЦенитель - https://github.com/vitkarpenko\n\tЗачинателя - https://github.com/Dairiss\n\t"
        "Раздражитель - https://github.com/Valhen-otto\n\tДля братишек - https://github.com/deeppomf/DeepCreamPy\n"
        "**Twitter**:\n\tВитика - https://twitter.com/karpenko_vitaly\n\t"
        "Иры - https://twitter.com/Valhen_Otto\n"
        "**Полезные ссылки**:\n\t Магазин исторических книг - http://kliobooks.ru/index.php/izdannye\n "
    )


@bot.command(description="Издевательство над людьми")
async def leet(context, *args):
    original_phrase = " ".join(args).lower()
    translated_phrase = "".join(
        [translate_letter_to_leet(letter) for letter in original_phrase]
    )
    await context.send(f"`{translated_phrase}`")


"""         
Cogs.
"""
bot.load_extension("acolyte.polls")
# bot.load_extension("acolyte.markov")
