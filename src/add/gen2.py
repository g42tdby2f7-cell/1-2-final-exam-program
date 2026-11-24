import sys,os,yaml; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
import h
for f in ['a_b2','a_bio8','a_b8n','a_n24','a_tak','a_tm','a_ks','a_pe']: exec(open(os.path.join(D,f+'.py'),encoding='utf-8').read(),{})
M={'b2e01':[4],'b2e02':[2],'b2e03':[6,7],'b2e04':[7],'b2e05':[8],'b2e06':[8,9],'b2e07':[11],'b2e08':[12],'b2e09':[15],'b2e10':[14],'b2e11':[16],'b2e12':[17,19],'b2e13':[18],'b2e14':[20],'b2e15':[21,22],'b2e16':[6,10],'b2d01':[25],'b2d02':[26],'b2d03':[27],'b2d04':[30],'b2d05':[23]}
for q in h.OUT:
    for n in M.get(q['id'],[]): q['ref'].append(f'bio8:{n}')
ids=[q['id'] for q in h.OUT]; assert len(ids)==len(set(ids))
yaml.safe_dump(h.OUT,open(os.path.join(D,'..','s_b2.yaml'),'w',encoding='utf-8'),allow_unicode=True,sort_keys=False)
print(len(h.OUT))
