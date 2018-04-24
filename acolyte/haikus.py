class Haiku:
    """Обнаруживает хайку в сообщениях."""

    def __init__(self, bot):
        self.bot = bot
        self.vowels = set('а о и е ё э ы у ю я'.split())


    async def on_message(self, message):
        text = message.content
        words = text.split()


def setup(bot):
    bot.add_cog(Haiku(bot))
