from pathlib import Path
import os
import random

import discord
import markovify


class Markov:

    def __init__(self, bot):
        self.bot = bot
        current_file = os.path.dirname(os.path.abspath(__file__))
        with \
                open(Path(current_file).parent / 'data' / 'sharpe.txt') as sharpe, \
                open(Path(current_file).parent / 'data' / 'fallout.txt') as fallout, \
                open(Path(current_file).parent / 'data' / 'eterna.txt') as eterna:
            data = sharpe.read() + fallout.read() + eterna.read()
            self.model = markovify.NewlineText(data, state_size=3)

        with open(Path(current_file).parent / 'data' / 'sharpe.txt') as sharpe:
            sharpe_model = markovify.NewlineText(sharpe, state_size=3)
        with open(Path(current_file).parent / 'data' / 'fallout.txt') as fallout:
            fallout_model = markovify.NewlineText(fallout, state_size=3)
        with open(Path(current_file).parent / 'data' / 'eterna.txt') as eterna:
            eterna_model = markovify.NewlineText(eterna, state_size=3)
        self.model = markovify.combine(
            [sharpe_model, fallout_model, eterna_model],
            [1, 1, 1]
        )

    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            phrase = self.model.make_sentence()
            while not phrase:
                phrase = self.model.make_sentence()
            phrase = phrase[0].lower() + phrase[1:]
            await self.bot.send_message(
                message.channel,
                f'{message.author.mention}, {phrase}'
            )

def setup(bot):
    bot.add_cog(Markov(bot))
