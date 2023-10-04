import db_manager as dbm


def save_nasdaq_to_database():
    # Create a database connection
    db=dbm.Database()

    parsed_data = dbm.read_csv_from_file('nasdaq2.csv')
    dbm.save_csv_to_database(db, parsed_data)

    # Display the inserted data
    dbm.display_stocks(db)

    # Close the database connection
    db.close() 

    print("Database connection closed")


def get_yahoo_to_database(start_date, end_date):
    db = dbm.Database()
    symbols = dbm.fetch_symbols_from_database(db)
    for symbol in symbols:
        print(symbol)
        dbm.fetch_and_save_stock_data(db, symbol, start_date, end_date)

    db.close()



if __name__ == '__main__':
    
    get_yahoo_to_database('2018-01-01', '2018-12-31')

    # save_nasdaq_to_database()


