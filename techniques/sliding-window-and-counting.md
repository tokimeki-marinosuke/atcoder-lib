# しゃくとり・区間集計：単調性と頻度を使う

## どちらを使うか

「連続区間」でも条件で手法が変わります。非負数列の和の上限は[既存のしゃくとり法](../learning-notes/09_complexity.md)、重複禁止なら頻度を維持する窓、負数を含む和の一致なら累積和と辞書を検討します。

しゃくとり法では右端を伸ばし、条件を満たさなくなったら左端を進めます。各端点が戻らず全体でN回進むので、二重ループでもO(N)です。**左端を進めれば違反を解消でき、捨てた左端を後から必要としない**ことを確認します。

## 重複しない最長連続区間

入力はNとN個の整数。要素が全て異なる最長連続区間の長さを出力します。辞書操作の平均時間を使うと全体 $O(N)$、空間 $O(N)$。負数も使用可能。

```python
from collections import defaultdict
import sys
input = sys.stdin.readline
n = int(input())
a = list(map(int, input().split()))
count = defaultdict(int)
left = answer = 0
for right, x in enumerate(a):
    count[x] += 1
    while count[x] > 1:
        count[a[left]] -= 1
        left += 1
    answer = max(answer, right - left + 1)
print(answer)
```

入力例：

```text
6
1 2 1 3 2 4
```

出力例：

```text
4
```

## 累積和と辞書で区間和を数える

累積和をSとすると、区間 `[l,r)` の和がKという条件は $S[l]=S[r]-K$。右端rの処理時に、それ以前の累積和の出現数を辞書から取得します。負数があっても単調性を要求しません。

## 和がKの非空連続区間数

入力はN KとN個の整数。時間は平均 $O(N)$、空間 $O(N)$。累積和の照会を登録より先に行い、空区間を数えないようにします。

```python
from collections import defaultdict
import sys
input = sys.stdin.readline
n, k = map(int, input().split())
a = list(map(int, input().split()))
seen = defaultdict(int)
seen[0] = 1  # 先頭から始まる区間のための空の接頭辞
prefix = answer = 0
for x in a:
    prefix += x
    answer += seen[prefix - k]
    seen[prefix] += 1
print(answer)
```

入力例：

```text
4 0
1 -1 0 2
```

出力例：

```text
3
```

## よくある間違い

負数がある和の条件に非負数用のしゃくとりを流用しません。区間和の辞書では頻度が必要で、集合だと同じ累積和の複数回出現を失います。全要素0・K=0なら答えはN(N+1)/2です。部分列（飛び飛びに選べる列）は連続区間とは異なり、通常この方法は使えません。

関連：[累積和](prefix-sums-and-imos.md)・[計算量](../algorithms/complexity.md)・[早見表](../algorithms/common-techniques.md)
