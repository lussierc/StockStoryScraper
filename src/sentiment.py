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
from spacy.lang.en.stop_words import STOP_WORDS

from search_scraper import *
nlp = en_core_web_sm.load()
punct = string.punctuation
stopwords = list(STOP_WORDS)

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

def main():
    # load spacy small model as the nlp

    # gather stop words & punctutation

    # TRAIN
    data_yelp = pd.read_csv("data/data.txt", sep="\t", header=None)  # currently using yelp review data
    columnName = ["Review", "Sentiment"]
    data_yelp.columns = columnName

    print(data_yelp.head(5))
    print(data_yelp.shape)

    data = data_yelp

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

    data = run()

    articles = [j for i in data for j in i] # combine inner and outer list elements (results of individual search queries)


    for article in articles:
        title = []
        desc = []
        text = []

        print("\n\n------ ARTICLE: -------")
        # print("* Title:", article['title'])
        title.append(article['title'])
        title_sent = pipe.predict(title)
        # print("* * Title Sentiment Rating:", title_sent[0])
        article['title_sent'] = title_sent[0]

        # print("* Desc:", article['desc'])
        desc.append(article['desc'])
        desc_sent = pipe.predict(desc)
        # print("* * Desc Sentiment Rating:", desc_sent[0])
        article['desc_sent'] = desc_sent[0]

        print("* Text: (Keywords):",)
        # print(dataCleaning(article['text']))
        text.append(article['text'])
        text_sent = pipe.predict(text)
        # print("* * Text Sentiment Rating:", text_sent[0])
        article['text_sent'] = text_sent[0]

    print(articles)
    return articles
