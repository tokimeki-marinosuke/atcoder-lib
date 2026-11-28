# 元のACコードとは別の整理版。オンラインジャッジには未提出。
from collections import defaultdict
import sys
input = sys.stdin.readline
N = int(input())
points = [tuple(map(int, input().split())) for _ in range(N)]
x0, y0 = map(int, input().split())
ordered = sorted(((x - x0) ** 2 + (y - y0) ** 2, c) for x, y, c in points)
q = int(input())
freq = defaultdict(int)
ans = []
max_cnt = 0
best_class = None
for _, c in ordered:
    freq[c] += 1  # 変化したクラスだけを比較する
    if freq[c] > max_cnt:
        max_cnt = freq[c]
        best_class = c
    elif freq[c] == max_cnt:
        best_class = min(best_class, c)
    ans.append(best_class)
for _ in range(q):
    k = int(input())
    print(ans[k - 1])
