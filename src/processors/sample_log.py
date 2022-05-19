from typing import Dict
from data import Update, UpdateType
from processor import DataProcessor


class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)
        self.pairs = []

    def on_update(self, update: Update):
        if update.type == UpdateType.PING_RESULT:
            self.pairs.append((update.config.exchange_url, update.inner.latency, update.ts))

    def on_terminate(self):
        print(self.pairs)
