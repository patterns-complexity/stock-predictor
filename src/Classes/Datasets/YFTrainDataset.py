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
        future_offset_point: int = 1,
        history_time_range: int = 7,
        price_type: str = "Close",
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
        - `future_offset_point` : `int`
            -   Optional
            -   Number of time units to predict into the future
            -   Default: `1`
        - `history_time_range` : `int`
            -   Optional
            -   Number of time units to take into account when predicting the future
            -   Default: `7`
        - `dtype` : `dtype`
            -   Optional
            -   Data type
            -   Default: `torch.float64`
        """
        super(YFTrainDataset, self).__init__()

        self._ticker_to_predict = ticker_to_predict
        self._price_type = price_type

        self._max_size = max_size
        self._dtype = dtype

        self._history_time_range = history_time_range
        self._future_offset_point = future_offset_point

        self._data: YahooData = YahooData(tickers, YFService())

    def __len__(self):
        return self._max_size

    def __getitem__(self, idx):
        random_date = self._data.get_random_date(
            margin_from_min=self._history_time_range,
            margin_from_max=self._future_offset_point
        )

        date_before_random_date = (
            random_date -
            Timedelta(value=1, unit=self._data._interval_key)
        )

        past_date = (
            random_date -
            Timedelta(value=self._history_time_range,
                      unit=self._data._interval_key)
        )

        past_date_data = self._data.get_data_for_date_range(
            start_date=past_date,
            end_date=date_before_random_date
        )

        future_date = (
            random_date +
            Timedelta(value=self._future_offset_point,
                      unit=self._data._interval_key)
        )

        future_date_data = self._data.get_data_for_date(
            date=future_date
        )

        future_data_for_ticker = future_date_data[self._ticker_to_predict][self._price_type]

        return [
            self.data_to_tensor(past_date_data),
            self.data_to_tensor(future_data_for_ticker),
            self.date_to_tensor(random_date)
        ]

    def data_to_tensor(self, data: DataFrame | float) -> Tensor:
        if isinstance(data, DataFrame):
            return tensor(data.values, dtype=self._dtype)
        else:
            return tensor(data, dtype=self._dtype)

    def date_to_tensor(self, date: datetime) -> Tensor:
        day, month, year = date.day, date.month, date.year
        return tensor([day, month, year], dtype=self._dtype)
