"""C問題のfir/fin実装を、全ての1要素移動を試す愚直解と照合する。"""
from itertools import product
from pathlib import Path
import random
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'contests/C-Move-One-Card.md'


def reachable_arrays(a):
    """候補配列の生成は検証用だけに使用する。元位置への挿入も含む。"""
    results = set()
    for i in range(len(a)):
        for j in range(len(a)):
            result = list(a)
            card = result.pop(i)
            result.insert(j, card)
            results.add(tuple(result))
    return results


class MoveOneCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        blocks = re.findall(r'```python\n(.*?)```', PAGE.read_text(), re.S)
        if len(blocks) != 1:
            raise AssertionError('C問題の主役となるPython実装は1つにする')
        cls.compiled = compile(blocks[0], str(PAGE), 'exec')

    def fast(self, a, b):
        lines = iter([str(len(a)), ' '.join(map(str, a)), ' '.join(map(str, b))])
        output = []
        exec(self.compiled, {'input': lines.__next__, 'print': output.append})
        self.assertEqual(len(output), 1)
        self.assertIn(output[0], ('Yes', 'No'))
        return output[0] == 'Yes'

    def test_shared_official_samples(self):
        cases = [
            ([1, 4, 1, 4, 2, 1], [1, 4, 1, 1, 4, 2], True),
            ([1, 1], [1, 2], False),
            ([1, 2, 3], [1, 2, 3], True),
            (
                [25, 11, 21, 15, 30, 20, 17, 19, 17, 21, 10, 13, 22, 10, 22, 14, 30, 25, 17, 25, 11, 19, 27, 27, 15, 18, 16, 16, 20, 16],
                [25, 11, 15, 30, 20, 17, 19, 17, 21, 10, 13, 22, 10, 22, 14, 30, 25, 17, 25, 11, 19, 27, 27, 15, 21, 18, 16, 16, 20, 16],
                True,
            ),
        ]
        for a, b, expected in cases:
            with self.subTest(n=len(a), a=a):
                self.assertEqual(self.fast(a, b), expected)
                self.assertEqual(tuple(b) in reachable_arrays(a), expected)

    def test_boundaries_and_middle(self):
        cases = [
            ([1], [1], True),
            ([1, 2, 3, 4], [2, 3, 4, 1], True),
            ([1, 2, 3, 4], [4, 1, 2, 3], True),
            ([1, 2, 3, 4, 5], [1, 3, 2, 4, 5], True),
            ([1, 2, 2, 3], [2, 1, 2, 3], True),
            ([1, 2, 3, 4], [4, 3, 2, 1], False),
            ([5, 1, 2, 3, 4, 6], [5, 4, 3, 2, 1, 6], False),
            ([1, 1, 1], [1, 1, 1], True),
            ([1, 1], [1, 2], False),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(self.fast(a, b), expected)
                self.assertEqual(tuple(b) in reachable_arrays(a), expected)

    def test_all_small_pairs(self):
        checked = 0
        # N<=4は値域1..NでA/Bの全組合せを照合する
        # N=5..7は値域1..2に絞り、同値が多い全組合せを照合する
        for n in range(1, 8):
            alphabet = range(1, n + 1) if n <= 4 else range(1, 3)
            arrays = list(product(alphabet, repeat=n))
            for a in arrays:
                reachable = reachable_arrays(a)
                for b in arrays:
                    self.assertEqual(self.fast(a, b), b in reachable, (a, b))
                    checked += 1
        self.assertEqual(checked, 87786)

    def test_random_arrays(self):
        rng = random.Random(2718)
        for case in range(1000):
            n = rng.randrange(1, 13)
            a = [rng.randrange(1, n + 1) for _ in range(n)]
            b = a[:]
            if case % 3 == 0:
                # 確実に到達可能なケース
                value = b.pop(rng.randrange(n))
                b.insert(rng.randrange(n), value)
            elif case % 3 == 1:
                rng.shuffle(b)  # 値の個数が同じでも到達できるとは限らない
            else:
                b = [rng.randrange(1, n + 1) for _ in range(n)]
            self.assertEqual(self.fast(a, b), tuple(b) in reachable_arrays(a), (a, b))

    def test_maximum_n(self):
        n = 200000
        a = list(range(1, n + 1))
        self.assertTrue(self.fast(a, a))
        self.assertTrue(self.fast(a, a[1:] + a[:1]))
        self.assertTrue(self.fast(a, a[-1:] + a[:-1]))
        self.assertFalse(self.fast(a, list(reversed(a))))


if __name__ == '__main__':
    unittest.main()
