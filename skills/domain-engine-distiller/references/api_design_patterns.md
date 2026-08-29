# 高性能领域引擎 API 设计模式规范 (High-Performance Engine API Design Patterns)

> 本文档总结了在设计领域级引擎（Three.js 同级项目）时，兼顾“极简开发体验 (DX)”与“60/120fps 极限性能”的五大设计模式。

---

## 1. 模式一：双模 API 架构（声明式 + 链式构建器）

引擎应同时支持**声明式参数配置**（适合初学者与序列化）与**链式构建器 (Fluent Builder)**（适合进阶动态组装）：

```typescript
// 风格 A：纯声明式配置（10 秒上手）
const entity = new SimField({
  structure: new ParticleGrid({ count: 1_000_000 }),
  kernel: new FluidKernel({ viscosity: 0.05 })
});

// 风格 B：链式构建器（类型安全且易于动态流转）
const entity = new SimField()
  .setStructure(new ParticleGrid().withCount(1_000_000))
  .setKernel(new FluidKernel().withViscosity(0.05));
```

---

## 2. 模式二：原地复用与零临时分配 (In-Place Mutation)

在动画、渲染与实时计算主循环中，**严禁使用返回新对象的方法**。必须采用“原地修改（In-Place）”或“目标参数传入（Target Passing）”模式：

```typescript
// ❌ 错误做法：每帧产生垃圾对象，导致 GC 掉帧
function update() {
  const diff = player.position.subtract(target.position); // 内部 new Vector3()
}

// ✅ 正确做法：预分配临时变量或原地计算
const _tempVec = new Vector3(); // 单例内部复用

function update() {
  _tempVec.copy(player.position).sub(target.position);
}
```

---

## 3. 模式三：严格 TypeScript 泛型推导与类型守卫

让开发者在 IDE 中敲击 `.` 即可获得完整的智能感知（IntelliSense），无需翻阅文档：

```typescript
export interface EntityOptions<TStructure extends Structure, TProperty extends Property> {
  structure: TStructure;
  property: TProperty;
  name?: string;
  tags?: string[];
}

export class Entity<TStructure extends Structure = Structure, TProperty extends Property = Property> {
  public readonly structure: TStructure;
  public property: TProperty;

  constructor(options: EntityOptions<TStructure, TProperty>) {
    this.structure = options.structure;
    this.property = options.property;
  }
}
```

---

## 4. 模式四：解耦的“Headless 核心”与“可替换渲染后端”

核心状态机与数据拓扑应当是 **Headless（无头）** 的，渲染后端作为插件动态挂载，从而轻松支持服务端 SSR、测试自动化与多端渲染：

```typescript
// 核心容器与实体纯 JS/TS 计算，无 DOM 依赖
const stage = new UniversalStage();
stage.add(new UniversalEntity());

// 场景 1：浏览器端 Canvas/WebGPU 渲染
const webEngine = new WebGPURenderer({ canvas: domElement });
webEngine.render(stage);

// 场景 2：Node.js 服务端 Headless 离线计算与测试
const headlessEngine = new HeadlessComputeEngine();
const resultBuffer = headlessEngine.step(stage, 1.0);
```

---

## 5. 模式五：细粒度响应式脏标记 (Dirty-Flag Optimization)

避免每帧全量遍历与全量上传 GPU 显存。当且仅当属性被修改时标记 `isDirty = true`：

```typescript
export class Material {
  private _color: number = 0xffffff;
  public needsUpdate: boolean = false;

  get color(): number {
    return this._color;
  }

  set color(val: number) {
    if (this._color !== val) {
      this._color = val;
      this.needsUpdate = true; // 告知引擎下一帧上传 Uniform Buffer
    }
  }
}
```
