# Roadmap: todo-cli

## Overview

一個單一、範圍鎖死的交付：Ralph（VPS 上的無人值守自主 loop）從空專案出發，實作出零依賴的 Python 標準庫 CLI 待辦管理器（`todo.py` + `test_todo.py`），涵蓋 `add` / `list` / `done` / `rm` 四個指令、JSON 持久化與邊界錯誤處理，直到 `pytest test_todo.py` 全綠為止。因為 scope 極小且 granularity 為 coarse，10 個 v1 需求全部收斂在單一 phase 內一次交付，沒有中間依賴需要拆分。

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Core Todo CLI** - 實作 add/list/done/rm 四指令 + JSON 持久化 + 錯誤處理，`pytest test_todo.py` 全綠

## Phase Details

### Phase 1: Core Todo CLI

**Goal**: 使用者（及自主執行的 Ralph）可透過單一 `todo.py` 標準庫 CLI 完成任務的新增、列出、標記完成、刪除，資料持久化於 `tasks.json`，所有邊界情況（無效 id、空字串、檔案不存在）皆有正確錯誤處理，且測試套件 `pytest test_todo.py` 全綠作為唯一完工判準。
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: CMD-01, CMD-02, CMD-03, CMD-04, DATA-01, DATA-02, ERR-01, ERR-02, ERR-03, TEST-01
**Success Criteria** (what must be TRUE):

  1. 使用者執行 `add "<文字>"` 可新增任務，id 自動遞增，初始狀態為 pending（CMD-01, DATA-01, DATA-02）
  2. 使用者執行 `list` 可看到全部任務，格式為 `[ ] 1 買牛奶` / `[x] 2 已完成事項`（CMD-02, DATA-01）
  3. 使用者執行 `done <id>` 與 `rm <id>` 可分別標記完成與刪除指定任務，且變更持久化於 `tasks.json`（CMD-03, CMD-04, DATA-02）
  4. 對無效 id 執行 `done`/`rm`、對 `add` 傳入空字串、或 `tasks.json` 不存在時，程式分別回報錯誤（exit code 1）或視為空清單而不崩潰（ERR-01, ERR-02, ERR-03）
  5. `pytest test_todo.py` 執行全綠，涵蓋四指令與上述所有邊界情況（TEST-01）
**Plans**: TBD

Plans:

- [ ] 01-01: TBD (refined during planning)

## Progress

**Execution Order:**
Phases execute in numeric order: 1

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Todo CLI | 0/TBD | Not started | - |
