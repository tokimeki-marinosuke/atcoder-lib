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
        self.assertEqual(count, 11)

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


if __name__ == '__main__':
    unittest.main()
