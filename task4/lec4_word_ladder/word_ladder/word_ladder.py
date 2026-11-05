from collections import defaultdict, deque


def load_words(path):
    with open(path, encoding="utf-8") as handle:
        return [line.strip().lower() for line in handle if line.strip()]


def group_by_length(words):
    groups = defaultdict(list)
    for word in dict.fromkeys(words):
        groups[len(word)].append(word)
    return dict(groups)


def wildcard_patterns(word):
    return [word[:i] + "*" + word[i + 1:] for i in range(len(word))]


def build_graph(words):
    buckets = defaultdict(list)
    for word in words:
        for pattern in wildcard_patterns(word):
            buckets[pattern].append(word)
    adj = {word: [] for word in words}
    for members in buckets.values():
        for u in members:
            for v in members:
                if u != v:
                    adj[u].append(v)
    return adj


def build_graph_all_pairs(words):
    adj = {word: [] for word in words}
    for i, u in enumerate(words):
        for v in words[i + 1:]:
            if len(u) == len(v) and sum(a != b for a, b in zip(u, v)) == 1:
                adj[u].append(v)
                adj[v].append(u)
    return adj


def bfs(adj, s, target=None):
    dist = {s: 0}
    parent = {s: None}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == target:
            break
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
    return dist, parent


def path(parent, v):
    p = []
    while v is not None:
        p.append(v)
        v = parent[v]
    return p[::-1]


def word_ladder(words, start, target):
    start, target = start.lower(), target.lower()
    if len(start) != len(target):
        return None
    candidates = group_by_length(words).get(len(start), [])
    if target not in set(candidates):
        return None
    vertices = candidates if start in set(candidates) else candidates + [start]
    adj = build_graph(vertices)
    dist, parent = bfs(adj, start, target)
    if target not in dist:
        return None
    return path(parent, target)


def longest_shortest_ladder(adj):
    best = (0, None, None)
    for source in adj:
        dist, parent = bfs(adj, source)
        farthest = max(dist, key=dist.get)
        if dist[farthest] > best[0]:
            best = (dist[farthest], source, farthest)
    return best


def longest_shortest_ladder_in_dictionary(words):
    best = (0, None, None)
    groups = group_by_length(words)
    for length in sorted(groups):
        distance, source, target = longest_shortest_ladder(build_graph(groups[length]))
        if distance > best[0]:
            best = (distance, source, target)
    return best
