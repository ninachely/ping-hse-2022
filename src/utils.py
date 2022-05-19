from pathlib import Path
from time import time_ns
from typing import Callable, Dict, Optional
from requests import Response
from datetime import timedelta

from data import MS_TO_SEC

class RestClient:

    def __init__(self):
        pass

    @staticmethod
    def time_ms():
        return time_ns() // 10 ** 6

    def request(self, base_url: str, request_type: Callable, endpoint: str, data: Optional[Dict] = None) -> float:
        if data is None:
            data = dict()
        data['timestamp'] = self.time_ms()
        return request_type(base_url + endpoint, params=data).elapsed.total_seconds() / MS_TO_SEC


class Config:

    def __init__(self, **entries):
        self.__dict__.update(entries)