# CLAUDE.md - Claude Code Project Instructions

Welcome to the **Agent Skills Repository** (`Skills`).

> ℹ️ **Universal Agent Instructions**:
> Full detailed SOPs, repository map, and guardrails are defined in [AGENTS.md](AGENTS.md).
> Always refer to [`AGENTS.md`](AGENTS.md) when creating, editing, importing, or auditing skills.

---

## 🛠️ Quick Commands

- **Validate all skills**:
  ```bash
  ./scripts/validate_skills.py
  ```

- **Scaffold a new skill**:
  ```bash
  ./scripts/create_skill.py <skill-name> -d "<skill-description>"
  ```

---

## 🎯 Core Rules for Claude Code

1. **New Skill Creation**:
   Always run `./scripts/create_skill.py <skill-name> -d "<desc>"` first.

2. **No Extraneous Files**:
   Do NOT place `README.md` inside individual skill directories (`skills/<skill-name>/`). `SKILL.md` is the only entry point.

3. **No Hardcoded Absolute Paths**:
   Do NOT include `/Users/...` or `/home/...` in code or docs. Use relative paths or `~`.

4. **Always Validate**:
   Always execute `./scripts/validate_skills.py` before completing a task.

5. **Update Index**:
   Update the catalog table in [`README.md`](README.md) whenever adding or deleting a skill.
