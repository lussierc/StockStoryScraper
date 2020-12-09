# app1.py
import streamlit as st
import pandas as pd
from PIL import Image
import csv_handler
import results_generator

def app():
    st.title('Import a CSV')
    st.write('Welcome to the CSV importer!')
    st.markdown("#### Enter Your CSV Filepath:")
    csv_input = st.text_input(
        "Enter your chosen csv name (example: results.csv):"
    )

    # declare necessary variables:
    websites = []
    scored_articles = []
    stocks_list = []
    abbrv_list = []
    stocks = ""
    stock_abbrvs = ""
    start_date = ""
    end_date = ""
    scrape_new_dec = "N"


    articles, inputted_csv_list = csv_handler.read_data(
        csv_input,
        scrape_new_dec,
        stocks,
        websites,
        start_date,
        end_date,
        stock_abbrvs,
    )

    scored_articles = articles  # since articles are only read in from csv, they are already scored

    for article in scored_articles:
        if article["stock"] in stocks_list:
            pass
        else:
            stocks_list.append(article["stock"])

        if article["abbrv"] in abbrv_list:
            pass
        else:
            abbrv_list.append(article["abbrv"])

    st.markdown('reading complete')
        # find duplicate links and remove them
    links = []
    for article in scored_articles:
        check_list = isinstance(article, list)
        if article["link"] in links:
            print("*!!* Duplicate article - removing...", article["link"])
            scored_articles.remove(article)
        else:
            links.append(article["link"])

    fin_scored_stocks = results_generator.generate_results(stocks_list, abbrv_list, scored_articles)

    st.markdown("## View Summary Info for all Stocks:")
    if st.checkbox('See All Stocks Overview'):
        df = pd.DataFrame(fin_scored_stocks, index = stocks_list).T
        st.bar_chart(df)  # display dataframe/graph that vizualizes commit info

    #checkboxes for the price, checkbox for stock well being, checkbox for sents, checkbox for media

    st.markdown('## See Individual Stock Graphs/Info')
    for stock in fin_scored_stocks:

        st.markdown("### View Content For Stock:")

        if st.checkbox(stock['stock']):
            st.markdown("### Price Information:")
            st.markdown("#### Current Price at Time of Scrape:")
            st.write(stock['current_price'])
            st.markdown("#### Current Volume at Time of Scrape:")
            st.write(stock['volume'])
            st.markdown("#### Average Volume at Time of Scrape:")
            st.write(stock['avg_volume'])

            st.markdown("### Stock Well Being Prediction:")
            st.write(stock['stock_well_being_prediction'])
            st.markdown("#### The tool rates this stock as having this level of well being: " + stock['stock_well_being_prediction_feelings'])

            if st.checkbox('View Sentiment Information'):
                st.markdown('### Average Stock Sentiment Score:')
                st.write(stock['avg_stock_sent_score'])
                st.markdown('#### # of Articles:')
                st.write(stock['article_count'])

                st.write("### View Specific Sentiment Info:")
                if st.checkbox('View Recent Sentiment Info'):
                    # within this give the option for looking at the graph or textual
                    st.markdown("### Recent Sentiment:")
                    st.markdown("#### Within the last week:")
                    st.write(stock['rcnt_text_sent_score'])
                    st.markdown("Number of articles within this time frame:")
                    st.write(stock['recent_article_count'])
                    st.markdown("#### Within the last day:")
                    st.write(stock['day_stock_sent_score'])
                    st.markdown("Number of articles scraped/analyzed for the last day:")
                    st.write(stock['day_article_count'])

                if st.checkbox('View Media Specific Ratings'):
                    for media in stock['media_results']:
                        st.markdown("### Media Source: " + media['media'])

                        st.markdown("#### Media Average Sent Score:")
                        st.write(media['media_avg_sent_score'])

                        st.markdown("For this media source, the sentiment was rated overall as:")
                        st.write(media['media_sent_rating'])

                        st.markdown("#### Article Count:")
                        st.write(media['article_count'])
                st.markdown("### Overall Stock Trifold Rating")
                st.markdown("Average rating of all article sentiment ratings for the title, description/summary, and text.")
                st.write(stock['ovr_stock_trifold_rating'])



    # columns = st.multiselect(label="Enter the names of specific contributors below:", options=df.columns)  # allow users to display specific contributor information on dataframe graph
