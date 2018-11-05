import os

import twitter
import requests
from bs4 import BeautifulSoup


class TwitterQuoter:
    def __init__(self):
        self.twitter = twitter.Api(
            consumer_key='XFRqXC0pOEgIas4QVb4vQFyTz',
            consumer_secret='CpVf0x3lFRr0XHUnWaOCcpApT17AmFBsq6Ib4tZoKCHQqH7FOQ',
            access_token_key='734460717303271425-0afYAgCMqPozfioZ6CuBLqQc4yj7wqA',
            access_token_secret='uzooK4vC8Vg6jZCJgDoklmxuGKQuFYvLi4FafRcVSmFTd',
        )
        self.username = 'karpenko_vitaly'
        self.tweets = self.fetch_latest_tweets()

    def fetch_updates_ids(self):
        """ Получает последние твиты, записывает их в twitter.tweets
        и возвращает ID новых твитов.
        """
        latest_tweets = self.fetch_latest_tweets()
        updates_ids = set(tweet.id for tweet in self.fetch_latest_tweets()) - set(
            tweet.id for tweet in self.tweets
        )
        self.tweets = latest_tweets
        return updates_ids

    def fetch_latest_tweets(self):
        return list(self.twitter.GetUserTimeline(screen_name=self.username, count=50))

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
