"""Will handle output of data to CSV and handle input of old data to CSV. Will also verify that incoming data is new."""

import csv
import sentiment_analyzer
import search_scraper


def write_data(data):
    """Writes article data to a CSV file."""
    # eventually will have write_file come in from the interface.
    # write_file = input("\nEnter the CSV filename you wish to write data to: ")

    # if ".csv" not in write_file:
    write_file = "results2.csv"
        # print(
        #     "*!!* You provided an invalid output file name, outputting to the default file (results.csv)!"
        # )

    print("Writing data to your chosen CSV file....")

    keys = data[0].keys()

    with open(write_file, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def read_data(
    csv_file, scrape_new_dec, stocks, websites, start_date, end_date, abbrv_list
):
    """Reads a CSV file back in."""

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        inputted_csv_list = list(reader)

    if scrape_new_dec == "Y":
        # run everything thru individually
        print("Scraping new content in addition to your CSV content....")
        # scrape new Articles
        article_dicts = search_scraper.run_web_search_scraper(
            stocks, abbrv_list, websites, start_date, end_date, inputted_csv_list
        )
        articles = sentiment_analyzer.analyze_all_articles(article_dicts)
        # # IF CSV then do this for new articles, if not do for all
        # scored_articles = calc_article_sent_scores(articles)
    else:
        print("Your CSV file was read in successfully...")
        articles = inputted_csv_list

    return articles, inputted_csv_list


# verify_new_data()
# which makes sure there are no duplicate article links
