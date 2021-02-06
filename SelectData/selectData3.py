import pymongo
from collections import Counter
import re
import pandas as pd
import csv

# Connection to MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["testimport"]
mycol = mydb["tweetsAnalyticsFix"]
# mysave = mydb["tweetsJul-Aug"]

emotion = []
# wordArray = []
# textArray = []

if __name__ == "__main__":
    # wordArray = []

    # Looping for Selecting Coloumn we Needed
    print("Start")
    # test3 = "test"
    # f = open("tesct.csv", "w")
    # for tweet in mycol.find({"created_at" : { "$regex": 'Aug 06.*' }}):
    # global wordArray2 = []
    # final_words = []
    word_array = []
    for tweet in mycol.find(
            {"created_at": {"$regex": 'Dec 19.*'}, "text_emotion": "Tidak Bahagia", "place_object.country_code": "ID",
             "language": "in"}):

        text = tweet["text"]
        # print(text)

        # Tokenizing Tweet
        tokenized_words = text.split()

        final_words = []
        # word_array = []
        for word in tokenized_words:
            final_words.append(word)
        # print("Array Tweets :",final_words)

        with open('emotiondatasettidakbahagia.csv', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').strip()
                word, emotion = clear_line.split(',')
                # print(word)

                # Compare Emotion Data Training an Data Testing, and Add to Array
                if word in final_words:
                    word_array.append(word)

            # print(word_array)
            # count_word = Counter(word_array)
            # print(count_word)
            # count_word1 = pd.Series(count_word)

    # tweets = {
    #     "id" :tweet["id"],
    #     "created_at": tweet["created_at"],
    #     "text": tweet["text"],
    #     "text_emotion": tweet["text_emotion"]
    # }
    # label = tweet["text_emotion"]
    # emotion.append(label)
    # print(tweets)
    # test2 = test3
    # test.append(test2)

countEmotion = Counter(word_array)
countWord = pd.Series(countEmotion)
print("Jumlah Emosi :\n",countWord)
print("End")



