"""App Interface."""

import streamlit as st
import pandas as pd
from PIL import Image

from sentiment import *
st.title("StockTextMining")

data = main()
print("\n\n\nDATADOGS:", data)

for i in range(len(data)):
    article = data[i]

    st.markdown("## Article", i)

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
