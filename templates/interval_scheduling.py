def select_intervals(intervals, *, closed=True):
    """s < t の区間から最大個数を選ぶ。closed=Falseなら半開区間。"""
    selected = []
    last_end = None
    for s, t in sorted(intervals, key=lambda interval: interval[1]):
        # 閉区間は端点の共有も重複。半開区間は端点を共有できる。
        fits = last_end is None or (last_end < s if closed else last_end <= s)
        if fits:
            selected.append((s, t))
            last_end = t
    return selected
