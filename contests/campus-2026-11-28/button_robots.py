import sys
input = sys.stdin.readline

N, C = map(int, input().split())
A = list(map(int, input().split()))

left = 0
right = 10**18

while right - left > 1:
    mid = (left + right) // 2
    cnt = sum(mid // a for a in A)

    if cnt >= C:
        right = mid
    else:
        left = mid

print(right)
