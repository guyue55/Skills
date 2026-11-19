#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单连接完成 quiz: 导航->retake->点选->提交->读结果。全程不重复 goto。"""
import sys,os,json,time
sys.path.insert(0,'/Users/apple/.workbuddy/skills/browser-automation-cdp/scripts')
sys.path.insert(0,'/Users/apple/.workbuddy/skills/google-course-automator/scripts')
from cdp import CDPClient
import gca

url=sys.argv[1]; ansfile=sys.argv[2]
answers=json.load(open(ansfile,encoding='utf-8'))
c=CDPClient(port=int(os.environ.get("GCA_PORT","9333")),timeout=30); c.ensure_page()
def ev(expr,default=None):
    try:
        raw=c.evaluate(expr).get('value')
        if raw is None: return default
        if isinstance(raw,(dict,list)): return raw
        try: return json.loads(raw)
        except Exception: return raw
    except Exception as e:
        return default

# 导航
try:c.navigate(url,timeout=30)
except Exception:pass
time.sleep(3)
# retake（递归 ql-button.retake-button）
RETAKE=r"""(function(){let b=null;const s=new Set();function w(x,d){if(!x||s.has(x)||d>20||b)return;s.add(x);for(const e of (x.querySelectorAll?x.querySelectorAll('*'):[])){if(e.shadowRoot)w(e.shadowRoot,d+1);if(b)return;const tag=(e.tagName||'').toLowerCase();if(tag==='ql-button'&&(e.className||'').includes('retake-button')){b=e;return}}}w(document,0);if(!b)return 'NONE';b.scrollIntoView({block:'center'});b.click();return 'RETAKE';})()"""
prep=ev(RETAKE,'NONE')
if prep=='RETAKE': time.sleep(3)
# 等待题目渲染
for _ in range(15):
    seq=ev(gca.LIN_JS,[]) or []
    if sum(1 for x in seq if x.get('k')=='S')>=len(answers): break
    time.sleep(0.8)
# 诊断：目标选项当前 on 状态
DIAG=r"""(function(){const items=ITEMS;function clean(s){return (s||'').replace(/\s+/g,' ').trim()}
let seq=[];function lin(n,d){if(d>25||!n)return;const tag=n.tagName||'';if(tag==='QL-ITEM-STEM')seq.push({k:'S',t:clean(n.innerText||n.textContent)});else if(tag==='MD-RADIO'||tag==='MD-CHECKBOX')seq.push({k:'O',el:n,t:tag,l:clean(n.getAttribute('aria-label')||n.getAttribute('data-aria-label'))});if(n.shadowRoot)lin(n.shadowRoot,d+1);for(const ch of (n.children||[]))lin(ch,d+1)}lin(document,0);
let groups=[],cur=null;for(const x of seq){if(x.k==='S'){cur={stem:clean(x.t).toLowerCase(),opts:[]};groups.push(cur)}else if(x.k==='O'&&cur)cur.opts.push(x)}
let out=[];items.forEach((it,i)=>{let g=groups.find(gg=>it.kw&&gg.stem.includes(it.kw))||groups[i];if(!g){out.push('Q'+i+':NOGROUP');return}it.opts.forEach(w=>{let o=g.opts.find(oo=>oo.l===w||(it.fuzzy&&oo.l.indexOf(w)>=0));if(!o){out.push('Q'+i+':NOMATCH:'+w.slice(0,20));return}let on=o.el.checked===true||o.el.getAttribute('aria-checked')==='true'||o.el.hasAttribute('checked');out.push('Q'+i+':'+w.slice(0,18)+':on='+on)})});
return JSON.stringify(out)})()"""
diag=ev(DIAG.replace('ITEMS',json.dumps(answers,ensure_ascii=False)),[])
print('DIAG:',json.dumps(diag,ensure_ascii=False),flush=True)
# 点选（三轮）
expr=gca.CLICK_JS_TMPL.replace('ITEMS',json.dumps(answers,ensure_ascii=False))
res={}
for rnd in range(3):
    res=ev(expr,{}) or {}
    time.sleep(0.7)
time.sleep(1)
SUBMIT=r"""(function(){let b=null;const s=new Set();function w(x,d){if(!x||s.has(x)||d>20||b)return;s.add(x);for(const e of (x.querySelectorAll?x.querySelectorAll('*'):[])){if(e.shadowRoot)w(e.shadowRoot,d+1);if(b)return;const tag=(e.tagName||'').toLowerCase();if(tag==='ql-button'&&(e.className||'').includes('submit-button')){b=e;return}}}w(document,0);if(!b)return 'NO';b.scrollIntoView({block:'center'});b.click();return 'SUBMITTED';})()"""
sub=ev(SUBMIT,'NO'); time.sleep(4)
RESULT=r"""(function(){let r=[];function w(root,d){if(d>18)return;root.querySelectorAll('*').forEach(e=>{if(e.children.length===0){let t=(e.textContent||'').trim();if(/score|passed|Congrat|Unfortunately|correct|incorrect|正确|错误/i.test(t)&&t.length<160)r.push(t)}if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);return JSON.stringify([...new Set(r)].slice(0,30))})()"""
result=ev(RESULT,[])
print(json.dumps({'prep':prep,'click':res,'submit':sub,'result':result},ensure_ascii=False,indent=1),flush=True)
