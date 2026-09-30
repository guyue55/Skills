# 百万字小说影视化全资产解耦拓扑与引用规范 (Large-Scale Adaptation Topology)

> **工业定位**：面向 200 万字以上长篇巨著、百集以上短剧/漫剧工业化生产的**资产解耦、跨文件标准化引用、状态继承与环境脱敏**工程架构。  
> **设计哲学**：拒绝单文档臃肿与重复定义；以高内聚、低耦合的模块化矩阵支撑数百集剧本与海量视觉生成。

---

## 🗺️ 一、 五大核心解耦库目录标准拓扑

```
<project-root>/
├── 00_MASTER_INDEX.md                      # [总控] 全剧集与资产快速索引目录
├── 01_WORLD_AND_POWER_SYSTEM.md            # [设定] 宏观世界观、战力法则与美学混血底座
├── AGENTS.md                               # [手册] AI Agent 创作守则与提示词编译规范
├── README.md                               # [概览] 生产工程导航与资产统计说明
│
├── 01_CHARACTERS/                          # 核心角色规格书库 (CHAR_001 ~ CHAR_NNN)
│   ├── CHARACTERS_INDEX.md                 # 角色总索引 (多形态/年龄段/状态机映射)
│   └── CHAR_001_LENG_YU.md                # 单角色规格书 (四层复合锁/FACS/Voice)
│
├── 02_SCENES/                              # 核心场景规格书库 (SCENE_001 ~ SCENE_NNN)
│   ├── SCENES_INDEX.md                     # 场景总索引 (光学/色温/地标/破坏历史)
│   └── SCENE_001_ACADEMY_HALL.md          # 单场景规格书 (全景/中景/微距/材质)
│
├── 03_PROPS_AND_ASSETS/                    # 核心道具/神兵规格书库 (PROP_001 ~ PROP_NNN)
│   ├── PROPS_INDEX.md                      # 道具总索引 (材质/物理/信物持有者)
│   └── PROP_001_RUSTY_SWORD.md            # 单道具规格书 (微观表面/动态光效)
│
├── 03_MARTIAL_ARTS_AND_VFX/                # 绝世武学与视效矩阵 (SKILL_001 ~ VFX_NNN)
│   ├── MARTIAL_ARTS_INDEX.md               # 武学与视效总索引 (出场/对战/旁白矩阵)
│   ├── SKILL_001_LUOYU.md                  # 单武学演练与对战规格书 (含动态字幕/旁白)
│   └── VFX_001_CRYSTAL_CIRCUITS.md        # 视效物理力学规范文档
│
├── 04_EPISODES/                            # 分卷分集短剧剧本文档 (VOL_01 ~ VOL_NN)
│   ├── EPISODES_INDEX.md                   # 300+ 集总目录索引
│   └── VOL_01/                             # 单卷目录 (EP_001.md ~ EP_008.md)
│       └── EP_001_入学风波.md               # 仅通过相对链接引用上述资产，轻量高效
│
└── 05_METADATA/                            # 全工程机器元数据图谱
    └── manifest_full.json
```

---

## 🔗 二、 跨文件解耦引用标准与去硬编码铁律

1.  **单集剧本极简引用原则**：
    分集剧本（`04_EPISODES/VOL_XX/EP_YYY.md`）严禁重复粘贴角色的完整 50 字外貌描述或场景说明，必须使用标准化 Markdown 相对链接引用：
    ```markdown
    * 主演：[冷羽 (CHAR_001)](../../01_CHARACTERS/CHAR_001_LENG_YU_冷羽.md)
    * 场景：[赫氏学院正门 (SCENE_001)](../../02_SCENES/SCENE_001_HESHI_ACADEMY_HALL.md)
    * 使用武学：[落羽神恋曲 (SKILL_001)](../../03_MARTIAL_ARTS_AND_VFX/SKILL_001_LUOYU_SHENLIANQU_落羽神恋曲.md)
    ```
2.  **绝对路径禁绝律 (De-hardcoding Rule)**：
    所有文件内的超链接一律使用相对路径（`../` 或 `./`），严禁硬编码 `/Users/...` 或 `/home/...`。