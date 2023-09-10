import pandas as pd

from typing import List
from torch.utils.data import TensorDataset
from random import randint

from src.Classes.YFinance.YahooData import YahooData
from src.Services.YFService import YFService


class YFTrainDataset(TensorDataset):
    def __init__(self, tickers: List[str], max_size: int = 100000, future_days_range: int = 7, past_days_range: int = 30):
        super(YFTrainDataset, self).__init__()

        self._max_size = max_size

        self._data = YahooData(tickers, YFService())

        self.min_date_possible = self._data.get_min_date()
        self.max_date_possible = self._data.get_max_date()

        self.past_days_range = past_days_range
        self.future_days_range = future_days_range

        self.possible_range: int = (self.max_date_possible -
                                    self.min_date_possible).days

        self.preloaded_data = []

        for _ in range(self._max_size):
            random_date = self.min_date_possible + \
                pd.Timedelta(days=randint(0, self.possible_range))

            past_date = random_date - \
                pd.Timedelta(days=self.past_days_range)
            future_date = random_date + \
                pd.Timedelta(days=self.future_days_range)

            past_range_data = self._data.get_data_for_date_range(
                tickers, past_date, random_date
            )
            future_date_data = self._data.get_data_for_date(
                tickers, future_date
            )

            self.preloaded_data.append(
                {
                    "date": random_date,
                    "past": past_range_data,
                    "future": future_date_data
                }
            )

    def __len__(self):
        return len(self.preloaded_data)

    def __getitem__(self, idx):
        data = self.preloaded_data[idx]

        return [
            data["past"],
            data["future"],
            data["date"]
        ]
