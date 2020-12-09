import app1
import app2
import app3

import streamlit as st
PAGES = {
    "Home": app1,
    "Read in CSV": app2,
    "Fresh Run": app3
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to:", list(PAGES.keys()))
page = PAGES[selection]
page.app()
