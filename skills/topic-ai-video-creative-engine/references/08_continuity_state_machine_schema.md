# 跨集实体状态机规范与资产字典 (Continuity State Machine & Schema)

> 本文档规范了短剧/漫剧百集量产中的实体状态机数据模型、跨集连续性追踪机制、场景破坏累积记忆以及道具流转防丢失算法。

---

## 🗄️ 一、实体状态机全局 JSON Schema 规范

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "DramaContinuityStateMachine",
  "type": "object",
  "required": ["project_id", "current_episode", "character_states", "scene_states", "prop_registry"],
  "properties": {
    "project_id": { "type": "string" },
    "current_episode": { "type": "string", "pattern": "^EP_[0-9]{3}$" },
    "character_states": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["name", "costume_version", "battle_damage", "equipped_props", "realm_stage"],
        "properties": {
          "name": { "type": "string" },
          "costume_version": { "type": "string", "description": "如: 宗门锦袍_v1 / 战损残破黑袍_v2" },
          "battle_damage": {
            "type": "array",
            "items": { "type": "string" },
            "description": "如: ['左眼角带血痕', '右臂衣袖撕裂露出青铜绷带']"
          },
          "equipped_props": {
            "type": "array",
            "items": { "type": "string" },
            "description": "当前随身持有的道具 ID 列表"
          },
          "realm_stage": { "type": "string", "description": "如: 金丹境初期 (附带微弱青光光环)" }
        }
      }
    },
    "scene_states": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["scene_name", "damage_history", "current_lighting"],
        "properties": {
          "scene_name": { "type": "string" },
          "damage_history": {
            "type": "array",
            "items": { "type": "string" },
            "description": "已发生的物理破坏，后集必须保留。如: ['正殿中央大理石地面存在3米深坑', '左侧盘龙柱坍塌断裂']"
          },
          "current_lighting": { "type": "string", "description": "如: 暴雨夜残月 + 闪电穿透破损屋顶" }
        }
      }
    },
    "prop_registry": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["prop_name", "current_holder", "physical_condition"],
        "properties": {
          "prop_name": { "type": "string" },
          "current_holder": { "type": "string", "description": "当前持有角色 ID 或所处场景位置" },
          "physical_condition": { "type": "string", "description": "如: 剑身有两道裂纹，剑尖微钝" }
        }
      }
    }
  }
}
```

---

## 🔄 二、状态机跨集时序流转与自动化注入算法

在生成第 `N` 集的分镜提示词时，编译器自动执行以下注入逻辑：

```python
# 状态机注入伪代码示意
def inject_state_into_prompt(shot_definition, global_state):
    """根据当前集状态机，将角色外貌、场景破损与道具状态动态合成入提示词"""
    char_id = shot_definition.character_id
    scene_id = shot_definition.scene_id
    
    char_state = global_state["character_states"][char_id]
    scene_state = global_state["scene_states"][scene_id]
    
    # 动态组装服装与战损
    costume_prompt = f"{char_state['costume_version']}, {', '.join(char_state['battle_damage'])}"
    
    # 动态组装场景破损记忆
    damage_prompt = f"场景状态: {scene_state['current_lighting']}, 环境中保留破坏痕迹: {'; '.join(scene_state['damage_history'])}"
    
    # 合成至第 2 段与第 3 段
    shot_definition.segment_2_character += f", {costume_prompt}"
    shot_definition.segment_3_scene += f", {damage_prompt}"
    
    return shot_definition.compile()
```

---

## 🛡️ 三、资产三大防崩坏红线

1.  **角色服装版本锁定**：在同一大事件弧（如一场持续 3 集的决战）中，角色服装版本必须绝对恒定，除非有明确剧情中弹/被撕裂并记录入状态机。
2.  **道具流转单持原则**：全局唯一的神兵利器（如“玄天斩灵剑”），在同一时刻其 `current_holder` 只能指向单一实体，严禁同时在两人手中出现。
3.  **场景不可逆破坏机制**：被炸毁的大门、被斩断的树木，在后续所有镜头中必须保持残损状态，严禁出现“下一个特写镜头大门自动完好无损”的严重穿帮。
