from itertools import count
from time import sleep
from multiprocessing.connection import Client
import tweepy
import pprint
import Configuration.secret as sc
from Configuration.configuration import Configuration
from Database.database import PajaroDatabase
import random

class Pajaro:
    def __init__(self, sfilename, cfilename):
        self.authentication_TWAPIv11(sc.get_secrets(sfilename))
        self.config = Configuration(cfilename)
        self.db = PajaroDatabase(self.config)

    def authentication_TWAPIv11(self, secret):
        auth = tweepy.OAuth1UserHandler(str(secret[0]['api_key']),
                                        str(secret[0]['api_key_secret']), 
                                        str(secret[0]['access_token']),
                                        str(secret[0]['access_token_secret']))
        self.api = tweepy.API(auth)

    def authentication_TWAPIv2_keys(self, secret):
        api_key = str(secret[0]['api_key'])
        api_key_secret = str(secret[0]['api_key_secret'])
        access_token = str(secret[0]['access_token'])
        access_token_secret = str(secret[0]['access_token_secret'])

        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def authentication_TWAPIv2_bearer_token(self, secret):
        token = str(secret[0]['bearer_token'])
        self.client = tweepy.Client(bearer_token=token)

    def post_tweet(self, tweet=None):
        if tweet != None:
            self.api.update_status(tweet)
        else:
            print('No tweet given.')

    def update_post_metrics(self, post_id, tweet_id):
        for status in self.api.lookup_statuses(id=[tweet_id]):
            self.db.update_post_metrics(post_id, status)

    def get_latest_tweet_id(self):
        for status in self.api.user_timeline(count=1):
            self.latest_tweet_id = status.id

    def post_latest_tweet(self):
        try:
            self.db.insert_posts_from_fetcher()
            post = self.db.get_latest_not_posted()
            tweet = post[1] + ' ' + post[3] + '\n\n' + post[2]
            self.post_tweet(tweet)
            sleep(5)
            self.db.set_post_as_posted(int(post[0]))
            self.get_latest_tweet_id()
            self.update_post_metrics(int(post[0]), self.latest_tweet_id)

        except Exception as e:
            print(e)
            pass
    

    def run(self):
        self.post_latest_tweet()
        sleep(random.randint(600, 900))
            

        