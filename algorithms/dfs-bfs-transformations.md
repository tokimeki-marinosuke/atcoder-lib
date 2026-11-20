# DFS・BFSのコード変形帳：どの行を、なぜ変えるか

完成コードは[基礎](../learning-notes/05_graph.md)・[実践](dfs-bfs-patterns.md)・[発展](dfs-bfs-advanced.md)・[状態BFS](dfs-bfs-states.md)・[マッチング](bipartite-matching.md)に置き、このページは**変更箇所の比較**に集中します。下のdiffは差分の抜粋で、単独実行するプログラムではありません。`-`は変更前、`+`は変更後です。

## 0. まず変える場所を5つに分ける

|場所|問い|
|---|---|
|状態の入れ物|dist/seenの添字は、番号・座標・複数変数のどれ？|
|初期化|始点は1個？ 複数？ 初期状態の値は？|
|取り出し口|FIFOならpopleft、LIFOならpop。重み付きならどう並べる？|
|隣接先の生成|入力の辺？ 4近傍？ 鍵や方向の条件？|
|登録と終了|未発見か、距離の改善か、経路を戻すのか？ 答えをどこで取得する？|

## 1. 到達判定 → 最短距離

到達判定をBFSで書いた場合の差分です。変えるのは「印の配列」「未発見の判定」「発見時の登録」です。DFSで書いていた場合は取り出し順もFIFOへ変える必要があります。

```diff
-seen = [False] * V
-seen[start] = True
+dist = [-1] * V
+dist[start] = 0

-if not seen[y]:
-    seen[y] = True
+if dist[y] == -1:
+    dist[y] = dist[x] + 1
     queue.append(y)
```

単に変数名を変えるのではなく、発見時に親の距離+1を保存します。各辺が1であることを確認してください。[完成例](../learning-notes/05_graph.md)

## 2. 最短距離 → 経路復元

発見・距離の更新と**同じ場所**で親を保存します。最後に距離だけ出す処理へ、目標から親をたどる処理を追加します。

```diff
 dist = [-1] * V
+prev = [-1] * V

 if dist[y] == -1:
     dist[y] = dist[x] + 1
+    prev[y] = x
     queue.append(y)
```

```text
未到達なら復元しない
current = goal
current != -1 の間、経路へ追加して current = prev[current]
最後に経路を逆順にする
```

親を毎回上書きせず、最短の発見時だけ保存するのがポイントです。座標ならprevにも前の座標、鍵付きなら前の鍵を含む状態全体を保存します。[完成例](dfs-bfs-patterns.md#path)

## 3. 単一始点 → 複数始点

変えるのは初期化だけです。後のwhileループは同じにできます。

```diff
-dist[start] = 0
-queue = deque([start])
+queue = deque()
+for start in sources:
+    if dist[start] == -1:
+        dist[start] = 0
+        queue.append(start)
```

全始点が同じ時刻に出発するから同じ距離0です。各始点ごとにdistを初期化してBFSし直す必要はありません。[完成例](dfs-bfs-patterns.md#multi-source)

## 4. 頂点番号 → 二次元座標

状態・配列の次元・隣接先の生成・登録する値がセットで変わります。

```diff
-dist = [-1] * V
+dist = [[-1] * W for _ in range(H)]

-x = queue.popleft()
-for y in g[x]:
+r, c = queue.popleft()
+for dr, dc in directions:
+    nr, nc = r + dr, c + dc
+    if not (0 <= nr < H and 0 <= nc < W):
+        continue

-    dist[y] = dist[x] + 1
-    queue.append(y)
+    dist[nr][nc] = dist[r][c] + 1
+    queue.append((nr, nc))
```

実際には未発見・壁の判定も必要です。この差分だけを貼り付けず、次の条件を追加します。[座標の完成例](dfs-bfs-patterns.md#grid)

## 5. 障害物のあるグリッドへ

座標の範囲を確かめた後、**登録する前**に通れるか確認します。範囲外チェックより先にboardを読まないようにします。

```diff
 if not (0 <= nr < H and 0 <= nc < W):
     continue
+if board[nr][nc] == '#':
+    continue
 if dist[nr][nc] == -1:
     dist[nr][nc] = dist[r][c] + 1
```

「壁を1回壊せる」なら常に壁を飛ばすのではなく、壊した回数を状態へ追加します。次の鍵付きと同じ考え方です。

## 6. 二次元座標 → 位置＋鍵の三次元状態

変更はvisitedの次元だけでは終わりません。キューの要素、扉判定、取得後の状態、初期化、ゴールの取り出し方も変えます。

```diff
-dist = [[-1] * W for _ in range(H)]
-dist[sr][sc] = 0
-queue = deque([(sr, sc)])
+dist = [[[-1] * 2 for _ in range(W)] for _ in range(H)]
+dist[sr][sc][0] = 0
+queue = deque([(sr, sc, 0)])

-r, c = queue.popleft()
+r, c, key = queue.popleft()

+if cell == 'A' and key == 0:
+    continue
+new_key = int(key == 1 or cell == 'a')
-if dist[nr][nc] == -1:
-    dist[nr][nc] = dist[r][c] + 1
-    queue.append((nr, nc))
+if dist[nr][nc][new_key] == -1:
+    dist[nr][nc][new_key] = dist[r][c][key] + 1
+    queue.append((nr, nc, new_key))
```

新しい状態への変換を先に済ませ、変換後の添字で未訪問を確認します。キーが違えば同じ座標も別の頂点です。[完成例](dfs-bfs-states.md#key-state)

## 7. 通常DFS → バックトラッキング

同じ頂点の先を全体で1回だけ調べるか、**経路が違えば再び調べるか**が違いです。

```diff
-seen[x] = True
+on_path[x] = True
 for y in g[x]:
-    if not seen[y]:
+    if not on_path[y]:
         dfs(y)
+on_path[x] = False
```

取り消しは帰りがけです。目標で途中returnするなら取り消しを忘れない構造にします。到達性の問題でこの変更を行うと、不要な経路全探索になって遅くなります。[完成例](dfs-bfs-advanced.md#backtracking)

## 8. 通常DFS → 二部マッチングのDFS

見た目はdfsでも、探索する遷移と、成功して戻るときの処理が変わります。

```diff
-for y in g[u]:
-    if not seen[y]:
-        dfs(y)
+for v in adj[u]:
+    other = pair_right[v]
+    if other == -1 or dfs(other):
+        pair_right[v] = u
+        return True
```

上は核心部分の差分です。実際には各増加道探索のstampを使ったseen判定も必要です。`dfs(other)` は「すでにその右頂点を使っている人へ、別の候補を探してもらう」処理。奥の成功が返ってから、手前のペアを変更します。seenの意味は1回の増加道探索の訪問済みであり、単純パス全列挙のon_pathとは異なります。[基本法の完成例](bipartite-matching.md#basic-matching)

## 9. 通常BFS → 0-1 BFS

未訪問だけでなく、距離が改善されるかを判定します。0の辺は先頭、1の辺は末尾へ入れます。

```diff
-if dist[y] == -1:
-    dist[y] = dist[x] + 1
-    queue.append(y)
+nd = dist[x] + cost
+if nd < dist[y]:
+    dist[y] = nd
+    if cost == 0:
+        queue.appendleft((nd, y))
+    else:
+        queue.append((nd, y))
```

初期値は未到達を無限大にし、取り出し側も(登録時距離,頂点)へ合わせます。古い候補を捨てる処理まで含めた[完成例](dfs-bfs-states.md#zero-one)を確認してください。

## 演習

**Level 3：鍵付きBFSに経路復元を追加すると、prevの次元と値は何にする？**

<details markdown="1"><summary>ヒント</summary>

同じ座標へ鍵なしで来た親と、鍵ありで来た親は区別できる必要があります。

</details>

<details markdown="1"><summary>解説</summary>

distと同じH×W×2のprevを用意し、新しい状態を発見したときに親の(r,c,key)を保存します。最初に取り出したゴールの鍵状態から始点状態まで戻ります。親の座標だけを保存すると鍵取得前後の状態を復元できません。

</details>

[困りごと索引へ](../problem-solving-index.md)・[コースの目次へ](../learning-notes/graph-search-roadmap.md)
