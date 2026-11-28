# 復習から取り出したPythonテンプレート

[困りごと索引へ戻る](../problem-solving-index.md)

[2026年11月28日の学内コンテスト](../contests/campus-2026-11-28/README.md)から再利用部分を関数にした。各ファイルは標準入力を読む解答ではなく、インポートして使う部品。以下のコードはリポジトリ直下で、それぞれ単独で実行できる。解答用の元コードはコンテストのフォルダに残している。

## 1. 重ならない区間の最大個数

[interval_scheduling.py](interval_scheduling.py) の `select_intervals` は終了時刻順に走査し、採用区間のリストを返す。入力を変更しない。前提は各区間の `s < t`。終了が早い区間への交換で個数を減らさないことが根拠。

```python
from templates.interval_scheduling import select_intervals

jobs = [(1, 5), (6, 10), (2, 10)]
print(len(select_intervals(jobs)))  # 閉区間：2
print(len(select_intervals([(1, 2), (2, 3)], closed=False)))  # 半開区間：2
```

`last_end` は最後に採用した終了時刻。未採用をNoneで区別するので負の時刻でも使える。`closed=True` では `last_end < s`、Falseでは `last_end <= s`。時間 O(N log N)、空間 O(N)。[問題の交換法・境界・反例](../contests/campus-2026-11-28/task-scheduling.md)を参照。

## 2. FalseからTrueになる最小の整数

[meguru_binary_search.py](meguru_binary_search.py) の `first_true(ng, ok, is_ok)` は `ng < ok`、`is_ok(ng) == False`、`is_ok(ok) == True` を前提とする。判定は区間内で単調であること。関数は境界の真偽や単調性を自動検証しない。

```python
from templates.meguru_binary_search import first_true

A = [2, 3]
C = 9

def is_ok(t):
    return sum(t // a for a in A) >= C

print(first_true(0, min(A) * C, is_ok))  # 12
```

変更するのは判定関数と初期境界。二分探索の境界更新はそのままでよい。判定1回の時間をF、初期の差をDとすると O(F log D)（D=1なら判定不要）、関数自体の追加空間 O(1)。[ロボット問題の不変条件とトレース](../contests/campus-2026-11-28/button-robots.md)を参照。

## 3. 各接頭辞の最頻値を逐次更新する

[prefix_modes.py](prefix_modes.py) の `prefix_modes` は整数列を受け取り、各接頭辞の最頻値をリストで返す。同率なら小さい整数。空入力なら空リスト。

```python
from templates.prefix_modes import prefix_modes

print(prefix_modes([3, 1, 3, 1, 1]))  # [3, 1, 3, 1, 1]
```

`freq` は出現数、`max_count` は最大回数、`best_class` は同率最小値。1個追加して変化したクラスだけを比較する。時間は平均 O(N)、辞書と答えの空間 O(N)。**追加専用であり、減少・削除にはそのまま使えない。** [分類問題での正しさと事前計算](../contests/campus-2026-11-28/data-classification.md)へ。

## 検証

[自動テスト](../tests/test_campus_2026_11_28.py)は区間の部分集合全探索、1秒ずつのシミュレーション、Counterによる最頻値の再計算など、独立した方法と比較する。実行は `python3 -m unittest discover -s tests -v`。
