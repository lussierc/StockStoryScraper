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
    googlenews.clear()  # clear past results


    # set search query parameters:
    googlenews = GoogleNews(start='09/01/2020',end='09/21/2020')
    googlenews.search('slack site:https://www.wsj.com')
    googlenews.getpage(1)

    # print the results:
    print(googlenews.result())  # prints all info
    results = googlenews.result()

    print(googlenews.gettext())  # prints titles
    for result in results:
        print("\n***", result)
    print("\n\n", results[0])
    print("\n\n\n")

main()
