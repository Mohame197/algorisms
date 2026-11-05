from typing import List

import numpy as np
import pandas as pd


def load_prices(path: str, date_column: str = "Date", price_column: str = "Close") -> pd.DataFrame:
    frame = pd.read_csv(path)
    for column in (date_column, price_column):
        if column not in frame.columns:
            raise ValueError(f"column '{column}' not found in {path}")
    frame = frame[[date_column, price_column]].rename(
        columns={date_column: "Date", price_column: "Price"}
    )
    frame["Date"] = pd.to_datetime(frame["Date"])
    frame["Price"] = pd.to_numeric(frame["Price"], errors="coerce")
    frame = frame.dropna().sort_values("Date").reset_index(drop=True)
    return frame


def generate_prices(n: int, seed: int = 42, start: float = 100.0) -> List[float]:
    rng = np.random.default_rng(seed)
    log_returns = rng.normal(loc=0.0, scale=0.01, size=n - 1)
    series = start * np.exp(np.concatenate(([0.0], np.cumsum(log_returns))))
    return series.tolist()
