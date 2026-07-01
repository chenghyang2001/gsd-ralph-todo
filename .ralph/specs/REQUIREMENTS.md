# Requirements: todo-cli

**Defined:** 2026-07-02
**Core Value:** Ralph 能在無人值守下把鎖定規格自主實作到 `pytest` 全綠

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Commands

- [ ] **CMD-01**: 使用者可用 `add "<文字>"` 新增任務，id 自動遞增，初始狀態 pending
- [ ] **CMD-02**: 使用者可用 `list` 列出全部任務，格式 `[ ] 1 買牛奶` / `[x] 2 已完成事項`
- [ ] **CMD-03**: 使用者可用 `done <id>` 將指定任務標記為完成
- [ ] **CMD-04**: 使用者可用 `rm <id>` 刪除指定任務

### Data

- [ ] **DATA-01**: 任務資料模型為 `{ "id": int, "text": str, "done": bool }`
- [ ] **DATA-02**: 任務持久化於程式同目錄的 `tasks.json`

### Errors

- [ ] **ERR-01**: 對無效 id 執行 `done`/`rm` 時印出錯誤訊息並以 exit code 1 結束
- [ ] **ERR-02**: `add` 傳入空字串時拒絕並報錯
- [ ] **ERR-03**: `tasks.json` 不存在時視為空清單，不崩潰

### Tests

- [ ] **TEST-01**: `pytest test_todo.py` 全綠，涵蓋 add / list / done / rm 與邊界（空清單、無效 id、空字串）

## v2 Requirements

(None — scope 明文鎖定於 v1 4 指令，不預留 v2)

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --------- | -------- |
| 第三方依賴 | 規格要求零依賴，只用標準庫 |
| 額外指令（優先級 / 到期 / 標籤 / 編輯文字） | scope 明文「就這 4 個，不多做」 |
| 多使用者 / 網路 / 資料庫 | 單機單檔 JSON 已足夠 |
| TUI / GUI | 純 CLI |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
| ------------- | ------- | -------- |
| CMD-01 | Phase 1 | Planned |
| CMD-02 | Phase 1 | Planned |
| CMD-03 | Phase 1 | Planned |
| CMD-04 | Phase 1 | Planned |
| DATA-01 | Phase 1 | Planned |
| DATA-02 | Phase 1 | Planned |
| ERR-01 | Phase 1 | Planned |
| ERR-02 | Phase 1 | Planned |
| ERR-03 | Phase 1 | Planned |
| TEST-01 | Phase 1 | Planned |

**Coverage:**

- v1 requirements: 10 total
- Mapped to phases: 10 ✓ (fully mapped)
- Unmapped: 0

---
*Requirements defined: 2026-07-02*
*Last updated: 2026-07-02 after roadmap creation (Phase 1 covers all v1 requirements)*
