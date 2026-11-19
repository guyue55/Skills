#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提交课程满意度调查（course_surveys）。用法: submit_survey.py <survey_url>
每题选正面项：满意度类 value=5，平衡/中立类 value=3，N/A 类 value=0 不选。"""
import os, sys, json, time
sys.path.insert(0, '/Users/apple/.workbuddy/skills/browser-automation-cdp/scripts')
from cdp import CDPClient

PORT = int(os.environ.get('GCA_PORT', '9333'))
URL = sys.argv[1] if len(sys.argv) > 1 else None
if not URL:
    print(json.dumps({'error': '用法: submit_survey.py <survey_url>'}, ensure_ascii=False)); sys.exit(2)

c = CDPClient(port=PORT, timeout=30)
c.ensure_page()
c.navigate(URL, timeout=30)
time.sleep(3)

# 按 name 分组，选每组最高 value（满意度=5，平衡题该组最高是3则有3，N/A=0 不选）
PICK = r'''(function(){
  var groups={};
  document.querySelectorAll('input[type=radio]').forEach(function(r){
    var n=r.name||''; if(!n) return;
    var m=n.match(/\[(\d+)\]\[response\]/); var k=m?m[1]:n;
    var v=parseInt(r.value,10);
    if(!groups[k]||v>groups[k].v) groups[k]={el:r,v:v};
  });
  var picked=[];
  Object.keys(groups).forEach(function(k){
    var g=groups[k];
    if(g.v===0) return; // N/A 不选
    g.el.click(); picked.push(k+':'+g.v);
  });
  return JSON.stringify(picked);
})()'''
ev = c.evaluate(PICK)
picked = json.loads(ev.get('value', '[]'))

time.sleep(0.8)
# 点 Submit（shadow DOM 递归找 ql-button 文案 Submit）
SUBMIT = r'''(function(){
  var found=null;
  function w(x,d){if(d>15||found)return;try{Array.from(x.querySelectorAll('*')).forEach(function(e){
    if(found)return; if(e.shadowRoot)w(e.shadowRoot,d+1);
    var t=(e.textContent||'').trim();
    if((e.tagName==='QL-BUTTON'||e.tagName==='BUTTON')&&/^submit$/i.test(t)) found=e;
  });}catch(y){}}
  w(document,0); if(!found) return 'NO_BUTTON';
  if(found.hasAttribute('disabled')) return 'DISABLED';
  found.click(); return 'CLICKED';
})()'''
st = c.evaluate(SUBMIT).get('value')
time.sleep(3)
text = c.page_text(6000)
done = 'Completed:' in text or '已完成:' in text or 'submitted' in text.lower() or 'thank' in text.lower()
print(json.dumps({'url': URL, 'picked': picked, 'submit': st, 'done': done,
                  'snippet': text[:400]}, ensure_ascii=False, indent=2))
