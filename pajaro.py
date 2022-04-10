from http import client
from multiprocessing.connection import Client
import tweepy
import pprint
import Configuration.secret as sc

class Pajaro:
    def __init__(self, filename):
        self.authentication_TWAPIv11(sc.get_secrets(filename))

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

    def get_user_settings(self):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.api.get_settings())