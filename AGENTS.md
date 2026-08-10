# Universal AI Agent Instruction Manual (AGENTS.md)

> **FOR ALL AI TOOLS & AGENTS** (Antigravity, Codex, Claude Code, Cursor, Windsurf, Copilot, ChatGPT, etc.):
> This document is the primary instruction manual for AI agents operating in this repository (`Skills`).
> You MUST follow the directory map, step-by-step SOPs, and guardrails defined below whenever you are asked to create, edit, audit, or import skills.

---

## 🗺️ Repository Map & Entry Points

| Path | Description | Access Rules |
| :--- | :--- | :--- |
| `skills/` | Main storage directory for all Skill modules (`skills/<skill-name>/`) | All new skills MUST be stored under this directory. |
| `.template/SKILL.md` | Standard Skill template | Reference when scaffolding or editing skills. |
| `scripts/create_skill.py` | CLI scaffold tool (`./scripts/create_skill.py <name> -d "<desc>"`) | Use this script to create new skill directory structures. |
| `scripts/validate_skills.py` | Compliance validator (`./scripts/validate_skills.py`) | MUST be executed after creating/editing any skill. |
| `scripts/setup_hooks.sh` | Local Git pre-commit installer (`./scripts/setup_hooks.sh`) | Run once locally to attach validator to `git commit`. |
| `.github/workflows/` | GitHub Actions CI workflow | Runs `./scripts/validate_skills.py` on PR and push to main. |
| `README.md` | Repository catalog & index table | MUST be updated whenever a skill is added/removed. |
## Agent skills

### Issue tracker

GitHub Issues (`guyue55/Skills`). See [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).

### Triage labels

Canonical role mapping enabled (`needs-triage`, `ready-for-agent`, etc.). See [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).

### Domain docs

Single-context repository (`AGENTS.md` + `docs/`). See [`docs/agents/domain.md`](docs/agents/domain.md).

---

## 📋 Standard Skill Anatomy

Each individual skill directory under `skills/` MUST follow this exact structure:

```
skills/<skill-name>/
├── SKILL.md            # [REQUIRED] Main definition file (YAML frontmatter + Markdown body)
├── scripts/            # [OPTIONAL] Executable helper scripts (Python/Bash)
│   └── .gitkeep
├── references/         # [OPTIONAL] Documentation, schemas, and reference guides
│   └── .gitkeep
└── assets/             # [OPTIONAL] Output templates, boilerplate, fonts, icons
    └── .gitkeep
```

> [!WARNING]
> **Extraneous File Ban**: Do NOT create `README.md`, `INSTALLATION.md`, or `CHANGELOG.md` INSIDE individual skill subdirectories (`skills/<skill-name>/`). `SKILL.md` is the sole entry point for AI agents.

---

## 🚀 Step-by-Step SOP for AI Agents

### Task 1: Creating a New Skill

When the user asks to "create a skill", "build a skill", "make a new skill", or "add a skill for X":

1. **Scaffold Directory**:
   Run the scaffold script in terminal:
   ```bash
   ./scripts/create_skill.py <skill-name> -d "<Concise description and trigger triggers>"
   ```
   *Note: `<skill-name>` MUST be lowercase alphanumeric with hyphens (e.g., `git-workflow-helper`).*

2. **Edit `skills/<skill-name>/SKILL.md`**:
   - Ensure Frontmatter is present:
     ```yaml
     ---
     name: "<skill-name>"
     description: "<Clear description of what the skill does AND exact triggers/contexts for when to invoke it>"
     ---
     ```
   - Complete the Markdown body with sections:
     - `# Skill Title`
     - `> [!NOTE]` Overview
     - `## 触发条件与使用时机 (When to Use)`
     - `## 详细工作流 (Workflow & Instructions)`
     - `## 红线与禁忌 (Guardrails & Anti-Patterns)`
     - `## 示例 (Examples)`

3. **Populate Subdirectories (If applicable)**:
   - Put executable Python/Bash scripts into `skills/<skill-name>/scripts/`.
   - Put detailed reference docs/schemas into `skills/<skill-name>/references/`.
   - Put output templates or assets into `skills/<skill-name>/assets/`.

4. **Validate Compliance**:
   Run the validator script:
   ```bash
   ./scripts/validate_skills.py
   ```
   Ensure it reports: `🎉 所有 Skill 模块校验通过！`.

5. **Update Index Catalog**:
   Add a new row to the table in [`README.md`](README.md):
   ```markdown
   | `<skill-name>` | `<description>` | [`skills/<skill-name>/SKILL.md`](skills/<skill-name>/SKILL.md) |
   ```

6. **Prompt Git Commit**:
   Stage and commit changes using the required format: `type(scope): 中文描述` (e.g., `feat(skill): 新增 <skill-name> 技能`).

---

### Task 2: Importing or Migrating an Existing Skill

When the user provides an existing skill or raw prompt语料 to import:

1. Create directory `skills/<skill-name>/`.
2. Save the skill definition to `skills/<skill-name>/SKILL.md`.
3. Verify that `SKILL.md` starts with valid YAML Frontmatter (`name`, `description`).
4. Ensure `name` in frontmatter EXACTLY matches `<skill-name>`.
5. Remove any `README.md` if present inside `skills/<skill-name>/`.
6. Run `./scripts/validate_skills.py` to confirm clean validation.
7. Update the catalog table in `README.md`.
8. Stage and commit changes using `feat(skill): 导入 <skill-name> 技能`.

---

### Task 3: Auditing & Validating Skills

When asked to "check", "audit", "validate", or "review" skills:

1. Execute `./scripts/validate_skills.py`.
2. Inspect output for:
   - Missing `SKILL.md` files.
   - Frontmatter `name` / directory mismatch.
   - Hardcoded absolute paths (`/Users/` or `/home/`).
   - Placeholders (`TODO:`, `FIXME:`, `pass`, `...`).
   - Extraneous `README.md` files inside skill folders.
3. Fix any identified errors and re-run `./scripts/validate_skills.py` until 100% clean.
4. Stage and commit fixes using `fix(audit): 修复 Skill 校验问题`.

---

## 🛑 Guardrails & Hard Directives (红线与硬性约束)

1. **De-hardcoding (环境脱敏)**:
   NEVER hardcode personal absolute paths (such as `/Users/username/...` or `/home/username/...`). Always use relative paths (`./`), `~`, or environment variables.

2. **Anti-Laziness (拒绝虚假代码与占位符)**:
   NEVER submit code with `pass`, `...`, or `TODO: fill in later` in production skills. All instructions and scripts MUST be complete and functional.

3. **Single Entrypoint (单文件入口)**:
   Each skill MUST have `SKILL.md` as its sole documentation file. Do NOT put `README.md` inside `skills/<skill-name>/`.

4. **Git Preservation (版本控制完整性)**:
   Keep `.gitkeep` files in `scripts/`, `references/`, and `assets/` when they contain no other files, ensuring Git tracks the directory structure.

5. **Traceability (日志明文透明)**:
   Output clear diagnostic trace logs (e.g., `[Trace: Skills/Workflow] ...`) when performing multi-step operations.

6. **Prompt Git Commit & Standard Format (及时 Git 提交与规范格式)**:
   AI Agents MUST promptly commit changes to Git upon completing a task or bug fix.
   **Commit Message Format**: MUST strictly follow `type(scope): 中文描述` (e.g., `feat(skill): 新增 git-workflow 技能`, `refactor(script): 优化校验流程`).

7. **Chinese Comments Requirement (中文注释)**:
   All code, Python/Bash scripts, and instructions written or modified by AI Agents MUST contain detailed, high-quality Chinese comments (`中文注释`) to maintain readability and maintainability.

8. **Zero-Leakage & Sensitive Credentials Ban (隐私与敏感信息防泄密红线)**:
   NEVER commit private, sensitive, or confidential information (e.g., API keys `sk-`, `AIza`, `ghp_`, passwords, secrets, private keys, database credentials, tokens).
   AI Agents MUST verify all code and markdown files with `./scripts/validate_skills.py` before committing to ensure no sensitive credentials leak into Git history.
