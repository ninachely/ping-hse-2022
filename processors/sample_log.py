from data import Update, UpdateType
from processor import DataProcessor

class Module(DataProcessor):

    def __init__(self) -> None:
        super().__init__()

    def on_update(self, update: Update):
        if update.type == UpdateType.PING_RESULT:
            print(update.inner.latency, update.inner.ts, update.inner.config.exchange_name)

    def on_terminate():
        print('Goodbye!')
        pass