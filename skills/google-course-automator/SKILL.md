---
name: google-course-automator
description: Google Skills 课程自动化助手。当用户发来 skills.google 课程/路径链接或课程名称（如 Associate Cloud Engineer、Cloud Digital Leader、某门课名），并要求"过完/加速完成/自动做课/标记完成/刷题/考过 quiz/接管浏览器做课程"时使用；也用于"领免费点数/加入 GEAR/开通 Lab 权限/查点数余额/做 Lab"等权益相关诉求。自动探测并复用当前可用的浏览器入口（已开放 CDP / Browser Use MCP / chrome-devtools MCP），没有才自建独立调试 profile：视频一键标记完成、Quiz 读题后由 Agent 作答争取通过、Lab/文档跳过、实时读取进度；并支持 GEAR 官方链路入会、点数/权益只读诊断。触发词：Google Skills、技能徽章、认证课程、过课、刷题、标记完成、自动考试、skills.google 链接、GEAR、免费点数、实验点数、领取点数、订阅、Skillshop、Credential 正式考试、skillshop.exceedlms.com 链接、结业考试。
---

# Google Course Automator（GCA）

> 用户发一个 Google Skills 课程链接或课程名称，接管已登录浏览器把课程推进到当前机制下的完成极限。

---

## L1: 能做什么 / 不能做什么

**能**（只用平台自带的按钮和链接，效果等同用户亲手点）：

- 视频 → 点 "Mark as completed"
- Quiz → 读题目与选项 → Agent 用领域知识判断 → 点选提交 → 没过就 Retake 纠错重考
- Lab / Document / html_bundle → 点平台 Next 跳过
- 读取路径/课程的完成进度、活动清单、未通过 Quiz 清单
- 只读诊断权益状态（点数余额 / GEAR 会员 / 开发者资料是否公开）→ `entitlement`
- 引导用户完成 GEAR 官方入会（填资料、设为公开）以开通每月 35 免费点数——见 Phase 4
- 有有效点数/令牌且用户授权时，在无痕上下文真实操作 Lab 并逐项点"检查我的进度"验证
- 在**用户本人账号、本人在场、明确知情授权**前提下，辅助 Google Skillshop（`skillshop.exceedlms.com`）正式 Credential 结业考试：逐题联网核实官方文档后给出候选答案、由用户逐题确认、登录密码由用户本人输入、提交前逐题复核——见 Phase 5

**不能**（硬边界，任何情况下都不做）：

- 不伪造请求、不改后台数据、不直接改 `isComplete`/分数
- 不为**他人**代考、不提供或使用泄题/灰产答案、不绕过监考、不伪造身份；不满足"本人账号 + 本人在场 + 明确知情授权 + 每题联网核实 + 关键步骤本人确认"全部条件时，一律拒绝正式 Credential 考试辅助（口径见 Phase 5 与 L5 第 5 条）
- Lab（动手实验）需在真实 GCP 环境里完成计时任务，通常还消耗实验点数/令牌；无有效点数/令牌、或未获用户明确授权购买时**不能启动**，更不能用脚本伪造完成。若用户提供令牌并授权，可在无痕上下文里真实操作、逐项点“检查我的进度”验证
- 不改动用户日常 Chrome 的默认 profile 数据；优先复用已登录/已授权的页面或调试实例，必要时才用独立 profile（只复制登录态，不改源文件）

---

## L2: 核心机制（实测，决定成败）

| 对象      | 平台 DOM / 行为                                                                                  | 处理方式                 |
| ------- | -------------------------------------------------------------------------------------------- | -------------------- |
| 活动清单    | 路径页 `ql-contents-menu` 的 `modules` 属性（JSON），字段 `href/title/isComplete/progress`              | `read-acts` 解析       |
| 视频      | `ql-button[href*="complete_button"]`（"Mark as completed"），点击后自动跳下一步                          | `advance` 自动点        |
| Next    | `ql-button.next-button`，完成前 disabled；Lab 页点击常被拦截，**直接导航其 href 可跳过**                          | `advance` 用导航        |
| Quiz 入口 | URL 含 `/quizzes/<id>`；未开始有 `a.start-button`，未通过有 `ql-button.retake-button`                   | `quiz-read --retake` |
| Quiz 题目 | 题干 `QL-ITEM-STEM`，选项 `md-radio`(单选)/`md-checkbox`(多选)，**都在 Shadow DOM 里**；`aria-label` 是选项文本 | 递归遍历（脚本已封装）          |
| Quiz 提交 | 提交按钮是 `ql-button.submit-button`，**不是 Next**（Next 只是翻题）                                       | `quiz-answer` 自动点    |
| Quiz 重排 | 每次 Retake，题目顺序和选项顺序都**重新随机**                                                                 | 按题干关键词+选项文本定位，不按位置   |

**三条铁律**（违反必出错）：

1. **入口不僵化，但浏览器只启动一次**：优先复用当前会话已提供的浏览器工具（Browser Use / chrome-devtools MCP）或已开放的 CDP 端口；只有都不可用时才自建独立调试浏览器。反复启动/重启才是"弹窗关不掉"的真正根因。启动命令带 `--remote-allow-origins=*`，各 `gca.py` 命令作为短连接调用安全；`advance` 内部单进程单连接跑完整轮次。**核心是复用，不是绑定某个入口。**
2. **等渲染**：网络卡顿时页面 3-8 秒才出题目，必须轮询探测到题干出现再操作（脚本已内置）。
3. **按文本定位**：Quiz 选项每次重考重排、且可能同名，必须"题干关键词 + 选项文本"双重定位，绝不按下标。

---

## L2.5: 全局进度总览与完成判定（DoD）

> 专治"只做一部分就宣告结束"。接任务先建总账，只有用户最终要的交付物（L0）经权威字段核实完成，才能说"完成/结束"。本节的刷新点复用各 Phase 已有的 CHECKPOINT（见下方"刷新时机"），不另起一套流程。

**三条判定纪律：**

1. **动作 ≠ 意图**：点 Next / 提交答卷 / 访问过页面只是动作，回读权威字段才算完成。
2. **局部 ≠ 整体**：单题通过 ≠ Quiz 完成；Quiz 完成 ≠ 课程完成；课程完成 ≠ 路径完成；考试通过 ≠ 证书到手（Phase 5 Step 5 即此坑）。
3. **信号 ≠ 状态**："Congratulations" 文本、进度条、记忆、几步前的中间读数都可能滞后，以权威字段为准。

**全局进度总账（接任务先建，对话内维护、上下文压缩后先重建再续）：**

| 层级      | 记什么                        | 权威依据（按交付物配对，必须回读）                                                                         |
| ------- | -------------------------- | ----------------------------------------------------------------------------------------- |
| L0 用户意图 | 最终交付物（写具体，如"证书到手"而非"通过考试"） | 证书类只认**证书弹窗完成ID**；课程类认路径全 completed；考试类认最终成绩——各类判据不可互相替代                                  |
| L1 阶段   | 必经阶段：各课程、各模块、各 activity    | `read-acts` 的 `complete`、`quiz-list` 的 `isComplete`、`li.outerHTML` 含 `completed`、`recert` |
| L2 动作   | 视频标记 / Quiz 作答 / 模块滚到底     | 动作返回 + 回读对应 L1 字段确认生效                                                                     |

状态只写三种：`⬜未做` / `✅已完成（附权威依据）` / `⛔阻塞（Lab/点数/授权，注明原因）`，禁止"好像完成了"。**只有 L0 全 ✅ 才算整体完成**；L1/L2 全绿而 L0 未达成，仍不算完成。

**刷新时机**：复用已有 CHECKPOINT——Phase 3a/3b 的 `read-acts`/`quiz-list` 复查、Phase 5 的证书弹窗复核，就是总账刷新点，不必新增步骤；关键节点交付前再回读一次。

**终局核验 DoD（说"完成/结束/拿下了"之前强制，不可省）：**

1. **回读**：重新访问权威入口读当前真实状态（`read-acts` / `quiz-list` / 证书弹窗 / `recert`），不用记忆、缓存或旧中间结果。
2. **对照**：逐项扫总账，显式列出未达项与阻塞项。
3. **宣告**：L0 全 ✅ 才说"完成"并附权威依据；否则只报"当前 X/Y，剩余：…"，**主动给出剩余项与下一动作，不等用户追问**。

---

## L3: 工作流

### Phase 0 — 探测并接管浏览器（每次会话先做）

**原则：浏览器调用方式只是入口，不是目的。** 目标是拿到一个已登录 skills.google、可执行 DOM/JS 操作的页面。按下面顺序自动探测，命中即停，不僵化于自建 CDP。

```bash
# 1) 一键探测：已开放 CDP 端口 / 本机浏览器技能 / MCP 配置（只读，不启动浏览器）
python3 <skill>/scripts/gca.py browser-detect
# 若已知当前会话有浏览器 MCP 工具，可带上工具名让建议更准：
python3 <skill>/scripts/gca.py browser-detect --session-tools "mcp__browser__browsers_list,mcp__chrome-devtools__evaluate"
```

**决策矩阵（按优先级）**

| 探测结果                                                   | 采用入口                                                               | 注意事项                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------ | ---------------------------------------- |
| 已有 CDP 端口且标签页含 `skills.google`                         | 直接复用该端口：`GCA_PORT=<port>` 或每条命令 `--port <port>`                    | **绝不重启浏览器**；gca.py 默认端口不可达时也会自动复用可用端口并提示 |
| 有 CDP 端口但没有目标标签                                        | 先在该端口打开课程链接确认登录态，再复用                                               | 别把无关浏览器当目标                               |
| 当前会话有 `mcp__browser__*` / `mcp__chrome-devtools__*` 工具 | 优先用 MCP 打开页面、读 DOM、点击；批量 Quiz 若有 `evaluate` 能力则直接复用 gca.py 的 JS 片段 | 配置里写了 MCP ≠ 本会话已加载；以工具清单为准，不要假装能用        |
| 以上都没有                                                  | 走下面的「自建 CDP」fallback                                               | 只启动一次                                    |

**自建 CDP fallback（仅当上面都不可用）：**

1. 运行 `browser-start-info`，按输出从用户日常 Chrome 的 Default profile 复制登录态文件到独立 profile 目录。**Cookies 在 `Default/Cookies`，不是 `Default/Network/Cookies`**。
2. 用**后台任务机制**（不是 nohup）常驻运行输出里的 `start_command`，浏览器只启动一次。
3. 轮询 `curl http://127.0.0.1:9333/json/version` 直到 200。

- 🔴 CHECKPOINT：`browser-check` 返回 `ok:true`（或用 MCP 成功读到页面 DOM），且课程页能看到登录态，再继续 Phase 1。若读活动返回 NO_MENU / 要求登录，提示用户重新登录一次。
- 端口被占用或非标准服务时：设置 `GCA_PORT=9334`，或每条命令加 `--port 9334`（所有子命令都支持）。换端口后启动与后续命令必须一致。
- 若用 MCP 而非 gca.py 做操作，仍沿用 L2 的 DOM/Quiz 机制与 L5 黑名单；MCP 无法执行递归 JS 时不要硬凑，回落到 gca.py + CDP。

### Phase 1 — 理解任务范围

用户给的是**路径链接**（`/paths/<id>`）还是**单门课链接**（`/course_sessions/...` 或 `/course_templates/...`）？

```bash
python3 <skill>/scripts/gca.py read-acts "<用户给的URL>"
```

- 返回 12 个活动 = 路径；返回若干 = 课程。记录 `title / progress / complete`。
- 若用户只给课程名称（没链接）：先用 WebSearch 查 `site:skills.google <课程名>` 定位 URL；查不到就问用户确认链接。
- 🔴 按 L2.5 建**全局进度总账**：把用户最终要的交付物写进 L0（如"证书到手"而非"通过考试"），各课/模块/活动列进 L1。后续在各 Phase 已有 CHECKPOINT 处刷新，宣告完成前必做终局核验。
- 🛑 STOP：把识别到的课程/路径范围复述给用户确认，尤其是"要全过"还是"只过某几项"。

### Phase 2 — 选择推进模式（关键决策点）

🛑 STOP — 根据用户意图和平台机制，明确告知并选择：

| 模式         | 动作                                      | 结果                      |
| ---------- | --------------------------------------- | ----------------------- |
| **最快模式**   | 视频全标记，Lab/Quiz/Document 全跳过             | 最快，但进度停在 80-90%，课程显示未完成 |
| **争取通过模式** | 视频标记 + Quiz 全部作答争取过，只跳 Lab              | 完成度高，仍受 Lab 限制          |
| **只要进度**   | 只标记视频，其他跳过                              | 追求速度                    |
| **自主选课模式** | 用户说"由你决定/找个值得做的/只要结果"时：见 Phase 2.5 自动挑课 | 连续推进多门，用户只看最终战报         |

- 用户说"快速过/尽快/能过就过" → 默认最快模式，但要**明确告知跳过 Quiz/Lab 会停在 80-90%**。
- 用户说"题目能做就做/争取考过" → 争取通过模式。
- 用户说"由你决定/我只要结果/找些其它值得做的/优先选开发类逐个做" → 自主选课模式（Phase 2.5），不必逐门回头确认，但要控制边界（不购买、不伪造、不碰认证考试）。
- 未明确时，用一次提问确认，不要擅自替用户决定。

### Phase 2.5 — 自主选课（用户"由你决定，只要结果"时）

按性价比挑课，用 `read-acts` 只读批量评估候选（**不改写任何东西**），再决定先做哪门：

1. 从 `https://www.skills.google/paths` 目录页搜开发类关键词（`developer` / `api` / `cloud` / `data` / `app`），收集候选路径 ID。
2. 对候选路径跑 `scan_courses.py <path_id ...>`：批量扫描路径内各 `course_template` 的活动构成（视频/Quiz/Lab/其他/待做非Lab数），按"零 Lab + 有 Quiz + 未完成非 Lab 多"自动排序，零 Lab 有 Quiz 的课（可快速完成）排在前面。需看某路径子课内部明细（含顶层看不到的 Quiz）时再跑 `dump_path.py <path_id>`。
3. 排序优先级：**Quiz 多 + Lab 少 + 非 Lab 内容多 + 未完成多** 的先做；`Quiz=0` 的纯 Lab 课直接跳过（做了也只会卡在 Lab）；已接近完成的先收尾。
4. 一次只推进一门，跑完按 L2/Phase 3 流程记战报，再挑下一门。全程沿用"争取通过模式"（视频标记 + Quiz 作答 + 跳 Lab）。

- 🔴 CHECKPOINT：选定后简短告知用户"将做哪门、为什么（Quiz 数/规模）"，然后连续推进，不必逐门等待确认。

### Phase 3a — 最快模式推进

```bash
python3 <skill>/scripts/gca.py advance "<路径或课程URL>" 200
```

- 循环：路径页选下一个新活动 → 视频点完成 → Lab/Quiz/Doc 导航 Next 跳过 → 卡住回路径页换活动。
- 用 `title` 去重（href 随进度变化，不能作稳定标识）；只处理 `progress<50` 的新活动。
- 输出每次 VIDEO/LAB/SKIP 和最终进度。
- **跳过已确认不做的纯 Lab 课**：`advance` 在路径页只能看到 `href`/`progress`（活动 JSON 无 type 字段），纯 Lab 课 `progress=0` 会被 `progress<50` 选中并导航进去逐个点 Next 走过每个 Lab——虽不消耗点数/不改数据，但属无谓访问。若已用 `scan_courses.py` 确认某课全 Lab、决定不做，跑推进时加 `--skip-course <id1,id2,...>`，在导航前就排除；参数既接受纯数字 ID，也直接接受 `scan_courses` 输出的 `template:648` / `session:41484246` 带前缀格式（取冒号后数字，无法解析的 token 会打警告）。注意 ID 形态须与当前路径页 href 一致：未报名用 `course_templates/<id>` 的数字、已报名用 `course_sessions/<id>` 的数字。也可只跑 `scan_courses.py`/`dump_path.py` 做只读扫描、完全不推进。
- 🔴 CHECKPOINT：跑完用 `read-acts` 复查进度，向用户报告每个活动的 %.
- **单课 `course_template`（非路径）的视频用 `advance` 效率极低**（实测 `switch` 十几次、`video` 仍 0：它依赖路径活动切换，单课没有这个结构）。此时改用 `complete_videos.py <template_id>` 逐视频导航点 `complete_button`；它内部按活动 href 逐个处理并跳过 Quiz/Lab。判断依据：URL 是 `/paths/<id>` 用 `advance`，是 `/course_templates/<tid>` 单独一门课用 `complete_videos.py`。
- **单课的 Quiz 衔接**：单课的 `quiz-list` 因需要路径 URL 而无效（不是读不到菜单）。改从课程内部活动清单取具体 `quizzes/<qid>` URL 作答——注意顶层 `read-acts` 可能看不到 Quiz（它们藏在子课程里，需进子课/内部菜单），拿到具体 Quiz URL 后直接喂给 `quiz-read` / `quiz_answer_stable.py`，这两个命令吃具体 URL、不依赖路径。

### Phase 3b — 争取通过模式（Quiz 作答）

**Step 1 找出未通过的 Quiz：**

```bash
python3 <skill>/scripts/gca.py quiz-list "<路径URL>"
```

**Step 2 逐个处理**（对每个未完成 quiz）：

```bash
# 读题（--retake 会先点 Retake/Start 进入答题态）
python3 <skill>/scripts/gca.py quiz-read "<quiz URL>" --retake
```

- 输出 `questions`: 每题 `stem` + `opts`（`label`/`type`/`selected`/`disabled`）。
- **作答前先读 `references/page-mechanics.md` 第 6 节**（已沉淀的 GCP 常见考点与多选坑），优先复用已验证经验。
- **Agent 逐题判断正确答案**；经验覆盖不到的再用 WebSearch 查官方文档核实，不要猜。

**Step 3 组装答案 JSON 并作答：**

```json
[
  {"kw": "题干中的一段关键词（小写，用于匹配题目）", "opts": ["要选的选项文本原文", "..."]},
  {"kw": "...", "opts": ["..."]}
]
```

- `kw` 取题干里独特的英文短语（如 `"amount of memory allocated in the heap"`），避免多题混淆。**必须小写且是题干的精确子串**——匹配不到会回退到按下标作答（易错），务必核对。
- `opts` 填选项的 `label` **原文**（精确匹配）；单选填 1 个，多选填全部正确项。若选项文本过长只想匹配部分，可加 `"fuzzy": true` 让 `opts` 按子串匹配。
- 保存到临时文件后：

```bash
python3 <skill>/scripts/gca.py quiz-answer "<quiz URL>" @/tmp/answers.json
```

- 脚本自动：进答题态 → 两轮点选（防异步漏点）→ 点 Submit → 读分数与反馈。
- 🔴 CHECKPOINT：检查返回的 `result` 里 `Your score` 是否 ≥ `Passing score`。没过 → 看 `result` 中的 Correct/Incorrect 反馈和 `feedback_questions`，定位选错的题，修正答案 JSON 后重跑（`quiz-answer` 会自动 Retake）。可无限重试。
- 常见坑：多选题少选一项也能过线但非满分；若要满分，核对每个正确项都在 `opts` 里。
- **Retake 时序坑（实测）**：`quiz-answer` 内置 Retake 只等 2.5s，慢网络下结果页 retake 按钮未渲染 → `prep=NONE` → 在结果页直接提交旧答案（`clicked=[]`, `notfound=[]`），反馈是旧的、不可信。判定信号：返回里 `prep:"NONE"` 且 `clicked:[]`。此时改用**单连接作答脚本** `<skill>/scripts/quiz_answer_stable.py`（思路：一个 CDP 连接内 `goto`→显式点 `ql-button.retake-button`→轮询题目渲染→三轮点选→提交→读反馈，**全程不重复 goto**，避免覆盖 retake 状态）。核心是 goto 一次、retake 后等题目真正渲染再点。**区分**：若 `prep:NONE` 且完全无分数（静默不提交，非旧反馈），是页面停驻结果页，改用 `quiz-read --retake` 先进答题态再作答（见 page-mechanics 16.6）；两种 prep:NONE 成因不同、处理不同。
- **fuzzy 匹配区分大小写**：`opts` 子串必须与选项 label 原文大小写一致（如 `LookML`/`SQL`/`Model Armor`），写成小写会 notfound。
- **结果页精确对错**：`ql-rationale` 的 `correct` 属性——空字符串=Correct，`null`=Incorrect；不要只读文本猜测。

**反馈迭代收敛法（答错题时）：** 目标是**过线不是满分**（实测 8/10 就能过），别为单题死磕。用 `quiz_answer_stable.py` 作答 → 读完整反馈 → 以 `quiz-list` 的 `isComplete` 判是否通过（结果文本数组可能错位，不可靠）→ 按平台反馈文字反推改正错项 → 重 retake；2-3 轮不过就搁置回头再攻，拿不准查官方文档。完整步骤与 LookML/Apigee 实例见 `references/page-mechanics.md` 第 12 节。

**Step 4 收尾复查：**

```bash
python3 <skill>/scripts/gca.py read-acts "<路径URL>"
```

向用户报告进度变化。

### Phase 4 — 权益/GEAR/Lab 前置（用户要"领点数/做 Lab"时）

Lab 必须消耗实验点数（1 点/个），账号点数不足时点"开始实验"只会弹出"本实验费用 1 个点数 / 请输入实验令牌"前置模态。因此做 Lab 前先诊断权益，别在模态框空转。

**Step 1 只读诊断（先做，不改动任何东西）：**

```bash
python3 <skill>/scripts/gca.py entitlement
```

读回三项（注意是嵌套字段）：点数余额 `points.balance`（只认顶栏 `ql-chip`，正文的"35 个点数"是套餐宣传，绝不能当余额）、GEAR 会员 `gear.likelyJoined`、开发者资料公开状态 `developer_profile.profilePublic`；另看 `developer_profile.gearBadgeOnProfile` 复核 GEAR 徽章是否已获。


**Step 2 按诊断结果分支：**

| 诊断 | 判断 | 下一步 |
|---|---|---|
| `balance>0` | 有点数 | 可直接进 Lab：点"开始实验"→ 用面板临时凭据在无痕上下文操作 → 逐项点"检查我的进度"。无痕上下文用同一 CDP 浏览器的 `Target.createBrowserContext`，不另起实例 |
| `balance=null`（未取到 chip / 未登录） | 登录态失效或页面未渲染 | 回 Phase 0 确认登录态，重开订阅页再诊断 |
| `balance=0` + GEAR 未加入 | 免费点数没开通 | 走 Step 3b 官方链路入会 |
| `balance=0` + 观测到"已加入但资料 Private" | 异常态（Public 本应是入会前置） | 用 `entitlement` 复核 `developer_profile.profilePublic` 与徽章；Public 必须在入会**之前**设好（Step 3a → Step 3b），不要想着入会后再补设 |
| `balance=0` + 都到位 | 服务端发放延迟 | 告知用户等几小时~一天；久未到账联系 `gdp-support@google.com`。不购买、不伪造 |

**Step 3a 开发者资料设为 Public（GEAR 前置条件）：**
- 打开 `https://me.developers.google.com/u/me/settings` → Account 区块的 Private/Public 单选（`input[aria-label=Public]`）。
- 必须 `scrollIntoView` + **真实鼠标点击**（JS 赋值不触发 Angular 表单）；切换即自动保存，无单独保存按钮。
- 刷新确认 `profilePublic:true` 再继续。

**Step 3b 官方链路加入 GEAR（关键，避开失效令牌）：**
- 🛑 不要在 skills.google 订阅页（`payments/new`）反复填 GEAR 表单——那个 `/gear/join_gear` 接口可能返回 `invalid_grant: Bad Request`（后端 OAuth 令牌失效），**重登 developers.google.com、Delete all 重连 Google Skills 授权都修不了**，别在此死磕。
- 正解：打开 `https://developers.google.com/program/gear?hl=zh-cn` → 点"成为会员"→ 弹出官方加入表单（走 developers.google.com 自身授权，绕过失效令牌）：
  - 字段：`devsite-profile-location` / `devsite-profile-organization` / `devsite-profile-title` / `profileattribute-First Name` / `profileattribute-Last Name` + "提交"按钮。
  - **坑1**：location 必须真实键盘逐字输入触发 Google 地点建议并点选（直接 `e.value=` 填文本会报"请从列表中选择城市/城镇"）。
  - **坑2**：对话框内容超高，先把内部滚动容器 `scrollTop=scrollHeight` 让"提交"按钮进入视口，再真实点击，否则点在视口外无效。
- 成功标志：显示"您赢得了 Gemini Agent Ready 徽章"。用 `entitlement` 复核 `developer_profile.gearBadgeOnProfile:true`。
- 用户资料（经验档位/城市/角色/单位）若未知，先问用户，不要替其猜。

**Step 4 权益边界（硬）：**
- 不擅自购买点数；令牌/购买需用户明确授权。
- 不伪造 Lab 完成状态；GEAR 加入只用官方按钮，不改后台数据。
- 点数到账是服务端行为，用户侧尽力后如实说明，不反复空转。

**Step 5 伙伴（代理商）专属权益（用户提供伙伴身份/想考证时）：**
- 若用户是 Google Cloud 合作伙伴，有两条专属免费通道，优先于个人付费路径：
  1. **Partner Certification Kickstart (PCK)**：官方页 `https://cloud.google.com/resources/pck-page`。**必须用伙伴企业邮箱注册**（个人邮箱无法访问平台/考试券）；免费含考试券（券资格与组织伙伴等级挂钩）、培训导师、Google Skills for Partners 全量访问。覆盖 ACE/ADP/GWA/PCA/PCD/PCDoE/PDE/PCDE/PMLE/PCNE/PCSE/PSOE 全部路径。
  2. **Google Skills for Partners**（`partner.skills.google`）：伙伴专属课程/续证平台。PCA 续证路径 `/paths/4178`、ACE `/paths/4177`，PDE/CDL 同平台对应路径（确切 ID 未公开，勿编造）。完成平台指定课程/徽章可**免费续证 +1 年**，但**必须在认证到期前最后一年内完成才计数**（提前做无效且不能重做）；当前支持 CDL/ACE/PCA/PDE 及 2026-07 扩展的 GAIL/AGWA/ADP/PCDBE/PCD/PCDE/PCSE/PCNE/PMLE/PSOE，以平台当日显示为准。
- 伙伴计划 2026-01 已由 Partner Advantage 换版为 **Google Cloud Partner Network（GCPN）**：层级 Registered→Select→Premier→Diamond，旧"Premier 需 12 证"口径作废；新增 Competency（21 类，与层级解耦）。认证仍是从业者能力的硬通货（PCA/PDE 覆盖面最广）。具体门槛以用户自己 Partner Network Hub 的 Requirements 为准，不要把媒体披露的 ACV/认证数字当官方门槛。
- **考试券 vs 续证互斥**：PCK 考试券明确不能用于续证（续证走 Partner Recertification Program，失效前申请 100% 折扣）。考试券是"完成培训后"才发且有有效期，所以用户"先不考、留进度以后拿券"要保留的是**尚未报名的 PCK 路径**（报名即开始 10 周倒计时），不要提前刷完拿券再拖着作废。完整规则与时效提醒见 `references/page-mechanics.md` 第 15 节。
- **查账号证书/续证状态**：`gca.py recert`（只读，见脚本速查）。它会列出到期日、是否进入续证窗口、90 天内到期、续证路径。
- 用户决定是否考证/用哪个通道由用户拍板；本技能只做只读诊断与导航，不代报名、不代考、不填伙伴后台资料。

### Phase 5 — Google Skillshop 正式 Credential 考试（本人账号 + 明确知情授权）

> **与课程内 Quiz 是两个完全不同的平台和机制**：本节对象是 Intellum/Exceed LMS（`skillshop.exceedlms.com`）的正式 Credential 结业考试——80% 及格、有时间限制、提交后不可修改、失败需等 24 小时、中途关闭算自动失败。Phase 3b 的"无限 Retake、可看反馈"经验**禁止**套用。完整机制、差异对比与联网核实方法见 `references/page-mechanics.md` 第 19 节。

**前置硬门槛（五项全部满足才进入，缺一项即拒绝）：**
1. 用户使用**自己的**账号、本人在场、明确知情授权拿下这场考试。
2. 用户已知晓并接受规则：80% 及格、时限、提交不可改、失败等 24 小时、中途关闭算自动失败。
3. 不为他人代考，不使用泄题/灰产答案，不绕过监考，不伪造身份。
4. 每题都联网核实 Google 官方文档，不凭记忆、不猜。
5. 关键步骤（登录密码、逐题确认、最终提交）全部由用户本人完成。

**Step 1 登录须用户本人配合：**
- 未登录时页面显示"需要验证，在下方登录以解锁附加内容"；登录链路固定为 `/authentication/google_authentication` → Google OAuth 账号选择器 → 密码页。
- 🛑 STOP：走到**密码页立即停下**，明确提示"请在浏览器里由本人输入账号密码并完成二步验证，完成后告诉我"。Agent 绝不代输密码、绝不读取或记录密码、绝不尝试绕过登录。
- 沿用 Phase 0 探测到的既有 CDP/MCP 浏览器入口，在用户当前标签页内操作；不为考试单独启动或重启浏览器（重启会中断进行中的考试）。
- 用户回复"已登录"后，复用 `gca.py` 的 `client`/`goto`/`evj` 读取页面（本节**不新增脚本**）：
```bash
cd <skill>/scripts && python3 -c "
import gca
c = gca.client()
gca.goto(c, '<考试URL>', wait=3.0)
print(gca.evj(c, 'document.body.innerText', ''))
"
```
- 确认已进入答题页、能看到第一题题干与选项，再继续 Step 2。

**Step 2 题库逐题联网核实（每题必做）：**
- 用上面的 `goto` + `evj` 读取当前题的题干与选项原文（每次翻题后都要重新读，题干/选项顺序可能变化）。
- **每一题**都用 WebSearch + WebFetch 到 Google 官方技术文档（`cloud.google.com`、`developers.google.com`）核实，以官方文档原文为唯一判据。
- `en.certificationanswers.com` 等第三方站**只有题目、没有可靠答案**（标题党），仅用于定位考点关键词，**禁止当作答案来源**。
- 为每题记录"题干关键词 → 官方文档 URL → 结论"写入临时笔记，供 Step 4 复查。

**Step 3 逐题交互确认：**
- 🛑 STOP：每得出一题的核实结论，把"题干摘要 + 候选选项 + 官方文档依据"回报用户，等用户确认或修改后再录入并翻到下一题。
- 用户说"按你的判断来"时，也要先把全部题目与依据逐题列明，再一次性取得明确确认。
- 依据不足或用户与核实结论有分歧的题，如实标注"依据不足"，由用户拍板，不擅自替用户决定。

**Step 4 提交前一题三查（不可跳过）：**
- 提交前对**每一题**做三查：①当前页面题干关键词与核实记录一致（题序/选项可能随机，按文本不按位置）；②页面读回的选中项（`checked` / `aria-checked`）与核实结论一致；③官方文档 URL 可访问、结论未变。
- 🔴 CHECKPOINT：三查全部通过、且用户明确回复"确认提交"后，才点击提交。提交后**不可修改**，禁止再改答案或重复点提交。
- 提交后只读回结果并报告。未过则提示用户"需等待 24 小时才能重考"，不反复空转、不立即重试、不关闭标签页。

**Step 5 考试通过 ≠ 证书到手（关键，务必补齐）：**
- 实测：只通过 Assessment **不会**发证书——"我的学习"里课程仍是"路径/进行中"，路径页无"查看奖励"。Credential 要求**整条路径全部活动完成**才发证书。
- 考完后回路径页 `/student/path/<pid>` 查每个 activity 的完成标记（`li.outerHTML` 含 `completed`）。若有未完成的学习模块（阅读型 content），逐个 goto 并**滚动到底部**（`window.scrollTo(0, scrollHeight)` + 内部容器 scrollTop，重复 3-4 次、每次停 1s）即自动标记完成——见 page-mechanics 19.10。
- 全部活动 completed 后，路径页顶部出现"通过：日期 / 到期日期 / 查看奖励"；点"查看奖励"弹窗显示证书（完成人/完成ID/到期日/打印）。**必须走到这步才算真正拿证**，并回报用户证书信息。
- 🔴 这正是 L2.5"局部≠整体"的典型：L0 = 证书到手，Assessment 通过只是 L1。未拿到证书弹窗前，总账 L0 保持 ⬜，绝不向用户说"考试完全结束/搞定了"。

---

## L4: 失败模式与回退（Fallback）

| 症状 | 原因 | 处理 |
|---|---|---|
| **把局部完成当成整体结束**（考试过了就说"结束"、Quiz 过了就说"搞定"，用户追问才发现漏了证书/模块/其他课） | 未在任务开始建 L2.5 总账，凭单一权威信号就宣告完成 | 立即按 L2.5 做终局核验 DoD：回读路径页/`quiz-list`/证书弹窗刷新总账，列出剩余项再报告；L0 未全 ✅ 前禁说"完成/结束"，只能报"当前 X/Y，剩余…" |
| 入口探测不到任何可用工具 | 会话未加载 MCP、本机也没有调试浏览器 | 按 Phase 0 决策矩阵走自建 CDP；或先用工具搜索再探一次 |
| 本机有浏览器技能/MCP 配置，但当前会话没有对应工具 | 配置存在 ≠ 本会话可用 | 不要调用不存在的工具；用已连通的 CDP 或自建 |
| 默认端口 9333 不通但其他端口通 | 浏览器被别的入口启动在 9222/9334 等 | gca.py 会自动复用并提示；确认标签页是目标即可继续，不要另起实例 |
| `browser-check` 失败 | 调试浏览器没开/端口变了 | 走 Phase 0 重新探测；确认后台任务常驻；换端口时保持全程一致 |
| `read-acts` 返回 `NO_MENU` / 要求登录 | 登录态没复制过来 | 确认复制了 `Default/Cookies`（非 Network 下），必要时让用户重登一次独立 profile |
| `quiz-read` 返回 `question_count:0` | 页面未渲染完 / 处于结果页 / CDP 直接返回了 Python 数组而 `evj` 误当 JSON 字符串解析（已修） | 加 `--retake`；等几秒重试；仍为 0 则读 `ql-quiz[quizversion]` 兜底；**避免连续多次 Retake** |
| `quiz-list` 返回 0 但课程里明显有未完成 Quiz | 用了 `/course_sessions/<id>` 根 URL，那里没有 `ql-contents-menu`（已修为用路径活动 href） | 用路径页活动里的具体 href 进入课程再扫描 |
| `quiz-answer` 全没点上 / 多选提交无效 | 点 `ql-checkbox`/`md-checkbox` host 不生效，或点击后立刻提交时状态未写回（已修：点内部 input + 三轮间隔） | 先确认题目渲染；多选尤其要按文本定位内部 input；提交前留 1s 稳定窗口 |
| `quiz-answer` 返回 `prep:NONE` 且无分数、无报错（静默不提交） | 页面停在结果页，未进答题态 | 先 `quiz-read <url> --retake` 确认返回题目，再 `quiz-answer`；逐个处理不要批量 for 连跑（见 page-mechanics 16.6） |
| **多选点选"点上却答错"/checkedCount 异常多于答案项**（实测坑） | `md-radio`/`md-checkbox` 的 **host.click() 会误触发相邻选项**，造成选中偏移（点 A 却选中 C）；再叠加 input.click() 更乱 | **只点内部 input**（`el.focus()` + `shadowRoot.querySelector('input').click()`），绝不点 host；提交前读回每个选项的 `checked`/`aria-checked` 与目标逐一比对，不符再纠偏。用 `quiz_solve.py`；**但 `quiz_solve.py` 单选 VERIFY 有已知错位 bug（`submit:DISABLED`），遇到就改用 `gca.py quiz-answer`（实测稳定）** |
| retake 后读到"上次残留答案"（选项已 selected）导致反复不过 | `quiz-read --retake` 的内置 retake 慢网络下未生效，读到旧答卷 | 显式轮询等 `ql-button.retake-button` 出现再点、等 radio 全部 `disabled` 消失且未选中才算新题态；`quiz_solve.py read` 已实现 |
| 得分没过 | 答案选错/漏选 | 读 `result` 的 Correct/Incorrect 反馈修正；可无限 Retake；**2-3 轮不过就搁置回头再攻** |
| 提交后只有 "Passing score: X%"、无 "Your score"，判为没过（**假顽固**） | **结果页渲染慢（约 4 秒）**，脚本固定等 3 秒就读，误判未过（686272 曾因此被冤枉搁置 4 轮，实则答案一直对，最终 100%） | 提交后**每秒轮询一次、最多 10 次**等 retake-button 或 "Congratulations"/"Your score" 出现再判定；作答前先 CLEAR 残留选中、VERIFY 连续 3 轮 `fixedCount=0` 再 Submit。详见 page-mechanics 第 18 节 |
| html_bundle 类内容包访问后不标记完成 | 纯 goto 访问不触发完成，需真实阅读停留（机制未完全摸清） | 属内容浏览型边界，不必死磕；文档 `documents/*` 则 goto 访问即自动完成 |
| 课程进度卡在 80-90% | 剩 Lab/Quiz 跳过部分 | 如实告知：Lab 无法代做；Quiz 可用 Phase 3b 补过 |
| 纯 Lab 课 0% | 无视频可标记，需真实完成 Lab | 平台机制；先查是否有实验点数/令牌，无则停下询问，不要反复空转 |
| 点"开始实验"弹出"本实验费用 X 个点数 / 请输入实验令牌" | 账号无可用实验点数或订阅 | 先 `entitlement` 诊断；无点数按 Phase 4 走 GEAR 入会；绝不擅自购买，也不伪造完成 |
| 订阅页填 GEAR 表单后回到原页、点数仍 0，响应体有 `invalid_grant: Bad Request` | skills.google 后端 OAuth 令牌失效，重登/重连都修不了 | 别死磕订阅页；改走 `developers.google.com/program/gear` 官方链路（Phase 4 Step 3b） |
| GEAR 官方表单报"请从列表中选择城市/城镇" | 城市字段直接赋值，未走地点建议 | 真实键盘输入触发 Google 地点建议并点选，`place_id` 才会填上 |
| GEAR 表单"提交"点了没反应 | 对话框超高，按钮在视口外 | 先把内部滚动容器 `scrollTop=scrollHeight`，再真实点击提交 |
| 已加入 GEAR 但 skills.google 点数仍 0 | 服务端权益发放延迟 | `entitlement` 复核徽章是否已获；告知等待，久未到账联系 gdp-support@google.com；不购买、不伪造 |
| `entitlement` 里 balance 对不上（读到 35） | 误把正文套餐宣传数字当余额 | 只认顶栏 `ql-chip` 的余额（脚本已修正） |
| 用户给的是正式认证考试（Exam/Credential）链接 | 需按对象与授权分流 | 本人账号 + 本人在场 + 明确知情授权 + 每题联网核实 + 关键步骤本人确认 → 走 Phase 5；替他人代考或使用灰产 → 拒绝，说明只做课程内 Quiz 与本人授权的考试 |
| Skillshop 考试卡在 Google 密码页 | 登录必须本人输入，Agent 不能代输 | 🛑 STOP 提示用户本人输入账号密码并完成二步验证，完成后再继续；不读取、不记录、不绕过 |
| Skillshop 考试提交后未过 | 一次机会机制，失败需等 24 小时，提交不可改 | 告知用户 24 小时重考窗口，不立即重试、不反复空转 |
| Skillshop 考试中途被关闭或切走标签页 | 中途关闭算自动失败 | 考试期间不导航离开、不重启浏览器；已中断则如实报告，按 24 小时规则重考 |
| 单课 `course_template` 用 `advance` 视频数为 0、`switch` 空转 | `advance` 靠路径活动切换，单课无此结构 | 改用 `complete_videos.py <template_id>` 逐视频点完成 |
| 课程 badge/完成凭证显示 `isLocked:true, disabled:true` | 依赖 Lab 完成，Lab 没做所以锁定 | 平台机制，如实告知；Lab 做完才会解锁，不伪造领取 |
| `read-acts` 报有 survey，但打开 `course_surveys/0` 跳首页/"访问遭拒" | 模板课的 survey 挂在实际 `course_sessions/<sid>` 下，不在 `course_templates/<tid>` | 从课程内部菜单读真实 href；读不到就判定无可填项，别硬试 |
| Quiz 反馈数组条数少于题数/疑似错位 | 新课程结果页只在题干下显示逐题 Correct，分数不进文本 | 以 `quiz-list` 的 `isComplete` 判过线；反馈文字只用于纠错方向，不当分数 |
| 自选课程挑到 `Quiz=0` 的纯 Lab 课 | 没按性价比评估就开做 | `read-acts` 先分类计数，跳过纯 Lab 课，选 Quiz 多的先做 |
| 不准备做的纯 Lab 课，`advance` 还是访问了、逐个点 Next 走过每个 Lab | 路径页活动 JSON 无 type 字段，纯 Lab 课 `progress=0` 被 `progress<50` 选中 | 先 `scan_courses.py` 确认全 Lab，再用 `advance --skip-course <id,...>` 导航前排除；只读扫描用 scan/dump 不推进 |

---

## L5: 反例黑名单（禁止）

1. ❌ 反复启动/重启调试浏览器 → 弹窗关不掉。✅ 浏览器只启动一次（各命令独立短连接是安全的）。
2. ❌ 按选项下标/位置点选 → 重排后全错。✅ 按题干关键词 + 选项文本。
3. ❌ 把 Quiz 的 Next 当提交 → 只是翻题。✅ 用 submit-button。
4. ❌ 遇到进度不满就伪造请求改状态。✅ 只用平台按钮，如实报告机制限制。
5. ❌ 替他人参加认证考试、使用泄题灰产答案、绕过监考或伪造身份。✅ 只做课程内 Quiz；仅当"本人账号 + 本人在场 + 明确知情授权 + 每题联网核实 + 关键步骤本人确认"全部满足时，才按 Phase 5 辅助 Skillshop Credential 考试，否则一律拒绝。
6. ❌ 不问模式就跳过所有 Quiz（用户可能想考过）。✅ Phase 2 明确确认。
7. ❌ 读不到题就反复狂点 Retake。✅ 等待渲染一次，异常就停下报告。
8. ❌ 把 Lab 课 0% 说成脚本坏了。✅ 说明是平台机制。
9. ❌ 僵化只用某一个浏览器入口；或看到 `mcp.json` 有配置就以为当前会话能用。✅ 先 `browser-detect`，以实际连通和当前工具清单为准。
10. ❌ 发现别的调试端口就重启自己的浏览器。✅ 复用已开放实例，全程只启动一次。
11. ❌ 在 skills.google 订阅页反复提交 GEAR 表单死磕 `invalid_grant`（重登/重连都修不了）。✅ 改走 `developers.google.com/program/gear` 官方链路。
12. ❌ 把正文"35 个点数"套餐宣传当余额，或擅自购买点数、伪造 Lab 完成。✅ 只认 `ql-chip` 余额，权益边界见 Phase 4 Step 4。
13. ❌ 城市字段直接赋值、或没滚动就让"提交"点在视口外。✅ 真实键盘输入选地点建议 + 滚动对话框后再点。
14. ❌ 对单门 `course_template` 用 `advance` 空转、视频数 0 还反复重试。✅ 改用 `complete_videos.py` 逐个点完成。
15. ❌ 为凑满分对一道错题反复 retake 死磕，或凭文本猜分数。✅ 目标是过线，`quiz-list` 确认 complete 即可；反馈文字只用于纠错方向。
16. ❌ 把受 Lab 限制而 `isLocked` 的 badge/survey 说成脚本坏了、或想办法绕过领取。✅ 如实说明是平台机制，Lab 完成才会解锁。
17. ❌ 自主选课时挑到 `Quiz=0` 的纯 Lab 课白费功夫。✅ 先 `read-acts` 分类计数，按"Quiz 多、Lab 少、未完成多"排序。
18. ❌ 只完成局部就宣布"结束/搞定/拿下了"（考试过≠证书到手、单 Quiz 过≠全课完成），等用户追问才发现漏项。✅ 按 L2.5：先建 L0/L1/L2 总账，宣告前强制 DoD 终局核验（回读权威字段 + 列剩余项），L0 未全 ✅ 只能报"X/Y，剩余…"。

---

## 脚本命令速查

```
<skill>/scripts/gca.py browser-detect                # 自动探测入口（CDP/MCP/技能，只读）
<skill>/scripts/gca.py browser-check                 # 检查连通
<skill>/scripts/gca.py browser-start-info            # 浏览器启动+登录态说明（fallback）
<skill>/scripts/gca.py entitlement                   # 只读诊断：点数/GEAR会员/资料公开状态
<skill>/scripts/gca.py recert                        # 一句话查证书/续证：到期日/可续/快到期/续证路径
<skill>/scripts/gca.py read-acts <url>               # 活动清单/进度
<skill>/scripts/gca.py quiz-list <url>               # 未完成 Quiz 清单
<skill>/scripts/gca.py quiz-read <url> [--retake]    # 读题（供 Agent 判断）
<skill>/scripts/gca.py quiz-answer <url> @answers.json # 作答+提交+读分（快，但慢网络有 retake 时序坑）
<skill>/scripts/quiz_answer_stable.py <url> @answers.json # 稳定作答：单连接 goto→retake→点选→提交（retake 坑时用）
<skill>/scripts/quiz_answer_inplace.py <url> @answers.json # 读题后不 retake、当前答题态直接作答（选项会变的课用；先 gca.py quiz-read --retake 读题）
<skill>/scripts/quiz_answer_paged.py <url> @answers.json # 分页式老课（Previous/Next 翻页）作答
<skill>/scripts/quiz_solve.py <url> read               # 【推荐】稳健读题：显式retake→等radio可点且未选中→打印当前题目原文
<skill>/scripts/quiz_solve.py <url> solve @answers.json # 【推荐】稳健作答：复用当前答题态→只点内部input(focus+input.click)→读回checked验证→提交
<skill>/scripts/submit_survey.py <survey_url>            # 提交课程满意度调查（全选正面项）
<skill>/scripts/complete_videos.py <template_id>     # 单课模板批量标记视频"已完成"
<skill>/scripts/scan_courses.py [path_id ...]        # 批量扫描课程构成，挑零Lab有Quiz的课（自主选课用）
<skill>/scripts/dump_path.py <path_id>               # 转储路径内各子课活动清单，找顶层看不到的Quiz
<skill>/scripts/gca.py advance <url> [steps] [--skip-course id,id] # 最快模式推进；纯Lab课按ID导航前排除
```
所有子命令均支持 `--port N`（或全局设环境变量 `GCA_PORT=N`）；独立脚本（complete_videos / scan_courses / dump_path / quiz_answer_* / submit_survey）也都读 `GCA_PORT` 或接受 `--port`。`complete_videos.py` 用于 `course_templates` 单课（`advance` 对单课视频效率低），路径模式仍用 `advance`。

## 参考资料

- `references/page-mechanics.md`：页面 DOM 选择器、登录态复制细节、多选作答坑、GCP 答题经验、Lab/GEAR/点数机制、单课推进与选课、反馈迭代收敛法、本轮战绩、伙伴专属认证资源与选课调研。Quiz 作答前必读第 6 节及 Phase 3b 的"反馈迭代收敛法"；做 Lab/领点数前必读第 9、10 节；单课/自主选课读第 11 节；答错题纠参见第 12 节；战报参考第 13 节；代理商认证与选课读第 14 节；续证规则、考试券策略、真实证书状态与时效性核查读第 15 节；Skillshop 正式 Credential 考试（Phase 5）必读第 19 节。

依赖：`gca.py` 的批量逻辑复用 `browser-automation-cdp` 技能的 `cdp.py`（路径 `~/.workbuddy/skills/browser-automation-cdp/scripts`），该技能须已安装。浏览器入口不绑定：由 `browser-detect` 自动探测并优先复用现有 CDP 端口或当前会话的浏览器 MCP，只有都不可用才走 `browser-start-info` 自建 profile。
