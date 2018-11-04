from pathlib import Path
import os
import random

import discord
import markovify


class Markov:
    def __init__(self, bot):
        self.bot = bot
        current_file = os.path.dirname(os.path.abspath(__file__))
        with open(
            Path(current_file).parent / 'data' / 'mim.txt', encoding='utf-8'
        ) as mim, open(
            Path(current_file).parent / 'data' / 'fallout.txt', encoding='utf-8'
        ) as fallout, open(
            Path(current_file).parent / 'data' / 'kamu.txt', encoding='utf-8'
        ) as kamu, open(
            Path(current_file).parent / 'data' / 'monten.txt', encoding='utf-8'
        ) as monten, open(
            Path(current_file).parent / 'data' / 'evrika.txt', encoding='utf-8'
        ) as evrika, open(
            Path(current_file).parent / 'data' / 'gosud.txt', encoding='utf-8'
        ) as gosud, open(
            Path(current_file).parent / 'data' / 'parsDeva.txt', encoding='utf-8'
        ) as parsDeva, open(
            Path(current_file).parent / 'data' / 'parsKandid.txt', encoding='utf-8'
        ) as parsKandid, open(
            Path(current_file).parent / 'data' / 'horn.txt', encoding='utf-8'
        ) as horn, open(
            Path(current_file).parent / 'data' / 'sharpe.txt', encoding='utf-8'
        ) as sharpe, open(
            Path(current_file).parent / 'data' / 'eterna.txt', encoding='utf-8'
        ) as eterna, open(
            Path(current_file).parent / 'data' / 'komm.txt', encoding='utf-8'
        ) as komm, open(
            Path(current_file).parent / 'data' / 'larosh.txt', encoding='utf-8'
        ) as larosh, open(
            Path(current_file).parent / 'data' / 'parsMonach.txt', encoding='utf-8'
        ) as parsMonach:
            data = (
                mim.read()
                + kamu.read()
                + gosud.read()
                + fallout.read()
                + monten.read()
                + parsDeva.read()
                + parsKandid.read()
                + parsMonach.read()
                + eterna.read()
                + evrika.read()
                + sharpe.read()
                + horn.read()
                + komm.read()
                + larosh.read()
            )

            self.model = markovify.NewlineText(data, state_size=3)

        with open(
            Path(current_file).parent / 'data' / 'mim.txt', encoding='utf-8'
        ) as mim:
            mim_model = markovify.NewlineText(mim, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'fallout.txt', encoding='utf-8'
        ) as fallout:
            fallout_model = markovify.NewlineText(fallout, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'kamu.txt', encoding='utf-8'
        ) as kamu:
            kamu_model = markovify.NewlineText(kamu, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'gosud.txt', encoding='utf-8'
        ) as gosud:
            gosud_model = markovify.NewlineText(gosud, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'monten.txt', encoding='utf-8'
        ) as monten:
            monten_model = markovify.NewlineText(monten, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'evrika.txt', encoding='utf-8'
        ) as evrika:
            evrika_model = markovify.NewlineText(evrika, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'parsDeva.txt', encoding='utf-8'
        ) as parsDeva:
            parsDeva_model = markovify.NewlineText(parsDeva, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'parsKandid.txt', encoding='utf-8'
        ) as parsKandid:
            parsKandid_model = markovify.NewlineText(parsKandid, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'parsMonach.txt', encoding='utf-8'
        ) as parsMonach:
            parsMonach_model = markovify.NewlineText(parsMonach, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'eterna.txt', encoding='utf-8'
        ) as eterna:
            eterna_model = markovify.NewlineText(eterna, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'evrika.txt', encoding='utf-8'
        ) as evrika:
            evrika_model = markovify.NewlineText(evrika, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'sharpe.txt', encoding='utf-8'
        ) as sharpe:
            sharpe_model = markovify.NewlineText(sharpe, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'horn.txt', encoding='utf-8'
        ) as horn:
            horn_model = markovify.NewlineText(horn, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'komm.txt', encoding='utf-8'
        ) as komm:
            komm_model = markovify.NewlineText(komm, state_size=3)
        with open(
            Path(current_file).parent / 'data' / 'larosh.txt', encoding='utf-8'
        ) as larosh:
            larosh_model = markovify.NewlineText(larosh, state_size=3)
        self.model = markovify.combine(
            [
                parsDeva_model,
                parsKandid_model,
                parsMonach_model,
                mim_model,
                kamu_model,
                evrika_model,
                gosud_model,
                monten_model,
                fallout_model,
                evrika_model,
                sharpe_model,
                horn_model,
                komm_model,
                larosh_model,
                eterna_model,
            ],
            [43, 80, 33, 15, 80, 25, 6.7, 4, 8, 33, 2, 2.3, 15, 117, 1],
        )

    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            phrase = self.model.make_short_sentence(250)
            while not phrase:
                phrase = self.model.make_short_sentence(250)
            phrase = phrase[0].lower() + phrase[1:]
            await self.bot.send_message(
                message.channel, f'{message.author.mention}, {phrase}'
            )


def setup(bot):
    bot.add_cog(Markov(bot))
