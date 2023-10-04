import streamlit as st
import db_manager as dbm
import plotly.graph_objects as go
import datetime
import yfinance as yf
import pandas as pd
import numpy as np



from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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
    symbol = symbol.split('.')[0]
     
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
    st.markdown(html_code, unsafe_allow_html=True)

def get_df(symbol):
    
    # Initialize a Yahoo Finance Ticker object
    ticker = yf.Ticker(symbol)
    # Fetch historical stock data for the past 5 years
    data = ticker.history(period="5y")
    # Create a DataFrame with the time series data
    df = pd.DataFrame(data)
    df = df.drop(columns=['Dividends', 'Stock Splits'])
    print(df.head())
    # Convert the index to a column
    df.reset_index(inplace=True)
    # Convert the Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    # Sort the DataFrame by the index
    df.sort_index(inplace=True)
    #st.write(df)
    return df


# Execute the main function
if __name__ == '__main__':

    page_icon="🚀"  
    st.set_page_config(page_title="Predict Stock Prices", layout="wide", page_icon=page_icon)
    #st.sidebar.title('Predict Stock Prices')
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
    st.sidebar.write("---")
    selected = st.sidebar.selectbox("Select a Stock:", options)
    selected_symbol = selected.split(" ")[0]  # extracting the selected symbol

    st.sidebar.write("---")
 

    # st.sidebar.write(f"## Add New Stock")
    # st.sidebar.text_input("Symbol", value="", max_chars=None, key=None, type='default')

    # Date input for start and end dates
    today = datetime.date.today()
    # start_date = st.sidebar.date_input("Start date", today - datetime.timedelta(days=365 *3))
    # end_date = st.sidebar.date_input("End date", today)

    start_date = (today - datetime.timedelta(days=365 *3))
    end_date = today

    #st.sidebar.write(f"Fetching data from {start_date} to {end_date}")


    # if st.sidebar.button("Add Stock to Database"):
    #     # Note: Add your database connection logic and pass the database object to the function
    #     # db = YourDatabaseConnectionFunction()
    #     dbm.fetch_and_save_stock_data(db, selected_symbol, start_date, end_date)
    #     st.write("Data fetched and saved!")

    # st.sidebar.write("---")
    

    # Display the selected stock name
    st.subheader(f"{symbol_to_name[selected_symbol]}")

        # Fetch stock data for the selected symbol and convert it to a DataFrame
    df = dbm.get_stock_data_as_dataframe(db, selected_symbol)

    tb1, tb2, tb3,tb4,tb5, tb6 = st.tabs(["Graph","Data","Logistic Regression", "Random Forest & XGBoost", "Long Short-Term Memory (LSTM)", "Prophet"  ])

    
    with tb1:
        
        fig = plot_stock_prices(selected_symbol)
        st.plotly_chart(fig)
        st.write(selected_symbol)
        #trade_view_graph(selected_symbol)
        df=get_df(selected_symbol)
        



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
        df= get_df(selected_symbol)
        # Feature Engineering
        df['Trend'] =(df['Close'].diff() > 0).astype(int)
        
        # Drop NaN values created due to differencing
        df.dropna(inplace=True)

        features = df.drop(columns=['Trend', 'Close']).columns.tolist()
        target = 'Trend'

        train_df, test_df = train_test_split(df, test_size=0.2, shuffle=False)
        X_train, y_train = train_df[features], train_df[target]
        X_test, y_test = test_df[features], test_df[target]

        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.fit_transform(X_test)

        # Train a Logistic Regression model
        from numpy.random.mtrand import logistic
        #Build and Train Model
        model = LogisticRegression()
        model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        y_pred  =model.predict(X_test_scaled)

    
        st.subheader('Model Evaluation')
        st.write("---")
        # Displaying Accuracy with a bar chart
        st.write('## Accuracy')
        accuracy = accuracy_score(y_test, y_pred)
        accuracy_chart = pd.DataFrame({'Accuracy': [accuracy]}, index=['Model'])
        st.write(accuracy_chart)
        #st.bar_chart(accuracy_chart)

        # Classification Report
        st.write('## Classification Report')
        st.text(classification_report(y_test, y_pred))

    
        import plotly.figure_factory as ff

        # # Confusion Matrix using DataFrame for better presentation
        # st.write('## Confusion Matrix')
        # cm = confusion_matrix(y_test, y_pred)
        # cm_df = pd.DataFrame(cm, index=['Actual Negative', 'Actual Positive'], columns=['Predicted Negative', 'Predicted Positive'])
        # st.write(cm_df)

        # Confusion Matrix using DataFrame for better presentation
        st.write('## Confusion Matrix')
        cm = confusion_matrix(y_test, y_pred)
        cm_df = pd.DataFrame(cm, index=['Actual Negative', 'Actual Positive'], columns=['Predicted Negative', 'Predicted Positive'])

        # Using plotly to display heatmap
        fig = ff.create_annotated_heatmap(z=cm_df.values, x=list(cm_df.columns), y=list(cm_df.index), colorscale='Blues', showscale=True)

        st.plotly_chart(fig)
        
        st.write(df)


    with tb4:
        st.write("Random Forest & XGBoost")
    
    with tb5:
        st.write("Long Short-Term Memory (LSTM)")

    with tb6:
        st.write("Prophet")
    


    
    #Close the database connection
    db.close()
    #st.write("Database connection closed")