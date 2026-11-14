"""Markdownの掲載コードそのものを実行し、出力・参照解・リンクを検証する。"""
from pathlib import Path
import random
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    'techniques/prefix-sums-and-imos.md',
    'techniques/sliding-window-and-counting.md',
    'algorithms/segment-tree.md',
    'algorithms/graph-patterns.md',
    'algorithms/string-patterns.md',
    'algorithms/tree-and-doubling.md',
    'techniques/hash-maps-and-sets.md',
    'techniques/coordinate-compression.md',
    'techniques/interval-merging.md',
    'learning-notes/02_binary_search.md',
    'techniques/count-distinct-left-moves.md',
]


def examples(page):
    # Pythonブロックに続く入力・出力例を順に読み取る
    text = (ROOT / page).read_text()
    pattern = r'```python\n(.*?)```\s*入力例：\s*```text\n(.*?)```\s*出力例：\s*```text\n(.*?)```'
    return re.findall(pattern, text, re.S)


def execute(code, data):
    result = subprocess.run(
        [sys.executable, '-c', code], input=data, text=True,
        capture_output=True, timeout=10,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout


class CommonTechniquesTests(unittest.TestCase):
    def test_all_samples(self):
        count = 0
        for page in PAGES:
            items = examples(page)
            self.assertEqual(len(items), len(re.findall(r'```python\n', (ROOT / page).read_text())))
            for code, data, expected in items:
                with self.subTest(page=page, example=count):
                    self.assertEqual(execute(code, data), expected)
                count += 1
        self.assertEqual(count, 21)

    def test_markdown_links(self):
        for page in ROOT.rglob('*.md'):
            if '.git' in page.parts:
                continue
            for target in re.findall(r'\]\(([^)]+)\)', page.read_text()):
                if not target.startswith(('http:', 'https:', '#')):
                    with self.subTest(page=str(page), target=target):
                        self.assertTrue((page.parent / target.split('#')[0]).is_file())

    def test_segment_tree_against_list(self):
        code = examples('algorithms/segment-tree.md')[0][0]
        rng = random.Random(184)
        for n in (1, 2, 3, 8, 17):
            values = [rng.randrange(-10, 11) for _ in range(n)]
            original = values[:]
            operations, expected = [], []
            for _ in range(60):
                if rng.randrange(2):
                    pos, value = rng.randrange(n), rng.randrange(-20, 21)
                    values[pos] = value
                    operations.append(f'0 {pos} {value}')
                else:
                    left = rng.randrange(n + 1)
                    right = rng.randrange(left, n + 1)
                    operations.append(f'1 {left} {right}')
                    expected.append(str(min(values[left:right])) if left < right else 'INF')
            data = f'{n} {len(operations)}\n' + ' '.join(map(str, original)) + '\n' + '\n'.join(operations) + '\n'
            self.assertEqual(execute(code, data), ''.join(x + '\n' for x in expected))

    def test_windows_against_enumeration(self):
        distinct, sums = [item[0] for item in examples('techniques/sliding-window-and-counting.md')]
        rng = random.Random(23)
        for n in (0, 1, 2, 5, 12):
            values = [rng.randrange(-2, 3) for _ in range(n)]
            intervals = [values[l:r] for l in range(n) for r in range(l + 1, n + 1)]
            longest = max([0] + [len(s) for s in intervals if len(set(s)) == len(s)])
            self.assertEqual(execute(distinct, f'{n}\n' + ' '.join(map(str, values)) + '\n'), f'{longest}\n')
            for k in (-1, 0, 2):
                expected = sum(sum(s) == k for s in intervals)
                self.assertEqual(execute(sums, f'{n} {k}\n' + ' '.join(map(str, values)) + '\n'), f'{expected}\n')

    def test_z_algorithm_against_direct_comparison(self):
        code = examples('algorithms/string-patterns.md')[1][0]
        for p, text in [('a', ''), ('aa', 'aaaa'), ('abcdef', 'abc'), ('#', '##a#'), ('aba', 'abababa')]:
            expected = [str(i) for i in range(len(text)) if text.startswith(p, i)]
            self.assertEqual(execute(code, p + '\n' + text + '\n'), ' '.join(expected) + '\n')

    def test_tree_distances_against_bfs(self):
        code = examples('algorithms/tree-and-doubling.md')[1][0]
        rng = random.Random(917)
        for n in (1, 2, 5, 15):
            edges = [(rng.randrange(v), v) for v in range(1, n)]
            g = [[] for _ in range(n)]
            for u, v in edges:
                g[u].append(v)
                g[v].append(u)
            expected = []
            for start in range(n):
                dist = [-1] * n
                dist[start] = 0
                queue = [start]
                for u in queue:
                    for v in g[u]:
                        if dist[v] == -1:
                            dist[v] = dist[u] + 1
                            queue.append(v)
                expected.extend(map(str, dist))
            data = f'{n} {n*n}\n' + ''.join(f'{u} {v}\n' for u, v in edges)
            data += ''.join(f'{u} {v}\n' for u in range(n) for v in range(n))
            self.assertEqual(execute(code, data), ''.join(x + '\n' for x in expected))

    def test_graph_boundaries(self):
        topo, floyd = [item[0] for item in examples('algorithms/graph-patterns.md')]
        self.assertEqual(execute(topo, '2 2\n0 1\n1 0\n'), 'CYCLE\n')
        self.assertEqual(execute(topo, '1 0\n'), '0\n')
        self.assertEqual(execute(floyd, '2 2\n0 1 -1\n1 0 -1\n'), 'NEGATIVE CYCLE\n')
        self.assertEqual(execute(floyd, '1 0\n'), '0\n')

    def test_frequency_and_reverse_index(self):
        pairs, positions = [item[0] for item in examples('techniques/hash-maps-and-sets.md')]
        rng = random.Random(46)
        for n in (0, 1, 5, 12):
            a = [rng.randrange(-2, 3) for _ in range(n)]
            expected = sum(a[i] == a[j] for i in range(n) for j in range(i + 1, n))
            self.assertEqual(execute(pairs, f'{n}\n' + ' '.join(map(str, a)) + '\n'), f'{expected}\n')
            queries = []
            answers = []
            for _ in range(20):
                l = rng.randrange(n + 1)
                r = rng.randrange(l, n + 1)
                x = rng.randrange(-3, 4)
                queries.append(f'{l} {r} {x}')
                answers.append(str(a[l:r].count(x)))
            data = f'{n} {len(queries)}\n' + ' '.join(map(str, a)) + '\n' + '\n'.join(queries) + '\n'
            self.assertEqual(execute(positions, data), ''.join(x + '\n' for x in answers))

    def test_compression_preserves_order_and_values(self):
        code = examples('techniques/coordinate-compression.md')[0][0]
        for a in ([], [7], [3, 3, 3], [-10**9, 0, 10**9, -10**9]):
            result = execute(code, f'{len(a)}\n' + ' '.join(map(str, a)) + '\n').splitlines()
            ranks, restored, counts = [list(map(int, row.split())) for row in result]
            self.assertEqual(restored, a)
            values = sorted(set(a))
            self.assertEqual(counts, [a.count(x) for x in values])
            for i in range(len(a)):
                for j in range(len(a)):
                    self.assertEqual(a[i] < a[j], ranks[i] < ranks[j])
                    self.assertEqual(a[i] == a[j], ranks[i] == ranks[j])

    def test_prefix_budget_and_nearest_against_enumeration(self):
        items = examples('learning-notes/02_binary_search.md')
        nearest, budget = items[2][0], items[3][0]
        for a in ([0, 0, 2, 0], [1], [2, 2, 2], []):
            prefix = [sum(a[:i]) for i in range(len(a) + 1)]
            queries = range(8)
            expected = [max(i for i, s in enumerate(prefix) if s <= b) for b in queries]
            data = f'{len(a)} 8\n' + ' '.join(map(str, a)) + '\n' + '\n'.join(map(str, queries)) + '\n'
            self.assertEqual(execute(budget, data), ''.join(f'{x}\n' for x in expected))
        for a in ([-5], [1, 3, 3, 7], [-9, 0, 9]):
            queries = [-20, -3, 0, 2, 5, 20]
            expected = [min(a, key=lambda value: (abs(value - x), value)) for x in queries]
            data = f'{len(a)} {len(queries)}\n' + ' '.join(map(str, a)) + '\n' + '\n'.join(map(str, queries)) + '\n'
            self.assertEqual(execute(nearest, data), ''.join(f'{x}\n' for x in expected))

    def test_interval_union_against_integer_cells(self):
        code = examples('techniques/interval-merging.md')[0][0]
        rng = random.Random(116)
        for n in (0, 1, 5, 15):
            intervals = [sorted([rng.randrange(-8, 9), rng.randrange(-8, 9)]) for _ in range(n)]
            cells = {x for l, r in intervals for x in range(l, r)}
            data = f'{n}\n' + ''.join(f'{l} {r}\n' for l, r in intervals)
            result = execute(code, data).splitlines()
            merged = [tuple(map(int, row.split())) for row in result[1:-1]]
            self.assertEqual(int(result[0]), len(merged))
            self.assertEqual(int(result[-1]), len(cells))
            self.assertEqual({x for l, r in merged for x in range(l, r)}, cells)
            self.assertTrue(all(l < r for l, r in merged))
            self.assertTrue(all(merged[i][1] < merged[i + 1][0] for i in range(len(merged) - 1)))


if __name__ == '__main__':
    unittest.main()
