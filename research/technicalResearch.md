# Technical Research

General technical research and information on resources found/used throughout the project.

## Research Points

### Simple Way To Web Scrape Articles

The pip plugin `newspaper3k` makes it simple to extract articles and their information. This includes their published date, author, and obviously the article text itself. [towardsdatascience.com](https://towardsdatascience.com/scraping-a-website-with-4-lines-using-python-200d5c858bb1) offers a nice tutorial on how to use it.

This could be useful for downloading and categorizing articles though a way to automatically query article downloads & automatically gather article links would have to be devised. Content could then be pushed into the text analyzer.

### How To Scrape Google Web Searches

While `newspaper3k` can easily be used to to extract articles and their text. While this will be perfect for web scraping the articles themselves and their content, there is no way in this tool to easily find these articles and their links.

A way must be found to scrape article links/searches so we can then get the article content to analyze and perform tasks with.

#### Google Search Query

Directly scrape google search results `https://google.com/search?q=<Query`, return the first 10 results.

#### `google-search-results` pypi package

Uses serp.api to get all the information we need. However, since it uses serp.api, you must have an account that at minimum costs $50 a month.

[PyPi Website](https://pypi.org/project/google-search-results/)

Information gathered includes:
- Title
- Link
- Source (Wall Street Times for example)
- Date
- Snippet
  - If we decide to use snippets instead of full text, then we can skip using `newspaper3k` and just use one package.

#### `requests` library

Give URL to Google Search, query by days.

#### Beautiful Soup

Similar to requests.

#### `GoogleNews` library
[GoogleNews 1.4.1](https://pypi.org/project/GoogleNews/) is a Python library that can be installed via Pip. It can be used to easily scrape google news results, and you can search specifically by site by using queries, such as `slack site:https://www.wsj.com'`.
