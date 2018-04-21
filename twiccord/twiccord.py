import os
import threading

import discord
import twitter

TOKENS = dict(
    CONSUMER_KEY=os.getenv('TWICCORD_TWITTER_CONSUMER_KEY'),
    CONSUMER_SECRET=os.getenv('TWICCORD_TWITTER_CONSUMER_SECRET'),
    ACCESS_TOKEN_KEY=os.getenv('TWICCORD_TWITTER_ACCESS_TOKEN_KEY'),
    ACCESS_TOKEN_SECRET=os.getenv('TWICCORD_TWITTER_ACCESS_TOKEN_SECRET')
)


class TwitterListener:
    """ Periodically checks user's timeline for new tweets with amazon kindle quotes.
    """
    def __init__(self, tokens, username):
        self.api = twitter.Api(
            consumer_key=tokens['CONSUMER_KEY'],
            consumer_secret=['CONSUMER_SECRET'],
            access_token_key=['ACCESS_TOKEN_KEY'],
            access_token_secret=['ACCESS_TOKEN_SECRET']
        )
        self.latest_tweets = list()
