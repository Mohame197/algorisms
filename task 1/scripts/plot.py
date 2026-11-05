import csv
import math
import os
import sys
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

KINDS = ["sorted", "reverse", "random"]
STYLE = {"insertion": ("tab:red", "o"), "merge": ("tab:blue", "s")}


def load(path):
    data = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            key = (row["algorithm"], row["input"])
            data[key].append(
                (int(row["n"]), float(row["comparisons"]),
                 float(row["moves"]), float(row["time_us"]))
            )
    for key in data:
        data[key].sort()
    return data


def slope(points):
    xs = [math.log(p[0]) for p in points]
    ys = [math.log(p[3]) for p in points]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def plot_time(data, out_dir):
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    for ax, kind in zip(axes, KINDS):
        for algo, (color, marker) in STYLE.items():
            pts = data[(algo, kind)]
            ax.plot([p[0] for p in pts], [p[3] for p in pts],
                    color=color, marker=marker, label=algo + " sort")
        ax.set_title(kind + " input")
        ax.set_xlabel("n")
        ax.set_ylabel("time (microseconds)")
        ax.grid(alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "time_vs_n.png"), dpi=150)
    plt.close(fig)


def plot_growth(data, out_dir):
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    for ax, kind in zip(axes, KINDS):
        pts = data[("insertion", kind)]
        ns = [p[0] for p in pts]
        times = [p[3] for p in pts]
        ax.plot(ns, times, color="tab:red", marker="o", label="measured")
        last_n, last_t = ns[-1], times[-1]
        ax.plot(ns, [last_t * n / last_n for n in ns], "--",
                color="gray", label="c * n")
        ax.plot(ns, [last_t * (n / last_n) ** 2 for n in ns], ":",
                color="black", label="c * n^2")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title("insertion sort, " + kind)
        ax.set_xlabel("n")
        ax.set_ylabel("time (microseconds)")
        ax.grid(alpha=0.3, which="both")
        ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "growth_loglog.png"), dpi=150)
    plt.close(fig)


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "results/results.csv"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "figures"
    os.makedirs(out_dir, exist_ok=True)
    data = load(csv_path)
    plot_time(data, out_dir)
    plot_growth(data, out_dir)
    print("log-log slope of time against n")
    for algo in STYLE:
        for kind in KINDS:
            print(f"{algo:10s} {kind:8s} {slope(data[(algo, kind)]):.2f}")


if __name__ == "__main__":
    main()
