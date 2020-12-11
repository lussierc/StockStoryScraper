# StockStoryScraper [SSS] Tool - Fall 2020 Report
#### *By*: Christian Lussier

Report for my Fall 2020 Independent Study under Dr. Bonham-Carter at Allegheny College.

## Introduction and Overview

The StockStoryScraper (SSS) tool gathers and analyzes the sentiment of news articles for user chosen stocks. It is nearly impossible to read every relevant news article for a stock, despite them having huge importance on a stock's price. Being in the know with regard to a stock's news can be the difference between making money and losing it. That's where the SSS tool comes into play.

Users give the tool their selected stocks, corresponding ticker symbols, date range, and an export file name (so articles can be used again for future analysis). The tool scrapes Google News to get relevant article information than scrapes their texts. VaderSentiment is then used to analyze the texts to determine their sentiment rating. Results are then generated that apply textual feelings to the numerical sentiment ratings. More in-depth results are then generated regarding the average sentiment of all articles for a stock and the stocks overall well being. Now all the articles are in one place for a stock and they have already been automatically analyzed to determine their positivity, saving both professional and amateur traders time and effort.

### Motivations

I have always had an interest in stocks. At the beginning of the COVID-19 lockdown, I began to trade some stocks lightly, on the side. I noticed the problem that it was impossible to keep up with the news surrounding stocks. With social media and internet news outlets being so prevalent in our society, it is near impossible to keep up. News can impact stocks in big ways, negatively or positively. It is important to be in the know regarding what is going on with stocks you currently own and stocks you are interested in.

By gathering all of the articles related to a stock from highly rated news websites, this issue can be solved. All the articles are on one tool, along with the stock price and target price information. The tool automatically analyzes the articles for sentiment and prints out a broad range of results, so you don't even have to read the articles unless you want to.

This tool can save significant time for both professionals and amateurs with regard to news research and analysis for their stocks.

## Methodology (Work Completed)

Originally, the idea behind this tool was that it would just analyze specific technology stocks. Overtime, the idea evolved and now the tool is designed to analyze all stocks. There were many challenges and setbacks while working on the project up to this point, but with patience and good design, I was able to create a functioning tool that scrapes and analyzes stock related news articles.

The tool started out just scraping articles. Search queries would be created by having the user enter their chosen stocks and website for scraping. The tool then utilizes the `GoogleNews` library to scrape the results from Google News, these results included the article link, description, and title. The `newspaper3k` library was then utilized to take those links and scrape the actual article text. A list of dictionaries was created to store this information, with each dictionary being an individual article.

These article dictionaries are then sent to the `sentiment_analyzer` which will get sentiment scores for them. A `VaderSentiment` analyzer is used to perform this, in collaboration with the `spacy` library. The sentiment analyzer generates sentiment scores for the title, description, and text of each article.

These articles, with their sentiment ratings now stored inside their respective dictionaries, then have further analysis performed upon them by `results_generator`. This file ensures the sentiment ratings for the articles are properly formatted and then calculates the trifold rating for that particular article. The trifold rating is the average of the title, description, and text sentiment scores, helping to paint a brief overall view of stock sentiment.

Additionally, the `results_generator` takes these articles and organizes them by stock (as defined by the user when the ran the tool). With this, further analysis is performed on the group of articles as a whole for each stock. Things like the average sentiment for all article texts are calculated, the recent sentiment for a stock (based on articles within the last week), and more. Additionally, textual feeling ratings are given to each numeric score when relevant. For instance, a sentiment rating of `.10` is slightly positive.

A stock well being prediction is also calculated. This is currently a weighted score of a number of attributes for a stock based on its articles and price information/trends but in the future should include some sort of AI/ML. The average stock sentiment rating is worth `25%` of the score, the average trifold rating of the stock is `15%`, the average stock sentiment score from the last week (if applicable) is worth `25%`, and a rating determined by the overall article feelings (were most of them positive) is worth `10%`. Also, the projected growth percentage of the stock price based on the current price versus the target price is worth `20%` while the trend in volume is also analyzed, for an allotted `5%`. With this, the max score a stock can get is `100%`, which is extremely unlikely. Stocks with a well being rating of `20-40%` are of a moderate well being, `40-65%` is good well being, anything above `65%` is very good well being rating, and anything below `20%` is poor. This rating will be refined in the future and should be the focal point of the tool in a way.

In order to run the tool and perform all of this analysis, the user has their choice of using a Command Line Interface (CML) or UI (web app). The CML is simple and color coded so it can be easily understandable. The UI uses the Streamlit library for data visualization. When the user starts the tool they are prompted to choose one of the interfaces. The user has the choice of performing a fresh run with all new stocks, a set date range, set websites, and a set export file. Alternatively, they can choose to read in an old CSV file to view its results once again. The UI visualizes the data using Pandas data-frames and Streamlit graphs paired with the libraries user interface formatting options. users can view things like the stock prices, average sentiment ratings, well being ratings, and more relative to each other. Users can also view individual article scores, text, and links if they wish. They can also view sentiment ratings by media, to see if any one news source is skewing data and what they think of a stock/topic overall. On the other hand, the CML, uses `prettytable` to format the scored stock information.

### Potential Future Work (& Related Shortcomings T.B.A.)

While my Independent Study will be over in mid-December for this tool, I still plan to keep working on it in my free time. There are a number of shortcomings in the area of code implementation, but these can be easily resolved. I feel it is decent right now but has real potential, that can be reached by perfecting the design, efficiency, and interface of the tool.

*Potential Future Work Will Include:*
- Refactoring Code: There is still significant work that needs to be done in this area, and I recognize that. I need to condense a lot of code and separate more components into their own functions. This will be the first thing I do as it is a big issue in my opinion, because while the code functions as intended right now, it would be much more efficient and testable once refactored.
  - With this I should add some more detailed comments in when necessary.
  - Optimize efficiency by testing code by looking at execution times and their big-Oh notation.
- Testing Code: I will use Pytest to create a test suite testing the tool's refactored functions to ensure they are functioning as intended.
- UI Improvements: Add more relevant graphs and features as necessary (as more results are generated/implemented). Add things like a progress bar so user can see how far along they are in the scraping & analysis process.
- Allow user to read in multiple CSVs of articles that were previously exported from the tool so they can compare them in an effort to see overall stock performance.
- Improve stock well being rating so it uses a neural network, machine learning, or something of the like.
- Add More Run Methods: Allow the user to run the program using other resources like Docker.

## Preliminary Evidence of Tool Accuracy
