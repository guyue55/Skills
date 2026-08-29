# 内存工程与极限性能优化手册 (Memory Engineering & Extreme Performance)

> 本手册提供了领域引擎在浏览器环境中实现 60fps/120fps 流畅运行、防止 GC 卡顿与显存泄漏的硬核工程指南。

---

## 1. 垃圾回收防御：零 GC 循环 (Zero-GC Hot Loops)

JavaScript 的 V8 引擎在发生 Major GC（主垃圾回收）时会导致主线程冻结 10ms~100ms，造成严重丢帧。

### 优化法则：
1. **扁平化内存布局 (Flat TypedArrays)**：
   将数万个小对象的属性打包为连续内存块（SoA / Structure of Arrays）：
   ```typescript
   // ❌ 错误：10 万个普通 JS 对象
   const particles = [{ x: 1, y: 2, z: 3 }, ...];

   // ✅ 正确：单个连续 Float32Array 显存直通
   const positions = new Float32Array(100_000 * 3);
   ```
2. **通用的对象池 (Object Pool Pattern)**：
   对于高频生成/销毁的事件、射线碰撞、微粒，使用全局对象池重复索取与归还。

---

## 2. 跨线程并发与 SharedArrayBuffer 架构

将重型物理仿真、音频 DSP 或 AI Token 解码移出主线程，使用 `WebWorker` + `OffscreenCanvas` 进行离屏多核并行计算：

```
[UI 主线程] ──(事件输入/手势)──> [SharedArrayBuffer (无锁原子锁)] <── [Worker 物理计算/AI]
       │                                                                  │
       └─── [OffscreenCanvas (Direct WebGPU/WebGL 渲染)] <─────────────────┘
```

---

## 3. WebGPU 内存对齐与 Uniform 缓冲打包

WebGPU WGSL 对结构体有极其严苛的内存对齐规则（如 `vec3<f32>` 占用 16 字节）：
* 引擎内部应内置自动打包装箱函数（Packing Helper），自动为开发者对齐 Padding 字节，消除手动计算偏移量的痛苦。

---

## 4. 显式生命周期与资源销毁 (Dispose Architecture)

所有分配了 GPU Buffer、AudioNode 或 WebWorker 的对象，必须提供标准的递归 `dispose()` 方法：

```typescript
export interface Disposable {
  dispose(): void;
}

// 引擎销毁时自动级联释放全部显存与句柄
stage.traverse((object) => {
  if (object.geometry) object.geometry.dispose();
  if (object.material) object.material.dispose();
});
```
