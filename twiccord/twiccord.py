import asyncio
import os
import random

from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import twitter
import requests

TOKENS = dict(
    CONSUMER_KEY=os.getenv('TWICCORD_TWITTER_CONSUMER_KEY'),
    CONSUMER_SECRET=os.getenv('TWICCORD_TWITTER_CONSUMER_SECRET'),
    ACCESS_TOKEN_KEY=os.getenv('TWICCORD_TWITTER_ACCESS_TOKEN_KEY'),
    ACCESS_TOKEN_SECRET=os.getenv('TWICCORD_TWITTER_ACCESS_TOKEN_SECRET'),
    BOT_TOKEN=os.getenv('TWICCORD_DISCORD_BOT_TOKEN')
)


class KindleQuotesRedirecter(commands.Bot):
    """ Periodically checks user's timeline for new tweets with amazon kindle quotes.
    Reposts new quotes to Discord channel.

    self.tweets is a list of last fetched tweets.
    """
    def __init__(self, tokens, username):
        super().__init__(command_prefix='!', description="За Кейли, двигатель и новый способ атомного бражения.")
        self.loop = asyncio.get_event_loop()
        self.twitter = twitter.Api(
            consumer_key=tokens['CONSUMER_KEY'],
            consumer_secret=tokens['CONSUMER_SECRET'],
            access_token_key=tokens['ACCESS_TOKEN_KEY'],
            access_token_secret=tokens['ACCESS_TOKEN_SECRET']
        )
        self.username = username
        self.tweets = self.fetch_latest_tweets()


    def fetch_updates_ids(self):
        """ Получает последние твиты, записывает их в self.tweets
        и возвращает ID новых твитов.
        """
        latest_tweets = self.fetch_latest_tweets()
        updates_ids = (
            set(tweet.id for tweet in self.fetch_latest_tweets())
            - set(tweet.id for tweet in self.tweets)
        )
        self.tweets = latest_tweets
        return updates_ids

    def fetch_latest_tweets(self):
        return list(
            self.twitter.GetUserTimeline(
                screen_name=self.username,
                count=50
            )
        )

    def find_kindle_quotes(self, message):
        text = message.text
        last_word = text.split()[-1]
        if not last_word.startswith('https://t.co/'):
            return None
        r = requests.get(last_word)
        parser = BeautifulSoup(r.text, 'lxml')
        quote = parser.find(id='kp-quote')
        if quote:
            return quote.string.strip(' \t\n"')
        else:
            return None

    def format_quote(self, quote):
        return f'**Виталий цитирует**:\n_{quote}_'

    async def post_updates_to_discord(self):
        books = self.get_channel('405339907012427779')
        updates_ids = self.fetch_updates_ids()
        updates = (tweet for tweet in self.tweets if tweet.id in updates_ids)
        for update in updates:
            quote = self.find_kindle_quotes(update)
            if quote:
                await self.send_message(
                    books,
                    self.format_quote(quote)
                )

    async def _run_periodically(self, period, method):
        while True:
            await method()
            await asyncio.sleep(period)

    async def on_ready(self):
        await self._run_periodically(10, self.post_updates_to_discord)

    @commands.command()
    async def roll(self, dice):
        global redirecter
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.say('**XdY**, просил же!')
        rolls = [random.randint(1, limit) for r in range(rolls)]
        comma_separated_rolls = ', '.join(str(roll) for roll in rolls)
        return self.say(f'**Выпало**: {comma_separated_rolls}\n**Сумма**: {sum(rolls)}')


def main():
    redirecter = KindleQuotesRedirecter(TOKENS, 'karpenko_vitaly')
    redirecter.add_command(roll)
    redirecter.run(TOKENS['BOT_TOKEN'])
