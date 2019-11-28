import operator

import discord
from discord.ext import commands


class Poll(commands.Cog):
    """Создание голосовалок."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, context, question, *options: str):
        if len(options) <= 1:
            await context.send("Пустые голосования не принимаются.")
            return
        if len(options) > 9:
            await context.send("Давай ограничимся девятью вариантами.")
            return

        if len(options) == 2 and options[0] == "да" and options[1] == "нет":
            reactions = ["✅", "❌"]
        else:
            reactions = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]

        description = []
        for x, option in enumerate(options):
            description += "\n{} {}".format(reactions[x], option)
        embed = discord.Embed(title=question, description="".join(description))
        react_message = await context.send(embed=embed)
        for reaction in reactions[: len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text="ID голосования: {}".format(react_message.id))
        await react_message.edit(embed=embed)

    @commands.command()
    async def tally(self, context, id):
        poll_message = await context.message.channel.fetch_message(id)
        if not poll_message.embeds:
            return
        embed = poll_message.embeds[0]
        if poll_message.author != context.me:
            return
        unformatted_options = [x.strip() for x in embed.description.split("\n")]
        options = (
            {x[:2]: x[3:] for x in unformatted_options}
            if unformatted_options[0][0] == "1"
            else {x[:1]: x[2:] for x in unformatted_options}
        )
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [
            context.me.id
        ]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in options.values()}
        for reaction in poll_message.reactions:
            if reaction.emoji in options.keys():
                async for reactor in reaction.users():
                    if reactor.id not in voters:
                        tally[options[reaction.emoji]] += 1
                        voters.append(reactor.id)

        results = sorted(tally.items(), key=operator.itemgetter(1), reverse=True)
        output = (
            '**Результаты голосования "{}":**\n```\n'.format(embed.title)
            + "\n".join(
                [
                    "{}: {}".format(result[0], '\U0001F4A0' * result[1])
                    for result in results
                ]
            )
            + '```\n'
        )

        await context.send(output)


def setup(bot):
    bot.add_cog(Poll(bot))
