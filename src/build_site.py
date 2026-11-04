import yaml, json, base64, glob, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
QS=[]
import figs
FIG={k:f() for k,f in figs.FIGS.items()}
for s,f in [('phys','q_phys'),('chem','q_chem'),('bio','q_bio'),('earth','q_earth'),('chem','x_chem'),('bio','x_bio'),(None,'x_ep'),('phys','q_qm')]:
    for q in yaml.safe_load(open(f+'.yaml')):
        if s: q['s']=s
        assert q.get('s') in ('phys','chem','bio','earth'), q['id']
        if q.get('fig'): assert q['fig'] in FIG, q['id']
        if q['t']!='essay' and 'lv' not in q: raise SystemExit('no lv '+q['id'])
        if q['t']=='essay': q['lv']=0
        for k in ('q','ex','sol'):
            if k in q and isinstance(q[k],str): q[k]=q[k].rstrip('\n')
        if q['t']=='mc':
            assert isinstance(q['a'],int) and 0<=q['a']<len(q['c']), q['id']
            q['c']=[str(c) for c in q['c']]
        if q['t']=='num': q['a']=float(q['a'])
        if q['t']=='txt': q['a']=[str(x) for x in q['a']]
        q['ref']=[str(r) for r in q.get('ref',[])]
        QS.append(q)
CX=yaml.safe_load(open('cx.yaml'))
for q in QS:
    if q['t']=='mc':
        assert q['id'] in CX and len(CX[q['id']])==len(q['c']), 'cx '+q['id']
        q['cx']=[str(x) for x in CX[q['id']]]
from mathify import mathify
for q in QS:
    for k in ('q','ex'): q[k]=mathify(q.get(k)) if q.get(k) else q.get(k)
    if q.get('sol'): q['sol']=mathify(q['sol'],True)
    if q['t']=='mc': q['c']=[mathify(c) for c in q['c']]; q['cx']=[mathify(c) for c in q['cx']]
    if q.get('kp'): q['kp']=[mathify(str(x)) for x in q['kp']]
ids=[q['id'] for q in QS]; assert len(ids)==len(set(ids)),'dup id'
KB=yaml.safe_load(open('kb.yaml'))
for k in KB: k['b']=mathify(k['b'],True)
for k in KB: k['kw']=[str(x) for x in k['kw']]; k['ref']=[str(r) for r in k.get('ref',[])]
NB={'n1':'생물 1차시 필기 (유전자와 단백질·비들테이텀·헤모글로빈)','n2':'생물 1차시 백신 수업 (영양요구성·원핵 RNA 중합효소·σ·rho)','n3':'1학기 중심원리 필기 (전사·번역·tRNA·리보솜)','n4':'생물 2차시 필기 (중심원리 보충·진핵/원핵 조절)','n5':'젖당 오페론 정리 (구조·알로락토오스·cis/trans)','n6':'박신 학원: 유도/구성/불능 판정·생장 그래프','n7':'심화 1~4 (알로락토오스·more/less·Oᶜ·보조작동자)','n8':'서술형 기출 (작동자 실험·도메인)','n9':'3차시 lac: 조절유전자 돌연변이·포도당 효과·이중생장','n10':'3차시 trp 오페론·감쇠'}
SRC={
 'bio5':dict(n='생물 5차시 PPT 「유전자와 단백질」',short='생물 5차시 PPT',s='bio',ic='📘'),
 'bio6':dict(n='생물 6차시 PPT 「유전자 발현의 조절」',short='생물 6차시 PPT',s='bio',ic='📘'),
 'nb':dict(n='내 필기 · 생물 (1-2 기말 복습노트)',short='내 필기',s='bio',note=True,labels=NB),
 'e4':dict(n='지학 「04) 케플러 3법칙, 궤도역학」 — 인공위성·탐사선의 궤도',short='지학 궤도역학',s='earth',ic='📗'),
 'c1':dict(n='지학 행성우주과학 III-1 「성단」',short='지학 III-1 성단',s='earth',ic='📗'),
 'c2':dict(n='지학 행성우주과학 III-2 「우리은하의 규모와 구조」',short='지학 III-2 우리은하',s='earth',ic='📗'),
 'ne':dict(n='내 필기 · 지학 (성단)',short='내 필기',s='earth',note=True,labels={'n1':'지학 성단 필기 (분류·색지수·전향점·기출)'}),
 'q':dict(n='화학 Ch.3 「열화학과 반응의 자발성」 학습지',short='화학 Ch.3 학습지',s='chem',ic='📙'),
 'r1':dict(n='화학 「2. 액체와 고체」 학습지 (고체·상평형·문제)',short='화학 고체 학습지',s='chem',ic='📙'),
 'r2':dict(n='화학 CHEMTAK 손필기본 (Solids · Phase Transitions)',short='CHEMTAK',s='chem',ic='📙'),
 'nc':dict(n='내 필기 · 화학 (열역학·열화학)',short='내 필기',s='chem',note=True,labels={'n1':'화학 열역학 필기 (제1법칙·Cp/Cv·가역/비가역)','n2':'화학 열화학 필기 (열량계·헤스·반응 엔탈피)'}),
 's2':dict(n='물리 「6. 다이오드」 수업 PPT',short='물리 다이오드 PPT',s='phys',ic='📕'),
 'qm':dict(n='물리 「양자역학」 수업 PPT·필기 (흑체 복사 ~ 양자 컴퓨터)',short='물리 양자역학',s='phys',ic='📕'),
 's1':dict(n='물리 「다이오드 추가」 PPT (근사 모델·예제)',short='물리 다이오드 추가',s='phys',ic='📕'),
}
IMG={}
import shutil as _sh
for _f in ('katex.min.js','contrib/auto-render.min.js'): None  # katex files are kept in docs/
import shutil
SITE=os.path.join(HERE,'..','docs'); os.makedirs(SITE+'/img',exist_ok=True)
for f in sorted(glob.glob(os.path.join(HERE,'..','docs','img','*.webp'))):
    key=os.path.basename(f)[:-5]
    IMG[key]='img/'+key+'.webp'
    dst=SITE+'/img/'+key+'.webp'
    if not os.path.exists(dst) or os.path.getsize(dst)!=os.path.getsize(f): shutil.copy(f,dst)
def pkey(p):
    if p.isdigit(): return (0,int(p),0)
    import re as _r
    m=_r.match(r'n(\d+)(?:-(\d+))?$',p); return (1,int(m.group(1)),int(m.group(2) or 0))
for k,S in SRC.items():
    ps=[key.split('_',1)[1] for key in IMG if key.split('_',1)[0]==k]
    S['pages']=sorted(ps,key=pkey)
    if S.get('note'):
        for pg in S['pages']:
            if '-' in pg:
                base,i=pg.split('-'); N=sum(1 for q in S['pages'] if q.startswith(base+'-'))
                S['labels'][pg]=S['labels'][base]+f' · 확대 {i}/{N}'
    assert S['pages'],k
# validate refs
bad=[]
for x in QS+KB:
    for r in x['ref']:
        src,pg=r.split(':')
        if src+'_'+pg not in IMG: bad.append((x['id'],r))
if bad: print('BAD REFS',bad); sys.exit(1)
import datetime
UPD=(datetime.datetime.utcnow()+datetime.timedelta(hours=9)).strftime('%m/%d %H:%M')
data='const UPDATED='+json.dumps(UPD)+';\nconst QS='+json.dumps(QS,ensure_ascii=False)+';\nconst KB='+json.dumps(KB,ensure_ascii=False)+';\nconst SRC='+json.dumps(SRC,ensure_ascii=False)+';\nconst FIG='+json.dumps(FIG,ensure_ascii=False)+';\nconst IMG='+json.dumps(IMG)+';'
open(SITE+'/data.js','w').write(data)
t=open('template.html').read().replace('<script>\n/*__DATA__*/\n</script>','<script src="data.js"></script>')
assert 'data.js' in t
out=SITE+'/index.html'
open(out,'w').write(t)
from collections import Counter
print('figQ',sum(1 for q in QS if q.get('fig')));print('Q',len(QS),Counter((q['s'],q['t']) for q in QS)); print('KB',len(KB),'IMG',len(IMG)); print('data KB',os.path.getsize(SITE+'/data.js')/1e3,'index KB',os.path.getsize(out)/1e3)
