from threading import Thread
from typing import Dict
from data import Update, UpdateType
from processor import DataProcessor
from flask import Flask

class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)

        self.app = Flask(__name__)

        @self.app.route('/data', methods=['GET'])
        def get_data():
            return '1'

        self.process = Thread(target=self.app.run, args=('localhost', 8080))
        self.process.start() 

    def on_update(self, update: Update):
        pass

    def on_terminate(self):
        self.process.join()
