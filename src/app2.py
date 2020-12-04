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
        st.write(article['title'])
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

    for stock in fin_scored_stocks:
        st.write(stock['stock'])
        st.write(stock['avg_stock_sent_score'])

    df = pd.DataFrame(fin_scored_stocks, index = stocks_list).T
    # columns = st.multiselect(label="Enter the names of specific contributors below:", options=df.columns)  # allow users to display specific contributor information on dataframe graph
    st.bar_chart(df)  # display dataframe/graph that vizualizes commit info
