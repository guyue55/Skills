#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GCA (Google Course Automator) —— Google Skills 课程自动化统一入口。

设计原则（来自实战）：
  1. 浏览器只启动一次（带 --remote-allow-origins=*）；各命令独立短连接安全，advance 内部用单连接跑完整轮次。反复重启浏览器才是弹窗根因。
  2. 只用平台自带的按钮/链接，不伪造请求、不改后台数据、不代考真实认证。
  3. Quiz 答案由 Agent 读题后用领域知识判断（本脚本不内置答案），支持无限重考纠错。

用法：
  python3 gca.py <command> [args...]
  python3 gca.py --help
"""
import sys, os, json, time, argparse, glob, re, urllib.request

# 复用已安装的 browser-automation-cdp 技能提供的 CDP 客户端
CDP_SCRIPTS = os.path.expanduser('~/.workbuddy/skills/browser-automation-cdp/scripts')
if CDP_SCRIPTS not in sys.path:
    sys.path.insert(0, CDP_SCRIPTS)
try:
    from cdp import CDPClient
except ImportError:
    print(json.dumps({'error': '找不到 cdp.py，请确认已安装 browser-automation-cdp 技能',
                      'expected': CDP_SCRIPTS}, ensure_ascii=False))
    sys.exit(2)

# 端口优先级：命令行 --port > 环境变量 GCA_PORT > 默认 9333
DEFAULT_PORT = int(os.environ.get('GCA_PORT', 9333))
BASE = 'https://www.skills.google'


# ---------------------------------------------------------------------------
# 浏览器入口探测（只读，不启动/不关闭浏览器）
# ---------------------------------------------------------------------------
BROWSER_KW = ('browser', 'cdp', 'chrome', 'playwright', '浏览器')


def http_json(url, timeout=1.5):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read(8192).decode('utf-8', 'replace'))
    except Exception:
        return None


def probe_cdp_port(port):
    """探测某个 CDP 端口；返回 None 表示不可用。"""
    ver = http_json('http://127.0.0.1:{}/json/version'.format(port))
    if not isinstance(ver, dict) or not ver.get('Browser'):
        return None
    tabs = http_json('http://127.0.0.1:{}/json/list'.format(port)) or []
    urls = [t.get('url', '') for t in tabs if isinstance(t, dict)]
    return {
        'port': int(port),
        'browser': ver.get('Browser'),
        'tab_count': len(urls),
        'has_skills_google': any('skills.google' in u for u in urls),
        'urls': [u[:120] for u in urls[:6]],
    }


def candidate_ports(preferred=None):
    """候选 CDP 端口：显式/环境端口 + 常用端口 + mcp.json 里声明的端口。"""
    ports = []
    for p in ([preferred] if preferred else []) + [os.environ.get('GCA_PORT')]:
        try:
            ports.append(int(p))
        except (TypeError, ValueError):
            pass
    ports.extend([9333, 9222, 9334])
    try:
        with open(os.path.expanduser('~/.workbuddy/mcp.json'), encoding='utf-8') as f:
            txt = f.read()
        for m in re.findall(r'--remote-debugging-port[= ]+(\d+)', txt):
            ports.append(int(m))
    except OSError:
        pass
    seen = set()
    return [p for p in ports if not (p in seen or seen.add(p))]


def detect_browser_tools(session_tools=''):
    """列出本机浏览器技能 / MCP 配置；是否真能用，以当前会话工具清单为准。"""
    skills, seen = [], set()
    patterns = [
        os.path.expanduser('~/.workbuddy/skills/*/SKILL.md'),
        os.path.expanduser('~/.workbuddy/native-runtimes/**/skills/*/SKILL.md'),
        os.path.expanduser('~/.workbuddy/plugins/cache/**/skills/*/SKILL.md'),
    ]
    for pat in patterns:
        for path in glob.glob(pat, recursive=True):
            if not any(k in path.lower() for k in BROWSER_KW):
                continue
            name = os.path.basename(os.path.dirname(path))
            if name in seen:
                continue
            seen.add(name)
            skills.append({'name': name, 'path': path})
    mcp_entries = []
    try:
        with open(os.path.expanduser('~/.workbuddy/mcp.json'), encoding='utf-8') as f:
            cfg = json.load(f)
        for name, srv in (cfg.get('mcpServers') or {}).items():
            if srv.get('disabled'):
                continue
            blob = (name + ' ' + json.dumps(srv, ensure_ascii=False)).lower()
            if any(k in blob for k in BROWSER_KW):
                mcp_entries.append({'name': name, 'command': srv.get('command'),
                                    'args': srv.get('args', []),
                                    'note': '配置存在 ≠ 当前会话已加载；以工具清单为准'})
    except (OSError, ValueError):
        pass
    tools = [t.strip() for t in (session_tools or '').split(',') if t.strip()]
    return {
        'skills_installed': skills,
        'mcp_configured': mcp_entries,
        'session_tools_reported': tools,
        'browser_use_mcp_in_session': any('mcp__' in t.lower() and 'browser' in t.lower() for t in tools),
        'devtools_mcp_in_session': any('mcp__' in t.lower() and ('devtools' in t.lower() or 'chrome' in t.lower()) for t in tools),
    }


# ---------------------------------------------------------------------------
# 公共工具
# ---------------------------------------------------------------------------
def client(port=DEFAULT_PORT):
    """连接 CDP；默认端口不可达时，自动复用已开放的调试端口（不重启浏览器）。"""
    if port == DEFAULT_PORT and not os.environ.get('GCA_PORT'):
        if not http_json('http://127.0.0.1:{}/json/version'.format(port)):
            for cand in candidate_ports():
                if cand == port:
                    continue
                info = probe_cdp_port(cand)
                if info and (info['has_skills_google'] or os.environ.get('GCA_ALLOW_ANY_CDP') == '1'):
                    print('[gca] 端口 {} 不可达，自动复用已开放的 CDP 端口 {}（{}）'.format(
                        port, cand, info['browser']), file=sys.stderr)
                    port = cand
                    break
    c = CDPClient(port=port, timeout=25)
    c.ensure_page()
    return c

def ev(c, expr, default=None):
    """执行 JS，异常返回 default，避免单步错误中断。"""
    try:
        return c.evaluate(expr).get('value')
    except Exception:
        return default

def evj(c, expr, default=None):
    """执行 JS 并解析 JSON；CDP 可能直接返回 dict/list，也可能返回 JSON 字符串。"""
    raw = ev(c, expr)
    if raw is None:
        return default
    # CDP Runtime.evaluate 对 JS 数组/对象会直接反序列化成 Python list/dict，
    # 不能再走 json.loads（否则 quiz-read 的题目恒为空）。
    if isinstance(raw, (dict, list)):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            return default
    return default

def absurl(href):
    if not href:
        return None
    return href if href.startswith('http') else BASE + href

def goto(c, url, wait=1.0):
    try:
        c.navigate(url, timeout=30)
    except Exception:
        pass
    time.sleep(wait)

# 递归（含 Shadow DOM）收集题目元素，统一线性化
# 输出 seq: S=题干(stem), O=选项(radio/checkbox)
LIN_JS = r"""
(function(){const clean=s=>(s||'').replace(/\s+/g,' ').trim();let seq=[];
 function lin(node,d){if(d>25||!node)return;const tag=node.tagName||'';
   if(tag==='QL-ITEM-STEM')seq.push({k:'S',t:clean(node.innerText||node.textContent)});
   else if(tag==='MD-RADIO'||tag==='MD-CHECKBOX')
     seq.push({k:'O',t:tag,
       l:clean(node.getAttribute('aria-label')||node.getAttribute('data-aria-label')),
       on:node.checked===true||node.getAttribute('aria-checked')==='true'||node.hasAttribute('checked'),
       dis:node.hasAttribute('disabled'),
       _el:node});
   if(node.shadowRoot)lin(node.shadowRoot,d+1);
   for(const ch of (node.children||[]))lin(ch,d+1);
 }
 lin(document,0);
 return seq.map(x=>x.k==='S'?{k:'S',t:x.t}:{k:'O',t:x.t,l:x.l,on:x.on,dis:x.dis});
})()
"""

# 带 DOM 引用的版本（用于点击，不能跨 evaluate 传递，需在同一函数内完成）
CLICK_JS_TMPL = r"""
(function(){const items=ITEMS;const clean=s=>(s||'').replace(/\s+/g,' ').trim();
 let seq=[];
 function lin(node,d){if(d>25||!node)return;const tag=node.tagName||'';
   if(tag==='QL-ITEM-STEM')seq.push({k:'S',t:clean(node.innerText||node.textContent)});
   else if(tag==='MD-RADIO'||tag==='MD-CHECKBOX')
     seq.push({k:'O',el:node,t:tag,l:clean(node.getAttribute('aria-label')||node.getAttribute('data-aria-label'))});
   if(node.shadowRoot)lin(node.shadowRoot,d+1);
   for(const ch of (node.children||[]))lin(ch,d+1);
 }
 lin(document,0);
 // 按题干顺序把 seq 切成若干题；items[i] 对应第 i 题（0-based）
 let groups=[],cur=null;
 for(const x of seq){
   if(x.k==='S'){cur={stem:clean(x.t).toLowerCase(),opts:[]};groups.push(cur);}
   else if(x.k==='O'&&cur)cur.opts.push(x);
 }
 let clicked=[],notfound=[];
 items.forEach((it,i)=>{
   // 优先按题干关键词匹配题目，兜底按顺序
   let g=groups.find(gg=>it.kw && gg.stem.includes(it.kw)) || groups[i];
   if(!g){notfound.push('Q'+i+':无此题');return;}
   it.opts.forEach(want=>{
     const o=g.opts.find(oo=>oo.l===want || (it.fuzzy && oo.l.indexOf(want)>=0));
     if(!o){notfound.push('Q'+i+':'+want.slice(0,30));return;}
     const on=o.el.checked===true||o.el.getAttribute('aria-checked')==='true'||o.el.hasAttribute('checked');
     if(!on){
       o.el.scrollIntoView({block:'center'});
       // Material Web 组件的点击处理器在内部 <input> 上；点 host 对多选不起作用。
       const inner=o.el.shadowRoot&&o.el.shadowRoot.querySelector('input[type=checkbox],input[type=radio]');
       (inner||o.el).click();
       clicked.push(want.slice(0,34));
     }
   });
 });
 return JSON.stringify({clicked,notfound,groupsCount:groups.length});
})()
"""


# ---------------------------------------------------------------------------
# 命令实现
# ---------------------------------------------------------------------------
def cmd_browser_detect(args):
    """自动探测浏览器入口并给出建议；入口只是手段，能复用就不启动。"""
    ports = []
    for p in candidate_ports(getattr(args, 'port', None)):
        info = probe_cdp_port(p)
        if info:
            ports.append(info)
    tools = detect_browser_tools(getattr(args, 'session_tools', ''))
    target = next((p for p in ports if p['has_skills_google']), None)
    caution = None
    if target:
        adapter = 'cdp_existing'
        action = '复用端口 {} 的浏览器（不要启动新实例）；后续命令加 --port {}'.format(
            target['port'], target['port'])
    elif ports:
        adapter = 'cdp_existing_unconfirmed'
        action = '端口 {} 可连但未发现 skills.google 标签，先确认是否目标浏览器'.format(ports[0]['port'])
        caution = '不要把无关浏览器当目标；必要时先打开课程链接再判断'
    elif tools['browser_use_mcp_in_session'] or tools['devtools_mcp_in_session']:
        adapter = 'session_mcp'
        action = '先用当前会话的浏览器 MCP 打开并确认登录页；批量 Quiz 仍需 CDP 执行 JS 能力'
        caution = 'MCP 是否支持 evaluate/Shadow DOM 决定能否直接跑 gca.py 的批量逻辑'
    else:
        adapter = 'cdp_self_start'
        action = '按 browser-start-info 准备登录态，并后台启动一次常驻调试浏览器'
        caution = '浏览器只启动一次；启动后全程复用同一端口'
    print(json.dumps({
        'adapter': adapter, 'action': action, 'caution': caution,
        'cdp_ports': ports, 'tools': tools,
        'rule': '入口只是手段：能复用就不启动；当前会话工具清单优先于本机配置清单'
    }, ensure_ascii=False, indent=1))


def cmd_browser_check(args):
    c = client(getattr(args, "port", DEFAULT_PORT))
    try:
        ver = c.version().get('Browser', '')
    except Exception as e:
        print(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False)); return
    print(json.dumps({'ok': True, 'browser': ver, 'port': args.port}, ensure_ascii=False))


def cmd_browser_start_info(args):
    """输出：如何准备登录态 + 启动常驻调试浏览器（供 Agent 用后台任务机制执行）。"""
    home = os.path.expanduser('~')
    src = os.path.join(home, 'Library/Application Support/Google/Chrome')
    info = {
        'note': 'Chrome 157+ 禁止直接调试日常默认 profile；需复制登录态到独立目录后启动。' ,
        'login_files': [
            'Local State -> <profile>/Local State',
            'Default/Cookies -> <profile>/Default/Cookies   (注意不是 Default/Network/Cookies)',
            'Default/Cookies-journal -> <profile>/Default/Cookies-journal',
            'Default/Login Data -> <profile>/Default/Login Data',
            'Default/Preferences -> <profile>/Default/Preferences',
            'Default/Secure Preferences -> <profile>/Default/Secure Preferences',
        ],
        'source_chrome_profile': src,
        'suggested_profile_dir': os.path.expanduser('~/.workbuddy/google-course-automator-profile'),
        'start_command': (
            '"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" '
            '--remote-debugging-port={port} --remote-allow-origins=* '
            '--user-data-dir="<profile_dir>" --no-first-run --no-default-browser-check '
            '--disable-background-networking --disable-sync --disable-extensions --no-sandbox about:blank'
        ).format(port=args.port, profile_dir=os.path.expanduser('~/.workbuddy/google-course-automator-profile')),
        'run_mode': '必须用后台任务机制常驻运行（不要用 nohup，会被环境回收）；浏览器只启动一次。',
        'ready_check': 'curl -s --max-time 3 http://127.0.0.1:{}/json/version'.format(args.port),
    }
    print(json.dumps(info, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# 权益诊断（只读）：点数余额 / GEAR 会员 / 开发者资料公开状态
# ---------------------------------------------------------------------------
# 这几轮实战中反复手工查的三件事，固化成一条只读命令。只读取页面文字与 DOM，
# 不点提交、不改授权、不购买点数。
ENT_POINTS_JS = r"""
(() => {
  // 真实余额只在顶栏 QL-CHIP（如 "0 个点数"）；正文里的 "35 个点数" 是套餐宣传，绝不能当余额。
  // 放宽匹配：允许 "0 个点数" / "余额 0 个点数" / "0 credits left" 等前后缀，但只取 chip 内文本。
  let chips = [...document.querySelectorAll('ql-chip')].map(x => (x.textContent||'').trim())
    .filter(s => /\d+\s*(个点数|credits?)/i.test(s));
  let label = chips[0] || '';
  let m = label.match(/(\d+)\s*(个点数|credits?)/i);
  return JSON.stringify({
    balance_label: label,
    balance: m ? parseInt(m[1], 10) : null,   // null = 未登录/未取到 chip，回 Phase 0 查登录态
    loggedIn: !!document.querySelector('ql-avatar'),
    url: location.href
  });
})()
"""

ENT_GEAR_JS = r"""
(() => {
  let txt = document.body ? document.body.innerText : '';
  let loading = /正在检查您的 GEAR 状态|Checking your GEAR status/i.test(txt);
  // 渲染完成的标志：出现 Gemini Agent Ready 标题或"欢迎加入 GEAR"（实测已加入态）。
  let rendered = /Gemini Agent Ready|欢迎加入 GEAR|Welcome to GEAR/i.test(txt);
  // 已加入：页面无"成为会员"CTA；未加入：有该 CTA。
  let cta = /成为会员|Become a member/.test(txt);
  let badge = /Gemini Agent Ready/.test(txt);
  let badgeDate = (txt.match(/Gemini Agent Ready[\s\S]{0,40}?(20\d{2})/)||[])[1] || '';
  return JSON.stringify({
    loading: loading || !rendered,          // 未渲染完也视为 loading，避免误判
    rendered: rendered,
    memberCtaPresent: cta,
    badgeTextPresent: badge,
    likelyJoined: rendered && !loading && !cta,
    badgeDate: badgeDate,
    url: location.href
  });
})()
"""

ENT_PROFILE_JS = r"""
(() => {
  let txt = document.body ? document.body.innerText : '';
  let pub = /Public profile|公开个人资料/.test(txt);
  let priv = /Private profile/.test(txt);
  let gearBadge = /Gemini Agent Ready/.test(txt);
  return JSON.stringify({
    profilePublic: pub,
    profilePrivate: priv,
    gearBadgeOnProfile: gearBadge,
    url: location.href
  });
})()
"""

def cmd_entitlement(args):
    """只读诊断：skills.google 点数余额 + GEAR 会员 + 开发者资料公开状态。"""
    c = client(getattr(args, "port", DEFAULT_PORT))
    out = {'checked_at': time.strftime('%Y-%m-%d %H:%M:%S')}

    # 1) 点数余额（skills.google）
    try:
        goto(c, BASE + '/payments/new?locale=zh', wait=2.5)
        out['points'] = evj(c, ENT_POINTS_JS, {})
    except Exception as e:
        out['points'] = {'error': str(e)}

    # 2) GEAR 会员状态（developers.google.com 官方页）——页面渲染慢，轮询等占位消失
    try:
        goto(c, 'https://developers.google.com/program/gear?hl=zh-cn', wait=3.0)
        g = evj(c, ENT_GEAR_JS, {})
        for _ in range(8):
            if g and not g.get('loading'):
                break
            time.sleep(1.5)
            g = evj(c, ENT_GEAR_JS, {})
        out['gear'] = g
    except Exception as e:
        out['gear'] = {'error': str(e)}

    # 3) 开发者资料公开状态（me.developers.google.com）
    try:
        goto(c, 'https://me.developers.google.com/u/me', wait=3.0)
        out['developer_profile'] = evj(c, ENT_PROFILE_JS, {})
    except Exception as e:
        out['developer_profile'] = {'error': str(e)}

    print(json.dumps(out, ensure_ascii=False, indent=2))


# ---- 续证/凭证只读诊断（2026-11-18 新增）----
RECERT_JS = r"""
(() => {
  const lines = (document.body.innerText||'').split('\n').map(s=>s.trim()).filter(Boolean);
  const out = {url: location.href, certs: [], badges: 0, credentials: 0, linked: true};
  // 顶栏统计：Certifications (1) / Badges (17) / Credentials (17)
  for (const l of lines) {
    let m = l.match(/^Certifications\s*\((\d+)\)/i); if (m) out.credentials = +m[1];
    m = l.match(/^Badges\s*\((\d+)\)/i); if (m) out.badges = +m[1];
    // 顶栏统计有时无括号："Badges 17" / "Credentials 17"
    m = l.match(/^Badges\s+(\d+)$/i); if (m && !out.badges) out.badges = +m[1];
  }
  // 凭证卡片结构：Issued <date> / Expires: <date> / <Name> / Active|Inactive
  const MONTHS={Jan:1,Feb:2,Mar:3,Apr:4,May:5,Jun:6,Jul:7,Aug:8,Sep:9,Oct:10,Nov:11,Dec:12};
  function parseDate(s){ const m=(s||'').match(/([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})/);
    return m ? `${m[3]}-${String(MONTHS[m[1]]||1).padStart(2,'0')}-${String(m[2]).padStart(2,'0')}` : null; }
  for (let i=0;i<lines.length;i++){
    if (/^Issued\s/i.test(lines[i])) {
      const issued=parseDate(lines[i]);
      let expires=null,name=null,status=null;
      for (let j=i+1;j<Math.min(i+6,lines.length);j++){
        if (/^Expires:/i.test(lines[j])) expires=parseDate(lines[j].replace(/^Expires:\s*/i,''));
        else if (/^(Active|Inactive|Expired|Renew)/i.test(lines[j])) { status=lines[j]; break; }
        else if (!name && !/^Certifications/i.test(lines[j])) name=lines[j];
      }
      out.certs.push({name, issued, expires, status});
    }
  }
  // 只有明确的 "Ineligible for recertification" 才判未关联；教程 banner 的 "Link your..." 不算
  const txt=lines.join(' ');
  if (/ineligible for recertification/i.test(txt)) out.linked=false;
  out.link_hint = /ineligible for recertification/i.test(txt)
    ? 'CM Connect 与 Google Skills 账号未关联，看不到续证资格' : '未见未关联提示（证书正常显示则通常已关联）';
  return JSON.stringify(out);
})()
"""

# Google Skills 继续教育续证支持的认证 -> 伙伴续证路径（2026-11 官方；以平台当前显示为准）
RECERT_PATHS = {
    # 已联网核实的路径（2026-11）；PDE/CDL 官方只说"同平台对应路径"，未给确切 ID，故标记待确认
    'associate cloud engineer': 'https://partner.skills.google/paths/4177',
    'professional cloud architect': 'https://partner.skills.google/paths/4178',
    'cloud digital leader': 'https://partner.skills.google/  （PDE/CDL 路径 ID 未在官方公开资料中确认，请以平台当日显示为准）',
    'professional data engineer': 'https://partner.skills.google/  （同上，路径 ID 待平台确认）',
}
RECERT_NOW_SUPPORTED = {
    'cloud digital leader', 'associate cloud engineer', 'professional cloud architect',
    'professional data engineer', 'generative ai leader', 'associate google workspace administrator',
    'associate data practitioner', 'professional cloud database engineer',
    'professional cloud developer', 'professional cloud devops engineer',
    'professional cloud security engineer', 'professional cloud network engineer',
    'professional machine learning engineer', 'professional security operations engineer',
}

def _days_until(date_str):
    if not date_str:
        return None
    try:
        from datetime import date
        y, m, d = [int(x) for x in date_str.split('-')]
        return (date(y, m, d) - date.today()).days
    except Exception:
        return None

def cmd_recert(args):
    """只读诊断账号证书与续证状态；一句话给出可续/快到期判定与续证路径。"""
    c = client(getattr(args, "port", DEFAULT_PORT))
    out = {'checked_at': time.strftime('%Y-%m-%d %H:%M:%S')}
    try:
        goto(c, BASE + '/profile/badges?locale=en', wait=3.0)
        d = evj(c, RECERT_JS, {})
    except Exception as e:
        d = {'error': str(e)}
    out['raw'] = d
    certs = d.get('certs') or []
    enriched = []
    for cert in certs:
        item = dict(cert)
        key = (cert.get('name') or '').lower().strip()
        days = _days_until(cert.get('expires'))
        item['days_until_expiry'] = days
        # 续证窗口：到期前 1 年（继续教育）；免费路径仅最后一年计数
        item['renew_window_open'] = (days is not None and days <= 365)
        item['expiring_soon_90d'] = (days is not None and days <= 90)
        item['recert_supported'] = key in RECERT_NOW_SUPPORTED
        item['recert_path'] = RECERT_PATHS.get(key)
        if days is not None and days < 0:
            item['advice'] = '已过期：只能重考标准考试（新 Series ID）；伙伴全免折扣不再适用'
        elif item['renew_window_open']:
            item['advice'] = '已进入续证窗口：完成指定课程/徽章（须在最后一年内完成才计数），自动延期1年'
        elif item['recert_supported']:
            item['advice'] = f'距到期 {days} 天，续证窗口（到期前365天）未开；现在刷课不计入、且不能提前存学分'
        else:
            item['advice'] = '该认证继续教育续证支持以平台当日显示为准；不在列表则走续证考试'
        enriched.append(item)
    out['certifications'] = enriched
    out['summary'] = {
        'cert_count': len(certs),
        'badges': d.get('badges') if d.get('badges') else '本页未列出（完整徽章数见 Dashboard 首页）',
        'credentials': d.get('credentials'),
        'cm_connect_linked': d.get('linked'),
        'renewable_now': [c.get('name') for c in enriched if c.get('renew_window_open')],
        'expiring_90d': [c.get('name') for c in enriched if c.get('expiring_soon_90d')],
        'note': 'PCK 考试券不可用于续证（走 Partner Recertification Program）；免费续证须在到期前最后一年内完成指定活动。以官方当日政策为准。',
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


READ_ACTS_JS = r"""
(() => {
  const e = document.querySelector('ql-contents-menu');
  if (!e) return 'NO_MENU';
  const m = JSON.parse(e.getAttribute('modules')||'[]');
  const acts = m.flatMap(mod => (mod.steps||[]).flatMap(s => (s.activities||[])));
  return JSON.stringify(acts.map(a => ({href:a.href, title:(a.title||'').slice(0,60),
    complete:a.isComplete, progress:a.progress})));
})()
"""

def cmd_read_acts(args):
    """读取路径页/课程页的全部活动清单及其完成状态。"""
    c = client(getattr(args, "port", DEFAULT_PORT))
    goto(c, args.url, wait=3.0)
    acts = evj(c, READ_ACTS_JS, [])
    if acts == 'NO_MENU' or not acts:
        print(json.dumps({'error': '未找到 ql-contents-menu，可能未登录或页面未加载', 'url': args.url}, ensure_ascii=False))
        return
    print(json.dumps({'url': args.url, 'count': len(acts), 'acts': acts}, ensure_ascii=False, indent=1))


def cmd_quiz_list(args):
    """扫描某路径下所有课程，列出未完成的 Quiz（供批量作答）。"""
    c = client(getattr(args, "port", DEFAULT_PORT))
    goto(c, args.url, wait=3.0)
    raw_acts = evj(c, READ_ACTS_JS, [])
    if not raw_acts or raw_acts == 'NO_MENU':
        print(json.dumps({'error': '无法读取活动清单'}, ensure_ascii=False)); return
    # 用路径活动里的具体 href 当入口（课程根 /course_sessions/<id> 没有 ql-contents-menu）
    entries, seen = [], set()
    for a in raw_acts:
        h = a.get('href') or ''
        if '/course_sessions/' in h:
            key = 'session:' + h.split('/course_sessions/')[1].split('/')[0]
        elif '/course_templates/' in h:
            key = 'template:' + h.split('/course_templates/')[1].split('/')[0]
        else:
            continue
        if key not in seen:
            seen.add(key)
            entries.append((key, h))
    quizzes = []
    for key, href in entries:
        goto(c, absurl(href), wait=2.2)
        qs = evj(c, r"""(function(){const e=document.querySelector('ql-contents-menu');if(!e)return [];
          const m=JSON.parse(e.getAttribute('modules')||'[]');
          const a=m.flatMap(x=>(x.steps||[]).flatMap(s=>(s.activities||[])));
          return a.filter(x=>/\/quizzes\//.test(x.href||'')&&!x.isComplete)
            .map(x=>({href:x.href,title:(x.title||'').slice(0,60)}));})()""", [])
        for q in (qs or []):
            q['course'] = key
            quizzes.append(q)
    print(json.dumps({'course_count': len(entries), 'unchecked_quiz_count': len(quizzes),
                      'quizzes': quizzes}, ensure_ascii=False, indent=1))


def cmd_quiz_read(args):
    """读取 Quiz 的题目与选项（含完成状态），输出 JSON 供 Agent 判断答案。

    --retake：若当前是结果页/未开始页，先点 Retake/Start 进入答题态再读题。
    """
    c = client(getattr(args, "port", DEFAULT_PORT))
    goto(c, args.url, wait=3.0)
    RETAKE = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.retake-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(b){b.click();return 'RETAKE';}return 'NONE';})()"""
    START = r"""(function(){let b=document.querySelector('a.start-button');if(b){b.click();return 'START';}return 'NONE';})()"""
    body = ev(c, "document.body?document.body.innerText.slice(0,1200):''", '') or ''
    score = None
    import re as _re
    m = _re.search(r'Your score:\s*(\d+)%', body)
    if m:
        score = int(m.group(1))
    status = 'answering'
    if score is not None:
        status = 'result_page'
    elif 'Start quiz' in body:
        status = 'not_started'
    prep = 'NONE'
    if args.retake and status in ('result_page', 'not_started'):
        prep = ev(c, RETAKE, 'NONE')
        if prep == 'NONE':
            prep = ev(c, START, 'NONE')
        if prep != 'NONE':
            status = 'answering'
            score = None
    # 关键：轮询等待题目渲染（网络卡顿时题干可能晚 3-8 秒才出现）
    seq = []
    for _ in range(12):
        seq = evj(c, LIN_JS, []) or []
        if any(x.get('k') == 'S' for x in seq):
            break
        time.sleep(0.8)
    # 聚合成题目
    qs = []
    for x in (seq or []):
        if x.get('k') == 'S':
            qs.append({'stem': x['t'], 'opts': []})
        elif x.get('k') == 'O' and qs:
            qs[-1]['opts'].append({'label': x.get('l', ''), 'type': x.get('t'),
                                   'selected': bool(x.get('on')), 'disabled': bool(x.get('dis'))})
    print(json.dumps({'url': args.url, 'status': status, 'score': score, 'prep': prep,
                      'question_count': len(qs), 'questions': qs,
                      'body_head': body[:400]}, ensure_ascii=False, indent=1))


def cmd_quiz_answer(args):
    """按答案 JSON 作答并提交。答案格式见 SKILL.md。若当前是结果页/未开始页会自动 Retake/Start 再作答。"""
    answers = json.loads(args.answers)
    c = client(getattr(args, "port", DEFAULT_PORT))
    goto(c, args.url, wait=2.5)
    # 结果页先 Retake
    RETAKE = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.retake-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(b){b.click();return 'RETAKE';}return 'NONE';})()"""
    START = r"""(function(){let b=document.querySelector('a.start-button');if(b){b.click();return 'START';}return 'NONE';})()"""
    r = ev(c, RETAKE, 'NONE')
    if r == 'NONE':
        r = ev(c, START, 'NONE')
    if r != 'NONE':
        time.sleep(2)
    # 轮询等待题目渲染完成再作答
    for _ in range(12):
        seq0 = evj(c, LIN_JS, []) or []
        if sum(1 for x in seq0 if x.get('k') == 'S') >= len(answers):
            break
        time.sleep(0.8)
    # 三轮点击 + 每次间隔（应对多选异步漏点 / 选项重排）
    # 实测：两轮后立刻提交会让 checkbox 状态还没写回 quizresponse，导致提交无效。
    expr = CLICK_JS_TMPL.replace('ITEMS', json.dumps(answers, ensure_ascii=False))
    res = {}
    for rnd in range(3):
        res = evj(c, expr, {})
        time.sleep(0.8)
    # 最后一轮点击后再给前端一次稳定窗口，再提交
    time.sleep(1.0)
    # 提交（Submit 在 Shadow DOM，不是 Next）
    SUBMIT = r"""(function(){let b=null;function w(r,d){if(d>18||b)return;b=r.querySelector('ql-button.submit-button');if(b)return;r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);if(!b)return 'NO';b.scrollIntoView({block:'center'});b.click();return 'SUBMITTED';})()"""
    sub = ev(c, SUBMIT, 'NO')
    time.sleep(4)
    RESULT = r"""(function(){let r=[];function w(root,d){if(d>18)return;root.querySelectorAll('*').forEach(e=>{if(e.children.length===0){let t=(e.textContent||'').trim();if(/Your score:|Passing score:|passed|Congrat|Unfortunately|Not passed|correct|incorrect/i.test(t)&&t.length<160)r.push(t);}if(e.shadowRoot)w(e.shadowRoot,d+1)})}w(document,0);return JSON.stringify([...new Set(r)].slice(0,25));})()"""
    result = evj(c, RESULT, [])
    seq = evj(c, LIN_JS, [])
    # 提取结果页每题的对错反馈（Correct:: / Incorrect::）
    feedback = []
    for x in (seq or []):
        if x.get('k') == 'S':
            feedback.append({'stem': x['t'], 'opts': []})
    print(json.dumps({'url': args.url, 'prep': r, 'click': res, 'submit': sub,
                      'result': result, 'feedback_questions': feedback}, ensure_ascii=False, indent=1))


PROBE_JS = r"""
(() => {
  const url = location.href;
  const bodyText = document.body ? (document.body.innerText||'') : '';
  const cb = document.querySelector('ql-button[href*="complete_button"]');
  const nb = document.querySelector('ql-button.next-button');
  const startBtn = document.querySelector('ql-button[href*="/enroll"], a.start-button');
  const isPathPage = /\/paths\/[^/]+(?:[/?#]|$)/.test(url) && !/\/paths\/[^/]+\//.test(url);
  return JSON.stringify({url, title: document.title||'', isPathPage,
    hasComplete: !!cb, completeDisabled: cb?cb.hasAttribute('disabled'):null,
    nextHref: nb?(nb.getAttribute('href')||''):'', nextDisabled: nb?nb.hasAttribute('disabled'):null,
    hasStart: !!startBtn, isLab: /\/labs\//.test(url),
    isQuiz: /\/quizzes\//.test(url),
    text: bodyText.slice(0,140)});
})()
"""

def _href_course_ids(href):
    """从活动 href 抽出课程 ID（template/session 的数字），用于跳过列表匹配。"""
    out = set()
    for pat in (r'/course_templates/(\d+)', r'/course_sessions/(\d+)'):
        out.update(re.findall(pat, href or ''))
    return out


def cmd_advance(args):
    """全流程推进：视频标记完成，Lab/Quiz/Document 跳过（最快模式）。

    --skip-course ID[,ID...]：扫描后已确认是纯 Lab 课（不准备做）时传入，
    在路径页候选阶段就排除，避免明知不做还导航进去逐个点 Next 走过每个 Lab。
    """
    # 解析跳过列表：兼容纯数字、以及 scan_courses 输出的 template:648 / session:41484246 带前缀格式
    skip = set()
    for tok in (getattr(args, 'skip_course', '') or '').split(','):
        tok = tok.strip()
        if not tok:
            continue
        m = re.search(r'(\d+)\s*$', tok)  # 取末尾数字，容忍 template:/session: 前缀
        if m:
            skip.add(m.group(1))
        else:
            print('[gca] 警告：无法解析的 --skip-course token: {}'.format(tok), file=sys.stderr)
    c = client(getattr(args, "port", DEFAULT_PORT))
    path_url = args.url
    goto(c, path_url, wait=3.0)
    stats = {'video': 0, 'skip': 0, 'switch': 0, 'lab_course_skipped': 0}
    processed = set()
    intro_visits, no_action = {}, 0
    for i in range(1, args.steps + 1):
        st = evj(c, PROBE_JS)
        if not st:
            time.sleep(1); continue
        url = st['url']
        # 安全网：万一已落在被跳过的课程页，直接回路径页，不走它的 Lab
        if skip and _href_course_ids(url) & skip:
            stats['lab_course_skipped'] += 1
            print('[{}] 跳过已标记 Lab 课: {}'.format(i, url[-40:]), flush=True)
            goto(c, path_url, wait=2.0)
            continue
        if st['isPathPage']:
            acts = evj(c, READ_ACTS_JS, []) or []
            cands = [a for a in acts if not a.get('complete') and (a.get('progress') or 0) < 50]
            # 关键修复：在导航前排除已确认不做的纯 Lab 课
            if skip:
                kept = [a for a in cands if not (_href_course_ids(a.get('href')) & skip)]
                stats['lab_course_skipped'] += len(cands) - len(kept)
                cands = kept
            cands.sort(key=lambda a: a.get('progress') or 0)
            nxt = next((a for a in cands if a['title'] not in processed), None)
            if not nxt:
                print(json.dumps({'done': True, 'stats': stats, 'note': '无剩余新活动'}, ensure_ascii=False)); return
            processed.add(nxt['title']); no_action = 0
            goto(c, absurl(nxt['href']), wait=1.5)
            print('[{}] 进入活动: {}'.format(i, nxt['title'][:40]), flush=True)
            continue
        if st['hasComplete'] and st['completeDisabled'] is False:
            old = url
            ev(c, "(()=>{const b=document.querySelector('ql-button[href*=complete_button]');if(!b)return 'NO';b.click();return 'OK';})()")
            stats['video'] += 1; no_action = 0
            print('[{}] VIDEO ✓ ({})'.format(i, stats['video']), flush=True)
            for _ in range(10):
                time.sleep(0.4)
                if ev(c, 'location.href') != old: break
            continue
        if st['nextHref'] and not st['nextDisabled']:
            kind = 'LAB' if st['isLab'] else ('QUIZ' if st['isQuiz'] else 'SKIP')
            goto(c, absurl(st['nextHref']), wait=1.0)
            stats['skip'] += 1; no_action = 0
            print('[{}] {} 跳过'.format(i, kind), flush=True)
            continue
        no_action += 1
        if no_action >= 3:
            no_action = 0; stats['switch'] += 1; goto(c, path_url, wait=2.0)
        else:
            time.sleep(0.8)
    print(json.dumps({'done': False, 'stats': stats, 'note': '达到步数上限'}, ensure_ascii=False))


def _add_port(sp):
    """给子命令统一加 --port（默认读 GCA_PORT 环境变量）。"""
    sp.add_argument('--port', type=int, default=DEFAULT_PORT,
                    help='CDP 调试端口，默认读 GCA_PORT 或 9333')

def main():
    p = argparse.ArgumentParser(prog='gca.py', description='Google Skills 课程自动化')
    sub = p.add_subparsers(dest='cmd', required=True)

    sp = sub.add_parser('browser-detect', help='自动探测浏览器入口（只读）')
    sp.add_argument('--session-tools', default='',
                    help='当前会话可用的浏览器 MCP 工具名，逗号分隔（可选）')
    _add_port(sp)
    sp = sub.add_parser('browser-check', help='检查调试浏览器连通'); _add_port(sp)
    sp = sub.add_parser('browser-start-info', help='输出浏览器启动与登录态准备说明'); _add_port(sp)
    sp = sub.add_parser('entitlement', help='只读诊断点数/GEAR会员/开发者资料公开状态'); _add_port(sp)
    sp = sub.add_parser('recert', help='只读查证书/续证状态：可续/快到期/续证路径'); _add_port(sp)
    sp = sub.add_parser('read-acts', help='读取活动清单'); sp.add_argument('url'); _add_port(sp)
    sp = sub.add_parser('quiz-list', help='列出未完成 Quiz'); sp.add_argument('url'); _add_port(sp)
    sp = sub.add_parser('quiz-read', help='读取 Quiz 题目')
    sp.add_argument('url'); sp.add_argument('--retake', action='store_true', help='先点Retake/Start进入答题态'); _add_port(sp)
    sp = sub.add_parser('quiz-answer', help='作答并提交 Quiz')
    sp.add_argument('url'); sp.add_argument('answers', help='答案 JSON 字符串或 @文件路径'); _add_port(sp)
    sp = sub.add_parser('advance', help='推进（视频标记+跳过）')
    sp.add_argument('url'); sp.add_argument('steps', type=int, nargs='?', default=200)
    sp.add_argument('--skip-course', default='',
                    help='逗号分隔的课程ID（纯Lab课，扫描后已确认不做），导航前排除，避免访问每个Lab')
    _add_port(sp)

    args = p.parse_args()
    fn = {
        'browser-detect': cmd_browser_detect,
        'browser-check': cmd_browser_check, 'browser-start-info': cmd_browser_start_info,
        'entitlement': cmd_entitlement, 'recert': cmd_recert,
        'read-acts': cmd_read_acts, 'quiz-list': cmd_quiz_list,
        'quiz-read': cmd_quiz_read, 'quiz-answer': cmd_quiz_answer, 'advance': cmd_advance,
    }[args.cmd]
    if args.cmd == 'quiz-answer' and args.answers.startswith('@'):
        path = os.path.expanduser(args.answers[1:])
        try:
            with open(path, encoding='utf-8') as f:
                args.answers = f.read()
        except OSError as e:
            print(json.dumps({'error': '读取答案文件失败', 'path': path, 'detail': str(e)}, ensure_ascii=False))
            sys.exit(3)
    fn(args)

if __name__ == '__main__':
    main()
