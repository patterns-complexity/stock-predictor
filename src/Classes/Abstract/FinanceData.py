import pandas as pd

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from src.Services.Service import Service


class FinanceData(ABC):
    def __init__(self, tickers: List[str], data_fetcher: Service) -> None:
        self._data = data_fetcher.fetch_data(tickers)

    @abstractmethod
    def get_tickers(self, tickers: list[str]) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_data_for_index_range(self, tickers: List[str], start_index: int, end_index: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_data_for_date_range(self, tickers: List[str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_data_for_date(self, tickers: List[str], date: datetime) -> pd.Series:
        pass

    @abstractmethod
    def fast_forward_n_days(self, anchor_date: datetime, n: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def rewind_n_days(self, anchor_date: datetime, n: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_min_date(self) -> datetime:
        pass

    @abstractmethod
    def get_max_date(self) -> datetime:
        pass
