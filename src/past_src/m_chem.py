# -*- coding: utf-8 -*-
# MEET·DEET 자연과학Ⅱ 화학 — 범위 문항 변형
from figs import plot

# O2 표준 몰 엔트로피–온도 (계단 모양)
o2 = [(40, 52), (54, 59), (54, 67), (90, 94), (90, 170), (150, 185), (220, 196), (298, 205)]
fig_o2 = plot((40, 300), (40, 220), [40, 54, 90, 150, 200, 250, 298], [40, 94, 170, 205], '온도 (K)', 'S° (J/mol·K)',
              curves=[(o2,)], minor=(10, 10), w=300, h=210, grid=True,
              marks=[(90, 120, 2.5), (90, 150, 2.5)], texts=[(93, 118, 'a'), (93, 148, 'b')])

# 가상의 물질 X 상그림 (개형)
fig_ph = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 200" width="290" height="200" font-family="Noto Sans CJK KR" font-size="10">'
          '<line x1="40" y1="180" x2="280" y2="180" stroke="#000"/><line x1="40" y1="180" x2="40" y2="10" stroke="#000"/>'
          '<text x="160" y="196" text-anchor="middle">온도</text><text x="12" y="95" transform="rotate(-90 12 95)" text-anchor="middle">압력 (로그 눈금)</text>'
          '<path d="M60 175 Q150 160 190 140" stroke="#000" stroke-width="1.6" fill="none"/>'
          '<path d="M190 140 Q240 110 275 70" stroke="#000" stroke-width="1.6" fill="none"/>'
          '<path d="M190 140 L165 60" stroke="#000" stroke-width="1.6" fill="none"/>'
          '<path d="M165 60 L200 15" stroke="#000" stroke-width="1.6" fill="none"/>'
          '<path d="M165 60 L50 45" stroke="#000" stroke-width="1.6" fill="none"/>'
          '<circle cx="190" cy="140" r="3"/><circle cx="165" cy="60" r="3"/><circle cx="178" cy="100" r="3" fill="#fff" stroke="#000"/><text x="183" y="104">p</text>'
          '<text x="90" y="25">상 Ⅰ</text><text x="95" y="110">상 Ⅱ</text><text x="225" y="60">상 Ⅲ</text><text x="230" y="170">상 Ⅳ</text>'
          '</svg>')

SUBJ = {
 'title': '화학Ⅱ (MEET·DEET)',
 'groups': {'고체·상전이': 70, '열화학·열역학': 30},
 'common': '◦ 이 과목은 계산기를 사용할 수 있다. ◦ $R=8.3\\,\\mathrm{J\\,mol^{-1}K^{-1}}$, $N_A=6.0\\times10^{23}\\,\\mathrm{mol^{-1}}$, $1\\,\\mathrm{pm}=10^{-10}\\,\\mathrm{cm}$. 기체는 이상 기체로 거동한다.',
 'qs': [
 {'g': '고체·상전이', 'src': '2017 MDEET 자연과학Ⅱ 6 변형',
  'stem': 'nickel(Ni) 결정은 면심 입방 구조이고 단위 세포 모서리 길이는 $352\\,\\mathrm{pm}$이다. 단위 세포의 윗면, 아랫면과, 단위 세포를 높이 방향으로 이등분하는 단면을 생각한다. (Ni의 원자량 58.7)',
  'subs': [
   {'q': '윗면과 이등분 단면에 놓인 원자 중심의 위치를 각각 설명하시오.', 'w': 2,
    'a': '윗면(아랫면): 네 꼭짓점 + 면의 중심(5개). 이등분 단면: 옆면 4개의 중심이 단면 정사각형의 <b>네 변의 가운데</b>에 놓인다(4개).'},
   {'q': '배위수, 단위 세포당 원자 수, 가장 가까운 원자 사이의 거리(pm)를 구하시오.', 'w': 2,
    'a': '배위수 <span class="fin">12</span>, <span class="fin">4개</span>, $\\dfrac{\\sqrt2}{2}\\times352\\approx$ <span class="fin">249 pm</span>'},
   {'q': 'Ni의 밀도(g/cm³)를 구하시오.', 'w': 2,
    'a': '$\\dfrac{4\\times58.7}{6.0\\times10^{23}\\times(3.52\\times10^{-8})^3}\\approx$ <span class="fin">$8.97\\,\\mathrm{g/cm^3}$</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2025 MDEET 5 · 2018 MDEET 7 · 2019 MDEET 6 변형',
  'stem': 'sodium chloride(NaCl, 암염형)와 calcium fluoride(CaF$_2$, 형석형) 결정의 입방 단위 세포를 비교한다.',
  'subs': [
   {'q': '두 결정에서 음이온의 배열과, 양이온이 들어가는 구멍(또는 위치)을 각각 쓰시오.', 'w': 2,
    'a': 'NaCl: Cl$^-$ 면심 입방, Na$^+$는 <b>팔면체 구멍 전부</b>. CaF$_2$: Ca$^{2+}$이 면심 입방이고 F$^-$이 사면체 구멍 전부를 채움 → 음이온(F$^-$)만 보면 <b>단순 입방</b> 배열이고 Ca$^{2+}$은 F$^-$ 정육면체의 중심(하나 건너)에 들어간다.'},
   {'q': '양이온의 배위수와 단위 세포당 양이온·음이온 수를 각각 비교하시오.', 'w': 2,
    'a': 'NaCl: Na$^+$ 배위수 6, Na$^+$ 4개·Cl$^-$ 4개. CaF$_2$: Ca$^{2+}$ 배위수 8, Ca$^{2+}$ 4개·F$^-$ 8개.'},
   {'q': '섬아연석형 zinc sulfide(ZnS)에서 S$^{2-}$의 배위수를 쓰고, 이 구조에서 Zn$^{2+}$이 채우는 사면체 구멍의 비율을 쓰시오.', 'w': 1, 'size': 'short',
    'a': 'S$^{2-}$ 배위수 <span class="fin">4</span>, 사면체 구멍의 <span class="fin">절반</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2020 MDEET 자연과학Ⅱ 7 변형',
  'stem': '(가)는 입방 조밀 쌓임 구조를 갖는 금속 nickel의 단위 세포이고, (나)는 Ni$^{2+}$이 면심 입방 구조로 배열된 nickel(II) oxide(NiO)의 단위 세포이다.',
  'subs': [
   {'q': '(가)의 충전율(원자가 차지하는 부피 비율)을 $\\pi$로 나타내시오.', 'w': 2, 'size': 'short',
    'a': '$4r=\\sqrt2a$ → $\\dfrac{4\\cdot\\frac43\\pi r^3}{a^3}=$ <span class="fin">$\\dfrac{\\sqrt2\\pi}{6}$</span> (약 74 %)'},
   {'q': '(나)에서 O$^{2-}$이 채우는 구멍의 종류를 쓰고, (가)의 Ni 배위수와 (나)의 O$^{2-}$ 배위수를 비교하시오.', 'w': 2,
    'a': 'Ni$^{2+}$ 격자의 <b>팔면체 구멍 전부</b>(암염형). (가) Ni 배위수 12, (나) O$^{2-}$ 배위수 6 → (가)가 2배.'},
  ]},
 {'g': '고체·상전이', 'src': '2021 MDEET 자연과학Ⅱ 5 변형',
  'stem': 'lithium bromide(LiBr)는 암염형 구조이고 단위 세포 모서리 길이는 $550\\,\\mathrm{pm}$이다. (Li 6.9, Br 80.0)',
  'subs': [
   {'q': 'Br$^-$에서 가장 가까운 Br$^-$의 개수와 그 거리(pm)를 구하시오.', 'w': 2,
    'a': '<span class="fin">12개</span>, $\\dfrac{550}{\\sqrt2}\\approx$ <span class="fin">389 pm</span>'},
   {'q': 'Li$^+$이 Br$^-$ 배열의 사면체 구멍과 팔면체 구멍 중 어디에 있는지 쓰고, LiBr의 밀도(g/cm³)를 구하시오.', 'w': 3,
    'a': '<b>팔면체 구멍</b>. $\\dfrac{4\\times86.9}{6.0\\times10^{23}\\times(5.50\\times10^{-8})^3}\\approx$ <span class="fin">$3.48\\,\\mathrm{g/cm^3}$</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2023 MDEET 자연과학Ⅱ 7 변형',
  'stem': 'iron(Fe)은 상온에서 체심 입방 구조(α-Fe, 모서리 $a_1$), 고온에서 면심 입방 구조(γ-Fe, 모서리 $a_2$)를 갖는다. 두 구조에서 가장 가까운 원자 사이의 거리는 같다고 가정한다.',
  'subs': [
   {'q': '배위수는 γ-Fe가 α-Fe의 몇 배인지 쓰시오.', 'w': 1, 'size': 'short',
    'a': '$12/8=$ <span class="fin">1.5배</span>'},
   {'q': '$a_2/a_1$을 구하시오.', 'w': 2,
    'a': '최단 거리: $\\dfrac{\\sqrt3}{2}a_1=\\dfrac{\\sqrt2}{2}a_2$ → $\\dfrac{a_2}{a_1}=\\sqrt{\\dfrac32}\\approx$ <span class="fin">1.22</span>'},
   {'q': '밀도는 γ-Fe가 α-Fe의 몇 배인지 구하고, 가열할 때 α → γ 전이에서 부피 변화를 쓰시오.', 'w': 2,
    'a': '$\\dfrac{4/a_2^3}{2/a_1^3}=\\dfrac{2}{(1.5)^{1.5}}\\approx$ <span class="fin">1.09배</span> → γ-Fe가 더 조밀하므로 전이 때 <b>부피가 줄어든다</b>.'},
  ]},
 {'g': '고체·상전이', 'src': '2024 MDEET 자연과학Ⅱ 7 변형',
  'stem': '이온 결정 cesium chloride(CsCl), potassium chloride(KCl, 암염형), copper(I) chloride(CuCl, 섬아연석형)의 입방 단위 세포를 비교한다. CsCl 단위 세포는 꼭짓점에 Cl$^-$, 중심에 Cs$^+$이 있다.',
  'subs': [
   {'q': 'CsCl의 단위 세포가 체심 입방 구조가 아닌 이유를 쓰고, 어떤 격자로 볼 수 있는지 쓰시오.', 'w': 2,
    'a': '꼭짓점(Cl$^-$)과 중심(Cs$^+$)의 입자 종류가 달라 같은 격자점이 아니다 → Cl$^-$와 Cs$^+$이 각각 만든 <b>단순 입방 격자 두 개가 엇갈려 겹친</b> 구조.'},
   {'q': 'Cl$^-$의 배위수를 세 결정에서 각각 쓰고, 단위 세포당 Cl$^-$ 수는 CuCl이 CsCl의 몇 배인지 쓰시오.', 'w': 3,
    'a': '배위수: CsCl 8, KCl 6, CuCl 4. Cl$^-$ 수: CuCl 4, CsCl 1 → <span class="fin">4배</span>'},
  ]},
 {'g': '고체·상전이', 'src': '2026 MDEET 자연과학Ⅱ 6 변형',
  'stem': '어떤 금속 M의 산화물 MO$_n$의 입방 단위 세포에서 M 이온은 모든 꼭짓점에, O$^{2-}$은 모든 모서리의 중심에 놓여 있다.',
  'subs': [
   {'q': '$n$을 구하는 과정을 쓰고, M 이온의 전하를 쓰시오.', 'w': 2,
    'a': 'M: $8\\times\\frac18=1$, O: $12\\times\\frac14=3$ → <span class="fin">$n=3$</span>, M$^{6+}$'},
   {'q': 'O$^{2-}$의 배위수와 M 이온의 배위수, M 이온이 이루는 격자의 종류를 쓰시오.', 'w': 2,
    'a': 'O$^{2-}$: <span class="fin">2</span>(양쪽 꼭짓점의 M), M: <span class="fin">6</span>, M은 <b>단순 입방</b> 격자'},
  ]},
 {'g': '고체·상전이', 'src': '2027 MDEET 자연과학Ⅱ 4 변형',
  'stem': 'KCl은 대기압에서 암염형(모서리 $a_1$), 높은 압력에서 CsCl형(모서리 $a_2$) 구조를 갖는다. 두 구조에서 인접한 K$^+$과 Cl$^-$ 사이의 거리는 같다고 가정한다.',
  'subs': [
   {'q': 'Cl$^-$의 배위수는 고압 구조가 대기압 구조의 몇 배인지, 단위 세포당 K$^+$ 수는 대기압 구조가 고압 구조의 몇 배인지 쓰시오.', 'w': 2,
    'a': '배위수 $8/6=$ <span class="fin">$\\frac43$배</span>, K$^+$ 수 $4/1=$ <span class="fin">4배</span>'},
   {'q': '$a_1/a_2$를 구하고, 고압에서 이 전이가 일어나는 이유를 밀도로 설명하시오.', 'w': 3,
    'a': '$\\dfrac{a_1}{2}=\\dfrac{\\sqrt3}{2}a_2$ → <span class="fin">$a_1/a_2=\\sqrt3$</span>. 밀도비(고압/대기압) $=\\dfrac{1/a_2^3}{4/a_1^3}=\\dfrac{3\\sqrt3}{4}\\approx1.3$ → 고압 구조가 더 조밀(부피가 작음)하므로 압력이 높으면 안정하다.'},
  ]},
 {'g': '고체·상전이', 'src': '2022 MDEET 5 · 2014 MEET 4 변형',
  'stem': '그림은 어떤 물질 X의 상그림이고, 상 Ⅰ~Ⅳ 중 기체상은 1개, 액체상은 1개, 고체상은 2개이다. 점 p는 상 Ⅱ와 상 Ⅲ의 경계선 위에 있다.',
  'fig': fig_ph,
  'subs': [
   {'q': '상 Ⅰ~Ⅳ가 각각 고체·액체·기체 중 무엇인지 쓰고, 삼중점의 개수를 쓰시오.', 'w': 2,
    'a': 'Ⅰ 고체(고압), Ⅱ 고체, Ⅲ 액체, Ⅳ 기체. 삼중점 <span class="fin">2개</span>'},
   {'q': 'p에서 밀도는 상 Ⅱ와 상 Ⅲ 중 어느 쪽이 큰지 근거와 함께 쓰고, p에서 온도를 일정하게 하고 압력을 높이면 어떤 상변화가 일어나는지 쓰시오.', 'w': 3,
    'a': 'Ⅱ–Ⅲ 경계선 기울기가 음수 → 클라페이롱 식 $\\frac{dP}{dT}=\\frac{\\Delta H}{T\\Delta V}$에서 녹을 때 $\\Delta V<0$ → <b>액체(Ⅲ)의 밀도가 더 크다</b>. 압력을 높이면 밀도가 큰 쪽으로 → <b>상 Ⅱ가 상 Ⅲ(액체)으로 녹는다</b>.'},
  ]},
 {'g': '고체·상전이', 'src': '2026 MDEET 자연과학Ⅱ 7 변형',
  'stem': '피스톤이 달린 실린더에 $400\\,\\mathrm{K}$, $4\\,\\mathrm{L}$, $1.5\\,\\mathrm{atm}$의 A(g)가 들어 있다. A를 $300\\,\\mathrm{K}$로 냉각한 뒤 고정 장치를 옮겨 부피를 바꾸며 평형 (가)~(라)에 도달시켰다. 온도는 $300\\,\\mathrm{K}$로 일정하고, A는 기체 또는 액체로 존재한다(액체 부피 무시).',
  'box': ('평형', '<table class="dt"><tr><th></th><th>(가)</th><th>(나)</th><th>(다)</th><th>(라)</th></tr><tr><td>부피 (L)</td><td>3</td><td>6</td><td>10</td><td>12</td></tr><tr><td>A(g) 압력 (atm)</td><td>$a$</td><td>$a$</td><td>$x$</td><td>$\\frac34a$</td></tr></table>'),
  'subs': [
   {'q': '(가)와 (나)에서 압력이 같은 이유를 쓰고, $a$를 구하시오.', 'w': 3,
    'a': '두 평형 모두 액체와 기체가 공존하므로 압력은 300 K의 <b>증기 압력</b>으로 같다. (라)는 압력이 증기 압력보다 낮으므로 모두 기체: $P=\\dfrac{1.5\\times4\\times\\frac{300}{400}}{12}=0.375=\\frac34a$ → <span class="fin">$a=0.5$</span>'},
   {'q': '$x$를 구하고, A(l)의 몰수는 (가)가 (나)의 몇 배인지 구하시오.', 'w': 2,
    'a': '전체 $nRT=4.5\\,\\mathrm{atm\\cdot L}$. (다) 모두 기체면 $4.5/10=0.45\\lt0.5$ → <span class="fin">$x=0.45$</span>. 액체(atm·L 단위): (가) $4.5-1.5=3.0$, (나) $4.5-3.0=1.5$ → <span class="fin">2배</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2017 MDEET 자연과학Ⅱ 8 변형',
  'stem': '그림은 1기압에서 oxygen(O$_2$)의 표준 몰 엔트로피를 온도에 따라 나타낸 것이다. 엔트로피는 54 K에서 59 → 67, 90 K에서 94 → 170 J/(mol·K)로 수직으로 증가한다.',
  'fig': fig_o2,
  'subs': [
   {'q': 'O$_2$의 녹는점과 끓는점을 쓰고, 70 K에서 O$_2$의 상태를 쓰시오.', 'w': 1, 'size': 'short',
    'a': '녹는점 54 K, 끓는점 90 K, 70 K에서 <b>액체</b>'},
   {'q': '몰 융해 엔탈피와 몰 기화 엔탈피를 구하시오.', 'w': 2,
    'a': '$\\Delta H_{fus}=54\\times(67-59)=$ <span class="fin">432 J/mol</span>, $\\Delta H_{vap}=90\\times(170-94)=$ <span class="fin">6840 J/mol</span>'},
   {'q': 'a → b 과정의 자유 에너지 변화를 쓰고, 기화할 때의 엔트로피 증가가 융해보다 훨씬 큰 이유를 쓰시오.', 'w': 2,
    'a': '끓는점에서의 평형 상변화 → <b>$\\Delta G=0$</b>. 기체가 되면 분자가 차지하는 부피와 운동의 자유도가 액체보다 훨씬 커져 무질서도가 크게 증가한다.'},
  ]},
 {'g': '열화학·열역학', 'src': '2017 MDEET 자연과학Ⅱ 9 변형',
  'stem': '25 °C에서 propane의 연소 반응은 C$_3$H$_8$(g) + 5O$_2$(g) → 3CO$_2$(g) + 4H$_2$O(l), $\\Delta H^\\circ=-2220\\,\\mathrm{kJ}$이다. CO$_2$(g)와 H$_2$O(l)의 표준 생성 엔탈피는 각각 $-394$, $-286\\,\\mathrm{kJ/mol}$이다.',
  'subs': [
   {'q': 'C$_3$H$_8$(g)의 표준 생성 엔탈피를 구하시오.', 'w': 2,
    'a': '$-2220=3(-394)+4(-286)-\\Delta H_f$ → <span class="fin">$\\Delta H_f=-106\\,\\mathrm{kJ/mol}$</span>'},
   {'q': '이 반응의 엔트로피 변화 부호를 쓰고, 표준 반응 내부 에너지 변화 $\\Delta E^\\circ$를 구하시오.', 'w': 3,
    'a': '기체 몰수 6 → 3으로 감소 → <b>$\\Delta S\\lt0$</b>. $\\Delta E=\\Delta H-\\Delta n_gRT=-2220+3\\times8.3\\times298\\times10^{-3}\\approx$ <span class="fin">$-2212.6\\,\\mathrm{kJ}$</span> ($\\Delta E\\gt\\Delta H$)'},
  ]},
 {'g': '열화학·열역학', 'src': '2017 MDEET 자연과학Ⅱ 10 변형',
  'stem': 'calcium carbonate의 분해 반응 CaCO$_3$(s) ⇌ CaO(s) + CO$_2$(g)의 $\\Delta H^\\circ=178\\,\\mathrm{kJ}$, $\\Delta S^\\circ=161\\,\\mathrm{J/K}$이고 온도에 무관하다. 온도 $T$에서 $K_p=1$이다.',
  'subs': [
   {'q': '$T$를 구하고, 이때 평형에서 CO$_2$의 압력을 쓰시오.', 'w': 2,
    'a': '$K_p=1$ → $\\Delta G^\\circ=0$ → $T=\\dfrac{178000}{161}\\approx$ <span class="fin">1106 K</span>, $P_{CO_2}=K_p=$ <span class="fin">1 atm</span>'},
   {'q': '평형 상태에서 CaO(s)를 더 넣을 때와 부피를 절반으로 줄일 때 CO$_2$의 평형 압력이 각각 어떻게 되는지 쓰시오(CaCO$_3$은 남아 있다).', 'w': 2,
    'a': '두 경우 모두 <b>변하지 않는다</b>. $K_p=P_{CO_2}$로 고체의 양·부피와 무관하므로, 부피를 줄이면 CO$_2$ 일부가 CaO와 반응해 원래 압력으로 돌아온다.'},
  ]},
 {'g': '열화학·열역학', 'src': '2019 MDEET 자연과학Ⅱ 11 변형',
  'stem': '298 K에서 (가) PCl$_5$(g) ⇌ PCl$_3$(g) + Cl$_2$(g)의 $\\Delta H^\\circ=88$, $\\Delta G^\\circ=38\\,\\mathrm{kJ}$이고, (나) P(s, 백린) + $\\frac52$Cl$_2$(g) ⇌ PCl$_5$(g)의 $\\Delta H^\\circ=-375$, $\\Delta G^\\circ=-305\\,\\mathrm{kJ}$이다.',
  'subs': [
   {'q': 'PCl$_3$(g)의 표준 생성 자유 에너지를 구하시오.', 'w': 2, 'size': 'short',
    'a': '(가)+(나): $-305+38=$ <span class="fin">$-267\\,\\mathrm{kJ/mol}$</span>'},
   {'q': '반응 (가)의 $\\Delta S^\\circ$와 $\\Delta E^\\circ$를 구하시오.', 'w': 3,
    'a': '$\\Delta S^\\circ=\\dfrac{88000-38000}{298}\\approx$ <span class="fin">168 J/K</span>. $\\Delta n_g=1$ → $\\Delta E^\\circ=88-8.3\\times298\\times10^{-3}\\approx$ <span class="fin">85.5 kJ</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2020 MDEET 자연과학Ⅱ 9 변형',
  'stem': '300 K에서 CO(g) + $\\frac12$O$_2$(g) → CO$_2$(g) 반응에 대해 CO(g)와 CO$_2$(g)의 표준 생성 엔탈피는 각각 $-110$, $-394\\,\\mathrm{kJ/mol}$, 표준 생성 자유 에너지는 각각 $-137$, $-394\\,\\mathrm{kJ/mol}$이다.',
  'subs': [
   {'q': '$\\Delta H^\\circ$, $\\Delta G^\\circ$, $\\Delta S^\\circ$를 구하시오.', 'w': 3,
    'a': '$\\Delta H^\\circ=$ <span class="fin">$-284$ kJ</span>, $\\Delta G^\\circ=$ <span class="fin">$-257$ kJ</span>, $\\Delta S^\\circ=\\dfrac{-284+257}{300}\\times1000=$ <span class="fin">$-90$ J/K</span>'},
   {'q': '$\\Delta E^\\circ$와 $\\Delta H^\\circ$의 크기를 비교하시오.', 'w': 1,
    'a': '$\\Delta n_g=-\\frac12$ → $\\Delta E=\\Delta H+\\frac12RT\\approx-282.8\\,\\mathrm{kJ}$ → $\\Delta E^\\circ\\gt\\Delta H^\\circ$ (덜 음수)'},
  ]},
 {'g': '열화학·열역학', 'src': '2021 MDEET 자연과학Ⅱ 13 변형',
  'stem': '298 K에서 표준 생성 자유 에너지(kJ/mol)와 표준 몰 엔트로피(J/K·mol)는 C$_6$H$_6$(l) 125, 173 / O$_2$(g) 0, 205 / CO$_2$(g) $-394$, 214 / H$_2$O(l) $-237$, 70이다. 액체 benzene 1 mol이 완전 연소한다.',
  'subs': [
   {'q': '$\\Delta G^\\circ$와 $\\Delta S^\\circ$를 구하시오.', 'w': 3,
    'a': 'C$_6$H$_6$ + 7.5O$_2$ → 6CO$_2$ + 3H$_2$O(l). $\\Delta G^\\circ=6(-394)+3(-237)-125=$ <span class="fin">$-3200$ kJ</span>. $\\Delta S^\\circ=6(214)+3(70)-173-7.5(205)=$ <span class="fin">$-216.5$ J/K</span>'},
   {'q': '$\\Delta H^\\circ$를 구하고, $\\Delta E^\\circ-\\Delta H^\\circ$를 구하시오.', 'w': 2,
    'a': '$\\Delta H^\\circ=\\Delta G^\\circ+T\\Delta S^\\circ=-3200+298(-0.2165)\\approx$ <span class="fin">$-3265$ kJ</span>. $\\Delta n_g=-1.5$ → $\\Delta E-\\Delta H=1.5RT\\approx$ <span class="fin">+3.7 kJ</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2024 MDEET 자연과학Ⅱ 11 변형',
  'stem': '반응 A(g) + B(l) ⇌ 2C(g)의 $\\Delta H^\\circ=30\\,\\mathrm{kJ}$, $\\Delta S^\\circ=100\\,\\mathrm{J/K}$이고 온도에 무관하다.',
  'subs': [
   {'q': '$\\Delta H^\\circ$와 $T\\Delta S^\\circ$를 온도에 따라 나타낸 두 직선이 만나는 온도를 구하고, 그 온도의 의미를 쓰시오.', 'w': 2,
    'a': '$T=\\dfrac{30000}{100}=$ <span class="fin">300 K</span>. $\\Delta G^\\circ=0$, $K=1$이 되는 온도(이보다 높으면 정반응이 자발적).'},
   {'q': '280 K와 320 K에서 $\\Delta G^\\circ$를 구하고, 온도가 높아질 때 평형 상수의 변화를 쓰시오.', 'w': 2,
    'a': '280 K: $+2\\,\\mathrm{kJ}$, 320 K: $-2\\,\\mathrm{kJ}$. 흡열 반응이므로 온도가 높을수록 <b>$K$ 증가</b>.'},
   {'q': '300 K에서 C(g) 2 mol이 생성될 때 $\\Delta E^\\circ$를 구하시오.', 'w': 1, 'size': 'short',
    'a': '$\\Delta n_g=2-1=1$ → $30-8.3\\times300\\times10^{-3}\\approx$ <span class="fin">27.5 kJ</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2026 MDEET 자연과학Ⅱ 12 변형',
  'stem': '피스톤이 달린 실린더에서 1 mol의 H$_2$O(l)이 1 atm, 100 °C에서 가역적으로 H$_2$O(g)로 변하였다. 100 °C에서 물의 표준 기화 엔탈피는 $40.7\\,\\mathrm{kJ/mol}$이다. (액체 부피 무시)',
  'subs': [
   {'q': '이 과정의 $\\Delta G$와 $\\Delta S$를 구하시오.', 'w': 2,
    'a': '평형 상변화 → <span class="fin">$\\Delta G=0$</span>, $\\Delta S=\\dfrac{40700}{373}\\approx$ <span class="fin">109 J/K</span>'},
   {'q': '계가 한 일과 내부 에너지 변화를 구하시오.', 'w': 2,
    'a': '$w=P\\Delta V=RT=8.3\\times373\\approx$ <span class="fin">3.10 kJ</span>, $\\Delta E=40.7-3.10=$ <span class="fin">37.6 kJ</span>'},
  ]},
 {'g': '열화학·열역학', 'src': '2019 MDEET 자연과학Ⅱ 10 변형',
  'stem': '298 K, 표준 상태에서 hydrogen peroxide의 분해와 관련된 반응 엔탈피는 다음과 같다. (b) 2H$_2$O$_2$(g) → 2H$_2$O(g) + O$_2$(g), $\\Delta H^\\circ=-206\\,\\mathrm{kJ}$ / (c) 2H$_2$O$_2$(l) → 2H$_2$O(g) + O$_2$(g), $\\Delta H^\\circ=-100\\,\\mathrm{kJ}$',
  'subs': [
   {'q': 'H$_2$O$_2$의 몰 기화 엔탈피를 헤스 법칙으로 구하시오.', 'w': 2,
    'a': '(c) − (b): 2H$_2$O$_2$(l) → 2H$_2$O$_2$(g), $\\Delta H=+106$ → <span class="fin">53 kJ/mol</span>'},
   {'q': '과정 (b)에서 계의 엔트로피 변화 부호를 쓰고 이유를 쓰시오.', 'w': 1,
    'a': '기체 2 mol → 3 mol로 증가 → <b>$\\Delta S\\gt0$</b>'},
  ]},
 {'g': '열화학·열역학', 'src': '2020 MDEET 자연과학Ⅱ 8 변형',
  'stem': '298 K에서 황의 동소체 S(g), S$_2$(g), S$_8$(g)의 표준 생성 엔탈피는 각각 278, 128, 102 kJ/mol이다. 또 4S$_2$(g) + 8O$_2$(g) → 8SO$_2$(g)의 $\\Delta H^\\circ=-2896\\,\\mathrm{kJ}$이다.',
  'subs': [
   {'q': 'S$_2$(g)의 S=S 결합 에너지를 구하시오.', 'w': 2, 'size': 'short',
    'a': 'S$_2$ → 2S: $2(278)-128=$ <span class="fin">428 kJ/mol</span>'},
   {'q': 'SO$_2$(g)의 표준 생성 엔탈피와, S$_8$(g) + 8O$_2$(g) → 8SO$_2$(g)의 $\\Delta H^\\circ$를 구하시오.', 'w': 3,
    'a': '$8\\Delta H_f(\\mathrm{SO_2})=-2896+4(128)$ → <span class="fin">$-298$ kJ/mol</span>. $8(-298)-102=$ <span class="fin">$-2486$ kJ</span>'},
  ]},
 ]}
