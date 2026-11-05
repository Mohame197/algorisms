import itertools
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from word_ladder import (
    bfs,
    build_graph,
    build_graph_all_pairs,
    group_by_length,
    load_words,
    longest_shortest_ladder,
    path,
    wildcard_patterns,
    word_ladder,
)

EXAMPLE_WORDS = ["hot", "dot", "dog", "lot", "log", "cog"]


def differ_by_one(u, v):
    return len(u) == len(v) and sum(a != b for a, b in zip(u, v)) == 1


class Grouping(unittest.TestCase):
    def test_group_by_length(self):
        groups = group_by_length(["a", "to", "at", "cat", "dog", "to"])
        self.assertEqual(groups, {1: ["a"], 2: ["to", "at"], 3: ["cat", "dog"]})

    def test_load_words_lowercases_and_skips_blank_lines(self):
        path_ = os.path.join(os.path.dirname(__file__), "sample_words.txt")
        with open(path_, "w", encoding="utf-8") as handle:
            handle.write("Hot\n\n dot \nLOG\n")
        try:
            self.assertEqual(load_words(path_), ["hot", "dot", "log"])
        finally:
            os.remove(path_)

    def test_wildcard_patterns(self):
        self.assertEqual(wildcard_patterns("hit"), ["*it", "h*t", "hi*"])


class GraphConstruction(unittest.TestCase):
    def test_example_edges(self):
        adj = build_graph(EXAMPLE_WORDS)
        self.assertEqual(set(adj["hot"]), {"dot", "lot"})
        self.assertEqual(set(adj["dog"]), {"dot", "log", "cog"})
        self.assertEqual(set(adj["cog"]), {"dog", "log"})

    def test_no_self_loops_no_duplicates_and_symmetry(self):
        adj = build_graph(EXAMPLE_WORDS)
        for u, neighbours in adj.items():
            self.assertNotIn(u, neighbours)
            self.assertEqual(len(neighbours), len(set(neighbours)))
            for v in neighbours:
                self.assertIn(u, adj[v])

    def test_handshake_rule(self):
        adj = build_graph(EXAMPLE_WORDS)
        edges = sum(1 for u, v in itertools.combinations(EXAMPLE_WORDS, 2) if differ_by_one(u, v))
        self.assertEqual(sum(len(n) for n in adj.values()), 2 * edges)

    def test_buckets_match_all_pairs_on_random_words(self):
        rng = random.Random(1)
        words = list({"".join(rng.choice("abcd") for _ in range(4)) for _ in range(120)})
        fast = build_graph(words)
        slow = build_graph_all_pairs(words)
        self.assertEqual({w: set(n) for w, n in fast.items()}, {w: set(n) for w, n in slow.items()})

    def test_empty_and_single_word(self):
        self.assertEqual(build_graph([]), {})
        self.assertEqual(build_graph(["cat"]), {"cat": []})


class BfsAndPath(unittest.TestCase):
    def test_distances_and_parents(self):
        adj = build_graph(["hit"] + EXAMPLE_WORDS)
        dist, parent = bfs(adj, "hit")
        self.assertEqual(dist["hot"], 1)
        self.assertEqual(dist["dot"], 2)
        self.assertEqual(dist["cog"], 4)
        self.assertIsNone(parent["hit"])

    def test_path_rebuilds_from_parents(self):
        parent = {"a": None, "b": "a", "c": "b"}
        self.assertEqual(path(parent, "c"), ["a", "b", "c"])
        self.assertEqual(path(parent, "a"), ["a"])

    def test_unreachable_vertices_are_not_in_dist(self):
        adj = build_graph(["cat", "bat", "dog"])
        dist, _ = bfs(adj, "cat")
        self.assertNotIn("dog", dist)


class Ladders(unittest.TestCase):
    def test_lecture_example(self):
        ladder = word_ladder(EXAMPLE_WORDS, "hit", "cog")
        self.assertEqual(ladder, ["hit", "hot", "dot", "dog", "cog"])
        self.assertEqual(len(ladder) - 1, 4)

    def test_target_missing_from_dictionary(self):
        self.assertIsNone(word_ladder(["hot", "dot", "dog", "lot", "log"], "hit", "cog"))

    def test_no_connection(self):
        self.assertIsNone(word_ladder(["cat", "dog", "cot", "dot"], "cat", "pig"))
        self.assertIsNone(word_ladder(["cat", "bat", "dog"], "cat", "dog"))

    def test_same_start_and_target(self):
        self.assertEqual(word_ladder(["cat", "bat"], "cat", "cat"), ["cat"])

    def test_different_lengths(self):
        self.assertIsNone(word_ladder(["cat", "cats"], "cat", "cats"))

    def test_adjacent_words(self):
        self.assertEqual(word_ladder(["cat", "bat"], "cat", "bat"), ["cat", "bat"])

    def test_case_is_ignored(self):
        self.assertEqual(word_ladder(EXAMPLE_WORDS, "HIT", "Cog"), ["hit", "hot", "dot", "dog", "cog"])

    def test_every_step_changes_one_letter_and_uses_valid_words(self):
        rng = random.Random(5)
        words = list({"".join(rng.choice("abc") for _ in range(4)) for _ in range(60)})
        for _ in range(100):
            start, target = rng.sample(words, 2)
            ladder = word_ladder(words, start, target)
            if ladder is None:
                continue
            self.assertEqual((ladder[0], ladder[-1]), (start, target))
            for u, v in zip(ladder, ladder[1:]):
                self.assertTrue(differ_by_one(u, v))
            for word in ladder:
                self.assertIn(word, words)

    def test_ladder_length_matches_floyd_warshall(self):
        rng = random.Random(11)
        words = list({"".join(rng.choice("abc") for _ in range(3)) for _ in range(40)})
        infinity = float("inf")
        distance = {(u, v): 0 if u == v else (1 if differ_by_one(u, v) else infinity) for u in words for v in words}
        for k in words:
            for i in words:
                for j in words:
                    if distance[i, k] + distance[k, j] < distance[i, j]:
                        distance[i, j] = distance[i, k] + distance[k, j]
        for u, v in itertools.product(words, words):
            ladder = word_ladder(words, u, v)
            if distance[u, v] == infinity:
                self.assertIsNone(ladder)
            else:
                self.assertEqual(len(ladder) - 1, distance[u, v])


class Extension(unittest.TestCase):
    def test_longest_shortest_ladder_on_a_chain(self):
        adj = build_graph(["aaa", "aab", "abb", "bbb", "bbc"])
        distance, source, target = longest_shortest_ladder(adj)
        self.assertEqual(distance, 4)
        self.assertEqual({source, target}, {"aaa", "bbc"})

    def test_longest_shortest_ladder_without_edges(self):
        self.assertEqual(longest_shortest_ladder(build_graph(["abc", "xyz"]))[0], 0)


if __name__ == "__main__":
    unittest.main()
