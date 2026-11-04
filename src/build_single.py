import re,base64,json,os,sys
S=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs')
OUT=sys.argv[1] if len(sys.argv)>1 else '1-2기말_복습프로그램.html'
html=open(S+'/index.html',encoding='utf-8').read()
data=open(S+'/data.js',encoding='utf-8').read()
m=re.search(r'const IMG=(\{.*\});',data); IMG=json.loads(m.group(1))
for k,v in IMG.items():
    IMG[k]='data:image/webp;base64,'+base64.b64encode(open(S+'/'+v,'rb').read()).decode()
data=data[:m.start()]+'const IMG='+json.dumps(IMG)+';'+data[m.end():]
for js in ('katex.min.js','auto-render.min.js'):
    t='<script src="'+js+'"></script>'; assert t in html
    html=html.replace(t,'<script>'+open(S+'/'+js,encoding='utf-8').read().replace('</script','<\\/script')+'</script>')
tag='<script src="data.js"></script>'; assert tag in html
out=html.replace(tag,'<script>\n'+data.replace('</script','<\\/script')+'\n</script>')
open(OUT,'w',encoding='utf-8').write(out)
print(OUT,os.path.getsize(OUT)/1e6,'MB')
