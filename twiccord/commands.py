import asyncio

from discord.ext import commands

@commands.command()
async def roll(dice):
    nonlocal redirecter
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await redirecter.say('**XdY**, просил же!')
    rolls = [random.randint(1, limit) for r in range(rolls)]
    comma_separated_rolls = ', '.join(str(roll) for roll in rolls)
    return redirecter.say(f'**Выпало**: {comma_separated_rolls}\n**Сумма**: {sum(rolls)}')
