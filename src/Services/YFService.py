# YFinanceService

# Imports
import yfinance as yf
from os import getenv

# Own imports
from src.Models.YFinance.YFData import YFData


class YFService:
    def __init__(self) -> None:
        """
        YFinanceService

        This class is a wrapper for Yahoo Finance's (yfinance) API.

        The `DATA_PERIOD` and `DATA_INTERVAL` environment variables are used to determine the period and interval to get data for.

        Methods:
          `get_stock_data(tickers: list[str], interval: str | None = None) -> YFinanceData`: Downloads data for the specified tickers and returns a `YFinanceData` object.
        """
        pass

    def get_stock_data(
        self,
        tickers: list[str],
        interval: str | None = None
    ) -> YFData:
        """
        Parameters:
          `tickers` (`list[str]`): A list of tickers to download data for

          `interval` (`str`): The interval to get data from. Defaults to the value of the `DATA_INTERVAL` environment variable.

        Downloads data for the specified tickers and returns a `YFinanceData` object.
        """
        ticker = ",".join(tickers)
        data = yf.download(
            tickers=ticker,
            period=getenv('DATA_PERIOD'),
            interval=getenv('DATA_INTERVAL') or interval,
            group_by="ticker",
            auto_adjust=True,
            prepost=True,
            threads=getenv('MAX_THREADS'),
            proxy=None
        )

        return YFData(data)
