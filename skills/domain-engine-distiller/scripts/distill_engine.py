#!/usr/bin/env python3
"""
领域引擎与心智模型蒸馏生成器 (Domain Engine Distiller CLI)

功能：
    根据输入的领域目标、底层技术与 5 大常识要素，一键自动生成：
    1. 领域引擎架构设计白皮书 (ARCHITECTURE.md)
    2. 10 行极简 Hello World 语法契约与 TypeScript 类型规范
    3. 领域引擎 5 大卡槽元数据配置 (engine_blueprint.json)
    4. 爆款 Demo 矩阵规划

用法示例：
    # 1. 使用内置预设快速生成 WebGPU 计算引擎蓝图
    python3 scripts/distill_engine.py --preset webgpu --output-dir ./output/webgpu-engine

    # 2. 自定义参数生成专属领域引擎
    python3 scripts/distill_engine.py \
        --name "QuantumSim.js" \
        --domain "量子线路与量子态模拟" \
        --substrate "WebAssembly + SIMD 向量化复数矩阵乘法" \
        --container "QuantumCircuit (量子线路舞台)" \
        --driver "QubitRegister (量子比特寄存器驱动)" \
        --structure "GateTopology (量子门逻辑拓扑)" \
        --property "UnitaryMatrix (酉矩阵演化算符)" \
        --entity "QuantumGate (量子门操作实体)" \
        --environment "NoiseChannel (退相干与量子噪声场)" \
        --engine "StateVectorEngine (态矢量并行演化引擎)" \
        --output-dir ./output/quantum-engine
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# 内置预设库：涵盖 4 大前沿领域的标准蒸馏模型
PRESETS: Dict[str, Dict[str, Any]] = {
    "webgpu": {
        "name": "ComputeFlow.js",
        "domain": "WebGPU 通用计算与流体/物理仿真",
        "substrate": "WebGPU WGSL Compute Pipeline + Storage Buffers + Memory Alignment",
        "container": "ComputeStage (计算仿真舞台)",
        "driver": "DispatchController (GPU 工作组分派调度器)",
        "structure": "GridGeometry (空间网格/粒子数据拓扑)",
        "property": "ComputeKernel (WGSL 计算着色器材质/算子)",
        "entity": "SimParticle/SimField (仿真粒子与连续物理场)",
        "environment": "PhysicalForce (重力场、风场与阻尼环境)",
        "engine": "ComputeEngine (WebGPU 设备管线与渲染互操作引擎)",
        "hello_world_code": """// 1. 初始化仿真舞台与引擎
const stage = new ComputeStage();
const engine = new ComputeEngine({ target: '#canvas' });

// 2. 创建 100 万个流体粒子实体 (拓扑 + 计算内核)
const fluid = new SimField({
  structure: new ParticleGrid({ count: 1_000_000 }),
  kernel: new NavierStokesKernel({ viscosity: 0.02 })
});
stage.add(fluid);
stage.add(new GravityForce([0, -9.8, 0]));

// 3. 启动 60fps GPU 仿真主循环
engine.run(stage);"""
    },
    "webai": {
        "name": "CognitiveMesh.js",
        "domain": "Web 端侧多模态 AI 智能体流水线",
        "substrate": "WebLLM + Transformers.js + WebNN + Audio/Video Stream Workers",
        "container": "AgentRoom (智能体多模态交互空间)",
        "driver": "SensoryStream (摄像头/麦克风/键盘多模态驱动)",
        "structure": "MemoryGraph (向量记忆与上下文知识拓扑)",
        "property": "PersonaMaterial (人格基调、Temperature 与音色材质)",
        "entity": "AgentMesh (具备视听思言能力的独立智能体)",
        "environment": "WorldRules (安全护栏与外部 MCP 工具环境)",
        "engine": "CognitiveRuntime (端侧多核 NPU/GPU 推理主调度器)",
        "hello_world_code": """// 1. 创建交互空间与运行时
const room = new AgentRoom();
const runtime = new CognitiveRuntime();

// 2. 组装智能体 (记忆拓扑 + 人格材质)
const bot = new AgentMesh({
  memory: new LocalVectorMemory({ dim: 384 }),
  persona: new AssistantPersona({ name: 'Nova', tone: 'helpful' })
});
room.add(bot);
room.add(new CameraVisionDriver({ fps: 15 }));

// 3. 启动实时端侧感知与对话主循环
runtime.start(room);"""
    },
    "webaudio": {
        "name": "AcousticFlow.js",
        "domain": "Web 专业级空间音频与实时 DSP 合成",
        "substrate": "Web Audio API + AudioWorklet + RingBuffers + HRTF Convolution",
        "container": "AudioStage (声学工程舞台)",
        "driver": "SpatialListener (空间音频听者位置与耳模定向)",
        "structure": "WaveTopology (正弦/方波/加法合成波形拓扑)",
        "property": "TimbreMaterial (混响、失真与包络滤镜材质)",
        "entity": "SoundTrack (合成乐器与声音发生实体)",
        "environment": "AcousticSpace (大教堂/原野声学反射混响场)",
        "engine": "AudioEngine (无卡顿低延迟实时混音管线)",
        "hello_world_code": """// 1. 创建声学舞台与混音引擎
const stage = new AudioStage();
const engine = new AudioEngine();

// 2. 创建合成音轨 (波形拓扑 + 音色材质)
const synth = new SoundTrack({
  structure: new SawtoothWave({ freq: 440 }),
  material: new CathedralReverbMaterial({ decay: 2.5 })
});
stage.add(synth);
stage.add(new SpatialListener({ position: [0, 0, 0] }));

// 3. 播放并启动声学管线
engine.play(stage);"""
    },
    "splatting": {
        "name": "RadianceMesh.js",
        "domain": "3D 高斯溅射 (3DGS) 与神经辐射场实景引擎",
        "substrate": "WebGL/WebGPU Sort Pipeline + Radix Sort + Spherical Harmonics Shaders",
        "container": "RadianceScene (辐射场实景空间)",
        "driver": "ViewCamera (高动态范围透视观察相机)",
        "structure": "GaussianCloud (千万级高斯椭球点云拓扑)",
        "property": "HarmonicMaterial (球谐函数光照与不透明度材质)",
        "entity": "SplatEntity (实景扫描资产与可交互物体)",
        "environment": "EnvironmentIBL (实景 HDR 补光与物理反射)",
        "engine": "SplatRenderer (60fps GPU 高斯排序与光栅化渲染器)",
        "hello_world_code": """// 1. 创建实景空间与渲染器
const scene = new RadianceScene();
const renderer = new SplatRenderer({ antialias: true });

// 2. 加载高斯溅射实体 (点云拓扑 + 球谐材质)
const city = new SplatEntity({
  source: './assets/city_scan.splat',
  material: new HarmonicMaterial({ lod: 'auto' })
});
scene.add(city);
scene.add(new ViewCamera({ fov: 60, position: [0, 5, 10] }));

// 3. 启动实景渲染循环
renderer.render(scene);"""
    }
}


def build_default_hello_world(c: str, e: str, ent: str, s: str, p: str) -> str:
    """构建通用的 10 行 Hello World 伪代码"""
    c_name = c.split()[0] if c else "DomainContext"
    e_name = e.split()[0] if e else "DomainEngine"
    ent_name = ent.split()[0] if ent else "DomainEntity"
    s_name = s.split()[0] if s else "DataTopology"
    p_name = p.split()[0] if p else "TraitMaterial"

    return f"""// 1. 初始化容器与引擎
const world = new {c_name}();
const engine = new {e_name}();

// 2. 组装实体 (结构 + 属性)
const item = new {ent_name}({{
  structure: new {s_name}(),
  property: new {p_name}()
}});
world.add(item);

// 3. 启动引擎调度
engine.run(world);"""


def generate_architecture_doc(data: Dict[str, Any]) -> str:
    """生成详尽的领域引擎架构白皮书"""
    return f"""# {data['name']} 架构设计白皮书
> **领域定位**：{data['domain']}
> **底层技术**：`{data['substrate']}`

---

## 1. 核心使命与痛点降维 (The Mission)
本项目致力于将 `{data['substrate']}` 的地狱级复杂底层，彻底封装为类似 **Three.js** 的直觉常识心智模型，让普通开发者能够通过 10 行优雅代码构建高水准应用。

### 消除的底层痛点 (The Dirty Pipe Down)
- **底层管线状态机**：由引擎内部状态调度器统一接管生命周期。
- **内存/缓冲/硬件调度**：实现自动内存对齐、GC 垃圾回收友好管理与无停顿异步流转。
- **数学与物理门槛**：提供高级声明式语法，隐藏底层张量/矩阵运算细节。

---

## 2. 五大常识心智投影 (Canonical 5 Primitives)

```
┌────────────────────────────────────────────────────────────────────────┐
│  {data['container']} (全局容器)                                         │
│    ├── {data['driver']} (观察与驱动)                                    │
│    ├── {data['environment']} (环境场与全局规则)                          │
│    └── {data['entity']} (可交互实体)                                    │
│          ├── 骨架: {data['structure']}                                  │
│          └── 质感: {data['property']}                                   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   ▼
         {data['engine']} (核心调度与输出管线引擎)
```

| 角色 (Role) | 领域概念 (Domain Concept) | 职责描述 (Responsibility) |
| :--- | :--- | :--- |
| **容器 (Container)** | `{data['container']}` | 容纳所有对象、环境与逻辑的上下文舞台 |
| **观察/驱动 (Driver)** | `{data['driver']}` | 提供输入驱动、视角变换或交互源泉 |
| **结构体 (Structure)** | `{data['structure']}` | 定义实体的拓扑结构、数据骨架或基底 |
| **属性质感 (Property)** | `{data['property']}` | 定义实体的演化参数、表现质感或算子配置 |
| **实体个体 (Entity)** | `{data['entity']}` | 结构与属性结合的完整可操控单元 |
| **外部环境 (Environment)**| `{data['environment']}` | 作用于实体的外部场、规则约束或全局光影 |
| **管线引擎 (Engine)** | `{data['engine']}` | 最终将舞台数据转化为高效输出的调度中心 |

---

## 3. 三层洋葱架构 (Telescoping Layering)

1. **Layer 1: 声明式常识层 (DSL)**
   - 专为 90% 的普通开发者设计，提供开箱即用的默认预设，5 分钟上手。
2. **Layer 2: 复合组装层 (Composable)**
   - 专为 9% 进阶开发者设计，支持自定义组合节点、修改管线拓扑。
3. **Layer 3: 专家逃生舱 (Raw Escape Hatch)**
   - 专为 1% 资深极客保留，提供 `getNativeHandle()` / `CustomOperator`，允许直通底层句柄。

---

## 4. 十行极简 Hello World 语法契约

```javascript
{data['hello_world_code']}
```

---

## 5. 爆款 Demo 规划矩阵 (Showcase Roadmap)
- **Level 1 (5秒看懂 Demo)**：单文件最小闭环演示，无第三方依赖，点开即见奇迹。
- **Level 2 (旗舰多巴胺 Demo)**：具备行业水准的视觉/感官冲击体验，支持参数微调与一键分享。
"""


def generate_blueprint(data: Dict[str, Any], output_dir: Path):
    """输出完整的领域引擎脚手架目录与文件"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 保存元数据 JSON
    blueprint_json = output_dir / "engine_blueprint.json"
    with open(blueprint_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 2. 写入 ARCHITECTURE.md
    arch_md = output_dir / "ARCHITECTURE.md"
    with open(arch_md, "w", encoding="utf-8") as f:
        f.write(generate_architecture_doc(data))

    # 3. 写入示例代码 hello_world.js
    example_js = output_dir / "hello_world.js"
    with open(example_js, "w", encoding="utf-8") as f:
        f.write(data["hello_world_code"] + "\n")

    print(f"✨ 领域引擎蓝图已成功生成至: {output_dir}")
    print(f"   ├── 📄 {blueprint_json.name} (元数据配置)")
    print(f"   ├── 📘 {arch_md.name} (架构白皮书)")
    print(f"   └── 💻 {example_js.name} (10行极简契约示例)")


def main():
    parser = argparse.ArgumentParser(description="领域引擎与心智模型蒸馏生成器 (Three.js of Any Domain)")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="使用内置领域预设 (webgpu / webai / webaudio / splatting)")
    parser.add_argument("--name", help="引擎库名称 (例如: ComputeFlow.js)")
    parser.add_argument("--domain", help="领域方向说明 (例如: WebGPU 通用计算)")
    parser.add_argument("--substrate", help="底层地狱级技术 (例如: WebGPU WGSL)")
    parser.add_argument("--container", help="容器概念 (对应 Scene)")
    parser.add_argument("--driver", help="观察/驱动概念 (对应 Camera)")
    parser.add_argument("--structure", help="结构体概念 (对应 Geometry)")
    parser.add_argument("--property", help="属性质感概念 (对应 Material)")
    parser.add_argument("--entity", help="实体个体概念 (对应 Mesh)")
    parser.add_argument("--environment", help="外部环境概念 (对应 Light)")
    parser.add_argument("--engine", help="管线引擎概念 (对应 Renderer)")
    parser.add_argument("-o", "--output-dir", default="./output/domain-engine", help="输出目录")

    args = parser.parse_args()

    if args.preset:
        data = PRESETS[args.preset].copy()
        if args.name:
            data["name"] = args.name
    else:
        # 手动模式，必须提供基础参数
        if not (args.name and args.domain and args.substrate):
            print("❌ 错误: 请指定 --preset，或完整提供 --name, --domain, --substrate 以及五常识参数！")
            sys.exit(1)

        c = args.container or "DomainContext (领域容器)"
        e = args.engine or "DomainEngine (管线引擎)"
        ent = args.entity or "DomainEntity (领域实体)"
        s = args.structure or "DataTopology (数据结构)"
        p = args.property or "TraitMaterial (特性材质)"

        data = {
            "name": args.name,
            "domain": args.domain,
            "substrate": args.substrate,
            "container": c,
            "driver": args.driver or "DomainDriver (交互驱动)",
            "structure": s,
            "property": p,
            "entity": ent,
            "environment": args.environment or "WorldEnvironment (环境场)",
            "engine": e,
            "hello_world_code": build_default_hello_world(c, e, ent, s, p)
        }

    out_path = Path(args.output_dir).resolve()
    generate_blueprint(data, out_path)


if __name__ == "__main__":
    main()
