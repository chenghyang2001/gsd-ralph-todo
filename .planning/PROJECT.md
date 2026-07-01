# todo-cli

## What This Is

一個單檔 Python CLI 待辦管理器，只用標準庫、零第三方依賴，資料存本地 `tasks.json`。它同時是 **GSD 規劃 → VPS Ralph 無人值守自主執行** 的 demo 標的：scope 刻意鎖死在 4 個指令，讓 Ralph 能自主從空專案實作到測試全綠。

## Core Value

Ralph 能在無人值守下，把這份鎖定的規格自主實作到 `pytest test_todo.py` 全綠。

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

(None yet — ship to validate)

### Active

<!-- Current scope. Building toward these. -->

- [ ] `add "<文字>"` — 新增任務，id 自動遞增，狀態 pending
- [ ] `list` — 列出全部（`[ ] 1 買牛奶` / `[x] 2 已完成事項`）
- [ ] `done <id>` — 標記完成
- [ ] `rm <id>` — 刪除任務
- [ ] 錯誤處理：無效 id、空字串、`tasks.json` 不存在
- [ ] `pytest test_todo.py` 全綠（涵蓋 4 指令 + 邊界）

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- 第三方依賴 — 規格要求零依賴，只用 argparse / json / pathlib / sys
- 任何額外指令（優先級 / 到期日 / 標籤 / 編輯文字等）— scope 明文「就這 4 個，不多做」
- 多使用者 / 網路 / 資料庫 — 單機單檔 JSON 已足夠
- TUI / GUI — 純 CLI

## Context

- 本專案是 GSD workflow demo，規格已由使用者事先寫死在根目錄 `REQUIREMENTS.md`（"scope 就是這些，不多做"）。
- 下游 Ralph 自主 loop 依賴 pytest 全綠作為唯一完工訊號，因此測試覆蓋是硬需求。
- 技術環境：Python 3，Windows 開發、可能於 VPS（Linux）執行；路徑用 `pathlib`，`tasks.json` 放程式同目錄。

## Constraints

- **Tech stack**: Python 3 標準庫（argparse / json / pathlib / sys） — 規格要求零第三方依賴
- **Data**: JSON 檔 `tasks.json` 存於程式同目錄 — 規格明訂的持久化方式
- **Scope**: 僅 4 個指令，不擴充 — 讓 Ralph 有明確、可收斂的完工邊界
- **Done gate**: `pytest` 全綠 — 唯一的自主完工判準

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
| ---------- | ----------- | --------- |
| 單檔 `todo.py` + `test_todo.py` 兩檔結構 | 規格指定；最小化 Ralph 需管理的檔案數 | — Pending |
| 快速通道初始化（跳過訪談 / 研究） | 規格已鎖定，深度訪談與領域研究對 4 指令 CLI 零槓桿 | — Pending |
| Coarse 粒度 + YOLO 模式 | 專案極小且為無人值守 demo，宜單一寬 phase 自動執行 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):

1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):

1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-07-02 after initialization*
