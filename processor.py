from abc import abstractmethod
from data import MainConfig
from utils import import_data_processor


class DataProcessor:

    @abstractmethod
    def on_update(): ...

    @abstractmethod
    def on_terminate(): ...


class MasterDataProcessor:

    def __init__(self, config: MainConfig) -> None:
        self.processors = [
            import_data_processor() for name in config.outputs
        ]
