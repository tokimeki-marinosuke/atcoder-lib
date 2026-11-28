# 復習仕様を負の重みにも拡張した版。公式に負値があるという意味ではない。
import sys
input = sys.stdin.readline
N, M, Q = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(M)]
members = [False] * (N + 1)
for _ in range(Q):
    op, x = input().split()
    members[int(x)] = op == "+"
ans = None  # 未発見と、重み0や負の重みを区別する
for a, b, w in edges:
    if members[a] != members[b] and (ans is None or w > ans):
        ans = w
print(0 if ans is None else ans)
