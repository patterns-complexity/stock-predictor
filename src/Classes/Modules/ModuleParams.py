from abc import ABC, abstractmethod


class ModuleParams(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass
