# Imports
import pandas as pd


# Own imports
from src.Models.YFinance.YFTicker import YFTicker


class YFData:
    def __init__(self, data: pd.DataFrame) -> None:
        """
        YFinanceData

        This class is a wrapper for Yahoo Finance's (yfinance) API.

        Parameters:
        - `data` (`pd.DataFrame`): The data returned by Yahoo Finance's
        (`yfinance`) API

        Methods:
        - `get_ticker(ticker: str) -> YFinanceTicker`: Returns all data for
        the specified Yahoo Finance ticker as a `YFinanceTicker` object.
        - `get_tickers(tickers: list[str]) -> list[YFinanceTicker]`: Returns a
        list of Yahoo Finance ticker objects.

        The data parameter is a pandas DataFrame
        """
        self._data = data

    def get_ticker(self, ticker: str) -> YFTicker:
        """
        Parameters:
          `ticker` (`str`): The ticker to get data for

        Retruns all data for the specified Yahoo Finance ticker as a
        `YFinanceTicker` object.
        """
        return YFTicker(name=ticker, price_history=self._data[ticker])

    def get_tickers(self, tickers: list[str]) -> list[YFTicker]:
        """
        tickers: list[str]

        Returns a list of Yahoo Finance ticker objects.
        """
        return [self.get_ticker(ticker) for ticker in tickers]
