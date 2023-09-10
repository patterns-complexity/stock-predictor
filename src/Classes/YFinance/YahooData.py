from typing import List
import pandas as pd

from datetime import datetime

from src.Classes.Abstract.FinanceData import FinanceData
from src.Services.Service import Service


class YahooData(FinanceData):
    def __init__(self, tickers: List[str], data_fetcher: Service) -> None:
        super().__init__(tickers, data_fetcher)

    def get_tickers(self, tickers: list[str]) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        return self._data[tickers]

    def get_data_for_index_range(self, tickers: list[str], start_index: int, end_index: int) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for
          `start_index` (`int`): The start index
          `end_index` (`int`): The end index

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        return self._data[tickers].iloc[start_index:end_index]

    def get_data_for_date_range(self, tickers: list[str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for
          `start_date` (`datetime`): The start date
          `end_date` (`datetime`): The end date

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        tickers_data = self._data[tickers] if len(tickers) > 1 else self._data
        start_index = tickers_data.index.get_indexer(
            [start_date], method="nearest")[0]
        end_index = tickers_data.index.get_indexer(
            [end_date], method="nearest")[0]
        return tickers_data.iloc[start_index:end_index]

    def get_data_for_date(self, tickers: list[str], date: datetime) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for
          `date` (`datetime`): The date

        Returns a pandas Series of the data for the specified Yahoo Finance tickers
        """
        date_index = self._data.index.get_indexer([date], method="nearest")[0]
        return self._data[tickers].iloc[date_index] if len(tickers) > 1 else self._data.iloc[date_index]

    def fast_forward_n_days(self, anchor_date: datetime, n: int) -> pd.DataFrame:
        """
        Parameters:
          `n` (`int`): The number of days to fast forward

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        date_to_seek = anchor_date + pd.Timedelta(days=n)
        index_to_seek = self._data.index.get_indexer(
            [date_to_seek], method="nearest")
        return self._data.iloc[index_to_seek]

    def rewind_n_days(self, anchor_date: datetime, n: int) -> pd.DataFrame:
        """
        Parameters:
          `n` (`int`): The number of days to rewind

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        return self.fast_forward_n_days(anchor_date, -n)

    def get_min_date(self) -> datetime:
        """
        Returns the minimum date in the dataset
        """
        return self._data.index.min()

    def get_max_date(self) -> datetime:
        """
        Returns the maximum date in the dataset
        """
        return self._data.index.max()
