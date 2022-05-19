from statistics import stdev, mean, median
from typing import Dict
from data import Update, UpdateType
from processor import DataProcessor


class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)
        self.data_by_exchange = {}

    def on_update(self, update: Update):
        if update.type == UpdateType.PING_RESULT:
            if update.config.exchange_name not in self.data_by_exchange:
                self.data_by_exchange[update.config.exchange_name] = []
            self.data_by_exchange[update.config.exchange_name].append(update.inner.latency)

    def print_statistics(self):
        print(f"Total exchanges: {len(self.data_by_exchange)}")
        print("exchange     \t min \t avg \t max \t stdev \t median")
        for exchange, data in self.data_by_exchange.items():
            print(f"{exchange} \t %.1f \t %.1f \t %.1f \t %.1f \t %.1f" %
                  (min(data), mean(data), max(data), stdev(data), median(data))
                  )

    def on_terminate(self):
        self.print_statistics()
