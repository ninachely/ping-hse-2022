from io import BytesIO
from threading import Thread
from typing import Dict

from matplotlib import pyplot as plt
import matplotlib
from data import Update, UpdateType
from processor import DataProcessor
from flask import Flask, send_file

from processors.visuals import Datapoint, construct_df, fig2img, heatmap, plot_of_time_ping


class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)
        matplotlib.use('Agg')

        self.app = Flask(__name__)
        self.app.config['DEBUG'] = False
        self.latest_latencies = {}
        self.datapoints = []

        def serve_pil_image(pil_img):
            img_io = BytesIO()
            pil_img.save(img_io, 'PNG', quality=70)
            img_io.seek(0)
            return send_file(img_io, mimetype='image/jpeg')

        @self.app.route('/data', methods=['GET'])
        def get_data():
            try:
                fig, ax = plt.subplots(2, figsize=(20, 20))
                df = construct_df(self.datapoints)
                heatmap(df, ax[0])
                plot_of_time_ping(df, ax[1])
                return serve_pil_image(
                    fig2img(fig)
                )
            except Exception as e:
                print(e)
                return "Not enough data yet, wait a bit!"

        self.process = Thread(target=self.app.run, args=('localhost', 8080))
        self.process.daemon = True
        self.process.start()

    def on_update(self, update: Update):
        if update.type == UpdateType.PING_RESULT:
            self.datapoints.append(Datapoint(
                update.config.exchange_url, update.inner.latency, update.ts
            )
            )

    def on_terminate(self):
        self.process.join()
