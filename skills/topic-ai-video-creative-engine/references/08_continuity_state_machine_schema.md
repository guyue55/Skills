# 跨集实体状态机规范与资产字典 (Continuity State Machine & Schema)

> 本文档规范了短剧/漫剧百集量产中的实体状态机数据模型、跨集连续性追踪机制、六维角色演化变量、场景破坏累积记忆以及道具流转防丢失算法。

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
        "required": [
          "name",
          "biological_age_tier",
          "class_evolution_stage",
          "costume_version",
          "battle_damage",
          "power_manifestation_tier",
          "corruption_level",
          "permanent_scars",
          "equipped_props"
        ],
        "properties": {
          "name": { "type": "string" },
          "biological_age_tier": {
            "type": "string",
            "description": "生理年龄段与外貌骨相，如: 32-35_weathered_veteran / 17_youth / 38_ancient_400yo"
          },
          "class_evolution_stage": {
            "type": "string",
            "description": "当前社会身份阶段，如: 赫氏学院贫困生 / 银龙骑士团统帅 / 联盟霸主"
          },
          "costume_version": { "type": "string", "description": "如: 粗布学员制服_v1 / 烫金龙骑战袍_v2" },
          "battle_damage": {
            "type": "array",
            "items": { "type": "string" },
            "description": "当前集可自愈/需延续战损，如: ['右颊浅浅血痕', '左侧护肩破损裂纹']"
          },
          "power_manifestation_tier": {
            "type": "string",
            "description": "当前修为光华异象，如: 微波透明场_初阶 / 极寒黑夜寒焰_魔化全开"
          },
          "corruption_level": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "心智黑化/魔化程度，0.0为纯善，1.0为完全暴走嗜血"
          },
          "permanent_scars": {
            "type": "array",
            "items": { "type": "string" },
            "description": "终生不可逆生理印记与信物，如: ['盲目淡紫双眸', '眉尾细微剑痕', '银鹰吊坠']"
          },
          "equipped_props": {
            "type": "array",
            "items": { "type": "string" },
            "description": "当前随身持有的道具/神兵 ID 列表"
          }
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

在生成第 N 集的分镜提示词时，编译器自动执行以下注入逻辑：

```python
# 状态机注入逻辑示例
def inject_state_into_prompt(shot_definition, global_state):
    # 根据当前集状态机，将角色外貌、演化层、场景破损与道具状态动态合成入提示词
    char_id = shot_definition.character_id
    scene_id = shot_definition.scene_id
    
    char_state = global_state["character_states"][char_id]
    scene_state = global_state["scene_states"][scene_id]
    
    # 动态组装四层复合角色锁
    four_layer_anchor = (
        f"{char_state['name']}, {char_state['biological_age_tier']}, "
        f"{char_state['class_evolution_stage']} ({char_state['costume_version']}), "
        f"{char_state['power_manifestation_tier']} (魔化度: {char_state['corruption_level']:.1f}), "
        f"永久特征: {', '.join(char_state['permanent_scars'])}, "
        f"战损: {', '.join(char_state['battle_damage'])}"
    )
    
    # 动态组装场景破损记忆
    damage_prompt = f"场景状态: {scene_state['current_lighting']}, 环境中保留破坏痕迹: {'; '.join(scene_state['damage_history'])}"
    
    # 合成至第 2 段与第 3 段
    shot_definition.segment_2_character = four_layer_anchor
    shot_definition.segment_3_scene += f", {damage_prompt}"
    
    return shot_definition.compile()
```

---

## 🛡️ 三、资产三大防崩坏红线

1.  **生理年龄与骨相恒定锁**：无论集数如何演进，角色当前的生理年龄段、须发衰老特征必须严格受控，杜绝任何将成熟统帅/老油条生成为少年偶像的视觉幼态化漂移。
2.  **道具流转单持原则**：全局唯一的神兵利器（如“生锈铁剑”），在同一时刻其 `current_holder` 只能指向单一实体，严禁同时在两人手中出现。
3.  **场景不可逆破坏机制**：被炸毁的大门、被斩断的石柱，在后续所有镜头中必须保持残损状态，严禁出现“下一个特写镜头石柱自动完好无损”的严重穿帮。
