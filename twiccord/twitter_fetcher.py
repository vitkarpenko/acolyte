import os

import twitter
import requests
from bs4 import BeautifulSoup


class TwitterFetcher:
    def __init__(self):
        self.twitter = twitter.Api(
            consumer_key=os.getenv('TWICCORD_TWITTER_CONSUMER_KEY'),
            consumer_secret=os.getenv('TWICCORD_TWITTER_CONSUMER_SECRET'),
            access_token_key=os.getenv('TWICCORD_TWITTER_ACCESS_TOKEN_KEY'),
            access_token_secret=os.getenv('TWICCORD_TWITTER_ACCESS_TOKEN_SECRET')
        )
        self.tweets = list()
        self.username = 'karpenko_vitaly'


    def fetch_updates_ids(self):
        """ Получает последние твиты, записывает их в twitter.tweets
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
