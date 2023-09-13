from typing import List
from pandas import DataFrame, Timedelta
from datetime import datetime
from random import randint

from src.Classes.Abstract.FinanceData import FinanceData
from src.Classes.Services.Service import Service


class YahooData(FinanceData):
    def __init__(self, tickers: List[str], data_fetcher: Service) -> None:
        """
        ### Yahoo Finance data

        #### Parameters
        - `tickers` : `List[str]`
            -   List of tickers
        - `data_fetcher` : `Service`
            -   Data fetcher service
        """
        super().__init__(tickers, data_fetcher)

    def get_tickers(self) -> DataFrame:
        """
        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers

        #### Returns
        - `DataFrame`
            -   Data for the specified Yahoo Finance tickers
        """
        return self._tickers

    def get_data_for_index_range(self, start_index: int, end_index: int) -> DataFrame:
        """
        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers

        #### Parameters
        - `start_index` : `int`
            -   Data index for the beginning of the range
        - `end_index` : `int`
            -   Data index for the end of the range

        #### Returns
        - `DataFrame`
            -   Data for the specified index range
        """
        return self._data[self._tickers].iloc[start_index:end_index]

    def get_data_for_date_range(self, start_date: datetime, end_date: datetime) -> DataFrame:
        """
        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers

        #### Parameters
        - `start_date` : `datetime`
            -   Date for the beginning of the range
        - `end_date` : `datetime`
            -   Date for the end of the range

        #### Returns
        - `DataFrame`
            -   Data for the specified date range
        """
        tickers_data = self._data[self._tickers] if len(
            self._tickers) > 1 else self._data

        start_index = tickers_data.index.get_indexer(
            [start_date], method="nearest")[0]
        end_index = tickers_data.index.get_indexer(
            [end_date], method="nearest")[0]

        return tickers_data.iloc[start_index:end_index]

    def get_data_for_date(self, date: datetime) -> DataFrame:
        """
        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers for the specified date

        #### Parameters
        - `date` : `datetime`
            -   Date for the data

        #### Returns
        - `DataFrame`
            -   Data for the specified date
        """
        date_index = self._data.index.get_indexer([date], method="nearest")[0]
        return self._data[self._tickers].iloc[date_index] if len(self._tickers) > 1 else self._data.iloc[date_index]

    def get_min_date(self) -> datetime:
        """
        Returns the minimum date in the dataset

        #### Returns
        - `datetime`
            -   Minimum date in the dataset
        """
        return self._data.index.min()

    def get_max_date(self) -> datetime:
        """
        Returns the maximum date in the dataset

        #### Returns
        - `datetime`
            -   Maximum date in the dataset
        """
        return self._data.index.max()

    def get_random_date(self, margin_from_min: int, margin_from_max: int) -> datetime:
        """
        Returns a random date in the dataset

        #### Parameters
        - `margin_from_min` : `int`
            -   Margin from the minimum date
        - `margin_from_max` : `int`
            -   Margin from the maximum date
        """
        min_date: datetime = self.get_min_date() + \
            Timedelta(days=margin_from_min)
        max_date: datetime = self.get_max_date() - \
            Timedelta(days=margin_from_max)

        random_date: datetime = min_date + \
            Timedelta(days=randint(0, (max_date - min_date).days))

        return random_date
