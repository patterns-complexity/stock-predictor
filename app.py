# Bootstrap

# %% Imports
from environs import Env
from datetime import datetime

# %% Own imports
from src.Services.YFService import YFService

# %% Parse environment variables
env = Env()
env.read_env()

# %% Create YFinanceService instance
yfinance_service = YFService()

# %% Determine range of dates
# timezone utc
date_start = datetime(2021, 1, 1)
date_end = datetime(2021, 1, 31)
single_date = datetime(2021, 1, 4)
price_type = "Open"

# %% Get stock data
stock = yfinance_service.get_stock_data(
    tickers=["AAPL", "MSFT", "GOOG", "AMZN", "FB", "TSLA"]
)

# %% Get data for a single ticker
single_ticker = stock.get_ticker("AAPL")

# %% Get that ticker's price history
single_ticker_price_history = single_ticker.get_price_history()

# %% Get stock data for that ticker in a date range
prices_in_date_range = single_ticker_price_history.get_prices_by_date_range(
    start_date=date_start, end_date=date_end
).get_price(price_type)

print(prices_in_date_range,
      f"Prices in date range ({date_start} - {date_end})")

# %% Get stock data for that ticker on a specific date
prices_on_date = single_ticker_price_history.get_prices_by_date(
    date=single_date
).get_price(price_type)

print(prices_on_date, f"Prices on date ({single_date})")

# %%
