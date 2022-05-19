from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from typing import Dict, List, Optional, Union
import logging as log
import json
from requests import Response
from dacite import from_dict

MS_TO_SEC = 0.001


@dataclass
class RestClientConfig:
    skey: str
    pkey: str
    

@dataclass
class RequestConfig:
    name: str
    base_url: str
    endpoint: str


class UpdateType(Enum):
    PING_RESULT = 1
    REQUEST_RESPONSE = 2


@dataclass
class ExchangeConnectorConfig:
    exchange_name: str
    exchange_url: str
    rest_client_config: Optional[RestClientConfig]
    requests: List[RequestConfig]


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
    data_processors: List[Dict]    



class PingResult:
    def __init__(self, config: ExchangeConnectorConfig, ts: float, exit_code: int, report: str) -> None:
        self.success: bool = exit_code == 0
        self.latency: Optional[float] = None if not self.success \
            else float(report.split('\n')[1].split()[-2].split('=')[-1])
        self.config = config
        self.ts = ts
 

@dataclass
class Update:
    type: UpdateType
    inner: Union[PingResult, Response]



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