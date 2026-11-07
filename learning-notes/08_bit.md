# bit演算・bit全探索

## 概要と使いどころ

N個の要素の選択状態をNビットの整数で表します。i番目のビットが1なら要素iを選択したと解釈します。小さいNの全探索、集合の合併・共通部分、状態圧縮に使います。

|式|意味|
|---|---|
|`mask & (1 << i)`|i番目が1か調べる|
|`mask \| (1 << i)`|i番目を1にする|
|`mask & ~(1 << i)`|i番目を0にする|
|`mask ^ (1 << i)`|i番目を反転|
|`a & b` / `a \| b`|共通部分 / 和集合|
|`a ^ b`|片方にだけ含まれる要素|
|`mask.bit_count()`|立っているビット数（Python 3.10以降）|

整数maskを0から$2^N-1$まで動かすと全ての部分集合を一度ずつ列挙できます。例えば3要素のmask=5は2進数101で、添字0と2を選びます。

### 部分集合和のbit全探索

入力はN SとN個の整数。和Sの部分集合数を出力。空集合も含みます。負数も扱えます。maskごとにNビット調べるので時間$O(N2^N)$、空間$O(N)$。Nは20程度までをまず目安にし、実測します。

```python
import sys
input = sys.stdin.readline
n, target = map(int, input().split())
a = list(map(int, input().split()))
answer = 0
for mask in range(1 << n):
    total = 0
    for i in range(n):
        if mask & (1 << i):
            total += a[i]
    if total == target:
        answer += 1
print(answer)
```

入力例：

```text
3 3
1 2 3
```

出力例：

```text
2
```

## 部分集合だけを列挙する仕組み

集合maskの非空部分集合subは `sub = (sub - 1) & mask` で次へ進めます。1を引いて下位ビットを変え、mask外のビットを落とすことで大きい順に列挙します。0からさらに進めるとmaskに戻るので終了判定が必要です。

### 指定した集合の全部分集合

入力は非負整数mask。空集合も最後に出力。kをmaskの立っているビット数とすると時間$O(2^k)$、通常の整数モデルで追加空間$O(1)$（出力は逐次）。

```python
mask = int(input())
sub = mask
while True:
    print(sub)
    if sub == 0:
        break  # 0の次に進むと元のmaskに戻ってしまう
    sub = (sub - 1) & mask
```

入力例：

```text
5
```

出力例：

```text
5
4
1
0
```

## 注意点

PythonのXORは `^`、べき乗は `**` です。ビットは0始まりです。`~mask` は負数にもなるため、Nビット内の補集合は `((1 << N) - 1) ^ mask` とします（maskがNビット内の場合）。全maskとその部分集合を二重に列挙すると合計$O(3^N)$回です。Pythonの整数は任意精度なので巨大なmaskの演算は定数時間ではありません。

順列を列挙したい場合は部分集合と異なり、`itertools.permutations`（$N!$通り）を使います。[DP](03_dp.md)の状態を集合にするbit DPも、この表現を使います。

## 練習問題

- [abc128_c：スイッチの状態を全探索](https://atcoder.jp/contests/abc128/tasks/abc128_c)
- [abc147_c：正直者の集合を全探索](https://atcoder.jp/contests/abc147/tasks/abc147_c)
- [abc147_d：XORをビットごとに数える](https://atcoder.jp/contests/abc147/tasks/abc147_d)

[目次へ](README.md)
