# 二分探索

## 図でつかむ：条件の境界へ向けて、探索範囲を半分にする

xの2乗が10以上となる最小の非負整数xを探す例です。成立・不成立が一方向にだけ変わることが前提です。

```mermaid
flowchart LR
    A["候補: 0〜10<br/>成立の境界を探す"] --> B["5は成立<br/>左側へ絞る"]
    B --> C["2は不成立、3も不成立<br/>4は成立"]
    C --> D["境界: 4"]
```

## 概要・用途・仕組み

探索範囲を半分ずつ縮めます。整列済み配列の値の位置、条件を満たす最小値・最大値を求めるときに使います。答えを二分探索するには、判定結果が「偽→真」など一方向にだけ変化する単調性が必要です。

`bisect_left(a, x)` はx以上の最初の位置、`bisect_right(a, x)` はxより大きい最初の位置です。該当位置がなければlen(a)。重複の個数は両者の差です。前提となる[ソート](01_sorting.md)は別途必要です。

### bisectで範囲と個数を調べる

入力はNとx、N個の整数。整列後の左境界・右境界・個数を出力します。整列$O(N\log N)$、探索各$O(\log N)$、空間$O(N)$。

```python
from bisect import bisect_left, bisect_right
import sys
input = sys.stdin.readline
n, x = map(int, input().split())
a = sorted(map(int, input().split()))
l = bisect_left(a, x)
r = bisect_right(a, x)
print(l, r, r - l)  # 添字は0始まり、範囲は[l, r)
```

入力例：

```text
5 3
3 1 3 7 3
```

出力例：

```text
1 4 3
```

### 答えを二分探索する

非負整数Sに対し、$x^2\ge S$となる最小の非負整数xを求めます。loは常に不成立、hiは常に成立。区間幅1でhiが答えです。判定回数$O(\log(S+2))$、通常の整数演算モデルで空間$O(1)$。

```python
s = int(input())
lo, hi = -1, max(1, s)
while hi - lo > 1:
    mid = (lo + hi) // 2
    if mid * mid >= s:  # mid以上もすべて成立する
        hi = mid
    else:
        lo = mid
print(hi)
```

入力例：

```text
10
```

出力例：

```text
4
```

## 注意点

探索開始時の境界が本当に成立・不成立か確認します。配列長0や全要素同じ場合、探索値が最大値より大きい場合も確認しましょう。bisectの戻り値で配列を読む前に範囲を確認します。`insort` は位置探索こそ$O(\log N)$ですが要素移動で$O(N)$です。浮動小数点の探索は整数の終了条件を流用せず、回数や誤差を定めます。

[DPのLIS](03_dp.md)でもbisectを利用します。

## 練習問題

- [abc146_c：予算以内の最大整数を二分探索](https://atcoder.jp/contests/abc146/tasks/abc146_c)
- [abc061_c：ソートと累積個数で順位を探す](https://atcoder.jp/contests/abc061/tasks/abc061_c)

[目次へ](README.md)
