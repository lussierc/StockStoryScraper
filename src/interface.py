"""App Interface."""

import streamlit as st
import pandas as pd
from PIL import Image

from sentiment import *
st.title("StockTextMining")

data = main()
print("\n\n\nDATADOGS:", data)

for i in len(data):
    st.subheader("Article #", i)
    article = data[i]
    st.markdown("- Title:", article['title'])
