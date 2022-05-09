from tweepy.streaming import Stream
from tweepy import api
from tweepy import OAuthHandler
from tweepy import Stream

import json

config = open('config.json')
config = json.load(config)

class TwitterAuthenticator():
    # class for authenticating to twitter
    def authenticate_twitter_app(self):
        authenticate = OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
        authenticate.set_access_token(config['ACCESS_TOKEN'], config['ACCESS_TOKEN_SECRET'])
        return authenticate

class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    # streams and processes live tweets
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        authenticate = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(authenticate, listener)
        stream.filter(track=['covid 19', 'covid', 'covid-19'])

class TwitterListener(Stream):
    # basic listener class
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as file:
                file.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # return false on_data method in case rate limit is reached
            return False
        print(status)


if __name__ == "main":
    hash_tag_list = ['covid 19', 'covid', 'covid-19']
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
