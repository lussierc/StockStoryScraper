"""App Interface."""

import streamlit as st
import pandas as pd
from PIL import Image

from sentiment import *

st.title("StockTextMining")
st.markdown("#### Enter Stock Names:")
stocks_input = st.text_input(
    "Enter Stock Names Separated by Commas (EX: Apple, Draftkings):"
)


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


data = main(stocks_input, websites)

print("\n\n\nDATADOGS:", data)

for i in range(len(data)):
    article = data[i]

    st.markdown("## Article", i)
    st.markdown("#### Stock:")
    st.markdown(article["stock"])
    st.markdown("#### Media:")
    st.markdown(article["media"])
    st.markdown("### Title:")
    st.markdown(article["title"])
    st.markdown("#### Title Sentiment:")
    if article["title_sent"] == 0:
        st.markdown("Negative")
    elif article["title_sent"] == 1:
        st.markdown("Positive")

    st.markdown("### Description:")
    st.markdown(article["desc"])
    st.markdown("#### Description Sentiment:")
    if article["desc_sent"] == 0:
        st.markdown("Negative")
    elif article["desc_sent"] == 1:
        st.markdown("Positive")

    st.markdown("### Overall Text Sentiment:")
    if article["text_sent"] == 0:
        st.markdown("Negative")
    elif article["text_sent"] == 1:
        st.markdown("Positive")
