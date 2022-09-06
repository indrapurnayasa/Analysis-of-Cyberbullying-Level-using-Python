import json
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

qry = input("Masukkan Query yang akan anda cari :")
countKeyword=100

tweet = tweepy.Cursor(api.search, q=qry, lang="in",tweet_mode='extended',
                      since='yyyy-mm-dd',until='yyyy-mm-dd', #max 7 days
                      count='countKeyword', wait_on_rate_limit=True).items(10000)

for tweets in tweet:
    json_str = json.dumps(tweets._json)
    print(json_str)
    collection.insert_one(tweets._json)

