"""共有された5テーマの教材コードを、直接走査・実盤面削除・全探索と比較する。"""
import ast
from functools import lru_cache
from io import StringIO
from itertools import product
from pathlib import Path
import random
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
BINARY = 'contests/ABC231-C.md'
COMPRESSION = 'contests/ABC213-C.md'
UNION_FIND = 'algorithms/union-find.md'
VIRUS = 'contests/ABC304-C.md'
JUMP = 'contests/ABC240-C.md'
PAGES = (BINARY, COMPRESSION, UNION_FIND, VIRUS, JUMP)


@lru_cache(None)
def examples(page):
    pattern = r'```python\n(.*?)```\s*入力例：\s*```text\n(.*?)```\s*出力例：\s*```text\n(.*?)```'
    return re.findall(pattern, (ROOT / page).read_text(), re.S)


@lru_cache(None)
def compiled(page, index):
    return compile(examples(page)[index][0], page, 'exec')


def execute(page, data, index=0):
    old_in, old_out = sys.stdin, sys.stdout
    reader, writer = StringIO(data), StringIO()
    namespace = {'__name__': '__main__'}
    try:
        sys.stdin, sys.stdout = reader, writer
        exec(compiled(page, index), namespace)
        return writer.getvalue(), namespace
    finally:
        sys.stdin, sys.stdout = old_in, old_out


def graph_components(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = set()
    count = 0
    for start in range(n):
        if start in seen:
            continue
        count += 1
        seen.add(start)
        pending = [start]
        for u in pending:
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    pending.append(v)
    return count


class AtCoderFiveTopicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tree = ast.parse(examples(UNION_FIND)[0][0])
        node = next(n for n in tree.body if isinstance(n, ast.ClassDef))
        namespace = {}
        exec(compile(ast.Module(body=[node], type_ignores=[]), UNION_FIND, 'exec'), namespace)
        cls.DSU = namespace['DSU']

    def test_six_complete_samples(self):
        total = 0
        for page in PAGES:
            self.assertEqual(len(examples(page)), (ROOT / page).read_text().count('```python\n'))
            for index, (_, data, expected) in enumerate(examples(page)):
                self.assertEqual(execute(page, data, index)[0], expected, page)
                total += 1
        self.assertEqual(total, 6)

    def test_binary_counts_against_linear_scan(self):
        rng = random.Random(231)
        for n in (1, 2, 5, 20, 100):
            for _ in range(20):
                a = [rng.randrange(1, 21) for _ in range(n)]
                queries = [0, 1, 10, 20, 21] + [rng.randrange(25) for _ in range(20)]
                expected = [sum(value >= x for value in a) for x in queries]
                data = f'{n} {len(queries)}\n' + ' '.join(map(str, a)) + '\n' + '\n'.join(map(str, queries)) + '\n'
                self.assertEqual(list(map(int, execute(BINARY, data)[0].split())), expected)

    def test_compression_against_deleting_rows_and_columns(self):
        rng = random.Random(213)
        for _ in range(200):
            h, w = rng.randrange(1, 9), rng.randrange(1, 9)
            points = rng.sample([(r, c) for r in range(h) for c in range(w)], rng.randrange(1, h*w+1))
            board = [[0] * w for _ in range(h)]
            for i, (r, c) in enumerate(points):
                board[r][c] = i + 1
            board = [row for row in board if any(row)]
            for c in range(w-1, -1, -1):
                if all(row[c] == 0 for row in board):
                    for row in board:
                        del row[c]
            expected = [None] * len(points)
            for r, row in enumerate(board):
                for c, card in enumerate(row):
                    if card:
                        expected[card-1] = (r+1, c+1)
            data = f'{h} {w} {len(points)}\n' + ''.join(f'{r+1} {c+1}\n' for r, c in points)
            actual = [tuple(map(int, row.split())) for row in execute(COMPRESSION, data)[0].splitlines()]
            self.assertEqual(actual, expected)

    def test_dsu_operations_and_component_sizes(self):
        rng = random.Random(284)
        for n in range(1, 20):
            uf = self.DSU(n)
            labels = list(range(n))
            for _ in range(100):
                x, y = rng.randrange(n), rng.randrange(n)
                lx, ly = labels[x], labels[y]
                self.assertEqual(uf.union(x, y), lx != ly)
                if lx != ly:
                    labels = [lx if value == ly else value for value in labels]
                self.assertEqual(uf.group_count, len(set(labels)))
                self.assertEqual(len({uf.find(i) for i in range(n)}), uf.group_count)
                for i in range(n):
                    self.assertEqual(uf.same(i, x), labels[i] == labels[x])
                    self.assertEqual(uf.size(i), labels.count(labels[i]))
        self.assertEqual(self.DSU(0).group_count, 0)

    def test_nonroot_attachment_counterexample_and_iterative_find(self):
        bad = self.DSU(4)
        bad.union(0, 1)
        bad.union(0, 2)
        self.assertTrue(bad.same(0, 1))
        bad.parent[1] = 3  # 教材の誤りを再現。通常のunionでは実行しない
        self.assertFalse(bad.same(0, 1))
        good = self.DSU(4)
        good.union(0, 1)
        good.union(0, 2)
        good.union(1, 3)
        self.assertEqual(good.size(0), 4)
        n = 50000
        deep = self.DSU(n)
        deep.parent = list(range(1, n)) + [n-1]  # 反復findの検証用の有効な鎖
        deep._size[-1] = n
        deep.group_count = 1
        self.assertEqual(deep.find(0), n-1)
        self.assertTrue(all(parent == n-1 for parent in deep.parent))
        self.assertEqual(deep.size(0), n)

    def test_components_against_bfs_and_cycle(self):
        rng = random.Random(44)
        for n in range(1, 20):
            edges = [(u, v) for u in range(n) for v in range(u+1, n) if rng.randrange(4) == 0]
            data = f'{n} {len(edges)}\n' + ''.join(f'{u+1} {v+1}\n' for u, v in edges)
            self.assertEqual(int(execute(UNION_FIND, data)[0]), graph_components(n, edges))
        self.assertEqual(execute(UNION_FIND, '3 3\n1 2\n2 3\n1 3\n')[0], '1\n')
        self.assertEqual(execute(UNION_FIND, '6 3\n1 2\n2 3\n4 5\n')[0], '3\n')

    def test_virus_against_explicit_adjacency(self):
        rng = random.Random(304)
        for _ in range(250):
            n = rng.randrange(1, 31)
            d = rng.randrange(1, 11)
            points = rng.sample([(x, y) for x in range(20) for y in range(20)], n)
            g = [[] for _ in range(n)]
            for i in range(n):
                for j in range(i+1, n):
                    if sum((a-b)**2 for a, b in zip(points[i], points[j])) <= d*d:
                        g[i].append(j)
                        g[j].append(i)
            seen = {0}
            pending = [0]
            for u in pending:
                for v in g[u]:
                    if v not in seen:
                        seen.add(v)
                        pending.append(v)
            expected = ''.join('Yes\n' if i in seen else 'No\n' for i in range(n))
            data = f'{n} {d}\n' + ''.join(f'{x} {y}\n' for x, y in points)
            self.assertEqual(execute(VIRUS, data)[0], expected)
        self.assertEqual(execute(VIRUS, '2 5\n0 0\n3 4\n')[0], 'Yes\nYes\n')
        self.assertEqual(execute(VIRUS, '2 4\n0 0\n3 4\n')[0], 'Yes\nNo\n')

    def test_virus_long_chain(self):
        n = 2000
        data = f'{n} 1\n' + ''.join(f'{i} 0\n' for i in range(n))
        self.assertEqual(execute(VIRUS, data)[0], 'Yes\n' * n)

    def check_jump(self, choices, x):
        possible = {sum(path) for path in product(*choices)}
        expected_states = {value for value in possible if value <= x}
        expected = 'Yes\n' if x in possible else 'No\n'
        data = f'{len(choices)} {x}\n' + ''.join(f'{a} {b}\n' for a, b in choices)
        out, state = execute(JUMP, data)
        self.assertEqual(out, expected, data)
        self.assertEqual({j for j, ok in enumerate(state['DP']) if ok}, expected_states)
        out, state = execute(JUMP, data, 1)
        self.assertEqual(out, expected, data)
        self.assertEqual(state['reachable'], expected_states)

    def test_jump_exhaustive_and_update_counterexamples(self):
        checked = 0
        for n in range(1, 5):
            for choices in product(((1, 2), (1, 3), (2, 3)), repeat=n):
                for x in range(1, 13):
                    self.check_jump(choices, x)
                    checked += 1
        self.assertEqual(checked, 1440)
        self.check_jump([(1, 2)], 4)  # 同じターンで何度も跳ぶ誤りを検出
        self.check_jump([(1, 2), (3, 4)], 2)  # 旧状態を残す誤りを検出
        self.check_jump([(1, 3), (2, 4)], 7)  # DPの入れ替えを早める誤りを検出
        self.check_jump([(2, 3)], 1)  # 次の到達可能集合が空になる

    def test_random_jump_paths(self):
        rng = random.Random(240)
        for _ in range(300):
            choices = [tuple(sorted(rng.sample(range(1, 8), 2))) for _ in range(rng.randrange(1, 9))]
            self.check_jump(choices, rng.randrange(1, 41))


if __name__ == '__main__':
    unittest.main()
