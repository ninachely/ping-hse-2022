from typing import Dict
from data import Update, UpdateType
from processor import DataProcessor

class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)

    def on_update(self, update: Update):
        pass

    def on_terminate(self):
        pass