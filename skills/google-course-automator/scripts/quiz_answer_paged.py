#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分页式 Quiz 作答（老课：Previous/Next 翻页，最后一题 Next 后才出现 Submit）。
用法: quiz_answer_paged.py <url> @answers.json
流程: goto -> retake -> 一次性点选所有题(CLICK_JS_TMPL) -> 循环点 Next 直到 submit-button 出现 -> 点选最后一题 -> Submit -> 读结果。
与 quiz_answer_stable.py 区别: 后者针对"一页全题"的新课(直接有 submit-button)；本脚本针对分页老课。
答案 JSON 格式同 gca.py: [{kw, opts, fuzzy?},...]，kw 用题干原文子串，opts 用选项原文。
"""
import os, sys, json, time, re
sys.path.insert(0, '/Users/apple/.workbuddy/skills/google-course-automator/scripts')
sys.path.insert(0, '/Users/apple/.workbuddy/skills/browser-automation-cdp/scripts')
import gca
from cdp import CDPClient

PORT = int(os.environ.get('GCA_PORT', '9333'))
URL = sys.argv[1]
ANS = sys.argv[2] if len(sys.argv) > 2 else None
if not ANS:
    print(json.dumps({'error':'用法: quiz_answer_paged.py <url> @answers.json'},ensure_ascii=False)); sys.exit(2)
answers = json.load(open(gca.os.path.expanduser(ANS[1:] if ANS.startswith('@') else ANS), encoding='utf-8'))

RETAKE = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.retake-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(b){b.click();return 'RETAKE';}return 'NONE';})()"""
START = r"""(function(){let b=document.querySelector('a.start-button');if(b){b.click();return 'START';}return 'NONE';})()"""
NEXT = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.next-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(!b)return 'NONE';if(b.hasAttribute('disabled'))return 'DISABLED';b.scrollIntoView({block:'center'});b.click();return 'NEXT';})()"""
HAS_SUBMIT = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.submit-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);return b? 'YES':'NO';})()"""
SUBMIT = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.submit-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(!b)return 'NO';if(b.hasAttribute('disabled'))return 'DISABLED';b.click();return 'SUBMITTED';})()"""
RESULT = r"""(function(){var out=[];function w(root,d){if(d>18)return;root.querySelectorAll('*').forEach(function(e){if(e.children.length===0){var t=(e.textContent||'').trim();if(/score|pass|correct|incorrect|congrat|unfortunately/i.test(t)&&t.length<160)out.push(t);}if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);return JSON.stringify([...new Set(out)].slice(0,25));})()"""

c = gca.client(PORT)
gca.goto(c, URL, wait=2.5)
prep = gca.ev(c, RETAKE, 'NONE')
if prep == 'NONE':
    prep = gca.ev(c, START, 'NONE')
if prep != 'NONE':
    time.sleep(2)
# 等题目渲染
for _ in range(12):
    seq = gca.evj(c, gca.LIN_JS, []) or []
    if sum(1 for x in seq if x.get('k') == 'S') >= len(answers):
        break
    time.sleep(0.8)
# 一次性点选所有题（可能跨页，LIN_JS 读全部 DOM）
expr = gca.CLICK_JS_TMPL.replace('ITEMS', json.dumps(answers, ensure_ascii=False))
click = {}
for _ in range(3):
    click = gca.evj(c, expr, {}); time.sleep(0.6)
# 循环点 Next，直到 submit-button 出现
next_log = []
for i in range(30):
    if gca.ev(c, HAS_SUBMIT, 'NO') == 'YES':
        break
    n = gca.ev(c, NEXT, 'NONE')
    next_log.append(n)
    if n in ('NONE', 'DISABLED'):
        break
    time.sleep(1.0)
# submit 出现后再点选一次（最后一题可能刚渲染）
for _ in range(2):
    click = gca.evj(c, expr, {}); time.sleep(0.5)
time.sleep(0.8)
sub = gca.ev(c, SUBMIT, 'NO')
time.sleep(3)
result = gca.evj(c, RESULT, [])
print(json.dumps({'prep':prep,'click':click,'next':next_log,'submit':sub,'result':result}, ensure_ascii=False, indent=1))
