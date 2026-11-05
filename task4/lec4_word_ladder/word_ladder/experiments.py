import itertools
import math
import random
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from word_ladder import (
    bfs,
    build_graph,
    build_graph_all_pairs,
    group_by_length,
    load_words,
    longest_shortest_ladder,
    word_ladder,
)

REPEATS = 5
SCALING_SIZES = [10**3, 2 * 10**3, 5 * 10**3, 10**4, 2 * 10**4, 5 * 10**4, 10**5]
BUILD_SIZES = [250, 500, 1000, 2000, 4000]
ALPHABET = "abcd"


def best_time(function, repeats=REPEATS):
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        best = min(best, time.perf_counter() - start)
    return best


def synthetic_words(n, seed):
    length = 1
    while len(ALPHABET) ** length < 4 * n:
        length += 1
    rng = random.Random(seed)
    chosen = rng.sample(range(len(ALPHABET) ** length), n)
    words = []
    for code in chosen:
        letters = []
        for _ in range(length):
            code, digit = divmod(code, len(ALPHABET))
            letters.append(ALPHABET[digit])
        words.append("".join(letters))
    return words


def graph_size(adj, visited=None):
    vertices = list(adj) if visited is None else list(visited)
    return len(vertices), sum(len(adj[v]) for v in vertices) // 2


def scaling_experiment():
    rows = []
    for n in SCALING_SIZES:
        words = synthetic_words(n, seed=n)
        build_seconds = best_time(lambda: build_graph(words), repeats=3)
        adj = build_graph(words)
        source = max(adj, key=lambda w: len(adj[w]))
        dist, _ = bfs(adj, source)
        vertices, edges = graph_size(adj, dist)
        bfs_seconds = best_time(lambda: bfs(adj, source))
        total_vertices, total_edges = graph_size(adj)
        rows.append({
            "words": n,
            "length": len(words[0]),
            "V": total_vertices,
            "E": total_edges,
            "V_reached": vertices,
            "E_reached": edges,
            "build_s": build_seconds,
            "bfs_s": bfs_seconds,
            "bfs_ns_per_V_plus_E": bfs_seconds / (vertices + edges) * 1e9,
            "build_ns_per_V_plus_E": build_seconds / (total_vertices + total_edges) * 1e9,
        })
    return pd.DataFrame(rows)


def build_experiment(words):
    five = group_by_length(words)[5]
    rng = random.Random(314)
    rows = []
    for n in BUILD_SIZES:
        sample = rng.sample(five, n)
        fast = build_graph(sample)
        slow = build_graph_all_pairs(sample)
        assert {w: set(v) for w, v in fast.items()} == {w: set(v) for w, v in slow.items()}
        buckets_seconds = best_time(lambda: build_graph(sample), repeats=3)
        pairs_seconds = best_time(lambda: build_graph_all_pairs(sample), repeats=1)
        rows.append({
            "words": n,
            "edges": sum(len(v) for v in fast.values()) // 2,
            "buckets_s": buckets_seconds,
            "all_pairs_s": pairs_seconds,
            "speedup": pairs_seconds / buckets_seconds,
        })
    return pd.DataFrame(rows)


def dictionary_experiment(words):
    groups = group_by_length(words)
    rows = []
    for length in sorted(groups):
        adj = build_graph(groups[length])
        vertices, edges = graph_size(adj)
        seconds = time.perf_counter()
        distance, source, target = longest_shortest_ladder(adj)
        seconds = time.perf_counter() - seconds
        rows.append({
            "length": length,
            "V": vertices,
            "E": edges,
            "longest_shortest_ladder": distance,
            "from": source,
            "to": target,
            "all_sources_bfs_s": seconds,
        })
    return pd.DataFrame(rows)


def plot_scaling(results, path):
    figure, axis = plt.subplots(figsize=(4.2, 3.0))
    x = (results["V_reached"] + results["E_reached"]).to_numpy(dtype=float)
    y = results["bfs_s"].to_numpy() * 1000
    slope, intercept = np.polyfit(x, y, 1)
    axis.plot(x, y, "o", label="BFS (measured)")
    axis.plot(x, slope * x + intercept, "-", linewidth=1, label="straight-line fit")
    axis.set_xlabel("V + E")
    axis.set_ylabel("BFS time (ms)")
    axis.grid(True, alpha=0.3)
    axis.legend(fontsize=7)
    figure.tight_layout()
    figure.savefig(path, dpi=200)
    plt.close(figure)


def plot_example_graph(path):
    words = ["hot", "dot", "dog", "lot", "log", "cog", "hit"]
    adj = build_graph(words)
    positions = {
        "hit": (0, 1), "hot": (1, 1), "dot": (2, 1.6), "lot": (2, 0.4),
        "dog": (3, 1.6), "log": (3, 0.4), "cog": (4, 1),
    }
    ladder = ["hit", "hot", "dot", "dog", "cog"]
    on_path = set(zip(ladder, ladder[1:]))
    figure, axis = plt.subplots(figsize=(4.2, 2.3))
    for u, v in itertools.combinations(words, 2):
        if v in adj[u]:
            highlighted = (u, v) in on_path or (v, u) in on_path
            axis.plot(
                [positions[u][0], positions[v][0]], [positions[u][1], positions[v][1]],
                color="#d62728" if highlighted else "#999999",
                linewidth=2.2 if highlighted else 1.0, zorder=1,
            )
    for word, (x, y) in positions.items():
        axis.scatter([x], [y], s=620, color="#ffd966" if word in ladder else "#dddddd", edgecolor="#444444", zorder=2)
        axis.text(x, y, word, ha="center", va="center", fontsize=8, zorder=3)
    axis.set_xlim(-0.5, 4.5)
    axis.set_ylim(0, 2.0)
    axis.axis("off")
    figure.tight_layout()
    figure.savefig(path, dpi=200)
    plt.close(figure)


def main():
    words = load_words("data/words.txt")

    scaling = scaling_experiment()
    scaling.to_csv("results/scaling.csv", index=False)
    plot_scaling(scaling, "results/scaling.png")
    print(scaling.to_string(index=False))

    build = build_experiment(words)
    build.to_csv("results/build.csv", index=False)
    print(build.to_string(index=False))

    dictionary = dictionary_experiment(words)
    dictionary.to_csv("results/dictionary.csv", index=False)
    print(dictionary.to_string(index=False))

    plot_example_graph("results/example_graph.png")

    x = (scaling["V_reached"] + scaling["E_reached"]).to_numpy(dtype=float)
    y = scaling["bfs_s"].to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    r_squared = 1 - ((y - (slope * x + intercept)) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    print(f"BFS fit: slope {slope * 1e9:.1f} ns per (V+E), R^2 {r_squared:.4f}")

    for start, target in [("hit", "cog"), ("cold", "warm"), ("head", "tail")]:
        print(start, target, word_ladder(words, start, target))


if __name__ == "__main__":
    main()
