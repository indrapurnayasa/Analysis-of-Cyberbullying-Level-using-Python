#IMPORT LIBRARY
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.svm import LinearSVC
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['databaseName']
collection = db['collectionName']

dbStore = client['databaseStoreName']
collectionStore = dbStore['collectionStoreName']

#Membaca Data Training
data = pd.read_csv('fileCSV.csv', sep=',', encoding='latin-1')

#Model Klasifikasi
Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(data['text'],data['label'],test_size=0.1)

Tfidf_vect = TfidfVectorizer()
Tfidf_vect.fit(data['text'])

Train_X_Tfidf = Tfidf_vect.transform(Train_X)

svm = LinearSVC()
svm.fit(Train_X_Tfidf, Train_Y)

def classify(tweet):
    pred = svm.predict(Tfidf_vect.transform([tweet]))
    if pred == 1:
        return "Cyberbullying"
    return "Non-cyberbullying"

result = collection.find()
i = next(result, None)
for i in result:
    text = i['text']
    kelas = classify(text)
    mongo = {
        "date": i['date'],
        "text": i['text'],
        "klasifikasi": kelas,
        "location": i['location'],
        "language": i['language']
    }
    print("Tweet yang akan di prediksi :", text)
    print("Tweet tersebut masuk ke dalam klasifikasi :", kelas)
    print(mongo)
    print("===============================================================================")
    collectionStore.insert_one(mongo)


