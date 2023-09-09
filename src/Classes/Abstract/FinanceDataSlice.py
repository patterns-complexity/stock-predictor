import pandas as pd

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class FinanceDataSlice(ABC):
    def __init__(self, data: pd.DataFrame) -> None:
        self._data = data

    @abstractmethod
    def get_tickers(self, tickers: list[str]) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_data_for_date_range(self, tickers: List[str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_data_for_date(self, tickers: List[str], date: datetime) -> pd.Series:
        pass
