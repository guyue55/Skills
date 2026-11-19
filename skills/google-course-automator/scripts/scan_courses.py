#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量扫描课程构成，识别"零 Lab 有 Quiz、可快速完成"的课（自主选课用）。

吸收自 /tmp/scan_templates.py，改为可复用工具：
  - 路径 ID 由命令行给定（不再硬编码）
  - 复用 gca.py 的 client/goto/evj/READ_ACTS_JS，不重复实现 CDP 逻辑
  - 支持 GCA_PORT 与 --port，不写死 9333
  - 结果同时打印表格与写 JSON（--out 可指定）

用法:
  scan_courses.py 4682 4683 4525 4676            # 扫描指定路径
  scan_courses.py 4682,4683,4525 --out /tmp/scan.json
  scan_courses.py                                 # 不传则用内置常用路径集合
输出 JSON 每项: topic/tid/总活动/视频/Quiz/Lab/其他/标题/未完成的非Lab数。
"""
import os, sys, json, re, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gca

# 内置常用路径集合（用户可用命令行参数覆盖）
DEFAULT_PATHS = {
    '4682': '安全', '4683': '网络', '4525': 'Agent', '4676': 'GenAI',
    '4883': 'TPU', '3545': 'ADK', '19': '云开发', '82': '综合', '11': 'ACE',
}


def parse_args(argv):
    path_ids, out = [], '/tmp/gca_course_scan.json'
    port = int(os.environ.get('GCA_PORT', 9333))
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--out' and i + 1 < len(argv):
            out = argv[i + 1]; i += 2; continue
        if a == '--port' and i + 1 < len(argv):
            port = int(argv[i + 1]); i += 2; continue
        for part in a.split(','):
            if part.strip().isdigit():
                path_ids.append(part.strip())
        i += 1
    return (path_ids or list(DEFAULT_PATHS.keys())), out, port


def collect_templates(c, path_ids):
    """从各路径页收集每门子课的代表 URL。

    两种 href 形态都要处理（实测坑）：
      - 未报名：`/paths/<pid>/course_templates/<tid>`  → 逐 template read-acts
      - 已报名：`/paths/<pid>/course_sessions/<sid>/...` → 逐 session 取代表 URL
    只认 course_templates 会让已报名路径（如 19）扫出 0 门课。
    返回 [(pid, topic, key, rep_url, title)]。
    """
    allmap, seen = [], set()
    for pid in path_ids:
        topic = DEFAULT_PATHS.get(pid, pid)
        gca.goto(c, '{}/paths/{}?locale=en'.format(gca.BASE, pid), wait=3.0)
        acts = gca.evj(c, gca.READ_ACTS_JS, []) or []
        for a in acts:
            h = a.get('href') or ''
            m = re.search(r'course_templates/(\d+)', h)
            if m:
                key, rep = 'template:' + m.group(1), gca.absurl(h)
            else:
                m = re.search(r'course_sessions/(\d+)', h)
                if not m:
                    continue
                key, rep = 'session:' + m.group(1), gca.absurl(h)
            if key not in seen:
                seen.add(key)
                allmap.append((pid, topic, key, rep, (a.get('title') or '?')[:45]))
    return allmap


def scan_one(c, rep_url):
    """读单门子课（代表 URL）的活动构成，按 href 里的 type 分类计数。"""
    gca.goto(c, rep_url, wait=2.5)
    acts = gca.evj(c, gca.READ_ACTS_JS, []) or []
    v = q = l = o = pending_nonlab = 0
    for a in acts:
        h = a.get('href') or ''
        if '/video/' in h: v += 1
        elif '/quizzes/' in h: q += 1
        elif '/labs/' in h: l += 1
        else: o += 1
        if not a.get('complete') and '/labs/' not in h and h:
            pending_nonlab += 1
    return len(acts), v, q, l, o, pending_nonlab


def main():
    path_ids, out, port = parse_args(sys.argv[1:])
    c = gca.client(port)
    allmap = collect_templates(c, path_ids)
    print('收集到 {} 门课（来自 {} 条路径）'.format(len(allmap), len(path_ids)), flush=True)

    results = []
    for pid, topic, key, rep, title in allmap:
        try:
            n, v, q, l, o, pend = scan_one(c, rep)
            results.append({'path': pid, 'topic': topic, 'key': key, 'acts': n,
                            'video': v, 'quiz': q, 'lab': l, 'other': o,
                            'pending_nonlab': pend, 'title': title})
        except Exception as e:
            results.append({'path': pid, 'topic': topic, 'key': key, 'error': str(e), 'title': title})
        time.sleep(0.25)

    # 排序：零 Lab + 有 Quiz + 未完成非Lab多 的优先（自主选课性价比）
    results.sort(key=lambda r: (r.get('lab', 999) == 0, r.get('quiz', 0),
                                r.get('pending_nonlab', 0)), reverse=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=1)

    # key 形如 session:4149757557（约19字符），列宽给足 22 避免数字列错位
    print('{:<6}{:<22}{:<6}{:<6}{:<6}{:<5}{:<6}{}'.format(
        '主题', 'key', '活动', '视频', 'Quiz', 'Lab', '待做', '标题'), flush=True)
    for r in results:
        if 'error' in r:
            print('{:<6}{:<22}ERR {}'.format(r['topic'], r['key'], r['error']), flush=True)
            continue
        print('{:<6}{:<22}{:<6}{:<6}{:<6}{:<5}{:<6}{}'.format(
            r['topic'], r['key'], r['acts'], r['video'], r['quiz'],
            r['lab'], r['pending_nonlab'], r['title']), flush=True)
    fast = [r['key'] for r in results if r.get('lab') == 0 and r.get('quiz', 0) > 0]
    print(json.dumps({'out': out, 'total': len(results),
                      'zero_lab_with_quiz': fast}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
