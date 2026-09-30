# 音频工业级混音、声纹矩阵与声画对齐 (Audio Mixing & Voice Matrix)

> 本文档规范了跨集角色声纹 Voice ID 矩阵、旁白解说档案、四轨分离工程架构、动态闪避 (Sidechain Ducking) 算法、原生音轨冲突治理以及 EBU R128 工业级响度归一化标准。

---

## 🎙️ 一、跨集角色声纹 Voice ID 矩阵绑定 (Voice ID Matrix)

在短剧/漫剧长篇制作中，声音一致性与视觉一致性同等重要。必须为每位登场角色建立不可变的声纹档案：

```json
{
  "project_id": "Drama_S01",
  "voice_matrix": {
    "Hero_LengYu": {
      "name": "冷羽",
      "voice_id": "zh-CN-YunxiNeural-Custom_Hero_01",
      "timbre": "17岁青年沉稳、磁性、中低音、隐忍冷冽、语速 90 字/分",
      "pitch_shift": "-1st",
      "reverb_profile": "medium_hall_damped"
    },
    "Commander_Mekael": {
      "name": "梅凯尔",
      "voice_id": "zh-CN-YunyangNeural-Custom_Commander_04",
      "timbre": "38岁成熟统帅、金石交鸣、威严政客质感、语速 95 字/分",
      "pitch_shift": "-3st",
      "reverb_profile": "stone_cathedral_clear"
    },
    "Veteran_Rote": {
      "name": "罗特",
      "voice_id": "zh-CN-YunhaoNeural-Custom_Veteran_08",
      "timbre": "34岁老油条军官、沙哑烟嗓、玩世不恭低音、语速 88 字/分",
      "pitch_shift": "-4st",
      "reverb_profile": "bar_room_dry"
    }
  }
}
```

---

## 🎚️ 二、四轨分离混音工业架构 (4-Stem Audio Architecture)

任何成片严禁将所有声音粗暴混入单轨，必须建立独立的四轨工程：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          四轨分离工业混音标准                               │
├─────────┬──────────────────────┬─────────────┬──────────────────────────────┤
│ 轨道 ID │ 轨道名称             │ 目标响度    │ 混音职责与声场定位           │
├─────────┼──────────────────────┼─────────────┼──────────────────────────────┤
│ A1      │ 主对白轨 (Dialogue)  │ -12.0 LUFS  │ 主体角色对白/呼吸，中置居中  │
│         │                      │ (最高优先级)│ 高频 3-5kHz 清晰度提升，去喷音│
├─────────┼──────────────────────┼─────────────┼──────────────────────────────┤
│ A2      │ 真人旁白轨 (Narrate) │ -14.0 LUFS  │ 史诗解说/内心OS，立体声微扩展│
│         │                      │ (高优先级)  │ 低切 80Hz，营造大片叙事纵深  │
├─────────┼──────────────────────┼─────────────┼──────────────────────────────┤
│ A3      │ 配乐轨 (BGM/Music)   │ -18.0 LUFS  │ 情绪渲染，受 A1/A2 侧链闪避  │
│         │                      │ (基准未压制)│ 触发时自动下压 -10dB ~ -12dB │
├─────────┼──────────────────────┼─────────────┼──────────────────────────────┤
│ A4      │ 音效轨 (Foley & SFX) │ -14.0 LUFS  │ 刀剑劈砍、法术爆炸、脚步环境音│
│         │                      │ (瞬态峰值)  │ 精准对齐视频物理接触帧 (±0.05s│
└─────────┴──────────────────────┴─────────────┴──────────────────────────────┘
```

---

## 📉 三、动态闪避 (Sidechain Compression / Ducking) 算法

为防止 BGM 掩盖关键台词或旁白解说，必须在 A1/A2 与 A3（配乐）之间建立硬件级/软件级侧链压缩：

```
【侧链动态闪避核心参数】
 • 触发门限 (Threshold)   : -28.0 dB (只要有人声对白或旁白出现即刻触发)
 • 压制深度 (Ducking Depth): -10.0 dB 至 -12.0 dB (BGM 整体音量瞬间下压)
 • 启动时间 (Attack Time) : 20 ms 至 40 ms (极速压制，杜绝吞字首音)
 • 释放时间 (Release Time): 300 ms 至 450 ms (说话结束后平滑平稳回升，严禁抽吸感)
 • 保持时间 (Hold Time)   : 150 ms (防止台词中途短暂换气导致的音量跳动)
```

---

## 🔇 四、视频模型原生音轨冲突治理 (-18dB 策略)

主流视频模型（如 Kling 3.0 / Seedance 2.5 / Hailuo）常自带 AI 生成的背景白噪声或低质合成音。
*   **治理铁律**：
    1.  当 A1 或 A2 轨道存在专业制作的音频时，**视频模型原生音频必须全局衰减 -18dB 至 -24dB**，或仅提取其中的微量高频环境声作为 A4 次级底噪。
    2.  若模型直出音频包含不可剥离的失真人声，**强制执行静音 (`-an`)**，完全以纯净四轨工程重新渲染。

---

## 🎛️ 五、EBU R128 工业级响度归一化标准

全片输出前必须通过 ffmpeg 双遍（Two-Pass）EBU R128 扫描，锁定全平台标准化响度：

```bash
# 工业级双遍 EBU R128 响度归一化标准命令
ffmpeg -i input_master.mp4 -af loudnorm=I=-16:TP=-1.0:LRA=11:measured_I=-20.5:measured_TP=-0.5:measured_LRA=9.2:measured_thresh=-31.0:offset=0.5:linear=true:print_format=summary -c:v copy -c:a aac -b:a 320k output_broadcast_master.mp4
```

*   **标准参数约束**：
    *   **整合响度 (Integrated Loudness)**：`-16.0 LUFS`（允许误差 ±0.5 LUFS）。
    *   **真峰值 (True Peak)**：`≤ -1.0 dBTP`（严格杜绝数字削波失真）。
    *   **响度范围 (Loudness Range)**：`LRA ≤ 11.0 LU`（适应移动端竖屏与耳机收听）。
