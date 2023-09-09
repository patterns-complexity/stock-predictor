# Bootstrap

# %% Imports
from environs import Env
from datetime import datetime
from src.Classes.YFinance.YahooDataIterator import YahooDataIterator
from src.Classes.YFinance.YahooDataSlice import YahooDataSlice

# %% Own imports
from src.Services.YFService import YFService

# %% Parse environment variables
env = Env()
env.read_env()

# %% Create YFinanceService instance
yf_finance_service = YFService()

# %% Determine range of dates
# timezone utc
date_start = datetime(2021, 1, 1)
date_end = datetime(2022, 12, 31)
single_date = datetime(2021, 6, 1)
price_type = "Open"

# %% Get stock data
stock = yf_finance_service.fetch_data(
    tickers=["AAPL", "MSFT", "GOOG", "AMZN"]
)

# %% Create instances
yf_data_slice = YahooDataSlice(stock)
yf_data_iterator = YahooDataIterator(yf_data_slice.get_data_for_date_range(
    tickers=["AAPL", "MSFT"],
    start_date=date_start,
    end_date=date_end
), single_date)

# %% Get stock data for date range
date_range = yf_data_slice.get_data_for_date_range(
    tickers=["AAPL", "MSFT"],
    start_date=date_start,
    end_date=date_end
)

# %% Get stock data for single date
date = yf_data_slice.get_data_for_date(
    tickers=["AAPL", "MSFT"],
    date=single_date
)

# %%
five_days_future = yf_data_iterator.fast_forward_n_days(5)
five_days_past = yf_data_iterator.rewind_n_days(15)

# %% Print results
date_range

# %% Print results
date

# %% Print results
five_days_future

# %% Print results
five_days_past

# %%
