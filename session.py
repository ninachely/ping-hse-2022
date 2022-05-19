from pickle import NONE
from connector import MasterConnector
from data import SessionConfig, read_master_connector_config
from processor import DataProcessor


class Session:

    def __init__(self, config: SessionConfig) -> None:
        self.connector = MasterConnector(
            read_master_connector_config(config.master_connector_config_path)
        )
        self.config = config


    def manage_connector(self, data_processor: DataProcessor) -> None:
        pass


    def run(self, data_processor: DataProcessor) -> None:
        print(5)
        for exchange in self.config.exchanges_list:
            print(exchange)
