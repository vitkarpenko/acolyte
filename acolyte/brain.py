import logging

from discord.ext.commands import Cog, command


class Brain(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        text = message.content
        logging.info(f'Треню на: "{text}"')
        await self.bot.brain.post('http://brain:8080/train', data=text)

    @command()
    async def speak(self, context):
        response = await self.bot.brain.get('http://brain:8080/test')
        message = await response.text()
        logging.info(f'От мозга пришло: "{message}"')
        await context.send(await response.text())


def setup(bot):
    bot.add_cog(Brain(bot))
