"""共有された復習仕様を、独立した愚直解と照合する。"""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations
from pathlib import Path
import random
import runpy
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from templates.interval_scheduling import select_intervals
from templates.meguru_binary_search import first_true
from templates.prefix_modes import prefix_modes

PAGES = ROOT / 'contests/campus-2026-11-28'


def run(name, data):
    # run_pathは実際の保存コードを実行し、標準入力の読取りも検証する。
    old = sys.stdin
    out = StringIO()
    try:
        sys.stdin = StringIO(data)
        with redirect_stdout(out):
            runpy.run_path(str(PAGES / name), run_name='__main__')
    finally:
        sys.stdin = old
    return out.getvalue().strip()


def schedule_brute(jobs, closed=True):
    best = 0
    for mask in range(1 << len(jobs)):
        chosen = [jobs[i] for i in range(len(jobs)) if mask >> i & 1]
        valid = all((b < c or d < a) if closed else (b <= c or d <= a)
                    for (a, b), (c, d) in combinations(chosen, 2))
        if valid:
            best = max(best, len(chosen))
    return best


class CampusTests(unittest.TestCase):
    def test_friendship_states(self):
        rng = random.Random(1128)
        for _ in range(150):
            n = rng.randint(1, 8)
            edges = [(a, b, rng.randrange(20)) for a, b in combinations(range(1, n + 1), 2)
                     if rng.randrange(2)]
            logs = [(rng.choice('+-'), rng.randint(1, n)) for _ in range(rng.randrange(12))]
            members = {x for x in range(1, n + 1)
                       if next((op for op, y in reversed(logs) if y == x), '-') == '+'}
            expected = max([w for a, b, w in edges if (a in members) != (b in members)], default=0)
            data = f'{n} {len(edges)} {len(logs)}\n' + ''.join(f'{a} {b} {w}\n' for a, b, w in edges)
            data += ''.join(f'{op} {x}\n' for op, x in logs)
            for name in ['villager_friendship.py', 'villager_friendship_improved.py']:
                self.assertEqual(run(name, data), str(expected))

    def test_negative_weights_are_separate_generalization(self):
        data = '2 1 1\n1 2 -7\n+ 1\n'
        self.assertEqual(run('villager_friendship.py', data), '0')
        self.assertEqual(run('villager_friendship_improved.py', data), '-7')
        self.assertEqual(run('villager_friendship_improved.py', '2 0 0\n'), '0')

    def test_schedule_random_and_boundaries(self):
        rng = random.Random(23)
        cases = [[(1, 5), (6, 10), (2, 10)], [(1, 2), (2, 3)],
                 [(1, 10), (2, 3), (4, 5)], [(1, 4), (4, 5), (5, 8)]]
        cases += [[tuple(sorted(rng.sample(range(1, 20), 2))) for _ in range(rng.randint(1, 8))]
                  for _ in range(180)]
        for jobs in cases:
            original = jobs[:]
            for closed in [True, False]:
                selected = select_intervals(jobs, closed=closed)
                self.assertEqual(len(selected), schedule_brute(jobs, closed))
            self.assertEqual(jobs, original)
            data = str(len(jobs)) + '\n' + ''.join(f'{s} {t}\n' for s, t in jobs)
            self.assertEqual(int(run('task_scheduling.py', data)), schedule_brute(jobs))
        self.assertEqual(select_intervals([]), [])
        self.assertEqual(len(select_intervals([(-5, -3), (-2, -1)])), 2)

    def test_prefix_modes_random(self):
        rng = random.Random(4)
        for _ in range(200):
            values = [rng.randint(-3, 5) for _ in range(rng.randrange(30))]
            expected = []
            for k in range(1, len(values) + 1):
                counts = Counter(values[:k])
                expected.append(min(counts, key=lambda c: (-counts[c], c)))
            self.assertEqual(prefix_modes(values), expected)

    def test_classification_both_versions(self):
        rng = random.Random(5)
        for _ in range(150):
            n = rng.randint(1, 16)
            points = [(rng.randint(-4, 4), rng.randint(-4, 4), rng.choice([1, 2, 3, 10**9]))
                      for _ in range(n)]
            x0, y0 = rng.randint(-4, 4), rng.randint(-4, 4)
            ordered = sorted(points, key=lambda p: ((p[0]-x0)**2 + (p[1]-y0)**2, p[2]))
            ks = list(range(1, n + 1)) + [1, n]
            rng.shuffle(ks)
            answers = []
            for k in ks:
                counts = Counter(c for x, y, c in ordered[:k])
                answers.append(str(min(counts, key=lambda c: (-counts[c], c))))
            data = f'{n}\n' + ''.join(f'{x} {y} {c}\n' for x, y, c in points)
            data += f'{x0} {y0}\n{len(ks)}\n' + ''.join(f'{k}\n' for k in ks)
            for name in ['data_classification.py', 'data_classification_improved.py']:
                self.assertEqual(run(name, data), '\n'.join(answers))

    def test_robots_given_and_random(self):
        cases = [([2, 3], 9, 12), ([18], 12, 216),
                 ([998244353], 998244353, 996491788296388609),
                 ([10**9], 10**9, 10**18), ([1, 1], 1, 1)]
        rng = random.Random(6)
        for _ in range(150):
            a = [rng.randint(1, 12) for _ in range(rng.randint(1, 6))]
            c = rng.randint(1, 30)
            t = count = 0
            while count < c:
                t += 1
                count += sum(t % period == 0 for period in a)
            cases.append((a, c, t))
        for a, c, expected in cases:
            data = f'{len(a)} {c}\n' + ' '.join(map(str, a)) + '\n'
            for name in ['button_robots.py', 'button_robots_improved.py']:
                self.assertEqual(int(run(name, data)), expected)
            self.assertEqual(first_true(0, min(a)*c, lambda t: sum(t//x for x in a) >= c), expected)

    def test_binary_search_boundaries(self):
        for boundary in range(-10, 11):
            self.assertEqual(first_true(-11, 11, lambda x: x >= boundary), boundary)
        self.assertEqual(first_true(3, 4, lambda x: x >= 4), 4)
        with self.assertRaises(ValueError):
            first_true(1, 1, lambda x: True)

    def test_document_examples(self):
        import re
        for page, names in [
            ('villager-friendship.md', ['villager_friendship.py', 'villager_friendship_improved.py']),
            ('task-scheduling.md', ['task_scheduling.py']),
            ('data-classification.md', ['data_classification.py', 'data_classification_improved.py']),
            ('button-robots.md', ['button_robots.py', 'button_robots_improved.py']),
        ]:
            text = (PAGES / page).read_text()
            data = re.search(r'入力例[^\n]*：\n\n```text\n(.*?)```', text, re.S).group(1)
            expected = re.search(r'出力例：\n\n```text\n(.*?)```', text, re.S).group(1).strip()
            for name in names:
                self.assertEqual(run(name, data), expected)
        text = (ROOT / 'templates/README.md').read_text()
        for block in re.findall(r'```python\n(.*?)```', text, re.S):
            with redirect_stdout(StringIO()):
                exec(compile(block, 'templates/README.md', 'exec'), {})

    def test_large_classification(self):
        # 最大N・Qで、入力処理と答えの表引きを実際の別プロセスで確認。
        n = 100000
        data = f'{n}\n' + '0 0 1000000000\n' * n + f'0 0\n{n}\n' + f'{n}\n' * n
        for name in ['data_classification.py', 'data_classification_improved.py']:
            result = subprocess.run([sys.executable, str(PAGES/name)], input=data, text=True,
                                    capture_output=True, check=True, timeout=20)
            self.assertEqual(result.stdout, '1000000000\n' * n)


if __name__ == '__main__':
    unittest.main()
