import json
import snscrape.modules.twitter as sntwitter
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler

client = MongoClient('localhost', 27017)
db = client['testimport']
collection = db['tweetsAug16']

# consumer_key = 'yoIwFkjZGYDa49aO16XqSNqcN'
# consumer_secret = 'gl4LQOItV7Z1aFwNrlvaiKJ3t8o8h99blMIAmnmdHxYjzjRAxO'
# access_token = '624310916-E7fDF2IE8P6bfY1oVFglASf6F8RnxMd3vgSXFqnZ'
# access_token_secret = 'ID9JcoXHsDcKtvNcnmBGcCQhUlO0wmwAxBJ6LCesiUAas'

consumer_key = 'YvfuzG3IaSfOnAdsd7CZFXyO7'
consumer_secret = 'UtTb9GvjXfQ3WHSgl1FkCO16AEwynPvVb4EfkCigQMvfMryrFT'
access_token = '1116904069975511041-lSrhUOPRnlPXJ6VRkyMi3dQgy7GcL8'
access_token_secret = '9DBdN1waJvIPhgpIEaocFPMVHOLX6IZuSnGhyBmlBmg2u'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

last_id: int = 128681341227028889617281737
# last_id: int = 1291524444712652801
while True :
    try :

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper('since:2020-08-20 until:2020-08-21 + lang:in').get_items()):

            id = tweet.id
            print("id = ", id)
            print("last id", last_id)
            if last_id <= id:
                print("sudah diambil")
                continue
            else :
                last_id = id
                getTweet = api.get_status(id, wait_on_rate_limit=True, tweet_mode='extended')
                json_str = json.dumps(getTweet._json)
                print(json_str)
                # collection.insert_one(getTweet._json)
                continue

    except:
        print("Data tidak masuk")