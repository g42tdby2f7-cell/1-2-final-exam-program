# -*- coding: utf-8 -*-
"""임용·MEET·DEET·PEET 기출 변형 문항 → ../x_past.yaml + ../past_figs.json
원본 시험지 데이터: past_src/{phys,chem,bio,earth}.py (모의고사 PDF와 같은 데이터)
"""
import os, re, sys, json, importlib, yaml
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)

SUBS = {'_0': '₀', '_1': '₁', '_2': '₂', '_3': '₃', '_a': 'ₐ', '^2': '²', '^3': '³', '^{-1}': '⁻¹', '\\phi': 'φ', '\\lambda': 'λ',
        '\\theta': 'θ', '\\vec ': '', "\\'": '′', "'": '′', '\\,': ' ', '\\mathrm': '', '{': '', '}': ''}
def _conv(m):
    t = m.group(1)
    for k, v in SUBS.items(): t = t.replace(k, v)
    return '<tspan font-style="italic">' + t + '</tspan>'
def svgmath(svg): return re.sub(r'\$([^$]+)\$', _conv, svg)

def plain(s):
    """q·p 필드는 화면에서 escape되므로 태그 제거"""
    s = s.replace('<br>', '\n')
    s = re.sub(r'</?(b|span|i)[^>]*>', '', s)
    return s.replace('&lt;', '<').replace('&gt;', '>').strip()

def kps(ans):
    items = [plain(x) for x in re.split(r'<br>', ans) if plain(x)]
    return items

# 자동 채점 단답(수치): (과목, 문항 번호, 소문항 번호) -> (값, 단위, 허용 오차)
NUM = {
 ('phys', 1, 1): (2.7, 'eV', .02), ('phys', 1, 2): (3.3, 'V', .02), ('phys', 6, 1): (0.6, 'c', .02), ('phys', 6, 3): (5, '초', .02),
 ('phys', 9, 2): (0.8, 'MeV', .03), ('phys', 12, 1): (0.10, 'nm', .05), ('phys', 12, 2): (0.10, 'nm', .05), ('phys', 13, 1): (9, '배', .01),
 ('phys', 15, 1): (496, 'nm', .02), ('phys', 17, 1): (413, 'nm', .02), ('phys', 20, 2): (6.4, '×10⁻³⁴ J·s', .03),
 ('chem', 3, 3): (-1215, 'kJ/mol', .01), ('chem', 8, 2): (-137, 'atm/K', .03), ('chem', 9, 2): (0.17, 'mol', .06),
 ('chem', 11, 1): (40, 'J/(K·mol)', .01), ('chem', 11, 2): (12.8, 'J/K', .03), ('chem', 11, 3): (40.6, 'kJ', .02),
 ('chem', 19, 2): (0.57, 'm³', .03), ('chem', 19, 3): (4150, 'J', .01), ('chem', 20, 1): (0.004, 'atm/K', .03), ('chem', 20, 2): (0.015, 'L/K', .03),
 ('bio', 17, 2): (8, '배', .01),
 ('earth', 2, 1): (4, '배', .01), ('earth', 2, 2): (11.3, '등급', .01), ('earth', 3, 2): (0.54, '등급', .06), ('earth', 4, 3): (5.5, '등급', .02),
 ('earth', 5, 2): (70, 'km/s/Mpc', .02), ('earth', 9, 1): (10.8, '배', .02), ('earth', 12, 3): (9, '', .01), ('earth', 14, 1): (8.5, '등급', .02),
 ('earth', 14, 2): (0.05, '″', .05), ('earth', 16, 1): (-500, 'km/s', .02), ('earth', 17, 2): (3, '', .01), ('earth', 20, 2): (3, 'R', .01),
}
NUM.update({
 ('mbio', 3, 2): (32, '배', .01), ('mchem', 1, 3): (8.97, 'g/cm³', .02), ('mchem', 5, 1): (1.5, '배', .01), ('mchem', 5, 2): (1.22, '', .02),
 ('mchem', 12, 1): (-106, 'kJ/mol', .01), ('mchem', 14, 1): (-267, 'kJ/mol', .01),
 ('mchem', 17, 3): (27.5, 'kJ', .02), ('mchem', 19, 1): (53, 'kJ/mol', .01), ('mchem', 20, 1): (428, 'kJ/mol', .01),
})
TXT = {('mbio', 13, 1): ['알라닌', 'Ala', 'alanine'], ('bio', 15, 1): ['ACCGTAATCG', "5'-ACCGTAATCG-3'"], ('bio', 15, 3): ['ddATP', 'ddA', 'A']}

KIND = {'임용': '임용', 'MEET': 'MEET', 'DEET': 'DEET', 'PEET': 'PEET'}
NAME = {'phys': '물리', 'chem': '화학', 'bio': '생물', 'earth': '지구과학'}
out, figs = [], {}
import build_scale
MODS = [('phys', 'phys', 'xp_'), ('chem', 'chem', 'xp_'), ('bio', 'bio', 'xp_'), ('earth', 'earth', 'xp_'),
        ('phys', 'm_phys', 'xm_'), ('chem', 'm_chem', 'xm_'), ('bio', 'm_bio', 'xm_')]
for s, modname, pre in MODS:
    subj = build_scale.scale_points(importlib.import_module(modname).SUBJ)
    common = subj.get('common', '')
    for n, q in enumerate(subj['qs'], 1):
        kind = 'MEET·DEET' if ('MEET' in q['src'] or 'DEET' in q['src']) else '임용'
        item = {'id': f'{pre}{s}{n:02d}', 's': s, 'u': q['g'], 't': 'set', 'lv': 3, 'col': 'past', 'xs': kind,
                'q': f"[{q['src']}] " + plain(q['stem'])}
        tb = ''
        if q.get('box'):
            tb += f'<div class="bogi"><div class="bt">&lt; {q["box"][0]} &gt;</div>{q["box"][1]}</div>'
        if common:
            tb += f'<details class="pcom"><summary>공통 조건 · 상수 · 근삿값</summary><div>{common}</div></details>'
        if tb: item['tb'] = tb
        if q.get('fig'):
            k = f'{pre}{s}{n:02d}'; figs[k] = svgmath(q['fig']); item['fig'] = k
        parts = []
        for i, sb in enumerate(q['subs'], 1):
            p = {'p': plain(sb['q']), 'pt': sb.get('w', 2) * 2, 'sol': sb['a']}
            key = (s, n, i) if pre == 'xp_' else ('m' + s, n, i)
            if key in NUM:
                v, u, tol = NUM[key]; p.update(t='num', a=v, tol=tol)
                if u: p['unit'] = u
            elif key in TXT:
                p.update(t='txt', a=TXT[key])
            else:
                p.update(t='essay', kp=kps(sb['a']))
            parts.append(p)
        item['parts'] = parts
        m = re.match(r'(\d{4}) 임용 (\S+) ([AB])-(\d+)', q['src'])
        org = ('의·치의학교육입문검사(MEET·DEET), 의·치의학교육입문검사협의회 공개 기출' if kind != '임용'
               else '한국교육과정평가원 중등교사 임용시험 1차')
        item['ex'] = ('원본: ' + q['src'].replace(' 변형', '') + f' ({org}). 이 문항은 원본의 개념·아이디어를 바탕으로 숫자·조건·표현을 바꾼 변형 문항이에요.')
        out.append(item)

yaml.safe_dump(out, open(os.path.join(HERE, '..', 'x_past.yaml'), 'w'), allow_unicode=True, sort_keys=False, width=1000)
json.dump(figs, open(os.path.join(HERE, '..', 'past_figs.json'), 'w'), ensure_ascii=False)
from collections import Counter
print(len(out), Counter(x['s'] for x in out), 'figs', len(figs),
      'num parts', sum(1 for x in out for p in x['parts'] if p['t'] != 'essay'))
