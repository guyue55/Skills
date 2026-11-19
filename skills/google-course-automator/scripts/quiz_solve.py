#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""稳健 Quiz 作答（吸收 640560/640571/645356 攻坚经验）。
用法（两步，读题→作答分离，因 retake 会换题/选项，读题后不可再 retake）：
  1) python3 quiz_solve.py <url> read          # 显式 retake→等 radio 可点且全部未选中→打印当前题目原文(JSON)
  2) Agent 读题判断，写 answers.json（kw=题干子串, opts=当前选项完整原文）
  3) python3 quiz_solve.py <url> solve @answers.json  # 复用当前答题态：点选→读回选中态逐一比对+纠偏→提交→读结果
关键机制（实测坑）：
  - retake 后 radio 短暂 disabled，且可能残留上次答卷的选中态；必须等 disabled 消失且全部未选中才算新题态。
  - 选项集合每次 retake 都变（含题干顺序），所以 read 和 solve 之间绝不能再 goto/retake。
  - 只点内部 input（el.focus()+shadowRoot input.click()），绝不点 host——实测 md-radio/md-checkbox 的
    host.click() 会误触发相邻选项造成选中偏移（点 A 却选中 C）。
  - 提交前读回所有选项 checked 态，与目标逐一比对：目标未选的补点、非目标误选的取消，全一致才提交。
  - 匹配用双向 contains（选项原文可能比 opts 长或短），kw 用题干原文子串定位题目。
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gca

PORT = int(os.environ.get('GCA_PORT', '9333'))
URL = sys.argv[1]
MODE = sys.argv[2] if len(sys.argv) > 2 else 'read'

RETAKE = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.retake-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(b&&!b.hasAttribute('disabled')){b.click();return 'RETAKE';}if(b)return 'DISABLED';var s=document.querySelector('a.start-button');if(s){s.click();return 'START';}return 'NONE';})()"""
READ_JS = r'''(function(){
  function lin(n,d,seq){if(d>25||!n)return;const tag=n.tagName||'';
    if(tag==='QL-ITEM-STEM')seq.push({k:'S',t:(n.innerText||n.textContent||'').trim()});
    else if(tag==='MD-RADIO'||tag==='MD-CHECKBOX')seq.push({k:'O',t:(n.getAttribute('aria-label')||n.getAttribute('data-aria-label')||''),dis:n.hasAttribute('disabled'),sel:(n.checked===true||n.getAttribute('aria-checked')==='true'),type:tag});
    if(n.shadowRoot)lin(n.shadowRoot,d+1,seq);
    for(const c of (n.children||[]))lin(c,d+1,seq);}
  var seq=[];lin(document,0,seq);var out=[],cur=null;
  for(const x of seq){if(x.k==='S'){cur={stem:x.t,opts:[]};out.push(cur);}else if(x.k==='O'&&cur)cur.opts.push(x);}
  return JSON.stringify(out);})()'''

PICK_TMPL = r'''(function(){const items=ITEMS;
 function cl(s){return (s||'').replace(/\s+/g,' ').trim();}
 function lin(n,d,seq){if(d>25||!n)return;const tag=n.tagName||'';
   if(tag==='QL-ITEM-STEM')seq.push({k:'S',t:cl(n.innerText||n.textContent)});
   else if(tag==='MD-RADIO'||tag==='MD-CHECKBOX')seq.push({k:'O',el:n,t:tag,l:cl(n.getAttribute('aria-label')||n.getAttribute('data-aria-label'))});
   if(n.shadowRoot)lin(n.shadowRoot,d+1,seq);
   for(const ch of (n.children||[]))lin(ch,d+1,seq);}
 var seq=[];lin(document,0,seq);var groups=[],cur=null;
 for(const x of seq){if(x.k==='S'){cur={stem:cl(x.t).toLowerCase(),opts:[]};groups.push(cur);}else if(x.k==='O'&&cur)cur.opts.push(x);}
 var clicked=[],notfound=[];
 items.forEach((it,i)=>{
   var g=groups.find(gg=>it.kw&&gg.stem.indexOf(cl(it.kw).toLowerCase())>=0)||groups[i];
   if(!g){notfound.push('Q'+i+':无此题');return;}
   it.opts.forEach(want=>{
     var o=g.opts.find(oo=>oo.l.indexOf(want)>=0||want.indexOf(oo.l)>=0);
     if(!o){notfound.push('Q'+i+':'+want.slice(0,25));return;}
     var on=o.el.checked===true||o.el.getAttribute('aria-checked')==='true';
     if(!on){o.el.scrollIntoView({block:'center'});o.el.focus();
       // 关键：只点内部 input，绝不点 host（实测 md-radio/md-checkbox 的 host.click()
       // 会误触发相邻选项，导致选中偏移；focus()+input.click() 才精确）。
       var inp=o.el.shadowRoot&&o.el.shadowRoot.querySelector('input[type=radio],input[type=checkbox]');
       if(inp)inp.click(); else notfound.push('Q'+i+':NO_INPUT:'+want.slice(0,18));
       clicked.push('Q'+i+':'+want.slice(0,22));}
   });
 });
 return JSON.stringify({clicked,notfound,groups:groups.length});})()'''
# 核心闭环：读回所有选项 checked 态，按题干分组；目标项未选→补点，非目标项误选→取消。
# 返回 ok(是否全部一致) + 每组的实际选中文本，供 Agent/脚本确认。绝不点 host，只点内部 input。
VERIFY_TMPL = r'''(function(){const items=ITEMS;
 function cl(s){return (s||'').replace(/\s+/g,' ').trim();}
 function lin(n,d,seq){if(d>25||!n)return;const tag=n.tagName||'';
   if(tag==='QL-ITEM-STEM')seq.push({k:'S',t:cl(n.innerText||n.textContent)});
   else if(tag==='MD-RADIO'||tag==='MD-CHECKBOX')seq.push({k:'O',el:n,l:cl(n.getAttribute('aria-label')||n.getAttribute('data-aria-label'))});
   if(n.shadowRoot)lin(n.shadowRoot,d+1,seq);
   for(const ch of (n.children||[]))lin(ch,d+1,seq);}
 var seq=[];lin(document,0,seq);var groups=[],cur=null;
 for(const x of seq){if(x.k==='S'){cur={stem:cl(x.t).toLowerCase(),opts:[]};groups.push(cur);}else if(x.k==='O'&&cur)cur.opts.push(x);}
 function clickOpt(o,on){var isOn=o.el.checked===true||o.el.getAttribute('aria-checked')==='true';if(isOn===on)return false;
   o.el.scrollIntoView({block:'center'});o.el.focus();
   var inp=o.el.shadowRoot&&o.el.shadowRoot.querySelector('input[type=radio],input[type=checkbox]');
   if(inp)inp.click();return true;}
 var fixes=[],report=[];
 items.forEach((it,i)=>{
   var g=groups.find(gg=>it.kw&&gg.stem.indexOf(cl(it.kw).toLowerCase())>=0)||groups[i];
   if(!g){report.push('Q'+i+':无此题');return;}
   var wantTexts=it.opts.map(w=>cl(w));
   var matched=[];
   wantTexts.forEach(function(want){var o=g.opts.find(oo=>oo.l.indexOf(want)>=0||want.indexOf(oo.l)>=0);
     if(o){matched.push(o);if(clickOpt(o,true))fixes.push('Q'+i+':选+'+want.slice(0,16));}});
   // 取消同组内非目标的误选（host.click 偏移的后遗症）
   g.opts.forEach(function(o){if(matched.indexOf(o)<0){var on=o.el.checked===true||o.el.getAttribute('aria-checked')==='true';
     if(on&&clickOpt(o,false))fixes.push('Q'+i+':撤-'+o.l.slice(0,16));}});
   var curSel=g.opts.filter(function(o){return o.el.checked===true||o.el.getAttribute('aria-checked')==='true';}).map(o=>o.l.slice(0,20));
   report.push('Q'+i+':'+JSON.stringify(curSel));
 });
 return JSON.stringify({fixes,report,fixedCount:fixes.length});})()'''
SUBMIT = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.submit-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(!b)return 'NO';if(b.hasAttribute('disabled'))return 'DISABLED';b.click();return 'SUBMITTED';})()"""

def main():
    c = gca.client(PORT)
    if MODE == 'read':
        gca.goto(c, URL, 3)
        # 轮询等 retake 按钮渲染并点击（慢网络下 goto 后立即找会 NONE）
        prep = 'NONE'
        for _ in range(10):
            prep = gca.ev(c, RETAKE, 'NONE')
            if prep in ('RETAKE', 'START'):
                break
            time.sleep(1)
        # 等 radio 渲染、全部可点且全部未选中（真正的新题态；排除上次答卷残留）
        data, stale = None, False
        for attempt in range(15):
            cand = gca.evj(c, READ_JS, []) or []
            radios = [o for g in cand for o in g.get('opts', [])]
            any_sel = any(o.get('sel') for o in radios)
            if attempt >= 8 and any_sel:
                stale = True  # 多轮后仍有选中：retake 可能没生效，标记供 Agent 判断
            if radios and all(not o.get('dis') for o in radios) and not any_sel:
                data = cand
                break
            time.sleep(0.8)
        if data is None:
            data = gca.evj(c, READ_JS, []) or []
        print(json.dumps({'prep': prep, 'stale_warning': stale, 'questions': data, 'count': len(data)}, ensure_ascii=False, indent=1))
        return
    if MODE == 'solve':
        ans_path = sys.argv[3] if len(sys.argv) > 3 else None
        if not ans_path:
            print(json.dumps({'error':'solve 需 answers.json'},ensure_ascii=False)); sys.exit(2)
        answers = json.load(open(gca.os.path.expanduser(ans_path[1:] if ans_path.startswith('@') else ans_path), encoding='utf-8'))
        pick_expr = PICK_TMPL.replace('ITEMS', json.dumps(answers, ensure_ascii=False))
        verify_expr = VERIFY_TMPL.replace('ITEMS', json.dumps(answers, ensure_ascii=False))
        log = gca.evj(c, pick_expr, {})       # 第一轮批量点选
        time.sleep(0.7)
        verify, fixed_total = {}, -1
        # 闭环：VERIFY 每次读回真实选中态，补漏选/撤误选；直到无需再修（fixedCount=0）
        for rnd in range(5):
            verify = gca.evj(c, verify_expr, {})
            fixed_total = verify.get('fixedCount', -1)
            time.sleep(0.5)
            if fixed_total == 0 and not log.get('notfound'):
                break
        sub = gca.ev(c, SUBMIT, 'NO')
        time.sleep(3)
        result = gca.evj(c, r'''(function(){var t=document.body.innerText||'';return [...new Set(t.split('\n').map(s=>s.trim()).filter(s=>/score|pass|correct|incorrect|congrat|unfortunat/i.test(s)))].slice(0,10);})()''', [])
        print(json.dumps({'round': rnd+1, 'pick': log, 'verify': verify, 'submit': sub, 'result': result}, ensure_ascii=False, indent=1))
        return
    print(json.dumps({'error':'mode 只能是 read / solve'},ensure_ascii=False)); sys.exit(2)

if __name__ == '__main__':
    main()
