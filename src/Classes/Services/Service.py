from pandas import DataFrame
from abc import ABC, abstractmethod


class Service(ABC):
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    @abstractmethod
    def fetch_data(self, tickers: list[str]) -> DataFrame:
        pass
