import logging
import os

from acolyte.bot import bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.run(os.getenv("ACOLYTE_DISCORD_TOKEN"))
