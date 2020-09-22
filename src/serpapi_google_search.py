"""Web scrape Google Searches to get article information."""

from serpapi.google_search_results import GoogleSearchResults
# pip3 install google-search-results


def main():
    queries = ["'motley fool' AND Slack"]

def scraper():
    month = 9
    from_day = 2
    to_day = 10
    year = 2020

    params = {
        "engine": "google",
        "q": "Trump",
        "google_domain": "google.com",
        "tbm": "nws",
        "tbs": f"cdr:1,cd_min:{month}/{from_day}/{year},cd_max:{month}/{to_day}/{year}",
    }

    client = GoogleSearchResults(params)
    data = client.get_dict()

    for result in data['news_results']:
        print(f"""\n\n*** Title: {result['title']} \n - Snippet: {result['snippet']} \n - Date: {result['date']} """)

scraper()
