"""App Interface."""

import streamlit as st
import pandas as pd
from PIL import Image

from sentiment import *
st.title("StockTextMining")
stocks_input = st.text_input("Enter Stock Names To Search (EX: Apple, Draftkings):")

WSJ = st.checkbox("www.wsj.com")
nyt = st.checkbox("www.nytimes.com")

websites = []
if WSJ:
    websites.append("www.wsj.com")

if nyt:
    websites.append("www.nytimes.com")

data = main(stocks_input, websites)

print("\n\n\nDATADOGS:", data)

for i in range(len(data)):
    article = data[i]


    st.markdown("## Article", i)
    st.markdown("#### Media:")
    st.markdown(article['media'])
    st.markdown("### Title:")
    st.markdown(article['title'])
    st.markdown("#### Title Sentiment:")
    if article['title_sent'] == 0:
        st.markdown("Negative")
    elif article['title_sent'] == 1:
        st.markdown("Positive")

    st.markdown("### Description:")
    st.markdown(article['desc'])
    st.markdown("#### Description Sentiment:")
    if article['desc_sent'] == 0:
        st.markdown("Negative")
    elif article['desc_sent'] == 1:
        st.markdown("Positive")

    st.markdown("### Overall Text Sentiment:")
    if article['text_sent'] == 0:
        st.markdown("Negative")
    elif article['text_sent'] == 1:
        st.markdown("Positive")
