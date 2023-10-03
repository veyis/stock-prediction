import streamlit as st
import db_manager as dbm
import plotly.graph_objects as go

  
def streamlit_settings():
    # Custom CSS to narrow the top margin
    st.markdown("""
    <style>
    .reportview-container .main .block-container {
        margin-top: 0px;  /* Adjust the value to your preference */
    }
    </style>
    """, unsafe_allow_html=True)

    # Custom CSS to hide the hamburger menu and footer
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

def plot_stock_prices(symbol):
    # Using your db_manager to get data as a DataFrame
    db = dbm.Database()
    df = dbm.get_stock_data_as_dataframe(db, symbol)
    db.close()
    
    # Create a Plotly figure
    fig = go.Figure()

    # Add trace for stock prices
    fig.add_trace(go.Candlestick(x=df['Date'],
                open=df['OpeningPrice'],
                high=df['High'],
                low=df['Low'],
                close=df['ClosingPrice'],
                name=symbol))

    # Set the title
    fig.update_layout(title=f"Stock prices for {symbol}")

    return fig

def trade_view_graph(symbol):
    html_code = f'''
    <div id="tradingview_34f5a" class="tradingview-widget-container">
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            var userLang = navigator.language || navigator.userLanguage;
            var tradingViewLocale = userLang.substring(0, 2);
            
            new TradingView.widget({{
                "width": 980,
                "height": 610,
                "symbol": "{symbol}",
                "interval": "D",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": tradingViewLocale,
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "allow_symbol_change": true,
                "container_id": "tradingview_34f5a"
            }});
        </script>
    </div>
    '''
    st.components.v1.html(html_code, width=1000, height=630)


# Execute the main function
if __name__ == '__main__':

    page_icon="🚀"  
    st.set_page_config(page_title="Predict Stock Prices", layout="wide", page_icon=page_icon)
    st.sidebar.title('Predict Stock Prices')
    streamlit_settings()

    # Create a database connection
    db = dbm.Database()
    
    # Fetch stock symbols and names
    stock_symbols_and_names = dbm.fetch_stock_symbols_and_names(db)

    # Unzip the symbols and names into separate lists
    symbols, names = zip(*stock_symbols_and_names)

    # Create a dictionary to map symbol to name for display purposes
    symbol_to_name = dict(zip(symbols, names))
    options = [f"{symbol} - {name}" for symbol, name in symbol_to_name.items()]

    # Streamlit selectbox
    selected = st.sidebar.selectbox("Select a Stock:", options)
    selected_symbol = selected.split(" ")[0]  # extracting the selected symbol

    # Display the selected stock name
    st.subheader(f"{symbol_to_name[selected_symbol]}")

        # Fetch stock data for the selected symbol and convert it to a DataFrame
    df = dbm.get_stock_data_as_dataframe(db, selected_symbol)

    tb1, tb2, tb3,tb4,tb5, tb6 = st.tabs(["Graph","Data","Logistic Regression", "Random Forest & XGBoost", "Long Short-Term Memory (LSTM)", "Prophet"  ])

    
    with tb1:
        
        # fig = plot_stock_prices(selected_symbol)
        # st.plotly_chart(fig)
        trade_view_graph(selected_symbol)

        



    with tb2:
        #Display the dataframe in Streamlit
        st.write(df)
        # Fetch stock details for the selected symbol
        selected_stock_details = dbm.fetch_stock_details_by_symbol(db, selected_symbol)

        # Display stock details
        if selected_stock_details:
            st.write("### Stock Details:")
            columns = ['Symbol', 'Name', 'MarketCap', 'Country', 'IPOYear', 'Sector', 'Industry']
            for col, value in zip(columns, selected_stock_details):
                st.write(f"**{col}:** {value}")
        else:
            st.warning("No details found for the selected stock!")


    
    with tb3:
        st.write("Logistic Regression")

    with tb4:
        st.write("Random Forest & XGBoost")
    
    with tb5:
        st.write("Long Short-Term Memory (LSTM)")

    with tb6:
        st.write("Prophet")
    


    
    #Close the database connection
    db.close()
    #st.write("Database connection closed")