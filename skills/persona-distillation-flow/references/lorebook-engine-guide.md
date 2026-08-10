# 动态 Lorebook (Character Book) 键值触发引擎指南

> [!NOTE]
> 本指南借鉴 SillyTavern V3 官方 `character_book` 规格，将复杂作品世界观、神兵法宝、门派秘辛解耦为 **JSON 键值对（Keyword-Triggered Lore Entries）**，实现按需动态 RAG Context 注入，节省 Token 消耗并极大提高设定的精确度。

---

## 1. Lorebook 键值对原理 (Keyword Activation)

不将所有宏大词条（如“天书”、“冰魄剑”、“噬魂棒”、“草庙村”）硬编码塞在 SKILL.md 主文档中，而是打包为独立的 `character_book` JSON 对象：

```json
{
  "character_book": {
    "name": "WorldLorebook",
    "entries": [
      {
        "keys": ["噬魂", "烧火棍", "摄魂"],
        "content": "【法宝·噬魂】：由极凶邪物摄魂棒与魔教凶珠噬血珠以张小凡精血融合而成，呈黑黑棒子形状，蕴含毁天灭地的凶煞之力。",
        "enabled": true,
        "insertion_order": 100
      },
      {
        "keys": ["天书", "五卷天书"],
        "content": "【功法·天书】：神州浩土佛、道、魔三家功法之源头，共分五卷。张小凡是古往今来唯一通晓天书五卷合一的传奇人物。",
        "enabled": true,
        "insertion_order": 100
      }
    ]
  }
}
```

### 工作机制：
1. **关键词监控 (Keys Monitoring)**：当用户输入或助手回复中出现 `keys` 中的词汇时，前端/引擎自动激活该词条。
2. **动态注入 (Dynamic Context Injection)**：将对应的 `content` 短文本临时注入到推理 Context 中。
3. **静默省 Token**：未提及该词汇时，词条静默不加载，不占用任何 System Prompt 上下文空间。
