import json
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler

client = MongoClient('localhost', 27017)
db = client['cyberbullyingMei']
collection = db['cyberbullyingIdiot']

access_token = "250996215-cRefKugh80cVxnQATGMjoXvHGKf0oQ1CvEbQ42tu"
access_token_secret = "plwBZRnSyrW2ugUQRHU7WOK7KzrHG6I8eCwunpk9gdazC"
consumer_key = "OB1ur1Q3NumIvPkpcSc6haGc3"
consumer_secret = "BzWvPKQy66q7o9N9NVyoTXYdjw100CGMybOvb19bbUc75M1zih"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

qry = input("Masukkan Query yang akan anda cari :")
countKeyword=100

tweet = tweepy.Cursor(api.search, q=qry, lang="in",tweet_mode='extended',
                      since='2022-05-01',until='2022-05-04',
                      count='countKeyword', wait_on_rate_limit=True).items(10000)

for tweets in tweet:
    json_str = json.dumps(tweets._json)
    print(json_str)
    collection.insert_one(tweets._json)

