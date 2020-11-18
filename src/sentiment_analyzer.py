"""Simple spacy & vaderSentiment based analyzer."""

# import necessary libraries:
import spacy, string, en_core_web_sm
import pandas as pd
from vaderSentiment import vaderSentiment

# pip install spacy vaderSentiment

# import other project files
from search_scraper import *


def analyze_all_articles(article_dicts):
    """Perform sentiment analysis on all articles' titles, descriptions, and texts."""

    article_dicts = [j for i in article_dicts for j in i]  # combine inner and outer list elements (results of individual search queries)

    print("Performing sentiment analysis on given article titles, descriptions, and texts....")
    for article in article_dicts:
        # analyze & store title
        title_sent = sent_analyze(article["title"])
        article["title_sent"] = title_sent

        # analyze & store description
        desc_sent = sent_analyze(article["desc"])
        article["desc_sent"] = desc_sent

        # analyze & store actual article text
        text_sent = sent_analyze(article["text"])
        article["text_sent"] = desc_sent

    return article_dicts


def sent_analyze(sentence):
    """Analyze a given sentence/block of text."""
    english = spacy.load("en_core_web_sm")
    # nlp = en_core_web_sm.load()
    result = english(sentence)
    sentences = [str(s) for s in result.sents]
    analyzer = vaderSentiment.SentimentIntensityAnalyzer()
    sentiment = [analyzer.polarity_scores(str(s)) for s in sentences]

    return sentiment
