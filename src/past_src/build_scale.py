# -*- coding: utf-8 -*-
# 그룹 비중(예: 70/30)에 맞춰 소문항 배점을 정수로 배분
def scale_points(subj):
    """그룹별 비중(%)에 맞게 소문항 배점을 정수로 배분 (총 100점)"""
    groups = subj['groups']  # {'현대물리': 70, '회로': 30}
    allpts = []
    for g, share in groups.items():
        items = [(qi, si, s.get('w', 2)) for qi, q in enumerate(subj['qs']) if q['g'] == g
                 for si, s in enumerate(q['subs'])]
        tot = sum(w for _, _, w in items)
        raw = [share * w / tot for _, _, w in items]
        ints = [max(1, round(r)) for r in raw]
        diff = share - sum(ints)
        # 차이를 큰 문항부터 조정
        order = sorted(range(len(items)), key=lambda k: -(raw[k] - ints[k]) if diff > 0 else (raw[k] - ints[k]))
        k = 0
        while diff != 0 and order:
            idx = order[k % len(order)]
            if diff > 0:
                ints[idx] += 1; diff -= 1
            elif ints[idx] > 1:
                ints[idx] -= 1; diff += 1
            k += 1
        for (qi, si, _), p in zip(items, ints):
            subj['qs'][qi]['subs'][si]['p'] = p
    return subj

