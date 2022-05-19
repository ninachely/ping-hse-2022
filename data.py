from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional
import logging as log
import json
from dacite import from_dict


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
class MainConfig:
    exchanges_list: List[str]
    additional_requests: List[str]
    duration: int
    run_name_format: str
    outputs: List[str]     


def read_master_connector_config(filename: Path) -> MasterConnectorConfig:
    log.info(f"Reading master connector config from file {filename}")
    connector_configs = json.load(open(filename))['exchange_connector_configs']
    return MasterConnectorConfig(exchange_connector_configs=[
        from_dict(data_class=ExchangeConnectorConfig, data=connector_config) 
        for connector_config in connector_configs
    ])
    

def read_main_config(filename: Path) -> MainConfig:
    log.info(f"Reading master connector config from file {filename}")
    config = json.load(open(filename))
    return from_dict(data_class=MainConfig, data=config)