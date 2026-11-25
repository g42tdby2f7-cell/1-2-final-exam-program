import sys,os,yaml; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
import h
exec(open(os.path.join(D,'a_bt.py'),encoding='utf-8').read(),{})
ids=[q['id'] for q in h.OUT]; assert len(ids)==len(set(ids))
yaml.safe_dump(h.OUT,open(os.path.join(D,'..','s_bt.yaml'),'w',encoding='utf-8'),allow_unicode=True,sort_keys=False)
print(len(h.OUT))
