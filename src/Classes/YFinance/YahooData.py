from os import getenv
from typing import List
from pandas import DataFrame, Timedelta, Timestamp
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

        # Convert all timezones to tz_naive
        self._data = self._data.tz_convert('UTC').tz_localize(None)

        self._data_interval = getenv('DATA_INTERVAL')

        # TODO: Fix this idiotic conditional
        self._interval_key = "days" if self._data_interval == "1d" else "hours"

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

    def get_data_for_date_range(self, start_date: Timestamp, end_date: Timestamp) -> DataFrame:
        """
        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers

        #### Parameters
        - `start_date` : `pd.Timestamp`
            -   Date for the beginning of the range
        - `end_date` : `pd.Timestamp`
            -   Date for the end of the range

        #### Returns
        - `DataFrame`
            -   Data for the specified date range
        """

        tickers_data = self._data[self._tickers] if len(
            self._tickers) > 1 else self._data

        return tickers_data.loc[start_date:end_date]

    def get_data_for_date(self, date: Timestamp) -> DataFrame:
        """
        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers for the specified date

        #### Parameters
        - `date` : `pd.Timestamp`
            -   Date for the data

        #### Returns
        - `DataFrame`
            -   Data for the specified date
        """

        date_index = self._data.index.get_indexer([date], method="nearest")[0]
        return self._data[self._tickers].iloc[date_index] if len(self._tickers) > 1 else self._data.iloc[date_index]

    def get_min_date(self) -> Timestamp:
        """
        Returns the minimum date in the dataset

        #### Returns
        - `pd.Timestamp`
            -   Minimum date in the dataset
        """
        return self._data.index.min()

    def get_max_date(self) -> Timestamp:
        """
        Returns the maximum date in the dataset

        #### Returns
        - `pd.Timestamp`
            -   Maximum date in the dataset
        """
        return self._data.index.max()

    def get_random_date(self, margin_from_min: int, margin_from_max: int) -> Timestamp:
        """
        Returns a random date in the dataset

        #### Parameters
        - `margin_from_min` : `int`
            -   Margin from the minimum date
        - `margin_from_max` : `int`
            -   Margin from the maximum date

        #### Returns
        - `pd.Timestamp`
            -   Random date in the dataset
        """
        min_date: Timestamp = self.get_min_date()
        max_date: Timestamp = self.get_max_date()

        min_date_fast_forwarded: Timestamp = min_date + \
            Timedelta(value=margin_from_min, unit=self._interval_key)
        max_date_rewound: Timestamp = max_date - \
            Timedelta(value=margin_from_max, unit=self._interval_key)

        min_index: int = self._data.index.get_indexer(
            [min_date_fast_forwarded], method="nearest"
        )[0]

        max_index: int = self._data.index.get_indexer(
            [max_date_rewound], method="nearest"
        )[0]

        random_date: Timestamp = self._data.index[randint(
            min_index, max_index)]

        return random_date

    def get_day_close_datetime_for_date(self, date: Timestamp) -> Timestamp:
        """
        Returns the timestamp of the day close for the specified date

        #### Parameters
        - `date` : `datetime`
            -   Date for the data

        #### Returns
        - `pd.Timestamp`
            -   Timestamp of the day close for the specified date
        """
        return Timestamp(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=16,
            minute=0,
            second=0
        )

    def timestamp_to_utc(self, timestamp: Timestamp) -> Timestamp:
        """
        Converts a timestamp to UTC

        #### Parameters
        - `timestamp` : `pd.Timestamp`
            -   Timestamp to convert

        #### Returns
        - `pd.Timestamp`
            -   Timestamp converted to UTC
        """
        return timestamp.tz_convert('UTC').tz_localize(None)
