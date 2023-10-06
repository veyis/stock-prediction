import pandas as pd
import yfinance as yf
import time

def get_symbols_from_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df['Symbol'].tolist()
    except Exception as e:
        print(f"Error reading {filename}. Reason: {e}")
        return []

filename = "ist.csv"
symbols = get_symbols_from_csv(filename)

for stock in symbols:
    try:
        stock_details = yf.Ticker(stock).info
        # get this info Symbol', 'Name', 'MarketCap', 'Country', 'IPOYear', 'Sector', 'Industry'
        print(stock_details['symbol'], stock_details['longName'], stock_details['marketCap'],
              stock_details.get('country', 'N/A'), stock_details.get('ipoYear', 'N/A'),
              stock_details.get('sector', 'N/A'), stock_details.get('industry', 'N/A')) 

        # wrtie to csv
        with open('ist2.csv', 'a') as f:
            f.write(f"{stock_details['symbol']},{stock_details['longName']},{stock_details['marketCap']},"
                    f"{stock_details.get('country', 'N/A')},{stock_details.get('ipoYear', 'N/A')},"
                    f"{stock_details.get('sector', 'N/A')},{stock_details.get('industry', 'N/A')}\n")
        
        
        # Optional: add a delay between requests
        time.sleep(1)

    except Exception as e:
        print(f"Error reading from yahoo for stock {stock}. Reason: {e}")



# def save_csv_to_database(db, data):
#     for row in data:
#         symbol = row[0]
#         name = row[1]
#         market_cap = float(row[5].replace(',', '').replace('"', '').replace(' ', ''))
#         country = row[6]
#         ipo_year = int(row[7]) if row[7] else None
#         sector = row[9]
#         industry = row[10]

#         # Insert into Stocks table
#         db.insert('Stocks', ['Symbol', 'Name', 'MarketCap', 'Country', 'IPOYear', 'Sector', 'Industry'],
#                   [symbol, name, market_cap, country, ipo_year, sector, industry])
        
