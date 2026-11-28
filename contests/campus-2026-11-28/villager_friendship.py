import sys
input = sys.stdin.readline

N, M, Q = map(int, input().split())

edges = []
for _ in range(M):
    a, b, w = map(int, input().split())
    edges.append((a, b, w))

members = [False] * (N + 1)

for _ in range(Q):
    op, x = input().split()
    x = int(x)
    members[x] = op == "+"

ans = 0

for a, b, w in edges:
    if members[a] != members[b]:
        ans = max(ans, w)

print(ans)
