"""Performs web scraping on Google News web searches."""

from GoogleNews import GoogleNews
# pip3 install GoogleNews

def main():
    """Google News Web Scraping."""
    # initialize google news:
    googlenews = GoogleNews()
    googlenews = GoogleNews(lang='en')
    googlenews = GoogleNews(period='d')
    googlenews = GoogleNews(encode='utf-8')

    # set search query parameters:
    googlenews = GoogleNews(start='06/12/2020',end='09/20/2020')
    googlenews.search('IDEX')
    googlenews.getpage(1)

    # print the results:
    print(googlenews.result())  # prints all info
    print("\n\n\n")
    print(googlenews.gettext())  # prints titles

main()
