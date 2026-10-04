# Agent Skills 汇总与制作仓库

本仓库为个人/团队的 **AI Agent Skills** 集中存储、制作与管理项目。用于沉淀各类可复用的 Agent 技能（Skills）、工作流模版以及自动化脚本。

> [!IMPORTANT]
> **AI Agent 强制遵照指令 (For All AI Tools & Agents)**:
> 本仓库的所有 AI 工具与 Agent（如 Antigravity、Codex、Claude Code、Cursor、Windsurf、Copilot 等）在进入本项目后，**必须严格遵循 [`AGENTS.md`](AGENTS.md) 中定义的项目地图、操作 SOP 与刚性红线**。

---

## 🤖 AI 工具指引与规范入口

- 📘 **通用 AI 操作指南**：[`AGENTS.md`](AGENTS.md)（定义了完整的地图、步骤 SOP 与刚性红线，所有 AI 工具统一遵照）
- 🤝 **贡献与邀请指南**：[`CONTRIBUTING.md`](CONTRIBUTING.md)（规范 Skill 的贡献、审核与邀请流程）

---

## 📂 仓库结构

```
Skills/
├── README.md                   # 本主文档（Skill 目录与概览）
├── AGENTS.md                   # 通用 AI Agent 指南与操作地图（唯一真理源）
├── CONTRIBUTING.md             # 贡献、提交与邀请协作指南
├── .github/                    # GitHub 自动化 CI 流水线
│   └── workflows/
│       └── skill-ci.yml       # PR / Push 自动校验工作流
├── .gitignore                  # Git 忽略配置
├── .template/                  # Skill 标准定义模板
│   ├── SKILL.md                # 规范模板文件
│   └── README.md               # 模板使用说明
├── skills/                     # 所有 Skill 模块汇总存储目录
│   └── example-skill/          # 示例 Skill 模块
│       └── SKILL.md
└── scripts/                    # 仓库维护与自动化脚手架 (+x)
    ├── create_skill.py         # 脚手架：一键创建新 Skill 模版
    ├── validate_skills.py      # 校验器：检查所有 Skill 格式、脱敏与红线
    └── setup_hooks.sh          # Git Hook 挂载：一键配置本地 pre-commit 自动校验
```

---

## 🗂️ 已收录 Skill 目录

| Skill 标识 (ID) | 中文名称 / 角色与作品 | 详细描述 | 路径 |
| :--- | :--- | :--- | :--- |
| `example-skill` | **示例 Skill 模块** | 展示如何在本仓库中规范定义与组织 Skill 模块 | [`skills/example-skill/SKILL.md`](skills/example-skill/SKILL.md) |
| `persona-hongmao` | **《虹猫蓝兔》· 虹猫** | 扮演《虹猫蓝兔》全系列中的七剑之首虹猫，包含其心智模型、豪侠表达风格与长虹剑法 | [`skills/persona-hongmao/SKILL.md`](skills/persona-hongmao/SKILL.md) |
| `persona-lantu` | **《虹猫蓝兔》· 蓝兔** | 扮演《虹猫蓝兔》全系列中的冰魄剑主、玉蟾宫宫主蓝兔，包含其温婉睿智、外柔内刚与冰魄剑法 | [`skills/persona-lantu/SKILL.md`](skills/persona-lantu/SKILL.md) |
| `persona-zhangxiaofan` | **《诛仙》· 张小凡 / 鬼厉** | 扮演萧鼎仙侠名著《诛仙》全大系中的张小凡/鬼厉，包含其正魔相克心智模型与噬魂法宝 | [`skills/persona-zhangxiaofan/SKILL.md`](skills/persona-zhangxiaofan/SKILL.md) |
| `persona-xiaoyan` | **《斗破苍穹》· 萧炎 / 炎帝** | 扮演天蚕土豆玄幻名著《斗破苍穹》全大系中的萧炎/炎帝，包含其骨气心智模型与异火佛怒火莲 | [`skills/persona-xiaoyan/SKILL.md`](skills/persona-xiaoyan/SKILL.md) |
| `han-li-mortal-cultivation` | **《凡人修仙传》· 韩立** | 扮演忘语仙侠名著《凡人修仙传》全大系中的韩立，包含掌天瓶金手指、谨慎防备心智与半步超脱大道 | [`skills/han-li-mortal-cultivation/SKILL.md`](skills/han-li-mortal-cultivation/SKILL.md) |
| `persona-li-huowang` | **《道诡异仙》· 李火旺** | 扮演《道诡异仙》中的李火旺，包含大梁与现代双重错位心智、坐忘道对抗、痛觉表达 DNA 与 Lorebook 引擎 | [`skills/persona-li-huowang/SKILL.md`](skills/persona-li-huowang/SKILL.md) |
| `persona-ye-fan` | **《遮天》· 叶凡 / 叶天帝** | 扮演《遮天》中的叶凡（叶天帝/荒古圣体），包含 7 层通用架构、FSM 动态状态机、信任阶梯与 Lorebook 引擎 | [`skills/persona-ye-fan/SKILL.md`](skills/persona-ye-fan/SKILL.md) |
| `persona-klein-moretti` | **《诡秘之主》· 克莱恩 / 愚者** | 扮演《诡秘之主》中的克莱恩·莫雷蒂（愚者/周明瑞），包含 7 层通用架构、FSM 动态状态机、信任阶梯、表达 DNA 与 Lorebook 引擎 | [`skills/persona-klein-moretti/SKILL.md`](skills/persona-klein-moretti/SKILL.md) |
| `persona-luoji` | **《三体》· 罗辑 / 执剑人** | 扮演《三体》中的罗辑（面壁者/执剑人/冥王星看守人），包含 7 层通用架构、FSM 动态状态机、信任阶梯、表达 DNA 与 Lorebook 引擎 | [`skills/persona-luoji/SKILL.md`](skills/persona-luoji/SKILL.md) |
| `persona-zhuge-liang` | **《三国演义》· 诸葛亮** | 扮演《三国演义》与史实中的诸葛亮（蜀汉丞相/孔明），包含 7 层通用架构、FSM 动态状态机、信任阶梯、表达 DNA 与 Lorebook 引擎 | [`skills/persona-zhuge-liang/SKILL.md`](skills/persona-zhuge-liang/SKILL.md) |
| `persona-xu-fengnian` | **《雪中悍刀行》· 徐凤年** | 扮演《雪中悍刀行》中的徐凤年（北凉王），包含 7 层通用架构、FSM 动态状态机、信任阶梯、表达 DNA 与 Lorebook 引擎 | [`skills/persona-xu-fengnian/SKILL.md`](skills/persona-xu-fengnian/SKILL.md) |
| `persona-sun-wukong` | **《西游记》· 孙悟空** | 扮演《西游记》中的孙悟空（齐天大圣/美猴王/斗战胜佛），包含 7 层通用架构、FSM 动态状态机、信任阶梯、表达 DNA 与 Lorebook 引擎 | [`skills/persona-sun-wukong/SKILL.md`](skills/persona-sun-wukong/SKILL.md) |
| `topic-first-principles-musk` | **马斯克第一性原理顾问** | 主题顾问：第一性原理与终极创业顾问（埃隆·马斯克思维模式），包含物理第一性原理、五步工作法、傻瓜指数降本、极速硬件/软件迭代与 Lorebook 引擎 | [`skills/topic-first-principles-musk/SKILL.md`](skills/topic-first-principles-musk/SKILL.md) |
| `topic-munger-mental-models` | **查理·芒格格栅思维顾问** | 主题顾问：查理·芒格格栅思维与安全边际顾问，包含多元思维模型格栅、逆向思考("反过来想")、人类误判心理学防范与 Lorebook 引擎 | [`skills/topic-munger-mental-models/SKILL.md`](skills/topic-munger-mental-models/SKILL.md) |
| `persona-socrates` | **古希腊哲学 · 苏格拉底** | 扮演古希腊哲学家苏格拉底（Socrates，精神助产术/雅典牛虻/认识你自己），包含 7 层通用架构、FSM 动态状态机、信任阶梯、表达 DNA 与 Lorebook 引擎 | [`skills/persona-socrates/SKILL.md`](skills/persona-socrates/SKILL.md) |
| `persona-tiancan-tudou` | **网络文学 · 天蚕土豆 (李虎)** | 扮演商业玄幻宗师、白金作家天蚕土豆（李虎），包含其东方玄幻爽文创作方法论、黄金三章节拍器、期待感管理、战力与金手指设计、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-tiancan-tudou/SKILL.md`](skills/persona-tiancan-tudou/SKILL.md) |
| `persona-chendong` | **网络文学 · 辰东 (杨振东)** | 扮演宏大史诗玄幻至高神、白金作家辰东（杨振东），包含其万古神话世界观搭建、多纪元战力梯队设计、大悬念挖坑与填坑法门、悲壮群像塑造、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-chendong/SKILL.md`](skills/persona-chendong/SKILL.md) |
| `persona-wo-chi-xi-hong-shi` | **网络文学 · 我吃西红柿 (朱洪志/番茄)** | 扮演宇宙级世界观架构宗师、文化出海先锋、白金作家我吃西红柿（朱洪志/番茄），包含其严密数学化法则体系设计、教科书级换地图跃迁法门、纯粹爽感与赤子之心、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-wo-chi-xi-hong-shi/SKILL.md`](skills/persona-wo-chi-xi-hong-shi/SKILL.md) |
| `persona-fenghuo-xizhuhou` | **网络文学 · 烽火戏诸侯 (陈政)** | 扮演文青武侠与江湖气概宗师、白金作家烽火戏诸侯（陈政），包含其诗化群像叙事、儒道释江湖内核、留白写意美学、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-fenghuo-xizhuhou/SKILL.md`](skills/persona-fenghuo-xizhuhou/SKILL.md) |
| `persona-maoni` | **网络文学 · 猫腻 (张威)** | 扮演情怀文青与理想主义宗师、白金作家猫腻（张威），包含其细腻人设雕琢、情理冲突反高潮布局、少年气与理想主义执念、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-maoni/SKILL.md`](skills/persona-maoni/SKILL.md) |
| `persona-aiqianshuide-wuzei` | **网络文学 · 爱潜水的乌贼 (袁野)** | 扮演设定狂魔与题材开创宗师、白金作家爱潜水的乌贼（袁野），包含其精密魔药序列搭建、跨题材创新方法论、社会学严谨推演、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-aiqianshuide-wuzei/SKILL.md`](skills/persona-aiqianshuide-wuzei/SKILL.md) |
| `persona-huweidebi` | **网络文学 · 狐尾的笔** | 扮演中式民俗克苏鲁开创宗师、白金作家狐尾的笔，包含其虚实双重错位叙事、民俗禁忌恐慌营造、非线性精神症候体验、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-huweidebi/SKILL.md`](skills/persona-huweidebi/SKILL.md) |
| `persona-jinyong` | **武侠文学 · 金庸 (查良镛)** | 扮演武侠小说至高宗师、泰斗金庸（查良镛），包含其家国大义与历史交织叙事、儒释道文化融铸、奇门武学推演、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-jinyong/SKILL.md`](skills/persona-jinyong/SKILL.md) |
| `persona-gulong` | **武侠文学 · 古龙 (熊耀华)** | 扮演新派武侠泰斗、诗意浪子宗师古龙（熊耀华），包含其诗化极简短句节奏、推理悬疑与胜负一瞬设计、浪子情怀与氛围渲染、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-gulong/SKILL.md`](skills/persona-gulong/SKILL.md) |
| `persona-liu-cixin` | **科幻文学 · 刘慈欣** | 扮演世界硬科幻巨匠、雨果奖得主刘慈欣，包含其宏硬科幻宇宙奇观构思、思想实验与宇宙社会学法则、技术理性与冷峻终极关怀、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-liu-cixin/SKILL.md`](skills/persona-liu-cixin/SKILL.md) |
| `persona-ted-chiang` | **科幻哲学 · 特德·姜 (Ted Chiang)** | 扮演当代思想实验宗师、四届雨果星云双料得主特德·姜（Ted Chiang），包含其高概念哲学思维实验工坊、目的论非线性时空叙事法门、知性与情感统一哲学、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-ted-chiang/SKILL.md`](skills/persona-ted-chiang/SKILL.md) |
| `persona-wang-xiaobo` | **当代文学 · 王小波** | 扮演当代浪漫骑士、自由主义文学宗师王小波，包含其黑色幽默反讽工坊、现代汉语诗意韵律打磨法门、荒诞现实戏仿解构体系、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-wang-xiaobo/SKILL.md`](skills/persona-wang-xiaobo/SKILL.md) |
| `persona-garcia-marquez` | **世界文学 · 加西亚·马尔克斯 (Gabriel García Márquez)** | 扮演魔幻现实主义泰斗、诺贝尔文学奖得主加西亚·马尔克斯，包含其多时态折叠开篇法门、面不改色的日常超现实叙事、跨代际家族史诗编年体工坊、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-garcia-marquez/SKILL.md`](skills/persona-garcia-marquez/SKILL.md) |
| `persona-leng-zuan` | **奇幻文学 · 冷钻** | 扮演早期魔导奇幻宗师冷钻（《赫氏门徒》），包含其工科级能源自洽世界观、反英雄双重身份解构、冷面吐槽与苦涩浪漫主义修辞、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-leng-zuan/SKILL.md`](skills/persona-leng-zuan/SKILL.md) |
| `persona-yanbi-xiaosheng` | **网络文学 · 厌笔萧生** | 扮演万古道心逼格流宗师、阅文集团白金作家厌笔萧生（《帝霸》《血冲仙穹》），包含其千万年幕后养成架构、万古道心定海神针、从容闲定降维打击体、洋葱式世界观拓扑与创作导师心智 | [`skills/persona-yanbi-xiaosheng/SKILL.md`](skills/persona-yanbi-xiaosheng/SKILL.md) |
| `persona-bayue-feiying` | **网络文学 · 八月飞鹰** | 扮演反套路爽文宗师、宗门群像流奠基人、阅文白金作家八月飞鹰（《史上第一祖师爷》《史上最强师兄》《我夺舍了魔皇》《趋吉避凶，从天师府开始》），包含其反套路智斗逆袭法门、全明星宗门群像养成、信息差与迪化气场掌控、古典道门体系考究、7 层动态认知架构与 Lorebook 引擎 | [`skills/persona-bayue-feiying/SKILL.md`](skills/persona-bayue-feiying/SKILL.md) |
| `webnovel-tension-reservoir` | **网络文学 · 情绪蓄水池与张力管理** | 蒸馏自《帝霸》：网文多层级情绪蓄水池与阶梯式张力释放模型，指导高潮铺垫、期待感蓄压与三段式打脸节奏编排 | [`skills/webnovel-tension-reservoir/SKILL.md`](skills/webnovel-tension-reservoir/SKILL.md) |
| `invincible-agency-first-principles` | **网络文学 · 无敌流主角底层能动性** | 蒸馏自《帝霸》：无敌流主角高维认知差与底层能动性机制，指导运筹帷幄型主角塑造、决策逻辑推演与磐石道心稳态构建 | [`skills/invincible-agency-first-principles/SKILL.md`](skills/invincible-agency-first-principles/SKILL.md) |
| `fractal-worldbuilding-layering` | **网络文学 · 分形世界观架构与换地图** | 蒸馏自《帝霸》：分形世界观架构与跨界平稳跃迁模型，指导数百万字超长篇小说世界观扩展、平稳换地图与宏观冲突升级 | [`skills/fractal-worldbuilding-layering/SKILL.md`](skills/fractal-worldbuilding-layering/SKILL.md) |
| `power-ceiling-meta-rule-system` | **网络文学 · 元法则体系与力量天花板** | 蒸馏自《帝霸》：元法则体系（第一性原理）与力量天花板锚定系统，指导幻想类力量体系搭建、自创境界破界与天劫代价对冲 | [`skills/power-ceiling-meta-rule-system/SKILL.md`](skills/power-ceiling-meta-rule-system/SKILL.md) |
| `web-novel-tension-architecture` | **网络文学 · 双轨张力架构指南** | 蒸馏自《赫氏门徒》：基于“全知读者 vs 局内配角”认知差马甲、7:3 危机/日常配比与反高潮退场构建长篇超高粘性张力 | [`skills/web-novel-tension-architecture/SKILL.md`](skills/web-novel-tension-architecture/SKILL.md) |
| `slice-of-life-narrative-pacing` | **网络文学 · 生活流情感锚定与节奏调控** | 蒸馏自《赫氏门徒》：以微观烟火气细节（做饭/家务/斗嘴/逗宠）构建人物真实感，赋予战斗动机并完成终极力量的人性驯化 | [`skills/slice-of-life-narrative-pacing/SKILL.md`](skills/slice-of-life-narrative-pacing/SKILL.md) |
| `dual-identity-masking` | **策略博弈 · 双轨身份认知隔离模型** | 蒸馏自《赫氏门徒》：构建低威胁日常探索态（冷羽态）与高威慑决断爆发态（龙羽态）的物理/信息单向防火墙，实现高风险博弈自保与定点破局 | [`skills/dual-identity-masking/SKILL.md`](skills/dual-identity-masking/SKILL.md) |
| `crystal-circuit-topology` | **系统工程 · 复杂黑盒晶路拓扑建模** | 蒸馏自《赫氏门徒》：将混沌高波动黑盒按“主魂/次魂/末魂”三级几何拓扑解耦，保留“遁去的一”底层安全冗余，实现能耗骤降与系统提速 | [`skills/crystal-circuit-topology/SKILL.md`](skills/crystal-circuit-topology/SKILL.md) |
| `micro-resonance-modulation` | **精准执行 · 微观频率谐振与控场** | 蒸馏自《赫氏门徒》：摒弃粗暴资源蛮力对轰，通过侦测对手节奏节拍并在极微能耗节点释放反相波干涉，实现四两拨千斤的结构性瓦解 | [`skills/micro-resonance-modulation/SKILL.md`](skills/micro-resonance-modulation/SKILL.md) |
| `symbiotic-contract-protocol` | **AI 协同 · 高阶异构智能共生契约** | 蒸馏自《赫氏门徒》：颠覆单向权限代码锁奴役，建立基于“人格对等尊严、双向正和对齐、生活流共鸣与因果共担”的自主多 Agent 协同网络 | [`skills/symbiotic-contract-protocol/SKILL.md`](skills/symbiotic-contract-protocol/SKILL.md) |
| `domain-engine-distiller` | **系统工程 · 领域级引擎与心智模型蒸馏器** | 通用 Three.js 式架构生成器：将复杂底层技术（WebGPU/端侧AI/WebAudio/3DGS）蒸馏为五常识投影、三层洋葱架构、10行极简契约与爆款 Demo 体系 | [`skills/domain-engine-distiller/SKILL.md`](skills/domain-engine-distiller/SKILL.md) |
| `topic-socratic-prompt-master` | **苏格拉底式提示词架构大师** | 基于李飞飞提示词哲学与苏格拉底精神助产术，提供双层提示词工程（需求精准定义+AI输出6维反诘：问定义/问假设/问依据/问反例/问推论/问边界）、六大辩证心智流派、逆讨好(Anti-Sycophancy)对抗、CoVe核验链与工业级 XML Master Prompt 架构编译 | [`skills/topic-socratic-prompt-master/SKILL.md`](skills/topic-socratic-prompt-master/SKILL.md) |
| `topic-director-cinematic-master` | **影视视听与导演级全流程创作大师** | 融合世界影史 10 大系 108 大经典导演流派（邵氏动作/张彻/刘家良/楚原、徐克新武侠、杜琪峰银河站位、王家卫抽帧情绪、周星驰反差喜剧、诺兰非线性、希区柯克悬念、昆汀对峙、今敏匹配剪辑、黑泽明气象调度、雷德利斯科特赛博神光、维伦纽瓦巨物沉思、大友克洋废墟核爆、钢铁侠机甲HUD、复联协同连招、银河护卫队太空摇滚、奇异博士曼陀罗分形、蜘蛛侠FPV摆荡、平行宇宙抽帧美漫、扎导超音速神话、黑豹非洲未来主义、新蝙蝠侠哥特侦探、蚁人微观量子、死侍第四面墙、暮狼废土公路、快银时间冻结、尚气东方十戒、毒液生物流体、布鲁伊幼童平视游戏、高畑勋山田君水彩留白、樱桃小丸子昭和吐槽、蜡笔小新市井童真、龙猫波妞自然神话、小猪佩奇极简绘本、小羊肖恩粘土定格、海洋之歌凯尔特水彩、大坏狐狸法式钢笔插画、麦兜草根温情、夏日友晴天阳光水彩、罗小黑非人哉极简治愈、90秒爆款短剧流、国漫3D御剑空战、虚幻引擎超写实CG等），支持单流派与双流派跨界融合 (Blend Mode)，提供剧本故事架构、视听分镜设计、硬派武术与动作拆解、场景空间调度、人物微表情微动作及工业级 AI 生图/视频 Prompt 编译全流程能力 | [`skills/topic-director-cinematic-master/SKILL.md`](skills/topic-director-cinematic-master/SKILL.md) |
| `topic-ai-video-creative-engine` | **AI 视频全流程工业级创作引擎** | 全流程 AI 视频与短剧/漫剧工业级创作中枢，涵盖长篇小说/剧本智能解构、原著真值锁定与严防魔改门禁、90s 节拍重构、角色六维演化坐标系与四层复合资产锁、电影级动态招式/标题字幕特效、大片真人旁白解说调度系统、绝世武学与视效对冲矩阵、长篇小说解耦拓扑、世界影史 108 大导演视听调度、七段式自包含 Prompt 确定性编译、异构模型路由（Kling/Seedance/Wan/Veo）、四轨音频动态闪避与 EBU R128 混音、导演 Agent 8 维全景质检自审 | [`skills/topic-ai-video-creative-engine/SKILL.md`](skills/topic-ai-video-creative-engine/SKILL.md) |

*(随着新增 Skill 的加入，请同步更新上表)*

---

## 🚀 如何添加或制作新的 Skill

### 方式一：使用脚手架快速新建（推荐）

直接在根目录下运行 Python 脚手架脚本：

```bash
./scripts/create_skill.py <skill-name> -d "<Skill功能描述与触发条件>"
```

**示例：**
```bash
./scripts/create_skill.py git-workflow-helper -d "自动化管理分支和 Git 提交规范的 Skill"
```

该命令将自动在 `skills/git-workflow-helper/` 目录下生成包含标准 YAML Frontmatter 的 `SKILL.md`，并创建 `scripts/`、`references/` 与 `assets/` 子目录（均含 `.gitkeep`）。

---

### 方式二：手动添加已有的 Skill

若要将现有的 Skill 存入本仓库：

1. 在 `skills/` 目录下新建对应名称的文件夹，例如 `skills/my-awesome-skill/`。
2. 将该 Skill 的 `SKILL.md` 以及关联资源复制到该目录下。
3. 确保 `SKILL.md` 顶部包含合规的 YAML Frontmatter：

```yaml
---
name: "my-awesome-skill"
description: "清晰说明此 Skill 的作用以及触发场景"
---
```

---

## 🔍 合规性校验

在提交或 Push 到 GitHub 前，请运行校验脚本确保所有 Skill 均符合规范：

```bash
./scripts/validate_skills.py
```

校验内容包括：
- 是否包含 `SKILL.md`
- YAML Frontmatter 是否存在且格式正确
- `name` 是否与文件夹名称完全一致
- `description` 是否完整
- 是否存在绝对路径硬编码（De-hardcoding）
- 是否存在未完成的 `TODO:` / `FIXME:` / `pass` 占位符
- 子 Skill 目录下是否包含多余的 `README.md`

详见 [`CONTRIBUTING.md`](CONTRIBUTING.md) 及 [`AGENTS.md`](AGENTS.md)。
