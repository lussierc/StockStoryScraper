import streamlit as st
import csv_handler
import results_generator
import pandas as pd
from PIL import Image
from streamlit.hashing import _CodeHasher
# other files:
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
    state = _get_state()
    pages = {
        "Home": page_home,
        "Dashboard": page_dashboard,
        "Settings": page_settings,
    }

    st.sidebar.title(":floppy_disk: Page states")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()

def page_home(state):
    st.title("WELCOME TO STOCKTEXTMINING")
    st.write("Welcome to the homepage lets go!")

def page_dashboard(state):
    st.title(":chart_with_upwards_trend: Dashboard page")
    display_state_values(state)
    st.write("---")


    if state.cb_csvread == True:
        st.write("we will read in ur csv now")
        display_data(state)
    elif state.cb_freshrun == True:
        st.write("Here is your newly scraped data:")
        display_data(state)


def read_csv(state):
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
    )

    scored_articles = articles  # since articles are only read in from csv, they are already scored

    for article in scored_articles:
        if article["stock"] in stocks_list:
            pass
        else:
            stocks_list.append(article["stock"])

        if article["abbrv"] in abbrv_list:
            pass
        else:
            abbrv_list.append(article["abbrv"])

    st.markdown('CSV has successfully been read in!')
        # find duplicate links and remove them
    links = []
    for article in scored_articles:
        check_list = isinstance(article, list)
        if article["link"] in links:
            print("*!!* Duplicate article - removing...", article["link"])
            scored_articles.remove(article)
        else:
            links.append(article["link"])

    state.scored_articles = scored_articles
    state.stocks_list = stocks_list
    state.abbrv_list = abbrv_list
    state.fin_scored_stocks = results_generator.generate_results(stocks_list, abbrv_list, scored_articles)

def fresh_run(state):
    inputted_csv_list = []

    # run thru process with only new articles
    article_dicts = search_scraper.run_web_search_scraper(
      state.stocks, state.abbrvs, state.websites, state.start_date, state.end_date, inputted_csv_list
    )
    articles = sentiment_analyzer.analyze_all_articles(article_dicts)
    state.scored_articles = results_generator.calc_article_sent_scores(articles)
    state.stocks_list = state.stocks.split(", ")
    state.abbrv_list = state.abbrvs.split(", ")
    state.fin_scored_stocks = results_generator.run_results_generator(
        state.scored_articles, state.stocks_list, state.abbrv_list
    )

def display_data(state):
    st.markdown("## View Summary Info for all Stocks:")
    if st.checkbox('See All Stocks Overview'):
        df = pd.DataFrame(state.fin_scored_stocks, index = state.stocks_list).T
        st.bar_chart(df)  # display dataframe/graph that vizualizes commit info

    #checkboxes for the price, checkbox for stock well being, checkbox for sents, checkbox for media

    st.markdown('## See Individual Stock Graphs/Info')
    for stock in state.fin_scored_stocks:

        st.markdown("### View Content For Stock:")

        if st.checkbox(stock['stock']):
            st.markdown("### Price Information:")
            st.markdown("#### Current Price at Time of Scrape:")
            st.write(stock['current_price'])
            st.markdown("#### Current Volume at Time of Scrape:")
            st.write(stock['volume'])
            st.markdown("#### Average Volume at Time of Scrape:")
            st.write(stock['avg_volume'])

            st.markdown("### Stock Well Being Prediction:")
            st.write(stock['stock_well_being_prediction'])
            st.markdown("#### The tool rates this stock as having this level of well being: " + stock['stock_well_being_prediction_feelings'])

            if st.checkbox('View Sentiment Information'):
                st.markdown('### Average Stock Sentiment Score:')
                st.write(stock['avg_stock_sent_score'])
                st.markdown('#### # of Articles:')
                st.write(stock['article_count'])

                st.write("### View Specific Sentiment Info:")
                if st.checkbox('View Recent Sentiment Info'):
                    # within this give the option for looking at the graph or textual
                    st.markdown("### Recent Sentiment:")
                    st.markdown("#### Within the last week:")
                    st.write(stock['rcnt_text_sent_score'])
                    st.markdown("Number of articles within this time frame:")
                    st.write(stock['recent_article_count'])
                    st.markdown("#### Within the last day:")
                    st.write(stock['day_stock_sent_score'])
                    st.markdown("Number of articles scraped/analyzed for the last day:")
                    st.write(stock['day_article_count'])

                if st.checkbox('View Media Specific Ratings'):
                    for media in stock['media_results']:
                        st.markdown("### Media Source: " + media['media'])

                        st.markdown("#### Media Average Sent Score:")
                        st.write(media['media_avg_sent_score'])

                        st.markdown("For this media source, the sentiment was rated overall as:")
                        st.write(media['media_sent_rating'])

                        st.markdown("#### Article Count:")
                        st.write(media['article_count'])
                st.markdown("### Overall Stock Trifold Rating")
                st.markdown("Average rating of all article sentiment ratings for the title, description/summary, and text.")
                st.write(stock['ovr_stock_trifold_rating'])

def page_settings(state):
    st.title(":wrench: Fresh Run")
    display_state_values(state)

    st.write("---")
    if st.checkbox("Read in Previous CSV", state.cb_csvread):
        state.cb_csvread = True
        state.csv_file = st.text_input("Enter CSV Filename", state.csv_file or "")
        if st.button("Read in CSV", state.bt_csv):
            state.bt_csv = True
            read_csv(state)
        if state.bt_csv == True:
            st.write("Go to the dashboard to view your data.")

    elif st.checkbox("Fresh Run", state.cb_freshrun):
        state.cb_freshrun = True

        options = ["Hello", "World", "Goodbye"]
        state.stocks = st.text_input("Enter Stock Names", state.stocks or "")
        state.abbrvs = st.text_input("Enter Stock Tickers", state.abbrvs or "")
        state.start_date = st.text_input("Enter Start of Date Range", state.start_date or "")
        state.end_date = st.text_input("Enter End of Date Range", state.end_date or "")

        # state.slider = st.slider("Set slider value.", 1, 10, state.slider)
        # state.radio = st.radio("Set radio value.", options, options.index(state.radio) if state.radio else 0)
        #state.foolbox = st.checkbox("Set checkbox value.", state.foolbox)

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



        if st.button("Run the Scraping Tool", state.bt_fresh):
            state.bt_fresh = True
            fresh_run(state)
        if state.bt_fresh == True:
            st.write("Go to the dashboard to view your newly scraped data.")

    # if st.checkbox("Set checkbox2 value."):
    #     state.websites.append("Yahoo")

    # state.selectbox = st.selectbox("Select value.", options, options.index(state.selectbox) if state.selectbox else 0)
    # state.multiselect = st.multiselect("Select value(s).", options, state.multiselect)
    #
    # # Dynamic state assignments
    # for i in range(3):
    #     key = f"State value {i}"
    #     state[key] = st.slider(f"Set value {i}", 1, 10, state[key])


def display_state_values(state):
    st.write("Read in Old CSV", state.cb_csvread)
    st.write("CSV Name", state.csv_file)
    st.write("Input state:", state.stocks)
    st.write("Input state:", state.abbrvs)
    st.write("Input state:", state.start_date)
    st.write("Input state:", state.end_date)

    # st.write("Slider state:", state.abbrvs)
    # st.write("Radio state:", state.radio)
    #st.write("Motley Fool state:", state.foolbox)
    st.write("Websites:", state.websites)
    # st.write("Selectbox state:", state.selectbox)
    # st.write("Multiselect state:", state.multiselect)
    #
    # for i in range(3):
    #     st.write(f"Value {i}:", state[f"State value {i}"])

    if st.button("Clear state"):
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
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
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
