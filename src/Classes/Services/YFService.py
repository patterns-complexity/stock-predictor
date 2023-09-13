# YFinanceService

# Imports
from pandas import DataFrame, date_range
from yfinance import download
from os import getenv

# Own imports
from src.Classes.Services.Service import Service


class YFService(Service):
    def __init__(self) -> None:
        super().__init__()

    def fetch_data(self, tickers: list[str]) -> DataFrame:
        """
        ### Fetch data from Yahoo Finance

        #### Parameters
        - `tickers` : `list[str]`
            -   List of tickers
        """
        ticker = ", ".join(tickers)
        data: DataFrame = download(
            tickers=ticker,
            period=getenv('DATA_PERIOD'),
            interval=getenv('DATA_INTERVAL'),
            group_by="ticker",
            auto_adjust=True,
            prepost=True,
            threads=getenv('MAX_THREADS'),
            proxy=None
        )

        data.to_csv('./cache/raw.csv')

        # Drop rows with "NaN" values
        data = data.dropna(axis=0, how="any")

        # Interpolate missing rows so that dates are continuous
        data = data.reindex(
            date_range(start=data.index[0], end=data.index[-1], freq="1D")
        )

        # Fill missing values with interpolation
        data = data.interpolate(method="linear")

        # Group by ticker
        data.groupby(axis=1, level=0)

        data.to_csv('./cache/processed.csv')

        return data
