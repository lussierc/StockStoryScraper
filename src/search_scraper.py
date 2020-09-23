"""Performs web scraping on Google News web searches."""

from GoogleNews import GoogleNews
from newspaper import Article
# pip3 install GoogleNews, pip install newspaper3k


def main():
    scrape_google_news_search()

main()

def scrape_google_news_search():
    """Google News Web Scraping."""

    # initialize google news:
    googlenews = GoogleNews()
    googlenews = GoogleNews(lang='en')
    googlenews = GoogleNews(period='d')
    googlenews = GoogleNews(encode='utf-8')
    googlenews.clear()  # clear past results


    # set search query parameters:
    googlenews = GoogleNews(start='09/01/2020',end='09/21/2020')
    googlenews.search('slack site:https://www.wsj.com')
    googlenews.getpage(1)

    # print the results:
    print(googlenews.result())  # prints all info
    results = googlenews.result()
    print("\n\n\n")
    print(googlenews.gettext())  # prints titles
    print("\n\n\n")
    for result in results:
        print("\n***", result)

def scrape_article(link):
    article = Article(link)
    article.download()
    article.parse()

    print("Article Text:")
    print(article.text)
