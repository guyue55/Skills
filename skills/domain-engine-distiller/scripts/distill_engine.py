#!/usr/bin/env python3
"""
领域引擎与心智模型蒸馏生成器 (Domain Engine Distiller CLI)

功能特性：
    1. 预设驱动与定制化蒸馏：内置 8 大前沿领域标准模型（WebGPU、端侧AI、WebAudio、3DGS、生物计算、WebXR、量化金融、无限画布）。
    2. 架构与规范全量产出：一键生成架构白皮书 (ARCHITECTURE.md)、10 行极简代码与元数据 (engine_blueprint.json)。
    3. 工业级 TypeScript 项目脚手架 (--scaffold-ts)：一键搭建基于 Vite + TS 的完整引擎源码骨架。
    4. 领域引擎统治力智能审计与评分 (--audit <file>)：评估 5 大卡槽完备度、DX 摩擦力与逃生舱设计，输出评分报告。

用法示例：
    # 1. 使用内置预设快速生成 WebGPU 计算引擎白皮书
    python3 scripts/distill_engine.py --preset webgpu --output-dir ./output/webgpu-engine

    # 2. 生成完整的 TypeScript 引擎源码项目骨架
    python3 scripts/distill_engine.py --preset webai --scaffold-ts --output-dir ./output/webai-project

    # 3. 对已有引擎蓝图进行统治力评分审计
    python3 scripts/distill_engine.py --audit ./output/webgpu-engine/engine_blueprint.json

    # 4. 自定义参数生成专属领域引擎
    python3 scripts/distill_engine.py \
        --name "BioFoldMesh.js" \
        --domain "端侧蛋白质折叠与分子动力学" \
        --substrate "WebAssembly SIMD + WebGPU 力场计算" \
        --container "ProteinStage (分子演化舞台)" \
        --driver "DynamicsDriver (动力学演化驱动器)" \
        --structure "ResidueSequence (氨基酸残基拓扑)" \
        --property "ElectrostaticMaterial (静电势与范德华力材质)" \
        --entity "ProteinMolecule (蛋白质大分子实体)" \
        --environment "SolventEnvironment (水溶剂与离子热噪声场)" \
        --engine "MolecularDynamicsEngine (分子动力学实时计算引擎)" \
        --output-dir ./output/bio-engine
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# 8 大前沿领域内置预设库
PRESETS: Dict[str, Dict[str, Any]] = {
    "webgpu": {
        "name": "ComputeFlow.js",
        "domain": "WebGPU 通用计算与流体/物理仿真",
        "substrate": "WebGPU WGSL Compute Pipeline + Storage Buffers + Memory Alignment",
        "container": "ComputeStage (计算仿真舞台)",
        "driver": "DispatchController (GPU 工作组分派调度器)",
        "structure": "GridGeometry (空间网格/粒子数据拓扑)",
        "property": "ComputeKernel (WGSL 计算着色器材质/算子)",
        "entity": "SimField (物理场具象化个体)",
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
    },
    "biofold": {
        "name": "BioFoldMesh.js",
        "domain": "端侧生物大分子折叠与分子动力学",
        "substrate": "WebAssembly SIMD + WebGPU 3D 空间力场计算",
        "container": "ProteinStage (蛋白质分子演化舞台)",
        "driver": "DynamicsDriver (动力学演化驱动器)",
        "structure": "ResidueSequence (氨基酸残基拓扑骨架)",
        "property": "ElectrostaticMaterial (静电势与范德华力材质)",
        "entity": "ProteinMolecule (蛋白质大分子实体)",
        "environment": "SolventEnvironment (水溶剂与离子热噪声场)",
        "engine": "MolecularDynamicsEngine (分子动力学实时计算引擎)",
        "hello_world_code": """// 1. 初始化分子舞台与引擎
const stage = new ProteinStage();
const engine = new MolecularDynamicsEngine();

// 2. 组装蛋白质实体 (残基骨架 + 静电力场)
const protein = new ProteinMolecule({
  structure: new ResidueSequence({ pdb: './assets/hemoglobin.pdb' }),
  property: new ElectrostaticMaterial({ dielectric: 78.5 })
});
stage.add(protein);
stage.add(new SolventEnvironment({ temperature: 310 }));

// 3. 启动分子动力学演化模拟
engine.simulate(stage);"""
    },
    "webxr": {
        "name": "SpatialCraft.js",
        "domain": "WebXR 空间计算与 MR 手势交互",
        "substrate": "WebXR Device API + Hand Tracking + Hit Test + Spatial Anchors",
        "container": "SpatialStage (虚实共生空间上下文)",
        "driver": "SpatialController (双手25骨节与视线凝视驱动)",
        "structure": "SpatialAnchorGrid (空间锚点与房间几何拓扑)",
        "property": "HolographicMaterial (全息光效与深度遮蔽材质)",
        "entity": "SpatialWidget (悬浮空间 UI 与交互实体)",
        "environment": "PassthroughLighting (真实环境光照估计场)",
        "engine": "SpatialEngine (WebXR 立体双目渲染与触觉引擎)",
        "hello_world_code": """// 1. 创建空间舞台与引擎
const stage = new SpatialStage();
const engine = new SpatialEngine({ referenceSpace: 'local-floor' });

// 2. 创建空间全息交互面板
const panel = new SpatialWidget({
  structure: new SpatialAnchorGrid({ position: [0, 1.2, -1.0] }),
  material: new HolographicMaterial({ blur: 16 })
});
stage.add(panel);
stage.add(new SpatialController({ mode: 'hands-and-gaze' }));

// 3. 启动 WebXR 会话循环
engine.startSession(stage);"""
    },
    "quant": {
        "name": "QuantFlow.js",
        "domain": "量化金融高频行情流与策略回测",
        "substrate": "WebSocket Binary Stream + Arrow/Parquet + WebAssembly SIMD",
        "container": "MarketStage (多资产订单簿与行情舞台)",
        "driver": "TickDriver (高频行情流与回放驱动器)",
        "structure": "OrderBookSeries (密集深度图与K线拓扑)",
        "property": "AlphaStrategy (量化因子与交易策略材质)",
        "entity": "TradingPortfolio (策略投资组合实体)",
        "environment": "MarketMicrostructure (流动性冲击与延迟波动场)",
        "engine": "QuantEngine (超低延迟回测与流转引擎)",
        "hello_world_code": """// 1. 创建行情舞台与回测引擎
const stage = new MarketStage();
const engine = new QuantEngine();

// 2. 组装量化策略组合
const portfolio = new TradingPortfolio({
  structure: new OrderBookSeries({ symbol: 'BTC-USDT' }),
  strategy: new AlphaStrategy({ fastEMA: 12, slowEMA: 26 })
});
stage.add(portfolio);
stage.add(new TickDriver({ speed: 10.0 }));

// 3. 启动毫秒级实时回测
engine.backtest(stage);"""
    },
    "nodecanvas": {
        "name": "NodeCanvas.js",
        "domain": "无限画布与生成式节点图元引擎",
        "substrate": "Canvas2D/WebGL 混合管线 + 空间四叉树索引 + DAG 拓扑流",
        "container": "CanvasStage (无限空间画布舞台)",
        "driver": "ViewportCamera (平移缩放与视口驱动器)",
        "structure": "DAGGraphTopology (节点与端口连线网络)",
        "property": "NodeSkinMaterial (节点外观主题与流光材质)",
        "entity": "GraphNode (功能图元实体)",
        "environment": "GridSnapField (磁吸对齐网格与碰撞力场)",
        "engine": "CanvasEngine (四叉树视锥剔除与渲染引擎)",
        "hello_world_code": """// 1. 创建画布舞台与引擎
const stage = new CanvasStage();
const engine = new CanvasEngine({ container: '#canvas-root' });

// 2. 创建计算图元节点
const node = new GraphNode({
  structure: new DAGGraphTopology({ inputs: 2, outputs: 1 }),
  material: new NodeSkinMaterial({ theme: 'dark-cyber' })
});
stage.add(node);
stage.add(new ViewportCamera({ zoom: 1.0 }));

// 3. 启动渲染与连线交互循环
engine.render(stage);"""
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


def generate_typescript_scaffold(data: Dict[str, Any], output_dir: Path):
    """一键生成基于 Vite + TypeScript 的完整引擎项目源码结构"""
    src_dir = output_dir / "src"
    core_dir = src_dir / "core"
    types_dir = src_dir / "types"
    examples_dir = output_dir / "examples"

    for d in [core_dir, types_dir, examples_dir]:
        d.mkdir(parents=True, exist_ok=True)

    c_name = data['container'].split()[0]
    d_name = data['driver'].split()[0]
    s_name = data['structure'].split()[0]
    p_name = data['property'].split()[0]
    ent_name = data['entity'].split()[0]
    env_name = data['environment'].split()[0]
    eng_name = data['engine'].split()[0]

    # package.json
    pkg_json = {
        "name": data["name"].lower().replace(".js", "").replace(" ", "-"),
        "version": "0.1.0",
        "description": data["domain"],
        "main": "dist/index.js",
        "module": "dist/index.mjs",
        "types": "dist/index.d.ts",
        "scripts": {
            "dev": "vite",
            "build": "vite build && tsc --emitDeclarationOnly",
            "test": "vitest"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "vite": "^5.1.4",
            "vitest": "^1.3.1"
        }
    }
    with open(output_dir / "package.json", "w", encoding="utf-8") as f:
        json.dump(pkg_json, f, indent=2, ensure_ascii=False)

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "ESNext",
            "moduleResolution": "bundler",
            "declaration": True,
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "outDir": "dist"
        },
        "include": ["src/**/*"]
    }
    with open(output_dir / "tsconfig.json", "w", encoding="utf-8") as f:
        json.dump(tsconfig, f, indent=2)

    # src/types/index.ts
    types_code = f"""/**
 * {data['name']} 核心类型定义
 */

export interface Disposable {{
  dispose(): void;
}}

export interface EngineConfig {{
  target?: string | HTMLElement;
  powerPreference?: 'high-performance' | 'low-power';
  antialias?: boolean;
}}

export interface EntityOptions<TStructure, TProperty> {{
  structure: TStructure;
  property: TProperty;
  name?: string;
}}
"""
    with open(types_dir / "index.ts", "w", encoding="utf-8") as f:
        f.write(types_code)

    # src/core/container.ts
    with open(core_dir / "container.ts", "w", encoding="utf-8") as f:
        f.write(f"""import {{ Disposable }} from '../types';
import {{ {ent_name} }} from './entity';

/**
 * {data['container']}
 * 容纳所有实体与环境场的全局宇宙舞台
 */
export class {c_name} implements Disposable {{
  public readonly children: {ent_name}[] = [];
  public readonly environments: any[] = [];

  public add(item: {ent_name} | any): this {{
    if (item instanceof {ent_name}) {{
      this.children.push(item);
    }} else {{
      this.environments.push(item);
    }}
    return this;
  }}

  public remove(item: {ent_name} | any): this {{
    const idx = this.children.indexOf(item);
    if (idx !== -1) this.children.splice(idx, 1);
    return this;
  }}

  public dispose(): void {{
    this.children.forEach(c => c.dispose());
    this.children.length = 0;
    this.environments.length = 0;
  }}
}}
""")

    # src/core/entity.ts
    with open(core_dir / "entity.ts", "w", encoding="utf-8") as f:
        f.write(f"""import {{ Disposable, EntityOptions }} from '../types';

/**
 * {data['entity']}
 * 具象化操作个体 (Structure ⊗ Property)
 */
export class {ent_name} implements Disposable {{
  public structure: any;
  public property: any;
  public name: string;

  constructor(options: {{ structure: any; property: any; name?: string }}) {{
    this.structure = options.structure;
    this.property = options.property;
    this.name = options.name || '{ent_name}';
  }}

  public dispose(): void {{
    if (this.structure && typeof this.structure.dispose === 'function') {{
      this.structure.dispose();
    }}
    if (this.property && typeof this.property.dispose === 'function') {{
      this.property.dispose();
    }}
  }}
}}
""")

    # src/core/engine.ts
    with open(core_dir / "engine.ts", "w", encoding="utf-8") as f:
        f.write(f"""import {{ EngineConfig, Disposable }} from '../types';
import {{ {c_name} }} from './container';

/**
 * {data['engine']}
 * 核心调度与管线输出引擎
 */
export class {eng_name} implements Disposable {{
  private _config: EngineConfig;
  private _isRunning: boolean = false;
  private _nativeHandle: any = null;

  constructor(config: EngineConfig = {{}}) {{
    this._config = config;
  }}

  /**
   * 专家逃生舱：获取底层硬件句柄
   */
  public getNativeHandle<T>(): T {{
    return this._nativeHandle as T;
  }}

  public run(stage: {c_name}): void {{
    this._isRunning = true;
    console.log(`🚀 [{data['name']}] 引擎主循环已启动，当前管理实体数: ${{stage.children.length}}`);
  }}

  public stop(): void {{
    this._isRunning = false;
  }}

  public dispose(): void {{
    this.stop();
  }}
}}
""")

    # src/index.ts
    with open(src_dir / "index.ts", "w", encoding="utf-8") as f:
        f.write(f"""export * from './types';
export * from './core/container';
export * from './core/entity';
export * from './core/engine';
""")

    # examples/index.html
    html_demo = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{data['name']} - 10秒极简 Playground</title>
  <style>
    body {{ background: #0b0d19; color: #fff; font-family: system-ui; padding: 40px; }}
    pre {{ background: #1a1e36; padding: 16px; border-radius: 8px; color: #00d2ff; }}
  </style>
</head>
<body>
  <h1>✨ {data['name']} 运行中</h1>
  <p>领域：{data['domain']}</p>
  <pre>{data['hello_world_code']}</pre>
</body>
</html>
"""
    with open(examples_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_demo)


def audit_blueprint(blueprint_path: Path) -> bool:
    """对领域引擎蓝图进行统治力指标评分与合规审计"""
    if not blueprint_path.exists():
        print(f"❌ 错误: 找不到蓝图文件: {blueprint_path}")
        return False

    with open(blueprint_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n🔬 [Three.js 统治力引擎审计报告: {data.get('name', 'Unknown')}]")
    print("=" * 60)

    score = 100
    deductions: List[str] = []

    # 1. 检查 5 大卡槽完备性
    required_slots = ["container", "driver", "structure", "property", "entity", "environment", "engine"]
    for slot in required_slots:
        if not data.get(slot):
            deductions.append(f"缺失五常识核心卡槽: {slot} (-15分)")
            score -= 15

    # 2. 检查名称直觉性（避免学术黑话）
    complex_jargons = ["heterogeneous", "differentiable", "isomorphic", "tensorarray", "subroutine"]
    for k, v in data.items():
        if isinstance(v, str):
            for jargon in complex_jargons:
                if jargon in v.lower():
                    deductions.append(f"发现概念学术黑话 '{jargon}' 于 {k}，违反低认知负荷准则 (-5分)")
                    score -= 5

    # 3. 检查 10 行极简契约行数
    code = data.get("hello_world_code", "")
    lines = [l for l in code.strip().splitlines() if l.strip() and not l.strip().startswith("//")]
    if len(lines) > 15:
        deductions.append(f"Hello World 代码量过长 ({len(lines)} 行 > 15 行)，破坏 180 秒多巴胺体验 (-10分)")
        score -= 10

    # 4. 检查底层痛点描述
    if not data.get("substrate") or len(data.get("substrate", "")) < 10:
        deductions.append("底层技术痛点描述过弱，缺乏足够的降维势能 (-10分)")
        score -= 10

    print(f"📊 统治力综合得分: {max(0, score)} / 100")
    if score >= 90:
        print("🏆 评级: S 级 (具备成为领域绝对统治标准的潜力)")
    elif score >= 75:
        print("🥇 评级: A 级 (设计优秀，稍作打磨即可引爆社区)")
    else:
        print("⚠️ 评级: B/C 级 (需进一步重构心智模型与代码契约)")

    if deductions:
        print("\n🔧 优化建议项:")
        for d in deductions:
            print(f"  • {d}")
    else:
        print("\n✨ 恭喜！各项指标全部符合顶级领域引擎设计规范！")

    print("=" * 60 + "\n")
    return score >= 75


def generate_blueprint(data: Dict[str, Any], output_dir: Path, scaffold_ts: bool = False):
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

    if scaffold_ts:
        generate_typescript_scaffold(data, output_dir)
        print(f"📦 已同步生成 TypeScript 完整工程骨架 (src/core, package.json, vite.config)")

    print(f"✨ 领域引擎蓝图已成功生成至: {output_dir}")
    print(f"   ├── 📄 {blueprint_json.name} (元数据配置)")
    print(f"   ├── 📘 {arch_md.name} (架构白皮书)")
    print(f"   └── 💻 {example_js.name} (10行极简契约示例)")


def main():
    parser = argparse.ArgumentParser(description="领域引擎与心智模型蒸馏生成器 (Three.js of Any Domain)")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="使用内置 8 大领域预设")
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
    parser.add_argument("--scaffold-ts", action="store_true", help="一键生成完整 TypeScript 项目源码脚手架")
    parser.add_argument("--audit", help="对指定 engine_blueprint.json 进行统治力指标审计与评分")
    parser.add_argument("-o", "--output-dir", default="./output/domain-engine", help="输出目录")

    args = parser.parse_args()

    if args.audit:
        audit_blueprint(Path(args.audit).resolve())
        sys.exit(0)

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
    generate_blueprint(data, out_path, scaffold_ts=args.scaffold_ts)


if __name__ == "__main__":
    main()
