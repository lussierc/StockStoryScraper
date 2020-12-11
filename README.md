# StockStoryScraper [SSS]

Scrapes new articles from highly rated stock news websites thru Google News, analyzes them for sentiment among other things, then scores them and provides an overall rating of stock sentiment and well-being. Allows users to get a quick look into how a stock is performing in the news.

Fall 2020 Independent Study - Allegheny College.

![SSS Logo](sss.png)

## Tool Overview

- Scrapes articles from highly rated stock news websites specified by the user. The user also enters their chosen stocks, their ticker symbols, date range for scraping, and an export file (CSV) that can be read back into the tool.
  - With this, users can read back in their previously exported CSVs of article information to view their results again.
- Uses vaderSentiment to perform textual sentiment analysis.
- Scores the articles, gathers their price information, and generates results pertaining to the stocks overall sentiment feelings and well being.
- Tool is used via a User Interface (web application) using Streamlit or a Command Line Interface.
- More features to be added soon.

### What's the point?

It takes a lot of time to read every available news article about a stock, whether you are a professional trader or an amateur. The tool quickly gathers all the relevant articles from highly rated stock websites in the user's defined date range, then analyzes their textual sentiments. The user can read the articles that were scraped if they choose or look at the numerous graphs on the tool depicting article sentiments and overall stock feelings/performance.

This saves lots of time and gives users a one stop shop for stock news and the automatic analysis of them.

## Running the Program using Pipenv
Make sure Python(3) and Pipenv are installed on your machine. Find information on installing pipenv [here](https://pipenv-fork.readthedocs.io/en/latest/install.html).

### Pipenv

The project comes with a `Pipfile` in the `src` directory that will install the necessary packages for the program, making it easy for users with Pipenv to run the project on their machines.

First navigate to the `src` directory using `cd src`. Then run the command `pipenv lock` to install the necessary Python packages.

You can then run the command `pipenv run python3 run_tool.py` to run the program. You will be presented with the option to run either the UI web interface or the Command Line Interface.

## Problems, Ideas, or Praise

Please leave an issue in the Issue Tracker if you encounter errors, have ideas, or anything of the like!

## Future Work

View the Issue Tracker to see future tasks that will be completed in the near future.
