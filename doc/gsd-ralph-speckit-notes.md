# GSD / Ralph / Spec Kit 對比筆記

> 整理自 gsd-ralph-todo session（2026-07-03）。三個主題：執行方式、產規格方式、brownfield 適用性。

---

## 一、gsd-execute-phase（GSD） vs Ralph standalone

核心：**GSD 用「結構」換確定性；Ralph 用「邊界」換自主性。**

| 面向 | GSD（gsd-execute-phase） | Ralph standalone |
| ------ | -------------------------- | ------------------ |
| 哲學 | 規劃先行、人在迴圈裡 | 無人值守、暴力迴圈收斂 |
| 前置條件 | 必須先有 PLAN.md（先 plan-phase） | 一份鎖定規格 + 一個 done gate |
| 執行方式 | 派 gsd-executor 分波執行、atomic commit、deviation handling、checkpoint | 單一 prompt 反覆自呼叫（讀狀態→做下一件事→檢查 done gate→重複） |
| 驗證 | gsd-verifier 做 goal-backward（任務完成 ≠ 目標達成） | done gate 自己就是判準（本專案 = pytest 全綠） |
| 防呆 | 階段 gate + 驗證 loop | circuit breaker（防無限迴圈燒錢） |
| 成本 | 較重（多 subagent + 驗證 + 狀態管理） | 極輕（本 demo：4 loops / 3 API calls / ~12,641 tokens） |

**選型**：需要人決策 / 多階段 / 會演化 → GSD；規格已鎖死、有明確 done gate、想丟 VPS 無人值守 → Ralph。

**備註**：本專案 scope 刻意鎖死（4 指令、零依賴、pytest 全綠 = 唯一 done gate），正是讓 Ralph 能自主收斂的必要條件。實務常見組合：**GSD 規劃 → Ralph 無人執行**。

---

## 二、GSD 產鎖定規格 vs Spec Kit 產鎖定規格

定位：**Spec Kit** 是 GitHub 出的輕量、agent 無關的「規格驅動開發」工具組；**GSD** 是 opinionated 全生命週期框架（roadmap→milestone→phase→plan→execute→verify）。

**Spec Kit 流程**

```
/constitution → 專案原則（護欄）
/specify      → spec.md（只寫 WHAT/WHY，不碰技術）
/clarify      → 結構化問答消歧
/plan         → plan.md（才決定 HOW / tech stack）
/tasks        → tasks.md（扁平、有序、可勾選清單）
/analyze      → 跨檔一致性 gate
/implement    → 執行
```

**GSD 流程**

```
/gsd:new-project → PROJECT.md → roadmap 切 phases
/gsd:discuss-phase → 自適應提問
/gsd:plan-phase    → PLAN.md + 驗證 loop（gsd-plan-checker）
/gsd:execute-phase → 分波派 gsd-executor
/gsd:verify-work   → gsd-verifier 驗目標達成
```

| 面向 | Spec Kit | GSD |
| ------ | ---------- | ----- |
| 規格產物 | spec.md + plan.md + tasks.md | 規格內嵌 PLAN.md |
| WHAT/HOW 分離 | 強制分離 | 較融合 |
| 鎖定機制 | 三檔一致性 + constitution 護欄 | phase 目標 + goal-backward 驗證 |
| agent 綁定 | 無關（多家 AI 可吃） | 綁專屬 agents |
| 人的介入 | 偏輕 | 偏重 |

**對「餵 Ralph」而言**：Spec Kit 的 `tasks.md` 是更天然的交棒物（有序、有驗收準則、可勾選、agent 無關），對上 Ralph 無狀態暴力迴圈；GSD 強項（roadmap、跨 phase 整合、自帶 verifier）對鎖死小 demo 是 overkill。

**選型**：要乾淨 / agent 無關 / WHAT/HOW 分離 / 直接產可餵 Ralph 的 tasks.md → Spec Kit；要 roadmap / 多 milestone / 跨 phase 整合 / 內建驗證 → GSD。

---

## 三、Spec Kit 能用在 brownfield（既有專案）嗎？

**能，官方明確支援**（三大使用情境之一 = Iterative Enhancement / brownfield：既有系統加功能、現代化 legacy、調整既有流程）。但有痛點。

**怎麼用**

- `specify init --here`（或 `.`）在既有 repo 就地初始化，不建新資料夾、不動現有碼。
- 用 `/constitution` 鎖住既有慣例（tech stack / 目錄結構 / coding style / 不可破壞約束）當護欄。
- **per-feature，不是 per-system**：一次規格化一個新功能，而不是想用一份 spec 描述整個既有系統。
- `/plan` 這步會實際讀既有碼、對齊現有 stack（前提是相關檔案在 agent 讀得到範圍內）。

**brownfield 特有痛點**

1. **沒有專門的「既有碼盤點」步驟** —— 理解舊碼靠背後 coding agent 在 /plan、/implement 時去讀，大型/雜亂 codebase 上常常 context 不夠，要人工餵關鍵檔。
2. **產出的 tasks 可能不尊重既有 pattern**（偏乾淨新建思維），要靠 constitution + 人工審 tasks.md 收斂。
3. **spec 的 tech-agnostic 特性在 brownfield 有點彆扭**（stack 已綁死，WHAT/HOW 分離價值下降），重點落在 /plan 對齊既有實作。

**一句話結論**

- 既有專案 + 對「單一新功能」做規格驅動 → Spec Kit 完全可行。
- 既有專案 + 需先大規模理解/盤點舊碼、對映既有 pattern → GSD 佔優（有 gsd-map-codebase / code-explorer / pattern-mapper），Spec Kit 這塊要人工補 context。

---

## 三個 Insight

1. **鎖定的「形狀」不同**：Spec Kit 是文件一致性式鎖定，GSD 是目標達成式鎖定。
2. **WHAT/HOW 分離是 Spec Kit 招牌**：spec.md 不寫技術，避免過早綁死實作。
3. **給 Ralph 用，tasks.md > PLAN.md**：規格越像扁平 checklist，Ralph 越好收斂。
4. **「支援 brownfield」≠「brownfield 最佳工具」**：Spec Kit 骨架為 0→1 設計，既有碼理解外包給 coding agent；brownfield 正是 GSD 相對佔優的場景。
