OUT=[]
def M(i,s,u,lv,q,opts,ex,ref):
    OUT.append(dict(id=i,s=s,u=u,t='mc',lv=lv,q=q,c=[o[0] for o in opts],cx=[o[1] for o in opts],a=0,ex=ex,ref=ref))
def B(i,s,u,lv,q,bg,ref,ex=''):
    d=dict(id=i,s=s,u=u,t='mc',lv=lv,q=q,bg=bg,ref=ref)
    if ex: d['ex']=ex
    OUT.append(d)
def N(i,s,u,lv,q,a,tol,unit,ex,ref):
    OUT.append(dict(id=i,s=s,u=u,t='num',lv=lv,q=q,a=a,tol=tol,unit=unit,ex=ex,ref=ref))
def T(i,s,u,lv,q,a,ex,ref):
    OUT.append(dict(id=i,s=s,u=u,t='txt',lv=lv,q=q,a=a,ex=ex,ref=ref))
def E(i,s,u,q,kp,sol,ref):
    OUT.append(dict(id=i,s=s,u=u,t='essay',q=q,kp=kp,sol=sol,ref=ref))
def S(i,s,u,lv,q,parts,ref,fig=None):
    d=dict(id=i,s=s,u=u,t='set',lv=lv,q=q,parts=parts,ref=ref)
    if fig: d['fig']=fig
    OUT.append(d)
def pn(p,a,tol,unit,pt,sol): return dict(p=p,t='num',a=a,tol=tol,unit=unit,pt=pt,sol=sol)
def pt_(p,a,pt,sol): return dict(p=p,t='txt',a=a,pt=pt,sol=sol)
def pe(p,pt,kp,sol): return dict(p=p,t='essay',pt=pt,kp=kp,sol=sol)
