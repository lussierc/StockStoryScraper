# app1.py
import streamlit as st
def app():
    st.title('Run the StockTextMining Tool')
    st.markdown('Welcome to the StockTextMining Tool! This page will run the tool for new stocks! It performs a fresh run!')

    # user_input_dict = {"Stock":""}
    #
    # for k in user_input_dict.items():
    #
    #     user_input_dict[k] = st.text_input(
    #         "Enter your chosen csv name (example: results.csv):"
    #     )
    #     st.write(user_input_dict[k])
    user_stock_input_dict = {"Stock Names":"", "Stock Abbreviations":"", "Begin Date Range": "", "End Date Range":""}

    for k, v in user_stock_input_dict.items():
        if k == "Stock Names":
            st.markdown("### Enter your Stock Names, separated by commas, then press enter:")
            st.markdown("#### Example: Apple, Draftkings")
        elif k == "Stock Abbreviations":
            st.markdown("### Enter your Stock Ticker Symbols (abbreviations), separated by commas, then press enter:")
            st.markdown("#### Example: AAPL, DKNG")
        elif k == "Begin Date Range":
            st.markdown("### Enter the Start of your Date Range to Scrape:")
            st.markdown("#### Example: 11/21/2020")
        elif k == "End Date Range":
            st.markdown("### Enter the End of your Date Range:")
            st.markdown("#### Example: 11/28/2020")
        user_stock_input_dict[k] = st.text_input(k, v)
    st.write(user_stock_input_dict)