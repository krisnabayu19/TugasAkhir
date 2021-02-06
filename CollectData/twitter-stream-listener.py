import tweepy
import json
from pymongo import MongoClient
import pymongo

# Connection to MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["indonesia"]
mycol = mydb["tweetsdata"]

# Class Streaming
class StreamListener(tweepy.StreamListener):

    # Connected
    def on_connect(self):
         print("You're connected to the streaming server.")

    # Not Connected
    def on_error(self, status_code):
        print('Error: ' + repr(status_code))
        return False

    # Save Data to MongoDB
    def on_data(self, data):

        client = MongoClient()
        db = client.training_tweets

        # Save Data JSON Format
        datajson = json.loads(data)
        print(datajson)
        # mycol.save(datajson)


if __name__ == "__main__":

    # Twitter API
    # consumer_key = "YvfuzG3IaSfOnAdsd7CZFXyO7"
    # consumer_secret = "UtTb9GvjXfQ3WHSgl1FkCO16AEwynPvVb4EfkCigQMvfMryrFT"
    # access_token = "1116904069975511041-lSrhUOPRnlPXJ6VRkyMi3dQgy7GcL8"
    # access_token_secret = "9DBdN1waJvIPhgpIEaocFPMVHOLX6IZuSnGhyBmlBmg2u"
    access_token = "1325627047662641155-fuAD0pgWVjPgt51g6GUj5kXziXOKno"
    access_token_secret = "KUlniVkgOS6aXW0RhojvYovHnUTtjSxOgQTzEnYw6vzw2"
    consumer_key = "ywkfwFy7IOS9nVJovtMxG0YsB"
    consumer_secret = "RQTlsTom6049Kf0ZhnNczcVqT3sndfNYXF23kLkiecIJPWIpp9"

    # Access Twitter API
    auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth1.set_access_token(access_token, access_token_secret)

    # Variable Coordinate Location
    LOCATIONS = [95.31644, -10.1718, 140.71813, 5.88969]
    # [west_long south_lat east_long north_lat]

    # Variable Language
    language =['in']

    # Function Streaming with Filtering Language and Location
    stream_listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    stream = tweepy.Stream(auth=auth1, listener=stream_listener)
    stream.filter(languages=language,locations=LOCATIONS)