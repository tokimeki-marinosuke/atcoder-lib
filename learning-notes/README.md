# AtCoder学習ノート — Python 3

[茶色→緑色向けの学習順](brown-to-green.md)では、連想配列・座標圧縮・累積和・二分探索を軸に、近い技術と組み合わせ方を案内しています。

制約から解法を選び、仕組みを理解してから実装するための参考書です。Python 3.12でコード例を実行確認しています。外部パッケージは不要です。既存のリポジトリ直下のREADMEとsorting/sort.mdは保持しています。

## 目次と学習順序

|順序|ノート|まず覚えること|次の段階|
|---|---|---|---|
|1|[計算量](09_complexity.md)|制約とループ回数|累積和・しゃくとり法|
|2|[ソート](01_sorting.md)|sort・sorted・key|安定性・座標圧縮・マージソート|
|3|[二分探索](02_binary_search.md)|bisectと境界|答えを二分探索|
|4|[データ構造](06_data_structures.md)|list・dict・set・deque|heapq・Union-Find・Fenwick木|
|5|[貪欲法](04_greedy.md)|選択の正当化|交換法による証明|
|6|[グラフ探索](05_graph.md)|隣接リスト・BFS・DFS|Dijkstra法|
|7|[動的計画法](03_dp.md)|状態・初期条件・遷移|ナップサック・区間DP・LIS|
|8|[数学](07_math.md)|GCD・素因数分解|篩・組合せ・逆元|
|9|[bit演算](08_bit.md)|集合を整数で表す|bit全探索・部分集合列挙|

問題で詰まったら「制約 → 必要な操作 → 計算量 → 境界ケース」の順に確認します。最小化なら無限大、数え上げなら0など、初期値の意味を説明できるようにしましょう。

## 読み方と実行

各Pythonコードブロックは独立したプログラムです。1つをmain.pyに保存し、対応する入力例を標準入力に渡してください。複数の例を連結しないでください。入力例は学習用で、リンク先問題の公式サンプルとは限りません。入力は各例の形式と制約を満たすものとします。

実行コマンドは `python3 main.py < input.txt` です。ノート中の空間計算量は、断りがなければ入力を保持する領域を含みます。整数演算は通常の競技プログラミングの範囲で定数時間とみなし、巨大整数は計算量ノートで補足します。

## 練習問題リンクの確認方法

AtCoder本体への接続が環境のネットワーク制限で拒否されたため、問題IDの存在は [AtCoder Problemsの初心者コース一覧](https://github.com/kenkoooo/AtCoderProblems/blob/master/atcoder-problems-frontend/public/static_data/courses/boot_camp_for_beginners.json) と [AtCoder公式ACLの問題一覧](https://github.com/atcoder/ac-library/blob/master/test/example/problems.toml) で確認しました（2026-11-07）。本体のHTTP応答は未確認です。問題IDを推測してリンクを追加しない方針です。
