"""教材の基本コードをそのまま実行し、全操作を列挙する参照解と照合する。"""
from itertools import product
from pathlib import Path
import random
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'techniques/count-distinct-left-moves.md'


def moved(a, l, r):
    """位置rをlへ移す。高速解の条件式は使用しない。"""
    b = list(a)
    value = b.pop(r)
    b.insert(l, value)
    return tuple(b)


def brute_force(a):
    return len({moved(a, l, r) for r in range(len(a)) for l in range(r + 1)})


class DistinctLeftMovesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        blocks = re.findall(r'```python\n(.*?)```', PAGE.read_text(), re.S)
        if len(blocks) != 1:
            raise AssertionError('主役となる実行可能なPythonコードは1つにする')
        cls.compiled = compile(blocks[0], str(PAGE), 'exec')

    def fast(self, a):
        # 数千のケースごとにプロセスを起動せず、掲載コードに入力と出力だけを渡す
        lines = iter([str(len(a)), ' '.join(map(str, a))])
        output = []
        exec(self.compiled, {'input': lines.__next__, 'print': output.append})
        self.assertEqual(len(output), 1)
        return output[0]

    def test_requested_cases(self):
        cases = [
            ([1], 1),
            ([1, 1, 1], 1),
            ([1, 2, 3], 4),
            ([1, 2, 1], 3),
            ([1, 2, 2], 2),
            ([1, 4, 1, 4, 2, 1], 12),
            ([1, 2, 2, 3, 2, 3], None),
        ]
        for a, expected in cases:
            with self.subTest(a=a):
                actual = brute_force(a)
                if expected is not None:
                    self.assertEqual(actual, expected)
                self.assertEqual(self.fast(a), actual)

    def test_exhaustive_small_arrays(self):
        checked = 0
        # N<=5は値域1..Nを完全列挙する
        for n in range(1, 6):
            for a in product(range(1, n + 1), repeat=n):
                self.assertEqual(self.fast(a), brute_force(a), a)
                checked += 1
        # N=6,7は全値域ではなく、同値の重複が多い値域1..3を完全列挙する
        for n in (6, 7):
            for a in product(range(1, 4), repeat=n):
                self.assertEqual(self.fast(a), brute_force(a), a)
                checked += 1
        self.assertEqual(checked, 6329)

    def test_random_arrays(self):
        rng = random.Random(20261115)
        for _ in range(1000):
            n = rng.randrange(1, 13)
            a = [rng.randrange(1, n + 1) for _ in range(n)]
            self.assertEqual(self.fast(a), brute_force(a), a)

    def test_changed_endpoints_are_a_unique_normal_form(self):
        # 実際の結果との差分から端点を取り出し、証明に使った性質も確認する
        for n in range(1, 5):
            for a in product(range(1, n + 1), repeat=n):
                representatives = {}
                for r in range(n):
                    for l in range(r + 1):
                        b = moved(a, l, r)
                        changed = [j for j in range(n) if a[j] != b[j]]
                        if not changed:
                            continue
                        left, right = changed[0], changed[-1]
                        self.assertLess(left, right)
                        self.assertNotEqual(a[left], a[right])
                        self.assertNotEqual(a[right - 1], a[right])
                        self.assertEqual(moved(a, left, right), b)
                        key = (left, right)
                        if key in representatives:
                            self.assertEqual(representatives[key], b)
                        representatives[key] = b
                self.assertEqual(len(representatives), len(set(representatives.values())))
                self.assertEqual(len(representatives) + 1, brute_force(a))

    def test_maximum_size_known_answers(self):
        n = 200000
        self.assertEqual(self.fast([1] * n), 1)
        self.assertEqual(self.fast(list(range(1, n + 1))), 1 + n * (n - 1) // 2)


if __name__ == '__main__':
    unittest.main()
