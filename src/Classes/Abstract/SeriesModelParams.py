from abc import ABC, abstractmethod


class SeriesModelParams(ABC):
    @abstractmethod
    def get_input_size(self) -> int:
        pass

    @abstractmethod
    def get_output_size(self) -> int:
        pass

    @abstractmethod
    def get_hidden_dim(self) -> int:
        pass

    @abstractmethod
    def get_series_length(self) -> int:
        pass

    @abstractmethod
    def get_series_count(self) -> int:
        pass

    @abstractmethod
    def get_batch_size(self) -> int:
        pass
