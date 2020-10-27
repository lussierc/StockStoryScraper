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

    return search_queries


def run(stocks, websites):
    """Driver function, runs other necesssary fucntions."""
    googlenews = initalize_google_news()

    queries = get_search_queries(stocks, websites)
    results = []
    for search_query in queries:
        print(search_query)
        results.append(scrape_google_news_search(googlenews, search_query))

    return results


def scrape_google_news_search(googlenews, search_query):
    """Scrapes a Google News web search using a specifc query."""

    googlenews.clear()  # clear past results

    # set search query parameters:
    googlenews.search(search_query)
    googlenews.getpage(1)

    # print the results:
    search_results = googlenews.result()
    # print(search_results, "\n\n")  # prints all info

    # print("*** Gathering titles:")
    # titles = googlenews.gettext()
    # print(titles, "\n\n")  # prints titles

    # print("*** Printing results:")
    for result in search_results:
        #print("***", result["title"])

        link = result["link"]
        #print("***", link)
        article_text = scrape_article(link)
        result["text"] = article_text

    # print("*** Gathering results:")
    # #print(search_results, "\n\n")  # prints all info
    # print(search_results[0]['title'], "\n\n")  # prints all info

    return search_results


def initalize_google_news():
    """Initializes the googlenews object."""

    print("initalize_google_news...")

    googlenews = GoogleNews()  # create googlenews object
    googlenews = GoogleNews(lang="en")
    googlenews = GoogleNews(period="d")
    googlenews = GoogleNews(encode="utf-8")
    googlenews = GoogleNews(start="10/01/2020", end="10/26/2020")

    return googlenews


def scrape_article(link):
    """Scrapes a specific article given a link."""

    try:
        article = Article(link)
        article.download()
        article.parse()

        text = article.text

        # print("Article Text:")
        # print(text)
    except:
        print("nope")

    return text
