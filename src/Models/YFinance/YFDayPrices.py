# Imports
import pandas as pd


class YFDayPrices:
    def __init__(self, day_prices: pd.DataFrame) -> None:
        """
        YFinanceDayPrices

        This class is a wrapper over a Yahoo Finance ticker's specific day / date range price history

        Parameters:
          `day_prices` (`pd.DataFrame`): The price history of the ticker for a specific day / date range

        Methods:
          `get_price(price_type: str) -> pd.Series`: Returns the price history of the ticker as a `pd.Series` object

          `get_difference_between_prices(price_type_1: str, price_type_2: str) -> pd.Series`: Returns the difference between two price types as a `pd.Series` object

          `get_open_vs_close() -> pd.Series`: Returns the difference between the open and close prices as a `pd.Series` object

          `get_date() -> pd.Series`: Returns the date of the price history as a `pd.Series` object
        """
        self._data: pd.DataFrame = day_prices

    def get_price(self, price_type: str) -> pd.Series:
        """
        Parameters:
          `price_type` (`str`): The price type to get data for

        Returns the price history of the ticker as a `pd.Series` object

        The price types are:
        - `Open`
        - `High`
        - `Low`
        - `Close`
        - `Adj Close`
        """
        print(self._data)
        return self._data[price_type]

    def get_volume(self) -> pd.Series:
        """
        Returns the volume of the ticker as a `pd.Series` object
        """
        return self._data["Volume"]

    def get_difference_between_prices(
        self, price_type_1: str, price_type_2: str
    ) -> pd.Series:
        """
        Parameters:
          `price_type_1` (`str`): The first price type to get data for

          `price_type_2` (`str`): The second price type to get data for

        Returns the difference between two price types as a `pd.Series` object

        The price types are:
        - `Open`
        - `High`
        - `Low`
        - `Close`
        - `Adj Close`
        """
        return self.get_price(price_type_1) - self.get_price(price_type_2)

    def get_open_vs_close(self) -> pd.Series:
        """
        Returns the difference between the open and close prices as a `pd.Series` object
        """
        return self.get_difference_between_prices("Close", "Open")

    def get_date(self) -> pd.Series:
        """
        Returns the date of the price history as a `pd.Series` object
        """
        return self._data.index.to_series()

    def __str__(self) -> str:
        return self._data.to_csv()
