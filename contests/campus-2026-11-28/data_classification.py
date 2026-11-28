import sys
input = sys.stdin.readline

N = int(input())
array = []

for _ in range(N):
    array.append(list(map(int, input().split())))

x0, y0 = map(int, input().split())

for i in range(N):
    a, b, c = array[i]
    array[i] = [(a-x0)**2 + (b-y0)**2, c]

array.sort()

q = int(input())
array2 = {}
ans = []

for i in range(N):
    c = array[i][1]
    array2[c] = 0

max_cnt = 0
best_class = 0

for i in range(N):
    c = array[i][1]
    array2[c] += 1

    if max_cnt < array2[c]:
        max_cnt = array2[c]
        best_class = c

    if max_cnt == array2[c]:
        best_class = min(best_class, c)

    ans.append(best_class)

for i in range(q):
    k = int(input())
    print(ans[k-1])
