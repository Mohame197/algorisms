import argparse

import numpy as np
import pandas as pd


def generate(n, seed, start_price=100.0, volatility=0.02):
    rng = np.random.default_rng(seed)
    returns = rng.normal(0.0002, volatility, n - 1)
    prices = start_price * np.cumprod(np.concatenate(([1.0], 1.0 + returns)))
    dates = pd.bdate_range("2020-01-01", periods=n)
    return pd.DataFrame({"date": dates, "price": prices.round(2)})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=314)
    parser.add_argument("--output", default="data/prices.csv")
    args = parser.parse_args()
    generate(args.days, args.seed).to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
