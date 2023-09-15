from pandas import DataFrame, date_range
from yfinance import download
from os import getenv

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
            start=getenv('FETCH_START_DATE'),
            end=getenv('FETCH_END_DATE'),
            interval=getenv('DATA_INTERVAL'),
            group_by="ticker",
            auto_adjust=True,
            prepost=True,
            threads=int(getenv('MAX_THREADS')),
            proxy=None
        )

        # Remove NaN values
        data = data.dropna(axis=0, how="any")

        # Reindex data
        data = data.reindex(date_range(
            start=data.index[0],
            end=data.index[-1],
            freq=getenv('DATA_INTERVAL')
        ))

        # Interpolate data
        data = data.interpolate(method='linear', axis=0)

        # Group by ticker
        data.groupby(axis=1, level=0)

        # TODO: Start actually using cache lmao
        data.to_csv('./cache/processed.csv')

        return data
