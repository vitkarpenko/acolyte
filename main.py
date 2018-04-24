import os

from acolyte.bot import bot


if __name__ == '__main__':
    bot.run(os.getenv('TWICCORD_DISCORD_BOT_TOKEN'))
