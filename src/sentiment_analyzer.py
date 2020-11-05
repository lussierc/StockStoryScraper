"""Simple spacy & vaderSentiment based analyzer."""

# import necessary libraries:
import spacy, string, en_core_web_sm
import pandas as pd
from vaderSentiment import vaderSentiment

# pip install spacy vaderSentiment

# import other project files
from search_scraper import *


def analyze_all_articles(stocks, websites):
    article_dicts = get_article_dicts(stocks, websites)

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
    """Analyze the title, desc, and text."""
    english = spacy.load("en_core_web_sm")
    # nlp = en_core_web_sm.load()
    result = english(sentence)
    sentences = [str(s) for s in result.sents]
    analyzer = vaderSentiment.SentimentIntensityAnalyzer()
    sentiment = [analyzer.polarity_scores(str(s)) for s in sentences]
    return sentiment


def get_article_dicts(stocks, websites):
    data = run_web_search_scraper(stocks, websites)

    articles = [
        j for i in data for j in i
    ]  # combine inner and outer list elements (results of individual search queries)

    return articles
