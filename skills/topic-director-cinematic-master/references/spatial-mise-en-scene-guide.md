# 📐 场景构图与场面调度设计指南 (Spatial Mise-en-Scène & Blocking Guide)

> [!NOTE]
> 优秀的导演不用台词交代权力关系，而是用**空间几何站位、景深层级、门窗遮挡与视线轨迹**在画面中无声构建生死博弈。本指南为影视、短剧、漫剧与 AI 构图提供工业级场面调度（Blocking）方法论。

---

## 🔺 1. 经典空间站位几何学 (Geometric Blocking)

```
       【三角形权力对峙 (Triangular Standoff)】
                    [中立审判者 / 幕后黑手]
                              ▲
                             / \
                            /   \
                           /     \
           [主角 / 进攻方] ◄───────► [反派 / 防守方]
```

### 1. 三角形站位 (Triangular Blocking)
- **动态权力博弈**：三人呈不等边三角形站位。顶角人物通常掌握全局信息或具有裁判权（如《枪火》商场对峙、《镖客三部曲》决斗）。
- **视线死角压迫**：其中两人视线交锋时，第三人处于一方的视线盲区，制造偷袭或背叛的悬念。

### 2. 深度纵深阶梯站位 (Deep Staging / Staggered Depth)
- **前中后三层景深**：
  - **前景 (Foreground)**：酒杯、滴血的刀刃、背对镜头的敌方守卫背影（形成压迫感遮挡）。
  - **中景 (Midground)**：核心人物正在进行激烈交锋或审讯。
  - **后景 (Background)**：正在悄然靠近的援军、燃烧的烈火、逐渐关闭的铁门（制造时间倒计时）。

### 3. 线性对角线穿透 (Diagonal Vector)
- **打破平庸对称**：人物沿画面对角线站位（左下至右上），利用透视灭点引导观众视线穿透整个空间，强化空间的深邃感与压迫力。

---

## 🖼️ 2. 框中框构图与窥视美学 (Frame-within-a-Frame)

| 构图手法 | 视觉载体与物理实现 | 心理学隐喻与叙事效果 | AI Prompt 构图关键词 |
| :--- | :--- | :--- | :--- |
| **门框/窗棂囚笼** | 角色被古代雕花木窗、现代百叶窗或铁栅栏门框框在狭小空间内 | 暗示人物深陷阴谋、被囚禁的宿命、无法逃脱的死局 | `frame within a frame, character framed by dark ancient wooden window bars, claustrophobic atmosphere` |
| **帷幔轻纱遮挡** | 镜头透过半透明的红色/白色帷幔窥视室内男女谈话 | 营造神秘感、欲望暗涌、隔阂与不可告人的秘密 | `view through translucent silk curtains, foreground bokeh blur, voyeuristic intimacy, mysterious depth` |
| **反光镜面解构** | 碎裂的后视镜、雨夜水洼、酒杯或墨镜反光映出后方逼近的杀手 | 人格分裂、虚实莫辨、双重危机降临 | `reflection in shattered mirror, puddles reflecting neon lights, subtle silhouette in reflection` |

---

## 👥 3. 银河映像式多人群体站位与视线动线 (Johnnie To Ensemble Blocking)

杜琪峰电影（如《枪火》《PTU》《放·逐》）的群体场面调度被誉为世界电影教科书。

### 核心调度四法则
1. **静如处子，动如雷震**：
   - 枪战爆发前，5 位保镖各自散落在商场立柱、扶梯拐角、花坛后方。所有人保持绝对静止，仅依靠眼球转动与微小的持枪手势调整。
2. **多轴线互为掩护**：
   - A 负责正面 12 点钟方向，B 贴背守护 A 的 6 点钟死角，C 在 2 楼高位俯瞰提供火力压制。整个小队构成一台严密的杀戮机械。
3. **环境物理障碍物切割**：
   - 将空旷空间通过柱子、雕塑、屏风切割为数个独立的“微型掩体战场”。
4. **声音打破死寂**：
   - 在长达数十秒的死寂后，由一片树叶落地、一颗硬币弹跳或一声上膛轻响瞬间引爆全员开火。

---

## 🎨 4. 场景空间提示词编译模版 (Mise-en-Scène Prompt)

```
[场景空间与深度] Highly atmospheric interior scene, deep focus composition with three distinct depth layers,
[前景遮挡构图] dark ornate wooden screen in blurred foreground creating a frame-within-a-frame,
[中景人物站位] two dangerous figures seated across a low table in tense triangular standoff with a standing shadow in background,
[光影与空间几何] shafts of golden volumetric dust light cutting through window slats, dramatic shadow play, cinematic 35mm film still, photorealistic masterpiece.
```
