import streamlit as st
import db_manager as dbm

  
def streamlit_settings():
    # Custom CSS to narrow the top margin
    st.markdown("""
    <style>
    .reportview-container .main .block-container {
        margin-top: 0px;  /* Adjust the value to your preference */
    }
    </style>
    """, unsafe_allow_html=True)

    



# Execute the main function
if __name__ == '__main__':

    # Set the page title and the layout
    page_icon="🚀"  # You can specify the emoji as the icon
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
    st.write(f"Stock Name: {symbol_to_name[selected_symbol]}")

    # Fetch stock details for the selected symbol
    selected_stock_details = dbm.fetch_stock_details_by_symbol(db, selected_symbol)

    # Display stock details
    if selected_stock_details:
        st.sidebar.write("### Stock Details:")
        columns = ['Symbol', 'Name', 'MarketCap', 'Country', 'IPOYear', 'Sector', 'Industry']
        for col, value in zip(columns, selected_stock_details):
            st.sidebar.write(f"**{col}:** {value}")
    else:
        st.sidebar.warning("No details found for the selected stock!")


    # Fetch stock data for the selected symbol and convert it to a DataFrame
    df = dbm.get_stock_data_as_dataframe(db, selected_symbol)

    tb1, tb2, tb3,tb4,tb5 = st.tabs(["Data","Logistic Regression", "Random Forest & XGBoost", "Long Short-Term Memory (LSTM)", "Prophet"  ])

    with tb1:
        #Display the dataframe in Streamlit
        st.write(df)
    
    with tb2:
        st.write("Logistic Regression")

    with tb3:
        st.write("Random Forest & XGBoost")
    
    with tb4:
        st.write("Long Short-Term Memory (LSTM)")

    with tb5:
        st.write("Prophet")
    
    



    
    #Close the database connection
    db.close()

    st.write("Database connection closed")