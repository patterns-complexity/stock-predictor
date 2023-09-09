# Imports
import pandas as pd
from datetime import datetime

# Own imports
from src.Models.YFinance.YFinanceDayPrices import YFinanceDayPrices

class YFinanceTickerPriceHistory:
  def __init__(self, history: pd.DataFrame) -> None:
    """
    YFinanceTickerPriceHistory

    This class is a wrapper over a Yahoo Finance ticker's price history

    Parameters:
      `history` (`pd.DataFrame`): The price history of the ticker

    Methods:
      `get_prrices_by_date(date: datetime) -> YFinanceDayPrices`: Returns the price history of the ticker as a `YFinanceDayPrices` object

      `get_prrices_by_date_range(start_date: datetime, end_date: datetime) -> YFinanceDayPrices`: Returns the price history of the ticker as a `YFinanceDayPrices` object
    """
    self._data = history

  def get_prices_by_date(self, date: datetime) -> YFinanceDayPrices:
    return YFinanceDayPrices(self._data[date])

  def get_prices_by_date_range(self, start_date: datetime, end_date: datetime) -> YFinanceDayPrices:
    return YFinanceDayPrices(self._data.loc[start_date:end_date])
  