"""Performs web scraping on Google News web searches."""

from GoogleNews import GoogleNews
from newspaper import Article
# pip3 install GoogleNews, pip install newspaper3k

def main():
    googlenews = initalize_google_news()
    scrape_google_news_search(googlenews)

def scrape_google_news_search(googlenews):
    """Google News Web Scraping."""
    googlenews.clear()  # clear past results


    # set search query parameters:
    googlenews = GoogleNews(start='09/01/2020',end='09/21/2020')
    googlenews.search('apple site:https://www.wsj.com')
    googlenews.getpage(1)

    # print the results:
    print(googlenews.result())  # prints all info
    results = googlenews.result()
    print("\n\n\n")
    print(googlenews.gettext())  # prints titles
    print("\n\n\n")
    for result in results:
        print("\n***", result)

def initalize_google_news():
    print("initalize_google_news...")
    # initialize google news:
    googlenews = GoogleNews()
    googlenews = GoogleNews(lang='en')
    googlenews = GoogleNews(period='d')
    googlenews = GoogleNews(encode='utf-8')
    return googlenews

def scrape_article(link):
    article = Article(link)
    article.download()
    article.parse()

    print("Article Text:")
    print(article.text)

main()
