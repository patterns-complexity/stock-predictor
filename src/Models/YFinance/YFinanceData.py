# Imports
import pandas as pd

# Own imports
from src.Models.YFinance.YFinanceTicker import YFinanceTicker

class YFinanceData:
  def __init__(self, data: pd.DataFrame) -> None:
    """
    YFinanceData

    This class is a wrapper for Yahoo Finance's (yfinance) API.

    Parameters:
    - `data` (`pd.DataFrame`): The data returned by Yahoo Finance's (`yfinance`) API

    Methods:
    - `get_ticker(ticker: str) -> YFinanceTicker`: Returns all data for the specified Yahoo Finance ticker as a `YFinanceTicker` object.
    - `get_tickers(tickers: list[str]) -> list[YFinanceTicker]`: Returns a list of Yahoo Finance ticker objects.

    The data parameter is a pandas DataFrame with the following structure:

    | Date       | Open       | High       | Low        | Close      | Adj Close  | Volume     |
    | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
    | 2020-01-01 | 1        | 1          | 1          | 1          | 1          | 1          |
    | 2020-01-02 | 2      | 2          | 2          | 2          | 2          | 2          |
    """
    self._data = data

  def get_ticker(self, ticker: str) -> YFinanceTicker:
    """
    Parameters:
      `ticker` (`str`): The ticker to get data for

    Retruns all data for the specified Yahoo Finance ticker as a `YFinanceTicker` object.
    """
    return YFinanceTicker(
      name=ticker,
      price_history=self._data[ticker]
    )

  def get_tickers(self, tickers: list[str]) -> list[YFinanceTicker]:
    """
    tickers: list[str]

    Returns a list of Yahoo Finance ticker objects.
    """
    return [self.get_ticker(ticker) for ticker in tickers]

