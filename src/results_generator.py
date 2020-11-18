"""Determines and saves results."""

# libraries:
import bs4
import requests
from bs4 import BeautifulSoup

# other files:
import sentiment_analyzer
import csv_handler
import search_scraper


def temp_cml_interface():

    websites = []
    stocks = ""
    stock_abbrvs = ""
    start_date = ""
    end_date = ""

    read_in_dec = input("*  Do you want to read in a CSV file Y or N: ")


    if read_in_dec == 'Y':
        csv_file = input("\n** Enter your CSV filename of previous articles: ")
        scrape_new_dec = input("** Enter Y if you wish to scrape new articles. Enter N if you wish to just use your inputted CSV articles: ")
        if scrape_new_dec == 'Y':
            websites = ["www.fool.com"]
            stocks = input("** Enter your stocks, separated by commas: ")
            stock_abbrvs = input("** Enter your stock abbreviations, separated by commas, in the same order you entered the names above: ")
            start_date = input ("** Enter the START of the date range you want to use for article scraping: ")
            end_date = input ("** Enter the END of the date range you want to use for article scraping: ")
            articles, inputted_csv_list = csv_handler.read_data(csv_file, scrape_new_dec, stocks, websites, start_date, end_date, stock_abbrvs)
            new_scored_articles = calc_article_sent_scores(articles)
            scored_articles = []
            scored_articles = inputted_csv_list + new_scored_articles
            # scored_articles.append(inputted_csv_list)
            # scored_articles.append(new_scored_articles)

            stocks_list = []
            stocks_list = stocks.split(", ")
            abbrv_list = []
            abbrv_list = stock_abbrvs.split(", ")

            for article in scored_articles:
                if article['stock'] not in stocks_list:
                    stocks_list.append(article['stock'])
                else:
                    pass
                if article['abbrv'] not in abbrv_list:
                    abbrv_list.append(article['abbrv'])
                else:
                    pass

        else:
            stock_abbrvs = ""
            articles, inputted_csv_list = csv_handler.read_data(csv_file, scrape_new_dec, stocks, websites, start_date, end_date, stock_abbrvs)
            scored_articles = articles # since articles are only read in from csv, they are already scored
            stocks_list = []
            abbrv_list = []
            for article in scored_articles:
                if article['stock'] in stocks_list:
                    pass
                else:
                    stocks_list.append(article['stock'])

                if article['abbrv'] in abbrv_list:
                    pass
                else:
                    abbrv_list.append(article['abbrv'])

            # TODO automatically gather stocks and stock abbreviations
    else:
        # fresh run
        inputted_csv_list = [] # empty as not to verify any links for fresh run
        websites = ["www.fool.com"]
        stocks = input("** Enter your stocks, separated by commas: ")
        stock_abbrvs = input("** Enter your stock abbreviations, separated by commas, in the same order you entered the names above: ")
        start_date = input ("** Enter the START of the date range you want to use for article scraping: ")
        end_date = input ("** Enter the END of the date range you want to use for article scraping: ")
        # run thru process with only new articles
        article_dicts = search_scraper.run_web_search_scraper(stocks, stock_abbrvs, websites, start_date, end_date, inputted_csv_list)
        articles = sentiment_analyzer.analyze_all_articles(article_dicts)
        scored_articles = calc_article_sent_scores(articles)
        stocks_list = []
        stocks_list = stocks.split(", ")
        abbrv_list = []
        abbrv_list = stock_abbrvs.split(", ")

    print("SCORED ARTICLES")
    print(scored_articles)

    links = []
    for article in scored_articles:
        check_list = isinstance(article, list)
        if check_list is True:
            for articles in article:
                scored_articles.append(articles)
        else:
            if article['link'] in links:
                print("*!!* Duplicate article - removing...", article['link'])
                scored_articles.remove(article)
            else:
                links.append(article['link'])

    generate_results(stocks_list, abbrv_list, scored_articles)

def generate_results(stocks_list, abbrv_list, scored_articles):


    scored_stocks = calc_stock_sentiment(scored_articles, stocks_list)
    # save run date to overall dict for csv purposes
    scored_stocks = calc_recent_stock_sentiment(scored_articles, scored_stocks)

    scored_stocks = calc_stock_trifold_rating(scored_articles, scored_stocks)

    scored_stocks = calc_ovr_stock_article_feelings(scored_articles, scored_stocks)
    print("\n\nScored Stocks", scored_stocks)
    csv_handler.write_data(scored_articles)

    scored_stocks = calc_ovr_media_rating(scored_articles, scored_stocks)
    print(scored_stocks)

    i = 0

    print("ABBRV", abbrv_list)
    while i < len(scored_stocks):
        print(abbrv_list[i])
        price, previous_close, open_price, avg_volume, volume = search_scraper.get_stock_attributes(abbrv_list[i])

        print('Current Stock Price is : $' + str(price))
        print('Previous Close was : $' + str(previous_close))
        print('Open Price of the Day was : $' + str(open_price))
        print('Current stock volume is : ' + str(volume))
        print('Average stock volume is : ' + str(avg_volume))

        print(scored_stocks[i])
        scored_stocks[i]['current_price'] = price
        scored_stocks[i]['volume'] = volume
        scored_stocks[i]['avg_volume'] = avg_volume
        print(scored_stocks[i])

        i += 1

    fin_scored_stocks = predict_stock_well_being(scored_stocks)
    print(fin_scored_stocks)

def calc_article_sent_scores(articles):
    """Averages all sentence scores together, if multiple, and produces one averaged score for a body of text."""
    print("Calcuting text score....")
    for article in articles:
        #ovr_text_sent_score
        ovr_text_sent_score = 0
        sent_count = 0
        for txsent in article['text_sent']:
            sent_count += 1
            ovr_text_sent_score += txsent['compound']
        ovr_text_sent_score = ovr_text_sent_score / sent_count

        #ovr_title_sent_score
        ovr_title_sent_score = 0
        sent_count = 0
        for tisent in article['title_sent']:
            sent_count += 1
            ovr_title_sent_score += tisent['compound']
        ovr_title_sent_score = ovr_title_sent_score / sent_count

        #ovr_desc_sent_score
        ovr_desc_sent_score = 0
        sent_count = 0
        for dsent in article['desc_sent']:
            sent_count += 1
            ovr_desc_sent_score += dsent['compound']
        ovr_desc_sent_score = ovr_desc_sent_score / sent_count

        article['ovr_text_sent_score'] = float(ovr_text_sent_score)
        article['ovr_title_sent_score'] = float(ovr_title_sent_score)
        article['ovr_desc_sent_score'] = float(ovr_desc_sent_score)

        trifold_score, trifold_rating = calc_article_trifold_rating(ovr_text_sent_score, ovr_title_sent_score, ovr_desc_sent_score)
        article['trifold_score'] = trifold_score
        article['trifold_rating'] = trifold_rating



        # call calc_sent_rating():
        #text_sent_rating
        text_sent_rating = calc_sent_rating(ovr_text_sent_score)
        article['text_sent_rating'] = text_sent_rating
        #title_sent_rating
        title_sent_rating = calc_sent_rating(ovr_title_sent_score)
        article['title_sent_rating'] = title_sent_rating
        #desc_sent_rating
        desc_sent_rating = calc_sent_rating(ovr_desc_sent_score)
        article['desc_sent_rating'] = desc_sent_rating

        # add all these scores back to articles dictionary and return it so others can ues the scores

    return articles

def calc_sent_rating(sent_score):
    """Calculates the sentiment rating for a given title, description, or text sentiment rating for an article."""
    rating = "Unknown"
    if float(sent_score) >= -0.05554 and float(sent_score) <= 0.05554:
        rating = "Neutral"
    elif float(sent_score) <= -.05555 and float(sent_score) >= -.30554:
        rating = "Somewhat Negative"
    elif float(sent_score) <= -.30555 and float(sent_score) >= -.70554:
        rating = "Negative"
    elif float(sent_score) <= -.70555 and float(sent_score) >= 1.0:
        rating = "Very Negative"
    elif float(sent_score) >= .05555 and float(sent_score) <= .30554:
        rating = "Somewhat Positive"
    elif float(sent_score) >= .30555 and float(sent_score) <= .70554:
        rating = "Positive"
    elif float(sent_score) >= .70555 and float(sent_score) <= 1.0:
        rating = "Very Positive"

    return rating

def calc_article_trifold_rating(ovr_text_sent_score, ovr_title_sent_score, ovr_desc_sent_score):
    """Calculates a overall 'trifold' score for an article based on the title, description, and text sentiment scores."""

    trifold_score = (ovr_text_sent_score + ovr_title_sent_score + ovr_desc_sent_score) / 3

    trifold_rating = calc_sent_rating(trifold_score)

    return trifold_score, trifold_rating


def calc_stock_sentiment(scored_articles, stocks_list):
    # pass articles and stocks_list
    """Calculates average sentiment score for a stock based on all articles (text) for given stock."""
    scored_stocks = []
    for stock in stocks_list:
        article_count = 0
        stock_sent_score = 0
        for article in scored_articles:
            check_list = isinstance(article, list)
            if check_list is True:
                for articles in article:
                    scored_articles.append(articles)
            else:

                if article['stock'] == stock:
                    article_count += 1
                    stock_sent_score += float(article['ovr_text_sent_score'])


        # try:
        print(stock_sent_score, "/", article_count)
        avg_stock_sent_score = stock_sent_score / article_count
        # except:
        #     avg_stock_sent_score = 0
        stock_sent_dict = {'stock': stock, 'avg_stock_sent_score': avg_stock_sent_score, 'article_count': article_count}
        scored_stocks.append(stock_sent_dict)

    return scored_stocks

def calc_recent_stock_sentiment(scored_articles, scored_stocks):
    # pass articles, stocks, and stock_sentiments{}
    """Calculates average sentiment score for a stock based the most recent articles (within last 7 days)."""
    # must go by date
    # if article[date] == '1 week ago'
    # average score

    for stock in scored_stocks:
        recent_article_count = 0
        day_article_count = 0
        day_stock_sent_score = 0
        stock_sent_score = 0
        for article in scored_articles:
            check_list = isinstance(article, list)
            if check_list is True:
                for articles in article:
                    scored_articles.append(articles)
            else:
                if article['stock'] == stock['stock']:
                    if 'day' in article['date']: # see if day is in it because then we know it is less than a week old/recent
                        recent_article_count += 1
                        stock_sent_score += float(article['ovr_text_sent_score'])
                    elif 'hour' in article['date']:
                        #day
                        day_article_count += 1
                        day_stock_sent_score += float(article['ovr_text_sent_score'])
                        #recent
                        recent_article_count += 1
                        stock_sent_score += float(article['ovr_text_sent_score'])

        try:
            rcnt_text_sent_score = stock_sent_score / recent_article_count
        except:
            rcnt_text_sent_score = 0
        stock['recent_article_count'] = recent_article_count
        stock['rcnt_text_sent_score'] = rcnt_text_sent_score

        try:
            day_text_sent_score = day_stock_sent_score / day_article_count
        except:
            day_text_sent_score = 0
        stock['day_article_count'] = day_article_count
        stock['day_stock_sent_score'] = day_stock_sent_score

    return scored_stocks


def calc_ovr_stock_article_feelings(scored_articles, scored_stocks):
    """Sees if the articles for a stock are generally positive, neutral, or negative."""
    # parses all of the article['text_sent_rating']
    # if neutral,
    # if somewhat positive, positiive, extremely positive,
    # if somewhat negative, negative, very negative
    for stock in scored_stocks:
        positive_article_count = 0
        neutral_article_count = 0
        negative_article_count = 0

        for article in scored_articles:
            sent_score = article['ovr_text_sent_score']
            if article['stock'] == stock['stock']:
                if float(sent_score) > .05:
                    positive_article_count += 1
                elif float(sent_score) >= -0.05 and float(sent_score) <= 0.05:
                    neutral_article_count += 1
                elif float(sent_score) < -.05:
                    negative_article_count += 1
                else:
                    pass

        count_list = []
        count_list.append(positive_article_count)
        count_list.append(neutral_article_count)
        count_list.append(negative_article_count)
        largest = max(count_list)
        if largest == positive_article_count:
            stock['overall_stock_articles_feelings'] = 'Positive'
        elif largest == neutral_article_count:
            stock['overall_stock_articles_feelings'] = 'Neutral'
        elif largest == negative_article_count:
            stock['overall_stock_articles_feelings'] = 'Negative'
        else:
            stock['overall_stock_articles_feelings'] = 'Undetermined'


        stock['positive_article_count'] = positive_article_count
        stock['neutral_article_count'] = neutral_article_count
        stock['negative_article_count'] = negative_article_count
        return scored_stocks

def calc_stock_trifold_rating(scored_articles, scored_stocks):
    """Takes the trifold ratings for each article for a given stock and gets the average trifold rating."""
    for stock in scored_stocks:
        stock_trifold_rating = 0
        stock_article_count = 0
        for article in scored_articles:
            check_list = isinstance(article, list)
            if check_list is True:
                for articles in article:
                    scored_articles.append(articles)
            else:
                if article['stock'] == stock['stock']:
                    stock_article_count += 1
                    stock_trifold_rating += float(article['trifold_score'])

    try:
        ovr_stock_trifold_rating = stock_trifold_rating / stock_article_count
    except:
        ovr_stock_trifold_rating = 0
    stock['ovr_stock_trifold_rating'] = ovr_stock_trifold_rating

    return scored_stocks

def calc_ovr_media_rating(scored_articles, scored_stocks):
    """Calculates a given websites rating for a given stock based on it's overall articles."""

    media_list = []
    for article in scored_articles:
        check_list = isinstance(article, list)
        if check_list is True:
            for articles in article:
                scored_articles.append(articles)
        else:
            media = article['media']
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
                check_list = isinstance(article, list)
                if check_list is True:
                    for articles in article:
                        scored_articles.append(articles)
                else:
                    if article['media'] == media and article['stock'] == stock['stock']:
                        article_count += 1
                        media_sent_score += float(article['ovr_text_sent_score'])

            try:
                stock_media_avg_sent_score = media_sent_score / article_count
            except:
                stock_media_avg_sent_score = 0
            media_sent_rating = calc_sent_rating(stock_media_avg_sent_score)
            media_dict = {'media': media, 'media_avg_sent_score': stock_media_avg_sent_score, 'article_count': article_count, 'media_sent_rating': media_sent_rating}
            stock_media_list.append(media_dict)
        stock['media_results'] = stock_media_list

    return scored_stocks

def predict_stock_well_being(scored_stocks):
    """Predicts the overall view of a stock and whether it will continue to rise or fall."""
    # CURRENTLY BASIC - more updates to come
    # takes stock_trifold_rating, ovr_stock_text_sent, calc_recent_stock_sentiment, ovr_stock_feelings as inputs
    for stock in scored_stocks:
        wght_rcnt_text = .25 * (float(stock['rcnt_text_sent_score']) * 100) #.25
        wght_avg_text = .25 * (float(stock['avg_stock_sent_score']) * 100) #.25
        wght_trifold = .20 * (float(stock['ovr_stock_trifold_rating']) * 100) #.20

        if stock['overall_stock_articles_feelings'] == 'Positive': #.20
            weight_feelings = 20
        elif stock['overall_stock_articles_feelings'] == 'Neutral':
            weight_feelings = 10
        elif stock['overall_stock_articles_feelings'] == 'Negative':
            weight_feelings = 0
        elif stock_sentiments == 'Undertermined':
            weight_feelings = 0
            print("*!!* Stock Sentiment is Undetermined.")
        else: pass

        volume = int(stock['volume'].replace(',', ''))
        print(volume)
        avg_volume = int(stock['avg_volume'].replace(',', ''))
        print(type(avg_volume))

        if volume > avg_volume:
            volume_wght = 10
        elif avg_volume > volume:
            volume_wght = 0
        elif volume == avg_volume:
            volume_wght = 7.5
        else:
            volume_wght = 5

        print("wgh_rcnt", wght_rcnt_text)
        print("wgh_avg", wght_avg_text)
        print("wght_trifold", wght_trifold)
        print("weight_feelings", weight_feelings)
        print("volume_wght", volume_wght)

        stock_well_being_prediction = wght_rcnt_text + wght_avg_text + weight_feelings + wght_trifold + volume_wght
        print("STOCK WELL BEING PREDICTION for stock,", stock['stock'], "= ", stock_well_being_prediction)

temp_cml_interface()
