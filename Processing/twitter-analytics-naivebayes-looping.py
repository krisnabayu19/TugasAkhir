import numpy as np
import texttable as tt
import csv
from pymongo import MongoClient
import pymongo
import pandas as pd


# Connection to MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["testimport"]
mycol = mydb["tweetsAnalytics"]


# Training data set
# TRAINING_DATA = [["restaurant review", "classification"],
#                  ["gembira", "+"],
#                  ["senang", "+"],
#                  ["terpesona", "+"],
#                  ["berterimakasih", "+"],
#                  ["optimis", "+"],
#                  ["murung", "-"],
#                  ["sedih", "-"],
#                  ["menangis", "-"],
#                  ["hancur", "-"],
#                  ["frustasi", "-"]]

with open('testDataTrain5.csv', newline='') as csvfile:
    TRAINING_DATA = list(csv.reader(csvfile))

class NaiveBayes:
    def __init__(self, data, vocab):
        self._displayHelper = DisplayHelper(data,vocab)
        self._vocab = vocab
        labelArray = []
        for i in range(1, len(data)):
            labelArray.append(data[i][1])
        self._label = np.array(labelArray)
        docArray = []
        for i in range(1, len(data)):
            docArray.append(self.map_doc_to_vocab(data[i][0].split()))
        self._doc = np.array(docArray)
        self.calc_prior_prob().calc_cond_probs()

    def calc_prior_prob(self):
        sum = 0
        for i in self._label:
            if ("-".__eq__(i)) : sum += 1;
        self._priorProb = sum / len(self._label)
        self._displayHelper.set_priors(sum, len(self._label))
        #
        return self

    def calc_cond_probs(self):
        pProbNum = np.ones(len(self._doc[0])); nProbNum = np.ones(len(self._doc[0]))
        pProbDenom = len(self._vocab); nProbDenom = len(self._vocab)
        for i in range(len(self._doc)):
            if "-".__eq__(self._label[i]):
                nProbNum += self._doc[i]
                nProbDenom += sum(self._doc[i])
            else:
                pProbNum += self._doc[i]
                pProbDenom += sum(self._doc[i])
        self._negProb = np.log(nProbNum / nProbDenom)
        self._posProb = np.log(pProbNum / pProbDenom)
        self._displayHelper.display_calc_cond_probs(nProbNum, pProbNum, nProbDenom, pProbDenom)

        return self

    def classify(self, doc):
        global sentiment
        sentiment = "-"
        nLogSums = doc @ self._negProb + np.log(self._priorProb)
        pLogSums = doc @ self._posProb + np.log(1.0 - self._priorProb)
        self._displayHelper.display_classify(doc, pLogSums, nLogSums)
        if pLogSums > nLogSums:
            sentiment = "Bahagia"

        if pLogSums < nLogSums:
            sentiment = "Tidak Bahagia"

        if pLogSums == nLogSums:
            sentiment = "Netral"
        return "text classified as expressing ("+ sentiment+ ") emotion\n""=========================================="


    def map_doc_to_vocab(self, doc):
        mappedDoc = [0] * len(self._vocab)
        for d in doc:
            counter = 0
            for v in self._vocab:
                if (d.__eq__(v)): mappedDoc[counter] += 1
                counter += 1
        return mappedDoc


class DisplayHelper:
    def __init__(self, data, vocab):
        self._vocab = vocab
        self.print_training_data(data)
    def print_training_data(self, data):
        table = tt.Texttable()
        table.header(data[0])
        for i in range(1, data.__len__()): table.add_row(data[i])

        # Display Data Training
        # print(table.draw().__str__())

    def set_priors(self, priorNum, priorDenom):
        self._priorNum = priorNum
        self._priorDenom = priorDenom
    def display_classify(self, sentiment, posProb, negProb):

        # Positif
        temp = "logprior + loglikelihood of (Bahagia) emotion = ln("+ \
               (self._priorDenom - self._priorNum).__str__()+ "/"+ self._priorDenom.__str__()+ ")"
        for i in range(0, len(sentiment)):
            if sentiment[i] == 1 :
                temp = temp.__add__(" + ln("+(int)(self._pProbNum[i]).__str__()
                                    + "/" + self._pProbDenom.__str__()+")")
        print(temp,"=",posProb)


        # Negatif
        temp = "logprior + loglikehood of (Tidak Bahagia) emotion = ln("+ self._priorNum.__str__()\
                                    + "/"+ self._priorDenom.__str__()+ ")"
        for i in range(0, len(sentiment)):
            if sentiment[i] == 1:
                temp = temp.__add__(" + ln("+ (int)(self._nProbNum[i]).__str__()
                                    + "/" + self._nProbDenom.__str__()+")")
        print(temp, "=", negProb)

        print("prior + likelihood of (Bahagia) emotion = ", np.exp(posProb))
        print("prior + likelihood of (Tidak Bahagia) emotion = ", np.exp(negProb))
        # print("prob of (Bahagia) emotion = ", np.exp(posProb) / (np.exp(posProb) + np.exp(negProb)))
        # print("prob of (Tidak Bahagia) emotion = ", np.exp(negProb) / (np.exp(posProb) + np.exp(negProb)))
        # print(np.exp2(posProb))
        # print(np.exp2(negProb))
        # print(posProb)
        # print(negProb)

    def display_calc_cond_probs(self, nProbNum, pProbNum, nProbDenom, pProbDenom):
        nProb = []
        nProb.append("P(w|Tidak Bahagia)")
        for i in range (0, len(self._vocab)):
            nProb.append((int)(nProbNum[i]).__str__()+"/"+nProbDenom.__str__())
        pProb = []
        pProb.append("P(w|Bahagia)")
        for i in range (0, len(self._vocab)):
             pProb.append((int)(pProbNum[i]).__str__()+ "/" + pProbDenom.__str__())
        tempVocab = []
        tempVocab.append("")
        for i in range(0, len(self._vocab)) : tempVocab.append(self._vocab[i])

        # Limit table row
        table = tt.Texttable(1000000)

        table.header(tempVocab)
        table.add_row(pProb)
        table.add_row(nProb)

        # Display Probabilitas Data Training
        # print(table.draw().__str__())

        self._nProbNum = nProbNum; self._pProbNum = pProbNum
        self._nProbDenom = nProbDenom; self._pProbDenom = pProbDenom


def prepare_data():
    data = []
    for i in range(0, len(TRAINING_DATA)):
        data.append([TRAINING_DATA[i][0].lower(), TRAINING_DATA[i][1]])
    return data


def prepare_vocab(data):
    vocabSet = set([])
    for i in range(1, len(data)):
        for word in data[i][0].split(): vocabSet.add(word)
    return list(vocabSet)

if __name__ == '__main__':

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

    read = read_mongo('tweetsClean', 'tweetsCleanJuli2020New', {})


    # def prepare_data():
    #     data = []
    #     for i in range(0, len(TRAINING_DATA)):
    #         data.append([TRAINING_DATA[i][0].lower(), TRAINING_DATA[i][1]])
    #     return data
    #
    #
    # def prepare_vocab(data):
    #     vocabSet = set([])
    #     for i in range(1, len(data)):
    #         for word in data[i][0].split(): vocabSet.add(word)
    #     return list(vocabSet)


    # data = prepare_data()
    # handle_command_line(NaiveBayes(data, prepare_vocab(data)))


    # Looping for Analytics
    for index, row in read.iterrows():

        # Select field row to analytics
        textTweet = row['text']
        print("Text Tweet :",textTweet)

        def handle_command_line(nb):
            print(nb.classify(np.array(nb.map_doc_to_vocab(textTweet.lower().split()))))

        # def prepare_data():
        #     data = []
        #     for i in range(0, len(TRAINING_DATA)):
        #         data.append([TRAINING_DATA[i][0].lower(), TRAINING_DATA[i][1]])
        #     return data
        #
        # def prepare_vocab(data):
        #     vocabSet = set([])
        #     for i in range(1, len(data)):
        #         for word in data[i][0].split(): vocabSet.add(word)
        #     return list(vocabSet)

        data = prepare_data()
        handle_command_line(NaiveBayes(data, prepare_vocab(data)))

        # # Variable After Cleanning Tweets
        mongo = {
            "id": row["id"],
            "created_at": row["created_at"],
            "followers": row["followers"],
            "text": textTweet,
            "text_emotion": sentiment,
            "place_object":row['place_object'],
            "language": row["language"]
        }

        # print(mongo)


        # Save to MongoDB
        # x = mycol.insert_one(mongo)



