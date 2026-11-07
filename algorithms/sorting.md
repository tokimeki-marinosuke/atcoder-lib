# ソート：順序と比較条件を明確にする

## 基本と用途

順位づけ、中央値、処理順の整理に使います。詳しい仕組み・マージソート・座標圧縮は[既存のソートノート](../learning-notes/01_sorting.md)にまとめています。ここでは比較条件の設計を確認します。

|操作|意味|戻り値|
|---|---|---|
|`a.sort()`|元のリストを昇順に変更|`None`|
|`sorted(a)`|昇順の新しいリストを作る|新しいリスト|
|`sorted(a, reverse=True)`|降順の新しいリストを作る|新しいリスト|
|`sorted(a, key=...)`|各要素から作ったキーで比較|新しいリスト|

N要素の時間は最悪 $O(N\log N)$、組込みソートの追加空間は最悪 $O(N)$。`sort()`でも追加空間は定数ではありません。キーの計算・比較を定数時間とする見積もりです。

## 複数条件をタプルにする

「得票数が多い順、同票なら番号が小さい順」はキー `(-votes, candidate_id)` の昇順です。タプルは左から比較し、左が等しい場合に次の項目を比較します。

次のコードは単独で実行できます。候補者番号は1始まりです。

```python
votes = [2, 2, 1, 0]
ascending = sorted(votes)  # 元のvotesは変更しない
print(*ascending)
votes_copy = votes.copy()
votes_copy.sort(reverse=True)  # 元のコピーだけを降順に変更
print(*votes_copy)
order = sorted(range(1, len(votes) + 1),
               key=lambda i: (-votes[i - 1], i))
print(*order)  # 得票数降順、番号昇順
```

出力：

```text
0 1 2 2
2 2 1 0
1 2 3 4
```

`reverse=True`で全体を反転すると、同票の番号も降順になります。優先する条件ごとに方向を決めましょう。`a = a.sort()`とするとaはNoneになります。Pythonのソートは安定で、同じキーなら入力順を保ちますが、候補者番号が必要なら明示的にキーに入れる方が安全です。

## ABC483 Cとの関係

[ABC483 C](../contests/ABC483-C.md)では上位2候補だけが必要です。ソートでも前計算できますが $O(N\log N)$ かかります。[1回の走査で上位2候補を求める方法](../techniques/top-two-values.md)なら $O(N)$ です。全順位が要るか、上位数個だけでよいかを先に判断します。

関連：[同点処理](../techniques/tie-breaking.md)・[計算量](complexity.md)・[目次](../README.md)
