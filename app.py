import streamlit as st
import db_manager as dbm

  


# Execute the main function
if __name__ == '__main__':

    # Set the page title and the layout
    page_icon="🚀"  # You can specify the emoji as the icon
    st.set_page_config(page_title="Predict Stock Prices", layout="wide", page_icon=page_icon)
    st.sidebar.title('Predict Stock Prices')



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


    # Fetch stock data for the selected symbol and convert it to a DataFrame
    df = dbm.get_stock_data_as_dataframe(db, selected_symbol)

    #Display the dataframe in Streamlit
    st.write(df)

    #Close the database connection
    db.close()

    st.write("Database connection closed")