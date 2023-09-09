import pandas as pd

from datetime import datetime

from src.Classes.Abstract.FinanceDataSlice import FinanceDataSlice


class YahooDataSlice(FinanceDataSlice):
    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data)
        # interpolate nan values
        self._data.interpolate(inplace=True)

    def get_tickers(self, tickers: list[str]) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        return self._data[tickers]

    def get_data_for_date_range(self, tickers: list[str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for
          `start_date` (`datetime`): The start date
          `end_date` (`datetime`): The end date

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        return self._data[tickers].loc[start_date:end_date]

    def get_data_for_date(self, tickers: list[str], date: datetime) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for
          `date` (`datetime`): The date

        Returns a pandas Series of the data for the specified Yahoo Finance tickers
        """
        return self._data[tickers].loc[date:date]
