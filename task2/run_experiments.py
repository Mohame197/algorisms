import csv
import math
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from maxprofit import (
    generate_prices,
    load_prices,
    max_profit_divide_and_conquer,
    max_profit_linear,
)

SIZES = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
ALGORITHMS = [
    ("linear", max_profit_linear),
    ("divide_and_conquer", max_profit_divide_and_conquer),
]


def median_time_ms(function, prices, repeats):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(prices)
        times.append((time.perf_counter() - start) * 1000.0)
    return statistics.median(times)


def run(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for n in SIZES:
        prices = generate_prices(n, seed=42)
        linear = max_profit_linear(prices)
        divide = max_profit_divide_and_conquer(prices)
        if not math.isclose(linear.profit, divide.profit, rel_tol=1e-9, abs_tol=1e-9):
            raise SystemExit(f"algorithms disagree at n = {n}")
        repeats = 9 if n <= 100_000 else 5
        for name, function in ALGORITHMS:
            rows.append((name, n, median_time_ms(function, prices, repeats), linear.profit))
            print(f"{name:20s} n={n:>9,d} {rows[-1][2]:10.3f} ms", file=sys.stderr)
    path = os.path.join(out_dir, "results.csv")
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["algorithm", "n", "time_ms", "profit"])
        for name, n, ms, profit in rows:
            writer.writerow([name, n, f"{ms:.4f}", f"{profit:.4f}"])
    return path


def real_data(csv_path):
    frame = load_prices(csv_path)
    prices = frame["Price"].tolist()
    linear = max_profit_linear(prices)
    divide = max_profit_divide_and_conquer(prices)
    return frame, linear, divide


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "results"
    print(run(out))
