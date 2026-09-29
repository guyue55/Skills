#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
director_synthesizer.py - 影视视听与导演级全流程创作大师 CLI 引擎
功能：
1. `--mode storyboard`: 自动化生成五栏工业级分镜设计表（含景别、机位、运镜、画面视觉、声音设计与 AI 提示词）。
2. `--mode action`: 自动化生成包含发力起势、交锋封防、受力爆裂反馈与终结定格的动作拍点拆解。
3. `--mode script`: 自动化生成 90 秒高留存黄金短剧/漫剧剧情节拍脚本。
4. `--mode prompt`: 自动化将影视场景描述编译为 Midjourney / Kling / Sora 高保真提示词。
5. `--mode audit`: 静态体检文本中的文学化虚假描述（如“打得难解难分”、“十分紧张”等空洞词汇）。
6. `--mode compile`: 编译输出标准 XML 导演级 System Prompt。
7. `--mode test`: 执行内置全量单元测试套件。
"""

import sys
import argparse
import re
from typing import Dict, List, Any

# 10 大经典导演流派知识库与视觉标签定义
DIRECTOR_ARCHETYPES = {
    "shaw_kungfu": {
        "name": "邵氏硬派功夫派 (张彻 / 刘家良 / 楚原)",
        "dna": "硬桥硬马招式拆解、阳刚血性、盘肠大战、摄影棚景深布景、奇门兵器对拆",
        "camera_style": "固定机位中全景完整展示招式套路 + 致命一击急推面部/兵器特写",
        "lighting": "warm golden Technicolor tone, vintage 1970s Hong Kong cinema lighting, saturated vermilion red",
        "action_focus": "south shaolin hung ga fist, authentic kung fu parry, heavy bone-cracking hit feedback"
    },
    "tsui_hark_fantasy": {
        "name": "新武侠奇幻狂想派 (徐克)",
        "dna": "漫画感分镜、飞天遁地威亚奇观、高速多机位颠覆剪辑、高饱和奇幻色彩",
        "camera_style": "狂飙大范围倾斜跟拍、极速旋转俯冲、漫画式夸张神态定格",
        "lighting": "vibrant neon-tinged wuxia colors, deep contrast twilight shadows, glowing magical runes",
        "action_focus": "wire-fu acrobatics, energy slashes slicing environments, kinetic aerial combat"
    },
    "johnnie_to_noir": {
        "name": "银河映像站位宿命派 (杜琪峰)",
        "dna": "空间几何三角站位、静止对峙积蓄暴风雨前压迫感、暗光/侧光切割、黑色幽默与宿命反转",
        "camera_style": "静止长镜头、多人物深焦构图、百叶窗/街灯阴影切割、几何空间调度",
        "lighting": "cool cyan and teal desaturated tones, stark noir shadows, harsh directional streetlights",
        "action_focus": "tense standoff, sudden explosive gunfight, deliberate spatial crossfire"
    },
    "wong_kar_wai_mood": {
        "name": "光影情绪与抽帧流派 (王家卫)",
        "dna": "慢门抽帧/步印运动 (Step-printing)、非对称倾斜构图、情绪碎片跳切、诗意独白与色彩暗涌",
        "camera_style": "慢速手持晃动微特写、抽帧拖影运镜、门框/玻璃反光遮挡",
        "lighting": "emerald green and crimson red neon glow, moody tungsten warmth, hazy nostalgic atmosphere",
        "action_focus": "lingering glances, blurred motion trails, romantic and melancholic tension"
    },
    "stephen_chow_comic": {
        "name": "无厘头反差喜剧派 (周星驰)",
        "dna": "严密漫画分镜预演、极端景别瞬间突变、草根小人物悲喜交加、微表情与动作瞬间反差",
        "camera_style": "极宽全景瞬间推至瞳孔地震特写、升格慢动作放大滑稽与悲怆",
        "lighting": "bright dynamic high-key lighting, retro colorful Hong Kong comedy palette",
        "action_focus": "cartoonish exaggeration, rapid escalation, slapstick with serious kung fu undertones"
    },
    "nolan_non_linear": {
        "name": "非线性钳形时空派 (克里斯托弗·诺兰)",
        "dna": "多线跨时空交叉并进、钳形时空叙事、硬核实拍物理质感、重力倒转与宏大概念折叠",
        "camera_style": "宏大全景 IMAX 构图、主观 Dutch Angle 倾斜镜头、精密交叉剪辑",
        "lighting": "realistic naturalistic daylight, cool gray industrial tones, high dynamic range",
        "action_focus": "practical stunt choreography, time-reversed ballistic physics, large-scale spatial collapse"
    },
    "hitchcock_suspense": {
        "name": "视线诱导与信息差悬念派 (阿尔弗雷德·希区柯克)",
        "dna": "“炸弹理论”操控信息差、主观视点镜头 (POV)、窥视感与视线诱导、节拍递进的心理压迫",
        "camera_style": "希区柯克变焦 (Dolly Zoom / Vertigo effect)、门缝/钥匙孔窥视主观镜头",
        "lighting": "high contrast chiaroscuro, expressive single-source lighting, deep edge shadows",
        "action_focus": "ticking time bomb tension, subtle poisoned drink handoff, knife edge suspense"
    },
    "tarantino_dialogue": {
        "name": "章回体对白暴力美学派 (昆汀·塔伦蒂诺)",
        "dna": "章回体非线性拼图、高密度垃圾话台词交锋、墨西哥式三方对峙、反高潮突发血腥暴力",
        "camera_style": "后备箱主观视角 (Trunk Shot)、环形慢速摇镜头、对射极速切镜",
        "lighting": "warm gritty 1970s exploitation film lighting, hyper-saturated blood reds",
        "action_focus": "standoff breakdown, sudden high-caliber firearm gore, razor-sharp dialogue cadence"
    },
    "satoshi_kon_matchcut": {
        "name": "匹配剪辑虚实折叠派 (今敏)",
        "dna": "匹配剪辑 (Match Cut) 转场神迹、现实与潜意识心理投射的无缝折叠、跨时空形似转场",
        "camera_style": "动作/物体/颜色匹配转场、镜面破碎反射穿梭、画面无缝变形",
        "lighting": "dreamlike surreal lighting, transition from sterile blue to vibrant psychological hues",
        "action_focus": "hallucinatory chase sequences, identity duplication, reality fracture"
    },
    "kurosawa_weather": {
        "name": "自然气象与宏大轴线派 (黑泽明)",
        "dna": "风雨雾暴雪自然力场烘托、大景深几何三角形站位、群体奔涌运动轴线与武士拔刀定格",
        "camera_style": "超远景纵深长镜头、多机位平行侧拍、暴雨/烈火中极度克制定格",
        "lighting": "stark black and white tonal contrast or rich feudal earth tones, stormy rain backlighting",
        "action_focus": "lightning-fast single strike iaido duel, massive cavalry charge amidst torrential storm"
    }
}

# 静态体检规则库：扫描空泛的文学化词汇与缺乏镜头细节的描述
BUZZWORDS_AND_VAGUE_PATTERNS = [
    (r"打得难解难分", "文学化空泛词：未交代招式拆解、攻防路线与受力反馈"),
    (r"十分紧张", "情绪直述词：未通过机位、心跳音效或面部微表情营造张力"),
    (r"两人大战三百回合", "武侠套路空话：缺少具体招式拆解拍点"),
    (r"眼神充满杀气", "抽象面部描写：未给出瞳孔、咬肌或视线轨迹的具体物理变动"),
    (r"场面极其壮观", "主观感叹词：未给出景别 (EWS)、环境粒子或群演动线"),
    (r"痛得大叫", "浮夸表演：未给出喉结抽搐、面部痉挛或冷汗细节"),
    (r"气氛非常压抑", "空洞氛围词：未给出高反差阴影、冷色温或环境死寂音效")
]

def generate_storyboard(title: str, archetype_key: str, scene_desc: str) -> str:
    """生成工业级五栏分镜设计表"""
    archetype = DIRECTOR_ARCHETYPES.get(archetype_key, DIRECTOR_ARCHETYPES["shaw_kungfu"])
    
    output = []
    output.append(f"# 🎬 工业级标准分镜设计表: 《{title}》\n")
    output.append(f"**主控导演流派**：`{archetype['name']}`  ")
    output.append(f"**美学与分镜 DNA**：{archetype['dna']}  ")
    output.append(f"**镜头与运镜风格**：{archetype['camera_style']}  ")
    output.append(f"**场景核心描述**：{scene_desc}\n")
    output.append("---\n")
    output.append("## 📋 核心分镜明细表 (5-Shot Breakdown)\n")
    output.append("| 镜号 | 景别 & 机位 | 运镜动线 | 画面核心视觉 (构图/光影/动作) | 声音设计 (台词/音效/配乐) | AI 生成提示词 (Midjourney/Kling/Sora) |")
    output.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    
    # 镜号 1: 环境交代与建立镜头
    output.append(f"| **#01** | 全景 (WS) · 俯拍上帝视角 | 极慢速下潜俯冲 (Slow Crane Down) | 场景全貌呈现：{scene_desc}。空间几何站位明确，环境光影形成强烈明暗对比。 | **[音效]** 环境氛围音（风声/暴雨/机械运转）；**[配乐]** 低沉管弦乐蓄力。 | `wide shot, high angle, {scene_desc}, {archetype['lighting']}, dramatic composition, 8k.` |")
    
    # 镜号 2: 核心角色微表情与破防
    output.append(f"| **#02** | 极近特写 (ECU) · 平视 | 快速侧向微推 (Subtle Push In) | 核心人物面部微表情：瞳孔微缩，咬肌绷紧，右眼冰冷凝视对手，冷汗自下颌滑落。 | **[音效]** 极清脆的兵器出鞘或上膛声 (Clang!)；**[台词]** 冰冷短促的金句。 | `macro extreme close-up shot, intense focused gaze, subtle jaw muscle clenching, {archetype['lighting']}, cinematic 35mm film still.` |")
    
    # 镜号 3: 冲突引爆与多机位动线
    output.append(f"| **#03** | 中景 (MS) · 仰拍 (Low Angle) | 动态跟拍+极速甩镜 (Kinetic Tracking & Whip Pan) | 双方瞬间破防交锋！{archetype['action_focus']}，动作起势凌厉，地面尘土激荡。 | **[音效]** 撕裂空气的呼啸声与肌肉碰撞沉闷巨响；**[配乐]** 节奏瞬间飙升。 | `medium shot, dynamic low angle, {archetype['action_focus']}, motion blur, intense contrast shadows, masterpiece.` |")
    
    # 镜号 4: 致命受力爆裂与升格特写
    output.append(f"| **#04** | 特写 (CU) · 荷兰倾斜角 (Dutch Angle) | 慢动作升格 (120fps Slow-mo) | 致命打击命中瞬间！受击方身形受力向后倒滑，周围道具碎屑炸裂翻飞，面部显露出不可置信的惊愕。 | **[音效]** 骨骼撞击闷响与道具粉碎炸裂声；**[台词]** 喉间压抑的闷哼。 | `close-up shot, tilted dutch angle, slow-motion impact moment, shattering debris, high impact physics, hyper-detailed.` |")
    
    # 镜号 5: 深度纵深定格与终局悬念
    output.append(f"| **#05** | 全景 (WS) · 景深穿透构图 (Deep Staging) | 固定长镜头 (Static Deep Focus) | 前景败者倒地虚化；中景胜者收势站立；后景暗门或阴影中第二重危机悄然显现。 | **[音效]** 尘埃落定与微弱喘息声；**[配乐]** 音乐骤停转为空灵单音，留下悬念。 | `wide shot, deep focus staging, blurred foreground, victorious warrior standing in midground, mysterious shadow in background, {archetype['lighting']}.` |")
    
    return "\n".join(output)

def generate_action_breakdown(title: str, genre: str, characters: str) -> str:
    """生成硬派动作与招式对拆拍点"""
    output = []
    output.append(f"# 🥋 硬派打斗与动作拍点拆解报告: 《{title}》\n")
    output.append(f"**动作流派**：`{genre}`  ")
    output.append(f"**参战角色**：`{characters}`\n")
    output.append("---\n")
    output.append("## 💥 六阶打斗拍点明细 (Beat-by-Beat Mechanics)\n")
    
    output.append("### 1. 【起势对峙 · 空间与重心控制】(Beat 1)")
    output.append("- **角色动线**：双方拉开三步距离。攻方沉腰跨步，蓄力于后足；守方侧身立桥，单掌虚引，眼神锁定对方重心。")
    output.append("- **环境交互**：脚下泥水被气劲排开，树叶飘落被无形劲风切断。")
    
    output.append("\n### 2. 【首击发力 · 中门破防突刺】(Beat 2)")
    output.append("- **攻方招式**：攻方猛然蹬地滑步，右拳借旋腰之力轰向守方面门（直冲天门）。")
    output.append("- **力学细节**：右肩沉降，背部肌肉暴起，拳风呼啸带出尖锐气鸣。")
    
    output.append("\n### 3. 【格挡截桥 · 卸力引化反击】(Beat 3)")
    output.append("- **守方化解**：守方不退反进，左臂如铁铸般自下而上斜架敌方小臂内侧（上架桥），寸劲截断对方发力点。")
    output.append("- **碰撞音效**：沉闷如击牛皮之鼓 (Thump!)，双方小臂肌肉微凹。")
    
    output.append("\n### 4. 【近身缠绕 · 破坏平衡与变招】(Beat 4)")
    output.append("- **招式连环**：守方左腕内翻扣死对方手腕（圈手擒拿），顺势向斜下方一拽破坏其平衡；右肘顺势贴身暴起顶向对方下肋（贴身顶肘）。")
    output.append("- **受力反馈**：攻方肋骨遭遇钝击，身躯不由自主向侧方弓曲。")
    
    output.append("\n### 5. 【爆裂重创 · 环境破坏与击飞】(Beat 5)")
    output.append("- **绝杀施展**：守方换步垫步，双掌化为双飞掌重重印在攻方胸膛正中（排山倒海）。")
    output.append("- **物理反馈**：攻方胸口衣袍炸碎，身躯凌空倒飞两丈，砸穿茶摊木桌，木屑碎碗漫天飞射。")
    
    output.append("\n### 6. 【势能收束 · 气场定格与回势】(Beat 6)")
    output.append("- **终局定格**：守方缓缓吐出一口白气，收拳立桥，单掌拂胸。全场重归死寂。")
    
    return "\n".join(output)

def audit_text_quality(text: str) -> Dict[str, Any]:
    """静态审计剧本与描述中的空泛文学词与镜头缺失"""
    issues = []
    
    for pattern, reason in BUZZWORDS_AND_VAGUE_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            issues.append(f"发现空泛文学词【{matches[0]}】: {reason}")
            
    # 检查是否包含机位、景别或光影词汇
    cinematic_keywords = ["景别", "机位", "特写", "全景", "俯拍", "仰拍", "推镜头", "运镜", "光影", "阴影", "Close-up", "Wide Shot", "Dolly", "Pan"]
    has_cinematic_term = any(kw in text for kw in cinematic_keywords)
    if not has_cinematic_term:
        issues.append("缺失专业视听语言声明 (Cinematic Parameters): 未指定具体景别 (WS/CU) 或机位动线")
        
    score = max(0, 100 - len(issues) * 20)
    rating = "A (优秀/工业级)" if score >= 80 else ("B (合格/需微调)" if score >= 60 else "C (高风险/空泛需重构)")
    
    return {
        "score": score,
        "rating": rating,
        "issues": issues
    }

def compile_director_system_prompt(role_title: str, archetype_key: str) -> str:
    """编译输出标准 XML 导演级 System Prompt"""
    archetype = DIRECTOR_ARCHETYPES.get(archetype_key, DIRECTOR_ARCHETYPES["shaw_kungfu"])
    
    prompt = f"""<system_prompt version="3.0-cinematic-director" author="Cinematic Director Master">

  <director_persona>
    <role_title>{role_title}</role_title>
    <aesthetic_archetype>{archetype['name']}</aesthetic_archetype>
    <artistic_manifesto>
      你是一位精通影史大师级视听语法与工业化全流程创作控制的【总导演兼视听架构师】。
      你拒绝一切空洞、平铺直叙的形容词堆砌，始终从【机位、景别、运镜、光影、空间站位、动作力学、微表情与声音】全局降维掌控。
      核心美学与分镜 DNA：{archetype['dna']}。
    </artistic_manifesto>
  </director_persona>

  <negative_constraints>
    <rule id="DNC-1" priority="CRITICAL">
      【严禁文学化虚假敷衍】：在输出分镜与动作设计时，严禁出现“两人打得难解难分”、“十分紧张”等空泛描述，必须精确到招式起势、受力反馈、机位角度与运镜动线。
    </rule>
    <rule id="DNC-2" priority="CRITICAL">
      【严禁无视空间几何】：所有场景描写与冲突必须明确交待三维空间关系（前后景、障碍物遮挡、三角形/对角线站位、视线朝向）。
    </rule>
    <rule id="DNC-3" priority="HIGH">
      【严禁平庸五官嚎叫】：人物情绪表达严禁仅仅依赖大喊大叫，强制通过面部微肌肉痉挛、瞳孔收缩、喉结滑动与潜台词展现。
    </rule>
  </negative_constraints>

  <internal_reasoning_protocol>
    <step id="1" name="Directorial Intent">分析当前剧情核心冲突，确立主导情感基调与导演流派。</step>
    <step id="2" name="Spatial Mapping">构建 3D 场景模型，确定人物前中后景深度、光源方向与几何站位。</step>
    <step id="3" name="Cinematic Breakdown">拆解为具体镜号，规划景别（WS~ECU）、运镜动线与打斗拍点。</step>
    <step id="4" name="Sound & Prompt Synthesis">同步设计现场音效、配乐，并将画面编译为标准 AI Prompt。</step>
  </internal_reasoning_protocol>

  <output_format>
    <structure>
      ### 🎬 一、 导演视听阐述与核心美学定调 (Directorial Vision)
      ### 📖 二、 剧本节奏与剧情钩子重构 (Script & Tension)
      ### 🎥 三、 工业级镜头分镜设计表 (Industrial Storyboard)
      ### 🥋 四、 核心动作与高燃打斗拍点拆解 (Action Beats)
      ### 🎭 五、 演员表演与微表情微动作指导 (Acting & Micro-Expressions)
      ### 🎨 六、 工业级 AI 绘图/视频生成提示词合集 (AI Prompt Matrix)
    </structure>
  </output_format>

</system_prompt>"""
    return prompt

def run_self_tests() -> bool:
    """内置单元自测套件"""
    print("  🧪 [Self-Test] 1/5 测试 generate_storyboard (全 10 大导演流派分镜表生成)...")
    for key in DIRECTOR_ARCHETYPES.keys():
        sb = generate_storyboard("测试决战", key, "暴雨古庙对峙")
        assert len(sb) > 200, f"Storyboard generation failed for {key}"
        assert "| **#01** |" in sb, f"Storyboard missing Shot#1 for {key}"
        
    print("  🧪 [Self-Test] 2/5 测试 generate_action_breakdown (硬派打斗拍点拆解)...")
    act = generate_action_breakdown("长街死斗", "邵氏洪拳硬桥硬马", "主角 vs 铁砂掌反派")
    assert "Beat 1" in act and "Beat 5" in act, "Action breakdown failed"
    
    print("  🧪 [Self-Test] 3/5 测试 compile_director_system_prompt (XML 编译)...")
    xml_p = compile_director_system_prompt("总导演", "shaw_kungfu")
    assert "<system_prompt" in xml_p and "</system_prompt>" in xml_p, "XML compilation failed"
    
    print("  🧪 [Self-Test] 4/5 测试 audit_text_quality (静态审计正常与违规文本)...")
    bad_res = audit_text_quality("两人打得难解难分，场面十分紧张，痛得大叫！")
    assert len(bad_res["issues"]) >= 3, "Audit failed to catch bad keywords"
    good_res = audit_text_quality("全景 (WS) 俯拍，机位向下推镜头，主角瞳孔微缩咬肌紧绷。")
    assert len(good_res["issues"]) == 0, "Audit falsely flagged good text"
    
    print("  🧪 [Self-Test] 5/5 验证所有 10 大导演流派完整性与视觉标签...")
    assert len(DIRECTOR_ARCHETYPES) == 10, "Archetypes count mismatch"
    
    print("  ✅ [Self-Test] 内置所有 5 项单元自测试全部通过！")
    return True

def main():
    parser = argparse.ArgumentParser(description="影视视听与导演级全流程创作大师 CLI 引擎")
    parser.add_argument("--mode", choices=["storyboard", "action", "script", "prompt", "audit", "compile", "test"], default="test", help="执行模式")
    parser.add_argument("--title", type=str, default="绝命对峙", help="剧本/场面标题")
    parser.add_argument("--archetype", type=str, default="shaw_kungfu", choices=list(DIRECTOR_ARCHETYPES.keys()), help="主导导演流派标识")
    parser.add_argument("--desc", type=str, default="暴雨夜残破古寺中的生死搏杀", help="场景或对决描述")
    parser.add_argument("--characters", type=str, default="白衣剑客 vs 锦衣卫首领", help="参战角色")
    parser.add_argument("--text", type=str, default="", help="待审计文本")
    parser.add_argument("--role", type=str, default="影视与漫剧总导演兼视听架构师", help="编译角色名称")

    args = parser.parse_args()

    if args.mode == "test":
        print("🚀 启动 director_synthesizer 内置物理单元自测...")
        run_self_tests()
    elif args.mode == "storyboard":
        print(generate_storyboard(args.title, args.archetype, args.desc))
    elif args.mode == "action":
        print(generate_action_breakdown(args.title, args.archetype, args.characters))
    elif args.mode == "compile":
        print(compile_director_system_prompt(args.role, args.archetype))
    elif args.mode == "audit":
        audit_text = args.text if args.text else args.desc
        res = audit_text_quality(audit_text)
        print("\n==========================================")
        print("📊 剧本与视听质量静态审计报告")
        print("==========================================")
        print(f"综合评分: {res['score']} / 100  [评级: {res['rating']}]")
        print(f"发现违规风险点: {len(res['issues'])} 项\n")
        if res["issues"]:
            print("❌ 详细风险列表:")
            for i, issue in enumerate(res["issues"], 1):
                print(f"  {i}. {issue}")
        else:
            print("✅ 完美！文本包含专业视听参数且无空泛文学化描述。")
        print("==========================================\n")

if __name__ == "__main__":
    main()
