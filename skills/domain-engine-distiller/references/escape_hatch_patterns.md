# 逃生舱与洋葱分层架构设计模式 (Escape Hatch & Layering Patterns)

> 本文档说明如何在保持上层语法极简的同时，为 1% 的顶级专家保留无损通往底层的“逃生舱通道”。

---

## 1. 为什么必须有逃生舱？

许多自命不凡的框架之所以迅速走向衰退，核心原因在于**“过度封装形成的黑盒牢笼”**：
* 当普通开发者想要做默认功能时，极其方便；
* 一旦进阶开发者需要编写一个自定义着色器、接入特殊硬件缓冲、或优化极端瓶颈时，发现框架将所有底层私有化，无法扩展，只能彻底抛弃框架。

**Three.js 的成功秘诀之一就在于其优雅的逃生舱**：
* 小白使用 `MeshBasicMaterial`；
* 专家使用 `ShaderMaterial` / `RawShaderMaterial`，直接书写自定义 GLSL/WGSL，与引擎内部矩阵和灯光系统无缝融合。

---

## 2. 三层洋葱架构标准模式 (The 3-Tier Layering Pattern)

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: 声明式常识层 (DSL / High-Level Declarative)         │
│  - 纯物理常识命名，面向 90% 开发者，开箱即用默认配置              │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: 复合组装层 (Composable Pipeline)                  │
│  - 面向 9% 进阶开发者，支持模块拓扑插拔与自定义中间件               │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: 专家逃生舱 (Raw Escape Hatch)                     │
│  - 面向 1% 极客，支持注入底层原生 Handles、Buffers 与 CustomOps │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 逃生舱实现模式示例

#### 模式 A：自定义底层算子注入 (Custom Operator Injection)
```typescript
// 允许高级用户直接书写底层 WGSL / GLSL / C++ 算子
const customKernel = new CustomComputeKernel({
  wgsl: `
    @compute @workgroup_size(64)
    fn main(@builtin(global_invocation_id) id : vec3<u32>) {
      // 专家级手写计算逻辑
    }
  `,
  bindings: [
    { binding: 0, buffer: myCustomRawGpuBuffer }
  ]
});
```

#### 模式 B：原生底层句柄无损暴露 (Native Handle Access)
```typescript
// 允许直接提取底层的 WebGPU Device / AudioContext / WebGL Context
const rawDevice = engine.getNativeHandle<GPUDevice>();
const rawAudioCtx = engine.getNativeHandle<AudioContext>();

// 用户可以直接在外部操作 rawDevice，引擎承诺不发生状态破坏
```

---

## 3. 内存与垃圾回收 (GC) 友好型设计准则

1. **零运行时内存分配 (Zero Allocations in Loop)**：
   在渲染/计算主循环（`run` / `render`）中，严禁 `new Object()` 或创建临时数组。所有向量运算使用原地复用（`target.copy(source)`）。
2. **对象池化管理 (Object Pooling)**：
   针对高频生成的粒子、音符、事件对象，内置 `Pool<T>` 机制。
3. **显式销毁钩子 (Explicit Dispose Hook)**：
   所有持抱显存/原生资源的实体必须实现 `dispose()` 方法，避免浏览器内存泄漏。
