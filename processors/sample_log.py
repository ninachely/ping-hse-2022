from typing import Dict
from data import Update, UpdateType
from processor import DataProcessor

class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)

    def on_update(self, update: Update):
        if update.type == UpdateType.PING_RESULT:
            for i in range(self.config.repeat_times):
                print("ping", update.inner.latency, update.ts, update.config.exchange_name)
        else:
            print(update.request_name, update.inner, update.ts, update.config.exchange_name)

    def on_terminate(self):
        print('Goodbye!')