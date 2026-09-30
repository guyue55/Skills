# 角色三视图定妆规格卡与固定描述锁模板 (Character Turnaround Spec)

> 本模板用于在剧集开拍前，对主要角色的视觉资产进行工业级“锁死定妆”，生成标准图生图/图生视频基准资产。

---

## 👤 一、角色定妆资产规格卡

```yaml
character_id: "CHAR_HERO_LIN"
character_name: "林风"
age: 20
height_cm: 182
physique: "修长精干、倒三角背阔肌、长期练剑造就的坚实臂膀"

# 50 字不可变固定外貌锁 (Fixed Prompt Anchor)
# 规则：在之后所有逐镜提示词的第 2 段中，逐字复制该段，严禁随意增删
fixed_appearance_prompt: "20-year-old East Asian male swordsman, sharp angular jawline, a subtle faint scar over the right eyebrow, intense deep-set dark pupils, messy tied-up jet-black hair with loose temples strands, wearing a fitted matte black silk tunic with dark gold embroidery and reinforced leather bracers."

# 专属声纹 Voice ID
voice_id: "zh-CN-YunxiNeural-Custom_Hero_01"
```

---

## 🖼️ 二、标准三视图生成提示词 (3-View Turnaround Prompts)

### 1. 正面全身标准站姿 (去头/重点锁定服装与体态)
```
Full body headless turnaround reference sheet, front view, standing upright in neutral pose, wearing fitted matte black silk tunic with dark gold embroidery and reinforced leather bracers, highly detailed textile weave, realistic fabric folds, clean studio neutral grey background, soft diffused flat lighting, 8k resolution, raw photo quality, zero shadow artifacts.
```

### 2. 背面全身标准站姿 (锁定后背轮廓与发型披挂)
```
Full body turnaround reference sheet, rear back view, showing the back of messy tied-up jet-black hair with flowing strands, rear tailoring of matte black silk robes, dark gold embroidered back pattern, dual leather sheath straps across shoulders, clean studio neutral grey background, soft flat lighting, 8k resolution.
```

### 3. 高清面部无死角特写 (锁定五官、眼神与皮肤微瑕)
```
Extreme close-up portrait of 20-year-old East Asian male, sharp angular jawline, subtle faint white scar over the right eyebrow tail, dark deep obsidian eyes, natural skin pores, fine peach fuzz, faint realistic skin texture, neutral expression with firm closed lips, 85mm lens, f/8 deep focus, neutral flat light, 8k raw photo, zero CGI gloss, zero plastic skin.
```
