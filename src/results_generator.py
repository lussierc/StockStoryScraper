"""Determines and saves results."""

# libraries:
import bs4
import requests
import os
from bs4 import BeautifulSoup
from prettytable import PrettyTable

# other files:
import sentiment_analyzer
import csv_handler
import search_scraper
#import web_interface


class color:
    """Defines different colors and text formatting settings to be used for CML output printing."""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def run_results_generator(scored_articles, stocks_list, abbrv_list, write_file):
    # find duplicate links and remove them
    links = []
    for article in scored_articles:
        check_list = isinstance(article, list)
        if article["link"] in links:
            print("*!!* Duplicate article - removing...", article["link"])
            scored_articles.remove(article)
        else:
            links.append(article["link"])

    fin_scored_stocks = generate_results(stocks_list, abbrv_list, scored_articles, write_file)

    return fin_scored_stocks

def generate_results(stocks_list, abbrv_list, scored_articles, write_file):
    """Driver function to generate results with."""

    scored_stocks = calc_stock_sentiment(scored_articles, stocks_list)
    # save run date to overall dict for csv purposes
    scored_stocks = calc_recent_stock_sentiment(scored_articles, scored_stocks)

    scored_stocks = calc_stock_trifold_rating(scored_articles, scored_stocks)

    scored_stocks = calc_ovr_stock_article_feelings(scored_articles, scored_stocks)

    # write data
    if write_file == "":
        pass
    elif '.csv' in write_file:
        print("VALID CSV")
        csv_handler.write_data(scored_articles, write_file)
    else:
        write_file = "my_results.csv"
        csv_handler.write_data(scored_articles, write_file)

    scored_stocks = calc_ovr_media_rating(scored_articles, scored_stocks)

    # get stock price/attribute information
    i = 0
    while i < len(scored_stocks):
        (
            price,
            previous_close,
            open_price,
            avg_volume,
            volume,
        ) = search_scraper.get_stock_attributes(abbrv_list[i])

        # ^^^ I should print this out in a results_table

        scored_stocks[i]["current_price"] = price
        scored_stocks[i]["volume"] = volume
        scored_stocks[i]["avg_volume"] = avg_volume

        i += 1

    fin_scored_stocks = predict_stock_well_being(scored_stocks)
    print("FINALIZED SCORED STOCKS", fin_scored_stocks)
    return fin_scored_stocks

    # will need to ask user if they want to get media results for the stocks inside the CML, not a UI issue




def calc_article_sent_scores(articles):
    """Averages all sentence scores together, if multiple, and produces one averaged score for a body of text."""

    print("Calcuting text score....")
    for article in articles:
        ovr_text_sent_score = 0
        sent_count = 0
        for txsent in article["text_sent"]:
            sent_count += 1
            ovr_text_sent_score += txsent["compound"]
        ovr_text_sent_score = ovr_text_sent_score / sent_count

        # ovr_title_sent_score
        ovr_title_sent_score = 0
        sent_count = 0
        for tisent in article["title_sent"]:
            sent_count += 1
            ovr_title_sent_score += tisent["compound"]
        ovr_title_sent_score = ovr_title_sent_score / sent_count

        # ovr_desc_sent_score
        ovr_desc_sent_score = 0
        sent_count = 0
        for dsent in article["desc_sent"]:
            sent_count += 1
            ovr_desc_sent_score += dsent["compound"]
        ovr_desc_sent_score = ovr_desc_sent_score / sent_count

        article["ovr_text_sent_score"] = float(ovr_text_sent_score)
        article["ovr_title_sent_score"] = float(ovr_title_sent_score)
        article["ovr_desc_sent_score"] = float(ovr_desc_sent_score)

        trifold_score, trifold_rating = calc_article_trifold_rating(
            ovr_text_sent_score, ovr_title_sent_score, ovr_desc_sent_score
        )
        article["trifold_score"] = trifold_score
        article["trifold_rating"] = trifold_rating

        # call calc_sent_rating():
        # text_sent_rating
        text_sent_rating = calc_sent_rating(ovr_text_sent_score)
        article["text_sent_rating"] = text_sent_rating
        # title_sent_rating
        title_sent_rating = calc_sent_rating(ovr_title_sent_score)
        article["title_sent_rating"] = title_sent_rating
        # desc_sent_rating
        desc_sent_rating = calc_sent_rating(ovr_desc_sent_score)
        article["desc_sent_rating"] = desc_sent_rating

        # add all these scores back to articles dictionary and return it so others can ues the scores

    return articles


def calc_sent_rating(sent_score):
    """Calculates the sentiment rating for a given title, description, or text sentiment rating for an article."""

    rating = "Unknown"
    if float(sent_score) >= -0.05554 and float(sent_score) <= 0.05554:
        rating = "Neutral"
    elif float(sent_score) <= -0.05555 and float(sent_score) >= -0.30554:
        rating = "Somewhat Negative"
    elif float(sent_score) <= -0.30555 and float(sent_score) >= -0.70554:
        rating = "Negative"
    elif float(sent_score) <= -0.70555 and float(sent_score) >= 1.0:
        rating = "Very Negative"
    elif float(sent_score) >= 0.05555 and float(sent_score) <= 0.30554:
        rating = "Somewhat Positive"
    elif float(sent_score) >= 0.30555 and float(sent_score) <= 0.70554:
        rating = "Positive"
    elif float(sent_score) >= 0.70555 and float(sent_score) <= 1.0:
        rating = "Very Positive"

    return rating


def calc_article_trifold_rating(
    ovr_text_sent_score, ovr_title_sent_score, ovr_desc_sent_score
):
    """Calculates a overall 'trifold' score for an article based on the title, description, and text sentiment scores."""

    trifold_score = (
        ovr_text_sent_score + ovr_title_sent_score + ovr_desc_sent_score
    ) / 3

    trifold_rating = calc_sent_rating(trifold_score)

    return trifold_score, trifold_rating


def calc_stock_sentiment(scored_articles, stocks_list):
    """Calculates average sentiment score for a stock based on all articles (text) for given stock."""
    scored_stocks = []
    for stock in stocks_list:
        article_count = 0
        stock_sent_score = 0
        for article in scored_articles:
            if article["stock"] == stock:
                article_count += 1
                stock_sent_score += float(article["ovr_text_sent_score"])
        avg_stock_sent_score = stock_sent_score / article_count
        avg_stock_sent_feelings = calc_sent_rating(avg_stock_sent_score)

        stock_sent_dict = {
            "stock": stock,
            "avg_stock_sent_score": avg_stock_sent_score,
            "avg_stock_sent_feelings": avg_stock_sent_feelings,
            "article_count": article_count,
        }
        scored_stocks.append(stock_sent_dict)

    return scored_stocks


def calc_recent_stock_sentiment(scored_articles, scored_stocks):
    """Calculates average sentiment score for a stock based the most recent articles (within last 7 days)."""

    for stock in scored_stocks:
        recent_article_count = 0
        day_article_count = 0
        day_stock_sent_score = 0
        stock_sent_score = 0
        for article in scored_articles:
            if article["stock"] == stock["stock"]:
                if (
                    "day" in article["date"]
                ):  # see if day is in it because then we know it is less than a week old/recent
                    recent_article_count += 1
                    stock_sent_score += float(article["ovr_text_sent_score"])
                elif "hour" in article["date"]:
                    # day
                    day_article_count += 1
                    day_stock_sent_score += float(article["ovr_text_sent_score"])
                    # recent
                    recent_article_count += 1
                    stock_sent_score += float(article["ovr_text_sent_score"])

        try:
            rcnt_text_sent_score = stock_sent_score / recent_article_count
        except:
            rcnt_text_sent_score = 0
        stock["recent_article_count"] = recent_article_count
        stock["rcnt_text_sent_score"] = rcnt_text_sent_score

        try:
            day_text_sent_score = day_stock_sent_score / day_article_count
        except:
            day_text_sent_score = 0
        stock["day_article_count"] = day_article_count
        stock["day_stock_sent_score"] = day_stock_sent_score

    return scored_stocks


def calc_ovr_stock_article_feelings(scored_articles, scored_stocks):
    """Sees if the articles for a stock are generally positive, neutral, or negative."""
    # parses all of the article['text_sent_rating']

    for stock in scored_stocks:
        positive_article_count = 0
        neutral_article_count = 0
        negative_article_count = 0

        for article in scored_articles:
            sent_score = article["ovr_text_sent_score"]
            if article["stock"] == stock["stock"]:
                if float(sent_score) > 0.05:
                    positive_article_count += 1
                elif float(sent_score) >= -0.05 and float(sent_score) <= 0.05:
                    neutral_article_count += 1
                elif float(sent_score) < -0.05:
                    negative_article_count += 1
                else:
                    pass

        count_list = []
        count_list.append(positive_article_count)
        count_list.append(neutral_article_count)
        count_list.append(negative_article_count)
        largest = max(count_list)
        if largest == positive_article_count:
            stock["overall_stock_articles_feelings"] = "Positive"
        elif largest == neutral_article_count:
            stock["overall_stock_articles_feelings"] = "Neutral"
        elif largest == negative_article_count:
            stock["overall_stock_articles_feelings"] = "Negative"
        else:
            stock["overall_stock_articles_feelings"] = "Undetermined"

        stock["positive_article_count"] = positive_article_count
        stock["neutral_article_count"] = neutral_article_count
        stock["negative_article_count"] = negative_article_count

    return scored_stocks


def calc_stock_trifold_rating(scored_articles, scored_stocks):
    """Takes the trifold ratings for each article for a given stock and gets the average trifold rating."""
    for stock in scored_stocks:
        stock_trifold_rating = 0
        stock_article_count = 0
        for article in scored_articles:
            if article["stock"] in stock["stock"]:
                stock_article_count += 1
                stock_trifold_rating += float(article["trifold_score"])

        try:
            ovr_stock_trifold_rating = stock_trifold_rating / stock_article_count
        except:
            ovr_stock_trifold_rating = 0
        stock["ovr_stock_trifold_rating"] = ovr_stock_trifold_rating
        stock['ovr_stock_trifold_feelings'] = calc_sent_rating(ovr_stock_trifold_rating)

    return scored_stocks


def calc_ovr_media_rating(scored_articles, scored_stocks):
    """Calculates a given websites rating for a given stock based on it's overall articles."""

    media_list = []
    for article in scored_articles:
        media = article["media"]
        if media in media_list:
            pass
        else:
            media_list.append(media)

    for stock in scored_stocks:
        stock_media_list = []
        for media in media_list:
            article_count = 0
            media_sent_score = 0
            for article in scored_articles:
                if article["media"] == media and article["stock"] == stock["stock"]:
                    article_count += 1
                    media_sent_score += float(article["ovr_text_sent_score"])

            try:
                stock_media_avg_sent_score = media_sent_score / article_count
            except:
                stock_media_avg_sent_score = 0
            media_sent_rating = calc_sent_rating(stock_media_avg_sent_score)

            if not media:
                media = "Unknown Source"
                
            media_dict = {
                "media": media,
                "media_avg_sent_score": stock_media_avg_sent_score,
                "article_count": article_count,
                "media_sent_rating": media_sent_rating,
            }
            stock_media_list.append(media_dict)
        stock["media_results"] = stock_media_list

    return scored_stocks


def predict_stock_well_being(scored_stocks):
    """Predicts the overall view of a stock and whether it will continue to rise or fall."""

    # CURRENTLY BASIC FUNCTION/CALCULATION - more updates to come in future PRs
    # takes stock_trifold_rating, ovr_stock_text_sent, calc_recent_stock_sentiment, ovr_stock_feelings as inputs

    for stock in scored_stocks:
        wght_rcnt_text = 0.25 * (float(stock["rcnt_text_sent_score"]) * 100)  # .25
        wght_avg_text = 0.25 * (float(stock["avg_stock_sent_score"]) * 100)  # .25
        wght_trifold = 0.20 * (stock["ovr_stock_trifold_rating"] * 100)  # .20

        if stock["overall_stock_articles_feelings"] == "Positive":  # .20
            weight_feelings = 20
        elif stock["overall_stock_articles_feelings"] == "Neutral":
            weight_feelings = 10
        elif stock["overall_stock_articles_feelings"] == "Negative":
            weight_feelings = 0
        elif stock_sentiments == "Undertermined":
            weight_feelings = 0
            print("*!!* Stock Sentiment is Undetermined.")
        else:
            pass

        volume = int(stock["volume"].replace(",", ""))
        avg_volume = int(stock["avg_volume"].replace(",", ""))

        if volume > avg_volume:
            volume_wght = 10
        elif avg_volume > volume:
            volume_wght = 0
        elif volume == avg_volume:
            volume_wght = 7.5
        else:
            volume_wght = 5

        stock_well_being_prediction = (
            wght_rcnt_text
            + wght_avg_text
            + weight_feelings
            + wght_trifold
            + volume_wght
        )

        stock["stock_well_being_prediction"] = stock_well_being_prediction
        # will need to finetune these calculations
        if stock_well_being_prediction < 15.5555 or stock_well_being_prediction < 0:
            stock["stock_well_being_prediction_feelings"] = "Poor Wellbeing"
        if (
            stock_well_being_prediction > 15.5555
            and stock_well_being_prediction < 40.55555
        ):
            stock["stock_well_being_prediction_feelings"] = "Moderate Wellbeing"
        elif (
            stock_well_being_prediction > 40.55555
            and stock_well_being_prediction < 65.555
        ):
            stock["stock_well_being_prediction_feelings"] = "Good Wellbeing"
        elif (
            stock_well_being_prediction > 65.555
            and stock_well_being_prediction < 100.555
        ):
            stock["stock_well_being_prediction_feelings"] = "Extremely Good Wellbeing"

    return scored_stocks



def predict_historical_stock_well_being():
    """Given an input file of scored stocks over time, generate/predict the overall stock well being rating more accurately given more data."""
    # to be implemented later
