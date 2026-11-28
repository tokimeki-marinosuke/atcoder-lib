from collections import defaultdict


def prefix_modes(classes):
    """各接頭辞の最頻値。同率なら小さい整数を返す。空入力は空リスト。"""
    freq = defaultdict(int)
    answers = []
    max_count = 0
    best_class = None
    for c in classes:
        freq[c] += 1
        if freq[c] > max_count:
            max_count = freq[c]
            best_class = c
        elif freq[c] == max_count:
            best_class = min(best_class, c)
        answers.append(best_class)
    return answers
