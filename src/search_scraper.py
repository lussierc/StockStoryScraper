"""Performs web scraping on Google News web searches."""

from GoogleNews import GoogleNews
from newspaper import Article

# pip3 install GoogleNews, pip install newspaper3k


def main():
    """Driver function, runs other necesssary fucntions."""
    googlenews = initalize_google_news()
    scrape_google_news_search(googlenews)


def scrape_google_news_search(googlenews):
    """Scrapes a Google News web search using a specifc query."""

    googlenews.clear()  # clear past results

    # set search query parameters:
    googlenews.search("apple site:https://www.wsj.com")
    googlenews.getpage(1)

    # print the results:
    search_results = googlenews.result()
    print(search_results, "\n\n")  # prints all info

    # print("*** Gathering titles:")
    # titles = googlenews.gettext()
    # print(titles, "\n\n")  # prints titles

    print("*** Printing results:")
    for result in search_results:
        print("***", result['title'])

        link = result['link']
        print("***", link)
        article_text = scrape_article(link)
        result['text'] = article_text

    print("*** Gathering results:")
    print(search_results, "\n\n")  # prints all info



def initalize_google_news():
    """Initializes the googlenews object."""

    print("initalize_google_news...")

    googlenews = GoogleNews()  # create googlenews object
    googlenews = GoogleNews(lang="en")
    googlenews = GoogleNews(period="d")
    googlenews = GoogleNews(encode="utf-8")
    googlenews = GoogleNews(start="09/01/2020", end="09/21/2020")

    return googlenews


def scrape_article(link):
    """Scrapes a specific article given a link."""

    article = Article(link)
    article.download()
    article.parse()

    text = article.text

    print("Article Text:")
    print(text)

    return text


main()
