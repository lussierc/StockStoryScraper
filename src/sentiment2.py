"""Simple spacy-based sentiment analyzer."""
# Sentiment Insipiration: https://www.kaggle.com/krutarthhd/sentiment-classification-using-spacy/notebook
# 1 sentiment is positive, 2 is 0

#pip install spacy vaderSentiment


# import necessary libraries:
import spacy, string, en_core_web_sm
import pandas as pd
from vaderSentiment import vaderSentiment
from search_scraper import *
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.svm import LinearSVC
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS

sentence = "Apple needs to maintain its free trials in order to give viewers a chance to see if Apple+ is something they're interested in. Netflix has been moving away from free. God help us I hate it."


def analyze(sentence):
    """Analyze the title, desc, and text."""
    english = spacy.load("en_core_web_sm")
    #nlp = en_core_web_sm.load()
    result = english(sentence)
    sentences = [str(s) for s in result.sents]
    analyzer = vaderSentiment.SentimentIntensityAnalyzer()
    sentiment = [analyzer.polarity_scores(str(s)) for s in sentences]
    print(sentiment)

def get_article_dicts(stocks, websites):
    data = run(stocks, websites)

    articles = [j for i in data for j in i] # combine inner and outer list elements (results of individual search queries)

    return articles

analyze(sentence)
