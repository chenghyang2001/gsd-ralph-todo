# Demo 實錄：GSD 規劃 → VPS → Ralph 自主執行（todo-cli）

> 一條「本機用 GSD 把需求壓成可執行計劃 → 丟到 VPS 用 Ralph 無人值守迴圈蓋到測試全綠」的完整流水線。
> 專案：`chenghyang2001/gsd-ralph-todo` ｜ 完成日：2026-07-02
> 成果：Ralph 4 個 loop / 3 次 API call / 12,641 tokens（走 Claude Max，$0）→ **pytest 11 passed**。

---

## 0. 這個 demo 想證明什麼

**兩個框架各司其職、用 git 當交接介面：**

| 框架 | 角色 | 在哪跑 | 產出 |
|------|------|--------|------|
| **GSD**（Get Shit Done） | 規劃大腦：把模糊需求 → 結構化、機器可讀的 `PLAN.md` | 本機 PC | `.planning/`（PROJECT / ROADMAP / PLAN / SKELETON） |
| **Ralph**（frankbria/ralph-claude-code） | 執行手：讀計劃無人值守迴圈實作到測試全綠 | VPS | `todo.py` / `test_todo.py` + 自動 commit |

**核心洞見**：GSD 的 `PLAN.md` 跟「誰來施工」是**解耦**的。所以可以跳過 GSD 自己的執行器（`/gsd-execute-phase`），把施工圖原封搬去 VPS 交給 Ralph。

**App 選型原則**：越簡單越好、但能跑完整條流程。選 `todo-cli`（Python stdlib、4 個命令 add/list/done/rm、JSON 持久化、pytest 當唯一完工判準）——因為 Ralph 自主迴圈的「完工判斷」靠的是**可自動驗證的訊號**（pytest 綠），純函式 + 明確測試 > 需要人肉看畫面的東西。

---

## 1. Phase 0：準備工作區（本機）

- 開**獨立 repo** `~/workspace/gsd-ralph-todo`（`git init` + 最小 README）。
- **重點**：故意不塞進課程 repo。因為 Ralph 會在 VPS 上**自主 commit**，混進課程 repo 會讓自動提交跟課程紀錄糾纏難清理。**隔離 = 安全**。

## 2. Phase 1：GSD 規劃（本機，一步一步跑）

1. `/gsd-new-project` → 深度訪談 → `PROJECT.md` + roadmap（1 phase，10/10 需求對應）。
2. `/gsd-plan-phase 1` → 產出 `01-01-PLAN.md`（add+list）、`01-02-PLAN.md`（done+rm）、`SKELETON.md`（架構契約）。

**回答訣竅（防 scope creep 的方向盤）**：GSD 想「好心加料」（登入 / 資料庫 / Web UI）時一律回「不需要，超出範圍」。開場把範圍框死 = 幫下游 Ralph 提前綁安全帶。

**重點：GSD 用 TDD（測試先行）**——先寫失敗測試當「契約」，再實作到綠。這對 Ralph 是天作之合：**測試就是 Ralph 每輪的客觀計分板**，不用猜「做對了嗎」，跑 pytest 紅→綠就知道。

### 插曲：冒號 vs 連字號的指令命名坑

GSD 提示 `/gsd:plan-phase 1`（冒號）但實際要打 `/gsd-plan-phase 1`（連字號）。
**根因**：GSD 官方以 **plugin** 發布（命名空間 `gsd:xxx`），但本機把它攤平成**全域 skills**（`~/.claude/skills/gsd-*/`，連字號）。SKILL.md 內文**硬編碼**了冒號提示（如 `gsd-new-project/SKILL.md:33`），全套 31 處。不是顯示 bug，是「安裝命名 vs 文件硬編碼」不一致。決策：不改，記住「看到冒號打連字號」。

## 3. Phase 2：交接到 VPS

- **2a** 建 GitHub public repo + `git push`（public 讓 VPS clone 免認證）。
- **2b** SSH 上 VPS 探勘 + `git clone`。**重點：先觀測再動手**——摸清 VPS 現況（claude 有沒有裝、Ralph 是不是舊實驗殘骸）比盲目照 SOP 更省事。發現 VPS 已有 `claude 2.1.146`、`python3.12`、`~/ralph-claude-code`（Ralph 獨立版現成）。
- **2c** 驗 auth（最關鍵）：`ANTHROPIC_API_KEY` **未設**（走 Max、$0，符合 cost-rules）+ `claude -p` 實測回「OK」（auth 正常能無人值守）。
  **重點**：Ralph 每輪都呼叫 `claude`，auth 沒綠燈就會一啟動整串失敗。

## 4. Phase 3：啟動 Ralph

- **3a** `install.sh` 裝全域指令。**坑**：裝進 `~/.local/bin` 但不在 PATH，且非互動 SSH 不載入 `.bashrc`（Ubuntu `.bashrc` 開頭「非互動就 return」）。**雙修**：① 寫進 `.bashrc`（互動用）② 自動化指令每次自己 `export PATH`（非互動用）。
- **3b** 客製 `.ralph/`（Ralph 的「大腦輸入」三件套）：

  | 檔案 | 作用 |
  | ------ | ------ |
  | `.ralph/PROMPT.md` | Ralph 每輪讀的指令（目標 / 原則 / 受保護檔 / **退出規則**） |
  | `.ralph/fix_plan.md` | 任務清單（`- [ ]` 勾選，做完打 `[x]`） |
  | `.ralph/specs/` | 細部規格（放 GSD 的 PLAN + SKELETON） |

  - **3b-2A（必修坑）**：`ralph-enable-ci` 生成的 `.ralphrc` 的 `ALLOWED_TOOLS` 是 Node.js 預設（`Bash(npm *)`、`Bash(pytest)` 無參數），**沒有 `python3` / `pytest 帶參數` / `pip`**。這是 autonomous agent 的「權限 vs 能力」矛盾——護欄太緊會讓它做不了正事。精準加開 Python 指令。
  - **3b-2B**：pytest 沒裝 → `pip install --user --break-system-packages pytest`（Ubuntu 24.04 externally-managed）。
  - **3b-2C**：`TASK_SOURCES=local`（用 fix_plan.md 不撈 GitHub）、`CLAUDE_AUTO_UPDATE=false`（demo 期間別自動更新）。
  - **3b-2D**：把 GSD 的 `PLAN.md`/`SKELETON.md`/`REQUIREMENTS.md` cp 進 `.ralph/specs/`。
  - **手法重點**：`.md` 用「本機 Write + scp」避開 SSH heredoc 的引號/CJK 地獄；`.ralphrc` 用 `sed` 就地只改 3 行（最小改動，保留 circuit breaker 等預設）。

  **GSD ↔ Ralph 的接合縫**：本質是「格式翻譯」——GSD 的階層任務 `PLAN.md` → Ralph 的扁平勾選清單 `fix_plan.md` + `PROMPT.md`（目標+退出規則）。內容一樣，只換成 Ralph 迴圈看得懂的格式。

- **3c** `ralph --dry-run`：不呼叫 API 空跑，確認 config 載入、讀得到 PROMPT/fix_plan。
- **3d** 正式跑：用 **detached tmux session** 啟動（`nohup+&` 會讓 SSH channel 收不乾淨回 255；tmux 最穩、斷線續跑）。

### Ralph 怎麼知道「做完了」（退出閘門）

每輪結束 Ralph 輸出狀態塊，`EXIT_SIGNAL: true` 的條件 = **fix_plan 全勾 + pytest 全過 + specs 全實作 + 沒剩東西做**：

```
---RALPH_STATUS---
STATUS: COMPLETE
TESTS_STATUS: PASSING
EXIT_SIGNAL: true
---END_RALPH_STATUS---
```

Ralph 還內建反 scope-creep 護欄（PROMPT 裡「測試 ≤20%、Implementation > Docs > Tests、別加 busywork」）。

## 5. 執行結果

```
Loop #1  寫 11 支失敗測試（d63f486）
Loop #2  實作 add + list，Plan-01 綠（fcffcee）
Loop #3  實作 done + rm，全套 11 支綠（cc2f46e）
Loop #4  偵測 fix_plan 7/7 全勾 → graceful exit: plan_complete
```

- **pytest：11 passed in 0.73s**
- API：3 次呼叫 / 12,641 tokens / **走 Max = $0**
- 產物：`todo.py`（stdlib only，argparse/json/pathlib/sys）、`test_todo.py`（subprocess + tmp_path 隔離）

## 6. 怎麼重現

```bash
# 本機
cd ~/workspace && mkdir gsd-ralph-todo && cd $_ && git init
# （寫 REQUIREMENTS.md）
/gsd-new-project        # 訪談 → PROJECT + roadmap
/gsd-plan-phase 1       # → .planning/phases/.../PLAN.md + SKELETON.md
gh repo create ... --public --source=. --push

# VPS
git clone <repo>
cd ralph-claude-code && ./install.sh          # 全域 ralph 指令
export PATH="$HOME/.local/bin:$PATH"
cd ~/gsd-ralph-todo && ralph-enable-ci        # 搭 .ralph 骨架
# 客製 .ralph/PROMPT.md + fix_plan.md（翻自 GSD PLAN）、修 .ralphrc ALLOWED_TOOLS（加 python/pytest/pip）、cp GSD PLAN → .ralph/specs/
pip install --user --break-system-packages pytest
tmux new-session -d -s ralph "ralph --verbose"   # 自主迴圈，跑到 pytest 綠自停
```

## 7. 帶走的重點（踩過才知道）

1. **auth 先綠燈再啟動**：Ralph 每輪呼叫 `claude`，`ANTHROPIC_API_KEY` 保持未設 → 走 Max、$0；先 `claude -p` 實測。
2. **ALLOWED_TOOLS 要對到語言**：Node 預設對 Python 專案會擋死 —— 精準加 `Bash(python3 *) / Bash(pytest *) / Bash(pip *)`。
3. **規格越小、Ralph 越準**：sample-prd 那種 Todoist 級大規格會讓它蓋很久還失焦；我們的 REQUIREMENTS 刻意小。
4. **detached 用 tmux** 不要 `ssh 'cmd &'`（會回 255）。
5. **`.md`/config 用本機 Write + scp**，別在 `ssh '...'` 裡塞 heredoc。
6. **TDD 是 Ralph 的計分板**：測試先行讓「完工」變成 pytest 紅→綠的客觀訊號。
