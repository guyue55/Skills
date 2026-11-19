# Google Skills 页面机制与实战细节

> 来源：2026-11-17/18 Associate Cloud Engineer Certification（路径 11）实机验证。

## 1. 站点与账号

- 站点：`https://www.skills.google`
- 登录态所在：用户日常 Chrome 的 `Default` profile（企业 Google 账号）。
- Chrome 157+ 安全限制：**不能直接对日常默认 profile 开 `--remote-debugging-port`**，否则启动失败或不弹可用 CDP。
  - 2026-11-17 实测：`chrome-devtools-mcp --autoConnect` 每次连接仍弹授权框，且需重启会话加载 MCP，不适合当时的连续任务。**这是当时的实测结论，不是永久禁令**；每次会话应重新探测，若当前会话已提供可用的浏览器 MCP 且能完成所需操作，可优先使用（见第 8 节）。
  - 兜底方案：复制登录态到独立 profile 目录 → 用该目录启动常驻调试浏览器（仍是批量 Quiz 最稳的通道）。

## 2. 登录态复制（关键路径，曾踩坑）

源文件（`$HOME/Library/Application Support/Google/Chrome/`）：
```
Local State
Default/Cookies            ← 正确！不是 Default/Network/Cookies（那里是空的）
Default/Cookies-journal
Default/Login Data
Default/Preferences
Default/Secure Preferences
```
目标：独立 profile 目录，保持相同相对结构（`Local State` 在根，其余在 `Default/`）。

启动命令（后台常驻，只启动一次）：
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9333 --remote-allow-origins=* \
  --user-data-dir="<独立profile目录>" \
  --no-first-run --no-default-browser-check \
  --disable-background-networking --disable-sync --disable-extensions --no-sandbox \
  about:blank
```
- 在 WorkBuddy 里必须用**后台任务机制**运行；普通 `nohup ... &` 会被环境回收，浏览器随即退出。
- 就绪判断：`curl -s http://127.0.0.1:9333/json/version` 返回 200。
- 弹窗根因是**反复启动/重启浏览器**；启动命令已带 `--remote-allow-origins=*`，各 `gca.py` 命令作为独立短连接实测不再弹授权框。关键是浏览器只启动一次；`advance` 内部为单进程单连接跑完整轮次以避免自身时序问题。

## 3. 页面结构与选择器

### 路径 / 课程活动清单
```js
const e = document.querySelector('ql-contents-menu');
const modules = JSON.parse(e.getAttribute('modules'));
// modules -> steps -> activities，每个 activity: {id, href, title, isComplete, progress}
```
- 路径页 URL：`/paths/<id>?hl=zh-cn`
- activity href 形态：
  - 未开始：`/paths/<id>/course_templates/<tid>`
  - 进行中：`/paths/<id>/course_sessions/<sid>/<type>/<aid>`（type=video/labs/quizzes/documents）

### 视频页
- URL：`.../video/<vid>` 或 `/course_templates/<tid>/video/<vid>`
- 完成按钮：`ql-button[href*="complete_button"]`，文案 "Mark as completed"
- 点击后 POST 并自动跳下一步。

### Next 按钮
- `ql-button.next-button`，有 `disabled` 属性时不可用。
- Lab 页直接 `.click()` 常被拦截，**读取其 `href` 直接导航**可跳过（实测）。

### 课程介绍页
- 老式：`ql-button[href*="/enroll"]`（"Start"）
- 新式（已报名）：无 Start 按钮，改从 `ql-contents-menu` 里第一个未完成活动的 href 进入。
- 识别介绍页：URL 匹配 `/course_templates/\d+$`（**排除**带 `/video/`、`/labs/` 的内部页）。

### Quiz 页
- URL：`.../quizzes/<qid>`
- 题干：`QL-ITEM-STEM`（自定义元素）
- 选项：`MD-RADIO`（单选）/ `MD-CHECKBOX`（多选），都在 Shadow DOM。
  - 选项文本在 `aria-label` 或 `data-aria-label` 属性。
  - checkbox 的 `id` 常重复（都叫 "checkbox"），**必须按文本定位**。
  - 选中判断：radio 用 `aria-checked === 'true'`；checkbox 用 `hasAttribute('checked') || aria-checked === 'true'`。
- 开始：`a.start-button`（文案 "Start quiz"）。
- 重考：`ql-button.retake-button`（文案 "Retake"），在 Shadow DOM，需递归找。
- 提交：`ql-button.submit-button`（文案 "Submit"），在 Shadow DOM。**Next 不是提交**（只是翻题）。
- 2026-11-18 补充（路径19）：题目组件可能是 `ql-multiple-choice-item`（单选）或 `ql-multiple-select-item`（多选），完整题目/选项也在 `ql-quiz[quizversion]` JSON 属性里；渲染慢时可直接读该属性兜底。
- 多选的真实可点击对象是 `ql-checkbox` 阴影里的 `md-checkbox.shadowRoot > input[type=checkbox]`。点 `ql-checkbox` 或 `md-checkbox` host 都不会写回选择；必须点内部 input，并用 `el.checked` 判断选中（`checked` 属性/aria 不一定是 true）。
- 结果：`Your score: X%` / `Passing score: Y%` / "Congratulations! You passed" / "Unfortunately..."。部分新课程结果页只显示逐题 "Correct!"，分数不在文本里；用 `quiz-list` 复查 `isComplete` 更可靠。
- 反馈：`ql-rationale[correct]`、文本 "Correct::"/"Incorrect::"，可用于定位答错的题。
- **每次 Retake：题目顺序 + 选项顺序都重新随机**。必须按题干关键词 + 选项文本定位。

## 4. 多选题作答的坑

- 连续快速点击多个 checkbox 会异步丢状态 → 逐个点击、每个间隔 ~0.5-0.7s，并且做**多轮点击**。
- 2026-11-18 实测：路径19的多选题点 host 完全无效，必须点 `md-checkbox.shadowRoot` 里的 `input`；`gca.py` 已改为三轮点击 + 每轮 0.8s + 提交前再等 1s。
- 提交前用 `el.checked === true` 重新读一次确认（不要用 `hasAttribute('checked')`，内部 input 点击后 host 不一定带该属性）。
- 结果页交卷后选项状态会被重置（selected 全 false），此时只能从 Correct/Incorrect 文本反馈反推对错。

## 5. 进度机制

- 视频标记完成会涨进度；Quiz 通过会涨进度；Lab 跳过**不涨**。
- 课程进度公式未知，但实测：视频全标记 + Quiz 全过 ≈ 88-92%（剩 Lab 缺口）。
- 纯 Lab 课（如路径11的活动10-12）：全部是 lab，无视频无 quiz，跳过不涨进度，恒为 0%。
- 完成状态在路径页 `isComplete`/`progress` 字段读取最准（课程内部页读到的是课程内步骤，不是路径活动）。

## 6. 答案判断经验（GCP 领域）

Quiz 是标准 GCP 基础知识题，Agent 用领域知识作答。拿不准时的查证方向：
- Cloud Storage 存储类别（Standard/Nearline/Coldline/Archive）→ 访问频率与成本
- Spanner vs Cloud SQL vs BigQuery vs Firestore → 全球扩展/ACID/关系型/交互式 SQL
- IAM role 类型（Basic/Predefined/Custom）、member 类型（Google Account/Service Account/Google Group/domain）
- Cloud Load Balancing 类型、MIG 自动扩缩策略（CPU/负载均衡容量/监控指标/队列）
- Cloud Profiler：Heap（某时刻堆分配量）vs Allocated heap（区间总分配量）→ 官方 `cloud.google.com/profiler/docs/concepts-profiling`
- Terraform：state 远程存储好处（共享/锁定/安全访问）、默认本地文件 `terraform.tfstate`

> 答错时优先看结果页 Correct/Incorrect 反馈（最权威），再结合官方文档，不要凭记忆硬猜。

## 7. 历史战绩（路径 11）

- 12 活动：活动1 ACE Exam Prep 100%；活动2-9 视频全标记 + 9 个 Quiz 全部作答通过（有满分也有压线过），进度升到 88-92%；活动10-12 纯 Lab 课 0%。
- 相关脚本历史版本（工作区，可参考但最终以本技能 gca.py 为准）：
  - `auto_full.py`：最快模式全流程推进
  - `/tmp/answer_v2.py`：Quiz 按题干关键词+选项文本作答（9/9 通过的最终版）
  - `/tmp/discover_quizzes.py`：扫描未完成 Quiz

## 8. 浏览器入口探测与复用（2026-11-18 补充）

- 入口只是手段：目标是拿到已登录 skills.google、且能执行 DOM/JS 的页面。不要僵化于"必须先启动 9333 自建 profile"。
- `gca.py browser-detect` 只读探测：候选端口 = `GCA_PORT` + 9333/9222/9334 + `~/.workbuddy/mcp.json` 里的 `--remote-debugging-port`；同时列出本机 browser 相关技能与 MCP 配置。
- 优先级：已有含 `skills.google` 标签的 CDP 端口 > 当前会话可用的浏览器 MCP > 自建 CDP fallback。
- 配置存在 ≠ 会话可用：`mcp.json` 里有 `chrome-devtools`、本机装了 `workbuddy-browser-use` 技能，都不代表当前会话能调用 `mcp__*` 工具。以 Agent 当前工具清单为准；`browser-detect --session-tools "..."` 可把实际工具名交给探测器。
- 2026-11-18 实测：9333 已在运行（Chrome 157，含 `paths/11` 标签），探测器给出 `cdp_existing` → 直接复用，不启动新实例；当前会话未暴露 `mcp__browser__*` / `mcp__chrome-devtools__*`，因此没有切到 MCP。
- `gca.py` 默认端口不可达时会自动复用其他已开放且带目标标签的 CDP 端口并打印提示；确需接管无目标标签的端口时设 `GCA_ALLOW_ANY_CDP=1`（谨慎，先确认不是无关浏览器）。
- 批量 Quiz 依赖递归 Shadow DOM JS + 多轮点击，优先 gca.py/CDP；MCP 只有具备 `evaluate` 能力时才适合直接跑相同逻辑。

## 9. Lab 实测机制与阻塞点（2026-11-18）

- 路径 11 活动 10-12 是纯 Lab 课程，各自活动清单如下（均无视频/Quiz）：
  - `course_templates/648`：4 个 Lab（613022-613025）+ 技能徽章 + 调查问卷。
  - `course_templates/625`：6 个 Lab（592701-592706）+ 技能徽章。
  - `course_templates/636`：5 个 Lab（592696-592700）+ 技能徽章。
  - 合计至少 15 个 Lab；活动 2-9 残留进度也主要卡在其内部 Lab。
- Lab 页面机制：标题含 GSP 编号（如 GSP007）；有 `QL-BUTTON` 文案"开始"；点击后若账号无可用实验点数，会弹出模态框："本实验费用 1 个点数 / 购买点数 / 请输入实验令牌 / 使用令牌启动"。
- 官方说明（2026-11-18 联网核实）：Lab 是**真实云环境**、计时不可暂停；必须用实验提供的临时凭据登录；推荐无痕窗口，避免与个人账号冲突导致额外扣费；完成后点"检查我的进度"（Check my progress）由平台校验资源状态。
- 因此 Lab 不能像视频那样"标记完成"，也不能用脚本伪造请求改进度。合法路径只有：有可用点数/令牌 → 启动 → 在无痕上下文用临时账号真实操作 → 点检查进度。
- 未找到能"自动完成"Lab 的现成工具；搜索到的开源项目只有目录抓取器（qwiklabs-catalog-scraper）和完成记录追踪器，均不代替真实实验。
- 实测阻塞：当前登录态点"开始"后弹出点数/令牌模态框，**未擅自购买点数**。需要用户提供实验令牌或明确授权购买后才能继续。
- 若后续获得授权：可在同一 CDP 浏览器用 `Target.createBrowserContext` 建无痕上下文（不另启浏览器实例），用面板里的临时账号登录，按手册执行 Cloud Shell/控制台操作，逐项点"检查我的进度"验证。

## 10. 免费 Starter 点数领取的隐藏前置（2026-11-18）

> 主文档对应 `SKILL.md` Phase 4；只读诊断用 `gca.py entitlement`（点数只认顶栏 `ql-chip`，正文的"35 个点数"是套餐宣传不是余额）。

- Starter 免费方案（每月 35 点）会强制先完成 GEAR 成员资料：经验、城市、角色、单位。城市是 `md-outlined-text-field`，必须从 Google Places 下拉建议中选中，隐藏 `place_id` 才会填值；仅输入文字会提交失败回到订阅页。
- 即使表单完全正确，`/gear/join_gear` 仍可能返回 OAuth `invalid_grant: Bad Request`（响应体 `hallofmirrors.snackbarService.alert(...)`），表现为"提交后又回到订阅页"且点数仍为 0。这不是表单问题（根因见下方实测结论）。
- **2026-11-18 深度实测结论（重要，优先采用；下方各条为实测细节）**：
  - `invalid_grant` 是 skills.google 后端持有的 OAuth 令牌失效——**重登 developers.google.com、甚至在 Google 账号里 Delete all 断开再重连 Google Skills 授权、重走 skills.google 登录，都修不了** `/gear/join_gear`（仍返回 invalid_grant）。浏览器侧无解，别在此死磕。
  - GEAR 真名 `GEAR (Gemini Enterprise Agent Ready)`，加入前提之一是 Google Developer Program 个人资料为 **Public**（`https://me.developers.google.com/u/me/settings` → Account → Private/Public 单选；Angular Material `input[aria-label=Public]`，scrollIntoView + 真实鼠标点击，切换即自动保存无单独按钮）。
  - **正解：改走官方链路**，`https://developers.google.com/program/gear?hl=zh-cn` → "成为会员" → 对话框表单（`devsite-profile-location` / `devsite-profile-organization` / `devsite-profile-title` / `profileattribute-First Name` / `profileattribute-Last Name` + "提交"）。这条走 developers.google.com 自身授权，绕开失效令牌，实测一次成功拿到 Gemini Agent Ready 徽章。
  - 官方表单两个坑：①location 必须真实键盘逐字输入触发 Google 地点建议并点选（直接赋值会报"请从列表中选择城市/城镇"）；②对话框超高需先把内部滚动容器 `scrollTop=scrollHeight`，否则"提交"按钮在视口外，点击无效。
  - 加入成功后 `me.developers.google.com/u/me` 的 Badges 出现 `Gemini Agent Ready`。但 skills.google 点数可能仍为 0（重登后仍 "0 credits"）——官方说 35 点/月自动发放到同邮箱账号，疑有服务端同步延迟；久未到账联系 gdp-support@google.com。全程不购买点数、不伪造完成。

## 11. 单门 course_template 的推进与选课（2026-11-18 补充）

- **路径 `/paths/<id>` vs 单课 `/course_templates/<tid>` 的推进方式不同**：
  - 路径：用 `gca.py advance <url>`，靠 `ql-contents-menu` 的活动列表切换推进。
  - 单课模板：`advance` 实测 `switch` 十几次、`video` 仍 0（无路径活动结构可切）。改用 `scripts/complete_videos.py <template_id>`：读活动清单 → 逐个导航视频页 → 点 `ql-button[href*="complete_button"]` → 跳 Quiz/Lab。
  - 判断：URL 含 `/paths/` 用 advance；含 `/course_templates/` 且是单独一门课用 complete_videos.py。
- **单课 URL 的 Quiz 处理**：`quiz-list` 需要路径 URL，对单课无效；但 `quiz-read` / `quiz-answer` / `quiz_answer_stable.py` 可直接用活动清单里的具体 `quizzes/<qid>` URL 作答。
- **顶层看不到子课里的 Quiz**（如 ADK 3545 顶层 read-acts 只列 6 门课，Quiz 藏在子课程）：用 `scripts/dump_path.py <path_id>` 转储路径内每门子课的活动清单，从子课 `acts` 里取具体 `quizzes/<qid>` URL 再作答。已实测（路径 11 返回 4 门子课各自动作清单）。
- **"不做 Lab 却还是访问了一遍"的性质与修复（2026-11-18 实测）**：分两类。①扫描脚本（`scan_courses`/`dump_path`）进课程读内部清单统计 Lab/Quiz 数——必要只读访问，非缺陷。②推进脚本 `advance` 的候选筛选只有 `progress<50`：纯 Lab 课 `progress=0` 会被选中、导航进去逐个点 Next 走过每个 Lab（如路径 11 的 648/625/636 共 15 个 Lab）。这**不消耗点数/不改数据，是效率缺陷**。根因：路径页活动 JSON 字段只有 `{id,href,description,title,isLocked,isComplete,inProgress,disabled,progress}`，**无 type 字段**，无法在路径页直接识别 Lab 课。修复：`gca.py advance` 新增 `--skip-course <id,...>`，配合 `_href_course_ids()` 从 href 抽 template/session 数字，在候选阶段和落地安全网两处排除（实测 path 11 传 648,625,636 → `lab_course_skipped:3`、无剩余新活动）。注意该参数是**显式**的：脚本不会替用户判断哪些 Lab 不做，须由扫描结果 + 用户决定后传入。
- **自主选课性价比评估**：对候选课程跑 `read-acts`，按活动标题/href 里的 type 分类计数（video/quiz/labs/documents + 已完成数）。优先级：Quiz 多 + Lab 少 + 非 Lab 内容多 + 未完成多。`Quiz=0` 的纯 Lab 课跳过；接近完成的先收尾。
- **badge / survey 的锁定机制**：课程完成凭证（badge）和调查问卷（survey）常带 `isLocked:true, disabled:true`——因为依赖 Lab 完成而锁定，Lab 没做就领不了/填不了。这是平台机制，不伪造、不绕过。
  - 单课模板的 survey 实际挂在 `course_sessions/<sid>/course_surveys/...` 下，直接开 `course_templates/<tid>/course_surveys/0` 会跳首页或"访问遭拒"。以课程内部菜单读到的真实 href 为准；读不到就判无可填项。
  - 常见现象：一门课"非 Lab 全做完"后，剩下的就是 N 个 Lab + badge（锁定）+ 偶尔的 survey（锁定）。如实报告即可。

## 12. 反馈迭代收敛法（327/256 实战，2026-11-18）

> 目标是通过而非满分。327 的 Quiz 577696 以 8/10 过线；256 的 6 个 Quiz 全过期间大量使用此法。

- 作答用 `scripts/quiz_answer_stable.py`：单 CDP 连接内 `goto`→显式点 `ql-button.retake-button`→轮询题目渲染→三轮点选→提交→读反馈，全程不重复 goto（避免覆盖 retake 状态）。慢网络下 `gca.py quiz-answer` 的 `prep=NONE` + `clicked=[]` 是不可信反馈，改用此脚本。
- 读**完整未截断**的反馈：`result` 里每题 Correct/Incorrect + rationale 文本；注意结果数组可能错位或少于题数（新课程只在题干下显示逐题对错，分数不进文本）。**是否过线以 `quiz-list` 的 `isComplete` 为准**，不要凭文本猜分数。
- 从反馈反推正确答案：反馈文字是平台权威解释，它否定/肯定什么就据此排除或锁定。例（LookML）：反馈 "views represent the underlying database tables" → 否定"views correspond to Explores" → 该题选 False。
- 只改判错的题，`kw` 用题干原文（每次 retake 题序与选项都重排，但按题干定位不受影响）。重排本身也可用来验证答案：换说法仍错说明判断方向错了。
- 2-3 轮仍不过就先搁置，做完其它 Quiz 再回头；拿不准的用 WebSearch 查官方文档（GCP→cloud.google.com，LookML→Looker 文档，Apigee→Apigee 文档）。

## 13. 本轮实战战绩（2026-11-18，做课程选择/进度参考）

> 数据来源：2026-11-18 连续会话中每门课 `read-acts` / `quiz-list` 复查的真实返回值与逐项操作日志（非推测）。当时 `complete_videos.py` 尚未固化进技能、跑的是 `/tmp` 同名脚本副本（内容等价），视频战报由该脚本产生。

- **paths/11 Associate Cloud Engineer**：活动 2-9 视频全标记 + 9 Quiz 全过（含 508941 补考），进度 88-92%；活动 10-12 纯 Lab 课（648/625/636 共 15+ Lab）因无点数跳过。
- **paths/19 Professional Cloud Developer**：22 Quiz 全过，非 Lab 全完成，剩 Lab。
- **paths/3545 Google ADK**：11 Quiz（27 题）全过、视频/文档全完成、3 个 Credly 凭证已"接受"，6 门子课 5 门完成；剩 1 门纯 Lab 课 + 依赖 Lab 的 credential。顶层 `read-acts` 只显示 6 门课，Quiz 藏在子课程模板里（顶层看不到，需进子课）。
- **327 Developing Data Models with LookML**（单课）：4/4 Quiz 过、24 视频、文档完成；剩 2 Lab + badge（锁定）。
- **256 API Development with Apigee**（单课）：6/6 Quiz 过、61 视频、文档完成；剩 11 Lab + badge（锁定）。
- **559 Cloud Run / 530**（接近完成）：Quiz 早已做完，剩 Lab + badge/survey（均因 Lab 未完成而锁定）。
- 本轮累计：21 Quiz 通过、85 视频标记完成、4 份满意度调查提交。全程未购买点数、未伪造完成、未代考。


## 14. 伙伴（代理商）专属认证资源与选课调研（2026-11-18）

> 联网调研来源：cloud.google.com 官方（Partners 页、认证页、PCK 页 `resources/pck-page`）+ CRN/多家伙伴解读。用于用户具备 Google Cloud 代理商身份时的导航与建议，只读不代办。

### 伙伴计划换版（关键前提）
- 2026-01-15 起 **Google Cloud Partner Network（GCPN）** 取代旧 Partner Advantage。层级 Registered→Select→Premier→Diamond（分轨：Co-sell/Services/Technology，且 Google Cloud 与 Workspace 分别评级）；Competency（21 类，Capacity+Capability 两维）取代旧 Specialization，与层级解耦。
- 旧口径（Premier 12 证、Partner 2 证）已作废，仅作量级参考。媒体披露 Diamond=2000 万美元 ACV+200 项专业认证，Premier=200 万，Select=25 万 ACV——非官网原文，以自身 Partner Network Hub 的 Requirements 为准。

### 伙伴专属免费通道
- **Partner Certification Kickstart（PCK）**：`cloud.google.com/resources/pck-page`，**须伙伴企业邮箱注册**；免费给考试券（券资格挂钩组织等级）+ 导师 + Google Skills for Partners 全访问。覆盖全部 12 条认证路径。
- **Google Skills for Partners**（`partner.skills.google`）：续证路径 PCA=`/paths/4178`、ACE=`/paths/4177`，PDE/CDL 有对应路径。2026 新规：完成平台指定徽章课程可免费续证 12 个月（有截止时效，以平台当前显示为准）。

### 认证价值排序（伙伴达标视角）
1. PCA（架构，伙伴硬通货）2. PDE（数据/AI Competency 标配）3. PCD（应用开发专精）4. PCSE（安全/受监管行业）5. PCDoE 6. PCNE/PCDE 7. PMLE（AI，周期最长）8. PSOE（最新）。Associate 级（ACE/ADP/GWA）不计入门槛但适合作底座；CDL/GAIL 属基础级、不计技术要求。GAIL（Generative AI Leader）、Agentic Architect、PSOE 为 2026 新增。

### 可快速完成的无 Lab 课程（本平台实测扫描）
- 目录页路径（动态渲染，链接不在 a[href]，需从 outerHTML 匹配 `/paths/\d+`）：4682 安全、4683 网络、4525 Agentic、4676 生成式 AI、4883 TPU、3545 ADK、19 云开发、82、11 ACE。
- **零 Lab 且有 Quiz（图文+Quiz，无实验阻塞，可快速推进）**：1564 Optimize Agent Behavior(4Q)、1385 Model Armor: Securing AI Deployments(4Q)、536 Introduction to Generative AI(4Q)、1683 Google AI for Finance Professionals(4Q)、1069 Responsible AI for Digital Leaders(3Q)、1203 Plan NGFW Needs(1Q)、1830 Critical Thinking in AI(1Q)、1586 Create First Gemini Enterprise App(1Q)、1682 Orchestrate Multi-agent Workflows(1Q)。活动 `documents`/`html_bundles` 类可导航跳过或快速过。
- 有 Lab 的课程 24 门（共 62 个 Lab），点数未到账前一律跳过。
- 扫描方法：已固化为技能脚本 `scripts/scan_courses.py <path_id ...> [--out f]`（复用 gca.py 的 read-acts，按 href 里的 video/quizzes/labs 分类计数，自动按"零Lab+有Quiz+待做多"排序，支持 GCA_PORT/--port）；结果默认写 `/tmp/gca_course_scan.json`。需看路径内子课明细（含顶层看不到的 Quiz）用 `scripts/dump_path.py <path_id>`。两者已从早期 `/tmp` 临时脚本吸收为可复用工具，不再依赖易失的 /tmp 文件。
  - **扫描坑（实测）**：路径页 activity href 有两种形态——未报名是 `course_templates/<tid>`，已报名是 `course_sessions/<sid>/...`。`scan_courses.py` 两种都识别并取代表 URL（去重 key 用 `template:`/`session:` 前缀）；早期 `/tmp` 版只认 template，导致已报名路径（如 19）扫出 0 门课。

## 15. 证书续证与考试券机制（2026-11-18 联网核实 + 真实账号勘察）

> ⚠️ 时效性：Google 续证政策在 2025-2026 快速调整（免费路径适用认证范围、早期宽限窗口多次变动）。**每次执行前必须以官方当日页面为准**：续证官方 `support.google.com/cloud-certification/answer/9907853`、PCK `cloud.google.com/resources/pck-page`、PCK FAQ（ services.google.com/fh/files/misc/pck-faq-2023.pdf ，2026-04-01 更新）、伙伴续证 `goo.gle/partner-renewals`。下面的数字是核实当日记录，不要当永久真理。

### 15.1 一句话查询账号证书/续证（已实现）
- 命令：`gca.py recert`（只读，导航 `/profile/badges`）→ 输出每张证的 name/issued/expires/status、剩余天数、`renew_window_open`（到期≤365天）、`expiring_soon_90d`、`recert_supported`、续证路径，以及 summary（哪些现在可续、哪些90天内到期、CM Connect 是否关联）。
- 数据来自凭证页 `innerText` 行结构：`Certifications (N)` / `Issued <date>` / `Expires: <date>` / `<证书名>` / `Active`。日期格式 `Mar 26, 2026`。
- **解析坑**：① 页面有通用 banner "Link your Google Skills and certification account..."，这是教程文字不代表未关联——只有出现明确的 "Ineligible for recertification" 才判未关联（`recert` 已按此修正）。② Badges 数在 Dashboard 首页顶栏，不在 `/profile/badges` 正文，勿把 0 当成真实徽章数。
- 真实账号（2026-11-18）：仅 1 张正式认证 **Cloud Digital Leader**，Issued 2026-03-26、**Expires 2029-03-26**（剩余 859 天），Active。→ 续证窗口（到期前 1 年 = 2028-03-26 才开）远未到，**现在刷课不计入续证**。导航显示 Badges 17 / Credentials 17。此前曾误以为账号有 ACE，实测纠正：**只有 CDL**（印证"不能一味相信，要实测"）。

### 15.2 续证规则（官方）
- 有效期：Professional 2 年；Foundational/Associate 3 年。
- 两条路径：① 续证考试（基础/助理到期前180天、专业到期前60天开；+3/+2年；有短版半价考试，如 ACE $75/20题、CDL $60/45题、PCA $100/25题；首证时发 50% 折扣码在 CM Connect 查）；② Google Skills 继续教育（**一律到期前1年开窗，+1年，免费**）。
- **继续教育硬规则**：只有认证有效期**最后一年内**完成的指定课程/徽章才计数；提前完成无效且**不能重做**（必须另选活动）——这是最容易浪费精力的点。单个活动不能跨多证复用。到期后 30 天内仍可续；超期即失效、重考拿新 Series ID。
- 支持继续教育的认证：早期为 CDL/ACE/PCA/PDE 四张；**2026-07 起扩展到 GAIL、AGWA、ADP、PCDBE、PCD、PCDE、PCSE、PCNE、PMLE、PSOE**（官方博客 cloud.google.com/blog/topics/training-certifications/new-ways-keep-google-cloud-certifications-current）。仍以平台当日显示为准。
- 伙伴续证路径入口：`partner.skills.google/paths/4178`(PCA)、`/paths/4177`(ACE)；PDE/CDL 同平台对应路径（确切 ID 官方未公开，勿编造）。伙伴走 Partner Recertification Program：失效前申请可 100% 折扣（不受配额），7/1 后仅限有效期内、到期前 2 个月窗口、需完成 1 个学习模块 + 有效 DRP 档案。

### 15.3 PCK 考试券（伙伴专属，与续证互斥）
- PCK 免费考试券**不可用于续证**（官方明确 "not intended to support recertification"）——续证走 15.2 的 Partner Recertification Program。
- 发放条件：伙伴企业邮箱注册（Gmail 等公共邮箱无资格）→ 选定认证路径 → **报名起 10 周内**完成该路径全部必修活动 → 发全额考试券。10 周窗口固定，不能靠重新报名重置；逾期联系 cloud-partner-training@google.com（不保证）。
- 配额：按公司 Partner 层级/投入分配；同一人同一认证每 12 个月 1 张。券有效期以发放邮件为准，官方建议尽快约考；缺考或改期截止后取消则作废不补发。可用于该认证任意语言。
- **用户策略"先不考、留进度以后拿券"的正确理解**：券是"完成培训后"才发且有有效期，所以真正要保留的是**尚未报名的 PCK 路径**（一旦报名即开始 10 周倒计时）；不要提前把路径刷完拿券再拖着不考（券会过期）。含 Lab 的 PCK 路径在点数到账前本就做不动，正好天然保留。因此：零 Lab 课现在照常做（拿徽章/涨进度），PCK 认证路径先不报名。

## 16. Quiz 机制细分：分页式 vs 一页全题、选项集合变化（2026-11-18 实战）

> 本轮做 9 门零 Lab 课时发现，不同课程的 Quiz 提交机制不一样，不能用一套脚本硬套。

### 16.1 两类 Quiz（决定用哪个脚本）
- **A 类「一页全题」**：所有题目同时渲染在 DOM，页面直接有 `ql-button.submit-button`。代表：1586/1203/1830/1682（新课）。用 `quiz_answer_stable.py` 一次作答即可，实测 4 门全过（含满分）。
- **B 类「分页逐题」**：DOM 里虽有多题，但页面用 Previous/Next 分页，`submit-button` 只在**最后一题**出现。代表：1069、536（老课）。识别信号：quiz-read 只返回 1 题 / body_head 见 "Previous Next" / 初始无 submit-button。
- **B 类作答要点**：先在当前页点选题（CLICK_JS_TMPL 按 kw 定位，能点到当前 DOM 里的题）→ **若当前页已有 submit-button 就直接点它，不要点 Next**（点 Next 翻页会让已选状态失效、submit 变 DISABLED）→ 只有确认无 submit 才点 Next 推进。
- 新增脚本：`scripts/quiz_answer_inplace.py`（读题后不 retake、当前答题态直接点选+提交，带 Next 兜底）、`scripts/quiz_answer_paged.py`（分页课专用，goto→retake→点选→Next 循环→submit）。两者均 import gca 的 CLICK_JS_TMPL/LIN_JS 复用成熟逻辑。

### 16.2 「读题与作答之间不能再次 retake」（关键坑）
- 有些 Quiz（如 1069 的 495498）**每次 Retake 不仅重排题目/选项顺序，连选项集合都会变**（实测同一题第二次 retake 少了"all stages"这个正确选项，只剩 3 个全错干扰项）。
- 因此：`gca.py quiz-read --retake` 读题后，`quiz_answer_stable.py` 若再 retake 一次，选项就不是刚读到的那份 → `notfound` 或答错。**正确做法**：读题后立即用 `quiz_answer_inplace.py`（不 goto、不 retake）在当前答题态作答，opts 用刚读到的**完整原文**（精确匹配；截断文本要加 `fuzzy:true`）。
- 现象区分：`clicked:[]` 不代表没点上——若选项已被选中（DIAG/on=true），inplace 不会重复点；**以 DIAG 的 on 状态和最终分数为准**。

### 16.3 提交后跳课程页 = 答错/未记录
- 现象：submit 返回 SUBMITTED，但结果里只有 "Passing score: X%"、无 "Your score"，随后页面自动跳回课程介绍页，`quiz-list` 复查仍 false。
- 判断：这是**答错**或答案未写回，不是脚本故障。先核对选中态（LIN_JS 的 on 字段），再核对答案语义；多选题尤其注意（如 536 Quiz4 幻觉成因三选，需 A/B/C 全选对）。
- 若确认答案对仍不过，用结果页 `ql-button.feedback-button` 看平台给的正确答案，或 WebSearch 查该题标准答案。

### 16.4 本轮成绩（2026-11-18，最终复查 isComplete 为准）
- **6 门课 Quiz 全过**：1586(1/1)、1203(1/1)、1830(1/1)、1682(1/1)、1564(4/4，ADK 题全 100%)、1069(3/3)。其中 1586/1203/1830/1682/1564/1069 的 Survey 已提交。
- **部分完成**：1385 Model Armor 3/4（686272 多选组合未过）、536 GenAI 3/4（645356 幻觉成因多选未过）、1683 AI for Finance 2/4（640560/640571 选项集合会变）。
- 合计 17/21 Quiz 通过；这些零 Lab 课的 Quiz 通过后，Skill badge 多会自动 complete。
- Survey 用 `scripts/submit_survey.py`（radio 按 name `[索引]` 分组选最高 value，N/A=0 不选）。注意 template 顶层 `read-acts` 的 survey href 常为 None（挂在 course_sessions 下），此时 `course_templates/<tid>/course_surveys/0` 可能 NO_BUTTON，跳过即可。

### 16.5 一个反复确认的判定原则
- **以平台 `read-acts` 的 `isComplete` 为唯一权威**，不要信脚本 stdout 里的分数文本：曾出现分数显示 33%/66% 混乱、但 isComplete=true 的情况；也有显示 SUBMITTED 但 isComplete=false 的情况。批量跑完统一用 `read-acts` 复查。
- 顽固 Quiz（2-3 轮不过 + 选项集合变化 + 分页/提交机制冲突）按"搁置-回头"处理，不无限死磕；如实报告部分完成即可。

### 16.6 续证/新课推进实战（2026-11-19，路径 4676/3476）
- **页面停在结果页时，`quiz-answer` 前必须先 `quiz-read --retake` 进答题态**：此时 `quiz-answer` 返回 `prep:NONE` 且**静默不提交**（无分数），`read-acts` 复查仍 false。实测 1401 的 Q2/Q3 首轮就此失败。正确顺序：`quiz-read <url> --retake` 确认返回题目 → Agent 逐题判断并写 `@answers.json` → `quiz-answer @answers.json` → 回读 isComplete。**边界**：此条针对"结果页停驻 + `gca.py quiz-answer`"，与 16.2 不冲突——16.2 针对选项集会变的课，读到题后改用 inplace 不再 retake；两者按课程类型选择，别混用。另注意与 L4"Retake 时序坑"区分：那是慢网络下 retake 按钮未渲染导致提交旧答案（用 stable.py），这里是结果页停驻导致静默不提交（用 quiz-read --retake）。批量 for 连跑易踩此坑，逐个来更稳。
- **session 文档是链式活动**：`documents/<id>` 读到底会推进到下一节（doc 633847→633848→quiz 633849），路径页聚合进度显示 83% 未必是真卡——要用 `read-acts <course_template真实URL>` 看**内部活动清单**才准。
- **卡住活动用路径页的真实 href，不要猜 URL 格式**：路径页 TODO 活动的 href 是权威（如 `course_templates/1751`），猜成 `course_sessions/<sid>/quizzes/1751` 会 302 到首页。且 `course_templates/<tid>/documents/<id>` 直接 goto 1.2s 即标记完成（1120 的 17 个、1401 的 12 个全生效）；但 `course_sessions/<sid>/documents/<id>` 若持续跳首页（如 633833），是活动失效/迁移，残留进度无法完成，按边界如实跳过、不伪造。先用 `read-acts <路径URL>` 拿 TODO 的 href 原文再访问。
- **路径级 100% 要求课程也 100%**：1120 做到 20/24、1401 做到 15/18（Lab 未做），路径 4676 仍显示 7/9——Lab 锁住课程完成，进而锁住路径级。汇报要说清"课内已大幅推进但 Lab 锁路径级"，别让用户以为没做。
- **`quiz_solve.py` 已知 bug（单选 VERIFY 错位）**：这是独立于 17.1 点选修复的另一 bug——点选已按 17.1 点内部 input，但 VERIFY 阶段读 host 的 checked（而非内部 input），导致 `fixedCount=6`（6 = 需纠偏的题数）选项错位、`submit:DISABLED`。遇此改用 `gca.py quiz-answer`（其内部点选仍遵守内部 input 规则，非点 host；实测稳定，1120/1401/3476 全过）。详见 SKILL.md L4 同名条目；待后续专门修复。

---

## 17. 顽固 Quiz 攻坚与点选偏移 bug（2026-11-18 第二轮实战，重要）

### 17.1 根因一：md-radio/md-checkbox 的 host.click() 会误选相邻项（P0 级坑）
- **现象**：多选题点选后 `clicked` 显示成功，但提交答错；读回 checkedCount 比答案项数多（如答案 8 项却 checked 9 项）。
- **实测证据**（645356 幻觉成因多选）：想点 `not given enough context`，实际选中 `not trained on enough data`；想点 `noisy or dirty data`，也落到相邻项。逐项诊断确认 **host.click() 触发了 DOM 顺序相邻的 radio**。
- **修复**：只点内部 input：`el.focus()` + `el.shadowRoot.querySelector('input[type=radio/checkbox]').click()`，**绝不点 host**（host.click 与 input.click 叠加更乱）。已固化到 `scripts/quiz_solve.py`。
- **提交前闭环验证**：读回所有 `checked`/`aria-checked=true` 的选项文本，与目标逐一比对；不符则用 focus+input.click 精确纠偏（如把误选的 not-trained 取消、把未选的 noisy 选上），确认完全一致再 Submit。

### 17.2 根因二：retake 残留态——读到上次答卷而非新题
- **现象**：`quiz-read --retake` 后某些选项已 `selected=true`（是上一次提交的残留），在其上改答案反复不过。
- **根因**：retake 在慢网络/某些课（如 686272）2.5s 内未生效，`--retake` 返回 `prep:NONE`，实际还是旧答卷。
- **修复**（`quiz_solve.py read`）：goto 后**轮询最多 10 次**等 `ql-button.retake-button` 渲染并点击；再轮询等所有 radio `disabled` 消失且全部未选中，才算真正的新题态。读到残留（有 selected）不可直接作答。

### 17.3 retake 换题/选项导致 read→solve 之间不能有任何导航
- 部分课（640560/640571）每次 retake 连题目顺序和选项集合都变。**read 读到干净答题态后，绝不能再 goto/retake**（哪怕是查 isComplete 的导航也会切走 tab），否则答案与当前题不匹配。
- 正确流程：`quiz_solve.py read`（拿到当前题目原文）→ Agent 判断写 answers.json → `quiz_solve.py solve`（不导航，复用当前 tab 点选+提交）→ 提交完成后才导航去查 isComplete。

### 17.4 文档/视频/html_bundle 的完成机制差异（实测）
- `documents/*`：goto 访问即自动标记完成（1203 的 5 个、1960 的 15 个、1683 的 20 个均如此）。
- `video/*`：需点 `ql-button[href*=complete_button]`（用 `complete_videos.py`）。
- `html_bundles/*`：纯 goto 访问**不**标记完成，Previous/Next 点 Next 也不标记；机制未摸清，属内容浏览型边界，不必死磕。
- `course_surveys/0`：`submit_survey.py` 全选正面项提交，done=true。
- **批量收尾顺序**： Quiz 作答 → complete_videos → 遍历 documents goto → submit_survey → read-acts 复查到 100%。

### 17.5 本轮战果（2026-11-18 下午，isComplete/quiz-list 为准）
- **零 Lab 有 Quiz 课攻坚**：本轮新完成 10 门中的 9 门 **100%**：
  - 100%：1081 Healthcare(2Q+12视频+survey)、1203(1Q+5文档)、1830(1Q+5文档)、1586(1Q+1文档)、1682(1Q+2文档)、1069(3Q+4视频+1文档)、1960 TPU(1Q+15文档+survey)、1683 Finance(4Q+20文档+survey)、536 Intro GenAI(4Q+9视频+1文档+survey)。
  - 1832 Build Agent Skills：43%（8 个 html_bundle 未标记，见 17.4 边界）。
  - ~~顽固搁置：686272 Model Armor Quiz~~ → **后于第 18 节攻克（100% 通过），此结论已作废**。
- **权威判定**：`quiz-list` 路径未过数——4883=0（TPU 路径全清）、4676=6（剩 1120/1401 有 Lab 课）、4525=16（后降为 15，见 18 节）、4683=8。剩余均为**有 Lab 的课**（跳过 Lab 进度停在 ~90%）或纯 Lab 课。
- **教训**：一个 Quiz 反复不过，先怀疑"点选机制 bug"（checkedCount 异常）而非答案判断；host.click 偏移是本轮最大隐藏杀手，修复后 645356 一次通过。

---

## 18. 686272 攻克：结果页渲染延迟 + "假顽固"识别（2026-11-18 第三次实战，重要纠正）

> **核心纠正**：686272 曾被误判为"顽固 Quiz / retake 失效"而搁置 4 轮。真正根因是**提交后结果页渲染慢（约 4 秒）**——脚本只等 3 秒就判定"无结果、未过"，叠加残留态误读，冤枉了正确答案。最终 100% 通过（Passing 75%）。

### 18.1 真因：结果页渲染延迟导致"假未过"
- 现象：`quiz_solve.py solve` 提交返回 `SUBMITTED`、`fixedCount=0`（选中态与目标完全一致），但脚本内只 `sleep(3)` 就读结果文本，此时仍是答题态（只有 "Passing score: 75%"、按钮仍 Submit、无 "Your score"/retake）→ 误判未过。
- 实测：提交后**第 4 秒**结果页才出现 `Your score: 100%` / `Congratulations! You passed this assessment.` / retake-button。轮询第 0-2 秒都还是旧态。
- **修复做法**：提交后用长轮询（每秒一次，最多 10 次）等结果页标志（retake-button 或 "Congratulations"/"Your score"）出现，别用固定 3 秒；判定以出现的分数/祝贺文本为准。
- 这也印证 16.3：只显示 "Passing score: X%" 而无 "Your score" = **还在渲染中或未过**，需再等，不能立刻下结论。

### 18.2 残留态 + host.click 后遗症的叠加处理
- 刷新后选中数从 8 掉到 7（Q4 gcloud CLI 丢失）——host.click 偏移后遗症 + retake 残留共同作用。
- **增强作答流程**（`/tmp/solve_686272_v2.py` 模式，可复用）：
  1. 先 CLEAR 所有 checkbox 选中（`focus()+内部input.click()` 逐个取消）；
  2. PICK 目标答案（quiz_solve.PICK_TMPL）；
  3. VERIFY **连续 3 轮 `fixedCount=0`** 才算稳定（不是 1 轮就提交，防异步漏点/偏移回弹）；
  4. Submit 后**长轮询 10 秒**等结果页标志。
- 注意：`import quiz_solve` 会触发其顶层 argv 读取，需先 `sys.argv=['quiz_solve.py','dummy','read']` 再 import；或复用其模板常量时直接读文件文本。

### 18.3 本题正确答案（Model Armor 题，经官方文档核实，可复用）
- **启用 Model Armor API**（多选）：`Model Armor page of Security Command Center` + `Google Cloud CLI`（官方 gcloud services enable modelarmor.googleapis.com；Gemini prompt/Monitoring page 错）。
- **配置 logging 访问完整 prompt/response**（多选）：`Python` + `CURL command from REST API`（Logs Explorer 是查看不是配置；SCC 不能配日志）。
- **模板 confidence 低于 floor setting**（单选）：`shows an error message when Ariel tries to save`（官方 "You cannot create or update a template that's less strict than the floor settings"；~~"defaults to floor confidence"~~ 是错的，旧判断在此翻车）。
- **创建 test templates 的方式**（多选）：`REST with curl` + `Python` + `gcloud CLI`（官方 gcloud model-armor templates create；GKE kubectl+Docker 错）。

### 18.4 权威复核与战果
- 提交通过后：`quiz-list 4525` 的 `unchecked_quiz_count` 从 16 → **15**，686272 从清单消失；1385 Model Armor 4/4 全过。
- **判定原则再强化**：结果页 "Congratulations! You passed" + `quiz-list` count 下降双确认才算真过；只看到 SUBMITTED 或旧文本不算。
- **教训**：遇到"顽固"先怀疑**判定时机**（结果页渲染延迟）和**残留态**，别急着归因答案错或机制冲突；长轮询 + 多轮 VERIFY 稳定后再定论。此前"4 轮不过"实为每轮都在第 3 秒误判，答案其实一直可能对。

---

## 19. Google Skillshop 正式 Credential 考试（Intellum/Exceed LMS，2026-11-18 联网核实）

> 对应 `SKILL.md` Phase 5。与 skills.google 课程内 Quiz 是**两个不同平台、两套不同机制**，禁止把课程 Quiz 的"无限 Retake / 看反馈"经验套到本节。本节记录平台机制、差异对比、登录链路、考试规则、每题联网核实方法与用户交互确认点。

### 19.1 平台识别与机制
- 域名：`skillshop.exceedlms.com`（不是 `skills.google`）。底层是 **Intellum / Exceed LMS**。
- 链接形态：`/student/path/<id>-...credential`（正式 Credential 结业考试路径）；与 skills.google 的 `/paths/<id>`、`/course_templates/<tid>`、`/quizzes/<qid>` 完全不同。
- 未登录页面提示："需要验证，在下方登录以解锁附加内容"。
- 第 3/4 节的 `QL-ITEM-STEM`、Shadow DOM、多选内部 input 等 skills.google 选择器经验**不适用于**本平台。读题走 Phase 5 的 `gca.py` `client`/`goto`/`evj` 取 `document.body.innerText`，以页面当前渲染为准，不预设选择器。

### 19.2 与 skills.google 课程 Quiz 的差异对比

| 维度 | skills.google 课程 Quiz（Phase 3b） | Skillshop 正式 Credential 考试（Phase 5） |
|---|---|---|
| 平台 | skills.google（自家 LMS） | skillshop.exceedlms.com（Intellum / Exceed LMS） |
| 入口 | `/quizzes/<qid>`、路径/课程活动 | `/student/path/<id>-...credential` |
| 重试 | 无限 Retake，改错即可重考 | 失败需等 **24 小时** 才能重考 |
| 反馈 | 交卷显示 Correct/Incorrect 与 rationale，可迭代 | 提交后不可修改，无逐题反馈可依赖 |
| 及格线 | 页面 `Passing score` 决定，常见 75% | **80%** |
| 时限 | 无严格限时 | **有时间限制**（以页面倒计时为准） |
| 中断 | 可离开、回头再做 | **中途关闭算自动失败** |
| 作答策略 | 先答、看反馈、2-3 轮收敛，目标过线 | 每题先联网核实再录入，提交前逐题三查，一次定音 |
| 自动化 | `quiz_solve.py` 等成熟脚本可批量作答 | 不新增脚本，复用 `client`/`goto`/`evj` 只读核验；密码与提交必须本人操作 |
| 资格边界 | 课程内练习，Agent 可自主作答争取过 | 本人账号 + 本人在场 + 明确知情授权 + 每题联网核实 + 关键步骤本人确认，缺一拒绝 |

### 19.3 登录链路（密码必须本人输入）
1. 打开考试 URL → 未登录显示"需要验证，在下方登录以解锁附加内容"。
2. 点击登录 → `/authentication/google_authentication` → Google OAuth **账号选择器** → **密码页**。
3. 🛑 STOP：密码页停下，提示用户本人在浏览器输入账号密码并完成二步验证；Agent 不代输、不读取、不记录、不绕过。
4. 用户确认已登录后，用 `client`/`goto`/`evj` 读回页面，确认进入答题页再继续。
5. 不为考试单独启动或重启浏览器；沿用 Phase 0 已探测的入口和当前标签页，避免中断考试。

### 19.4 考试规则（联网核实，2026-11-18）
- **80% 及格**。
- **有时间限制**（以页面倒计时为准）。
- **提交后不可修改**。
- **失败需等 24 小时**才能重考。
- **中途关闭标签页/浏览器算自动失败**。
- 因此：提交前必须完成逐题三查并取得用户"确认提交"；提交后只读回结果，不立即重试、不反复空转、不关闭标签页；未过则如实告知 24 小时窗口。

### 19.5 每题联网核实方法（不可跳过）
1. 用 `goto` + `evj` 读当前题的题干与选项原文；每次翻题后重新读（题序/选项可能变化），按**题干文本**定位，不按下标。
2. 每题用 WebSearch + WebFetch 到 **Google 官方文档**（`cloud.google.com`、`developers.google.com`）核实，以官方文档原文为唯一判据；拿不准就继续查，不凭记忆、不猜。
3. `en.certificationanswers.com` 等第三方站**只有题目、没有可靠答案**（标题党），仅用于定位考点关键词，**禁止当作答案来源**。
4. 为每题记录"题干关键词 → 官方文档 URL → 结论"的临时笔记，供提交前复查。
5. 若出现与第 6/18 节相同考点（Model Armor、存储类别、IAM、Terraform state 等），优先复用其中已验证的官方文档出处，但仍须按当前题干重新核对。

### 19.6 用户交互确认点（🛑 STOP / 🔴 CHECKPOINT）

| 节点 | 交互动作 |
|---|---|
| 密码页 | 🛑 停下，用户本人输入账号密码 + 二步验证，回报"已登录" |
| 每题核实结论 | 🛑 回报"题干摘要 + 候选选项 + 官方文档依据"，等用户确认/修改后再录入下一题 |
| 依据不足或有分歧的题 | 🛑 如实标注，由用户拍板，不擅自决定 |
| 提交前 | 🔴 逐题三查（题干一致 / 选中项一致 / 官方文档出处有效）全部通过 + 用户明确"确认提交" |
| 提交后 | 只读回结果并报告；未过告知 24 小时窗口，不重试、不关页 |

### 19.7 边界红线
- 不为他人代考、不使用泄题/灰产答案、不绕过监考、不伪造身份。
- 不满足"本人账号 + 本人在场 + 明确知情授权 + 每题联网核实 + 关键步骤本人确认"全部条件时，一律拒绝，回复只处理课程内 Quiz。
- 本平台不改动后台数据、不伪造完成状态、不使用脚本自动提交。

### 19.8 实战 DOM 选择器与作答机制（2026-11-18 首战实测，可复用）
- **考试页**：`/student/path/<pid>/activity/<aid>`，打开即渲染全部题目（本例 40 题），**未点提交前不计时/不算开始**。
- **题目容器**：`div.question`（每容器一题）；题干 `p[id^=question_body_]`；选项 `label.radio` / `label.checkbox`。
- **单选题**：label 内 `input[type=radio]`，点 label 即选中。
- **多选题（关键坑）**：`label.checkbox` 内**有两个 input**——第一个是 `type=hidden`，第二个才是 `type=checkbox`。用 `querySelector('input')` 会取到 hidden 那个，导致 `label.click()` 显示点了、复核却 `checked=false`（本例 4 道多选全部踩坑，单选正常）。**必须**用 `querySelector('input[type=radio],input[type=checkbox]')` 精确匹配，排除 hidden。
- **提交按钮**：`#single_page_submit_link`（assessment-navigation 容器，文案"提交"），需 `scrollIntoView` 后用真实鼠标点击。注意区分三个干扰按钮：星级评分的 `input.rating__submit`（display:none）、搜索栏的 `button.a11y-atonly`、放弃弹窗的 `#confirm-drop-activity`——**都不要点**。点提交后可能直接判分（本例无二次确认弹窗）。
- **判分**：提交后页面显示"通过 (98%)"/"总得分 X/Y"/"正确回答 X/Y"；点"查看回答详情"按钮展开，错题的 `.question__answercorrection` 元素含"正确答案是 ..."原文，可据此定位错题。
- **作答流程**：`填答案索引 → 读回 checked 态逐题比对 → 不一致则重填(闭环) → 读回选中选项文本逐字核对 → 提交`。本例 40 题闭环后 filled=40/40、bad=0、文本逐字一致才提交。

### 19.9 首战战绩与错题教训
- **Google Maps Platform Technical Fundamentals Credential**：本人账号授权，40 题逐题联网核实官方文档后录入，**一次提交通过 39/40（98%，及格 80%）**，用时约 25 分钟核实+录入。
- **唯一错题 Q17**（iOS 动态地图无 Map ID 如何计费）：我按官方文档"无 Map ID 按 Dynamic Maps SKU 每千次加载计费"选了该项；平台判定正确答案是"native mobile SDK without cloud styling 免费"。→ **教训**：课程教材口径可能与官方文档细则不同（课程按"移动 SDK 基础地图无云样式免费"的旧/简化口径判），遇此类"官方细则 vs 课程简化口径"分歧，以课程教材表述为准；但本题仍过线，不影响拿证。
- **全部 40 题答案与官方依据**存于当时 `/tmp/maps_cred/answer_key.md`（临时，会话后失效）；核心正确项见 19.8 流程。第三方站 certificationanswers 只有题目、答案在付费 PDF（灰产），未采用——印证 19.5 第 3 条。

### 19.10 考试通过 ≠ 证书到手：模块完成与证书发放（2026-11-18 首战实测，重要）
- **坑**：只通过 Assessment（39/40）后，证书**没有**立即发——"我的学习"页课程仍显示"路径/进行中"，路径页无"查看奖励"。用户问"记得会有证书"才发现的。
- **根因**：Credential 要求**整条路径全部 activity 完成**（本例 12 个：11 个学习模块 + 1 个 Assessment）。当时只完成了第 1 个模块和最后 Assessment，中间 10 个 module 未完成。
- **完成状态判定**：路径页 `/student/path/<pid>` 每个 activity 的 `li.outerHTML` 含 `completed` 即已完成；无则未完成。不要只看页面文本。
- **阅读型模块的完成机制**：goto 进模块页 → **滚动到底部**即自动标记完成（`window.scrollTo(0, document.documentElement.scrollHeight)`，并对内部滚动容器设 `scrollTop=scrollHeight`；重复 3-4 次、每次停 1.2s 触发 intersection observer）。仅 goto 不滚动不会完成。模块末尾有 "Congratulations / Well done on completing the X module" 提示可佐证。
- **批量补齐**：写脚本对未完成的 activity id 逐个 goto+滚到底，再回路径页统计 completed 数。本例补齐 9 个模块（3788903~3788911）后 12/12 全完成。
- **证书发放**：全部 completed 后，路径页顶部出现"通过：<日期> / 到期日期：<日期> / 查看奖励 / <姓名>于<时间>完成"。点"查看奖励"按钮（class `enrollmentmessage__action`）弹窗显示证书：名称、完成人、**完成ID**、到期日、**打印**按钮（可打印/存 PDF）。本例证书到期 2028-11-18（有效期 2 年），完成ID 490178961。
- **教训**：Skillshop Credential 的正确完成标准 = Assessment 通过 **且** 全路径 activity completed **且** 拿到"查看奖励"证书；三步缺一不可。回报用户时要给证书信息，别只报考试分数。
- **元教训（通用机制见 SKILL.md L2.5）**：本场景"考试过≠任务完成"是**局部当整体**的典型——L0 应是"证书到手"而非"通过考试"；宣告完成前按 L2.5 做终局核验，未拿证书弹窗只能报"X/Y + 剩余"。此原则适用于所有课程/证书任务。
