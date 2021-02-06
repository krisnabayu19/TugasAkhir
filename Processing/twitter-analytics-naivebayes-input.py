import numpy as np
import texttable as tt
import csv
from pymongo import MongoClient
import pymongo
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import string
import json


# TRAINING_DATA = [["text", "label"],
#                  ["chinese beijing chinese", "+"],
#                  ["chinese chinese sanghai", "+"],
#                  ["chinese macao", "+"],
#                  ["tokyo japan chinese", "-"]]

# TRAINING_DATA = [["text", "label"],
#                  ["gembira medengar kabarmu hari ini", "+"],
#                  ["senang melihat karya anda", "+"],
#                  ["nisa bersuka cita karena nilai ujian nasionalnya sangat tinggi", "+"],
#                  ["gembira sekali anda terlihat hari ini", "+"],
#                  ["bahagia mendengar kabarmu", "+"],
#                  ["ceria sekali kamu terlihat hari ini", "+"],
#                  ["kagum akan prestasimu", "+"],
#                  ["nisa puas dengan hasil yang sudah saya capai", "+"],
#                  ["geria suka padamu", "+"],
#                  ["terpesona dan jatuh cinta ku jadinya", "+"],
#                  ["daniel sudah berkecil hati terlebih dahulu sebelum dia mengikuti perlombaan", "-"],
#                  ["anita merasa malu karena mendapat nilai jelek", "-"],
#                  ["wisnu sangat kasihan dengan nenek itu", "-"],
#                  ["wajahnya yang biasa tam-pak berseri berubah menjadi murung", "-"],
#                  ["rasa pilu melihat teman baik teraniaya", "-"],
#                  ["reza sedih melihat rekaman video tadi, itu benar-benar menyentuh hati", "-"],
#                  ["kami dan keluarga turut berduka cita atas meninggalnya almarhum", "-"],
#                  ["sakit hati dan kecewa terkadang tidak bisa diungkapkan dengan kata-kata", "-"],
#                  ["patah hati adalah sebuah perasaan kecewa sedih marah resah yang rasanya hampir dirasakan semua orang", "-"],
#                  ["kiki prihatin melihat kondisi anak itu", "-"]]

# TRAINING_DATA = [["text", "label"],
#                  ["saya senang hari ini", "+"],
#                  ["bahagia deh hari ini", "+"],
#                  ["semangat ya sayang", "+"],
#                  ["saya merasa cemas", "-"],
#                  ["iri bilang bos", "-"],
#                  ["kecewa mendengar perkataanmu", "-"]]

with open('data-after-training.csv', newline='') as csvfile:
    TRAINING_DATA = list(csv.reader(csvfile))


class NaiveBayes:

    def __init__(self, data, vocab):
        self._displayHelper = DisplayHelper(data,vocab)
        self._vocab = vocab

        # LabelArray
        labelArray = []
        for i in range(1, len(data)):
            labelArray.append(data[i][1])
        self._label = np.array(labelArray)

        # LabelText
        docArray = []
        for i in range(1, len(data)):
            docArray.append(self.map_doc_to_vocab(data[i][0].split()))
        self._doc = np.array(docArray)
        self.calc_prior_prob().calc_cond_probs()


    def calc_prior_prob(self):
        sum = 0

        # Laplacian Smoothing
        for i in self._label:
            if ("-".__eq__(i)) : sum += 1;
        self._priorProb = sum / len(self._label)
        self._displayHelper.set_priors(sum, len(self._label))
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



    # Function classify label sentiment
    def classify(self, doc):
        sentiment = "-"
        nLogSums = doc @ self._negProb + np.log(self._priorProb)
        pLogSums = doc @ self._posProb + np.log(1.0 - self._priorProb)
        self._displayHelper.display_classify(doc, pLogSums, nLogSums)
        if pLogSums > nLogSums:
            sentiment = "Happy Emotion"

        if pLogSums < nLogSums:
            sentiment = "Unhappy Emotion"

        if pLogSums == nLogSums:
            sentiment = "Netral"
        return "text classified as ("+ sentiment+ ") label"



    def map_doc_to_vocab(self, doc):
        mappedDoc = [0] * len(self._vocab)
        for d in doc:
            counter = 0
            for v in self._vocab:
                if (d.__eq__(v)): mappedDoc[counter] += 1
                counter += 1
        return mappedDoc



# Class display
class DisplayHelper:
    def __init__(self, data, vocab):
        self._vocab = vocab
        self.print_training_data(data)

    def print_training_data(self, data):
        table = tt.Texttable()
        table.header(data[0])
        for i in range(1, data.__len__()): table.add_row(data[i])

        # Print table data training
        # print(table.draw().__str__())

    def set_priors(self, priorNum, priorDenom):
        self._priorNum = priorNum
        self._priorDenom = priorDenom


    def display_classify(self, sentiment, posProb, negProb):

        # # Positive
        # temp = "logprior + loglikelihood of (+) sentiment = ln("+ \
        #        (self._priorDenom - self._priorNum).__str__()+ "/"+ self._priorDenom.__str__()+ ")"
        # for i in range(0, len(sentiment)):
        #     if sentiment[i] == 1 :
        #         temp = temp.__add__(" x ln("+(int)(self._pProbNum[i]).__str__()
        #                             + "/" + self._pProbDenom.__str__()+")")
        # # print(temp,"=",posProb)
        # print(temp)
        # #
        # #
        # # # Negative
        # temp = "logprior + loglikehood of (-) sentiment = ln("+ self._priorNum.__str__()\
        #                             + "/"+ self._priorDenom.__str__()+ ")"
        # for i in range(0, len(sentiment)):
        #     if sentiment[i] == 1:
        #         temp = temp.__add__(" x ln("+ (int)(self._nProbNum[i]).__str__()
        #                             + "/" + self._nProbDenom.__str__()+")")
        # # print(temp, "=", negProb)
        # print(temp)

        # N-Gram Feature
        # Positive
        temp = "N-Gram Data Training Happy Emotion Label = ("+ \
               (self._priorDenom - self._priorNum).__str__()+ "/"+ self._priorDenom.__str__()+ ")"
        for i in range(0, len(sentiment)):
            if sentiment[i] == 1 :
                temp = temp
        print(temp)


        # Negative
        temp = "N-Gram Data Training Unhappy Emotion Label = ("+ self._priorNum.__str__()\
                                    + "/"+ self._priorDenom.__str__()+ ")"
        for i in range(0, len(sentiment)):
            if sentiment[i] == 1:
                temp = temp
        print(temp)








        # Probabilitas sentiment Naive Bayes Method
        print("Probabilitas of (Happy Emotion) = ", np.exp(posProb))
        print("Probabilitas of (Unhappy Emotion) = ", np.exp(negProb))



        # print("prob of (+) sentiment = ", np.exp(posProb) / (np.exp(posProb) + np.exp(negProb)))
        # print("prob of (-) sentiment = ", np.exp(negProb) / (np.exp(posProb) + np.exp(negProb)))


    def display_calc_cond_probs(self, nProbNum, pProbNum, nProbDenom, pProbDenom):

        # Array Calculation Negatif Data
        nProb = []
        nProb.append("P(w|Unhappy Emotion)")
        for i in range (0, len(self._vocab)):
            nProb.append((int)(nProbNum[i]).__str__()+"/"+nProbDenom.__str__())

        # Array Calculation Positif Data
        pProb = []
        pProb.append("P(w|Happy Emotion)")
        for i in range (0, len(self._vocab)):
             pProb.append((int)(pProbNum[i]).__str__()+ "/" + pProbDenom.__str__())

        tempVocab = []
        tempVocab.append("")
        for i in range(0, len(self._vocab)) : tempVocab.append(self._vocab[i])

        # Limit row table
        table = tt.Texttable(1000000)
        table.header(tempVocab)
        table.add_row(pProb)
        table.add_row(nProb)

        # print table calculation data training
        print(table.draw().__str__())

        self._nProbNum = nProbNum; self._pProbNum = pProbNum
        self._nProbDenom = nProbDenom; self._pProbDenom = pProbDenom

# Function to Clean
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|(_[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|"
                           "(\s([@#][\w_-]+)|(#\\S+))|((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))", " ", tweet).split())


# Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

stopwords = []
stopwords_list = []
data_input = []



if __name__ == '__main__':

    # Function input command line
    def handle_command_line(nb):
        flag = True
        while (flag):
            # entry = input("Input Text : ")

            data1 = input("> Input Text : ")
            data_input.append(data1)
            data = data_input

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

                print("Text Clean :", blob)
                print("Text Lower Case :", lower_case)
                print("Text Stemming :", hasilStemmer)
                print("Text After Stop Word :", strAppnd)
                entryData = strAppnd
                print("===============================================================================================")
                entry = entryData

            if (entry!= "exit"):
                print(nb.classify(np.array(nb.map_doc_to_vocab(entry.lower().split()))))
            else:
                flag = False

    # Prepare data training to lower case
    def prepare_data () :
        data = []
        for i in range (0, len(TRAINING_DATA)):
            data.append([TRAINING_DATA[i][0].lower(), TRAINING_DATA [i][1]])
        return data

    # Prepare to compare data training Naive Bayes
    def prepare_vocab(data) :
        vocabSet = set([])
        for i in range(1, len(data)):
            for word in data [i][0].split(): vocabSet.add(word)
        return list(vocabSet)
    data = prepare_data()
    handle_command_line(NaiveBayes(data, prepare_vocab(data)))
