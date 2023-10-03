# db_manager.py

from datetime import datetime
import psycopg2
import yfinance as yf
import csv
import pandas as pd

from decouple import config


class Database:
    def __init__(self):
        self._connect()
        
    def _connect(self):
        self.connection = psycopg2.connect(
            dbname=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            port=config('DB_PORT')
        )
        self.cursor = self.connection.cursor()
        
    def close(self):
        if self.connection:
            if hasattr(self, 'cursor'):
                self.cursor.close()
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def execute(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()

    def fetch(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching from database: {e}")
            return []

    def insert(self, table, columns, values):
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        self.execute(query, values)

    def update(self, table, columns, values, condition):
        set_clause = ', '.join([f"{col} = %s" for col in columns])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.execute(query, values)

    def delete(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute(query)

    def drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name};"
        self.execute(query)



def display_stocks(db):
    stocks = db.fetch("SELECT * FROM Stocks")
    print("\nStocks:")
    print("-" * 80)
    for stock in stocks:
        print(f"Symbol: {stock[0]} | Name: {stock[1]} | MarketCap: {stock[2]} | Country: {stock[3]} | IPOYear: {stock[4]} | Sector: {stock[5]} | Industry: {stock[6]}")

def display_stock_prices(db):
    stock_prices = db.fetch("SELECT * FROM StockPrices")
    print("\nStock Prices:")
    print("-" * 80)
    for price in stock_prices:
        print(f"Symbol: {price[0]} | Date: {price[1]} | Opening: {price[2]} | Closing: {price[3]} | High: {price[4]} | Low: {price[5]} | Volume: {price[6]}")



def read_tickers_from_file(file_path):
    with open(file_path, 'r') as f:
        tickers = [line.strip() for line in f.readlines()]
        print(f"Read {len(tickers)} tickers from file")
    return tickers

def save_stock_prices(db, symbol, period):
    stock_data = yf.download(symbol, period=period)
    print(f"Saving data for {symbol}...")
    print(stock_data)

    for index, row in stock_data.iterrows():
        db.insert('StockPrices', 
              ['Symbol', 'Date', 'OpeningPrice', 'ClosingPrice', 'High', 'Low', 'Volume'], 
              [symbol, index.date(), row['Open'], row['Close'], row['High'], row['Low'], int(row['Volume'])])

def manage_stocks(db, file_path):
    tickers = read_tickers_from_file(file_path)
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        period="MAX"
        save_stock_prices(db, ticker, period)


def read_csv_from_file(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        headers = next(reader)
        return [row for row in reader]

# Save parsed data to database
def save_csv_to_database(db, data):
    for row in data:
        symbol = row[0]
        name = row[1]
        market_cap = float(row[5].replace(',', '').replace('"', '').replace(' ', ''))
        country = row[6]
        ipo_year = int(row[7]) if row[7] else None
        sector = row[9]
        industry = row[10]

        # Insert into Stocks table
        db.insert('Stocks', ['Symbol', 'Name', 'MarketCap', 'Country', 'IPOYear', 'Sector', 'Industry'],
                  [symbol, name, market_cap, country, ipo_year, sector, industry])


def fetch_symbols_from_database(db):
    return [row[0] for row in db.fetch("SELECT Symbol FROM Stocks")]

def fetch_and_save_stock_data(db, symbol, period):
    print(f"Fetching data for {symbol}...")
    
    stock_data = yf.download(symbol, period=period)
    
    for index, row in stock_data.iterrows():
        date = index.date()
        opening_price = float(row['Open'])
        closing_price = float(row['Close'])
        high = float(row['High'])
        low = float(row['Low'])
        volume = int(row['Volume'])
        
        db.insert('StockPrices', 
                  ['Symbol', 'Date', 'OpeningPrice', 'ClosingPrice', 'High', 'Low', 'Volume'], 
                  [symbol, date, opening_price, closing_price, high, low, volume])

        print(f"Added data for {symbol} on {date}")


def get_stock_data_as_dataframe(db, symbol):
    """
    Fetch stock data for the given symbol and return as a pandas DataFrame.
    """
    stock_data = db.fetch(f"SELECT * FROM StockPrices WHERE Symbol='{symbol}'")
    columns = ['Symbol', 'Date', 'OpeningPrice', 'ClosingPrice', 'High', 'Low', 'Volume']
    df = pd.DataFrame(stock_data, columns=columns)
    return df


if __name__ == '__main__':

    db = Database()
    print("Connected to database")

    # # Stocks table creation
    # stocks_table_query = """
    # CREATE TABLE IF NOT EXISTS Stocks (
    #     Symbol VARCHAR(10) PRIMARY KEY,
    #     Name TEXT,
    #     MarketCap BIGINT,
    #     Country VARCHAR(50),
    #     IPOYear INTEGER,
    #     Sector VARCHAR(50),
    #     Industry VARCHAR(100)
    # );
    # """
    # db.execute(stocks_table_query)

    # # StockPrices table creation
    # stock_prices_table_query = """
    # CREATE TABLE IF NOT EXISTS StockPrices (
    #     Symbol VARCHAR(10) REFERENCES Stocks(Symbol),
    #     Date TIMESTAMP NOT NULL,
    #     OpeningPrice NUMERIC,
    #     ClosingPrice NUMERIC,
    #     High NUMERIC,
    #     Low NUMERIC,
    #     Volume BIGINT,
    #     PRIMARY KEY (Symbol, Date)
    # );
    # """
    # db.execute(stock_prices_table_query)



    # Inserting data into Stocks table
    # stocks_records = [
    #     ('AAPL', 'Apple Inc.', 2000000000000, 'USA', 1980, 'Technology', 'Consumer Electronics'),
    #     ('GOOGL', 'Alphabet Inc.', 1400000000000, 'USA', 2004, 'Technology', 'Internet Content & Information'),
    #     ('AMZN', 'Amazon.com Inc.', 1600000000000, 'USA', 1997, 'Consumer Cyclical', 'Internet Retail')
    #      ]

    # for record in stocks_records:
    #     db.insert('Stocks', ['Symbol', 'Name', 'MarketCap', 'Country', 'IPOYear', 'Sector', 'Industry'], record)

    # # Adding records for StockPrices


    # stock_prices_records = [
    #     ('AAPL', datetime(2023, 4, 5), 140.5, 142.2, 143.0, 140.0, 100000000),
    #     ('AAPL', datetime(2023, 4, 6), 142.2, 142.0, 142.8, 141.5, 95000000),
    #     ('GOOGL', datetime(2023, 4, 5), 2200, 2215, 2230, 2190, 1500000),
    #     ('AMZN', datetime(2023, 4, 5), 3100, 3120, 3135, 3090, 3000000),
    # ]

    # for record in stock_prices_records:
    #     db.insert('StockPrices', ['Symbol', 'Date', 'OpeningPrice', 'ClosingPrice', 'High', 'Low', 'Volume'], record)


    # parsed_data = read_csv_from_file('nasdaq2.csv')
    # save_csv_to_database(db, parsed_data)

    # # Display the inserted data
    # display_stocks(db)

    # symbols = fetch_symbols_from_database(db)
    # for symbol in symbols:
    #     print(symbol)
    #     fetch_and_save_stock_data(db, symbol, period="1Y")


    # db.close()