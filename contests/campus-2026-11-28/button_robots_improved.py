# ngは未達、okは到達済みという条件を維持する整理版。
import sys
input = sys.stdin.readline
N, C = map(int, input().split())
A = list(map(int, input().split()))
ng = 0
ok = min(A) * C  # 最速の1台だけでもC回押し終わる
while ok - ng > 1:
    mid = (ng + ok) // 2
    if sum(mid // a for a in A) >= C:
        ok = mid
    else:
        ng = mid
print(ok)
