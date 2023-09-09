# Imports
import pandas as pd


# Own imports
from src.Models.YFinance.YFTickerPriceHistory import (
    YFTickerPriceHistory
)


class YFTicker:
    def __init__(self, name: str, price_history: pd.DataFrame) -> None:
        """
        YFTicker

        This class is a wrapper over a Yahoo Finance's ticker data

        Parameters:
          `name` (`str`): The name of the ticker

          `price_history` (`pd.DataFrame`): The price history of the ticker

        Methods:
          `get_name() -> str`: Returns the name of the ticker

          `get_price_history() -> YFTickerPriceHistory`: Returns the price history of the ticker as a `YFTickerPriceHistory` object
        """
        self._name = name
        self._data = price_history

    def get_name(self) -> str:
        """
        Returns the name of the ticker
        """
        return self._name

    def get_price_history(self) -> YFTickerPriceHistory:
        """
        Returns the price history of the ticker as a
          `YFTickerPriceHistory` object
        """
        return YFTickerPriceHistory(self._data)
