# 困りごとから探す索引

**技術名が分からないときは、問題を読んで困っている言葉から探してください。** 各行の「最初に試すこと」を手元の例で試し、詳しく知りたくなったら右の資料へ進みます。リンク先には、独立した技術ページだけでなく、問題の解説内の章も含みます。

- [1個動かす・AをBにする・両端は合う](#operation-and-comparison)
- [同じ結果を数えてしまう・何を1回と数えるか](#counting-and-duplicates)
- [区間・範囲・まとめて更新](#ranges-and-updates)
- [値や境界を探す・候補を選ぶ](#search-and-choice)
- [移動・つながり・依存関係・最適値](#graphs-and-states)
- [間に合わない・正しいか分からない](#complexity-and-correctness)

技術名が既に分かるときは[頻出技術の早見表](algorithms/common-techniques.md)、順に学ぶときは[茶色→緑色の学習順](learning-notes/brown-to-green.md)へ進めます。

<a id="operation-and-comparison"></a>

## 1. 1個動かす・AをBにする・両端は合う

検索語：カード、取り出して挿入、並べ替え、巡回シフト、ずれる、不一致、真ん中、不変量。

|困りごと・問題文の言葉|最初に試すこと → 考え方の名前|読む資料・場所|
|---|---|---|
|1個取り出して別の位置に入れると、どこが変わる？|短い配列を手で動かし、動く区間とずれる方向を書く → 操作の言い換え|[C：Move One Card](contests/C-Move-One-Card.md) の2・5・6章|
|配列Aを配列Bにできるか調べたい|最初と最後の不一致を囲む → 不一致区間への絞り込み|[C：Move One Card](contests/C-Move-One-Card.md) の2・5章（fir / fin）|
|両端は合うのに、判定が間違う・中央を見落とす|区間の中身も1つずつずれるか比較する → 区間全体の検証|[C：Move One Card](contests/C-Move-One-Card.md) の3・5章（反例とall）|
|操作しても、絶対に変えられないものはある？|値ごとの個数などを確認する → 不変量。移動だけでは個数は変わらないが、個数一致だけで十分とは限らない|[C：Move One Card](contests/C-Move-One-Card.md) の1・5章|

<a id="counting-and-duplicates"></a>

## 2. 同じ結果を数えてしまう・何を1回と数えるか

検索語：重複、異なる配列、種類数、操作数、結果の数、代表、正規化、一対一対応、連続する同じ値。

|困りごと・問題文の言葉|最初に試すこと → 考え方の名前|読む資料・場所|
|---|---|---|
|異なる操作なのに、同じ結果ができてしまう|同じ結果を並べ、1つだけ残す規則を探す → 正規化・代表の選択|[左移動の種類数（今回のDで使う考え方）](techniques/count-distinct-left-moves.md) の4・9章|
|操作数を数えたのに、答えの種類数と合わない|「結果1つにつき、代表がちょうど1つ」を説明する → 一対一対応|[左移動の種類数](techniques/count-distinct-left-moves.md) の1・9章|
|同じ数字が続くと、どの位置を数えればいい？|連続するかたまりの左端を代表にする。離れた同じ値は別に考える → 連続同値の代表化|[左移動の種類数](techniques/count-distinct-left-moves.md) の5章|
|同じ値の個数を引くと、なぜ結果の数になる？|まず重複しない代表を決め、その数を頻度で計算する → 頻度管理による数え上げ|[左移動の種類数](techniques/count-distinct-left-moves.md) の3・4・9章（cnt / ans）|
|同じ値が何回あるか、何組できるか知りたい|値ごとの出現数を持つ → Counter・頻度表|[連想配列・集合](techniques/hash-maps-and-sets.md) の「同じ値を選ぶ2要素の組数」|

<a id="ranges-and-updates"></a>

## 3. 区間・範囲・まとめて更新

検索語：連続区間、部分配列、区間和、長方形、更新、重なり、巨大座標。

|困りごと・問題文の言葉|最初に試すこと → 考え方の名前|読む資料|
|---|---|---|
|同じ配列の区間和を何度も足し直している|左からの合計を作り、右−左で答える → 累積和|[累積和・いもす法](techniques/prefix-sums-and-imos.md)|
|範囲内の全要素へ、何度も加算している|更新を終えてから読むなら両端だけ記録する → いもす法|[累積和・いもす法](techniques/prefix-sums-and-imos.md)|
|条件を満たす最長の連続区間が欲しい|右端を伸ばし、違反が消えるまで左端を進められるか考える → しゃくとり法|[しゃくとり・区間集計](techniques/sliding-window-and-counting.md)|
|負数も含む配列で、和がKの区間を数えたい|過去の累積和の出現回数を持つ → 累積和＋辞書|[しゃくとり・区間集計](techniques/sliding-window-and-counting.md)|
|重なった時間・範囲の総長が欲しい|開始位置順に見て重なるものを併合する → 区間マージ|[区間マージ](techniques/interval-merging.md)|
|座標や値が大きすぎて配列を作れない|大小関係だけで足りるか確認し、小さい順位へ変換する → 座標圧縮。距離は元の値で扱う|[座標圧縮](techniques/coordinate-compression.md)|
|配列の変更と区間集計が交互に来る|必要な演算を確認する → 区間和ならFenwick木、最小値などならセグメント木|[データ構造](learning-notes/06_data_structures.md)・[セグメント木](algorithms/segment-tree.md)|

<a id="search-and-choice"></a>

## 4. 値や境界を探す・候補を選ぶ

検索語：存在、出現位置、順位、何個まで、最小、最大、除外、同点。

|困りごと・問題文の言葉|最初に試すこと → 考え方の名前|読む資料|
|---|---|---|
|毎回、配列の中を探している|存在だけか、個数や位置も必要かを分ける → set・dict・逆引き|[連想配列・集合](techniques/hash-maps-and-sets.md)|
|ある値以上・以下、予算内で何個までか知りたい|順序や判定が単調かを確認する → ソート・二分探索・累積和との組み合わせ|[ソート](algorithms/sorting.md)・[二分探索](learning-notes/02_binary_search.md)|
|1位を除外した後の最大値を毎回探している|元の1位と2位を保持する → 上位2要素|[最大値と2番目の最大値](techniques/top-two-values.md)|
|一部の候補だけ変わるのに全員を再計算している|基準状態を持ち、変更先だけ見る条件を確認する → 差分更新・復元|[差分更新](techniques/partial-updates.md)・[ABC483 C](contests/ABC483-C.md)|
|同点のときに答えが変わる|優先条件を順番に並べる → タプル比較・同点処理|[同点処理](techniques/tie-breaking.md)|
|最小値・最大値を取り出し続けたい|先頭だけを素早く管理する → ヒープ|[データ構造](learning-notes/06_data_structures.md)|

<a id="graphs-and-states"></a>

## 5. 移動・つながり・依存関係・最適値

|困りごと・問題文の言葉|最初に試すこと → 考え方の名前|読む資料|
|---|---|---|
|マス目や街を、最小何回で移動できる？|全ての移動コストが1なら近い順に探索する → BFS|[グラフ探索](learning-notes/05_graph.md)|
|道ごとに移動コストが違う|非負重みか確認し、暫定距離の小さい順に処理する → Dijkstra|[グラフ探索](learning-notes/05_graph.md)|
|道を追加しながら、同じグループか調べたい|連結成分をまとめる → Union-Find|[データ構造](learning-notes/06_data_structures.md)|
|前提作業があり、処理順が分からない|前提が残っていない作業から処理する → トポロジカルソート|[グラフの典型](algorithms/graph-patterns.md)|
|同じ部分問題を何度も解いている|状態・初期値・遷移を決めて答えを再利用する → DP|[DPの入口](algorithms/dynamic-programming.md)・[DP詳説](learning-notes/03_dp.md)|
|よさそうなものから選んでいいか分からない|その選択へ交換しても損しないか説明する → 貪欲法・交換法|[貪欲法](learning-notes/04_greedy.md)|
|同じ移動を大量に繰り返す・木の2点距離が欲しい|2のべき乗回の移動を前計算する → ダブリング・LCA|[木とダブリング](algorithms/tree-and-doubling.md)|
|文字の連続やパターンの出現を調べたい|連続区間の集約か、一致位置の探索かを分ける → ランレングス・Z-algorithm|[文字列処理](algorithms/string-patterns.md)|
|約数・倍数・素数・大きな数の余りを扱う|整数の性質で調べる数を減らす → GCD・篩・剰余|[数学](learning-notes/07_math.md)|

<a id="complexity-and-correctness"></a>

## 6. 間に合わない・正しいか分からない

|困りごと|最初に試すこと → 考え方の名前|読む資料・場所|
|---|---|---|
|二重ループなので無理だと思ったが、各要素は数回しか見ていない|内側の長さの総和を数える → 計算量の合計評価|[計算量](algorithms/complexity.md)・[ABC483 C](contests/ABC483-C.md)|
|本当にこの候補だけ調べて十分？|省いた候補が勝てない理由・区間を縮められる理由を説明する → 正しさの証明|[差分更新](techniques/partial-updates.md)・[C：Move One Card](contests/C-Move-One-Card.md) の6章|
|実装は動いたが、自信がない|小入力で全操作を試し、速い解法と照合する → 愚直解による検証|[C：Move One Card](contests/C-Move-One-Card.md) の8章・[左移動の種類数](techniques/count-distinct-left-moves.md) の7章|
|全パターンを試してよい制約か分からない|候補数と1候補の処理量を掛ける → 全探索・bit全探索の見積もり|[計算量](learning-notes/09_complexity.md)・[bit全探索](learning-notes/08_bit.md)|

## 今後の教材を追加するとき

1. 「何という技術か」より先に、**どんな言葉で困っていたか**を1つ以上選びます。
2. 既存の行に当てはまる場合は、その行の資料欄に対応する教材・読む章を追記します。行がない場合だけ、適切な分類に追加します。
3. 新しい教材からこの索引へ戻れるリンクも付けます。既存教材の移動・改名や一斉改稿は不要です。
4. 技術の名前だけ並べず、「最初に試すこと」と成立条件を短く添えます。詳細解説はリンク先に置き、ここには重複して書きません。
5. リンク先が実在し、案内する考え方がそのページに書かれていることを確認します。独立ページがない考え方は、今回のように問題教材の該当章へ案内します。

[READMEへ戻る](README.md)
