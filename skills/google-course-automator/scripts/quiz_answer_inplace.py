#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""两段式 Quiz 作答，解决"读题 retake 一次、作答又 retake 导致选项集合变化"的坑。
用法：
  1) gca.py quiz-read <url> --retake        # 读题，浏览器停在答题态（选项已定）
  2) Agent 判断，写答案 JSON（kw=题干原文子串 + opts=当前选项原文，fuzzy 可选）
  3) quiz_answer_inplace.py <url> @answers.json   # 不 goto、不 retake，当前答题态直接点选+提交
关键：步骤1和3之间浏览器 tab 保持答题态，选项不会二次重排。
答案 JSON 格式与 gca.py quiz-answer 相同：[{kw,opts,fuzzy?},...]
"""
import os, sys, json, time
sys.path.insert(0, '/Users/apple/.workbuddy/skills/google-course-automator/scripts')
sys.path.insert(0, '/Users/apple/.workbuddy/skills/browser-automation-cdp/scripts')
import gca
from cdp import CDPClient

PORT = int(os.environ.get('GCA_PORT', '9333'))
URL = sys.argv[1]
ANS = sys.argv[2] if len(sys.argv) > 2 else None
if not ANS:
    print(json.dumps({'error':'用法: quiz_answer_inplace.py <url> @answers.json'},ensure_ascii=False)); sys.exit(2)

path = gca.os.path.expanduser(ANS[1:] if ANS.startswith('@') else ANS)
answers = json.load(open(path, encoding='utf-8'))

c = CDPClient(port=PORT, timeout=30)
c.ensure_page()
# 关键：不 goto、不 retake。先确认当前页还在答题态
cur = c.page_url()
if 'quizzes/' not in cur:
    print(json.dumps({'error':'当前 tab 不在答题页，请先运行 gca.py quiz-read <url> --retake','current_url':cur},ensure_ascii=False)); sys.exit(3)

expr = gca.CLICK_JS_TMPL.replace('ITEMS', json.dumps(answers, ensure_ascii=False))
for _ in range(3):
    log = gca.evj(c, expr, [])
    time.sleep(0.6)
st = gca.ev(c, gca.SUBMIT_JS, 'NONE') if hasattr(gca, 'SUBMIT_JS') else None
# gca 没暴露 SUBMIT_JS，用与 gca.py 完全一致的选择器逻辑（querySelector + shadow 递归）
SUBMIT = r'''(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.submit-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(!b)return 'NO';if(b.hasAttribute('disabled'))return 'DISABLED';b.scrollIntoView({block:'center'});b.click();return 'SUBMITTED';})()'''
NEXT = r'''(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.next-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(!b||b.hasAttribute('disabled'))return 'NO';b.click();return 'NEXT';})()'''
HAS_SUBMIT = r'''(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.submit-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);return b?'YES':'NO';})()'''
# 分页式 quiz：当前页无 submit 时点 Next 推进，直到 submit 出现
pages = []
for _ in range(20):
    if gca.ev(c, HAS_SUBMIT, 'NO') == 'YES':
        break
    n = gca.ev(c, NEXT, 'NO')
    pages.append(n)
    if n == 'NO':
        break
    time.sleep(1.0)
if st is None:
    st = gca.ev(c, SUBMIT, 'NO')
time.sleep(2)
result = gca.evj(c, r'''(function(){var t=document.body.innerText||'';return t.split('\n').map(function(s){return s.trim();}).filter(function(l){return /score|pass|correct|incorrect|congrat|unfortunately/i.test(l);}).slice(0,40);})()''', [])
print(json.dumps({'click':log,'pages':pages,'submit':st,'result':result}, ensure_ascii=False, indent=1))
