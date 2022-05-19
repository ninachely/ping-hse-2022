from plumbum import FG
from plumbum.cmd import ping
from data import ExchangeConnectorConfig, MasterConnectorConfig
from utils import PingResult
CONNECTOR_CONFIG_FILE_PATH = 'connector_config.json'


class ExchangeConnector:

    def __init__(self, config: ExchangeConnectorConfig):
        self.config = config


    def ping(self):
        exit_code, raw_data, _ = (ping["-c", 1, self.config.exchange_url]).run(retcode=None)
        return PingResult(exit_code, raw_data)


    def execute_custom_request(self, request_type: int):
        pass


class MasterConnector:

    def __init__(self, config: MasterConnectorConfig) -> None:
        self.exchange_connectors = {
            exchange_connector_config.exchange_name: ExchangeConnector(config=exchange_connector_config)
            for exchange_connector_config
            in config.exchange_connector_configs
        }

    def ping(self, exchange_name: str) -> PingResult:
        if exchange_name not in self.exchange_connectors:
            raise ValueError(f"not found exchange with name = {exchange_name}")
        return self.exchange_connectors.get(exchange_name).ping()