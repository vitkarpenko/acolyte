import discord
from collections import deque


class BadStructureError(Exception):
    pass


class Haiku:
    """Обнаруживает хайку в сообщениях."""

    def __init__(self, bot):
        self.bot = bot
        self.vowels = set('а о и е ё э ы у ю я'.split())
        self.words = deque()

    async def on_message(self, message):
        text = message.content
        self.words = deque(text.replace('\n', ' ').split())
        lines = self.format_haiku()
        if lines:
            embed = discord.Embed(
                title='О, смотрю, ты человек искусства? Сочиняешь хайку?',
                description=''.join(lines)
            )
            channel = message.channel
            await self.bot.send_message(
                channel,
                embed=embed
            )

    def format_haiku(self):
        try:
            return self.structure(5, 7, 5)
        except BadStructureError:
            return False

    def count_syllables(self, word):
        return sum(char in self.vowels for char in word.lower())

    def structure(self, *lengths):
        return [
            self.find_line(5),
            self.find_line(7),
            self.find_line(5)
        ]

    def find_line(self, length):
        passed_syllables = 0
        passed_words = []
        while self.words:
            word = self.words.popleft()
            passed_words.append(word)
            passed_syllables += self.count_syllables(word)
            if passed_syllables > length:
                raise BadStructureError
            elif passed_syllables == length:
                return ' '.join(passed_words) + '\n'
        if passed_syllables < length:
            raise BadStructureError

def setup(bot):
    bot.add_cog(Haiku(bot))
