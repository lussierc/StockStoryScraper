"""Determines and saves results."""

from sentiment_analyzer import *

stocks = "apple"
websites = ["www.fool.com"]


def generate_results(stocks, websites):

    articles = analyze_all_articles(stocks, websites)
    print("GEN",articles)


generate_results(stocks, websites)

def calc_text_score(articles):
    """Averages all sentence scores together, if multiple, and produces one averaged score for a body of text."""

def calc_trifold_rating():
    """Calculates a overall 'trifold' score for an article based on the title, description, and text sentiment scores."""

def calc_stock_sentiment():
    """Calculates average sentiment score for a stock based on all articles for given stock."""

def calc_recent_stock_sentiment():
    """Calculates average sentiment score for a stock based the most recent articles (within 5-7 days)."""

def predict_stock_swing():
    """Predicts the overall view of a stock and whether it will continue to rise or fall."""
