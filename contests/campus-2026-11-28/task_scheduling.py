import sys
input = sys.stdin.readline

N = int(input())
A = []

for _ in range(N):
    A.append(list(map(int, input().split())))

A.sort(key=lambda x: x[1])

temp = 0
cnt = 0

for s, t in A:
    if temp < s:
        cnt += 1
        temp = t

print(cnt)
