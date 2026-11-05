import math
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from max_profit import brute_force, divide_and_conquer, linear_scan, load_prices

SIZES = [10**3, 2 * 10**3, 5 * 10**3, 10**4, 2 * 10**4, 5 * 10**4, 10**5, 2 * 10**5, 5 * 10**5, 10**6]
BRUTE_FORCE_LIMIT = 5 * 10**3
REPEATS = 5


def random_walk(n, seed):
    steps = np.random.default_rng(seed).normal(0.0, 1.0, n)
    walk = np.cumsum(steps)
    return (walk - walk.min() + 1.0).round(2).tolist()


def best_time(function, prices):
    best = float("inf")
    for _ in range(REPEATS):
        start = time.perf_counter()
        function(prices)
        best = min(best, time.perf_counter() - start)
    return best


def run_runtime_experiment():
    rows = []
    for n in SIZES:
        prices = random_walk(n, seed=n)
        dc_trade = divide_and_conquer(prices)
        ls_trade = linear_scan(prices)
        assert math.isclose(dc_trade.profit, ls_trade.profit, rel_tol=1e-9, abs_tol=1e-9)
        row = {
            "n": n,
            "divide_and_conquer_s": best_time(divide_and_conquer, prices),
            "linear_scan_s": best_time(linear_scan, prices),
            "brute_force_s": best_time(brute_force, prices) if n <= BRUTE_FORCE_LIMIT else None,
            "profit": round(dc_trade.profit, 2),
        }
        row["dc_over_n_log_n_ns"] = row["divide_and_conquer_s"] / (n * math.log2(n)) * 1e9
        row["ls_over_n_ns"] = row["linear_scan_s"] / n * 1e9
        row["ratio"] = row["divide_and_conquer_s"] / row["linear_scan_s"]
        rows.append(row)
    return pd.DataFrame(rows)


def plot_runtime(results, path):
    figure, axis = plt.subplots(figsize=(4.2, 3.0))
    axis.loglog(results["n"], results["divide_and_conquer_s"], "o-", label="divide and conquer")
    axis.loglog(results["n"], results["linear_scan_s"], "s-", label="linear scan")
    brute = results.dropna(subset=["brute_force_s"])
    axis.loglog(brute["n"], brute["brute_force_s"], "^-", label="brute force")
    axis.set_xlabel("number of days n")
    axis.set_ylabel("time (s)")
    axis.grid(True, which="both", alpha=0.3)
    axis.legend(fontsize=7)
    figure.tight_layout()
    figure.savefig(path, dpi=200)
    plt.close(figure)


def plot_trade(csv_path, path):
    prices = load_prices(csv_path)
    trade = divide_and_conquer(prices)
    figure, axis = plt.subplots(figsize=(4.2, 3.0))
    axis.plot(range(len(prices)), prices, linewidth=0.8, color="#444444")
    axis.plot(trade.buy_day, prices[trade.buy_day], "go", label=f"buy (day {trade.buy_day})")
    axis.plot(trade.sell_day, prices[trade.sell_day], "ro", label=f"sell (day {trade.sell_day})")
    axis.set_xlabel("day")
    axis.set_ylabel("price")
    axis.grid(True, alpha=0.3)
    axis.legend(fontsize=7, loc="upper left")
    figure.tight_layout()
    figure.savefig(path, dpi=200)
    plt.close(figure)


def main():
    results = run_runtime_experiment()
    results.to_csv("results/runtime.csv", index=False)
    plot_runtime(results, "results/runtime.png")
    plot_trade("data/prices.csv", "results/trade.png")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
