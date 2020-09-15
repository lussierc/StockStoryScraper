"""Web scrapes articles to be used in text mining analysis."""

from newspaper import Article
# NOTE: pip install newspaper3k

def main():
    link = input("* Enter Link: ")
    scrape_article(link)

def scrape_article(link):
    article = Article(link)
    article.download()
    article.parse()

    print("Article Text:")
    print(article.text)

main()
