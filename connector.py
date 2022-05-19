from email.mime import base
from time import time
from plumbum import FG
from plumbum.cmd import ping
from data import ExchangeConnectorConfig, MasterConnectorConfig, Update, UpdateType, PingResult
from utils import RestClient
CONNECTOR_CONFIG_FILE_PATH = 'connector_config.json'


class ExchangeConnector:

    def __init__(self, config: ExchangeConnectorConfig):
        self.config = config
        self.rest_client = RestClient()

    def ping(self) -> Update:
        ts = time()
        exit_code, raw_data, _ = (ping["-c", 1, self.config.exchange_url]).run(retcode=None)
        return Update(type=UpdateType.PING_RESULT, inner=PingResult(self.config, ts, exit_code, raw_data))


    def execute_custom_request(self, request_type: str):
        pass


class MasterConnector:

    def __init__(self, config: MasterConnectorConfig) -> None:
        self.exchange_connectors = {
            exchange_connector_config.exchange_name: ExchangeConnector(config=exchange_connector_config)
            for exchange_connector_config
            in config.exchange_connector_configs
        }


    def get_exchange_connector(self, exchange_name: str) -> ExchangeConnector:
        if exchange_name not in self.exchange_connectors:
            raise ValueError(f"not found exchange with name = {exchange_name}")
        return self.exchange_connectors.get(exchange_name)