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
    st.markdown(article['title_sent'])

    st.markdown("### Description:")
    st.markdown(article['desc'])
    st.markdown("#### Description Sentiment:")
    st.markdown(article['desc_sent'])

    st.markdown("### Overall Text Sentiment:")
    st.markdown(article['text_sent'])
