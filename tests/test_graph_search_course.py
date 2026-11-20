"""教材の実装を直接検証。マッチングは独立な全探索、0-1 BFSはDijkstraと比較する。"""
import ast
from functools import lru_cache
import heapq
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path
import random
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    'learning-notes/05_graph.md',
    'algorithms/dfs-bfs-patterns.md',
    'algorithms/dfs-bfs-advanced.md',
    'algorithms/dfs-bfs-states.md',
    'algorithms/bipartite-matching.md',
    'contests/paiza-S082.md',
)
PATTERN = r'```python\n(.*?)```\s*入力例：\s*```text\n(.*?)```\s*出力例：\s*```text\n(.*?)```'


@lru_cache(None)
def examples(page):
    return re.findall(PATTERN, (ROOT / page).read_text(), re.S)


@lru_cache(None)
def compiled(page, index):
    return compile(examples(page)[index][0], page, 'exec')


def execute(page, data, index=0):
    previous_in, previous_out = sys.stdin, sys.stdout
    reader = TextIOWrapper(BytesIO(data.encode()))
    writer = StringIO()
    try:
        sys.stdin, sys.stdout = reader, writer
        exec(compiled(page, index), {'__name__': '__main__'})
        return writer.getvalue()
    finally:
        sys.stdin, sys.stdout = previous_in, previous_out
        reader.close()


def functions(page):
    # IO部分を動かさず、同じ教材内の関数を検証用に取り出す
    tree = ast.parse(examples(page)[0][0])
    nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), page, 'exec'), namespace)
    return namespace


def brute_matching(adj):
    # 左を順に「使わない／未使用の右へ割当」で全列挙。増加道のロジックは使わない
    masks = {0}
    for neighbors in adj:
        next_masks = set(masks)
        for mask in masks:
            for v in neighbors:
                if not (mask >> v) & 1:
                    next_masks.add(mask | (1 << v))
        masks = next_masks
    return max(map(int.bit_count, masks))


def dijkstra(g, start):
    dist = [float('inf')] * len(g)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        value, u = heapq.heappop(heap)
        if value != dist[u]:
            continue
        for v, cost in g[u]:
            nd = value + cost
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def tile_input(h, w, free_mask):
    fixed = [divmod(i, w) for i in range(h * w) if not (free_mask >> i) & 1]
    return f'{h} {w} {len(fixed)}\n' + ''.join(f'{r+1} {c+1}\n' for r, c in fixed)


class GraphSearchCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hk = staticmethod(functions('contests/paiza-S082.md')['hopcroft_karp'])
        cls.kuhn = staticmethod(functions('algorithms/bipartite-matching.md')['maximum_matching'])

    def test_every_complete_program_sample(self):
        total = 0
        for page in PAGES:
            code_count = (ROOT / page).read_text().count('```python\n')
            self.assertEqual(len(examples(page)), code_count, page)
            for i, (_, data, expected) in enumerate(examples(page)):
                with self.subTest(page=page, example=i):
                    self.assertEqual(execute(page, data, i), expected)
                total += 1
        self.assertEqual(total, 18)

    def check_matching(self, adj, right_count):
        expected = brute_matching(adj)
        size, left, right = self.hk(adj, right_count)
        self.assertEqual(size, expected, adj)
        self.assertEqual(self.kuhn(adj, right_count), expected, adj)
        self.assertEqual(sum(x != -1 for x in left), size)
        self.assertEqual(sum(x != -1 for x in right), size)
        for u, v in enumerate(left):
            if v != -1:
                self.assertIn(v, adj[u])
                self.assertEqual(right[v], u)
        for v, u in enumerate(right):
            if u != -1:
                self.assertEqual(left[u], v)

    def test_all_small_bipartite_graphs(self):
        for l in range(4):
            for r in range(4):
                for mask in range(1 << (l * r)):
                    adj = [[v for v in range(r) if (mask >> (u*r+v)) & 1] for u in range(l)]
                    self.check_matching(adj, r)

    def test_random_matching_graphs(self):
        rng = random.Random(20)
        for _ in range(2000):
            l, r = rng.randrange(10), rng.randrange(10)
            adj = [[v for v in range(r) if rng.randrange(3) == 0] for _ in range(l)]
            self.check_matching(adj, r)

    def test_long_augmenting_path_without_recursion(self):
        n = 45000
        adj = [[i, i+1] for i in range(n-1)] + [[0]]
        size, left, right = self.hk(adj, n)
        self.assertEqual(size, n)
        self.assertEqual(left[-1], 0)
        self.assertTrue(all(v != -1 for v in left + right))

    def test_all_small_tiling_boards(self):
        checked = 0
        for h, w in ((1, 1), (2, 3), (3, 3), (3, 4)):
            neighbors = [[] for _ in range(h*w)]
            for p in range(h*w):
                r, c = divmod(p, w)
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < h and 0 <= nc < w:
                        neighbors[p].append(nr*w+nc)

            @lru_cache(None)
            def best_dominoes(mask):
                if mask == 0:
                    return 0
                p = (mask & -mask).bit_length() - 1
                rest = mask ^ (1 << p)
                best = best_dominoes(rest)  # pは小タイルにする
                for q in neighbors[p]:
                    if (rest >> q) & 1:
                        best = max(best, 1 + best_dominoes(rest ^ (1 << q)))
                return best

            for mask in range(1 << (h*w)):
                expected = mask.bit_count() - 2 * best_dominoes(mask)
                self.assertEqual(execute('contests/paiza-S082.md', tile_input(h, w, mask)), f'{expected}\n', (h, w, mask))
                checked += 1
        self.assertEqual(checked, 4674)

    def test_paiza_second_sample_and_maximum_boards(self):
        page = 'contests/paiza-S082.md'
        self.assertEqual(execute(page, '2 5 0\n'), '0\n')
        self.assertEqual(execute(page, '300 300 0\n'), '0\n')
        full_fixed = '300 300 90000\n' + ''.join(f'{r+1} {c+1}\n' for r in range(300) for c in range(300))
        self.assertEqual(execute(page, full_fixed), '0\n')
        fixed = [(r+1, c+1) for r in range(300) for c in range(300) if (r+c) % 2]
        data = '300 300 45000\n' + ''.join(f'{r} {c}\n' for r, c in fixed)
        self.assertEqual(execute(page, data), '45000\n')

    def test_zero_one_bfs_against_dijkstra(self):
        rng = random.Random(17)
        for _ in range(100):
            n = rng.randrange(1, 10)
            edges = [(u, v, rng.randrange(2)) for u in range(n) for v in range(n) if rng.randrange(4) == 0]
            g = [[] for _ in range(n)]
            for u, v, cost in edges:
                g[u].append((v, cost))
            expected = [d if d != float('inf') else -1 for d in dijkstra(g, 0)]
            data = f'{n} {len(edges)}\n' + ''.join(f'{u} {v} {cost}\n' for u, v, cost in edges)
            self.assertEqual(list(map(int, execute('algorithms/dfs-bfs-states.md', data, 1).split())), expected)

    def test_key_and_direction_states(self):
        page = 'algorithms/dfs-bfs-states.md'
        self.assertEqual(execute(page, '1 5\na.SAG\n'), '6\n')
        self.assertEqual(execute(page, '1 3\nSAG\n'), '-1\n')
        self.assertEqual(execute(page, '1 4\nS..G\n', 2), '0\n')
        self.assertEqual(execute(page, '1 3\nS#G\n', 2), '-1\n')
        # 向きの状態を明示的なグラフに変え、ヒープの最短路と比較
        rng = random.Random(12)
        h, w = 3, 4
        ds = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for _ in range(60):
            board = [['#' if rng.randrange(4) == 0 else '.' for _ in range(w)] for _ in range(h)]
            board[0][0], board[-1][-1] = 'S', 'G'
            g = [[] for _ in range(h*w*4 + 1)]
            for r in range(h):
                for c in range(w):
                    if board[r][c] == '#':
                        continue
                    for d in range(4):
                        u = (r*w+c)*4+d
                        for nd, (dr, dc) in enumerate(ds):
                            nr, nc = r+dr, c+dc
                            if 0 <= nr < h and 0 <= nc < w and board[nr][nc] != '#':
                                g[u].append(((nr*w+nc)*4+nd, int(d != nd)))
            source = len(g)-1
            g[source] = [(d, 0) for d in range(4)]
            distance = dijkstra(g, source)
            expected = min(distance[(h*w-1)*4:(h*w)*4])
            if expected == float('inf'):
                expected = -1
            data = f'{h} {w}\n' + ''.join(''.join(row)+'\n' for row in board)
            self.assertEqual(execute(page, data, 2), f'{expected}\n')

    def test_dfs_events_components_and_cycles(self):
        rng = random.Random(9)
        for n in range(1, 25):
            edges = [(u, v) for u in range(n) for v in range(u+1, n) if rng.randrange(8) == 0]
            data = f'{n} {len(edges)}\n' + ''.join(f'{u} {v}\n' for u, v in edges)
            recursive = execute('learning-notes/05_graph.md', data, 1)
            iterative = execute('learning-notes/05_graph.md', data, 2)
            self.assertEqual(iterative, recursive)
        page = 'algorithms/dfs-bfs-advanced.md'
        self.assertEqual(execute(page, '3 3\n0 1\n0 2\n2 1\n', 1), 'No\n')
        self.assertEqual(execute(page, '1 1\n0 0\n', 1), 'Yes\n')
        self.assertEqual(execute(page, '4 4\n0 1\n1 2\n2 3\n3 0\n', 3), 'Yes\n')
        self.assertEqual(execute('algorithms/dfs-bfs-patterns.md', '4 0\n', 1), '4\n')

    def test_paths_and_multisource_boundaries(self):
        page = 'algorithms/dfs-bfs-patterns.md'
        self.assertEqual(execute(page, '1 0\n', 3), '0\n0\n')
        self.assertEqual(execute(page, '2 0\n', 3), '-1\n')
        self.assertEqual(execute(page, '3 1 2\n0 0\n0 1\n', 4), '0 1 -1\n')
        self.assertEqual(execute(page, '3 1 0\n\n0 1\n', 4), '-1 -1 -1\n')
        self.assertEqual(execute('algorithms/dfs-bfs-advanced.md', '1 0\n', 2), '1\n')

    def test_deep_tree_without_recursion(self):
        n = 10000
        data = f'{n}\n' + ''.join(f'{i} {i+1}\n' for i in range(n-1))
        lines = execute('algorithms/dfs-bfs-advanced.md', data).splitlines()
        self.assertEqual(list(map(int, lines[0].split())), list(range(n-1, -1, -1)))
        self.assertEqual(list(map(int, lines[1].split())), list(range(n, 0, -1)))


if __name__ == '__main__':
    unittest.main()
