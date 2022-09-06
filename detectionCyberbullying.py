#IMPORT LIBRARY
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.svm import LinearSVC

#READ DATA TRAIN
data = pd.read_csv('dataTrain.csv', sep=',', encoding='latin-1')

#TRAIN INIT
Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(data['text'],data['label'],test_size=0.1)

Tfidf_vect = TfidfVectorizer()
Tfidf_vect.fit(data['text'])

Train_X_Tfidf = Tfidf_vect.transform(Train_X)

svm = LinearSVC()
svm.fit(Train_X_Tfidf, Train_Y)

kalimat = input("Masukan kalimat yang akan di prediksi :")
def classify(tweet):
    pred = svm.predict(Tfidf_vect.transform([tweet]))
    if pred == 1:
        # print("Nilai Prediksi yang Didapatkan :",pred)
        return "Cyberbullying"
    # print("Nilai Prediksi yang Didapatkan :",pred)
    return "Non-Cyberbullying"

print("Hasil prediksi :",classify(kalimat))

