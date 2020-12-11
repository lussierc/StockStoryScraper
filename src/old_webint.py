"""App Interface."""

import streamlit as st
import pandas as pd
from PIL import Image

from sentiment_analyzer import *

st.title("StockTextMining")

# if run with old file call csv_handler
# if new file send her over to results_generator
st.markdown("#### Enter Stock Names:")
stocks_input = st.text_input(
    "Enter Stock Names Separated by Commas (EX: Apple, Draftkings):"
)

stocks_list = []
stocks_list = stocks_input.split(", ")

st.markdown("#### Choose Websites To Search Given Stocks With:")
WSJ = st.checkbox("www.wsj.com")
mfool = st.checkbox("www.fool.com")
mktwatch = st.checkbox("www.marketwatch.com")
bloom = st.checkbox("www.bloomberg.com")
yahoo = st.checkbox("finance.yahoo.com")

websites = []
if WSJ:
    websites.append("www.wsj.com")

if mfool:
    websites.append("www.fool.com")

if mktwatch:
    websites.append("www.marketwatch.com")

if bloom:
    websites.append("www.bloomberg.com")

if yahoo:
    websites.append("finance.yahoo.com")


data = analyze_all_articles(stocks_input, websites)

print("\n\n\nDATADOGS:", data)

graph_list = []

for stock in stocks_list:
    dict = {"stock": stock, "title_pos": 0, "title_neg": 0}
    for i in range(len(data)):
        article = data[i]
        if stock == article["stock"]:
            st.markdown("## Article", i)
            st.markdown("#### Stock:")
            st.markdown(article["stock"])
            st.markdown("#### Media:")
            st.markdown(article["media"])
            st.markdown("### Title:")
            st.markdown(article["title"])
            st.markdown("#### Title Sentiment:")
            st.markdown(title_sent)

    # for stock in stocks_list:
    #     for graph_dict in graph_list:
    #         if stock == graph_dict['stock']:
    #             df = pd.DataFrame.from_dict(graph_dict, orient="index")
    #             st.markdown("### Bar chart:")
    #             st.markdown(stock)
    #             st.bar_chart(df)  # display dataframe/graph that vizualizes commit info
