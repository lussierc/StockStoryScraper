"""Performs web scraping on Google News web searches."""

from GoogleNews import GoogleNews
from newspaper import Article
import spacy

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


def run_web_search_scraper(stocks, websites):
    """Driver function, runs other necesssary fucntions."""
    googlenews = initalize_google_news()

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


def initalize_google_news():
    """Initializes the googlenews object."""

    print("initalize_google_news...")

    googlenews = GoogleNews()  # create googlenews object
    googlenews = GoogleNews(lang="en")
    googlenews = GoogleNews(period="d")
    googlenews = GoogleNews(encode="utf-8")
    googlenews = GoogleNews(start="11/03/2020", end="11/06/2020")

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
