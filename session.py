from pickle import NONE
from threading import Thread
from time import sleep, time
from connector import MasterConnector
from data import MS_TO_SEC, SessionConfig, read_master_connector_config
from processor import DataProcessor


class Session:

    def __init__(self, config: SessionConfig, data_processor: DataProcessor) -> None:
        self.connector = MasterConnector(
            read_master_connector_config(config.master_connector_config_path)
        )
        self.config = config
        self.data_processor = data_processor


    def exchange_manager(self, exchange_name: str) -> None:
        connector = self.connector.get_exchange_connector(exchange_name)
        start_time = time()
        while time() - start_time < self.config.duration:

            sleep(self.config.interval_ms * MS_TO_SEC)


    def run(self, data_processor: DataProcessor) -> None:
        threads = []
        for exchange in self.config.exchanges_list:
            threads.append(Thread(self.exchange_manager))
