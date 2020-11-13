"""Performs web scraping on Google News web searches."""

from GoogleNews import GoogleNews
from newspaper import Article
import bs4
import requests
from bs4 import BeautifulSoup

# pip3 install GoogleNews, pip install newspaper3k
# pip install -U spacy

def get_search_queries(stocks, websites):
    """Gets search queries to be performed on Google News."""
    search_queries = []  # list to hold created search queries

    stock_list = stocks.split(", ")
    print(stock_list)

    for stock in stock_list:
        for website in websites:
            website = "site:https://" + website  # add necessary site portion of query for website
            # print(website)
            query = stock + " " + website  # create query
            # print(query)
            search_queries.append(query)  # store created query

    return search_queries, stock_list


def run_web_search_scraper(stocks, websites, start_date, end_date):
    """Driver function, runs other necesssary fucntions."""
    googlenews = initalize_google_news(start_date, end_date)

    queries, stock_list = get_search_queries(stocks, websites)
    results = []

    i = 0
    for search_query in queries:
        for stock in stock_list:
            if stock in search_query:
                current_stock = stock
        print(search_query, "STOCK", current_stock)
        results.append(scrape_google_news_search(googlenews, search_query, current_stock))

    return results


def scrape_google_news_search(googlenews, search_query, current_stock):
    """Scrapes a Google News web search using a specifc query."""

    googlenews.clear()  # clear past results

    # set search query parameters:
    googlenews.search(search_query)
    googlenews.getpage(1)

    # print the results:
    search_results = googlenews.result()

    for result in search_results:
        link = result['link']

        article_text = scrape_article(link)
        result['text'] = article_text

        result['stock'] = current_stock

    return search_results


def initalize_google_news(start_date, end_date):
    """Initializes the googlenews object."""

    print("initalize_google_news...")

    googlenews = GoogleNews()  # create googlenews object
    googlenews = GoogleNews(lang="en")
    googlenews = GoogleNews(period="d")
    googlenews = GoogleNews(encode="utf-8")
    googlenews = GoogleNews(start=start_date, end=end_date)

    return googlenews


def scrape_article(link):
    """Scrapes a specific article given a link."""

    try:
        article = Article(link)
        article.download()
        article.parse()

        text = article.text
    except:
        print("No text scraped for this article.")
        text = ""

    return text

def new_article_validator():
    """Ensures an article is new by looking at scraped links."""
    print("placeholder")


"""Simple stock price scraper. Gets real-time stock prices."""




def get_stock_attributes(abbreviation):
    """Gathers real time stock prices."""
    link = 'https://finance.yahoo.com/quote/' + abbreviation + '?p=' + abbreviation
    url = requests.get(link)
    soup = bs4.BeautifulSoup(url.text, features="html.parser")

    price = soup.find_all("div", {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    previous_close = soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[0].find('span').text
    open_price = soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[1].find('span').text
    volume = soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[6].find('span').text
    avg_volume = soup.find_all("td", {'class': 'Ta(end) Fw(600) Lh(14px)'})[7].find('span').text


    return price, previous_close, open_price, avg_volume, volume

def main():
    abbreviation = input("Enter stock abbreviation: ")
    price, previous_close, open_price, bid, ask, days_range, year_long_range, market_cap, avg_volume, volume = get_price(abbreviation)
    print('Current Stock Price is : $' + str(price))
    print('Previous Close was : $' + str(previous_close))
    print('Bid : ' + str(bid))
    print('Ask : ' + str(ask))
    print('Day Price Range : $' + str(days_range))
    print('52 Week Price Range : $' + str(year_long_range))
    print('Market Cap : ' + str(market_cap))
    print('Current stock volume is : ' + str(volume))
    print('Average stock volume is : ' + str(avg_volume))


main()
