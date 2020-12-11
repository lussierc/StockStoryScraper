from prettytable import PrettyTable
import results_generator
import csv_handler
import search_scraper
import sentiment_analyzer


class color:
    """Defines different colors and text formatting settings to be used for CML output printing."""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def run_cml():
    """A command line interface that can be used instead of the Streamlit UI if chosen."""

    # HAVE USERS ENTER WEBSITES or CHOOSE USING 1,2,3 CML

    print(
        "\n\n-------------------------------------------\n"
        + color.BOLD
        + color.GREEN
        + "| Welcome to the StockTextMining Program! |"
        + color.END
        + "\n|                                         |"
        + "\n|    You are running the CML version!     |"
        + color.END
        + "\n-------------------------------------------\n\n"
    )

    read_in_dec = input(
        color.BOLD
        + color.UNDERLINE
        + "{*} Do you want to read in a CSV file Y or N:"
        + color.END
        + color.END
        + "  "
    )

    if read_in_dec == "Y":  # read in csv
        scored_articles, stocks_list, abbrv_list = read_old_csv()
        write_file = ""
    else:  # new run
        scored_articles, stocks_list, abbrv_list, write_file = fresh_run()

    fin_scored_stocks = results_generator.run_results_generator(
        scored_articles, stocks_list, abbrv_list, write_file
    )  # get scored stocks

    print_cml_stock_table(fin_scored_stocks)  # print the table


def print_cml_stock_table(fin_scored_stocks):
    """Given completely scored stocks, print a table of major attributes."""

    table = PrettyTable()
    table.field_names = [
        "Stock",
        "avg_stock_sent_score",
        "article_count",
        "recent_article_count",
        "rcnt_text_sent_score",
        "ovr_stock_trifold_rating",
        "overall_stock_articles_feelings",
        "positive_article_count",
        "neutral_article_count",
        "negative_article_count",
        "current_price",
        "volume",
        "avg_volume",
        "stock_well_being_prediction",
        "stock_well_being_prediction_feelings",
    ]  # define field names for table

    for stock_dict in fin_scored_stocks:
        table.add_row(
            [
                stock_dict["stock"],
                stock_dict["avg_stock_sent_score"],
                stock_dict["article_count"],
                stock_dict["recent_article_count"],
                stock_dict["rcnt_text_sent_score"],
                stock_dict["ovr_stock_trifold_rating"],
                stock_dict["overall_stock_articles_feelings"],
                stock_dict["positive_article_count"],
                stock_dict["neutral_article_count"],
                stock_dict["negative_article_count"],
                stock_dict["current_price"],
                stock_dict["volume"],
                stock_dict["avg_volume"],
                stock_dict["stock_well_being_prediction"],
                stock_dict["stock_well_being_prediction_feelings"],
            ]
        )  # add data to table

    print(table)  # print prettytable of scored stock info


def read_old_csv():
    """CML content for reading in a previously exported CSV."""

    # declare necessary variables:
    websites = []
    scored_articles = []
    stocks_list = []
    abbrv_list = []
    stocks = ""
    stock_abbrvs = ""
    start_date = ""
    end_date = ""

    csv_file = input(
        color.BOLD
        + color.UNDERLINE
        + "\n{**} Enter your CSV filename of previous articles:"
        + color.END
        + color.END
        + "  "
    )
    scrape_new_dec = input(
        color.BOLD
        + color.UNDERLINE
        + "{***} Enter Y if you wish to scrape new articles. Enter N if you wish to just use your inputted CSV articles:"
        + color.END
        + color.END
        + "  "
    )
    if scrape_new_dec == "Y":
        # run with old csv and new articles
        websites = []
        print(
            "\n\n"
            + color.BOLD
            + color.UNDERLINE
            + "Choose your websites for news article scraping:"
            + color.END
            + color.END
            + "\n (1) Motley Fool \n (2) Yahoo Finance \n (3) Bloomberg \n (4) MarketWatch \n (5) Wall Street Journal"
        )
        website_choices = input(
            color.BOLD
            + color.UNDERLINE
            + color.GREEN
            + "{***} Enter the numbers corresponding to the website, separated by commas: "
            + color.END
            + color.END
            + color.END
        )
        website_numbers = website_choices.split(", ")

        for number in website_numbers:
            if int(number) == 1:
                websites.append("www.fool.com")
            elif int(number) == 2:
                websites.append("finance.yahoo.com")
            elif int(number) == 3:
                websites.append("www.bloomberg.com")
            elif int(number) == 4:
                websites.append("www.marketwatch.com")
            elif int(number) == 5:
                websites.append("www.wsj.com")

        stocks = input(
            color.BOLD
            + color.UNDERLINE
            + color.RED
            + "\n{***} Enter your stocks, separated by commas:"
            + color.END
            + color.END
            + color.END
            + "  "
        )
        stock_abbrvs = input(
            color.BOLD
            + color.UNDERLINE
            + color.BLUE
            + "{***} Enter your stock abbreviations, separated by commas, in the same order you entered the names above:"
            + color.END
            + color.END
            + color.END
            + "  "
        )
        start_date = input(
            color.BOLD
            + color.UNDERLINE
            + "\n {****} Enter the START of the Date Range you want to use for article scraping:"
            + color.END
            + color.END
            + "  "
        )
        end_date = input(
            color.BOLD
            + color.UNDERLINE
            + "{****} Enter the END of the Date Range you want to use for article scraping: "
            + color.END
            + color.END
            + "  "
        )

        articles, inputted_csv_list = csv_handler.read_data(
            csv_file,
            scrape_new_dec,
            stocks,
            websites,
            start_date,
            end_date,
            stock_abbrvs,
        )  # get old articles

        new_scored_articles = results_generator.calc_article_sent_scores(
            articles
        )  # score the new articles

        scored_articles = (
            inputted_csv_list + new_scored_articles
        )  # combine old and new articles

        stocks_list = stocks.split(", ")
        abbrv_list = stock_abbrvs.split(", ")

        for article in scored_articles:
            if (
                article["stock"] not in stocks_list
            ):  # get the stock names for new group of articles
                stocks_list.append(article["stock"])
            else:
                pass
            if article["abbrv"] not in abbrv_list:
                abbrv_list.append(
                    article["abbrv"]
                )  # get the stock tickers for new group of articles
            else:
                pass

    else:
        # Run CML using OLD ARTICLES ONLY

        scored_articles, inputted_csv_list = csv_handler.read_data(
            csv_file,
            scrape_new_dec,
            stocks,
            websites,
            start_date,
            end_date,
            stock_abbrvs,
        )  # read in articles from previously exorted csv

        for article in scored_articles:
            if article["stock"] in stocks_list:
                pass
            else:
                stocks_list.append(
                    article["stock"]
                )  # get the stock names for new group of articles

            if article["abbrv"] in abbrv_list:
                pass
            else:
                abbrv_list.append(
                    article["abbrv"]
                )  # get the stock tickers for new group of articles

        # TODO automatically gather stocks and stock abbreviations
    return scored_articles, stocks_list, abbrv_list


def fresh_run():
    """Runs the program from scratch with user selected run options."""

    # declare necessary variables:
    websites = []
    inputted_csv_list = []
    scored_articles = []
    stocks_list = []
    abbrv_list = []
    stocks = ""
    stock_abbrvs = ""
    start_date = ""
    end_date = ""

    print(
        "\n\n"
        + color.BOLD
        + color.UNDERLINE
        + "Choose your websites for news article scraping:"
        + color.END
        + color.END
        + "\n (1) Motley Fool \n (2) Yahoo Finance \n (3) Bloomberg \n (4) MarketWatch \n (5) Wall Street Journal"
    )  # ask user what websites they want to scrape from
    website_choices = input(
        color.BOLD
        + color.UNDERLINE
        + color.GREEN
        + "{***} Enter the numbers corresponding to the website, separated by commas: "
        + color.END
        + color.END
        + color.END
    )  # get their choices for websites
    website_numbers = website_choices.split(", ")

    for number in website_numbers:  # add websites to list of urls for scraping
        if int(number) == 1:
            websites.append("www.fool.com")
        elif int(number) == 2:
            websites.append("finance.yahoo.com")
        elif int(number) == 3:
            websites.append("www.bloomberg.com")
        elif int(number) == 4:
            websites.append("www.marketwatch.com")
        elif int(number) == 5:
            websites.append("www.wsj.com")

    stocks = input(
        color.BOLD
        + color.UNDERLINE
        + color.RED
        + "\n{***} Enter your stocks, separated by commas:"
        + color.END
        + color.END
        + color.END
        + "  "
    )
    stock_abbrvs = input(
        color.BOLD
        + color.UNDERLINE
        + color.BLUE
        + "{***} Enter your stock abbreviations, separated by commas, in the same order you entered the names above:"
        + color.END
        + color.END
        + color.END
        + "  "
    )
    start_date = input(
        color.BOLD
        + color.UNDERLINE
        + "\n {****} Enter the START of the Date Range you want to use for article scraping:"
        + color.END
        + color.END
        + "  "
    )
    end_date = input(
        color.BOLD
        + color.UNDERLINE
        + "{****} Enter the END of the Date Range you want to use for article scraping: "
        + color.END
        + color.END
        + "  "
    )
    write_file = input(
        color.BOLD
        + color.UNDERLINE
        + "{****} Enter a CSV file name to write your data to (if you wish): "
        + color.END
        + color.END
        + "  "
    )

    # run thru process with only new articles
    article_dicts = search_scraper.run_web_search_scraper(
        stocks, stock_abbrvs, websites, start_date, end_date, inputted_csv_list
    )  # scrape articles with user chosen options
    articles = sentiment_analyzer.analyze_all_articles(
        article_dicts
    )  # get sentiment analyzed articles
    scored_articles = results_generator.calc_article_sent_scores(
        articles
    )  # get scored articles

    stocks_list = stocks.split(", ")  # format lists
    abbrv_list = stock_abbrvs.split(", ")

    return scored_articles, stocks_list, abbrv_list, write_file
