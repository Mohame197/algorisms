import csv
import math
import os
import sys
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

LABELS = {"linear": "linear scan", "divide_and_conquer": "divide and conquer"}
COLORS = {"linear": "tab:blue", "divide_and_conquer": "tab:red"}


def load(path):
    series = defaultdict(list)
    with open(path, newline="") as handle:
        for row in csv.DictReader(handle):
            series[row["algorithm"]].append((int(row["n"]), float(row["time_ms"])))
    for key in series:
        series[key].sort()
    return series


def slope(points):
    xs = [math.log(n) for n, _ in points]
    ys = [math.log(t) for _, t in points]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "results/results.csv"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "figures"
    os.makedirs(out_dir, exist_ok=True)
    series = load(csv_path)

    fig, ax = plt.subplots(figsize=(6, 4))
    for name, points in series.items():
        ax.plot([n for n, _ in points], [t for _, t in points], marker="o",
                color=COLORS[name], label=LABELS[name])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (number of days)")
    ax.set_ylabel("time (ms)")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "time_vs_n.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    for name, points in series.items():
        if name == "linear":
            values = [t / n * 1000.0 for n, t in points]
            label = "linear scan: time / n"
        else:
            values = [t / (n * math.log2(n)) * 1000.0 for n, t in points]
            label = "divide and conquer: time / (n log2 n)"
        ax.plot([n for n, _ in points], values, marker="o", color=COLORS[name], label=label)
    ax.set_xscale("log")
    ax.set_ylim(bottom=0)
    ax.set_xlabel("n (number of days)")
    ax.set_ylabel("microseconds per unit of work")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "normalized.png"), dpi=150)
    plt.close(fig)

    print("log-log slope of time against n")
    for name, points in series.items():
        print(f"{name:20s} {slope(points):.3f}")


if __name__ == "__main__":
    main()
