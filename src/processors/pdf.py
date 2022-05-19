"""
This module generates a PDF report with images and statistics.
"""

from typing import Dict, List
from data import Update, UpdateType
from processor import DataProcessor
from processors.visuals import construct_df, heatmap, plot_of_time_ping, scatterplot_of_time_ping, Datapoint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Module(DataProcessor):

    def __init__(self, config: Dict) -> None:
        super().__init__(config)
        self.datapoints: List[Datapoint] = []

    def on_update(self, update: Update):
        if update.type == UpdateType.PING_RESULT:
            self.datapoints.append(Datapoint(
                update.config.exchange_url, update.inner.latency, update.ts
            )
            )

    def on_terminate(self):
        fig, ax = plt.subplots(3, figsize=(20, 20))
        df = construct_df(self.datapoints)
        scatterplot_of_time_ping(df, ax[0]),
        plot_of_time_ping(df, ax[1]),
        heatmap(df, ax[2])
        with PdfPages(self.config.pdf_path) as pdf:
            pdf.savefig(fig)
