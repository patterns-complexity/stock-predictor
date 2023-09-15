from pandas import DataFrame, Series, Timestamp
from abc import ABC, abstractmethod
from typing import List

from src.Classes.Services.Service import Service


class FinanceData(ABC):
    def __init__(self, tickers: List[str], data_fetcher: Service) -> None:
        self._tickers = tickers
        self._data = data_fetcher.fetch_data(tickers)

    @abstractmethod
    def get_tickers(self) -> DataFrame:
        pass

    @abstractmethod
    def get_data_for_index_range(self, tickers: List[str], start_index: int, end_index: int) -> DataFrame:
        pass

    @abstractmethod
    def get_data_for_date_range(self, start_date: Timestamp, end_date: Timestamp) -> DataFrame:
        pass

    @abstractmethod
    def get_data_for_date(self, date: Timestamp) -> Series:
        pass

    @abstractmethod
    def get_min_date(self) -> Timestamp:
        pass

    @abstractmethod
    def get_max_date(self) -> Timestamp:
        pass

    @abstractmethod
    def get_random_date(self, margin_from_min: int, margin_from_max: int) -> Timestamp:
        pass

    @abstractmethod
    def get_day_close_datetime_for_date(self, date: Timestamp) -> Timestamp:
        pass
