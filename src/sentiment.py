"""Simple spacy-based sentiment analyzer."""
# Insipiration: https://www.kaggle.com/krutarthhd/sentiment-classification-using-spacy/notebook
# 1 sentiment is positive, 2 is 0


# import necessary libraries
import spacy
from spacy import displacy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.svm import LinearSVC
import string
import en_core_web_sm

from search_scraper import *

# load spacy small model as the nlp
nlp = en_core_web_sm.load()
from spacy.lang.en.stop_words import STOP_WORDS

# gather stop words & punctutation
stopwords = list(STOP_WORDS)
punct = string.punctuation

# TRAIN
data_yelp = pd.read_csv("data/data.txt", sep="\t", header=None)  # currently using yelp review data
columnName = ["Review", "Sentiment"]
data_yelp.columns = columnName

print(data_yelp.head(5))
print(data_yelp.shape)

data = data_yelp

def dataCleaning(sentence):
    doc = nlp(sentence)
    tokens = []
    for token in doc:
        if token.lemma_ != "-PRON-":
            temp = token.lemma_.lower().strip()
        else:
            temp = token.lower_
        tokens.append(temp)
    clean_tokens = []
    for token in tokens:
        if token not in punct and token not in stopwords:
            clean_tokens.append(token)
    return clean_tokens


X = data["Review"]
y = data["Sentiment"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# print(X_train.shape, y_test.shape)


# preparing the model:
tfidf = TfidfVectorizer(tokenizer=dataCleaning)
svm = LinearSVC()
steps = [("tfidf", tfidf), ("svm", svm)]
pipe = Pipeline(steps)

pipe.fit(X_train, y_train)

y_pred = pipe.predict(X_test)
# print(classification_report(y_test, y_pred))
# print("\n\n")
# print(confusion_matrix(y_test, y_pred))

articles = run()
articles = articles[0] # remove outer list layer

for article in articles:
    title = []
    desc = []
    text = []
    print("\n\n------ ARTICLE: -------")
    print("* Title:", article['title'])
    title.append(article['title'])
    print("* * Title Sentiment Rating:", pipe.predict(title))
    print("* Desc:", article['desc'])
    desc.append(article['desc'])
    print("* * Desc Sentiment Rating:", pipe.predict(desc))
    print("* Text: (Keywords):",)
    print(dataCleaning(article['text']))
    text.append(article['text'])
    print("* * Text Sentiment Rating:", pipe.predict(text))



article = ["I am testing a sad bad sentence here", "Ah man, I just cried, what should I do", "this is the best day of my life"]

print("THE REAL TEST", pipe.predict(article))

print(dataCleaning("Today we are having heavy rainfall, We recommend you to stay at your home and be safe, Do not start running here and there"))
