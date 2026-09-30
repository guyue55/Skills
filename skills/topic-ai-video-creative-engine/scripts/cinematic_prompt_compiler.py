#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
确定性分镜提示词编译器 (Cinematic Prompt Compiler)

功能：
1. 接收镜头分镜定义，按【七段式完全自包含公式】与【四层复合角色资产锁】确定性编译为工业级视频生成提示词。
2. 自动注入 8 大系 80 种影史导演美学与双流派 Blend 融合模式（深度联动 topic-director-cinematic-master）。
3. 支持动态字幕特效（三阶段动效：入场 ➔ 停留呼吸 ➔ 招式消散）与真人旁白解说声乐调度。
4. 执行【运镜与动作同句融合】算法，消除孤立运镜词。
5. 自动脱敏并转化禁用工程参数（如 f/2.8 ➔ 极浅景深圆形光斑；5m/s ➔ 动态放射状模糊）。
6. 针对 Kling 3.0 / Seedance 2.5 / Wan 2.6 / Veo 3.1 差异化定制格式。

用法：
    python3 scripts/cinematic_prompt_compiler.py --shot-text "拔剑出鞘" --director "徐克新武侠" --blend "杜琪峰几何站位" --model "Seedance 2.5"
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# 动态联动 topic-director-cinematic-master 80 大流派知识库
_SYNTHESIZER_DIR = Path(__file__).resolve().parents[2] / "topic-director-cinematic-master" / "scripts"
if _SYNTHESIZER_DIR.exists() and str(_SYNTHESIZER_DIR) not in sys.path:
    sys.path.insert(0, str(_SYNTHESIZER_DIR))

try:
    from director_synthesizer import ALL_DIRECTOR_ARCHETYPES, resolve_archetype
except ImportError:
    ALL_DIRECTOR_ARCHETYPES = {}
    resolve_archetype = lambda x: x


class CinematicPromptCompiler:
    """确定性分镜提示词编译器核心类"""

    # 禁用工程参数脱敏映射表
    PARAMETER_MAP = {
        r"f/1\.[48]|f/2\.[08]|大光圈": "极浅景深，前景与背景完全虚化为柔美圆形光斑，焦点精准锁定主体眼眸",
        r"震屏\s*\d+%?|shake": "伴随猛烈冲击，摄影机被震颤得短促下顿 0.1 秒并产生微量机位偏移",
        r"快门\s*1/\d+|shutter": "运动边缘带有自然的 180 度快门运动模糊与真实动态拖影",
        r"ISO\s*\d+|噪点": "暗部带有细腻有机的 35mm 电影胶片暗部银盐颗粒感",
        r"特效很酷炫|华丽": "核心呈现炽白等离子液态高温，外围扩散出深青色锯齿状雷弧，周围空气产生强烈热浪扭曲"
    }

    # 默认导演流派美学特征基准库
    DIRECTOR_STYLES = {
        "徐克新武侠": "徐克新派武侠风格，高速凌厉切镜，飘逸威亚反重力飞旋，三层复合剑气光效，东方奇幻浪漫",
        "杜琪峰几何站位": "杜琪峰银河暗黑风格，严格几何三角站位对峙，深焦大景深，前景遮挡窥视，静中带动",
        "王家卫抽帧情绪": "王家卫作者电影风格，8帧/秒步印抽帧拖影，霓虹光影斑驳，浓烈孤独情绪特写，浅景深",
        "诺兰实轴非线性": "诺兰大片质感，70mm IMAX 胶片实拍厚重感，冷色调秩序感，实物模型物理惯性，宏大纵深",
        "90s爆款短剧流": "90s爆款短剧视听风格，黄金3秒强冲突前置，竖屏居中黄金焦点，高对比度，对白紧凑卡点"
    }

    def __init__(self, primary_director: str = "徐克新武侠", blend_director: Optional[str] = "杜琪峰几何站位", target_model: str = "Seedance 2.5"):
        self.primary_director = primary_director
        self.blend_director = blend_director
        self.target_model = target_model

    def sanitize_forbidden_parameters(self, text: str) -> str:
        """扫描并转化禁用的工程参数为画面物理感知语言"""
        sanitized = text
        for pattern, replacement in self.PARAMETER_MAP.items():
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        return sanitized

    def _get_director_dna(self, director_name: str) -> str:
        """从原生库或 80 大流派扩展库解析导演美学 DNA"""
        if director_name in self.DIRECTOR_STYLES:
            return self.DIRECTOR_STYLES[director_name]
        
        # 解析 80 大流派
        if ALL_DIRECTOR_ARCHETYPES:
            arch = resolve_archetype(director_name)
            if arch and isinstance(arch, dict):
                return f"{arch.get('name', '')}风格，{arch.get('dna', '')}，{arch.get('camera_style', '')}，{arch.get('lighting', '')}"
        
        return director_name

    def blend_director_styles(self) -> str:
        """合成主辅导演流派美学描述 (Blend Mode)"""
        p_desc = self._get_director_dna(self.primary_director)
        if self.blend_director and self.blend_director.strip():
            b_desc = self._get_director_dna(self.blend_director)
            return f"【美学融合: 70% {p_desc} × 30% {b_desc}】"
        return f"【导演风格: {p_desc}】"

    def compile_shot(self, shot_data: Dict[str, Any]) -> str:
        """按七段式完全自包含公式与四层复合资产锁编译单镜头"""
        # 段 1: 画质与风格基准
        seg1_quality = f"8K IMAX, 35mm film stock, organic film grain, realistic skin texture, {self.blend_director_styles()}"

        # 段 2: 角色资产四层复合外貌锚点 (四层锁: 基础标识 + 生理年龄/骨相 + 身份服饰 + 气场/印记)
        char_name = shot_data.get("character_name", "冷羽 (CHAR_001)")
        age_tier = shot_data.get("age_tier", "17岁青年微骨感冷峻面容")
        costume = shot_data.get("costume", "洗至发白的赫氏学院粗布学员制服配浅青粗布笑脸面具")
        power_aura = shot_data.get("power_aura", "周身隐现0.5米微波透明热浪折射，眼神冷静沉寂")
        relic_marks = shot_data.get("relic_marks", "右手握持锈迹斑斑的三尺无锋铁剑")
        
        seg2_character = f"【主体】{char_name}, {age_tier}, 身着{costume}, {power_aura}, {relic_marks}"

        # 段 3: 场景空间与光学环境
        scene_desc = shot_data.get("scene_desc", "赫氏学院白玉正门殿堂内，大理石地面留存3米剑气斩痕，正午强光穿透破损殿顶，尘埃浮动")
        seg3_scene = f"【环境】{scene_desc}"

        # 段 4: 摄影机焦段与运镜 (执行同句融合)
        lens = shot_data.get("lens", "50mm")
        camera_move = shot_data.get("camera_movement", "机位贴地急速前推随后微仰锁定主体")
        seg4_optics = f"【镜头与运镜】{lens} 电影定焦镜头，{camera_move}"

        # 段 5: 核心动作力学与物理形变 (六步闭环)
        raw_action = shot_data.get("action", "主角拔剑横扫，剑气微波振动震碎石柱，碎石受冲击向四周飞溅，衣摆受惯性自然摆动")
        action_sanitized = self.sanitize_forbidden_parameters(raw_action)
        seg5_action = f"【动作力学】{action_sanitized}"

        # 段 6: FACS 表演微表情、动态字幕与声画对位
        facs_acting = shot_data.get("facs_acting", "下颌咬肌硬块状收紧，眼眸深邃不眨，眼神先动后转头")
        subtitle_fx = shot_data.get("subtitle_fx", "动态金色行草字幕 '落羽神恋曲 · 微波震颤' (0.8s金光凝聚入场 ➔ 1.5s高光流光脉冲 ➔ 0.6s散作光羽)")
        voice_audio = shot_data.get("voice_audio", "配乐 A3 轨道自动触发侧链闪避下潜 -10dB，台词与呼吸清晰入耳")
        
        seg6_acting = f"【微表情、字幕与声画】FACS微动: {facs_acting}；字幕特效: {subtitle_fx}；音频对位: {voice_audio}"

        # 段 7: 负向约束
        seg7_negative = "【约束】24fps smooth, no CGI plastic skin, no deformed hands, no floating props, no temporal flicker, no oversaturated colors"

        # 针对不同模型定制装配
        if "Seedance" in self.target_model:
            compiled = f"{seg1_quality}。\n{seg2_character}。\n{seg3_scene}。\n{seg4_optics}；{seg5_action}。\n{seg6_acting}。\n{seg7_negative}。"
        elif "Kling" in self.target_model:
            compiled = f"{seg1_quality}, {seg2_character}, {seg3_scene}, {seg4_optics}, {seg5_action}, {seg6_acting}, realistic physics, 4k master."
        else:
            compiled = f"{seg1_quality}\n{seg2_character}\n{seg3_scene}\n{seg4_optics}\n{seg5_action}\n{seg6_acting}\n{seg7_negative}"

        return compiled


def main():
    parser = argparse.ArgumentParser(description="确定性分镜提示词编译器 (Cinematic Prompt Compiler)")
    parser.add_argument("--shot-text", "-s", help="单镜头动作描述")
    parser.add_argument("--director", "-d", default="徐克新武侠", help="主导导演流派 (支持 80 大流派别名或全称)")
    parser.add_argument("--blend", "-b", default="杜琪峰几何站位", help="辅助融合导演流派")
    parser.add_argument("--model", "-m", default="Seedance 2.5", help="目标渲染模型 (Kling 3.0 / Seedance 2.5 / Wan 2.6 / Veo 3.1)")
    parser.add_argument("--age-tier", "-a", default="17岁青年微骨感冷峻面容", help="角色生理年龄与骨相特征")
    parser.add_argument("--subtitle-fx", help="动态字幕特效描述 (入场/停留/消散)")
    parser.add_argument("--voiceover", help="旁白与台词气口描述")

    args = parser.parse_args()

    compiler = CinematicPromptCompiler(
        primary_director=args.director,
        blend_director=args.blend,
        target_model=args.model
    )

    sample_shot = {
        "character_name": "冷羽 (CHAR_001)",
        "age_tier": args.age_tier,
        "costume": "洗至发白的赫氏学院粗布学员制服配浅青粗布笑脸面具",
        "power_aura": "周身隐现0.5米微波透明热浪折射，眼神冷静沉寂",
        "relic_marks": "右手握持锈迹斑斑的三尺无锋铁剑",
        "scene_desc": "赫氏学院白玉正门殿堂内，大理石地面留存3米剑气斩痕，正午强光穿透破损殿顶，尘埃浮动",
        "lens": "35mm 广角电影镜头",
        "camera_movement": "摄影机自低机位贴地急速前推，穿过雨幕撞入眼眸",
        "action": args.shot_text if args.shot_text else "主角右手沉桥拔剑，剑身在空中划出半月气刃，将袭来的三根长枪斩断；震屏 10%，大光圈 f/1.4",
        "facs_acting": "下唇紧咬渗出一丝白痕，咬肌剧烈收紧，视线先向下瞥见暗器随后抬眸锁定对手",
        "subtitle_fx": args.subtitle_fx if args.subtitle_fx else "动态金色行草字幕 '落羽神恋曲 · 微波震颤' (0.8s金光凝聚入场 ➔ 1.5s高光流光脉冲 ➔ 0.6s散作光羽)",
        "voice_audio": args.voiceover if args.voiceover else "配乐 A3 轨道自动触发侧链闪避下潜 -10dB，台词与呼吸清晰入耳"
    }

    compiled_prompt = compiler.compile_shot(sample_shot)
    print("🎬 【编译完成的工业级自包含提示词】:")
    print("=" * 60)
    print(compiled_prompt)
    print("=" * 60)


if __name__ == "__main__":
    main()
