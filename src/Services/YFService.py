# YFinanceService

# Imports
import yfinance as yf
import pandas as pd

from os import getenv

# Own imports
from src.Services.Service import Service


class YFService(Service):
    def __init__(self) -> None:
        super().__init__()

    def fetch_data(self, tickers: list[str]) -> pd.DataFrame:
        """
        Parameters:
          `tickers` (`list[str]`): The tickers to get data for

        Returns a pandas DataFrame of the data for the specified Yahoo Finance tickers
        """
        ticker = ", ".join(tickers)
        data = yf.download(
            tickers=ticker,
            period=getenv('DATA_PERIOD'),
            interval=getenv('DATA_INTERVAL'),
            group_by="ticker",
            auto_adjust=True,
            prepost=True,
            threads=getenv('MAX_THREADS'),
            proxy=None
        )

        return data
