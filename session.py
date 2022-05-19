from time import sleep, time
from connector import MasterConnector
from data import MS_TO_SEC, SessionConfig, read_master_connector_config
from processor import MasterDataProcessor


class Session:

    def __init__(self, config: SessionConfig, data_processor: MasterDataProcessor) -> None:
        self.connector = MasterConnector(
            read_master_connector_config(config.master_connector_config_path)
        )
        self.config = config
        self.master_data_processor = data_processor

    def run(self) -> None:
        connectors = [
            self.connector.get_exchange_connector(exchange_name)
            for exchange_name in self.config.exchanges_list
        ]
        start_time = time()
        while time() - start_time < self.config.duration:
            for connector in connectors:
                updates = []
                updates.append(connector.ping())
                for request in self.config.additional_requests:
                    updates.append(connector.execute_custom_request(request))
                for update in updates:
                    self.master_data_processor.on_update(update)
            sleep(self.config.interval_ms * MS_TO_SEC)
