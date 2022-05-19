from typing import Dict
from data import Update, UpdateType
from processor import DataProcessor


class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)
        self.file = open(self.config.filename, 'w')
        self.file.write('exchange_name,latency,ts\n')

    def on_update(self, update: Update):
        if update.type == UpdateType.PING_RESULT:
            self.file.write(f'{update.config.exchange_name},{update.inner.latency},{update.ts}\n')

    def on_terminate(self):
        self.file.close()
