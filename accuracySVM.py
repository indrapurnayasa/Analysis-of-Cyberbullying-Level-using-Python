#IMPORT LIBRARY
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

from sklearn.metrics import confusion_matrix, classification_report


#Membaca Data Training
data = pd.read_csv('fileCsv.csv', sep=',', encoding='latin-1')

#Membuat Model
Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(data['text'],data['label'],test_size=0.4)

Tfidf_vect = TfidfVectorizer()
Tfidf_vect.fit(data['text'])

Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

svm = LinearSVC()
svm.fit(Train_X_Tfidf, Train_Y)

prediction_SVM = svm.predict(Test_X_Tfidf)

print("SVM Accuracy Score = ",accuracy_score(prediction_SVM, Test_Y)*100)
print("SVM Recall Score = ",recall_score(prediction_SVM, Test_Y)*100)
print("SVM Precision Score = ",precision_score(prediction_SVM, Test_Y)*100)
print("SVM f1 Score = ",f1_score(prediction_SVM, Test_Y)*100)
# print(classification_report(y_true=Test_Y,y_pred=prediction_SVM))
# print(confusion_matrix(y_true=Test_Y,y_pred=prediction_SVM))
#
# pd.set_option('display.max_rows', 500)
# print(Test_Y)
# labels_df = pd.DataFrame(Test_X, columns=['text'])
# labels_df.to_csv('dataTraining/text.csv',index = False)
# labels_df = pd.DataFrame(prediction_SVM, columns=['predicted_label'])
# labels_df.to_csv('dataTraining/predicted.csv',index = False)

# export = pd.DataFrame("text": pd.read_csv("dataTrain1000awal.csv")[text], "predicted_label":prediction_SVM)
# pd.to_csv("export.csv",index=False)

