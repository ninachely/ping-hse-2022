from typing import List
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from dataclasses import dataclass
import pandas as pd


@dataclass
class Datapoint:
    url: str
    latency: float
    ts: float


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it."""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def construct_df(datapoints: List[Datapoint]) -> pd.DataFrame:
    datapoints = datapoints[:]
    return pd.DataFrame(
        data={
          "url": map(lambda point: point.url, datapoints),
          "ts": map(lambda point: point.ts - min(datapoints, key=lambda x: x.ts).ts, datapoints),
          "latency": map(lambda point: point.latency, datapoints),
        }
    )


def scatterplot_of_time_ping(df: pd.DataFrame, ax: plt.Axes) -> None:
    sns.scatterplot(data=df, x="ts", y="latency", hue="url", ax=ax).set_title("Зависимость пинга от времени подачи")


def plot_of_time_ping(df: pd.DataFrame, ax: plt.Axes) -> None:
   sns.lineplot(data=df, x="ts", y="latency", hue="url", markers=True, dashes=False, ax=ax).set_title("Зависимость пинга от времени подачи")


PERCENTILES = [0, 5, 25, 50, 75, 90, 95, 99, 100]
def generate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    endpoints = set(df['url'].tolist())
    arr = []
    for endpoint in endpoints:
        for p in PERCENTILES:
            q = df[df['url'] == endpoint]['latency'].quantile(p / 100)
            arr.append([endpoint, p, q])
    stats = pd.DataFrame(columns=["url", "percentile", "latency"], data=arr)
    return stats


def heatmap(df: pd.DataFrame, ax: plt.Axes) -> None:
    stats = generate_statistics(df)
    piv = pd.pivot_table(stats, values="latency", columns=["percentile"], index=["url"], fill_value=0)
    sns.heatmap(piv, square=True, cmap='RdYlGn_r', annot=True, fmt=".3f", ax=ax)
    ax.title.set_text(f"Ping statistics heatmap for every exchange")

