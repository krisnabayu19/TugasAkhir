import pymongo
from collections import Counter
import re
import csv
import json

# Connection to MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tweetsKotor"]
mycol = mydb["tweetsData3"]
mysave = mydb["tweetsDesember2020"]

emotion = []
test = []


if __name__ == "__main__":

  # Looping for Selecting Coloumn we Needed
  print("Start")
  for tweet in mycol.find({"created_at" : { "$regex": 'Dec.*' }}):

      print(tweet)
      mysave.insert_one(tweet)

  print("End")