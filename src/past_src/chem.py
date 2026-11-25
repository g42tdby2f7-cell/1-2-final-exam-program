# -*- coding: utf-8 -*-
from figs import plot, fn
import math

def cube(points, labels=(), w=260, h=190, legend=''):
    """입방 단위 세포 사투영. points: [(x,y,z,'fill')], 좌표 0~1"""
    s = 110; ox, oy = 35, 160; dx, dy = 0.45 * s, -0.32 * s
    P = lambda x, y, z: (ox + x * s + y * dx, oy - z * s + y * dy)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="Noto Sans CJK KR" font-size="10">']
    edges = [((0,0,0),(1,0,0)),((0,0,0),(0,1,0)),((0,0,0),(0,0,1)),((1,0,0),(1,1,0)),((1,0,0),(1,0,1)),((0,1,0),(1,1,0)),((0,1,0),(0,1,1)),((0,0,1),(1,0,1)),((0,0,1),(0,1,1)),((1,1,0),(1,1,1)),((1,0,1),(1,1,1)),((0,1,1),(1,1,1))]
    for a, b in edges:
        dash = ' stroke-dasharray="3,2"' if (a == (0,0,0) and b in [(0,1,0)]) or (a==(0,1,0) and b in [(1,1,0),(0,1,1)]) else ''
        x1, y1 = P(*a); x2, y2 = P(*b)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#000" stroke-width="0.9"{dash}/>')
    for (x, y, z, f, r) in sorted(points, key=lambda p: -p[1]):
        cx, cy = P(x, y, z)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{f}" stroke="#000" stroke-width="0.7"/>')
    if legend:
        out.append(legend)
    out.append('</svg>')
    return ''.join(out)

corners = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
faces = [(0.5,0.5,0),(0.5,0.5,1),(0.5,0,0.5),(0.5,1,0.5),(0,0.5,0.5),(1,0.5,0.5)]
edges_c = [(0.5,0,0),(0.5,1,0),(0.5,0,1),(0.5,1,1),(0,0.5,0),(1,0.5,0),(0,0.5,1),(1,0.5,1),(0,0,0.5),(1,0,0.5),(0,1,0.5),(1,1,0.5)]
fig_cac2 = cube([(x,y,z,'#fff',5) for x,y,z in corners+faces] + [(x,y,z,'#555',4) for x,y,z in edges_c+[(0.5,0.5,0.5)]],
                legend='<circle cx="215" cy="20" r="5" fill="#fff" stroke="#000"/><text x="223" y="24">Ca²⁺</text><circle cx="215" cy="38" r="4" fill="#555" stroke="#000"/><text x="223" y="42">C₂²⁻</text>')
fig_perov = cube([(x,y,z,'#fff',5) for x,y,z in corners] + [(x,y,z,'#888',4) for x,y,z in faces] + [(0.5,0.5,0.5,'#000',3)],
                 legend='<circle cx="215" cy="16" r="5" fill="#fff" stroke="#000"/><text x="223" y="20">Sr²⁺</text><circle cx="215" cy="32" r="3" fill="#000"/><text x="223" y="36">Ti⁴⁺</text><circle cx="215" cy="48" r="4" fill="#888" stroke="#000"/><text x="223" y="52">O²⁻</text>')

# 액체-액체 상평형 그림 (A의 몰분율 vs 온도)
def dome(x):
    # T(x) 정규화: 임계점 x=0.5, T=1, x=0.05/0.95에서 0
    return max(0.0, 1 - ((x - 0.5) / 0.45) ** 2)
# T축: 300 K(바닥)~360 K(임계 350K)
Tmin, Tc = 300, 350
pts = [(x, Tmin + (Tc - Tmin) * dome(x)) for x in [0.05 + 0.9 * i / 120 for i in range(121)]]
# T2 = 332 K일 때 공존 조성: dome=0.64 → |x-0.5|/0.45=0.6 → x=0.23, 0.77
fig_ll = plot((0, 1), (300, 360), [0, 0.2, 0.4, 0.6, 0.8, 1.0], [300, 310, 320, 330, 340, 350, 360], 'A의 몰분율 X_A', '온도(K)',
              curves=[(pts,)], grid=True, minor=(0.05, 2), w=300, h=220,
              texts=[(0.42, 354, 'P = 1'), (0.42, 315, 'P = 2'), (0.08, 345, 'P = 1')],
              extra=lambda X, Y: f'<line x1="{X(0):.1f}" y1="{Y(332):.1f}" x2="{X(1):.1f}" y2="{Y(332):.1f}" stroke="#000" stroke-dasharray="4,3"/><text x="{X(1)-4:.1f}" y="{Y(332)-3:.1f}" text-anchor="end">T₂</text>')

SUBJ = {
 'title': '화 학 Ⅱ',
 'groups': {'고체·상전이': 70, '열화학·열역학': 30},
 'common': '◦ 이 과목은 계산기를 사용할 수 있다. ◦ 기체 상수 $R=8.3\\,\\mathrm{J\\,mol^{-1}K^{-1}}$, $1\\,\\mathrm{bar\\cdot L}=100\\,\\mathrm{J}$, 아보가드로 수 $N_A=6.0\\times10^{23}\\,\\mathrm{mol^{-1}}$.<br>'
           '◦ 별도 언급이 없으면 기체는 이상 기체로 거동하고, 이온·원자는 단단한 구로 가정한다.',
 'qs': [
 # ------------- 고체·상전이 -------------
 {'g': '고체·상전이', 'src': '2014 임용 화학 A-10 변형',
  'stem': '그림은 calcium carbide(CaC$_2$) 결정의 입방 단위 세포를 나타낸 것이다. Ca$^{2+}$은 꼭짓점과 면의 중심에, C$_2^{2-}$는 이원자 이온 형태로 모서리의 중앙과 입방체의 중심에 놓여 있다. 단위 세포 모서리의 길이는 $a$이다. (C$_2^{2-}$는 하나의 점으로 취급한다.)',
  'fig': fig_cac2,
  'subs': [
   {'q': '단위 세포 1개에 들어 있는 Ca$^{2+}$과 C$_2^{2-}$의 수를 각각 쓰시오.', 'w': 2, 'size': 'short',
    'a': 'Ca$^{2+}$: $8\\times\\frac18+6\\times\\frac12=$ <span class="fin">4</span>, C$_2^{2-}$: $12\\times\\frac14+1=$ <span class="fin">4</span>'},
   {'q': 'Ca$^{2+}$ 하나에서 가장 가까운 C$_2^{2-}$까지의 거리와 그 개수를 쓰시오.', 'w': 2, 'size': 'short',
    'a': '거리 <span class="fin">$\\dfrac a2$</span>, <span class="fin">6개</span> (팔면체 배위)'},
   {'q': 'Ca$^{2+}$ 하나에서 <b>두 번째로</b> 가까운 C$_2^{2-}$까지의 거리와 개수를 쓰시오.', 'w': 3,
    'a': '꼭짓점 Ca$^{2+}$(0,0,0)에서 체심 C$_2^{2-}$($\\frac a2,\\frac a2,\\frac a2$)까지 → <span class="fin">$\\dfrac{\\sqrt3}{2}a$</span>, 이웃 8개 단위 세포의 체심 → <span class="fin">8개</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2022 임용 화학 A-4 변형',
  'stem': '표는 금속 X와 Y에 대한 자료이다.',
  'box': ('자료', '<table class="dt"><tr><th>금속</th><th>X</th><th>Y</th></tr><tr><td>결정 구조</td><td>단순 입방</td><td>체심 입방</td></tr><tr><td>단위 세포 모서리</td><td>$l$</td><td>㉠</td></tr><tr><td>원자량</td><td>$a$</td><td>$0.25a$</td></tr><tr><td>밀도</td><td>$d$</td><td>$4d$</td></tr><tr><td>원자 반지름</td><td>$r$</td><td>㉡</td></tr></table>'),
  'subs': [
   {'q': '㉠을 $l$을 포함한 식으로 쓰시오.', 'w': 3,
    'a': '밀도 $=\\dfrac{Z\\cdot M}{N_A L^3}$. X: $d=\\dfrac{a}{N_Al^3}$, Y: $4d=\\dfrac{2\\times0.25a}{N_AL^3}$<br>→ $L^3=\\dfrac{0.5}{4}l^3=\\dfrac{l^3}8$ → <span class="fin">㉠ $=\\dfrac l2$</span>'},
   {'q': '㉡을 $r$을 포함한 식으로 쓰시오.', 'w': 2,
    'a': 'X(단순 입방): $l=2r$. Y(체심 입방): $4r_Y=\\sqrt3L=\\dfrac{\\sqrt3}{2}l=\\sqrt3r$ → <span class="fin">㉡ $=\\dfrac{\\sqrt3}{4}r$</span>'},
   {'q': 'X와 Y의 단위 세포에서 원자가 차지하는 부피의 비율(충전율)을 각각 구하시오.', 'w': 2, 'size': 'short',
    'a': '단순 입방 $\\dfrac{\\pi}{6}\\approx$ <span class="fin">52 %</span>, 체심 입방 $\\dfrac{\\sqrt3\\pi}{8}\\approx$ <span class="fin">68 %</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2020 임용 화학 A-10 변형',
  'stem': 'calcium fluoride(CaF$_2$)의 입방 단위 세포에서 Ca$^{2+}$은 면심 입방 구조를 이루고, F$^-$은 인접한 Ca$^{2+}$ 4개가 이루는 정사면체의 중심에 놓여 있다. 단위 세포 모서리의 길이는 $a$이다. 표는 CaF$_2$와 관련된 반응 엔탈피이다.',
  'box': ('자료', '<table class="dt"><tr><th>반응</th><th>$\\Delta H^\\circ$ (kJ/mol)</th></tr><tr><td>Ca(s) → Ca(g)</td><td>178</td></tr><tr><td>Ca(g) → Ca$^{2+}$(g) + 2e$^-$</td><td>1735</td></tr><tr><td>F$_2$(g) → 2F(g)</td><td>158</td></tr><tr><td>F$^-$(g) → F(g) + e$^-$</td><td>328</td></tr><tr><td>Ca$^{2+}$(g) + 2F$^-$(g) → CaF$_2$(s)</td><td>$-2630$</td></tr></table>'),
  'subs': [
   {'q': 'Ca$^{2+}$과 F$^-$의 배위수를 각각 쓰시오.', 'w': 2, 'size': 'short',
    'a': 'Ca$^{2+}$: <span class="fin">8</span>, F$^-$: <span class="fin">4</span>'},
   {'q': '인접한 Ca$^{2+}$과 F$^-$ 사이의 거리를 $a$로 쓰시오.', 'w': 2, 'size': 'short',
    'a': '사면체 구멍 $(\\frac a4,\\frac a4,\\frac a4)$ → <span class="fin">$\\dfrac{\\sqrt3}{4}a$</span>'},
   {'q': 'CaF$_2$(s)의 표준 생성 엔탈피를 구하는 과정과 결과를 쓰시오.', 'w': 3,
    'a': 'F(g) + e$^-$ → F$^-$(g)은 $-328$이므로<br>$\\Delta H_f=178+1735+158+2(-328)+(-2630)=$ <span class="fin">$-1215\\,\\mathrm{kJ/mol}$</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2023 임용 화학 A-11 변형',
  'stem': 'lithium oxide(Li$_2$O) 결정에서 O$^{2-}$은 입방 조밀 쌓임(면심 입방) 격자를 이루고, Li$^+$은 8개의 사면체 구멍을 모두 채운다. 인접한 Li$^+$과 O$^{2-}$ 사이의 거리는 $a$이고, O$^{2-}$의 반지름은 Li$^+$ 반지름의 $b$배이다.',
  'subs': [
   {'q': '입방 단위 세포의 모서리 길이 $l$을 $a$로 쓰시오.', 'w': 2, 'size': 'short',
    'a': '$a=\\dfrac{\\sqrt3}{4}l$ → <span class="fin">$l=\\dfrac{4a}{\\sqrt3}$</span>'},
   {'q': '단위 세포 부피에서 전체 이온이 차지하는 부피의 비율을 $b$와 $\\pi$로 나타내는 과정과 결과를 쓰시오.', 'w': 3,
    'a': '$r_{Li}=\\dfrac{a}{1+b}$, $r_O=\\dfrac{ab}{1+b}$. 단위 세포에 O$^{2-}$ 4개, Li$^+$ 8개.<br>$\\dfrac{\\frac43\\pi(4r_O^3+8r_{Li}^3)}{l^3}=\\dfrac{\\frac{16\\pi}{3}\\frac{(b^3+2)a^3}{(1+b)^3}}{\\frac{64a^3}{3\\sqrt3}}=$ <span class="fin">$\\dfrac{\\sqrt3\\,\\pi(b^3+2)}{4(1+b)^3}$</span>'},
   {'q': 'O$^{2-}$ 하나에서 두 번째로 가까운 이온의 종류와 개수를 쓰시오.', 'w': 2, 'size': 'short',
    'a': '가장 가까운 이온은 Li$^+$ 8개(거리 $a$), 두 번째는 <span class="fin">O$^{2-}$ 12개</span> (거리 $\\frac{l}{\\sqrt2}\\approx1.63a$)'},
  ]},
 {'g': '고체·상전이', 'src': '2021 임용 화학 A-4 변형',
  'stem': '그림은 strontium titanate(SrTiO$_3$)의 입방 단위 세포이다. Sr$^{2+}$, Ti$^{4+}$, O$^{2-}$은 각각 꼭짓점, 체심, 면심에 위치한다. 모서리 길이는 $a$이다.',
  'fig': fig_perov,
  'subs': [
   {'q': 'Sr$^{2+}$과 Ti$^{4+}$에 가장 가까운 O$^{2-}$의 수(배위수)를 각각 쓰시오.', 'w': 2, 'size': 'short',
    'a': 'Sr$^{2+}$: <span class="fin">12</span> (모서리 중심 방향 면심 O), Ti$^{4+}$: <span class="fin">6</span> (팔면체)'},
   {'q': 'Sr$^{2+}$과 O$^{2-}$이 서로 접촉하고, 반지름 비 $R_{Sr}/R_{O}=c$일 때 단위 세포에서 O$^{2-}$이 차지하는 부피의 비율을 $\\pi$와 $c$로 나타내시오.', 'w': 3,
    'a': 'Sr–O 거리 $=\\dfrac{a}{\\sqrt2}=R_{Sr}+R_O=(1+c)R_O$ → $R_O=\\dfrac{a}{\\sqrt2(1+c)}$<br>O$^{2-}$ 3개: $\\dfrac{3\\cdot\\frac43\\pi R_O^3}{a^3}=\\dfrac{4\\pi}{2\\sqrt2(1+c)^3}=$ <span class="fin">$\\dfrac{\\sqrt2\\,\\pi}{(1+c)^3}$</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2024 임용 화학 A-12 변형',
  'stem': '다음은 금속 M의 산화물 A와 B에 대한 설명이다. M과 O의 원자량은 각각 $m$, 16이다.',
  'box': ('설명', '◦ A의 입방 단위 세포에서 양이온 M$^{a+}$은 모든 꼭짓점에, O$^{2-}$은 모든 모서리 중심에 놓인다.<br>◦ B의 단위 세포에서 양이온 M$^{b+}$은 입방 조밀 쌓임으로 배열되고, O$^{2-}$은 모든 사면체 구멍을 채운다.<br>◦ A와 B의 단위 세포 모서리 길이(pm)는 각각 $l_1$, $l_2$이고, 인접한 M–O 사이 거리는 각각 $r_1$, $r_2$이다.'),
  'subs': [
   {'q': 'A의 화학식을 구하는 과정을 쓰고, $a$ 값을 구하시오.', 'w': 2,
    'a': 'M: $8\\times\\frac18=1$, O: $12\\times\\frac14=3$ → MO$_3$ → 전하 균형 $a=$ <span class="fin">6</span>'},
   {'q': '$\\dfrac{r_2}{r_1}$을 $l_1$, $l_2$로 나타내시오.', 'w': 2, 'size': 'short',
    'a': '$r_1=\\dfrac{l_1}2$, $r_2=\\dfrac{\\sqrt3}{4}l_2$ → <span class="fin">$\\dfrac{r_2}{r_1}=\\dfrac{\\sqrt3\\,l_2}{2l_1}$</span>'},
   {'q': 'B의 밀도(g/cm$^3$)를 $l_2$, $m$으로 나타내시오.', 'w': 2,
    'a': 'B: M 4개, O 8개 → MO$_2$ 4개. $1\\,\\mathrm{pm}=10^{-10}\\,\\mathrm{cm}$<br>$\\rho=\\dfrac{4(m+32)}{6.0\\times10^{23}\\times l_2^3\\times10^{-30}}=$ <span class="fin">$\\dfrac{4(m+32)\\times10^{7}}{6.0\\,l_2^3}$</span> g/cm$^3$'},
  ]},
 {'g': '고체·상전이', 'src': '2025 임용 화학 A-12 변형',
  'stem': 'zinc sulfide(ZnS, 섬아연석형) 결정에서 S$^{2-}$은 입방 조밀 쌓임 격자를 이루고, Zn$^{2+}$은 인접한 S$^{2-}$ 4개가 이루는 정사면체의 중심에 놓인다. S$^{2-}$의 반지름은 $r$, 인접한 Zn$^{2+}$과 S$^{2-}$ 사이의 거리는 $1.4r$이다.',
  'subs': [
   {'q': '단위 세포 하나에 있는 Zn$^{2+}$과 S$^{2-}$의 수를 쓰고, 단위 세포 모서리 길이 $l$을 $r$로 나타내시오.', 'w': 2,
    'a': 'Zn$^{2+}$ <span class="fin">4</span>, S$^{2-}$ <span class="fin">4</span> (사면체 구멍의 절반). $1.4r=\\dfrac{\\sqrt3}{4}l$ → <span class="fin">$l=\\dfrac{5.6}{\\sqrt3}r\\approx3.23r$</span>'},
   {'q': '가장 가까운 Zn$^{2+}$과 Zn$^{2+}$ 사이의 거리를 $r$로 구하시오.', 'w': 2, 'size': 'short',
    'a': 'Zn$^{2+}$도 면심 입방 배열 → $\\dfrac{l}{\\sqrt2}=\\dfrac{5.6}{\\sqrt6}r\\approx$ <span class="fin">$2.29r$</span>'},
   {'q': '단위 세포에서 Zn$^{2+}$이 차지하는 부피 비율을 구하고, 반지름 비 $r_{+}/r_{-}$로 볼 때 Zn$^{2+}$이 사면체 구멍에 들어가는 것이 적절한지 판단하시오. (사면체 배위의 반지름 비 범위: $0.225\\sim0.414$)', 'w': 3,
    'a': '$r_{Zn}=1.4r-r=0.4r$. 비율 $=\\dfrac{4\\cdot\\frac43\\pi(0.4r)^3}{(3.233r)^3}\\approx$ <span class="fin">$0.032$ (약 3.2 %)</span><br>$r_+/r_-=0.4$ → $0.225\\sim0.414$ 범위 안 → <b>사면체 배위가 적절</b>하다.'},
  ]},
 {'g': '고체·상전이', 'src': '2014 임용 화학 B-3 변형',
  'stem': '순물질의 상평형 그림에서 상 경계선의 기울기 $\\dfrac{dP}{dT}$는 두 상의 화학 퍼텐셜이 같다는 조건과 $d\\mu=-S_mdT+V_mdP$로부터 유도된다. water(H$_2$O)의 정상 녹는점은 $273\\,\\mathrm{K}$, 몰 융해 엔탈피는 $6.0\\,\\mathrm{kJ/mol}$이고, 녹을 때 몰 부피 변화는 $V_{m,l}-V_{m,s}=-1.6\\times10^{-6}\\,\\mathrm{m^3/mol}$이다. ($1\\,\\mathrm{atm}\\approx1.0\\times10^5\\,\\mathrm{Pa}$)',
  'subs': [
   {'q': '고체–액체 경계선의 $\\dfrac{dP}{dT}$를 $\\Delta H_{fus}$, $T$, $\\Delta V_m$으로 나타내시오.', 'w': 2, 'size': 'short',
    'a': '$-S_s dT+V_sdP=-S_ldT+V_ldP$ → $\\dfrac{dP}{dT}=\\dfrac{\\Delta S_m}{\\Delta V_m}=$ <span class="fin">$\\dfrac{\\Delta H_{fus}}{T\\,\\Delta V_m}$</span>'},
   {'q': '물의 고체–액체 경계선 기울기를 atm/K 단위로 구하고, 기울기의 부호가 뜻하는 바를 쓰시오.', 'w': 3,
    'a': '$\\dfrac{6000}{273\\times(-1.6\\times10^{-6})}\\approx-1.37\\times10^{7}\\,\\mathrm{Pa/K}\\approx$ <span class="fin">$-137\\,\\mathrm{atm/K}$</span><br>음수 → 압력이 높아질수록 녹는점이 낮아진다(고체가 액체보다 밀도가 작기 때문).'},
   {'q': '$100\\,\\mathrm{atm}$, $-0.5\\,^\\circ\\mathrm{C}$에서 물은 고체인지 액체인지 판단하고 근거를 쓰시오.', 'w': 2,
    'a': '$100\\,\\mathrm{atm}$에서 녹는점 $\\approx0-\\dfrac{99}{137}\\approx-0.72\\,^\\circ\\mathrm{C}$. $-0.5\\,^\\circ\\mathrm{C}$는 녹는점보다 높으므로 <span class="fin">액체</span>.'},
  ]},
 {'g': '고체·상전이', 'src': '2016 임용 화학 A-3 변형',
  'stem': '그림은 1기압에서 액체 A와 B 혼합물의 액체–액체 상평형 그림이고, $P$는 상의 개수이다. 점선은 온도 $T_2=332\\,\\mathrm{K}$를 나타낸다.',
  'fig': fig_ll,
  'subs': [
   {'q': '$T_2$에서 두 상으로 분리될 때 각 상의 A의 몰분율을 그림에서 읽어 쓰시오.', 'w': 2, 'size': 'short',
    'a': '약 <span class="fin">0.23</span>과 <span class="fin">0.77</span>'},
   {'q': '$X_A=0.10$인 혼합물 $1\\,\\mathrm{mol}$을 $T_2$로 유지하면서 A를 가해 두 상으로 분리시키려 한다. 가해야 할 A의 최소 몰수를 구하시오.', 'w': 3,
    'a': '$\\dfrac{0.10+x}{1+x}=0.23$ → $0.77x=0.13$ → <span class="fin">$x\\approx0.17\\,\\mathrm{mol}$</span> (이보다 많이 가하면 분리)'},
   {'q': '$X_A=0.50$인 혼합물이 $T_2$에서 두 상으로 나뉠 때 두 상의 몰수 비를 쓰고, 이 혼합물을 하나의 상으로 만들려면 온도를 어떻게 해야 하는지 쓰시오.', 'w': 2,
    'a': '지렛대 규칙: $(0.77-0.50):(0.50-0.23)=$ <span class="fin">1 : 1</span>. 임계 용해 온도(약 $350\\,\\mathrm{K}$)보다 높게 가열하면 한 상이 된다.'},
  ]},
 {'g': '고체·상전이', 'src': '2018 임용 화학 B-2 변형',
  'stem': '물질 A(l)의 $300\\,\\mathrm{K}$에서 증기압은 $0.20\\,\\mathrm{bar}$이고, 이 조건에서 몰 기화 엔탈피는 $a\\,\\mathrm{J/mol}$이다. 피스톤이 달린 용기에서 $300\\,\\mathrm{K}$, $0.20\\,\\mathrm{bar}$를 유지하며 A(l) $1\\,\\mathrm{mol}$을 모두 기화시킨 뒤, 온도를 $300\\,\\mathrm{K}$로 유지한 채 $0.05\\,\\mathrm{bar}$까지 가역적으로 팽창시켰다. (A(l)의 부피는 무시한다.)',
  'subs': [
   {'q': '전 과정에서 A의 내부 에너지 변화 $\\Delta U$를 구하시오.', 'w': 2,
    'a': '기화: $\\Delta U=\\Delta H-\\Delta(PV)=a-RT=a-2490$. 등온 팽창: $\\Delta U=0$<br>∴ <span class="fin">$\\Delta U=a-2490\\,\\mathrm{J}$</span>'},
   {'q': '전 과정에서 A의 깁스 에너지 변화 $\\Delta G$를 구하시오. ($\\ln4=1.39$)', 'w': 3,
    'a': '평형 기화(증기압 조건): $\\Delta G=0$. 등온: $\\Delta G=RT\\ln\\dfrac{P_2}{P_1}=8.3\\times300\\times\\ln\\dfrac14$<br>∴ <span class="fin">$\\Delta G\\approx-3.46\\times10^3\\,\\mathrm{J}$</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2024 임용 화학 B-6 변형',
  'stem': '물질 A의 1 atm에서 일정 압력 몰열용량은 $C_{p,m}=\\alpha+\\beta T$이며 표와 같다. A의 녹는점은 $350\\,\\mathrm{K}$, $350\\,\\mathrm{K}$에서 몰 융해 엔탈피는 $14\\,\\mathrm{kJ/mol}$이다.',
  'box': ('자료', '<table class="dt"><tr><th></th><th>$\\alpha$ (J K$^{-1}$mol$^{-1}$)</th><th>$\\beta$ (J K$^{-2}$mol$^{-1}$)</th></tr><tr><td>A(s)</td><td>30</td><td>0.04</td></tr><tr><td>A(l)</td><td>70</td><td>0</td></tr></table>'),
  'subs': [
   {'q': '$350\\,\\mathrm{K}$에서 A의 몰 융해 엔트로피를 구하시오.', 'w': 2, 'size': 'short',
    'a': '$\\dfrac{14000}{350}=$ <span class="fin">$40\\,\\mathrm{J\\,K^{-1}mol^{-1}}$</span>'},
   {'q': '$1\\,\\mathrm{mol}$의 A(l)를 $350\\,\\mathrm{K}$에서 $420\\,\\mathrm{K}$로 가열할 때 엔트로피 변화를 구하시오.', 'w': 2, 'size': 'short',
    'a': '$70\\ln\\dfrac{420}{350}=70\\ln1.2\\approx$ <span class="fin">$12.8\\,\\mathrm{J/K}$</span>'},
   {'q': '$250\\,\\mathrm{K}$의 A(s) $2\\,\\mathrm{mol}$을 가열하여 $380\\,\\mathrm{K}$의 A(l)로 만들 때 엔탈피 변화를 구하는 과정과 결과를 쓰시오.', 'w': 3,
    'a': '고체 가열: $\\int_{250}^{350}(30+0.04T)dT=3000+0.02(350^2-250^2)=4200\\,\\mathrm{J}$<br>융해 $14000$, 액체 가열 $70\\times30=2100$ → 1 mol당 $20300\\,\\mathrm{J}$<br>∴ <span class="fin">$\\Delta H=40.6\\,\\mathrm{kJ}$</span>'},
  ]},
 # ------------- 열화학·열역학 -------------
 {'g': '열화학·열역학', 'src': '2014 임용 화학 B-2 변형',
  'stem': '1 atm에서 nitrogen(N$_2$)의 끓는점은 $77\\,\\mathrm{K}$이고, $77\\,\\mathrm{K}$에서 몰 기화 내부 에너지 변화는 $\\Delta_{vap}U_m=a\\,\\mathrm{J/mol}$, $77\\sim154\\,\\mathrm{K}$에서 N$_2$(g)의 몰 열용량은 $C_{p,m}=b\\,\\mathrm{J\\,K^{-1}mol^{-1}}$이다.',
  'subs': [
   {'q': '$77\\,\\mathrm{K}$에서 몰 기화 엔탈피를 $a$로 쓰시오.', 'w': 1, 'size': 'short',
    'a': '$\\Delta H=\\Delta U+RT=$ <span class="fin">$a+639\\,\\mathrm{J/mol}$</span> ($8.3\\times77\\approx639$)'},
   {'q': '1 atm에서 $77\\,\\mathrm{K}$의 N$_2$(l) $1\\,\\mathrm{mol}$이 $154\\,\\mathrm{K}$의 N$_2$(g)로 변하는 과정의 엔트로피 변화를 구하는 과정과 결과를 쓰시오.', 'w': 3,
    'a': '$\\Delta S=\\dfrac{a+639}{77}+b\\ln\\dfrac{154}{77}=$ <span class="fin">$\\dfrac{a+639}{77}+b\\ln2$</span> J/K'},
  ]},
 {'g': '열화학·열역학', 'src': '2016 임용 화학 B-3 변형',
  'stem': '이원자 분자인 이상 기체 A $1.0\\,\\mathrm{mol}$을 압력이 $1.0\\,\\mathrm{bar}$로 일정한 주위에서 상태 (가) $3.0\\,\\mathrm{bar}$, $300\\,\\mathrm{K}$로부터 (나) $1.0\\,\\mathrm{bar}$, $400\\,\\mathrm{K}$로 변화시켰다. (병진과 회전 운동만 고려한다.)',
  'subs': [
   {'q': '계가 한 일의 크기 $|w|$를 $R$로 나타내시오.', 'w': 2, 'size': 'short',
    'a': '$|w|=P_{ext}(V_2-V_1)=1.0\\left(\\dfrac{400R}{1.0}-\\dfrac{300R}{3.0}\\right)=$ <span class="fin">$300R$</span>'},
   {'q': '계의 엔트로피 변화 $\\Delta S$를 $R$로 나타내시오.', 'w': 2,
    'a': '$C_p=\\frac72R$: $\\Delta S=\\frac72R\\ln\\frac{400}{300}-R\\ln\\frac{1.0}{3.0}=$ <span class="fin">$\\frac72R\\ln\\frac43+R\\ln3$</span>'},
   {'q': '같은 압력 변화를 $10\\,\\mathrm{K}\\to13.3\\,\\mathrm{K}$에서 일으키면 $\\Delta S$는 (2)와 비교해 어떠한지, A의 회전 온도($50\\,\\mathrm{K}$)와 관련지어 설명하시오.', 'w': 1,
    'a': '회전 온도보다 매우 낮아 회전 운동이 활성화되지 않으므로 $C_p\\approx\\frac52R$로 작아져 온도 항이 줄어든다 → <b>$\\Delta S$가 더 작다</b>.'},
  ]},
 {'g': '열화학·열역학', 'src': '2017 임용 화학 A-7 변형',
  'stem': '일정한 압력에서 $300\\,\\mathrm{K}$인 일정량의 물을 항온조에 넣어 $360\\,\\mathrm{K}$로 높이는 두 과정이 있다. (가)는 $360\\,\\mathrm{K}$ 항온조에 바로 넣고, (나)는 $330\\,\\mathrm{K}$ 항온조에서 평형에 이른 뒤 $360\\,\\mathrm{K}$ 항온조로 옮긴다. 물의 일정 압력 열용량은 $C_p$로 일정하다.',
  'subs': [
   {'q': '(가)와 (나)에서 ‘물의 엔트로피 변화 + 항온조의 엔트로피 변화’를 각각 $\\Delta S_1$, $\\Delta S_2$라 할 때, $\\Delta S_2-\\Delta S_1$을 $C_p$로 나타내시오.', 'w': 3,
    'a': '물의 $\\Delta S=C_p\\ln\\frac{360}{300}$은 같다. 항온조: (가) $-\\dfrac{60C_p}{360}$, (나) $-\\dfrac{30C_p}{330}-\\dfrac{30C_p}{360}$<br>$\\Delta S_2-\\Delta S_1=C_p\\left(\\dfrac{30}{360}-\\dfrac{30}{330}\\right)=$ <span class="fin">$-\\dfrac{C_p}{132}$</span>'},
   {'q': '결과로부터 항온조 단계를 더 잘게 나눌수록 전체 엔트로피 변화가 어떻게 되는지 쓰시오.', 'w': 1, 'size': 'short',
    'a': '전체 엔트로피 증가량이 줄어 0에 가까워진다(가역 과정에 가까워짐).'},
  ]},
 {'g': '열화학·열역학', 'src': '2019 임용 화학 A-11 변형',
  'stem': '실린더에 들어 있는 이상 기체 X가 $300\\,\\mathrm{K}$, $3.0\\,\\mathrm{bar}$, $1.0\\,\\mathrm{L}$ 상태에서 고정 장치를 풀어 외부 압력 $1.0\\,\\mathrm{bar}$에 대해 팽창하여 $300\\,\\mathrm{K}$, $1.0\\,\\mathrm{bar}$, $3.0\\,\\mathrm{L}$가 되었다. 실린더 외부 온도는 $300\\,\\mathrm{K}$로 일정하다. ($\\ln3=1.10$)',
  'subs': [
   {'q': 'X가 외부에 한 일의 크기와 흡수한 열을 J 단위로 구하시오.', 'w': 2, 'size': 'short',
    'a': '$|w|=1.0\\times(3.0-1.0)\\times100=$ <span class="fin">200 J</span>, 등온 $\\Delta U=0$ → <span class="fin">$q=200\\,\\mathrm{J}$</span>'},
   {'q': '계와 주위의 엔트로피 변화를 J/K 단위로 구하고, 이 과정이 자발적인지 판단하시오.', 'w': 3,
    'a': '$\\Delta S_{계}=nR\\ln3=\\dfrac{PV}{T}\\ln3=\\dfrac{300}{300}\\times1.10=$ <span class="fin">1.10 J/K</span><br>$\\Delta S_{주위}=-\\dfrac{200}{300}\\approx$ <span class="fin">$-0.67$ J/K</span> → 합 $+0.43>0$ → <b>자발적</b>'},
  ]},
 {'g': '열화학·열역학', 'src': '2019 임용 화학 B-2 변형',
  'stem': '기체 A와 B는 A(g) ⇌ 2B(g)의 평형을 이룬다. $300\\,\\mathrm{K}$에서 A의 $\\Delta H_f^\\circ=10.0$, $\\Delta G_f^\\circ=98.0\\,\\mathrm{kJ/mol}$, B의 $\\Delta H_f^\\circ=22.0$, $\\Delta G_f^\\circ=50.0\\,\\mathrm{kJ/mol}$이다. ($\\Delta H^\\circ$는 온도에 무관하다.)',
  'subs': [
   {'q': '$300\\,\\mathrm{K}$에서 반응의 $\\Delta G^\\circ$, $\\Delta H^\\circ$, $\\Delta S^\\circ$를 구하시오.', 'w': 2,
    'a': '$\\Delta G^\\circ=100-98=$ <span class="fin">2.0 kJ</span>, $\\Delta H^\\circ=44-10=$ <span class="fin">34 kJ</span>, $\\Delta S^\\circ=\\dfrac{34000-2000}{300}\\approx$ <span class="fin">107 J/K</span>'},
   {'q': '$300\\,\\mathrm{K}$와 $350\\,\\mathrm{K}$에서의 평형 상수 $K_1$, $K_2$에 대해 $\\ln K_1$, $\\ln K_2$를 구하시오.', 'w': 3,
    'a': '$\\ln K_1=-\\dfrac{2000}{8.3\\times300}\\approx$ <span class="fin">$-0.80$</span><br>$\\ln K_2=\\ln K_1-\\dfrac{\\Delta H^\\circ}{R}\\left(\\dfrac1{350}-\\dfrac1{300}\\right)=-0.80+\\dfrac{34000}{8.3}\\times4.76\\times10^{-4}\\approx$ <span class="fin">$1.15$</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2020 임용 화학 B-2 변형',
  'stem': '어떤 기체의 상태 방정식은 $P=\\dfrac{nRT}{V-nb}-\\dfrac{n^2a}{V^2}$이다($a,b>0$). 이 기체 $n$몰이 온도 $T$에서 부피 $V_1$로부터 $V_2$까지 가역 등온 팽창하였다. ($\\left(\\frac{\\partial U}{\\partial V}\\right)_T=T\\left(\\frac{\\partial P}{\\partial T}\\right)_V-P$를 이용한다.)',
  'subs': [
   {'q': '기체가 한 일을 $n, V_1, V_2, T, a, b, R$로 쓰시오.', 'w': 2,
    'a': '$w=\\int P\\,dV=$ <span class="fin">$nRT\\ln\\dfrac{V_2-nb}{V_1-nb}+n^2a\\left(\\dfrac1{V_2}-\\dfrac1{V_1}\\right)$</span>'},
   {'q': '내부 에너지 변화를 쓰고, 이상 기체와 비교해 그 의미를 설명하시오.', 'w': 2,
    'a': '$\\left(\\frac{\\partial U}{\\partial V}\\right)_T=\\dfrac{n^2a}{V^2}$ → <span class="fin">$\\Delta U=n^2a\\left(\\dfrac1{V_1}-\\dfrac1{V_2}\\right)>0$</span><br>이상 기체는 $\\Delta U=0$이지만, 분자 간 인력을 이기며 멀어지므로 퍼텐셜 에너지가 증가한다.'},
  ]},
 {'g': '열화학·열역학', 'src': '2022 임용 B-1 · 2023 임용 A-8 변형',
  'stem': '$dH=C_pdT+(1-\\alpha T)VdP$, $\\alpha=\\dfrac1V\\left(\\dfrac{\\partial V}{\\partial T}\\right)_P$이다. 기체 A $1\\,\\mathrm{mol}$의 $C_{p,m}=29\\,\\mathrm{J\\,K^{-1}mol^{-1}}$이다.',
  'subs': [
   {'q': 'A의 상태가 $1\\,\\mathrm{atm}$, $300\\,\\mathrm{K}$에서 $3\\,\\mathrm{atm}$, $320\\,\\mathrm{K}$로 변할 때, A를 이상 기체로 보면 $\\Delta H_1$은 몇 J인지 쓰시오.', 'w': 2, 'size': 'short',
    'a': '이상 기체: $\\alpha=\\frac1T$ → 압력 항 0 → <span class="fin">$\\Delta H_1=29\\times20=580\\,\\mathrm{J}$</span>'},
   {'q': 'A가 $P=\\dfrac{nRT}{V-nb}$를 만족하는 실제 기체라면 $\\Delta H_2$와 $\\Delta H_1$의 크기를 비교하시오.', 'w': 2,
    'a': '$V=nb+\\dfrac{nRT}{P}$ → $(1-\\alpha T)V=V-T\\dfrac{nR}{P}=nb$ → $\\Delta H_2=580+nb\\Delta P$ → <span class="fin">$\\Delta H_2\\gt \\Delta H_1$</span>'},
   {'q': '이 실제 기체 $1.0\\,\\mathrm{mol}$의 부피를 일정하게 하고 $250\\,\\mathrm{J}$의 열을 가했더니 $300\\,\\mathrm{K}$에서 $310\\,\\mathrm{K}$로 올랐다. $C_V$와 $C_p$를 구하시오. ($C_p-C_V=\\left[\\left(\\frac{\\partial U}{\\partial V}\\right)_T+P\\right]\\left(\\frac{\\partial V}{\\partial T}\\right)_P$)', 'w': 2,
    'a': '$C_V=\\dfrac{250}{10}=$ <span class="fin">25.0 J/K</span>. $\\left(\\frac{\\partial U}{\\partial V}\\right)_T=T\\frac{nR}{V-nb}-P=0$ → $C_p-C_V=P\\cdot\\dfrac{nR}{P}=R$ → <span class="fin">$C_p=33.3\\,\\mathrm{J/K}$</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2025 임용 화학 A-8 변형',
  'stem': '$1\\,\\mathrm{mol}$의 이상 기체가 상태 A($400\\,\\mathrm{K}$, $0.10\\,\\mathrm{m^3}$)에서 상태 B까지 등온 가역 팽창하는 과정과, 상태 A에서 상태 C($200\\,\\mathrm{K}$)까지 단열 가역 팽창하는 과정이 있다. B와 C의 부피는 $V_f$로 같고, 단열 팽창에서 기체가 한 일은 $4150\\,\\mathrm{J}$이다.',
  'subs': [
   {'q': '$C_{V,m}$을 구하고, 이 기체가 단원자·이원자 중 어느 쪽에 가까운지 쓰시오.', 'w': 2,
    'a': '$\\Delta U=-4150=C_V(200-400)$ → <span class="fin">$C_V=20.75\\,\\mathrm{J/K}=\\frac52R$</span> → 이원자'},
   {'q': '$V_f$를 구하는 과정과 결과를 쓰시오. ($2^{2.5}\\approx5.66$)', 'w': 2,
    'a': '$\\Delta S=0$: $C_V\\ln\\frac{200}{400}+R\\ln\\frac{V_f}{0.10}=0$ → $\\ln\\frac{V_f}{0.10}=2.5\\ln2$ → <span class="fin">$V_f\\approx0.57\\,\\mathrm{m^3}$</span>'},
   {'q': 'C에서 B로 변하는 과정의 $\\Delta U$를 구하시오.', 'w': 1, 'size': 'short',
    'a': '$C_V(400-200)=$ <span class="fin">$+4150\\,\\mathrm{J}$</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2021 임용 화학 A-1 변형',
  'stem': '일정한 온도에서 부피에 따른 내부 에너지 변화와 압력에 따른 엔탈피 변화가 모두 없는 기체 A가 있다. ($\\left(\\frac{\\partial S}{\\partial V}\\right)_T=\\left(\\frac{\\partial P}{\\partial T}\\right)_V$)',
  'subs': [
   {'q': 'A가 $300\\,\\mathrm{K}$, $1.2\\,\\mathrm{atm}$일 때 $\\left(\\dfrac{\\partial S}{\\partial V}\\right)_T$를 atm/K 단위로 구하시오.', 'w': 2, 'size': 'short',
    'a': 'A는 이상 기체처럼 거동 → $\\left(\\frac{\\partial P}{\\partial T}\\right)_V=\\dfrac PT=$ <span class="fin">$0.004\\,\\mathrm{atm/K}$</span>'},
   {'q': 'A가 $400\\,\\mathrm{K}$, $6.0\\,\\mathrm{L}$일 때 $\\left(\\dfrac{\\partial V}{\\partial T}\\right)_P$를 구하시오.', 'w': 2, 'size': 'short',
    'a': '$\\dfrac VT=\\dfrac{6.0}{400}=$ <span class="fin">$0.015\\,\\mathrm{L/K}$</span>'},
  ]},
 ]}
