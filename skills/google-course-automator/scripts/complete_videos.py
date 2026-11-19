#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量完成指定 course_template 的视频活动（点 complete_button）。用法: complete_videos.py <template_id>"""
import os,subprocess,sys,json,time
GCA='/Users/apple/.workbuddy/skills/google-course-automator/scripts/gca.py'
BASE='https://www.skills.google'; PORT=os.environ.get('GCA_PORT','9333')
tid=sys.argv[1] if len(sys.argv)>1 else '327'
url=BASE+'/course_templates/{}?locale=zh'.format(tid)
p=subprocess.run([sys.executable,GCA,'read-acts',url,'--port',PORT],capture_output=True,text=True,timeout=60)
d=json.loads(p.stdout)
videos=[a['href'] for a in (d.get('acts') or []) if '/video/' in (a.get('href') or '') and not a.get('complete')]
print('待完成视频',len(videos),flush=True)

sys.path.insert(0,'/Users/apple/.workbuddy/skills/browser-automation-cdp/scripts')
from cdp import CDPClient
c=CDPClient(port=int(os.environ.get("GCA_PORT","9333")),timeout=30); c.ensure_page()
COMPLETE='''(function(){var h=null;const s=new Set();function w(x,d){if(!x||s.has(x)||d>20||h)return;s.add(x);for(const e of (x.querySelectorAll?x.querySelectorAll('*'):[])){if(e.shadowRoot)w(e.shadowRoot,d+1);if(h)return;const tag=(e.tagName||'').toLowerCase();if(tag==='ql-button'&&/complete_button/i.test(e.getAttribute('href')||'')){h=e;return}}}w(document,0);if(!h)return 'NONE';if(h.hasAttribute('disabled'))return 'DISABLED';h.scrollIntoView({block:'center'});h.click();return 'CLICKED';})()'''
def nav(u):
    try:c.navigate(u,timeout=30)
    except Exception:pass
    time.sleep(1.8)
ok=0
for i,h in enumerate(videos,1):
    nav(BASE+h)
    st=c.evaluate(COMPLETE).get('value')
    print('[{}/{}] {} {}'.format(i,len(videos),h.split('/')[-1].split('?')[0],st),flush=True)
    if st=='CLICKED': ok+=1
    time.sleep(0.5)
print('完成',ok,'/',len(videos))
