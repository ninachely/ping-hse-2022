from time import time
from plumbum.cmd import ping
from data import ExchangeConnectorConfig, MasterConnectorConfig, Update, UpdateType, PingResult
from utils import RestClient
from requests import get
CONNECTOR_CONFIG_FILE_PATH = 'connector_config.json'


class ExchangeConnector:

    def __init__(self, config: ExchangeConnectorConfig):
        self.config = config
        self.rest_client = RestClient()

    def ping(self) -> Update:
        ts = time()
        exit_code, raw_data, _ = (ping["-c", 1, self.config.exchange_url]).run(retcode=None)
        return Update(type=UpdateType.PING_RESULT, config=self.config, ts=ts, inner=PingResult(exit_code, raw_data), request_name=None)

    def execute_custom_request(self, name: str) -> Update:
        ts = time()
        request = next(x for x in self.config.requests if x.name == name)
        response = self.rest_client.request(
            request.base_url, get, request.endpoint, {}
        )
        return Update(type=UpdateType.REQUEST_RESPONSE, config=self.config, ts=ts, inner=response, request_name=name)


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