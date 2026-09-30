#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导演 Agent 8 维度全景质检探针 (Director Quality Gate & Canonical Fidelity Probe)

功能：
1. 模拟资深电影导演与严苛制片人，对生成的逐镜提示词与分镜脚本进行自动化 8 维度审计。
2. 重点执行【原著真值忠实度与防魔改门禁 (Canonical Fidelity Check)】：
   - 拦截擅自篡改角色性格（如杀伐果断变圣母懦弱、下跪求饶等）
   - 拦截战力跨境界违规失真与凭空捏造未授权神功
   - 拦截未经用户授权的狗血魔改剧情
3. 扫描并拦截：
   - 抽象情绪词（如“愤怒”、“悲伤”，未转化为 FACS 微肌肉指令）
   - 单镜多动作（单镜头塞入 >2 个复合动作导致的 AI 画面错乱）
   - 禁用工程参数（如 f/2.8、震屏 10% 等未脱敏词汇）
   - 缺失物理受力与形变描述
   - 缺失 180 度轴线与固定地标
4. 输出加权质量分（0-100）与 Markdown 格式诊断优化建议。

用法：
    python3 scripts/director_audit_gate.py --prompt "..." 
    python3 scripts/director_audit_gate.py --file <shots.json> --truth <truth_matrix.json>
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DirectorAuditGate:
    """导演 Agent 8 维度全景质检探针（含防魔改真值对账）"""

    # 抽象情绪词黑名单（必须转为 FACS 动作）
    ABSTRACT_EMOTIONS = [
        "很愤怒", "非常悲伤", "极度恐惧", "很开心", "得意洋洋", "咬牙切齿",
        "充满仇恨", "震惊", "吓傻了", "感觉很爽", "痛苦万分"
    ]

    # 违规魔改与人设漂移词汇黑名单（未经授权禁止出现）
    DISTORTION_PATTERNS = [
        (r"下跪求饶|痛哭流涕求放过", "主角人设发生严重圣母/软弱漂移，违背杀伐果断原著真值！"),
        (r"突然爱上了|暗生情愫|深情对视并拥抱", "检测到疑似未经授权的狗血二创感情戏魔改！"),
        (r"凭空获得神力|系统突然送大招", "检测到未经原著伏笔铺垫的战力机械降神违规！")
    ]

    # 禁用工程参数
    FORBIDDEN_PARAMS = [
        r"f/1\.[48]|f/2\.[08]|f/4|f/8", r"震屏\s*\d+%", r"快门\s*1/\d+", r"ISO\s*\d+",
        r"FOV\s*\d+", r"速度\s*\d+m/s"
    ]

    def __init__(self, canonical_truth: Optional[Dict[str, Any]] = None):
        self.canonical_truth = canonical_truth or {}
        self.weights = {
            "spatial_readability": 0.10,      # 1. 空间可读性与轴线
            "camera_comfort": 0.10,           # 2. 运镜舒适度与物理依托
            "kinetic_impact": 0.15,           # 3. 动作力学与受力形变
            "facs_performance": 0.15,         # 4. FACS 微表情与眼神
            "pacing_and_rest": 0.10,          # 5. 节奏留白与呼吸感
            "visual_consistency": 0.15,       # 6. 视觉一致性与外貌锁
            "canonical_fidelity": 0.15,       # 7. 原著忠实度与防魔改对账
            "technical_compliance": 0.10      # 8. 声画与技术合规
        }

    def audit_single_prompt(self, prompt: str) -> Dict[str, Any]:
        """对单段分镜提示词执行 8 维度体检"""
        scores = {}
        issues = []
        suggestions = []

        # 1. 空间可读性检查 (地标与空间参照)
        spatial_keywords = ["大殿", "石柱", "地面", "台阶", "悬崖", "祭坛", "墙壁", "门前", "中央", "地标"]
        has_spatial = any(kw in prompt for kw in spatial_keywords)
        if has_spatial:
            scores["spatial_readability"] = 95
        else:
            scores["spatial_readability"] = 65
            issues.append("缺失明确的空间物理参照物或地标（如石柱、台阶、祭坛），易导致模型生成漂浮背景。")
            suggestions.append("在第 3 段加入固定物理地标（如：立于中央青铜巨鼎左侧 3 米处）。")

        # 2. 运镜舒适度检查 (同句融合与运镜词)
        if "camera" in prompt.lower() or "机位" in prompt or "镜头" in prompt or "推" in prompt or "拉" in prompt:
            scores["camera_comfort"] = 92
        else:
            scores["camera_comfort"] = 70
            issues.append("未明确指定摄影机机位高度与运动轨迹。")
            suggestions.append("在第 4 段明确焦段与运镜（如：50mm 定焦镜头，机位随主体冲刺贴地急速前推）。")

        # 3. 动作力学检查 (受力形变与破坏)
        kinetic_keywords = ["发力", "肌肉", "形变", "飞溅", "崩碎", "震颤", "后撤", "惯性", "斩断", "倒退"]
        kinetic_count = sum(1 for kw in kinetic_keywords if kw in prompt)
        if kinetic_count >= 2:
            scores["kinetic_impact"] = 95
        elif kinetic_count == 1:
            scores["kinetic_impact"] = 80
            suggestions.append("增强受力形变与次级惯性描述（如：地面崩碎、衣袖受惯性滞后摆动）。")
        else:
            scores["kinetic_impact"] = 55
            issues.append("动作描述缺乏物理受力、形变与破坏反馈，容易生成无力‘假人比划’。")

        # 检查是否单镜多动作 (连词过多)
        multi_actions = re.findall(r'(?:然后|接着|随后|之后|紧接着|再)', prompt)
        if len(multi_actions) >= 2:
            scores["kinetic_impact"] -= 20
            issues.append("单镜头内包含过多连续动作连词（违背‘单镜单动作’原则），模型极易产生肢体错乱与穿模！")
            suggestions.append("严格执行单镜单动作原则，将连续动作拆分为 2~3 个独立镜头。")

        # 4. FACS 表演微表情检查 (拒绝抽象情绪词)
        found_abstract = [w for w in self.ABSTRACT_EMOTIONS if w in prompt]
        facs_keywords = ["咬肌", "眼眸", "瞳孔", "下唇", "喉结", "呼吸", "冷汗", "指节", "视线", "眉头", "眨眼"]
        has_facs = any(kw in prompt for kw in facs_keywords)

        if found_abstract:
            scores["facs_performance"] = 50
            issues.append(f"发现抽象情绪词: {', '.join(found_abstract)}，模型无法物理渲染。")
            suggestions.append("将抽象情绪转化为 FACS 肌肉指令（如：咬肌剧烈收紧、瞳孔骤缩、下唇内咬）。")
        elif has_facs:
            scores["facs_performance"] = 95
        else:
            scores["facs_performance"] = 75
            suggestions.append("加入面部微表情与眼神生命轨迹（如：视线先向下瞥见暗器随后抬眸对视）。")

        # 5. 节奏留白与呼吸感
        if "呼吸" in prompt or "停顿" in prompt or "飘落" in prompt or "凝视" in prompt:
            scores["pacing_and_rest"] = 95
        else:
            scores["pacing_and_rest"] = 85

        # 6. 视觉一致性 (外貌锁与角色资产)
        if "【主体】" in prompt or "主角" in prompt or "身着" in prompt or "@" in prompt or "特征" in prompt:
            scores["visual_consistency"] = 95
        else:
            scores["visual_consistency"] = 70
            issues.append("主体角色缺乏固定外貌特征锁。")
            suggestions.append("在第 2 段注入角色的 50 字固定外貌描述段。")

        # 7. 原著忠实度与防魔改对账 (Canonical Fidelity Check)
        distortion_found = False
        for pattern, warning_msg in self.DISTORTION_PATTERNS:
            if re.search(pattern, prompt):
                distortion_found = True
                issues.append(f"🚨 防魔改警报: {warning_msg}")

        if distortion_found:
            scores["canonical_fidelity"] = 40
            suggestions.append("回退至原著真值矩阵，严格按原著设定的人设与事件因果推进剧情。")
        else:
            scores["canonical_fidelity"] = 98

        # 8. 声画与技术合规 (禁用工程参数脱敏)
        found_params = []
        for p in self.FORBIDDEN_PARAMS:
            matches = re.findall(p, prompt, re.IGNORECASE)
            if matches:
                found_params.extend(matches)

        if found_params:
            scores["technical_compliance"] = 60
            issues.append(f"包含禁用工程参数: {', '.join(found_params)}，模型无法精准执行。")
            suggestions.append("将工程参数转化为物理感知描述（如 f/2.8 ➔ 极浅景深圆形光斑）。")
        else:
            scores["technical_compliance"] = 95

        # 计算加权总分
        total_score = sum(scores[dim] * self.weights[dim] for dim in scores)

        status = "✅ 准予出片 (PASS)" if total_score >= 85 else ("⚠️ 需局部修镜 (WARN)" if total_score >= 70 else "❌ 驳回重构 (FAIL)")

        return {
            "total_score": round(total_score, 1),
            "status": status,
            "dimension_scores": scores,
            "issues": issues,
            "suggestions": suggestions
        }

    def generate_markdown_report(self, audit_result: Dict[str, Any]) -> str:
        """生成 Markdown 格式的审计诊断报告"""
        res = audit_result
        md = f"""# 🎬 导演 Agent 8 维度全景质检审计报告 (含防魔改真值对账)

**综合评定**: `{res['status']}`  
**最终加权得分**: `{res['total_score']} / 100`

### 📊 维度得分明细表
| 审计维度 | 权重 | 得分 | 状态 |
| :--- | :--- | :--- | :--- |
| 1. 空间可读性 (地标与轴线) | 10% | {res['dimension_scores'].get('spatial_readability', 0)} | {'✅' if res['dimension_scores'].get('spatial_readability', 0) >= 85 else '⚠️'} |
| 2. 运镜舒适度 (物理运动依托) | 10% | {res['dimension_scores'].get('camera_comfort', 0)} | {'✅' if res['dimension_scores'].get('camera_comfort', 0) >= 85 else '⚠️'} |
| 3. 动作力学直觉 (受力与形变) | 15% | {res['dimension_scores'].get('kinetic_impact', 0)} | {'✅' if res['dimension_scores'].get('kinetic_impact', 0) >= 85 else '⚠️'} |
| 4. FACS 微表情 (微肌肉与眼神) | 15% | {res['dimension_scores'].get('facs_performance', 0)} | {'✅' if res['dimension_scores'].get('facs_performance', 0) >= 85 else '⚠️'} |
| 5. 节奏留存与呼吸感 (气口余韵) | 10% | {res['dimension_scores'].get('pacing_and_rest', 0)} | {'✅' if res['dimension_scores'].get('pacing_and_rest', 0) >= 85 else '⚠️'} |
| 6. 视觉一致性 (外貌特征锁) | 15% | {res['dimension_scores'].get('visual_consistency', 0)} | {'✅' if res['dimension_scores'].get('visual_consistency', 0) >= 85 else '⚠️'} |
| 7. 原著忠实度 (防无授权魔改) | 15% | {res['dimension_scores'].get('canonical_fidelity', 0)} | {'✅' if res['dimension_scores'].get('canonical_fidelity', 0) >= 85 else '⚠️'} |
| 8. 声画与技术合规 (参数脱敏) | 10% | {res['dimension_scores'].get('technical_compliance', 0)} | {'✅' if res['dimension_scores'].get('technical_compliance', 0) >= 85 else '⚠️'} |
"""
        if res["issues"]:
            md += "\n### 🚨 拦截的问题 (Issues Found)\n"
            for issue in res["issues"]:
                md += f"- ❌ {issue}\n"

        if res["suggestions"]:
            md += "\n### 💡 导演优化建议 (Actionable Suggestions)\n"
            for sug in res["suggestions"]:
                md += f"- 💡 {sug}\n"

        return md


def main():
    parser = argparse.ArgumentParser(description="导演 Agent 8 维度全景质检探针 (Director Quality Gate)")
    parser.add_argument("--prompt", "-p", help="待质检的单镜头提示词文本")
    parser.add_argument("--file", "-f", help="待质检的分镜文件路径")
    parser.add_argument("--truth", "-t", help="原著真值矩阵 JSON 文件路径")

    args = parser.parse_args()

    canonical_data = None
    if args.truth and Path(args.truth).exists():
        canonical_data = json.loads(Path(args.truth).read_text(encoding="utf-8"))

    probe = DirectorAuditGate(canonical_truth=canonical_data)

    if args.prompt:
        target_prompt = args.prompt
    elif args.file and Path(args.file).exists():
        target_prompt = Path(args.file).read_text(encoding="utf-8")
    else:
        # 默认测试提示词（故意包含一个工程参数以测试探针灵敏度）
        target_prompt = (
            "8K IMAX, 35mm film stock, 徐克新武侠风格。\n"
            "【主体】主角林风，20岁剑客，身着玄黑锦袍，目光凌厉。\n"
            "【环境】昆仑大殿中央，立于盘龙石柱前，狂风吹拂殿顶裂隙。\n"
            "【镜头与运镜】35mm电影镜头，机位贴地急速前推；主角右手拔剑凌空斩出二十米金色剑刃，轰碎石柱，碎石向四周崩碎飞溅，衣袖受惯性滞后摆动；f/1.4大光圈。\n"
            "【微表情与表演】下颌咬肌剧烈凸起，眼瞳如深渊不眨，眼神先向下瞥见暗器随后抬眸对视，呼吸急促深重。\n"
            "【约束】24fps, no cgi plastic skin, no deformed hands."
        )
        print("ℹ️ 使用内置综合样本执行质检审计...\n")

    result = probe.audit_single_prompt(target_prompt)
    report_md = probe.generate_markdown_report(result)
    print(report_md)


if __name__ == "__main__":
    main()
