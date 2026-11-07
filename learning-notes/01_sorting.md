# ソート

## 概要と使いどころ

ソートは要素をある基準で並べ替える操作です。順位、中央値、小さい順の処理、重複除去、区間の整理で使います。整列すると「同じ値が隣り合う」「大小関係が位置に対応する」性質が生まれ、[二分探索](02_binary_search.md)や[貪欲法](04_greedy.md)につながります。

## 標準ライブラリと仕組み

|操作|結果|元のリスト|時間|追加空間の最悪値|
|---|---|---|---|---|
|`a.sort()`|戻り値はNone|変更する|$O(N\log N)$|$O(N)$|
|`sorted(a)`|新しいリスト|変更しない|$O(N\log N)$|$O(N)$|
|`sorted(a, reverse=True)`|降順のリスト|変更しない|$O(N\log N)$|$O(N)$|

Pythonのソートは安定です。同じキーの要素の入力順は保たれます。整列済みの区間を利用するTimsort系の実装で、既に整列していれば$O(N)$になる場合があります。組込みソートも補助領域を使うので、sortを「追加空間$O(1)$」とはしません。

`key` は要素から比較用の値を1回ずつ作ります。タプルは左の項目から辞書順で比較されます。数値文字列は文字列のままだと `"10" < "2"` です。数として並べるなら整数に変換します。

### 昇順・降順・安定な複数キー

入力はN、N個の整数、N行の名前と得点。整数の昇順・降順、得点降順かつ名前昇順を出力します。同得点・同名なら入力順を維持します。キー計算と比較を定数時間とすると時間$O(N\log N)$、空間$O(N)$。長い文字列の比較には文字数も影響します。

```python
import sys
input = sys.stdin.readline
n = int(input())
a = list(map(int, input().split()))
records = []
for _ in range(n):
    name, score = input().split()
    records.append((name, int(score)))
print(*sorted(a))
a.sort(reverse=True)  # 元のリストを降順に変更
print(*a)
for name, score in sorted(records, key=lambda x: (-x[1], x[0])):
    print(name, score)
```

入力例：

```text
3
3 1 2
sora 80
aoi 90
ren 80
```

出力例：

```text
1 2 3
3 2 1
aoi 90
ren 80
sora 80
```

## 比較ソートを理解する

|手法|仕組み|最悪時間|補助空間|安定性|
|---|---|---|---|---|
|選択ソート|未処理の最小値を探して交換|$O(N^2)$|$O(1)$|通常は不安定|
|挿入ソート|整列済み部分の適切な位置に挿入|$O(N^2)$|$O(1)$|同値を追い越さなければ安定|
|マージソート|半分ずつ整列して併合|$O(N\log N)$|$O(N)$|同値で左を優先すれば安定|
|クイックソート|基準値で分割|$O(N^2)$（平均$O(N\log N)$）|実装次第、再帰深さは最悪$O(N)$|通常は不安定|

比較のみで一般のN要素を整列するには最悪$\Omega(N\log N)$の比較が必要です。値域が小さい整数なら計数ソートで$O(N+K)$時間・$O(N+K)$空間（出力込み）が可能です。値域Kが巨大なら使えません。

マージソートでは左右を整列した後、両方の先頭の小さい方を選びます。各段の併合は合計$O(N)$、段数は$O(\log N)$です。例 `[4, 1, 3, 2]` は `[1, 4]` と `[2, 3]` を作り、1→2→3→4の順で併合します。

### マージソート

入力はNとN個の整数。時間$O(N\log N)$、スライス・出力・再帰を含むピーク空間$O(N)$。再帰の深さは$O(\log N)$です。

```python
import sys

def merge_sort(a):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # 同値なら左を先にし、安定性を保つ
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

input = sys.stdin.readline
n = int(input())
a = list(map(int, input().split()))
print(*merge_sort(a))
```

入力例：

```text
4
4 1 3 2
```

出力例：

```text
1 2 3 4
```

### 座標圧縮

大小関係だけを残して、巨大な値を0始まりの順位に置き換えます。頻度配列やFenwick木の添字に使います。同じ値は同じ順位です。元の差や距離は保存されません。時間$O(N\log N)$、空間$O(N)$（辞書・集合の操作は平均）。

```python
import sys
input = sys.stdin.readline
n = int(input())
a = list(map(int, input().split()))
values = sorted(set(a))  # 重複を除き、元の値の昇順にする
rank = {value: i for i, value in enumerate(values)}
print(*(rank[x] for x in a))
```

入力例：

```text
5
100 5 100 -2 5
```

出力例：

```text
2 1 2 0 1
```

## よくある間違い

- `a = a.sort()` と書くとaがNoneになります。
- `reverse=True` はタプルの全項目を逆順にします。一部だけ降順なら数値キーを負にします。
- sortで入力順が失われると困る場合は `enumerate` で元の添字も保持します。
- 最大K個だけ欲しい場合は全ソートと `heapq.nlargest` を比較します。Kが小さいとヒープが有利です。
- 安定性は同じキーに対する性質です。別の項目もkeyに入れると、その項目で並べ替わります。

## 練習問題

- [abc088_b：降順に並べて交互に取る](https://atcoder.jp/contests/abc088/tasks/abc088_b)
- [abc132_c：中央値付近の境界](https://atcoder.jp/contests/abc132/tasks/abc132_c)
- [abc142_c：元の添字を保持して並べる](https://atcoder.jp/contests/abc142/tasks/abc142_c)

[目次へ](README.md)
