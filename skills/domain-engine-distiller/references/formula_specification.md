# 通用领域引擎蒸馏公式规范 (Universal Engine Master Formula Specification)

> 本规范定义了如何将任意地狱级底层技术，转化为统治级开发者生态框架的数学模型与认知工程学规则。

---

## 1. 框架统治力动力学方程 (Dominance Dynamic Equation)

在软件工程演化史中，一个框架能否成为领域事实标准（De Facto Standard），取决于其**认知扩张势能**与**阻力系数**的比值：

$$\mathbf{Dominance} = \frac{\Delta \mathbf{P}_{\text{pain}} \times \mathbf{E}_{\text{paradigm}} \times \mathbf{A}_{\text{sweet-spot}}}{\mathbf{T}_{\text{time-to-wow}} \times \mathbf{C}_{\text{cognitive-load}}}$$

### 1.1 参数物理意义与量化度量

| 变量 | 物理意义 | 目标指标 / 检验阈值 |
| :--- | :--- | :--- |
| $\Delta \mathbf{P}_{\text{pain}}$ | **痛点消除倍率**：消除的原生样板代码与状态机复杂度 | $\ge 10\times \sim 100\times$ (如 200 行 WebGL $\to$ 10 行 Three.js) |
| $\mathbf{E}_{\text{paradigm}}$ | **范式红利乘数**：底层硬件或 Web 标准的代际转移势能 | 处于标准成熟期早期（如 WebGPU、端侧 WebAssembly NPU） |
| $\mathbf{A}_{\text{sweet-spot}}$ | **甜点位抽象指数**：不做臃肿黑盒全家桶，做高内聚画笔 | 保持核心无 GUI 依赖、无强制项目脚手架侵入 |
| $\mathbf{T}_{\text{time-to-wow}}$ | **惊艳时延**：从克隆项目到屏幕产生多巴胺反馈的时间 | $\le 180\text{ 秒}$（点开即见奇迹） |
| $\mathbf{C}_{\text{cognitive-load}}$ | **心智认知负荷**：理解核心工作流所需的非日常概念数量 | $\le 5\text{ 个核心实体名词}$（映射日常物理常识） |

---

## 2. 五常识投影法则 (The Universal 5 Primitives Matrix)

任何复杂系统的运行，都可以严格同构投影至以下 5 个物理常识元：

```
┌────────────────────────────────────────────────────────────────────────┐
│  Container (宇宙容器)                                                   │
│    ├── Driver / Observer (观察视角与交互输入)                           │
│    ├── Environment (外部全局场与约束法则)                                │
│    └── Entity (具象化可操作个体)                                         │
│          ├── Structure (骨架数据与几何拓扑)                               │
│          └── Property (演化材质与物理/行为特性)                          │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   ▼
         Engine (管线调度与多核输出引擎)
```

### 2.1 元投影推导公理
1. **容器独立性公理**：容器只负责维护拓扑树，不负责具体执行逻辑。
2. **实体解耦公理**：实体必须是 `Structure`（骨架/拓扑）与 `Property`（质感/算子）的直积组合（`Entity = Structure ⊗ Property`），支持材质或拓扑的独立热替换。
3. **管线幂等公理**：`Engine.run(Container)` 负责纯粹的数据流转与硬件调度，随时可暂停、重置或单帧步进。

---

## 3. 认知负荷控制红线 (Cognitive Anti-Patterns)

1. **拒绝发明学术黑话**：不要将“发声体”命名为 `DynamicAcousticHeterogeneousEmitter`，直接命名为 `SoundTrack` 或 `AudioSource`。
2. **拒绝强制双向绑定与深层继承**：采用组合优于继承模式，所有配置支持扁平 Plain Object 注入。
3. **拒绝隐式全局单例**：允许在同一个页面中无污染地并发实例化多个独立 `Container` 与 `Engine`。
