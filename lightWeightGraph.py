import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import json
import numpy as np
import yfinance as yf
import pandas as pd
import pandas_ta as ta


COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'   # #ef5350
bck_color = '#02172d'
txt_color ='white'
g_width = 600
g_height = (g_width/3)*2


def fetch_data(ticker, period):
    df = yf.Ticker(ticker).history(period=period)[['Open', 'High', 'Low', 'Close', 'Volume']]
    return df, ticker

def preprocess_data(df):
    df = df.reset_index()
    df.columns = ['time','open','high','low','close','volume']
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')
    df['color'] = np.where(df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)
    df.ta.macd(close='close', fast=6, slow=12, signal=5, append=True)
    return df


def convert_to_json(df):
    candles = json.loads(df.to_json(orient="records"))
    volume = json.loads(df.rename(columns={"volume": "value"}).to_json(orient="records"))
    macd_fast = json.loads(df.rename(columns={"MACDh_6_12_5": "value"}).to_json(orient="records"))
    macd_slow = json.loads(df.rename(columns={"MACDs_6_12_5": "value"}).to_json(orient="records"))
    df['color'] = np.where(df['MACD_6_12_5'] > 0, COLOR_BULL, COLOR_BEAR)
    macd_hist = json.loads(df.rename(columns={"MACD_6_12_5": "value"}).to_json(orient="records"))
    return candles, volume, macd_fast, macd_slow, macd_hist

def display_multipane_chart(df,ticker, period):

  
    st.subheader("Multipane Chart with Pandas")

    df = preprocess_data(df)
    candles, volume, macd_fast, macd_slow, macd_hist = convert_to_json(df)
    

    chartMultipaneOptions = [
    {
        "width": g_width,
        "height": g_height,
        "layout": {
            "background": {
                "type": "solid",
                "color": bck_color
            },
            "textColor": txt_color
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.2)"
                },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.2)"
            }
        },
        "crosshair": {
            "mode": 0
        },
        "priceScale": {
            "borderColor": "rgba(197, 203, 206, 0.7)",
        
            
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.7)",
            "barSpacing": 20
        },
        "watermark": {
            "visible": True,
            "fontSize": 48,
            "horzAlign": 'center',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.3)',
            "text": ticker,
        }
    },
    {
        "width": g_width,
        "height": g_height/4,
        "layout": {
            "background": {
                "type": 'solid',
                "color": 'transparent'
            },
            "textColor": txt_color,
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0.2)',
            }
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'top',
            "color": 'rgba(171, 71, 188, 0.5)',
            "text": 'Volume',
        }
    },
    {
        "width": g_width,
        "height": g_height/4,
        "layout": {
            "background": {
                "type": "solid",
                "color": bck_color
            },
            "textColor": txt_color
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'MACD',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0.2)',
            }
        },
     }
    ]

    seriesCandlestickChart = [
        {
            "type": 'Candlestick',
            "data": candles,
            "options": {
                "upColor": COLOR_BULL,
                "downColor": COLOR_BEAR,
                "borderVisible": False,
                "wickUpColor": COLOR_BULL,
                "wickDownColor": COLOR_BEAR
            }
        }
    ]

    seriesVolumeChart = [
        {
            "type": 'Histogram',
            "data": volume,
            "options": {
                "priceFormat": {
                    "type": 'volume',
                },
                "priceScaleId": "" # set as an overlay setting,
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0,
                    "bottom": 0,
                },
                "alignLabels": False
            }
        }
    ]

    seriesMACDchart = [
        {
            "type": 'Line',
            "data": macd_fast,
            "options": {
                "color": 'blue',
                "lineWidth": 2
            }
        },
        {
            "type": 'Line',
            "data": macd_slow,
            "options": {
                "color": 'green',
                "lineWidth": 2
            }
        },
        {
            "type": 'Histogram',
            "data": macd_hist,
            "options": {
                "color": 'red',
                "lineWidth": 1
            }
        }
    ]

    renderLightweightCharts([
                    {
            "chart": chartMultipaneOptions[0],
            "series": seriesCandlestickChart
        },
        {
            "chart": chartMultipaneOptions[1],
            "series": seriesVolumeChart
        },
        {
            "chart": chartMultipaneOptions[2],
            "series": seriesMACDchart
        }
    ], 'multipane')

if __name__ == '__main__':

    # ticker = 'TSLA'
    # period = '1Y'

    # df, ticker = fetch_data(ticker, period)  # Unpack the returned tuple
    # # Define chartMultipaneOptions, seriesCandlestickChart, seriesVolumeChart, and seriesMACDchart here
    pass
    #display_multipane_chart()
