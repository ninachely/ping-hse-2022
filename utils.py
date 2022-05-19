from hashlib import new, sha256
from pathlib import Path
from time import time_ns
from typing import Callable, Dict, Optional
from urllib.parse import urlencode


class RestClient:

    def __init__(self, pkey: str, skey: str):
        self.secret = skey
        self.headers = {
            "X-MBX-APIKEY": pkey,
        }

    @staticmethod
    def time_ms():
        return time_ns() // 10 ** 6

    def request(self, base_url: str, request_type: Callable, endpoint: str, data: Optional[Dict] = None) -> str:
        if data is None:
            data = dict()
        data['timestamp'] = self.time_ms()
        signature = new(self.secret.encode(),
                        urlencode(data).encode(), sha256).hexdigest()
        data['signature'] = signature
        return request_type(base_url + endpoint, params=data, headers=self.headers).content.decode("utf-8")


class Config:

    def __init__(self, **entries):
        self.__dict__.update(entries)