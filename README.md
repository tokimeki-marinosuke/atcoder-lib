# atcoder-lib
自分用atcoderで問題を解くときに役立つ知識詰め合わせセット

## 問題を解くときの入口

[AtCoder・競技プログラミングの頻出技術 早見表](algorithms/common-techniques.md)に、問題の特徴から使う技術を選ぶ表と学習順序をまとめています。まず制約・更新の有無・単調性などを確認し、各解説へ進んでください。

**茶色から緑色を目指す方へ：** [基礎4項目と組み合わせの学習順](learning-notes/brown-to-green.md)を用意しています。[連想配列](techniques/hash-maps-and-sets.md) → [座標圧縮](techniques/coordinate-compression.md) → [累積和](techniques/prefix-sums-and-imos.md) → [二分探索](learning-notes/02_binary_search.md)の順に、使い分けと境界条件を確認できます。

## 図から読む

各解説の冒頭の「図でつかむ」で、**何をしたいか → 何を変えるか → 何が得られるか**を確認できます。図の具体例を見てから、本文の成立条件・計算量・実装へ進んでください。図はGitHub標準のMermaid表示に対応し、値や操作も文字で併記しています。

|つかみたいイメージ|図のある資料|
|---|---|
|問題の特徴から手法を選ぶ|[技術の入口マップ](algorithms/common-techniques.md)|
|区間の両端だけを変える|[いもす法](techniques/prefix-sums-and-imos.md)|
|窓を伸ばして、条件違反を取り除く|[しゃくとり](techniques/sliding-window-and-counting.md)|
|更新した葉から根まで値を直す|[セグメント木](algorithms/segment-tree.md)|
|小さい問題の答えを足して次へ進む|[階段DP](learning-notes/03_dp.md)|
|辞退者の票だけ動かして戻す|[ABC483 C](contests/ABC483-C.md)|

## 目的と資料の使い方

AtCoderで学んだアルゴリズムや、解けなかった問題から得た考え方を蓄積する、自分用のPython 3参考書です。問題固有の記録と再利用できる知識を分け、相互リンクで復習できるようにします。既存の[学習ノート総目次](learning-notes/README.md)も利用できます。

## アルゴリズム一覧

|資料|主な内容|
|---|---|
|[ソート](algorithms/sorting.md)|sort・sorted・key・複数条件の順位|
|[動的計画法](algorithms/dynamic-programming.md)|状態・初期条件・遷移・フィボナッチ・ナップサック|
|[計算量](algorithms/complexity.md)|NとMの違い・二重ループの総処理回数|
|[セグメント木](algorithms/segment-tree.md)|1点変更・区間最小値・成立する演算|
|[グラフの典型](algorithms/graph-patterns.md)|トポロジカルソート・Warshall–Floyd・Kruskalの考え方|
|[木とダブリング](algorithms/tree-and-doubling.md)|K回移動・最小共通祖先LCA・木の距離|
|[文字列処理](algorithms/string-patterns.md)|標準機能・ランレングス圧縮・Z-algorithm|

詳細解説は既存の[ソート](learning-notes/01_sorting.md)・[DP](learning-notes/03_dp.md)・[計算量](learning-notes/09_complexity.md)を参照します。ほかに[二分探索](learning-notes/02_binary_search.md)・[貪欲法](learning-notes/04_greedy.md)・[グラフ](learning-notes/05_graph.md)・[データ構造](learning-notes/06_data_structures.md)・[数学](learning-notes/07_math.md)・[bit演算](learning-notes/08_bit.md)があります。

## テクニック一覧

|資料|主な内容|
|---|---|
|[最大値と2番目の最大値](techniques/top-two-values.md)|同率を含む上位2要素・1要素の除外|
|[差分更新](techniques/partial-updates.md)|変更先だけの比較・復元・成立条件|
|[同点処理](techniques/tie-breaking.md)|タプル比較・min/max/sorted・境界テスト|
|[累積和・いもす法](techniques/prefix-sums-and-imos.md)|2次元累積和・区間加算の一括処理|
|[しゃくとり・区間集計](techniques/sliding-window-and-counting.md)|重複禁止の窓・累積和と頻度辞書|
|[連想配列・集合](techniques/hash-maps-and-sets.md)|dict・Counter・defaultdict・set、出現位置と二分探索|
|[座標圧縮](techniques/coordinate-compression.md)|順位への変換・元の値への復元・使い分け|
|[区間マージ](techniques/interval-merging.md)|和集合・被覆長・いもすや貪欲との違い|
|[1要素を左へ移動した結果の種類数](techniques/count-distinct-left-moves.md)|数え上げ・頻度管理・連続同値の代表化・正規化による重複除去|

## コンテスト振り返り一覧

|資料|学んだこと|
|---|---|
|[ABC483 C — Second Choice Election](contests/ABC483-C.md)|上位2候補、票の差分更新、全体でO(N+M)となる根拠|
|[C — Move One Card](contests/C-Move-One-Card.md)|最初・最後の不一致fir/finと、区間全体の左右1つずれの判定|

## 今後の追加方法

1. `contests/ABCxxx-X.md` に、問題概要・制約・当時の方針・不足していた考え方・正解法と計算量・解答例・正しさ・境界条件・学び・関連リンクを記録します。
2. 公式問題文を確認し、提出コードがなければ推測で再現しません。ユーザー共有の本文などを用いた場合は出典と確認範囲を明記します。
3. 再利用できる知識は既存の `algorithms/`・`techniques/`・`learning-notes/` を探して追記し、同じ解説の重複を避けます。
4. 問題記録と技術資料を相互リンクし、この目次にも追加します。コードを単独で実行し、同点・最小入力などを検証します。

各Pythonコードブロックは独立したプログラムです。入力を読む例は `python3 main.py < input.txt` で実行できます。固定データを含む例は `python3 main.py` で実行してください。

計算量や式は、数式表示の機能がない画面でも読める通常の文字で記載しています。長い式はテキスト欄に分け、特殊な記号には本文で意味を補足します。

今回追加した頻出技術のコード例と参照解との比較は、リポジトリ直下で `python3 -m unittest discover -s tests -v` を実行すると再検証できます。外部パッケージは不要です。
