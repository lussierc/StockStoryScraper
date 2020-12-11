"""Web interface using Streamlit."""

# imports:
import streamlit as st
import csv_handler
import results_generator
import pandas as pd
from PIL import Image
from streamlit.hashing import _CodeHasher

import sentiment_analyzer
import csv_handler
import search_scraper

try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server


def main():
    """Runs the web interface."""
    state = _get_state()
    pages = {
        "Home": page_home,
        "Dashboard": page_dashboard,
        "Run Settings": page_settings,
    }

    st.sidebar.title(":mag: Navigation Hub")
    page = st.sidebar.radio("Select your page:", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


def page_home(state):
    """Sets up the home page of the web app."""

    st.title(":house: Welcome to StockStoryScraper (SSS)")

    image = Image.open("../sss.png")  # load logo
    st.image(image, use_column_width=True)

    st.markdown("## Tool Overview:")
    st.markdown(
        "The StockStoryScraper allows users to scrape news stories on their favorite stocks and then see what the general sentiment for these articles is. It saves investors, both new and old, time in terms of analyzing stock news. Now, you no longer need to spend numerous hours searching for articles about stocks online and then reading them to see what the thoughts/sentiment are. The tool will find the articles for you and analyze them to see if they are positive, negative, or neutral. By using the SSS tool, users can make more informed investing decisions."
    )

    st.markdown("## Using the Tool:")
    st.markdown(
        "Using the tool is simple once you are in the Web Interface! To run the tool, go to the `Run Settings` page.\nYou will then be presented with two options for running the tool:"
    )
    st.markdown(
        "- `Previous CSV`: You can choose to read in a CSV of scraped articles that would be previously exported by the tool during a fresh run. \n - `Fresh Run`: You can run the tool with no previous data, entering your stocks and their respective ticker symbols, among other information."
    )
    st.markdown(
        "After filling out the data fields for your chosen option, you can than click the button below to run the tool. After this, wait until the tool prompts you to `Go to the Dashboard to view your data`. Once prompted, you can then go to the Dashboard page and view your data."
    )
    st.markdown(
        "Within the Dashboard, you can then view information for all the stocks at once, or look at individual stocks and more specific information (pertaining to individual articles)."
    )


def page_dashboard(state):
    """Dashboard page where user sees their data."""

    st.title(":chart_with_upwards_trend: Dashboard")

    if st.checkbox(
        "View Your Chosen Run Settings"
    ):  # give user the option to view their defined run options
        display_state_values(state)
    st.write("---")

    if state.cb_csvread == True:  # displays results for imported data
        st.write(
            "Your CSV file of previously scraped articles has been properly imported! View the results below!"
        )
        st.write("# Your Imported Results:")
        display_data(state)
    elif state.cb_freshrun == True:  # displays results for newly scraped data
        st.write("Here is your newly scraped data:")
        st.write("# Your Scraped and Analyzed Results:")
        display_data(state)
    else:  # occurs if user does not define run options or they are improper
        st.markdown("## No Results Available!")
        st.markdown(
            "No results available. Configure your settings to run the program in the `Run Settings` page."
        )


def read_csv(state):
    """Reads in a user defined CSV of articles from a previous run."""

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
        state.csv_file,
        scrape_new_dec,
        stocks,
        websites,
        start_date,
        end_date,
        stock_abbrvs,
    )  # read in the csv

    scored_articles = (
        articles  # since articles are only read in from csv, they are already scored
    )

    for article in scored_articles:
        if article["stock"] in stocks_list:
            pass
        else:
            stocks_list.append(article["stock"])

        if article["abbrv"] in abbrv_list:
            pass
        else:
            abbrv_list.append(article["abbrv"])

    st.markdown(
        "### *PLEASE WAIT! Reading in your CSV now!*"
    )  # alert the user the program is still preparing their data

    # find duplicate links and remove them:
    seen = set()
    result = []
    for dic in scored_articles:
        key = (dic["link"], dic["title"])
        if key in seen:
            continue
        result.append(dic)
        seen.add(key)

    state.stocks_list = stocks_list
    state.abbrv_list = abbrv_list
    state.scored_articles = result
    state.fin_scored_stocks = results_generator.generate_results(
        stocks_list, abbrv_list, result, state.write_file
    )  # get scored stocks


def fresh_run(state):
    """Runs the program fresh, with their defined inputs."""

    inputted_csv_list = []  # shows no CSV is being read in, no impact

    # run thru process with only new articles
    article_dicts = search_scraper.run_web_search_scraper(
        state.stocks,
        state.abbrvs,
        state.websites,
        state.start_date,
        state.end_date,
        inputted_csv_list,
    )  # get articles

    articles = sentiment_analyzer.analyze_all_articles(
        article_dicts
    )  # sentiment analyze the articles
    scored_articles = results_generator.calc_article_sent_scores(
        articles
    )  # score the articles

    # find and remove duplicate links if necessary:
    seen = set()
    result = []
    for dic in scored_articles:
        key = (dic["link"], dic["title"])
        if key in seen:
            continue
        result.append(dic)
        seen.add(key)

    state.scored_articles = result
    state.stocks_list = state.stocks.split(", ")
    state.abbrv_list = state.abbrvs.split(", ")

    state.fin_scored_stocks = results_generator.run_results_generator(
        state.scored_articles, state.stocks_list, state.abbrv_list, state.write_file
    )  # get scored stock info


def display_data(state):
    """Displays user data on the Dashboard page."""

    st.markdown("## View An Overview of Your Analyzed Stock Data:")

    if st.checkbox("See All Stocks Overview"):
        st.markdown("### Graphical Sentiment Representation:")
        st.markdown("*Hover over specific columns to get a closer look.*")

        df_all_stock_ovr = pd.DataFrame.from_records(
            state.fin_scored_stocks, index=state.stocks_list
        ).T

        all_ovr_clm = st.multiselect(
            label="Enter the names of stocks scraped below:",
            options=df_all_stock_ovr.columns,
        )  # allow users to display stock information on dataframe graph

        df_all_sent = df_all_stock_ovr.iloc[[1, 10]]  # gets avg sent and trifold rating

        if not all_ovr_clm:  # if nothing is selected show all media!
            st.bar_chart(df_all_sent)
            if st.checkbox("View Data Table"):
                st.markdown("#### Sentiment Data Table:")
                st.write(df_all_sent)
        else:
            st.bar_chart(
                df_all_sent[all_ovr_clm]
            )  # display dataframe/graph that vizualizes info
            if st.checkbox("View Data Table"):
                st.markdown("#### Sentiment Data Table:")
                st.write(df_all_sent[all_ovr_clm])

        st.markdown("### Graphical Price & Well-Being Representation:")
        st.markdown("*Hover over specific columns to get a closer look.*")
        df_all_stock_ovr = df_all_stock_ovr.iloc[[float(17), float(20), float(21)]]

        if not all_ovr_clm:  # if nothing is selected show all media!
            st.bar_chart(df_all_stock_ovr)
            if st.checkbox("View Price & Well-Being Data Table"):
                st.markdown("#### Price & Well-Being Data Table:")
                st.write(df_all_stock_ovr)
        else:
            st.bar_chart(
                df_all_stock_ovr[all_ovr_clm]
            )  # display dataframe/graph that vizualizes info
            if st.checkbox("View Price & Well-Being Data Table"):
                st.markdown("#### Price & Well-Being Data Table:")
                st.write(
                    df_all_stock_ovr[all_ovr_clm]
                )  # display dataframe/graph that vizualizes info

        st.markdown("### Expanded Overview For All Stocks:")
        if st.checkbox("See Expanded Overview for All Stocks"):
            st.markdown("#### Graphical Representation:")
            st.markdown("*Hover over specific columns to get a closer look.*")
            df_all_stock_info = pd.DataFrame.from_records(
                state.fin_scored_stocks, index=state.stocks_list
            ).T

            columns = st.multiselect(
                label="Enter the names of stocks you scraped below:",
                options=df_all_stock_info.columns,
            )  # allow users to display stock information on dataframe graph

            df_all_stock_info = df_all_stock_info

            if not columns:  # if nothing is selected show all media!
                st.bar_chart(df_all_stock_info)
                st.markdown("#### Data Table:")
                st.write(df_all_stock_info)
            else:
                st.bar_chart(
                    df_all_stock_info[columns]
                )  # display dataframe/graph that vizualizes info
                st.markdown("#### Data Table:")
                st.write(
                    df_all_stock_info[columns]
                )  # display dataframe/graph that vizualizes info

    st.write("---")

    # checkboxes for the price, checkbox for stock well being, checkbox for sents, checkbox for media
    st.markdown("## See Individual Stock Graphs/Info")
    for stock in state.fin_scored_stocks:
        st.markdown("### View Content For Stock:")

        if st.checkbox(stock["stock"]):
            st.markdown("### Price Information:")
            st.markdown(
                "#### *Current Price at Time of Scrape:* $"
                + str(stock["current_price"])
            )
            st.markdown(
                "#### *Current Volume at Time of Scrape:* " + str(stock["volume"])
            )
            st.markdown(
                "#### *Average Volume at Time of Scrape:* " + str(stock["avg_volume"])
            )
            st.markdown(
                "#### *1-Year Target Price (from Yahoo! Finance)*: $"
                + str(stock["yr_target"])
            )

            st.markdown(
                "### The Overall Well-Being of this stock seems to be of a "
                + str(stock["stock_well_being_prediction_feelings"])
                + "."
            )

            st.markdown(
                " - *Numerical Stock Well Being Rating (from 0-100%):* "
                + str(stock["stock_well_being_prediction"])
                + "%"
            )

            if st.checkbox(
                "View More Specific Stock Sentiment Information for: " + stock["stock"]
            ):
                st.markdown(
                    "### The Average Stock Sentiment Score was "
                    + str(stock["avg_stock_sent_feelings"])
                    + "."
                )

                st.markdown(
                    "- *Numerical Sentiment Score: *"
                    + str(stock["avg_stock_sent_score"])
                )
                st.markdown(
                    " - *Number of Articles Used For Score:* "
                    + str(stock["article_count"])
                )

                st.write("### View Specific Sentiment Info:")

                ################### RECENT #############################
                if (
                    int(stock["recent_article_count"]) != 0
                ):  # if there are no recent articles, don't give the option to view them
                    if st.checkbox("View Recent Sentiment Info"):
                        # within this give the option for looking at the graph or textual
                        st.markdown("### Recent Sentiment:")

                        st.markdown(
                            "#### The sentiment with the last week was "
                            + str(stock["rcnt_text_sent_rating"])
                            + "."
                        )
                        st.markdown(
                            " - *Numerical Sentiment Score: *"
                            + str(stock["rcnt_text_sent_score"])
                        )
                        st.markdown(
                            " - *Number of Recent Articles Used For Score:* "
                            + str(stock["recent_article_count"])
                        )

                        st.markdown(
                            "#### The sentiment from articles scraped in the last day was "
                            + str(stock["day_stock_sent_rating"])
                        )
                        st.markdown(
                            " - *Numerical Sentiment Score: *"
                            + str(stock["day_stock_sent_score"])
                        )
                        st.markdown(
                            " - *Number of Recent Articles Used For Score:* "
                            + str(stock["day_article_count"])
                        )

                ################### MEDIA #############################
                if st.checkbox("View Media Specific Ratings for " + stock["stock"]):
                    media_results = stock["media_results"]
                    media_list = []
                    for media in stock["media_results"]:
                        media_list.append(media["media"])

                    df_media = pd.DataFrame.from_records(
                        media_results, index=media_list
                    ).T

                    columns = st.multiselect(
                        label="Enter the names of specific media sources below:",
                        options=df_media.columns,
                    )  # allow users to display specific media information on dataframe graph

                    df_media = df_media.iloc[1]  # only use the avg_sentiment
                    if not columns:  # if nothing is selected show all media!
                        st.bar_chart(df_media)
                    else:
                        st.bar_chart(
                            df_media[columns]
                        )  # display dataframe/graph that vizualizes info

                    if st.checkbox("View More In Depth Media-Specific Information"):

                        for media in stock["media_results"]:
                            st.markdown("### Media Source: " + media["media"])
                            st.markdown(
                                "#### The Average Sentiment Rating for this media source was "
                                + str(media["media_sent_rating"])
                            )
                            st.markdown(
                                " - Numerical Score: "
                                + str(media["media_avg_sent_score"])
                            )
                            st.markdown(
                                " - Article Count for this Media Source: "
                                + str(media["article_count"])
                            )
                ################################################

                if st.checkbox("View all Articles for " + stock["stock"]):
                    st.markdown("#### Choose Specific Articles to View:")
                    for article in state.scored_articles:
                        if article["stock"] == stock["stock"]:
                            if st.checkbox("View article: " + article["title"]):
                                st.write(article)

                if st.checkbox("View Stock Trifold Rating for " + stock["stock"]):
                    st.markdown(
                        "### The Overall Stock Trifold Rating was "
                        + str(stock["ovr_stock_trifold_feelings"])
                    )
                    st.markdown(
                        " - *Numerical Overall Stock Trifold Rating:* "
                        + str(stock["ovr_stock_trifold_rating"])
                    )
                    st.markdown(
                        " - *** This rating is the: Average rating of all article sentiment ratings for the title, description/summary, and text."
                    )

        st.write("---")


def page_settings(state):
    st.title(":wrench: Run Settings")
    st.markdown("### Your Chosen Settings are Currently:")
    display_state_values(state)

    st.write("---")
    st.markdown("## Choose your Run Type and configure it's Settings:")

    if st.checkbox("Read in Previous CSV", state.cb_csvread):
        state.cb_csvread = True
        st.markdown("#### Enter CSV Import File:")
        state.csv_file = st.text_input(
            "Enter CSV Filename (EX: oldresults.csv)", state.csv_file or ""
        )
        state.write_file = ""
        if st.button("Read in CSV", state.bt_csv):
            state.bt_csv = True
            read_csv(state)
        if state.bt_csv == True:
            st.markdown("## *Go to the dashboard to view your data.*")

    elif st.checkbox("Fresh Run", state.cb_freshrun):
        state.cb_freshrun = True

        st.markdown("#### Enter Stock Names:")
        state.stocks = st.text_input(
            "Enter Stock Names Separated by Commas (EX: apple, microsoft):",
            state.stocks or "",
        )
        st.markdown("#### Enter Stock Ticker Symbols:")
        state.abbrvs = st.text_input(
            "Enter Stock Ticker Symbols Separated by Commas in the same order as your stocks (EX: aapl, msft):",
            state.abbrvs or "",
        )

        st.markdown("#### Enter Date Range for Scraping:")
        state.start_date = st.text_input(
            "Enter Start of Date Range (EX: 11/21/2020):", state.start_date or ""
        )
        state.end_date = st.text_input("Enter End of Date Range:", state.end_date or "")

        st.markdown("#### Choose Websites for Scraping:")
        state.websites = []
        if st.checkbox("Motley Fool", state.cb_motfool):
            state.cb_motfool = True
            state.websites.append("www.fool.com")
        if st.checkbox("Yahoo! Finance", state.cb_yahoo):
            state.cb_yahoo = True
            state.websites.append("finance.yahoo.com")
        if st.checkbox("Bloomberg", state.cb_bloomberg):
            state.cb_bloomberg = True
            state.websites.append("www.bloomberg.com")
        if st.checkbox("MarketWatch", state.cb_mktwtch):
            state.cb_mktwtch = True
            state.websites.append("www.marketwatch.com")
        if st.checkbox("Wall Street Journal", state.cb_wsj):
            state.cb_wsj = True
            state.websites.append("www.wsj.com")

        st.markdown("#### Enter CSV Export File:")
        state.write_file = st.text_input(
            "Enter a CSV to save your result to (EX: myresults.csv):",
            state.write_file or "",
        )

        if st.button("Run the Scraping Tool", state.bt_fresh):
            state.bt_fresh = True
            st.markdown("### *PLEASE WAIT! Scraping and analyzing your articles now!*")
            fresh_run(state)
        if state.bt_fresh == True:
            st.markdown(
                "## *Go to the dashboard to view your newly scraped data data.*"
            )


def display_state_values(state):
    st.write("Read in Old CSV: ", state.cb_csvread)
    st.write("Chosen CSV Import Filename: ", state.csv_file)
    st.write("Chosen Stocks: ", state.stocks)
    st.write("Corresponding Stock Ticker Symbols (Abbreviations): ", state.abbrvs)
    st.write("Start of Date Range: ", state.start_date)
    st.write("End of Date Range: ", state.end_date)
    st.write("Selected Websites: ", state.websites)
    st.write("Chosen CSV Export Filename: ", state.write_file)

    if st.button("Reset Current Run Options (Restart Tool)"):
        state.clear()


class _SessionState:
    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(
                self._state["data"], None
            ):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


if __name__ == "__main__":
    main()
