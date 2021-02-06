from pymongo import MongoClient
import pymongo
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import string
import json
import csv

# Connection to MongoDB
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["tweetsKotor"]
# mycol = mydb["testClean"]

# Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

f = open("trainingDataFeb.csv", "w")

stopwords = []
stopwords_list = []

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://localhost:27017/' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

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

# Function to Clean
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|(_[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|"
                           "(\s([@#][\w_-]+)|(#\\S+))|((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))", " ", tweet).split())

# def clean_stopword(tweet) :


data_input = []


if __name__ == '__main__':
    # df = read_mongo('indonesia', 'test7', {})

    # df = pd.read_csv(r"testDataTrain7.csv", encoding='latin-1')  # Read CSV
    # # f = open("trainingData.csv", "w")
    # # df = pd.read_csv(r"testdata3.csv", encoding='latin-1')  # Read CSV
    #
    # data = df['Tweet']
    
    data1 = input("Input Text :")
    data_input.append(data1)
    data = data_input

    # Kata-Kata yang di Stop Word
    # stopwords = ['saya','kamu','dia','kita','mereka','kami','dan','atau','sebaliknya','pada','dalam','untuk','dari','kepada','terhadap','oleh','tetapi','juga','karena','seperti','ya','yg', 'yang', 'serta', 'cuma']

    with open('stopwordsfix.csv', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').strip()
            stopwords.append(clear_line)


    for index, entry in enumerate(data):
        

        #  get Tweet Kotor
        test = entry
        final_words = []
        after_stopwords = []

        print("Text Tweet :", test)
        # print(row['text'])

        # Pengurangan karakter ke n
        # n = len(test)
        # ges = test[0:n - 0]
        # print("Pengurangan Character :",ges)

        # toLowerCase Character
        gas = test.strip()
        blob = clean_tweet(gas)

        lower_case = clean_tweet(gas).lower()
        cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
        tokenized_words = cleaned_text.split()

        hasil = stemmer.stem(blob)
        hasilStemmer = stemmer.stem(hasil)

        cleaned_text1 = hasilStemmer.translate(str.maketrans('', '', string.punctuation))
        tokenized_words1 = cleaned_text1.split()
        # print(tokenized_words1)

        # # Looping text to stop word
        for tokenized_words2 in tokenized_words1:
            # print(tokenized_words2)
            if tokenized_words2 not in stopwords:
                # print(tokenized_words2)
                stopwords_list.append(stopwords)
                after_stopwords.append(tokenized_words2)

        strAppnd = ' '.join(after_stopwords)
        # print(strAppnd)


        print("Text Clean :",blob)
        print("Text Lower Case :", lower_case)
        print("Text Stemming :",hasilStemmer)
        print("Text After Stop Word :",strAppnd)

        test = str(strAppnd)
        f.write(test)
        f.write('\n')
        print("=========================================")






