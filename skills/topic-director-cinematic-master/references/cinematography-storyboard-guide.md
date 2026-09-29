# 🎥 分镜视听与镜头设计工程指南 (Cinematography & Storyboard Guide)

> [!NOTE]
> 本指南确立了导演级分镜视听语言的工业化参数标准。覆盖景别、机位角度、运镜动线、布光色彩与 AI 画面/视频 Prompt 映射规范。

---

## 📐 1. 景别工业化标准体系 (Shot Scale Standard)

| 景别代号 | 中文名称 | 英文术语 | 人体画幅范围 | 核心叙事功能与心理暗示 | AI Prompt 对应关键词 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EWS** | **极远景** | Extreme Wide Shot | 人物呈小点或环境主导 | 交代地理宏观环境、孤独渺小感、战争宏大阵仗 | `extreme wide shot, panoramic landscape, vast environment, epic scale` |
| **WS / LS**| **全景 / 远景** | Wide Shot / Long Shot | 完整呈现人物全身与立足点 | 展现人物与空间关系、群体阵型站位、完整起势动作 | `wide shot, full body view, full length shot, spatial context` |
| **MS** | **中景** | Medium Shot | 膝盖/腰部以上至头部 | 展现人物间常规对话、上半身肢体冲突、招式对拆交锋 | `medium shot, waist up shot, interaction framing` |
| **MCU** | **中近景** | Medium Close-Up | 胸部以上至头部 | 聚焦角色台词表达、情绪微动、兼顾肩颈肢体防守 | `medium close-up, chest up, focused character portrait` |
| **CU** | **特写** | Close-Up | 完整面部或单一部位 | 放大情绪爆发、眼神杀气、关键证物、扳机扣动瞬间 | `close-up shot, detailed facial expression, intense gaze` |
| **ECU** | **极近特写** | Extreme Close-Up | 瞳孔/嘴角/伤口/刀尖 | 极限心理压迫、微表情抽搐、致命细节一击、冷汗滴落 | `extreme close-up, macro shot, pupil dilation, trembling lips, blade tip` |

---

## 🔄 2. 机位角度与视点心理学 (Camera Angles & POV)

```
                    【俯拍/上帝视角 (Bird's-Eye View)】
                            宿命感 / 绝望 / 渺小
                                     │
    【仰拍 (Low Angle)】 ◄────────────┼────────────► 【平视 (Eye Level)】
    威严 / 压迫 / 绝对掌控力                 │              平等 / 客观 / 纪实
                                     │
                    【倾斜荷兰角 (Dutch Angle)】
                            失衡 / 癫狂 / 危机降临
```

1. **平视镜头 (Eye Level)**：
   - 保持客观中立视角，用于常规信息交代与理性博弈。
   - Prompt: `eye-level angle, neutral perspective, realistic viewpoint`.
2. **仰拍视角 (Low Angle)**：
   - 摄影机低于角色视线向上仰望，赋予角色崇高、威严、不可战胜的压迫感与统治力。
   - Prompt: `low angle shot, looking up, imposing presence, monumental stature`.
3. **俯拍与上帝视角 (High Angle / Top-Down Bird's Eye)**：
   - 摄影机自上而下俯视，凸显被摄者的困顿、脆弱、任人宰割或棋局全景。
   - Prompt: `high angle shot, bird's-eye view, top-down perspective, vulnerable subject`.
4. **荷兰角/倾斜构图 (Dutch Angle / Canted Angle)**：
   - 摄影机机身故意倾斜 15°~45°，心理学上打破重力平衡，暗示角色精神崩溃、暗藏危机或现实坍塌。
   - Prompt: `dutch angle shot, canted camera, tilted framing, psychological tension`.
5. **主观视点与过肩镜头 (POV / Over-The-Shoulder - OTS)**：
   - `POV`：观众直接代入角色双眼，体验被追杀、瞄准、窥视的沉浸感。
   - `OTS`：透过一方肩膀对话，建立两人的空间连线与权力压制关系。
   - Prompt: `first-person POV, subjective camera / over-the-shoulder shot, dynamic dialogue framing`.

---

## 🏃 3. 运镜动线与运动速率 (Camera Motion & Velocity)

| 运镜术语 | 中文释义 | 运动物理轨迹 | 影视情绪与叙事效果 | AI 视频控制 Prompt (Sora/Runway/Kling) |
| :--- | :--- | :--- | :--- | :--- |
| **Dolly In** | **推镜头** | 摄影机物理向前平滑推近 | 强化注意力、角色顿悟、危急逼近、情绪内聚 | `slow push-in, dolly zoom forward, tightening focus` |
| **Dolly Out**| **拉镜头** | 摄影机物理向后撤离 | 揭示周围隐藏危险、告别、从微观个体拉向残酷世界 | `dolly out, pull back shot, revealing background context` |
| **Tracking / Follow**| **跟镜头** | 伴随角色移动保持相对运动 | 沉浸式奔跑、巷战追逐、动作打击连贯跟随 | `tracking shot, smooth camera following subject motion` |
| **Pan / Tilt**| **摇镜头** | 机位不动，镜头水平/垂直旋转 | 视线搜寻、上下打量敌人装备、左右环顾对峙阵营 | `smooth camera pan left to right, vertical tilt up` |
| **Whip Pan** | **甩镜头** | 极速瞬间旋转伴随强烈动态模糊 | 瞬间转场、时空突变、注意力被巨响突发吸引 | `whip pan, fast motion blur transition, kinetic cut` |
| **Crane / Boom**| **升降镜头** | 机械臂垂直升起或俯冲落下 | 开场气势磅礴展示、决斗终局升空俯瞰尸横遍野 | `crane shot rising upwards, dramatic boom down` |
| **Handheld Shake**| **手持晃动** | 真实呼吸感微晃或剧烈颠簸 | 战场纪实感、近战肉搏冲击波、主角极度恐慌 | `gritty handheld camera, natural camera jitter, intense vibration` |

---

## 💡 4. 光影布光与色彩情绪盘 (Lighting & Color Temperature)

### 经典布光模式
1. **伦勃朗光 (Rembrandt Lighting)**：
   - 45° 主光在人物背光面脸颊形成标志性的倒三角形光斑。赋予角色深邃、复杂、兼具善恶的戏剧张力。
   - Prompt: `Rembrandt lighting, dramatic triangle cheek highlight, deep chiaroscuro`.
2. **高反差明暗对照法 (Chiaroscuro / Film Noir Lighting)**：
   - 强烈的明暗反差，利用百叶窗、铁栅栏、阴暗巷道投射条纹阴影。
   - Prompt: `film noir lighting, high contrast shadows, venetian blind shadow patterns, hard side light`.
3. **轮廓逆光 (Rim Light / Silhouette)**：
   - 强光源置于角色正后方，勾勒出锋利的金色/冷白发丝与身躯轮廓，正面完全隐没在阴影中。
   - Prompt: `dramatic rim light, backlighting, golden edge light, mysterious silhouette`.

### 色彩情绪盘与调色风格 (Color Grading)
- **邵氏经典暖金武侠色**：`warm golden tone, vintage 1970s Technicolor, saturated vermilion red and amber light`.
- **银河映像冷峻青灰**：`cool cyan and desaturated teal tone, deep shadowy blacks, cold fluorescent glow`.
- **王家卫迷幻红绿霓虹**：`emerald green and crimson red neon glow, moody tungsten warmth, hazy nostalgic atmosphere`.
- **末日废土灰黄高反差**：`bleach bypass, desaturated sepia and dusty yellow tint, high dynamic range`.

---

## 📋 5. 工业级分镜表标准输出模版 (Storyboard Sheet)

在输出具体剧本或短剧分镜设计时，必须严格执行以下五栏契约：

```markdown
| 镜号 | 景别 & 机位 | 运镜动线 | 画面核心视觉 (人物动作 / 构图 / 光影) | 声音设计 (台词 / 音效 / 配乐) | AI 提示词 (Midjourney / Kling) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **#01** | 全景 (WS) · 平视 | 慢速推镜头 (Slow Dolly In) | 暴雨倾盆的古庙门前，黑衣剑客持伞独立，积水倒映闪电冷光 | **[音效]** 惊雷炸响，雨水击打青石板脆响；**[配乐]** 苍凉洞箫起势 | `wide shot, ancient temple entrance, heavy torrential rain, solitary swordsman holding oil-paper umbrella...` |
| **#02** | 极近特写 (ECU) · 仰拍 | 快速下摇 (Quick Tilt Down) | 剑客右手拇指轻推剑格，利刃出鞘三寸，寒光照亮冷冽如冰的右眼 | **[音效]** 龙吟般清脆的金属拔刀声 (Clink!)；**[台词]** 独白：“第七个。” | `extreme close-up, thumb pushing katana sword guard, blade reflecting eye, intense cold gaze...` |
```
