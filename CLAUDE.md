<!-- GSD:project-start source:PROJECT.md -->
## Project

**todo-cli**

一個單檔 Python CLI 待辦管理器，只用標準庫、零第三方依賴，資料存本地 `tasks.json`。它同時是 **GSD 規劃 → VPS Ralph 無人值守自主執行** 的 demo 標的：scope 刻意鎖死在 4 個指令，讓 Ralph 能自主從空專案實作到測試全綠。

**Core Value:** Ralph 能在無人值守下，把這份鎖定的規格自主實作到 `pytest test_todo.py` 全綠。

### Constraints

- **Tech stack**: Python 3 標準庫（argparse / json / pathlib / sys） — 規格要求零第三方依賴
- **Data**: JSON 檔 `tasks.json` 存於程式同目錄 — 規格明訂的持久化方式
- **Scope**: 僅 4 個指令，不擴充 — 讓 Ralph 有明確、可收斂的完工邊界
- **Done gate**: `pytest` 全綠 — 唯一的自主完工判準
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
