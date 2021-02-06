import re
import string
import joblib
import pandas as pd
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk import pos_tag, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.metrics import confusion_matrix, recall_score, precision_score, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, svm, metrics
from sklearn.naive_bayes import MultinomialNB
import pymongo

np.random.seed(500)
# Stopword Sastrawii
# stop_factory = StopWordRemoverFactory()
# stopword = stop_factory.create_stop_word_remover()
# print(stopword)
#
stopwords = []

# f = open("trainingDataFeb.csv", "w")
# f = open("trainingDataNew.csv", "w", encoding="utf-8")
# with io.open(fname, "w", encoding="utf-8") as f

with open('stopwordsfix.csv', 'r') as file:
    for line in file:
        clear_line = line.replace("\n", '').strip()
        stopwords.append(clear_line)
    # print(stopwords)

# Stopword NLTK
factory = StemmerFactory()
# stopwordsNLTK = set(stopwords.words('english'))

# Stemmer NLTK
ps = PorterStemmer()
# Lemmatization
lemmatizer = WordNetLemmatizer()
# Stemming Sastrawii
stemmerSastrawii = factory.create_stemmer()



# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["indonesia"]
# mycol = mydb["test7"]
# mycol2 = mydb["test8"]




df = pd.read_csv(r"all-dataset-1.csv", encoding='latin-1')  # Read CSV
# df = pd.read_csv(r"testdata3.csv", encoding='latin-1')  # Read CSV

data = df['Tweet']
data = [re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', str(entry)) for entry in data]  # remove url
data = [re.sub('@[^\s]+', '', entry) for entry in data]  # remove mentions
data = [re.sub('([#])|([^a-zA-Z])([RT])', ' ', entry) for entry in data]  # hashtag & RT
data = [entry.translate(str.maketrans("", "", string.punctuation)) for entry in data]  # remove punctuation
data = [re.sub(r'\d+', '', entry).lower().split() for entry in data]  # remove numbers lowercase split

# Stopword & Stemming
for index, entry in enumerate(data):
    print("Text Before Cleaning",entry)


    Final_words = []
    for word, tag in pos_tag(entry):
        if word not in stopwords:
            Final_words.append(word)





        # Final_words.append(word)
    #     if stopwords.remove(word):
    #         word = stemmerSastrawii.stem(word)
    #         Final_words.append(word)
    strAppnd = ' '.join(Final_words)
    # test = str(strAppnd)
    print("Text Cleaning :",strAppnd)
    # f.write(strAppnd)
    # f.write('\n')








    # res = df.loc[index, 'Tweet'] = str(Final_words)
    # print("Text Cleaning", res)
    print("===========================================================================================================")


# Split Data Train & Data Test
Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(df['Tweet'], df['Label'], test_size=0.10)
# Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(textArrayPredict, labelArrayTrue, test_size=0.30)

# mengubah kelas menjadi angka
Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)

# TF-IDF
Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(df['Tweet'])
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

# Klasifikasi Metode SVM
# SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
# SVM.fit(Train_X_Tfidf, Train_Y)
# predictions_SVM = SVM.predict(Test_X_Tfidf)
#
# print("\nAkurasi SVM = ", metrics.accuracy_score(Test_Y, predictions_SVM) * 100)
# # cm_svm = confusion_matrix(Test_Y, predictions_MNB)
# # print("Confusion Matrix SVM\n", cm_svm)
# precision_svm = precision_score(Test_Y, predictions_SVM) * 100
# print("Precision SVM = ", precision_svm)
# recall_score_svm = recall_score(Test_Y, predictions_SVM, average='weighted') * 100
# print("Recall Score SVM = ", recall_score_svm)
# f1_score_svm = f1_score(Test_Y, predictions_SVM) * 100
# print("F1 Score SVM = ", f1_score_svm)

# Klasifikasi Metode MNB
clf = MultinomialNB()
clf.fit(Train_X_Tfidf, Train_Y)
predictions_MNB = clf.predict(Test_X_Tfidf)

print("\nAkurasi MNB = ", metrics.accuracy_score(Test_Y, predictions_MNB) * 100)
# cm_svm = confusion_matrix(Test_Y, predictions_MNB)
# print("Confusion Matrix SVM\n", cm_svm)
precision_mnb = precision_score(Test_Y, predictions_MNB) * 100
print("Precision MNB = ", precision_mnb)
recall_score_mnb = recall_score(Test_Y, predictions_MNB, average='weighted') * 100
print("Recall Score MNB = ", recall_score_mnb)
f1_score_mnb = f1_score(Test_Y, predictions_MNB) * 100
print("F1 Score MNB = ", f1_score_mnb)

# Save the trained model as a pickle string.
# joblib.dump(SVM, 'SVM model hatespech.pkl')