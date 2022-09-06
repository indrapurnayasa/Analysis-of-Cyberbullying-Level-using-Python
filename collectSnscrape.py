import json
import snscrape.modules.twitter as sntwitter
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler

client = MongoClient('localhost', 27017)
db = client['cyberbullyingTwitter']
collection = db['cyberbullying6Apr']

access_token = "250996215-QlydZXfPKlML21RTbcYbDTj82NmL2z4b0viP1wR8"
access_token_secret = "EyBPBYxsATRhXs84mqVewA14yVxeHqtPWiMAieVPYvpRb"
consumer_key = "FaMiOPzjvFZL9RvHYTq5eFlad"
consumer_secret = "rxbssYK7uY6nQlglo3aVefQL7zJEcXILe9YmK5Aa5Tikz91Yfk"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('brengsek + since:2022-04-06 until:2022-04-07 lang:in').get_items()):
    id = tweet.id
    if(id==None or id==''):
        continue
    getTweet = api.get_status(id, wait_on_rate_limit=True, wait_on_rate_limit_notify = True, tweet_mode='extended')
    json_str = json.dumps(getTweet._json)
    print(json_str)
    collection.insert_one(getTweet._json)
    #
    # geocode: -8.3919, 115.18756, 1000km

