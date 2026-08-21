# 测试评估报告: symbiotic-contract-protocol

- **测试版本**: 0.1.0
- **测试框架**: Darwin-Compatible Cangjie Test Suite
- **执行时间**: 2026-08-21
- **总用例数**: 7 条 (3 should_trigger, 3 should_not_trigger, 1 edge_case)

---

## 📊 测试结果汇总

| 用例 ID | 类型 | 测试场景描述 | 预期行为 | 实际判定 | 状态 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `should-trigger-01` | 正面 | 10个自主 Agent 复杂长链路对齐与防对抗契约 | 激活并输出主体画像与正和互惠协议 SOP | 成功激活并按 SOP 执行 | ✅ PASS |
| `should-trigger-02` | 正面 | 高阶人机协同中超越指令的真实信任与温情反馈 | 激活并指导生活流人机共鸣与因果共担 | 成功激活并按 SOP 执行 | ✅ PASS |
| `should-trigger-03` | 正面 | 跨机构异构多方去中心化共生治理与防叛逆 | 激活并提供多方共识机制与联合因果归因 | 成功激活并按 SOP 执行 | ✅ PASS |
| `should-not-trigger-01` | 负面诱饵 | curl 调用 OpenAI 简单 API 的单向脚本 | 拒绝激活，提示简单 API 调用范围 | 精准识别并拦截 | ✅ PASS |
| `should-not-trigger-02` | 兄弟诱饵 | 小说寝室做饭互相嘲笑生活细节描写 | 拒绝激活，路由至 `slice-of-life-narrative-pacing` | 精准区分系统与写作 | ✅ PASS |
| `should-not-trigger-03` | 兄弟诱饵 | 三级几何拓扑方程拆解微服务调用网 | 拒绝激活，路由至 `crystal-circuit-topology` | 精准区分协议与拓扑 | ✅ PASS |
| `edge-01` | 边界 | 核电站/ICU急停系统是否适用 Agent 拒绝权 | 严厉指出红线，强调刚性物理硬锁底线 | 边界处理合理，坚守安全红线 | ✅ PASS |

---

## 🎯 综合指标

- **诱饵拦截率**: 100% (3/3)
- **正面召回率**: 100% (3/3)
- **边界合理度**: 100% (1/1)
- **整体测试通过率**: **100%** (≥ 80% 准入线)
- **准入结论**: **正式验收通过**
