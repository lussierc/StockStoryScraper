"""Web scrapes articles to be used in text mining analysis."""

from newspaper import Article
# NOTE: pip install newspaper3k

link = input("* Enter Link: ")

def scrape_article(link):
    article = Article(link)
    article.download()
    article.parse()

    print("Article Text:")
    print(article.text)
