from abc import abstractmethod
import importlib
from data import SessionConfig

class DataProcessor:

    @abstractmethod
    def on_update(): ...

    @abstractmethod
    def on_terminate(): ...


def import_data_processor(name: str) -> DataProcessor:
    module = importlib.import_module(name)
    class_ = getattr(module, 'Module')
    assert(issubclass(class_, DataProcessor))
    return class_()


class MasterDataProcessor(DataProcessor):

    def __init__(self, config: SessionConfig) -> None:
        self.processors = [
            import_data_processor(name) for name in config.data_processors
        ]


    def on_update(self):
        pass


    def on_terminate(self):
        pass
