# Bootstrap

# %% Imports
from environs import Env
from datetime import datetime

from src.Classes.Datasets.YFTrainDataset import YFTrainDataset

# %% Parse environment variables
env = Env()
env.read_env()

# %% Determine range of dates
# timezone utc
date_start = datetime(2021, 1, 1)
date_end = datetime(2022, 12, 31)
single_date = datetime(2021, 6, 1)
price_type = "Open"

# %% Get data
yf_train_dataset = YFTrainDataset(
    tickers=["AAPL"],
    max_size=1000,
    future_days_range=7,
    past_days_range=30
)

# %% Get data for a single date to look up if the data is correct
for data in yf_train_dataset:
    x, y, z = data

    print('past', type(x))
    print('future', type(y))
    print('date', type(z))

    break

# %% Get data for a range of dates
