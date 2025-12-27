!pip install yfinance

import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# Define the tickers for the Australian-listed ETFs
TICKERS = ['VAS.AX', 'VGS.AX', 'NDQ.AX']
CSV_FILE = 'etf_prices.csv'

def fetch_and_store_prices():
    """
    Fetches the latest adjusted close price for specified tickers 
    and appends them to a CSV file.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    data_to_append = []

    for ticker_symbol in TICKERS:
        # Fetch the most recent data point.
        # Using period='2d' ensures we catch the last trading day even on weekends/holidays
        ticker_data = yf.Ticker(ticker_symbol).history(period='2d')
        
        if not ticker_data.empty:
            # *** FIX: Changed 'Adj Close' to 'Close' ***
            latest_price = ticker_data['Close'].iloc[-1] 
            # Get the date of the latest price
            latest_date = ticker_data.index[-1].strftime('%Y-%m-%d')
            data_to_append.append({'Date': latest_date, 'Ticker': ticker_symbol, 'Price': round(latest_price, 4)})
        else:
            print(f"Could not fetch data for {ticker_symbol}")

    # Create a DataFrame for the new data
    new_data_df = pd.DataFrame(data_to_append)

    # Check if the CSV file already exists
    if os.path.exists(CSV_FILE):
        # Read existing data and append new data, ensuring no duplicates
        existing_df = pd.read_csv(CSV_FILE)
        combined_df = pd.concat([existing_df, new_data_df]).drop_duplicates(subset=['Date', 'Ticker'], keep='last')
        combined_df.to_csv(CSV_FILE, index=False)
        print(f"Appended new data to {CSV_FILE}")
    else:
        # If the file does not exist, create it with headers
        new_data_df.to_csv(CSV_FILE, index=False)
        print(f"Created new file: {CSV_FILE}")

if __name__ == "__main__":
    fetch_and_store_prices()
