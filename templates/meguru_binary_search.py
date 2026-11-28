def first_true(ng, ok, is_ok):
    """整数の単調なFalse→True判定の境界。ngはFalse、okはTrueを渡す。"""
    if ng >= ok:
        raise ValueError("ng < ok が必要です")
    while ok - ng > 1:
        mid = (ng + ok) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok
