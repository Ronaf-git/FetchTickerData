# FetchTickerData

This tool allows you to retrieve historical stock data for specific tickers using the [yfinance](https://github.com/ranaroussi/yfinance) library, then export the data to a CSV file. The data is appended with new values when run again.

## Requirements
- Access to the internet (for API requests).

## How to Use

### Step 1: Extract the Archive
1. Extract the downloaded archive into a dedicated folder.

### Step 2: Customize Your Config Files
Inside the extracted folder, you'll find a configuration file where you can customize the following options:

- **OUTPUT_FILE**: The name of the output CSV file. This file will be saved in the same directory as the script.

- **YFINANCE_DEFAULT_PERIOD**: Choose the time range for the data. Available options are:
  - `"1d"`: Data for the last 1 day (intraday data, if available).
  - `"5d"`: Data for the last 5 days.
  - `"1mo"`: Data for the last 1 month.
  - `"3mo"`: Data for the last 3 months.
  - `"6mo"`: Data for the last 6 months.
  - `"1y"`: Data for the last 1 year.
  - `"2y"`: Data for the last 2 years.
  - `"5y"`: Data for the last 5 years.
  - `"10y"`: Data for the last 10 years.
  - `"ytd"`: Data from the start of the current year to the present date.
  - `"max"`: Data for the maximum available time (which can go back as far as the stock data is available for the ticker).

Additionally, you will find a text file containing the list of tickers to be tracked. Ensure that these tickers are present on Yahoo Finance.

### 3. Run the Executable
Once your configuration is set, simply run the script. It will retrieve the historical data for the tickers and append the new data to the specified CSV file. If the file doesn't exist, it will be created automatically.

---

### CSV File Format
The output CSV file will have the following columns:

- **Ticker**: The stock ticker symbol.
- **Ticker FullName**: The stock ticker's full name.
- **Date**: The date of the stock data.
- **Open**: The opening price of the stock for the given day or period. This is the price at which the stock first trades when the market opens or at the beginning of the specified period.
- **High**: The highest price the stock reached during the given day or period. This represents the peak value of the stock's trading price for that time frame.
- **Low**: The lowest price the stock reached during the given day or period. This is the bottom value the stock traded at during the session or period.
- **Close**: The closing price is the last price at which the stock traded before the market closed or the period ended. It is often considered the most important price of the day for investors and analysts.
- **Volume**: The total number of shares of the stock that were traded during the given day or period. It reflects the level of activity and liquidity in the stock.
- **Dividends**: The amount of money paid to shareholders per share for the given day or period.
- **Stock Splits**: Indicates the number of stock splits that occurred during the given period.

The data is appended to the CSV file, so only new values will be added when the script is rerun.

---

## Example Configuration

### Python Configuration
```python
OUTPUT_FILE = "stock_data.csv"  # Name of the output CSV file
YFINANCE_DEFAULT_PERIOD = "1y"  # Time range for the data (e.g., "1mo", "1y", etc.)
```

### Tickers List
```
AAPL
MSFT
TSLA
