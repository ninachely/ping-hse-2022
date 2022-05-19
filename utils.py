from hashlib import new, sha256
from pathlib import Path
from sqlite3 import DatabaseError
from time import time_ns
from typing import Callable, Dict, Optional
from urllib.parse import urlencode
import importlib
from processor import Module


class PingResult:
    
    def __init__(self, exit_code: int, report: str) -> None:
        self.success: bool = exit_code == 0
        self.latency: Optional[float] = None if not self.success \
            else float(report.split('\n')[1].split()[-2].split('=')[-1])


class RestClient:

    def __init__(self, base_url: str, pkey: str, skey: str):
        self.base_url = base_url
        self.secret = skey
        self.headers = {
            "X-MBX-APIKEY": pkey,
        }

    @staticmethod
    def time_ms():
        return time_ns() // 10 ** 6

    def request(self, request_type: Callable, endpoint: str, data: Optional[Dict] = None) -> str:
        if data is None:
            data = dict()
        data['timestamp'] = self.time_ms()
        signature = new(self.secret.encode(),
                        urlencode(data).encode(), sha256).hexdigest()
        data['signature'] = signature
        return request_type(self.base_url + endpoint, params=data, headers=self.headers).content.decode("utf-8")


def import_data_processor(name: str) -> DataProcessor:
    module = importlib.import_module(name)
    my_class = getattr(module, '')

    my_instance = my_class()
