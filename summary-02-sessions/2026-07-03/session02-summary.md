# Session 02 — Summary

**日期**：2026-07-03
**主機**：NB00547
**主題**：GSD/Ralph/Spec Kit 概念釐清 + google-docs MCP auth 修復 + 垃圾檔規則 + worktree 關聯教學 + 明日提醒排程

---

## 完成事項

### 1. 三組概念釐清（純問答，無寫碼）

- **gsd-execute-phase vs Ralph standalone**：GSD 用「結構」換確定性（規劃先行、人在迴圈、gsd-executor 分波、goal-backward 驗證）；Ralph 用「邊界」換自主性（無人值守暴力迴圈、done gate 自證、circuit breaker）。
- **GSD 產鎖定規格 vs Spec Kit 產鎖定規格**：Spec Kit（GitHub、agent 無關、WHAT/HOW 強制分離、spec.md+plan.md+tasks.md、/analyze 一致性 gate）；GSD（opinionated 全生命週期、規格內嵌 PLAN.md、goal-backward 驗證）。對餵 Ralph 而言 `tasks.md` > `PLAN.md`。
- **Spec Kit 能否用於 brownfield**：能（官方 Iterative Enhancement 情境），`specify init --here` 就地初始化、per-feature 而非 per-system；痛點是沒有專門的「既有碼盤點」步驟，這塊 GSD 佔優（gsd-map-codebase / code-explorer / pattern-mapper）。

### 2. google-docs MCP auth 修復（本 session 最大工程）

- 症狀：`mcp__google-docs__sendEmail` 回 `invalid_grant`。
- 根因：OAuth app 停在 **Testing 發布模式** → refresh token ~7 天過期（`refresh_token_expires_in: 604799`），2026-06-18 即失效。
- 修法：跑套件內建 `google-docs-mcp auth` loopback OAuth（起 localhost 隨機 port、印同意網址、使用者點擊授權）→ 寫入全新 `token.json`。
- 關鍵坑：**正在跑的 MCP server 記憶體抓舊 token、不重讀檔案** → 當下 MCP 仍失敗。改用「繞過 MCP、`NODE_PATH` 指向套件 node_modules、用 googleapis 讀新 refresh_token 直接呼叫 Gmail API」寄成功。
- 寄出兩封信：`19f26d523808f678`（GSD/Ralph/Spec Kit 前兩題）、`19f26e0382462577`（含 brownfield 完整筆記）。

### 3. 垃圾檔規則（全域 + 專案）

- 刪除 `bash.exe.stackdump`；專案 `.gitignore` 加 `*.stackdump` / `core` / `*.core` / `*.dmp`（commit `e54404e`）。
- 新增全域規則 `~/.claude/instructions/junk-files-gitignore.md`，並在 `~/.claude/CLAUDE.md` 掛 `@import`。
- 同步到 repo mirror `~/instructions/junk-files-gitignore.md` + `~/CLAUDE.md`；rebase 時發現「patch already upstream」（另一台機器已推同樣規則）。
- 使用者原說寫進 `~/.claude/rules`，我糾正為 `instructions/`（裸 `rules/` 不會被 CLAUDE.md 載入），使用者接受。

### 4. worktree 關聯教學（純問答）

- 結論：**沒有原生 frontmatter flag**（無 `worktree: true`）能綁 skill/subagent 到 worktree。兩條路：路1（寫進本體，指示跑 git worktree）＝ /code-session；路2（呼叫時 `isolation:"worktree"`）＝ Commander agent 實戰。

### 5. 明日提醒排程

- 建 Google Calendar 事件（`pfg4upkmds944sq2oc5e2cqfm8`，07-04 03:00 台北，popup+email 提醒）。
- 建 Gmail cloud routine（`trig_0118CsSSpbLnFEJ1z5U2nTT7`，07-03T19:00Z 觸發寄提醒信）。
- 內容：明早在本機建 `worktree-builder` subagent + `wt-feature` skill（走三 agent 鐵律）。

---

## 關鍵技術筆記

- **雙層 auth 獨立**：claude.ai 連接器（Calendar/Gmail/Drive）與 `@a-bonus/google-docs-mcp` 是**不同 auth**。google-docs token 死掉時，claude.ai Calendar 連接器仍可用 → 日曆事件直接建成功。
- **Testing 模式 = 7 天過期**：根治要到 Google Cloud Console 把 OAuth app 發布狀態改 Production。
- **MCP server 記憶體 token**：re-auth 後 MCP 當下仍失敗，需 `/mcp` 重連或重啟 Claude Code；或繞過 MCP 直接呼 API。
- **home repo 邊界**：`C:/Users/B00332` 是 repo（remote `.claude.git`），只追蹤 `CLAUDE.md` + `instructions/`；`.claude/` 子目錄不被此 repo 追蹤。commit 時只 `git add` 具名檔，避免掃進 secrets（`.bashrc_secrets` 等）。

---

## 產出檔案

| 檔案 | 動作 | commit |
| ------ | ------ | -------- |
| `doc/gsd-ralph-speckit-notes.md` | 新增（三主題對比筆記） | `c06d8cd` |
| `.gitignore` | 更新（垃圾檔排除） | `e54404e` |
| `~/.claude/instructions/junk-files-gitignore.md` | 新增（全域規則） | — |
| `~/.claude/CLAUDE.md` | 更新（@import） | — |
| `~/instructions/junk-files-gitignore.md` | 新增（mirror，已 upstream） | `.claude.git` |
| `~/.claude/projects/.../memory/google-docs-mcp-auth-fix.md` | 新增（救援 SOP） | — |
| `~/.claude/projects/.../memory/MEMORY.md` | 更新（索引） | — |

---

## HANDOFF（下次 session 優先處理）

### 立即行動

- [ ] **明早（07-04）建兩個檔**：`~/.claude/agents/worktree-builder.md`（subagent）+ `wt-feature` skill（SKILL.md），走三 agent 鐵律 writer→QA→reviewer，先確認複雜度。參考 `doc/gsd-ralph-speckit-notes.md` 與日曆事件/提醒信內容。
- [ ] （選）到 Google Cloud Console 把 google-docs OAuth app 發布狀態改 **Production**，根治 7 天過期。
- [ ] （選）若要用 MCP 的 `sendEmail`，先 `/mcp` 重連 google-docs 或重啟 Claude Code 讓它讀新 token。

### 進行中（需接續）

- worktree-builder / wt-feature 兩檔尚未建立，已排程明早提醒（日曆 + Gmail routine）。
- 完整規格與範例（Example A/B）已存於 `doc/gsd-ralph-speckit-notes.md` 與提醒內容。

### 注意事項

- google-docs MCP 這條的救援 SOP 已存記憶 `google-docs-mcp-auth-fix.md`，遇 `invalid_grant` 直接照做。
- 明早建檔屬全域 `~/.claude/`，不在本專案 repo；commit 時注意 home repo 只 `git add` 具名檔。
- 本專案 scope 仍鎖死（4 指令、pytest 綠 = done gate），worktree 兩檔屬全域工具，與本 demo repo 無關。
