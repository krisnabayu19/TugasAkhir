import pymongo
from collections import Counter
import re
import csv

# Connection to MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["indonesia"]
mycol = mydb["tweetsanalyticsfix"]
# mysave = mydb["tweetsJul-Aug"]

emotion = []
test = []

if __name__ == "__main__":

    # Looping for Selecting Coloumn we Needed
    print("Start")
    test3 = "test"
    # f = open("tesct.csv", "w")
    for tweet in mycol.find({"text" : { "$regex": 'psbb.*' },"text_emotion": "Tidak Bahagia", "place_object.country_code": "ID", "locations" : "Jawa Barat"}):
        # for tweet in mycol.find(
        #         {"created_at": {"$regex": 'Sep 02.*'}, "text_emotion": "Tidak Bahagia", "place_object.country_code": "ID", "language":"in", "text": {"$regex": 'duka.*'}}):
        #
        #     text = tweet["text"]
        #     print(text)

        tweets = {
            "id": tweet["id"],
            "created_at": tweet["created_at"],
            "text": tweet["text"]
        }

        label = tweet["text_emotion"]
        emotion.append(label)
        print(tweets)
        # test2 = test3
        # test.append(test2)

    countEmotion = Counter(emotion)
    print("Jumlah Emosi :", countEmotion)
    print("End")

