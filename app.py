import streamlit as st
import db_manager as dbm

  


# Execute the main function
if __name__ == '__main__':

    st.set_page_config(page_title="Stock Data Viewer", layout="wide")

    # Set the page title and the layout
    st.title('Stock Data Viewer')

    # Create a database connection
    db = dbm.Database()
    
    st.write("Connected to database from app.py")

    # Create a dropdown menu for user to select a stock symbol
    symbols = ['AAPL', 'GOOGL', 'AMZN']  # Add more symbols or fetch them dynamically from the Stocks table in your db_manager.py
    selected_symbol = st.selectbox('Choose a stock symbol:', symbols)
    
    #st.write("You selected: ", selected_symbol)


    # Fetch stock data for the selected symbol and convert it to a DataFrame
    df = dbm.get_stock_data_as_dataframe(db, selected_symbol)

    #Display the dataframe in Streamlit
    st.write(df)

    #Close the database connection
    db.close()

    st.write("Database connection closed")