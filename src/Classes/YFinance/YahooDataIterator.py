import pandas as pd
from datetime import datetime

from src.Classes.Abstract.FinanceDataIterator import FinanceDataIterator


class YahooDataIterator(FinanceDataIterator):
    def __init__(self, data: pd.DataFrame, anchor_date: datetime = datetime.now()) -> None:
        super().__init__(data, anchor_date)

    def fast_forward_n_days(self, n: int) -> pd.DataFrame:
        """
        Parameters:
          `n` (`int`): The number of days to fast forward

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        date_to_seek = self._anchor_date + pd.Timedelta(days=n)
        index_to_seek = self._data.index.get_indexer(
            [date_to_seek], method="nearest")
        return self._data.iloc[index_to_seek]

    def rewind_n_days(self, n: int) -> pd.DataFrame:
        """
        Parameters:
          `n` (`int`): The number of days to rewind

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        date_to_seek = self._anchor_date - pd.Timedelta(days=n)
        index_to_seek = self._data.index.get_indexer(
            [date_to_seek], method="nearest")
        return self._data.iloc[index_to_seek]
