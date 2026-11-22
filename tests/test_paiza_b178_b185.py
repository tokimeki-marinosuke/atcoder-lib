"""B178の同期更新と、B185/一般部分列DPを教材のコードで検証する。"""
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import random
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
GRID = 'contests/paiza-B178.md'
LOVE = 'contests/paiza-B185.md'
GENERAL = 'techniques/subsequence-counting.md'


@lru_cache(None)
def examples(page):
    pattern = r'```python\n(.*?)```\s*入力例：\s*```text\n(.*?)```\s*出力例：\s*```text\n(.*?)```'
    return re.findall(pattern, (ROOT / page).read_text(), re.S)


@lru_cache(None)
def compiled(page, index):
    return compile(examples(page)[index][0], page, 'exec')


def execute(page, data, index=0):
    lines = iter(data.splitlines())
    output = []
    namespace = {'input': lines.__next__, 'print': output.append}
    exec(compiled(page, index), namespace)
    if len(output) != 1:
        raise AssertionError(output)
    return output[0], namespace


def grid_input(n, m, sensors, threshold):
    return f'{n} {m}\n{len(sensors)}\n' + ''.join(f'{r+1} {c+1} {t}\n' for r, c, t in sensors) + f'{threshold}\n'


def synchronous_oracle(n, m, sensors):
    # 行配列のコピーではなく、前ラウンドの座標辞書と次ラウンドの変更集合を分ける
    known = {(r, c): t for r, c, t in sensors}
    while len(known) < n*m:
        pending = {}
        for r in range(n):
            for c in range(m):
                if (r, c) in known:
                    continue
                values = [known[(nr, nc)] for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)) if (nr, nc) in known]
                if values:
                    pending[(r, c)] = sum(values) // len(values)
        if not pending:
            raise AssertionError('センサーのない入力は参照解の対象外')
        known.update(pending)
    return [[known[(r, c)] for c in range(m)] for r in range(n)]


def subsequence_oracle(s, p):
    return sum(''.join(s[i] for i in indices) == p for indices in combinations(range(len(s)), len(p)))


class PaizaB178B185Tests(unittest.TestCase):
    def test_all_five_program_samples_as_processes(self):
        total = 0
        for page in (GRID, LOVE, GENERAL):
            self.assertEqual(len(examples(page)), (ROOT / page).read_text().count('```python\n'))
            for code, data, expected in examples(page):
                result = subprocess.run([sys.executable, '-c', code], input=data, text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected, page)
                total += 1
        self.assertEqual(total, 5)

    def check_grid(self, n, m, sensors, threshold):
        expected_grid = synchronous_oracle(n, m, sensors)
        expected = sum(t >= threshold for row in expected_grid for t in row)
        data = grid_input(n, m, sensors, threshold)
        for index in (0, 1):
            actual, state = execute(GRID, data, index)
            self.assertEqual(state['grid'], expected_grid, (index, data))
            self.assertEqual(actual, expected, data)
            if index == 1:
                distances = [[min(abs(r-sr) + abs(c-sc) for sr, sc, _ in sensors) for c in range(m)] for r in range(n)]
                self.assertEqual(state['dist'], distances)

    def test_b178_shared_samples(self):
        cases = [
            (3, 3, [(0, 0, 20), (0, 2, 25), (2, 2, 30)], 25, 5),
            (4, 6, [(0, 0, 20), (1, 3, 35), (3, 5, 25)], 30, 13),
            (3, 3, [(0, 0, 10), (2, 2, 40)], 25, 6),
        ]
        for n, m, sensors, threshold, expected in cases:
            self.check_grid(n, m, sensors, threshold)
            for index in (0, 1):
                self.assertEqual(execute(GRID, grid_input(n, m, sensors, threshold), index)[0], expected)

    def test_zero_temperature_same_round_and_sentinel(self):
        self.check_grid(1, 1, [(0, 0, 0)], 0)
        self.check_grid(2, 3, [(0, 0, 0)], 0)
        # 中央2マスは同じ距離。片方の新しい値を平均に混ぜてはいけない
        self.check_grid(1, 4, [(0, 0, 0), (0, 3, 100)], 75)
        self.assertEqual(execute(GRID, grid_input(1, 4, [(0, 0, 0), (0, 3, 100)], 75), 1)[0], 2)
        # 以下はNoneと負値が衝突しないことを調べる拡張ケース（公式制約の主張ではない）
        self.check_grid(1, 3, [(0, 0, -10), (0, 2, 10)], 0)
        self.check_grid(1, 3, [(0, 0, -1)], -1)

    def test_all_small_sensor_maps(self):
        checked = 0
        for n, m in ((1, 1), (1, 4), (2, 2), (2, 3)):
            for cells in product((None, 0, 10), repeat=n*m):
                sensors = [(i//m, i % m, t) for i, t in enumerate(cells) if t is not None]
                if not sensors:
                    continue
                self.check_grid(n, m, sensors, 5)
                checked += 1
        self.assertEqual(checked, 890)

    def test_random_sensor_maps(self):
        rng = random.Random(178)
        for _ in range(200):
            n, m = rng.randrange(1, 9), rng.randrange(1, 9)
            positions = rng.sample(range(n*m), rng.randrange(1, n*m+1))
            sensors = [(p//m, p % m, rng.randrange(101)) for p in positions]
            self.check_grid(n, m, sensors, rng.randrange(101))

    def test_largest_temperature_map(self):
        # 単一センサーなら全マスが同じ温度。最遠距離は98
        data = grid_input(50, 50, [(0, 0, 0)], 0)
        for index in (0, 1):
            answer, state = execute(GRID, data, index)
            self.assertEqual(answer, 2500)
            self.assertTrue(all(t == 0 for row in state['grid'] for t in row))
        self.assertEqual(state['dist'][-1][-1], 98)

    def test_no_sensor_is_explicitly_outside_documented_model(self):
        for index in (0, 1):
            with self.assertRaisesRegex(ValueError, 'センサー'):
                execute(GRID, '1 1\n0\n0\n', index)

    def test_love_shared_examples_and_traces(self):
        for s, expected in [('LOVEHEAVYE', 4), ('LOVELOVELOVE', 15), ('LOLOVE', 3), ('LOVE', 1), ('EVOL', 0), ('LLL', 0)]:
            for index in (0, 1):
                self.assertEqual(execute(LOVE, f'{len(s)}\n{s}\n', index)[0], expected)
            self.assertEqual(execute(GENERAL, s+'\nLOVE\n')[0], expected)

    def test_exhaustive_love_strings(self):
        checked = 0
        for n in range(7):
            for letters in product('LOVE', repeat=n):
                s = ''.join(letters)
                expected = subsequence_oracle(s, 'LOVE')
                for index in (0, 1):
                    self.assertEqual(execute(LOVE, f'{n}\n{s}\n', index)[0], expected, s)
                self.assertEqual(execute(GENERAL, s+'\nLOVE\n')[0], expected, s)
                checked += 1
        self.assertEqual(checked, 5461)

    def test_general_patterns_and_reverse_update(self):
        sources = [''.join(x) for n in range(7) for x in product('ab', repeat=n)]
        targets = [''.join(x) for n in range(5) for x in product('ab', repeat=n)]
        checked = 0
        for s in sources:
            for p in targets:
                self.assertEqual(execute(GENERAL, s+'\n'+p+'\n')[0], subsequence_oracle(s, p), (s, p))
                checked += 1
        self.assertEqual(checked, 3937)
        value, state = execute(GENERAL, 'L\nLL\n')
        self.assertEqual(value, 0)
        self.assertEqual(state['dp'], [1, 1, 0])
        self.assertEqual(execute(GENERAL, 'a a\naa\n')[0], 1)

    def test_maximum_love_length(self):
        s = 'L'*25 + 'O'*25 + 'V'*25 + 'E'*25
        for index in (0, 1):
            self.assertEqual(execute(LOVE, f'100\n{s}\n', index)[0], 25**4)
        self.assertEqual(execute(GENERAL, s+'\nLOVE\n')[0], 25**4)


if __name__ == '__main__':
    unittest.main()
