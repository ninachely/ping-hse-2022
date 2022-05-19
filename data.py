from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional
import logging as log
import json
from dacite import from_dict
MS_TO_SEC = 1000


@dataclass
class RestClientConfig:
    skey: str
    pkey: str
    

@dataclass
class CommandConfig:
    name: str
    base_url: str
    endpoint: str


@dataclass
class ExchangeConnectorConfig:
    exchange_name: str
    exchange_url: str
    rest_client_config: Optional[RestClientConfig]
    requests: List[CommandConfig]


@dataclass
class MasterConnectorConfig:
    exchange_connector_configs: List[ExchangeConnectorConfig]


@dataclass
class SessionConfig:
    master_connector_config_path: str
    exchanges_list: List[str]
    additional_requests: List[str]
    duration: int
    interval_ms: int
    run_name_format: str
    data_processors: List[str]     


def read_master_connector_config(filename: Path) -> MasterConnectorConfig:
    log.info(f"Reading master connector config from file {filename}")
    connector_configs = json.load(open(filename))['exchange_connector_configs']
    return MasterConnectorConfig(exchange_connector_configs=[
        from_dict(data_class=ExchangeConnectorConfig, data=connector_config) 
        for connector_config in connector_configs
    ])


def read_session_config(filename: Path) -> SessionConfig:
    log.info(f"Reading master connector config from file {filename}")
    config = json.load(open(filename))
    return from_dict(data_class=SessionConfig, data=config)