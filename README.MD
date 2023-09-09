# Stock Predictor

## Description

This project is designed to fetch and manipulate stock data from Yahoo Finance. It uses a modular approach and consists of various wrapper classes around the raw data to make it more user-friendly and manageable.

## Installation

1. Clone this repository:
   ```
   git clone <repository_url>
   ```
2. Navigate to the project folder:
   ```
   cd stock-predictor
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Dependencies

- `yfinance`: For fetching stock data from Yahoo Finance.
- `pandas`: For data manipulation and storage.
- `environs`: For environment variable parsing.

## Usage

The main entry point of the application is `app.py`. Run it as follows:

```bash
python app.py
```

### Environment Variables

Make sure to set the following environment variables or place them in a `.env` file:

- `DATA_PERIOD`: The period for which to fetch the stock data.
- `DATA_INTERVAL`: The interval between stock data points.
- `MAX_THREADS`: The maximum number of threads for fetching data.

## Classes and Methods

### YFService

- `get_stock_data(tickers: list[str], interval: str | None = None) -> YFData`: Downloads data for the specified tickers and returns a `YFData` object.

### YFData

- `get_ticker(ticker: str) -> YFTicker`: Returns all data for the specified Yahoo Finance ticker as a `YFTicker` object.
- `get_tickers(tickers: list[str]) -> list[YFTicker]`: Returns a list of Yahoo Finance ticker objects.

### YFTicker

- `get_name() -> str`: Returns the name of the ticker.
- `get_price_history() -> YFTickerPriceHistory`: Returns the price history of the ticker as a `YFTickerPriceHistory` object.

### YFTickerPriceHistory

- `get_prices_by_date(date: datetime) -> YFDayPrices`: Returns the price history of the ticker as a `YFDayPrices` object for a specific date.
- `get_prices_by_date_range(start_date: datetime, end_date: datetime) -> YFDayPrices`: Returns the price history of the ticker as a `YFDayPrices` object for a specific date range.

## Contributing

Feel free to submit pull requests or open issues to improve the project.

## License

MIT License