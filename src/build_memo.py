# builds docs/memo.html (반복 학습 · 암기 퀴즈) + docs/memo_data.js
# input: QS, FIG, SRC from build_site.py (exec'd there) + memo/bio_bank.json
import json, os, re
MD = os.path.join(HERE, 'memo')
bio = json.load(open(os.path.join(MD, 'bio_bank.json'), encoding='utf-8'))
SUBN = {'phys': '물리', 'chem': '화학', 'bio': '생명과학', 'earth': '지구과학'}
ORDER = ['phys', 'chem', 'bio', 'earth']
subjects = {s: {'id': s, 'name': SUBN[s], 'sections': []} for s in ORDER}
bank = []
secids = {s: {} for s in ORDER}
# 1) memorization bank (bio)
for sj in bio['SUBJECTS']:
    for sec in sj['sections']:
        subjects['bio']['sections'].append({'id': sec['id'], 'name': '[암기] ' + sec['name']})
for b in bio['BANK']:
    bank.append(b)
# 2) site questions -> same engine
def sec_of(s, u):
    m = secids[s]
    if u not in m:
        m[u] = 'u%d' % len(m)
        subjects[s]['sections'].append({'id': m[u], 'name': '[문제] ' + u})
    return m[u]
def srcname(q):
    r = (q.get('ref') or [''])[0].split(':')[0]
    return SRC.get(r, {}).get('short', '사이트 문제')
def srcfull(q):
    out = []
    for r in q.get('ref') or []:
        k, p = r.split(':')
        out.append(SRC.get(k, {}).get('short', k) + ' p' + p)
    return ', '.join(out)
used_figs = set()
for q in QS:
    s, t = q['s'], q['t']
    if t == 'essay' or q.get('col'): continue
    sec = sec_of(s, q.get('u') or '기타')
    base = dict(subj=s, sec=sec, sub=srcname(q), src=srcfull(q), raw=True)
    if q.get('fig'): base['fig'] = q['fig']; used_figs.add(q['fig'])
    if q.get('tb'): base['tb'] = q['tb']
    if t == 'mc':
        ex = q.get('ex', '')
        cx = q.get('cx') or []
        if cx:
            ex = (ex + '<br>' if ex else '') + '<span class="cxl">' + '<br>'.join(f'{"①②③④⑤⑥"[i]} {c}' for i, c in enumerate(cx)) + '</span>'
        bank.append(dict(base, id='site/' + q['id'], k='site/' + q['id'], type='mc', q=q['q'], choices=q['c'], answer=int(q['a']), exp=ex))
    elif t == 'num':
        bank.append(dict(base, id='site/' + q['id'], k='site/' + q['id'], type='sa', q=q['q'] + (f' (단위: {q["unit"]})' if q.get('unit') else ''),
                         answer=float(q['a']), tol=float(q.get('tol') or abs(float(q['a'])) * 0.02 + 1e-9), unit=q.get('unit', ''), exp=q.get('ex', '')))
    elif t == 'txt':
        a = q['a'] if isinstance(q['a'], list) else [q['a']]
        bank.append(dict(base, id='site/' + q['id'], k='site/' + q['id'], type='sa', q=q['q'], answer=a[0], alts=a[1:], exp=q.get('ex', '')))
    elif t == 'set':
        for j, p in enumerate(q.get('parts', [])):
            pid = f"site/{q['id']}-{j+1}"
            stem = f"{q['q']}<br><b>({j+1})</b> {p['p']}"
            if p['t'] == 'num':
                a = float(p['a']); tol = float(p.get('tol') or abs(a) * 0.02 + 1e-9)
                bank.append(dict(base, id=pid, k=pid, type='sa', q=stem + (f' (단위: {p["unit"]})' if p.get('unit') else ''), answer=a, tol=tol, unit=p.get('unit', ''), exp=p.get('sol', '')))
            elif p['t'] == 'txt':
                a = p['a'] if isinstance(p['a'], list) else [p['a']]
                bank.append(dict(base, id=pid, k=pid, type='sa', q=stem, answer=a[0], alts=a[1:], exp=p.get('sol', '')))
SUBJECTS = [subjects[s] for s in ORDER]
FIGM = {k: FIG[k] for k in used_figs if k in FIG}
open(os.path.join(SITE, 'memo_data.js'), 'w', encoding='utf-8').write(
    'const SUBJECTS=' + json.dumps(SUBJECTS, ensure_ascii=False) + ';\nconst BANK=' + json.dumps(bank, ensure_ascii=False) + ';\nconst FIGM=' + json.dumps(FIGM, ensure_ascii=False) + ';')
head = open(os.path.join(MD, 'head.html'), encoding='utf-8').read()
head = head.replace('<title>암기 퀴즈</title>', '<title>반복 학습 · 암기 퀴즈 | 1-2 기말 복습</title><script src="katex.min.js"></script><script src="auto-render.min.js"></script>')
head = head.replace('</style>', '''.backlink{display:inline-block;font-size:13px;color:var(--accent);text-decoration:none;margin:2px 0 4px}
.figbox{margin:6px 0 10px;text-align:center}.figbox svg{max-width:100%;height:auto}
table.t{border-collapse:collapse;margin:8px auto;font-size:14px}table.t td,table.t th{border:1px solid var(--line);padding:4px 8px;text-align:center}
.bogi{border:1px solid var(--line);border-radius:10px;padding:8px 10px;margin:8px 0;font-size:15px}.bogi .bt{text-align:center;font-weight:700;margin-bottom:4px}
.cxl{display:block;margin-top:6px;font-size:.93em;opacity:.9}
math{font-size:1.04em}
</style>''')
app = open(os.path.join(MD, 'app.js'), encoding='utf-8').read()
html = head + '<body>\n<div id="app"></div>\n<script src="memo_data.js"></script>\n<script>\n' + app + '\n</script>\n</body>\n</html>\n'
open(os.path.join(SITE, 'memo.html'), 'w', encoding='utf-8').write(html)
from collections import Counter
print('MEMO', len(bank), Counter((b['subj'], b['type']) for b in bank), 'KB', os.path.getsize(os.path.join(SITE, 'memo_data.js')) / 1e3)
