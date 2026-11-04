import math
INK='#2b2b2b'; MUT='#888'; BLUE='#3a5bd9'; RED='#d64545'; GRN='#1f9d55'; ORG='#d9822b'; PUR='#7c4ddb'

def svg(w,h,body,maxw=440):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{maxw}px;height:auto" '
            f'font-family="-apple-system,Apple SD Gothic Neo,Noto Sans KR,sans-serif" font-size="13" fill="{INK}">'
            '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            '<marker id="arB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
            '<marker id="arR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker></defs>'
            f'{body}</svg>')

import re as _re
def _subfix(s):
    return _re.sub(r'(?<![A-Za-z])([A-Za-z])_([A-Za-z0-9γ]+)',lambda m:m.group(1)+'<tspan baseline-shift="sub" font-size="72%">'+m.group(2)+'</tspan>',s)
def T(x,y,s,anchor='middle',size=13,fill=INK,weight='normal',style=''):
    s=_subfix(s)
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" font-weight="{weight}" {style}>{s}</text>'
def L(x1,y1,x2,y2,c=INK,w=1.6,dash='',mk=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    m=f' marker-end="url(#{mk})"' if mk else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}{m}/>'
def C(x,y,r,fill,stroke=INK,w=1.2):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def P(d,c=INK,w=1.8,fill='none',dash=''):
    dd=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}"{dd}/>'
def R(x,y,w,h,fill='#fff',stroke=INK,sw=1.4,rx=3):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

# ---------------- crystal cells ----------------
def cube(atoms,types,legend=True,s=150):
    x0,y0=40,70; dx,dy=0.42*s,-0.36*s
    def pt(x,y,z): return (x0+x*s+z*dx, y0+s-y*s+z*dy)
    corners=[(i,j,k) for i in (0,1) for j in (0,1) for k in (0,1)]
    edges=[(a,b) for a in corners for b in corners if a<b and sum(abs(a[t]-b[t]) for t in range(3))==1]
    body=''
    for a,b in edges:
        p1,p2=pt(*a),pt(*b)
        hid=(0,0,1) in (a,b)
        body+=L(*p1,*p2,c='#99a' if hid else '#556',w=1.2,dash='4 3' if hid else '')
    for (x,y,z,t) in sorted(atoms,key=lambda a:-a[2]):
        col,r,_=types[t]; X,Y=pt(x,y,z)
        body+=C(X,Y,r,col,stroke='#333',w=1)
    W=int(x0+s+dx+40); H=int(y0+s+18)
    if legend:
        lx=W+6; ly=40
        for t,(col,r,lab) in types.items():
            body+=C(lx+8,ly,min(r,9),col,'#333',1)+T(lx+24,ly+4.5,lab,'start')
            ly+=28
        W=lx+150
    return svg(W,H,body,maxw=420)

CORN=[(i,j,k) for i in (0,1) for j in (0,1) for k in (0,1)]
FACE=[(.5,.5,0),(.5,.5,1),(.5,0,.5),(.5,1,.5),(0,.5,.5),(1,.5,.5)]
EDGE=[(.5,0,0),(.5,1,0),(.5,0,1),(.5,1,1),(0,.5,0),(1,.5,0),(0,.5,1),(1,.5,1),(0,0,.5),(1,0,.5),(0,1,.5),(1,1,.5)]
def cell(kind):
    A={'A':('#8fb3ff',11,'원자')}
    if kind=='sc': return cube([(*c,'A') for c in CORN],A,legend=False)
    if kind=='bcc': return cube([(*c,'A') for c in CORN]+[(.5,.5,.5,'A')],A,legend=False)
    if kind=='fcc': return cube([(*c,'A') for c in CORN]+[(*f,'A') for f in FACE],A,legend=False)
    if kind=='nacl':
        return cube([(*c,'X') for c in CORN]+[(*f,'X') for f in FACE]+[(*e,'M') for e in EDGE]+[(.5,.5,.5,'M')],
                    {'X':('#7fd18b',12,'Cl⁻ (꼭짓점·면 중심)'),'M':('#b08cf0',7,'Na⁺ (모서리·체심)')})
    if kind=='cscl':
        return cube([(*c,'X') for c in CORN]+[(.5,.5,.5,'M')],{'X':('#7fd18b',10,'Cl⁻ (꼭짓점)'),'M':('#f0a35a',13,'Cs⁺ (체심)')})
    if kind=='perov':
        return cube([(*c,'A') for c in CORN]+[(.5,.5,.5,'B')]+[(*f,'X') for f in FACE],
                    {'A':('#f0a35a',10,'A (꼭짓점)'),'B':('#8fb3ff',12,'B (체심)'),'X':('#e86b6b',8,'X (면 중심)')})
    if kind=='nial':
        return cube([(*c,'A') for c in CORN]+[(*f,'N') for f in FACE],{'A':('#c0c0c0',10,'Y (꼭짓점)'),'N':('#7fd18b',10,'Z (면 중심)')})
    if kind=='edgeb':
        return cube([(*c,'A') for c in CORN]+[(*e,'B') for e in EDGE],{'A':('#8fb3ff',10,'P (꼭짓점)'),'B':('#e86b6b',8,'Q (모서리 중앙)')})

def lattice2d():
    # 2D square lattice; unit cell: corners M, edge midpoints A, centre A
    s=60; x0,y0=30,30; b=''
    pts=[]
    for i in range(4):
        for j in range(4):
            pts.append((x0+i*s,y0+j*s,'M'))
    for i in range(4):
        for j in range(3):
            pts.append((x0+i*s,y0+j*s+s/2,'A')); pts.append((x0+j*s+s/2,y0+i*s,'A'))
    for i in range(3):
        for j in range(3): pts.append((x0+i*s+s/2,y0+j*s+s/2,'A'))
    b+=R(x0+s,y0+s,s,s,fill='none',stroke=RED,sw=2,rx=0)
    for (x,y,t) in pts:
        b+=C(x,y,10 if t=='M' else 7,'#8fb3ff' if t=='M' else '#f0a35a','#333',1)
    b+=T(x0+1.5*s,y0+3*s+34,'빨간 사각형 = 단위 세포','middle',12,RED)
    lx=x0+3*s+40
    b+=C(lx,60,10,'#8fb3ff','#333',1)+T(lx+16,64,'M','start')+C(lx,95,7,'#f0a35a','#333',1)+T(lx+16,99,'A','start')
    return svg(lx+60,y0+3*s+50,b,maxw=380)

# ---------------- thermochemistry ----------------
def hess_co():
    b=''
    lv=[(40,'C(s) + O₂(g)',0),(118,'CO(g) + ½O₂(g)',1),(230,'CO₂(g)',2)]
    for y,lab,k in lv:
        x1,x2=(60,190) if k!=1 else (150,280)
        if k==2: x1,x2=(60,280)
        b+=L(x1,y,x2,y,w=2.4)+T(x2+6,y+4,lab,'start')
    b+=L(90,44,90,226,c=RED,mk='arR')+T(84,140,'ΔH₃ = ?','end',13,RED,'bold')
    b+=L(170,44,170,114,c=BLUE,mk='arB')+T(176,82,'ΔH₁ = −110.5 kJ','start',12,BLUE)
    b+=L(215,122,215,226,c=BLUE,mk='arB')+T(221,180,'ΔH₂ = −283.0 kJ','start',12,BLUE)
    b+=L(20,20,20,250,c=MUT,mk='ar')+T(14,135,'H','end',13,MUT)
    return svg(420,262,b)

def hess_form():
    b=''; Y0,Y1,Y2=60,120,215
    b+=L(30,25,30,245,c=MUT,mk='ar')+T(24,35,'H','end',13,MUT)
    b+=L(110,Y0,330,Y0,w=2.4)+T(335,Y0+4,'C₂H₄(g) + H₂(g)','start',12)
    b+=L(110,Y1,330,Y1,w=1.8,dash='6 4')+T(335,Y1+4,'2C(s) + 3H₂(g)','start',12)+T(335,Y1+20,'(기준 0)','start',11,MUT)
    b+=L(110,Y2,330,Y2,w=2.4)+T(335,Y2+4,'C₂H₆(g)','start',12)
    b+=L(140,Y1-3,140,Y0+4,c=BLUE,mk='arB')+T(134,(Y0+Y1)/2+4,'+52.3 kJ','end',12,BLUE)
    b+=L(200,Y1+3,200,Y2-4,c=BLUE,mk='arB')+T(194,(Y1+Y2)/2+4,'−84.7 kJ','end',12,BLUE)
    b+=L(290,Y0+3,290,Y2-4,c=RED,w=2.2,mk='arR')+T(284,(Y0+Y2)/2+20,'ΔH = ?','end',13,RED,'bold')
    return svg(450,240,b)

def struct_ch4():
    b=T(10,24,'반응: CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(g)','start',13,INK,'bold')
    y=100
    b+='<g font-size="15">'
    b+=T(70,y-28,'H')+T(70,y+38,'H')+T(70,y+6,'C',size=17,weight='bold')+T(38,y+6,'H')+T(102,y+6,'H')
    b+=L(70,y-22,70,y-10)+L(70,y+10,70,y+24)+L(46,y,60,y)+L(80,y,94,y)
    b+=T(140,y+6,'+  2')+T(175,y+6,'O')+L(186,y-2,198,y-2)+L(186,y+4,198,y+4)+T(208,y+6,'O')
    b+=T(240,y+6,'→')+T(268,y+6,'O')+L(278,y-2,290,y-2)+L(278,y+4,290,y+4)+T(300,y+6,'C',size=17,weight='bold')+L(310,y-2,322,y-2)+L(310,y+4,322,y+4)+T(332,y+6,'O')
    b+=T(364,y+6,'+ 2')+T(392,y+14,'H')+L(400,y+7,409,y-1)+T(415,y-4,'O')+L(421,y-1,430,y+7)+T(436,y+14,'H')
    b+='</g>'
    return svg(460,150,b,maxw=460)

def pv_paths():
    b=''; ox,oy=50,235; sx,sy=9,90
    X=lambda v:ox+v*sx; Y=lambda p:oy-p*sy
    b+=L(ox,oy,ox+330,oy,mk='ar')+L(ox,oy,ox,25,mk='ar')+T(ox+335,oy+4,'V (L)','start')+T(ox+6,22,'P (atm)','start')
    for v in (10,20,30): b+=L(X(v),oy,X(v),oy+5)+T(X(v),oy+18,str(v))
    for p in (1,2): b+=L(ox-5,Y(p),ox,Y(p))+T(ox-9,Y(p)+4,str(p),'end')
    b+=L(X(10),Y(2),X(30),Y(2),c=RED,w=2.2,mk='arR')+L(X(30),Y(2),X(30),Y(1),c=RED,w=2.2,mk='arR')
    b+=L(X(10),Y(2),X(10),Y(1),c=BLUE,w=2.2,mk='arB')+L(X(10),Y(1),X(30),Y(1),c=BLUE,w=2.2,mk='arB')
    for (v,p,n,dx,dy) in [(10,2,'A',-14,-6),(30,2,'C',8,-6),(30,1,'B',8,16),(10,1,'D',-14,16)]:
        b+=C(X(v),Y(p),4,INK)+T(X(v)+dx,Y(p)+dy,n,'middle',14,INK,'bold')
    b+=T(X(20),Y(2)-10,'경로 ACB','middle',12,RED)+T(X(20),Y(1)-8,'경로 ADB','middle',12,BLUE)
    return svg(420,260,b)

def pv_carnot():
    b=''; ox,oy=45,225; g=5/3
    X=lambda v:ox+v*68; Y=lambda p:oy-p*48
    b+=L(ox,oy,ox+340,oy,mk='ar')+L(ox,oy,ox,15,mk='ar')+T(ox+345,oy+4,'V','start')+T(ox+8,18,'P','start')
    VA,VB=1.0,2.0; k=(1/0.6)**(1/(g-1)); VC,VD=VB*k,VA*k
    def iso(v1,v2,c): return 'M'+' L'.join(f'{X(v1+(v2-v1)*i/40):.1f},{Y(c/(v1+(v2-v1)*i/40)):.1f}' for i in range(41))
    def adi(v1,v2,c): return 'M'+' L'.join(f'{X(v1+(v2-v1)*i/40):.1f},{Y(c/(v1+(v2-v1)*i/40)**g):.1f}' for i in range(41))
    b+=P(iso(VA,VB,4.0),c=RED,w=2.4)+P(adi(VB,VC,2.0*VB**g),c=INK,w=2.2)+P(iso(VC,VD,2.4),c=BLUE,w=2.4)+P(adi(VD,VA,(2.4/VD)*VD**g),c=INK,w=2.2)
    pts={"A":(VA,4.0),"B":(VB,2.0),"C":(VC,2.4/VC),"D":(VD,2.4/VD)}
    off={'A':(-12,-4),'B':(10,-6),'C':(6,-10),'D':(-6,-10)}
    for n,(v,p) in pts.items(): b+=C(X(v),Y(p),4,INK)+T(X(v)+off[n][0],Y(p)+off[n][1],n,'middle',14,INK,'bold')
    b+=T(X(1.6),Y(2.7),'T_h','start',12,RED,'bold')+T(X(3.0),Y(0.95)+16,"T_c",'start',12,BLUE,'bold')
    return svg(400,245,b)

def g_vs_t():
    b=''; ox,oy=50,130
    b+=L(ox,oy,ox+320,oy,mk='ar')+L(ox,215,ox,20,mk='ar')+T(ox+325,oy+4,'T (K)','start')+T(ox,15,'ΔG° (kJ)')
    # line from (0,+40) to (1000,-40) ; T*=500
    X=lambda t:ox+t*0.28; Y=lambda g:oy-g*2
    b+=L(X(0),Y(40),X(1050),Y(-44),c=RED,w=2.4)
    for t in (250,500,750,1000): b+=L(X(t),oy,X(t),oy+5)+T(X(t),oy+18,str(t),size=11)
    for g in (40,20,-20,-40): b+=L(ox-4,Y(g),ox,Y(g))+T(ox-7,Y(g)+4,str(g),'end',11)
    b+=C(X(500),oy,4,RED)+T(X(500)+4,oy-8,'T*','start',12,RED,'bold')
    return svg(400,230,b)

# ---------------- phase ----------------
def phase(kind='water'):
    b=''; ox,oy=50,230
    b+=L(ox,oy,ox+330,oy,mk='ar')+L(ox,oy,ox,15,mk='ar')+T(ox+335,oy+4,'T','start')+T(ox,10,'P')
    if kind=='water':
        TP=(130,170); CP=(330,50)
        b+=P(f'M60,222 Q 100,205 {TP[0]},{TP[1]}')
        b+=P(f'M{TP[0]},{TP[1]} Q 240,135 {CP[0]},{CP[1]}')
        b+=P(f'M{TP[0]},{TP[1]} L 118,25')
        b+=T(80,90,'고체')+T(220,85,'액체')+T(250,215,'기체')
        pts={'a':TP,'b':CP,'c':(85,140),'d':(230,180),'e':(200,108)}
        b+=L(ox,120,350,120,c=MUT,dash='4 3')+T(352,124,'1 atm','start',11,MUT)
    else:  # CO2-like, triple point above 1 atm
        TP=(170,140); CP=(320,55)
        b+=P(f'M60,225 Q 120,200 {TP[0]},{TP[1]}')+P(f'M{TP[0]},{TP[1]} Q 250,95 {CP[0]},{CP[1]}')+P(f'M{TP[0]},{TP[1]} L 200,25')
        b+=T(100,90,'고체')+T(250,60,'액체')+T(290,170,'기체')
        b+=L(ox,190,350,190,c=MUT,dash='4 3')+T(352,194,'1 atm','start',11,MUT)
        b+=T(180,155,'5.1 atm, −56.6 ℃','start',11,MUT)
        pts={'a':TP,'b':CP}
    for k,(x,y) in pts.items():
        b+=C(x,y,4,RED,RED)+T(x+7,y-6,k,'start',14,RED,'bold')
    return svg(410,250,b)

def heating():
    b=''; ox,oy=55,215
    b+=L(ox,oy,ox+330,oy,mk='ar')+L(ox,oy,ox,15,mk='ar')+T(ox+335,oy+4,'가한 열','start')+T(ox,10,'온도(℃)')
    pts=[(55,190),(85,150),(130,150),(175,70),(330,70),(370,30)]
    d='M'+' L'.join(f'{x},{y}' for x,y in pts); b+=P(d,c=RED,w=2.4)
    labs=['A','B','C','D','E']
    for i in range(5):
        x=(pts[i][0]+pts[i+1][0])/2; y=(pts[i][1]+pts[i+1][1])/2
        b+=T(x,y-8,labs[i],'middle',14,INK,'bold')
    b+=L(ox-4,150,ox,150)+T(ox-7,154,'0','end',11)+L(ox-4,70,ox,70)+T(ox-7,74,'100','end',11)
    b+=L(ox,150,85,150,c=MUT,dash='3 3')+L(ox,70,175,70,c=MUT,dash='3 3')
    return svg(400,235,b)

# ---------------- biology ----------------
def lac_map():
    b=''; y=60; h=32
    segs=[('P_I',30,'#d7e3ff'),('lacI',70,'#c6d4ff'),('O₃',30,'#ffffff'),('(가)',48,'#ffd0d0'),('P',30,'#cfe8ff'),('(나)',30,'#ffffff'),('lacZ',80,'#fff3a8'),('lacY',62,'#ffd29a'),('lacA',58,'#f0d6f5')]
    x=15
    for lab,w,col in segs:
        b+=R(x,y,w,h,fill=col,rx=0)+T(x+w/2,y+21,lab,'middle',13,INK,'bold' if lab.startswith('(') else 'normal'); x+=w
    b+=L(15,y+h+16,x,y+h+16,c=MUT,w=1)
    b+=T(70,y-12,'조절유전자','middle',12,MUT)+T(330,y-12,'구조유전자','middle',12,MUT)
    b+=L(270,y-6,410,y-6,c=MUT,w=1)
    return svg(x+15,130,b,maxw=460)

def trp_leader():
    b=''; y=70
    b+=L(10,y,440,y,c=MUT,w=2)+T(12,y-10,"5′",'start',12)+T(440,y-10,"3′",'end',12)+T(225,y+52,'trp 리더 mRNA (5′ → 3′, 전사·번역 방향)','middle',11,MUT)
    segs=[('1',60,RED),('2',130,ORG),('3',200,GRN),('4',270,BLUE)]
    for n,x,c in segs:
        b+=R(x,y-9,46,18,fill=c,stroke=c,rx=4)+T(x+23,y+5,n,'middle',13,'#fff','bold')
    b+=T(83,y+32,'UGG UGG','middle',11,RED)+T(330,y+5,'UUUUUUU','start',11,INK)
    b+=P('M83,61 Q 118,10 153,61',c=MUT,w=1.4,dash='3 3')+P('M153,61 Q 188,10 223,61',c=MUT,w=1.4,dash='3 3')+P('M223,61 Q 258,10 293,61',c=MUT,w=1.4,dash='3 3')
    b+=T(118,22,'1:2','middle',11,MUT)+T(188,22,'2:3','middle',11,MUT)+T(258,22,'3:4','middle',11,MUT)
    b+=T(30,y+5,'AUG','middle',11)
    return svg(450,130,b,maxw=460)

def diauxic():
    b=''; ox,oy=50,215
    b+=L(ox,oy,ox+320,oy,mk='ar')+L(ox,oy,ox,15,mk='ar')+T(ox+325,oy+4,'시간','start')+T(ox,10,'log(세포 수)')
    b+=P('M60,195 L160,95 L215,92 L360,35',c=RED,w=2.4)
    b+=L(160,20,160,oy,c=MUT,dash='4 3')+L(215,20,215,oy,c=MUT,dash='4 3')
    b+=T(110,30,'Ⅰ','middle',15,INK,'bold')+T(188,30,'Ⅱ','middle',15,INK,'bold')+T(285,30,'Ⅲ','middle',15,INK,'bold')
    b+=T(110,48,'포도당 + 젖당','middle',11,MUT)+T(285,48,'젖당만 남음','middle',11,MUT)
    return svg(390,235,b)

def binding():
    b=''; ox,oy=50,200
    b+=L(ox,oy,ox+320,oy,mk='ar')+L(ox,oy,ox,15,mk='ar')+T(ox+300,oy+22,'억제인자 농도','middle',12)+T(ox,10,'작동부위 결합률')
    b+=P('M50,200 C 70,60 120,45 360,42',c=BLUE,w=2.4)+T(362,40,'(가)','start',12,BLUE,'bold')
    b+=P('M50,200 C 140,190 200,80 360,62',c=RED,w=2.4)+T(362,66,'(나)','start',12,RED,'bold')
    b+=L(50,197,360,197,c=GRN,w=2.4)+T(362,195,'(다)','start',12,GRN,'bold')
    return svg(400,225,b)

def growth_table():
    rows=[('야생형','○','○','○','○'),('Ⅰ','×','○','○','○'),('Ⅱ','×','×','○','○'),('Ⅲ','×','×','×','○')]
    h='<table class="t"><tr><th>균주</th><th>최소배지</th><th>+ 물질 X</th><th>+ 물질 Y</th><th>+ 물질 Z</th></tr>'
    for r in rows: h+='<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>'
    return h+'</table><div style="font-size:12px;color:#888">○ 생장함, × 생장 못함 (각 첨가는 최소배지에 추가)</div>'

# ---------------- earth ----------------
def cmd_two():
    b=''; ox,oy=50,230
    b+=L(ox,oy,ox+320,oy,mk='ar')+L(ox,oy,ox,15,mk='ar')+T(ox+300,oy+20,'색지수(B−V)','middle',12)+T(ox+2,10,'절대 등급','start',12)
    b+=T(ox-6,30,'밝음','end',11,MUT)+T(ox-6,225,'어두움','end',11,MUT)
    b+=P('M70,40 Q 160,120 330,220',c='#ccc',w=10)+T(300,200,'표준 주계열','start',11,MUT)
    b+=P('M110,85 Q 120,70 135,60 M110,85 Q 180,140 300,215',c=BLUE,w=2.2)+P('M135,60 L 260,45',c=BLUE,w=2.2,dash='5 3')
    b+=P('M175,128 Q 190,110 220,100 L 300,60',c=RED,w=2.2)+P('M175,128 Q 230,170 310,222',c=RED,w=2.2)
    b+=T(140,58,'A','start',14,BLUE,'bold')+T(305,62,'B','start',14,RED,'bold')
    b+=C(110,85,4,BLUE,BLUE)+C(175,128,4,RED,RED)
    return svg(400,250,b)

def orbit():
    b=''; cx,cy=210,140
    b+=C(cx,cy,26,'#bcd3ff','#5577cc',1.5)+T(cx,cy+5,'지구','middle',12)
    A=(cx-70,cy)
    b+=f'<circle cx="{cx}" cy="{cy}" r="70" fill="none" stroke="{INK}" stroke-width="1.6"/>'+T(cx+50,cy-60,'C','middle',13,INK,'bold')
    b+=f'<ellipse cx="{cx-25}" cy="{cy}" rx="45" ry="36" fill="none" stroke="{BLUE}" stroke-width="1.6"/>'+T(cx-25,cy-42,'E₁','middle',13,BLUE,'bold')
    b+=f'<ellipse cx="{cx+45}" cy="{cy}" rx="115" ry="88" fill="none" stroke="{GRN}" stroke-width="1.6"/>'+T(cx+120,cy-70,'E₂','middle',13,GRN,'bold')
    b+=P(f'M{A[0]},{A[1]} C {A[0]},{cy-150} 330,{cy-150} 405,{cy-140}',c=ORG)+P(f'M{A[0]},{A[1]} C {A[0]},{cy+150} 330,{cy+150} 405,{cy+140}',c=ORG)+T(400,cy-118,'P','middle',13,ORG,'bold')
    b+=P(f'M{A[0]},{A[1]} C {A[0]+5},{cy-60} 300,{cy-130} 410,{cy-125}',c=RED,dash='5 3')+T(410,cy-108,'','middle')
    b+=P(f'M{A[0]},{A[1]} C {A[0]+5},{cy+60} 300,{cy+130} 410,{cy+125}',c=RED,dash='5 3')+T(395,cy+112,'H','middle',13,RED,'bold')
    b+=C(*A,5,INK)+T(A[0]-10,A[1]+4,'A','end',14,INK,'bold')+L(A[0],A[1],A[0],A[1]-40,mk='ar')+T(A[0]+6,A[1]-30,'v','start',13)
    return svg(430,285,b)

def pl_graph():
    b=''; ox,oy=55,210
    X=lambda lp:ox+lp*140; Y=lambda M:oy-(-M-1)*36
    b+=L(ox,oy,ox+300,oy,mk='ar')+L(ox,oy,ox,15,mk='ar')+T(ox+150,oy+34,'변광 주기 (일, 로그 눈금)','middle',12)+T(ox+8,14,'절대 등급 M','start',12)
    for lp,lab in [(0,'1'),(1,'10'),(2,'100')]: b+=L(X(lp),oy,X(lp),oy+5)+T(X(lp),oy+18,lab)
    for M in range(-1,-7,-1): b+=L(ox-4,Y(M),ox,Y(M))+T(ox-7,Y(M)+4,str(M),'end',11)+L(ox,Y(M),ox+290,Y(M),c='#eee',w=1)
    for lp in (0,1,2): b+=L(X(lp),oy,X(lp),20,c='#eee',w=1)
    b+=L(X(0),Y(-1.5),X(2),Y(-5.5),c=RED,w=2.4)
    return svg(380,252,b)

def ms_fit():
    b=''; ox,oy=55,230
    X=lambda c:ox+c*180; Y=lambda m:15+m*16
    b+=L(ox,oy,ox+300,oy,mk='ar')+L(ox,oy,ox,10,mk='ar')+T(ox+150,oy+34,'색지수 (B−V)','middle',12)+T(ox+8,12,'등급','start',12)
    for c in (0,0.5,1.0,1.5): b+=L(X(c),oy,X(c),oy+5)+T(X(c),oy+18,str(c),size=11)
    for m in range(0,14,2): b+=L(ox-4,Y(m),ox,Y(m))+T(ox-7,Y(m)+4,str(m),'end',11)
    b+=P(f'M{X(-0.1)},{Y(0.0)} Q {X(0.5)},{Y(3.0)} {X(1.4)},{Y(8.0)}',c='#888',w=2.4)+T(X(1.45),Y(7.4),'표준 주계열 (M)','start',11,MUT)
    b+=P(f'M{X(-0.1)},{Y(5.0)} Q {X(0.5)},{Y(8.0)} {X(1.4)},{Y(13.0)}',c=RED,w=2.4,dash='2 3')+T(X(1.45),Y(12.6),'성단 주계열 (m)','start',11,RED)
    return svg(430,272,b,maxw=430)

def gc_map():
    import random
    random.seed(7); b=''; ox,oy=200,130; s=10
    b+=L(20,oy,390,oy,c=MUT,w=1,mk='ar')+L(ox,240,ox,15,c=MUT,w=1,mk='ar')+T(392,oy+16,'x (kpc)','end',11,MUT)+T(ox+5,18,'z (kpc)','start',11,MUT)
    for x in (-10,0,10): b+=L(ox+x*s,oy-3,ox+x*s,oy+3,c=MUT)+T(ox+x*s,oy+16,str(x),size=10,fill=MUT)
    cx=9
    for _ in range(40):
        r=abs(random.gauss(0,5)); a=random.uniform(0,2*math.pi)
        x=cx+r*math.cos(a); z=r*math.sin(a)*0.9
        b+=C(ox+x*s,oy-z*s,3.2,'#f0a35a','#a66',0.6)
    b+=T(ox,oy+5,'★','middle',18,RED)+T(ox-6,oy-10,'태양','end',11,RED)
    b+=T(300,32,'● 구상 성단','start',11,ORG)
    return svg(400,250,b)

# ---------------- physics ----------------
def diode_sym(x1,y1,x2,y2,lab='',c=INK):
    # anode (x1,y1) -> cathode (x2,y2)
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
    s=11
    tip=(mx+ux*s,my+uy*s); b1=(mx-ux*s+px*s,my-uy*s+py*s); b2=(mx-ux*s-px*s,my-uy*s-py*s)
    out=L(x1,y1,mx-ux*s,my-uy*s,c=c)+L(tip[0],tip[1],x2,y2,c=c)
    out+=f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {b1[0]:.1f},{b1[1]:.1f} {b2[0]:.1f},{b2[1]:.1f}" fill="#fff" stroke="{c}" stroke-width="1.6"/>'
    out+=L(tip[0]+px*s,tip[1]+py*s,tip[0]-px*s,tip[1]-py*s,c=c,w=2.2)
    if lab: out+=T(mx+px*24,my+py*24+4,lab,'middle',12,c,'bold')
    return out

def resistor_h(x1,x2,y,lab=''):
    w=x2-x1; zz=f'M{x1},{y} '+' '.join(f'L{x1+w*(i+0.5)/8:.1f},{y+(-7 if i%2==0 else 7)}' for i in range(8))+f' L{x2},{y}'
    return P(zz,w=1.8)+(T((x1+x2)/2,y-12,lab,'middle',12) if lab else '')
def resistor_v(x,y1,y2,lab=''):
    h=y2-y1; zz=f'M{x},{y1} '+' '.join(f'L{x+(-7 if i%2==0 else 7)},{y1+h*(i+0.5)/8:.1f}' for i in range(8))+f' L{x},{y2}'
    return P(zz,w=1.8)+(T(x+12,(y1+y2)/2+4,lab,'start',12) if lab else '')

def series_circ(V,items):
    # battery on left (+ at top). items on top wire left->right: ('R',label) ('D','f'|'r',label)
    n=len(items); seg=110; W=80+n*seg+40; top=40; bot=170; xl=50; xr=W-40
    b=L(xl,top,xr,top)+L(xr,top,xr,bot)+L(xr,bot,xl,bot)+L(xl,bot,xl,118)+L(xl,92,xl,top)
    b+=L(xl-16,96,xl+16,96,w=2.4)+L(xl-9,112,xl+9,112,w=2.4)+T(xl-22,100,'+','end',13)+T(xl-26,112,V,'end',12)
    x=xl+40
    for it in items:
        b+=R(x-6,top-16,seg-28,32,fill='#fff',stroke='#fff',sw=0)
        if it[0]=='R': b+=resistor_h(x,x+seg-40,top,it[1])
        else:
            if it[1]=='f': b+=diode_sym(x,top,x+seg-40,top,'')
            else: b+=diode_sym(x+seg-40,top,x,top,'')
            b+=T(x+(seg-40)/2,top-18,it[2],'middle',12,INK,'bold')
        x+=seg
    return svg(W,bot+18,b,maxw=420)

def bridge():
    b=''; cx,cy,r=190,130,80
    Tn=(cx,cy-r); Bn=(cx,cy+r); Ln=(cx-r,cy); Rn=(cx+r,cy)
    b+=diode_sym(*Ln,*Tn,'D₁')+diode_sym(*Rn,*Tn,'D₂')+diode_sym(*Bn,*Ln,'D₃')+diode_sym(*Bn,*Rn,'D₄')
    for p in (Tn,Bn,Ln,Rn): b+=C(*p,3,INK)
    b+=L(Ln[0],Ln[1],Ln[0]-45,Ln[1])+C(Ln[0]-49,Ln[1],4,'#fff')+T(Ln[0]-58,Ln[1]+5,'a','end',15,INK,'bold')
    b+=L(Rn[0],Rn[1],Rn[0]+35,Rn[1])+C(Rn[0]+39,Rn[1],4,'#fff')+T(Rn[0]+39,Rn[1]+22,'b','middle',15,INK,'bold')
    xL=360
    b+=L(Tn[0],Tn[1],Tn[0],Tn[1]-22)+L(Tn[0],Tn[1]-22,xL,Tn[1]-22)+L(xL,Tn[1]-22,xL,cy-40)
    b+=resistor_v(xL,cy-40,cy+40,'부하')+L(xL,cy+40,xL,Bn[1]+22)+L(xL,Bn[1]+22,Bn[0],Bn[1]+22)+L(Bn[0],Bn[1]+22,Bn[0],Bn[1])
    b+=T(Tn[0]+10,Tn[1]-28,'출력 단자 X','start',11,MUT)+T(Bn[0]+10,Bn[1]+38,'출력 단자 Y','start',11,MUT)
    b+=T(40,cy-30,'교류 입력','middle',11,MUT)
    return svg(420,262,b)

def waves():
    b=''
    def axes(y,lab):
        return L(60,y,390,y,c=MUT,w=1)+T(18,y+5,lab,'start',13,INK,'bold')
    pts=lambda f,y: 'M'+' L'.join(f'{60+i*1.1:.1f},{y-f(i/300*4*math.pi)*28:.1f}' for i in range(301))
    b+=axes(45,'(가)')+P(pts(lambda t:max(0,math.sin(t)),45),c=BLUE,w=2)
    b+=axes(115,'(나)')+P(pts(lambda t:abs(math.sin(t)),115),c=RED,w=2)
    vals=[];vp=0
    for i in range(301):
        t=i/300*4*math.pi; v=abs(math.sin(t)); vp=max(v,vp*math.exp(-(4*math.pi/300)/2.2)); vals.append(vp)
    smooth=lambda t: vals[min(300,int(round(t/(4*math.pi)*300)))]
    b+=axes(185,'(다)')+P(pts(smooth,185),c=GRN,w=2)
    return svg(400,200,b)

def ripple():
    b=''; ox,oy=55,190
    b+=L(ox,oy,390,oy,c=MUT,mk='ar')+L(ox,oy,ox,15,c=MUT,mk='ar')+T(390,oy+16,'t','end')+T(ox-6,15,'V','end')
    Y=lambda v:oy-(v-6)*55
    d='M'+' L'.join(f'{ox+i:.1f},{Y(7.2+0.6*(1-((i%80)/80))) if i%80>10 else Y(7.2+0.6*((i%80)/10)):.1f}' for i in range(0,330))
    # sawtooth: rise quickly to 7.8 then decay to 7.2
    pts=[]
    for i in range(0,331):
        ph=i%80
        v=7.2+0.6*(ph/12) if ph<12 else 7.8-0.6*((ph-12)/68)
        pts.append(f'{ox+i:.1f},{Y(v):.1f}')
    b+=P('M'+' L'.join(pts),c=RED,w=2.2)
    for v in (7.2,7.8): b+=L(ox,Y(v),390,Y(v),c=MUT,dash='4 3')+T(ox-7,Y(v)+4,f'{v} V','end',11)
    b+=L(ox,Y(7.5),390,Y(7.5),c=BLUE,dash='2 3',w=1)+T(392,Y(7.5)+4,'V_DC = 7.5 V','end',10,BLUE)
    return svg(400,210,b)

def bands():
    b=''
    def panel(x,lab,gap,overlap=False):
        o=''
        if overlap:
            o+=R(x,40,70,70,fill='#cfd9ff')+R(x,95,70,60,fill='#e86b6b',stroke=INK)
        else:
            o+=R(x,40,70,50,fill='#cfd9ff')+R(x,90+gap,70,50,fill='#e86b6b')
            o+=L(x+75,90,x+75,90+gap,c=MUT,w=1)+T(x+80,95+gap/2,f'Eg','start',10,MUT)
        o+=T(x+35,225,lab,'middle',14,INK,'bold')
        return o
    b+=panel(30,'(가)',14)+panel(160,'(나)',0,True)+panel(290,'(다)',60)
    b+=T(200,22,'파랑: 전도띠   빨강: (채워진) 원자가 띠','middle',11,MUT)
    return svg(420,240,b)

def iv3():
    b=''
    def ax(x0,lab):
        return L(x0,150,x0+110,150,c=MUT,mk='ar')+L(x0+25,165,x0+25,30,c=MUT,mk='ar')+T(x0+55,185,lab,'middle',14,INK,'bold')+T(x0+112,165,'v','end',11)+T(x0+30,32,'i','start',11)
    b+=ax(10,'(가)')+P('M10,150 L45,150 L45,35',c=RED,w=2.2)+T(45,165,'V_γ','middle',10)
    b+=ax(150,'(나)')+P('M150,150 L175,150 L175,35',c=RED,w=2.2)
    b+=ax(290,'(다)')+P('M290,150 L325,150 L385,40',c=RED,w=2.2)+T(325,165,'V_γ','middle',10)
    return svg(420,195,b)

def doping(kind='P'):
    b=''; s=62; x0,y0=60,45
    for i in range(3):
        for j in range(3):
            x,y=x0+i*s,y0+j*s
            if i<2: b+=L(x+18,y-4,x+s-18,y-4,c=MUT)+L(x+18,y+4,x+s-18,y+4,c=MUT)
            if j<2: b+=L(x-4,y+18,x-4,y+s-18,c=MUT)+L(x+4,y+18,x+4,y+s-18,c=MUT)
    for i in range(3):
        for j in range(3):
            x,y=x0+i*s,y0+j*s
            if i==1 and j==1: b+=C(x,y,17,'#e86b6b' if kind=='X' else '#8fb3ff')+T(x,y+5,'X','middle',14,'#fff','bold')
            else: b+=C(x,y,16,'#eee')+T(x,y+5,'Si','middle',12)
    cx,cy=x0+s,y0+s
    if kind=='P':
        b+=C(cx+24,cy-22,5,'#3a5bd9','#3a5bd9')+L(cx+28,cy-26,250,25,c=BLUE,w=1)+T(252,22,'남는 전자','start',12,BLUE)
    else:
        b+=C(cx+31,cy-4,6,'#fff',RED,2)+L(cx+35,cy-9,250,25,c=RED,w=1)+T(252,22,'전자가 빈 자리','start',12,RED)
    return svg(360,190,b)


# ---------------- quantum ----------------
import math as _m
def _wave(x0,y0,x1,y1,c,amp=5,n=6):
    L=_m.hypot(x1-x0,y1-y0); ux,uy=(x1-x0)/L,(y1-y0)/L; px,py=-uy,ux; d=f'M{x0:.1f},{y0:.1f}'
    N=60
    for i in range(1,N+1):
        t=i/N; a=amp*_m.sin(2*_m.pi*n*t)
        d+=f' L{x0+ux*L*t+px*a:.1f},{y0+uy*L*t+py*a:.1f}'
    return P(d,c=c,w=1.8)
def compton():
    b=''; cx,cy=210,150
    b+=_wave(20,cy,cx-14,cy,RED,5,7)+T(80,cy-16,'입사 X선 (λ)','middle',12,RED)
    b+=L(cx,cy,400,cy,c=MUT,w=1,dash='4 4')
    th=_m.radians(40); x1,y1=cx+170*_m.cos(th),cy-170*_m.sin(th)
    b+=_wave(cx+12*_m.cos(th),cy-12*_m.sin(th),x1,y1,BLUE,4,9)+T(x1-10,y1-8,"산란 X선 (λ′ > λ)",'end',12,BLUE)
    ph=_m.radians(35); x2,y2=cx+130*_m.cos(ph),cy+130*_m.sin(ph)
    b+=L(cx,cy,x2,y2,c=INK,w=1.8,mk='ar')+T(x2+4,y2+16,'되튄 전자 (p_e)','middle',12)
    b+=P(f'M{cx+45},{cy} A45,45 0 0,0 {cx+45*_m.cos(th):.1f},{cy-45*_m.sin(th):.1f}',c=BLUE,w=1.3)+T(cx+55,cy-14,'θ','start',13,BLUE,'bold')
    b+=P(f'M{cx+38},{cy} A38,38 0 0,1 {cx+38*_m.cos(ph):.1f},{cy+38*_m.sin(ph):.1f}',c=INK,w=1.3)+T(cx+46,cy+22,'φ','start',13,INK,'bold')
    b+=C(cx,cy,9,'#ffe08a')+T(cx,cy+4,'e','middle',11)+T(cx-6,cy+30,'정지 전자','middle',11,MUT)
    return svg(420,265,b)
def coll1d():
    b=''; y=70
    b+=T(210,18,'충돌 전','middle',12,MUT)+C(60,y-20,20,'#dfe8ff',BLUE)+T(60,y-16,'m₁','middle',13)+L(84,y-20,140,y-20,c=BLUE,mk='arB')+T(112,y-30,'v₁,ᵢ','middle',12,BLUE)
    b+=C(260,y-20,26,'#ffe3e3',RED)+T(260,y-16,'m₂','middle',13)+T(260,y+18,'정지 (v₂,ᵢ = 0)','middle',11,MUT)
    b+=L(10,y+30,410,y+30,c=MUT,w=1,dash='4 4')+T(210,y+52,'충돌 후 (1차원 탄성 충돌)','middle',12,MUT)
    b+=C(60,y+85,20,'#dfe8ff',BLUE)+T(60,y+89,'m₁','middle',13)+L(84,y+85,130,y+85,c=BLUE,mk='arB')+T(108,y+75,'v₁,f','middle',12,BLUE)
    b+=C(260,y+85,26,'#ffe3e3',RED)+T(260,y+89,'m₂','middle',13)+L(290,y+85,370,y+85,c=RED,mk='arR')+T(330,y+75,'v₂,f','middle',12,RED)
    return svg(420,180,b)
def coll2d():
    b=''; cx,cy=200,110
    b+=C(50,cy,16,'#dfe8ff',BLUE)+T(50,cy+4,'m','middle',12)+L(70,cy,cx-22,cy,c=BLUE,mk='arB')+T(120,cy-12,'v₁,ᵢ','middle',12,BLUE)
    b+=C(cx,cy,16,'#ffe3e3',RED)+T(cx,cy+4,'m','middle',12)+T(cx,cy+34,'정지','middle',11,MUT)
    b+=L(cx,cy,390,cy,c=MUT,w=1,dash='4 4')
    th=_m.radians(35); ph=_m.radians(55)
    b+=L(cx+18*_m.cos(th),cy-18*_m.sin(th),cx+150*_m.cos(th),cy-150*_m.sin(th),c=BLUE,mk='arB')+T(cx+160*_m.cos(th),cy-160*_m.sin(th),'v₁,f','middle',12,BLUE)
    b+=L(cx+18*_m.cos(ph),cy+18*_m.sin(ph),cx+110*_m.cos(ph),cy+110*_m.sin(ph),c=RED,mk='arR')+T(cx+122*_m.cos(ph)+10,cy+118*_m.sin(ph),'v₂,f','middle',12,RED)
    b+=P(f'M{cx+50},{cy} A50,50 0 0,0 {cx+50*_m.cos(th):.1f},{cy-50*_m.sin(th):.1f}',c=BLUE,w=1.2)+T(cx+58,cy-12,'θ','start',13,BLUE,'bold')
    b+=P(f'M{cx+42},{cy} A42,42 0 0,1 {cx+42*_m.cos(ph):.1f},{cy+42*_m.sin(ph):.1f}',c=RED,w=1.2)+T(cx+46,cy+28,'φ','start',13,RED,'bold')
    return svg(420,220,b)
def bbody():
    b=''; ox,oy=50,210; W,H=340,180
    b+=L(ox,oy,ox+W,oy,mk='ar')+L(ox,oy,ox,oy-H,mk='ar')+T(ox+W-4,oy+18,'파장 λ','end',12)+T(ox+4,oy-H-4,'복사 세기','start',12)
    hc_k=1.4388e-2
    def plank(l,T): return 1/(l**5*(_m.exp(hc_k/(l*T))-1))
    Ts=[(6000,RED,'6000 K'),(5000,ORG,'5000 K'),(4000,BLUE,'4000 K')]
    mx=max(plank(2.9e-3/6000,6000),1)
    lmax=2.5e-6
    for Tk,col,lab in Ts:
        d=''
        for i in range(1,121):
            l=lmax*i/120; y=plank(l,Tk)/mx
            X=ox+W*0.95*l/lmax; Y=oy-H*0.9*y
            d+=('M' if i==1 else ' L')+f'{X:.1f},{Y:.1f}'
        b+=P(d,c=col,w=2)
        lp=2.9e-3/Tk; X=ox+W*0.95*lp/lmax; Y=oy-H*0.9*plank(lp,Tk)/mx
        b+=C(X,Y,3,col,col)+T(X+6,Y-6,lab,'start',11,col)
    return svg(420,230,b)
def bloch():
    b=''; cx,cy,r=200,125,85
    b+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#eef1fc" stroke="{BLUE}" stroke-width="1.6"/>'
    b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="24" fill="none" stroke="{BLUE}" stroke-width="1" stroke-dasharray="4 3"/>'
    b+=L(cx,cy,cx,cy-r-18,c=INK,w=1.3,mk='ar')+T(cx+8,cy-r-14,'z','start',12)
    b+=L(cx,cy,cx+r+22,cy,c=INK,w=1.3,mk='ar')+T(cx+r+26,cy+4,'y','start',12)
    b+=L(cx,cy,cx-50,cy+40,c=INK,w=1.3,mk='ar')+T(cx-58,cy+50,'x','middle',12)
    b+=C(cx,cy-r,4,INK,INK)+T(cx+10,cy-r+16,'|0⟩ (θ = 0)','start',12)
    b+=C(cx,cy+r,4,INK,INK)+T(cx+10,cy+r-6,'|1⟩ (θ = π)','start',12)
    tx,ty=cx+55,cy-58
    b+=L(cx,cy,tx,ty,c=RED,w=2,mk='arR')+T(tx+6,ty-4,'|ψ⟩','start',13,RED,'bold')
    b+=P(f'M{cx},{cy-30} A30,30 0 0,1 {cx+30*0.69:.1f},{cy-30*0.73:.1f}',c=RED,w=1.2)+T(cx+8,cy-36,'θ','start',12,RED)
    b+=T(cx,cy+r+30,'|ψ⟩ = cos(θ/2)|0⟩ + e<tspan baseline-shift="super" font-size="70%">iφ</tspan> sin(θ/2)|1⟩','middle',12,MUT)
    return svg(420,250,b)

FIGS={'compton':compton,'coll1d':coll1d,'coll2d':coll2d,'bbody':bbody,'bloch':bloch,

 'cell_sc':lambda:cell('sc'),'cell_bcc':lambda:cell('bcc'),'cell_fcc':lambda:cell('fcc'),'cell_nacl':lambda:cell('nacl'),'cell_cscl':lambda:cell('cscl'),
 'cell_perov':lambda:cell('perov'),'cell_nial':lambda:cell('nial'),'cell_edge':lambda:cell('edgeb'),'lattice2d':lattice2d,
 'hess_co':hess_co,'hess_form':hess_form,'struct_ch4':struct_ch4,'pv_paths':pv_paths,'pv_carnot':pv_carnot,'g_vs_t':g_vs_t,
 'phase_water':lambda:phase('water'),'phase_co2':lambda:phase('co2'),'heating':heating,
 'lac_map':lac_map,'trp_leader':trp_leader,'diauxic':diauxic,'binding':binding,'growth_table':growth_table,
 'cmd_two':cmd_two,'orbit':orbit,'pl_graph':pl_graph,'ms_fit':ms_fit,'gc_map':gc_map,
 'circ_f':lambda:series_circ('5 V',[('R','1 kΩ'),('D','f','D')]),
 'circ_r':lambda:series_circ('5 V',[('R','1 kΩ'),('D','r','D')]),
 'circ_2f':lambda:series_circ('5 V',[('R','1 kΩ'),('D','f','D₁'),('D','f','D₂')]),
 'circ_fr':lambda:series_circ('5 V',[('R','1 kΩ'),('D','f','D₁'),('D','r','D₂')]),
 'circ_ex':lambda:series_circ('V_A = 5 V',[('R','500 Ω'),('D','f','D')]),
 'bridge':bridge,'waves':waves,'ripple':ripple,'bands':bands,'iv3':iv3,'dope_n':lambda:doping('P'),'dope_p':lambda:doping('B'),
}
