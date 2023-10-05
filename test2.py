import streamlit as st
from streamlit_lightweight_charts import st_lightweight_chart, plot
import pandas as pd

st.set_page_config(layout='wide')

# Sample DataFrame
data = {
    'Date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'],
    'Open': [100, 101, 102, 103],
    'High': [102, 103, 104, 105],
    'Low': [98, 99, 100, 101],
    'Close': [101, 102, 103, 104],
    'Volume': [500, 505, 510, 515]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Convert DataFrame to the format expected by the plot function
plot_data = df.to_dict(orient="records")

# Prepare the data in the format expected by the library
formatted_data = [
    {
        "time": row["Date"],
        "open": row["Open"],
        "high": row["High"],
        "low": row["Low"],
        "close": row["Close"]
    }
    for row in plot_data
]

st_lightweight_chart(plot(formatted_data, type="candlestick"))
