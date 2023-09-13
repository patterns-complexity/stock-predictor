import re
from pandas import DataFrame, Timedelta
from typing import List
from datetime import datetime

from torch import dtype, tensor, Tensor, float64
from torch.utils.data import Dataset

from src.Classes.YFinance.YahooData import YahooData
from src.Classes.Services.YFService import YFService


class YFTrainDataset(Dataset):
    def __init__(
        self,
        tickers: List[str],
        ticker_to_predict: str,
        max_size: int = 100000,
        future_days_delta: int = 7,
        history_days_count: int = 30,
        device: str = "cuda",
        dtype: dtype = float64
    ):
        """
        ### Yahoo Finance train dataset

        #### Parameters
        - `tickers` : `List[str]`
            -   List of tickers
        - `max_size` : `int`
            -   Optional
            -   Maximum size of the dataset
            -   Default: `100000`
        - `future_days_delta` : `int`
            -   Optional
            -   Number of days to predict into the future
            -   Default: `7`
        - `history_days_count` : `int`
            -   Optional
            -   Number of days to take into account when predicting the future
            -   Default: `30`
        - `device` : `str`
            -   Optional
            -   Device to use
            -   Default: `"cuda"`
        - `dtype` : `dtype`
            -   Optional
            -   Data type
            -   Default: `torch.float64`
        """
        super(YFTrainDataset, self).__init__()

        self._ticker_to_predict = ticker_to_predict

        self._max_size = max_size
        self._device = device
        self._dtype = dtype

        self.history_days_count = history_days_count
        self.future_days_delta = future_days_delta

        self._data: YahooData = YahooData(tickers, YFService())

    def __len__(self):
        return self._max_size

    def __getitem__(self, idx):
        random_date = self._data.get_random_date(
            margin_from_min=self.history_days_count,
            margin_from_max=self.future_days_delta
        )

        past_data = self._data.get_data_for_date_range(
            start_date=random_date - Timedelta(days=self.history_days_count),
            end_date=random_date
        )

        future_data = self._data.get_data_for_date(
            date=random_date + Timedelta(days=self.future_days_delta)
        )

        future_data_for_ticker = future_data[self._ticker_to_predict]

        return [
            self.data_to_tensor(past_data),
            self.data_to_tensor(future_data_for_ticker),
            self.date_to_tensor(random_date)
        ]

    def data_to_tensor(self, data: DataFrame) -> Tensor:
        return tensor(data.values, dtype=self._dtype)

    def date_to_tensor(self, date: datetime) -> Tensor:
        day, month, year = date.day, date.month, date.year
        return tensor([day, month, year], dtype=self._dtype)
