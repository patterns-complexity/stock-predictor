import pandas as pd

from abc import ABC, abstractmethod
from datetime import datetime


class FinanceDataIterator(ABC):
    def __init__(self, data: pd.DataFrame, anchor_date: datetime = datetime.now()) -> None:
        super().__init__()
        self._data = data
        self._anchor_date = anchor_date

    @abstractmethod
    def fast_forward_n_days(self, n: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def rewind_n_days(self, n: int) -> pd.DataFrame:
        pass
