#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""转储某路径内各子课程的内部活动清单，用于发现顶层看不到的 Quiz（如 ADK 3545）。

吸收自 /tmp/gca_dump_path.py，改为复用 gca.py 的 client/goto/evj/READ_ACTS_JS；
支持 GCA_PORT 与 --port，不写死 9333。

用法: dump_path.py <path_id> [--port N]
输出: JSON，含 path_activity_count 与 courses[]（每门 key/rep/count/acts）。
"""
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gca


def main():
    argv = sys.argv[1:]
    port = int(os.environ.get('GCA_PORT', 9333))
    if '--port' in argv:
        i = argv.index('--port')
        if i + 1 < len(argv):
            port = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    pid = argv[0] if argv else '3545'

    c = gca.client(port)
    path_url = '{}/paths/{}?locale=en'.format(gca.BASE, pid)
    gca.goto(c, path_url, wait=3.0)
    path_acts = gca.evj(c, gca.READ_ACTS_JS, []) or []

    # 每门子课取一个代表 href，去重
    reps, seen = [], set()
    for a in path_acts:
        h = a.get('href') or ''
        if '/course_sessions/' in h:
            key = 'session:' + h.split('/course_sessions/')[1].split('/')[0]
        elif '/course_templates/' in h:
            key = 'template:' + h.split('/course_templates/')[1].split('/')[0]
        else:
            continue
        if key not in seen:
            seen.add(key)
            reps.append({'key': key, 'rep': gca.absurl(h), 'path_href': h})

    courses = []
    for r in reps:
        gca.goto(c, r['rep'], wait=2.2)
        acts = gca.evj(c, gca.READ_ACTS_JS, []) or []
        courses.append({'key': r['key'], 'rep': r['rep'], 'path_href': r['path_href'],
                        'count': len(acts), 'acts': acts})

    print(json.dumps({'path_id': pid, 'path_activity_count': len(path_acts),
                      'courses': courses}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
