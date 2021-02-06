# Twitter API authentication

import tweepy
import json
import pymongo
from pymongo import MongoClient


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["indonesia"]
mycol = mydb["tweetsJanuari09-end"]

api_key ='YvfuzG3IaSfOnAdsd7CZFXyO7'
api_secret_key ='UtTb9GvjXfQ3WHSgl1FkCO16AEwynPvVb4EfkCigQMvfMryrFT'
access_token ='1116904069975511041-lSrhUOPRnlPXJ6VRkyMi3dQgy7GcL8'
access_token_secret ='9DBdN1waJvIPhgpIEaocFPMVHOLX6IZuSnGhyBmlBmg2u'

authentication = tweepy.OAuthHandler(api_key, api_secret_key)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication)

user = "AnalyticsVidhya"
LOCATIONS = [95.31644, -10.1718, 140.71813, 5.88969]
language = ['in']
# public_tweet = api.geo_search(query="ID",granularity="country",count=5)
# public_tweet = api.user_timeline(id=user,count=5)
places = api.geo_search(query="Indonesia", granularity="country")

# last_id: int = 1289348324026249216
last_id: int = 128681341227028889617281737
# last_id: int = 1348134433455394818
while True :
    try:
        for place in places:
            print("placeid:%s" % place)
            public_tweets = tweepy.Cursor(api.search, count=100, q="place:%s" % place.id, since="2018-06-09",
                                          show_user=True, tweet_mode="extended").items()
            for tweet in public_tweets:
                id = tweet.id
                print("id = ", id)
                print("last id", last_id)


                if last_id <= id:
                    print("sudah diambil")
                    continue
                else:
                    last_id = tweet.id
                    json_str = json.dumps(tweet._json)
                    print(json_str)
                    # mycol.insert_one(tweet._json)
                    continue
    except:
        print("Data Tidak Masuk")







