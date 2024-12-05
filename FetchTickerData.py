# ----------------------------------------------------
# -- Projet : FetchTickerData
# -- Author : Ronaf - https://github.com/Ronaf-git
# -- Created : 05/12/2024
# -- Usage : Fetch Tickers data and save it into a csv file
# -- Update : 
# --  
# ----------------------------------------------------
# --- Install/Create Exe
#pip install yfinance
#pip install pandas
#pyinstaller --onefile --noconsole FetchTickerData.py

# ===============================================================
# INIT Variables
# ===============================================================

CONFIG_FILE = 'config.ini'

# ===============================================================
# Imports
# ===============================================================
import yfinance as yf #https://github.com/ranaroussi/yfinance
import pandas as pd
import os
import sys
import configparser
import ctypes

# ===============================================================
# Functions
# ===============================================================
# Function to show a Windows message box
def show_popup(title,text):
    ctypes.windll.user32.MessageBoxW(0, text, title,0x0)
    
def read_config(file_path):
        # Check if the config file exists
    if not os.path.exists(file_path):
        print(f"Error: The config file '{file_path}' does not exist.")
        return
    
    # Create a ConfigParser object with case-sensitive options
    config = configparser.ConfigParser(allow_no_value=True, delimiters=('=', ':'))
    config.optionxform = str  # Ensure option names are case-sensitive (default is lower case)
    
    config.read(file_path)
    
    # Loop through all sections and their options
    for section in config.sections():
        for key, value in config.items(section):
            # Check if the value is a comma-separated list, then convert it to a list
            if ',' in value:
                globals()[key] = value.split(',')
            else:
                globals()[key] = value


# Function to get the file path (works for both Python script and compiled executable)
def get_file_path(file_name):
    # If running from a bundled exe, the file will be in _MEIPASS directory
    if getattr(sys, 'frozen', False):
        # Running as a bundled exe
        return os.path.join(sys._MEIPASS, file_name)
    else:
        # Running as a Python script
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

# Function to fetch and process stock data for each ticker
def fetch_and_append_data(ticker,YFINANCE_DEFAULT_PERIOD,csv_file_path):
    # Fetch the stock data using yfinance
    stock_data = yf.Ticker(ticker)

    # Get the historical data for the stock (daily data)
    historical_data = stock_data.history(period=YFINANCE_DEFAULT_PERIOD).reset_index() 
    historical_data['Date'] = pd.to_datetime(historical_data['Date'], errors='coerce').dt.date
    # Add the ticker column as the first column
    historical_data.insert(0, 'Ticker', ticker)

    # Initialize an empty list to store the data
    data_to_append = []
    # Append the DataFrame to the list
    data_to_append.append(historical_data)

    # Concatenate all the price data into one DataFrame
    final_data = pd.concat(data_to_append, ignore_index=True)

    # Check if the CSV file already exists
    if os.path.exists(csv_file_path):
        # Load the existing CSV into a DataFrame
        existing_data = pd.read_csv(csv_file_path)

        existing_data['Date'] = pd.to_datetime(existing_data['Date'], errors='coerce').dt.date

        # Get the maximum date from 'existing_data' for the given ticker
        max_date = existing_data[existing_data['Ticker'] == ticker]['Date'].max()

        # If max_date is NaT, replace it with a default date (Unix epoch or another date)
        if pd.isna(max_date):
            max_date = pd.Timestamp(0).date() 

        # Filter the 'historical_data' for rows where the date is greater than max_date
        new_rows = historical_data[historical_data['Date'] > max_date]

        # Remove duplicates by checking the combination of 'Date', 'Ticker', and 'Price_Type'
        new_data = pd.concat([existing_data, new_rows], ignore_index=True)
        # Write the updated DataFrame to the CSV file
        new_data.to_csv(csv_file_path, index=False)
    else:
        # If the file doesn't exist, create it and write the data
        final_data.to_csv(csv_file_path, index=False)

# ===============================================================
# Script
# ===============================================================
# --- Variables
# - Get Config Variables
read_config(get_file_path(CONFIG_FILE))
# - adjust variables
csv_file_path = get_file_path(OUTPUT_FILE)  # Output CSV file

# Iterate through each ticker and process the data
for ticker in TICKERS:
    fetch_and_append_data(ticker,YFINANCE_DEFAULT_PERIOD,csv_file_path)

show_popup('Data updated',f"Data for your tickers has been exported to {csv_file_path}")
