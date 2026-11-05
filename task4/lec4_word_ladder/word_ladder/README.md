# Word Ladder

Turns one word into another by changing one letter at a time, using only words from a dictionary. Words are the vertices of a graph, two words are joined when they differ in exactly one letter, and BFS gives the shortest ladder.

## Structure

| Path | Purpose |
|---|---|
| `word_ladder.py` | `load_words`, `group_by_length`, `build_graph`, `bfs`, `path`, `word_ladder`, `longest_shortest_ladder` |
| `main.py` | Command line interface |
| `experiments.py` | Timing experiments, longest ladder per word length, figures |
| `tests/test_word_ladder.py` | Unit tests |
| `data/words.txt` | 61,935 lowercase English words, one per line (base forms of the Hunspell `en_US` dictionary) |
| `results/` | Experiment output |

## Setup

```
pip install -r requirements.txt
```

## Usage

```
python main.py hit cog
python main.py hit cog --words data/words.txt
python experiments.py
```

## Tests

```
python -m unittest discover -s tests -v
```

## Complexity

N words of length L, E edges.

| Step | Time |
|---|---|
| Build graph with wildcard buckets | O(N·L² + E) |
| Build graph comparing all pairs | Θ(N²·L) |
| BFS and path | O(V + E) |
| Longest shortest ladder (BFS from every word) | O(V·(V + E)) |
