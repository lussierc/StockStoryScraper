"""Performs web scraping on Google News web searches."""

from GoogleNews import GoogleNews
from newspaper import Article
import bs4
import requests
from bs4 import BeautifulSoup
import datetime

# pip3 install GoogleNews, pip install newspaper3k


def get_search_queries(stocks, websites):
    """Gets search queries to be performed on Google News."""
    search_queries = []  # list to hold created search queries

    for stock in stocks:
        for website in websites:
            website = (
                "site:https://" + website
            )  # add necessary site portion of query for website
            # print(website)
            query = stock + " " + website  # create query
            # print(query)
            search_queries.append(query)  # store created query

    return search_queries


def run_web_search_scraper(
    stocks, abbrvs, websites, start_date, end_date, inputted_csv_list
):
    """Driver function, runs other necesssary fucntions."""
    googlenews = initalize_google_news(start_date, end_date)

    stock_list = stocks.split(", ")
    abbrv_list = abbrvs.split(", ")

    queries = get_search_queries(stock_list, websites)
    results = []

    i = 0
    for current_stock in stock_list:
        for search_query in queries:
            if current_stock in search_query:
                current_abbrv = abbrv_list[i]
                print(
                    "RUNNING QUERY --",
                    search_query,
                    "STOCK",
                    current_stock,
                    "... ABRV",
                    current_abbrv,
                )
                results.append(
                    scrape_google_news_search(
                        googlenews,
                        search_query,
                        current_stock,
                        inputted_csv_list,
                        current_abbrv,
                    )
                )
        i += 1

    return results


def scrape_google_news_search(
    googlenews, search_query, current_stock, inputted_csv_list, current_abbrv
):
    """Scrapes a Google News web search using a specifc query."""

    googlenews.clear()  # clear past results

    # set search query parameters:
    googlenews.search(search_query)
    googlenews.getpage(1)

    # print the results:
    search_results = googlenews.result()

    for result in search_results:
        link = result["link"]
        for article in inputted_csv_list:
            if article["link"] == link:
                search_results.remove(result)

    for result in search_results:
        link = result["link"]
        article_text = scrape_article(link)
        result["text"] = article_text

        result["stock"] = current_stock
        result["abbrv"] = current_abbrv

    return search_results


def initalize_google_news(start_date, end_date):
    """Initializes the googlenews object."""

    print("initalize_google_news...")

    googlenews = GoogleNews(encode="utf-8")  # create googlenews object
    googlenews.setlang("en")
    googlenews.setperiod("d")
    googlenews.setencode("utf-8")
    googlenews.setTimeRange(start_date, end_date)

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


def get_stock_attributes(abbreviation):
    """Gathers real time stock prices."""
    link = "https://finance.yahoo.com/quote/" + abbreviation + "?p=" + abbreviation
    url = requests.get(link)
    soup = bs4.BeautifulSoup(url.text, features="html.parser")

    price = (
        soup.find_all("div", {"class": "My(6px) Pos(r) smartphone_Mt(6px)"})[0]
        .find("span")
        .text
    )
    previous_close = (
        soup.find_all("td", {"class": "Ta(end) Fw(600) Lh(14px)"})[0].find("span").text
    )
    open_price = (
        soup.find_all("td", {"class": "Ta(end) Fw(600) Lh(14px)"})[1].find("span").text
    )
    volume = (
        soup.find_all("td", {"class": "Ta(end) Fw(600) Lh(14px)"})[6].find("span").text
    )
    avg_volume = (
        soup.find_all("td", {"class": "Ta(end) Fw(600) Lh(14px)"})[7].find("span").text
    )
    yr_target = (
        soup.find_all("td", {"class": "Ta(end) Fw(600) Lh(14px)"})[15].find("span").text
    )

    return price, previous_close, open_price, avg_volume, volume, yr_target
