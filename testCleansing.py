from pymongo import MongoClient
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import nltk

client = MongoClient('localhost', 27017)
db = client['databaseName']
collection = db['collectionName']

dbStore = client['databaseStoreName']
collectionStore = dbStore['collectionStoreName']

#stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def cleanTweet(tweet):
    # Remove link web
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'https\S+', '', tweet)
    tweet = re.sub(r'www\S+', '', tweet)
    # Remove @username
    tweet = re.sub('@[^\s]+', '', tweet)
    # Remove #hastag
    tweet = re.sub(r'#([^\s]+)', '', tweet)
    # Remove angka termasuk angka yang berada dalam string
    # Remove non ASCII chars
    tweet = re.sub(r'[^\x00-\x7f]', r'', tweet)
    tweet = re.sub(r'(\\u[0-9A-Fa-f]+)', r'', tweet)
    tweet = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", tweet)
    tweet = re.sub(r'\\u\w\w\w\w', '', tweet)
    # Remove simbol, angka dan karakter aneh
    tweet = re.sub(r"[.,:;+!\-_<^/=?\"'\(\)\d\*]", " ", tweet)
    return tweet

result = collection.find(no_cursor_timeout=True)
collection_data = [doc for doc in result]
for doc in collection_data:
    if (doc['lang'] != 'in'):
        continue
    text = doc['full_text']
    print("Text Before Preprocessing :", text)
    #Clean Tweet
    cleanText = cleanTweet(text)
    print("Text Cleaning : ", cleanText)

    # Lowering Case
    lowerCase = cleanText.lower()
    print("Text Lower case : ", lowerCase)

    #Remove Three or More Character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    newPattern = pattern.sub(r"\1\1", lowerCase)
    # print("Text After Remove Three or More Character : ", newPattern)

    #Tokenize
    tokenisasi = nltk.word_tokenize(newPattern)
    # print("Text After Tokenize :", tokenisasi)

    #Replace Slang Word
    content = []
    kamus_slangword = eval(open("slangword.txt").read())  # Membuka dictionary slangword
    pattern = re.compile(r'\b( ' + '|'.join(kamus_slangword.keys()) + r')\b')  # Search pola kata (contoh kpn -> kapan)
    for kata in tokenisasi:
        filteredSlang = pattern.sub(lambda x: kamus_slangword[x.group()],kata)  # Replace slangword berdasarkan pola review yg telah ditentukan
        content.append(filteredSlang.lower())
    slangWord = ' '.join(content)
    print("Text After Replace Slang Word :", slangWord)

    # Tokenize
    tokenisasiStopwords = nltk.word_tokenize(slangWord)

    #Remove Stopword
    stopwords = []
    stopwords_list = []
    after_stopwords = []
    with open('stopwords.txt', 'r') as file:
         for line in file:
             clear_line = line.replace("\n", '').strip()
             stopwords.append(clear_line)

         for stopword in tokenisasiStopwords:
             if stopword not in stopwords:
                 stopwords_list.append(stopwords)
                 after_stopwords.append(stopword)

         afterStopword = " ".join(after_stopwords)
         print("Text After Remove Stopword :",afterStopword)

    # stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    textFix = stemmer.stem(afterStopword)
    print("Text After Stemming :", textFix)

    if (len(textFix) <= 1):
        continue
    mongo = {
        "date": doc['created_at'],
        "text": textFix,
        "location": doc['user']['location'],
        "language": doc['lang']
    }
    print(mongo)
    collectionStore.insert_one(mongo)
