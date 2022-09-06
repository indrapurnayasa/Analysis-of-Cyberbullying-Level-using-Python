import json
import snscrape.modules.twitter as sntwitter
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler

client = MongoClient('localhost', 27017)
db = client['databaseName']
collection = db['collectionName']

access_token = "xxxx"
access_token_secret = "xxxx"
consumer_key = "xxxx"
consumer_secret = "xxxx"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('keyword + since:yyyy-mm-dd until:yyyy-mm-dd lang:in').get_items()):
    id = tweet.id
    if(id==None or id==''):
        continue
    getTweet = api.get_status(id, wait_on_rate_limit=True, wait_on_rate_limit_notify = True, tweet_mode='extended')
    json_str = json.dumps(getTweet._json)
    print(json_str)
    collection.insert_one(getTweet._json)
    #
    # geocode: -8.3919, 115.18756, 1000km

