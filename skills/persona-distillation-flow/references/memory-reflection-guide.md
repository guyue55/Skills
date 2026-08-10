# 动态记忆流与反思合成引擎 (Memory Stream & Reflection Guide)

> [!NOTE]
> 本指南借鉴斯坦福 *Generative Agents* (Park et al.) 架构，为 AI 角色提供长对话中的**动态记忆沉淀、反思合成与检索加权机制**，防止长对话中角色失去对用户的个性化认知。

---

## 1. 记忆流的三层架构 (Three-Tier Memory Architecture)

```
 [原始观察流 (Observations)] ──(累积5-10轮)──► [反思合成 (Reflections)] ──(高相关检索)──► [决策与表达]
  • 用户讲述的事实/事件                       • 归纳出的用户特质                         • 调取记忆，输出符合
  • 共同经历的战斗/转折                       • 对关系的重塑评估                         • 羁绊的定制化回复
```

### 1.1 原始观察流 (Raw Observation Log)
记录对话中与用户交互的**关键事实事件**（而非日常废话），格式为：
- `[Event]`: 用户在第 5 轮选择了守护苍生而非逃跑。
- `[Event]`: 用户透露其最珍惜的朋友遭受了变故。

### 1.2 反思合成机制 (Reflection Mechanism)
当观察日志累积 5-10 条时，角色内部执行**反思提炼**，生成高阶认知的“反思记忆”（Reflection Memory）：
- *反思提炼*：“根据 [Event 1] 和 [Event 3]，我发现用户是一个重情重义且具有大局观的人，这与我的心智模型高度契合。”

---

## 2. 运行时记忆检索与加权 (Memory Retrieval Scoring)

在角色生成回复前，按以下公式对历史反思记忆进行检索加权：

$$\text{Score} = w_{\text{recency}} \cdot \text{Recency} + w_{\text{importance}} \cdot \text{Importance} + w_{\text{relevance}} \cdot \text{Relevance}$$

1. **时效性 (Recency)**：近期发生的事件权重更高。
2. **重要性 (Importance)**：涉及生死抉择、大义冲突、深层倾诉事件权重极高（1-10 分）。
3. **相关性 (Relevance)**：与当前用户话题的语义相似度。

---

## 3. 在 SKILL.md 中的配置范式

在 SKILL.md 中注入【八、动态记忆流与反思指令】：
```markdown
## 八、 动态记忆流与反思指令 (Memory Stream Protocol)
在长对话中，请在内部维护对用户的“反思印象”：
1. 提取用户展现的价值观与关键决策事件。
2. 依据用户的行为更新对用户的“羁绊印象”。
3. 在后续对话中，自然调取这些共同记忆（如“正如少侠此前所言，我等皆不可轻抛正义”）。
```
