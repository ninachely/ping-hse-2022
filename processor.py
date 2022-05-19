from abc import abstractmethod
from concurrent.futures import process
import importlib
from typing import List
from data import SessionConfig, Update

class DataProcessor:

    @abstractmethod
    def on_update(self, update: Update): ...

    @abstractmethod
    def on_terminate(self): ...


def import_data_processor(name: str) -> DataProcessor:
    module = importlib.import_module(name)
    class_ = getattr(module, 'Module')
    assert(issubclass(class_, DataProcessor))
    return class_()


class MasterDataProcessor(DataProcessor):

    processors: List[DataProcessor]

    def __init__(self, config: SessionConfig) -> None:
        self.processors = [
            import_data_processor(name) for name in config.data_processors
        ]


    def on_update(self, update: Update):
        for processor in self.processors:
            processor.on_update(update)


    def on_terminate(self):
        pass
