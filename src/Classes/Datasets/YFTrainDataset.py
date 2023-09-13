from pandas import DataFrame, Timedelta
from typing import List
from datetime import datetime

from torch import dtype, tensor, Tensor, float64
from torch.utils.data import Dataset

from src.Classes.YFinance.YahooData import YahooData
from src.Classes.Services.YFService import YFService


class YFTrainDataset(Dataset):
    def __init__(self, tickers: List[str], max_size: int = 100000, future_days_delta: int = 7, history_days_count: int = 30, device: str = "cuda", dtype: dtype = float64):
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

        self._max_size = max_size
        self._device = device
        self._dtype = dtype

        self._data = YahooData(tickers, YFService())

        self._preloaded_data = []

        for _ in range(max_size):
            random_date = self._data.get_random_date(
                history_days_count, future_days_delta)
            past_range_data = self._data.get_data_for_date_range(
                random_date -
                Timedelta(days=history_days_count), random_date
            )
            future_date_data = self._data.get_data_for_date(
                random_date + Timedelta(days=future_days_delta))
            self._preloaded_data.append(
                {
                    "past": self.data_to_tensor(past_range_data),
                    "future": self.data_to_tensor(future_date_data),
                    "date": self.date_to_tensor(random_date)
                }
            )

    def __len__(self):
        return len(self._preloaded_data)

    def __getitem__(self, idx):
        data = self._preloaded_data[idx]

        return data["past"], data["future"], data["date"]

    def data_to_tensor(self, data: DataFrame) -> Tensor:
        return tensor(data.values, dtype=self._dtype)

    def date_to_tensor(self, date: datetime) -> Tensor:
        day, month, year = date.day, date.month, date.year
        return tensor([day, month, year], dtype=self._dtype)
