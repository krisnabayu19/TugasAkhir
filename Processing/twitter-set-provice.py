from pymongo import MongoClient
from collections import Counter
import pymongo
import operator
from yandex.Translater import Translater
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from textblob import TextBlob
import re
import string
import json

# Connection to MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["testimport"]
mycol = mydb["tweetsAnalyticsFix"]


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://localhost:27017/' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    return df


if __name__ == '__main__':
    rty = read_mongo('testimport', 'tweetsAnalytics', {})

    stop_words = ['Kota','Kabupaten','City','Regency']


    # Looping for Analytics
    for index, row in rty.iterrows():

        locationTweet = row['place_object']
        final_words = []
        city_list = []
        province_list = []
        city_data = []


        if not locationTweet:
            print("Tidak Ada Lokasi")
            locationFix = "null"
        else:
            print("Ada Lokasi")
            locationName = row['place_object']['name']
            cleaned_text = locationName.translate(str.maketrans('', '', string.punctuation))
            tokenized_words = cleaned_text.split()

            # Looping text to stop word
            for cleaned_text1 in tokenized_words:
                if cleaned_text1 not in stop_words:
                    final_words.append(cleaned_text1)

            strAppnd = ' '.join(final_words)
            city_data.append(strAppnd)

            print(city_data)
            strCity = ''.join(city_data)


            with open('provinsifix.csv', 'r') as file:
                for line in file:

                    clear_line = line.replace("\n", '').strip()
                    city, province = clear_line.split(',')

                    if city in city_data:
                        # Emotion Label to Emotion List
                        province_list.append(province)

                        # Emotion Word to Word Array
                        city_list.append(city)

                strProvince = ''.join(province_list)

            # If condition check in array list city
            if not city_list:
                locationFix = strCity
                print(locationFix)
                print("===========================================")

            else:
                locationFix = strProvince
                print(locationFix)
                print("===========================================")

        # Variable After Cleanning Tweets
        mongo = {
            "id": row["id"],
            "created_at": row["created_at"],
            "followers": row["followers"],
            "text":row["text"],
            "text_emotion":row["text_emotion"],
            "locations": locationFix,
            "place_object":row['place_object'],
            "language": row["language"]
        }
        #


        # Save to MongoDB
        x = mycol.insert_one(mongo)




