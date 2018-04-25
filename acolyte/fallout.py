from pathlib import Path
import os
import random

import discord
import markovify


class Fallout:
    """Иногда отвечает на сообщения игроков,
    используя цепи Маркова, построенные на файлах
    диалогов из Fallout 2.
    """

    def __init__(self, bot):
        self.bot = bot
        current_file = os.path.dirname(os.path.abspath(__file__))
        with open(Path(current_file).parent / 'data' / 'fallout.txt') as fallout_phrases:
            self.model = markovify.NewlineText(fallout_phrases.read())

    async def on_message(self, message):
        #cant_hold_it = random.randint(0, 100) // 100
        #if cant_hold_it:
        message = self.model.make_sentence()
        message = message[0].lower() + message[1:]
        await self.bot.send_message(
            message.channel,
            f'{message.author.mention}, {message}'
        )

def setup(bot):
    bot.add_cog(Fallout(bot))
