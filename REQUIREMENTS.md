# todo-cli 需求規格

> 給 GSD 規劃訪談與 Ralph 自主執行參照。**scope 就是這些，不多做**。

## 目標

一個單檔 Python CLI 待辦管理器，無人值守可由 Ralph 自主實作到測試全綠。

## 技術約束

- Python 3，只用標準庫（argparse / json / pathlib / sys），零第三方依賴
- 資料存 JSON 檔 `tasks.json`（放程式同目錄）

## 功能（就這 4 個，不多做）

| 指令 | 行為 |
| ------ | ------ |
| `add "<文字>"` | 新增任務，id 自動遞增，狀態 pending |
| `list` | 列出全部，格式：`[ ] 1 買牛奶` / `[x] 2 已完成事項` |
| `done <id>` | 標記完成 |
| `rm <id>` | 刪除任務 |

## 資料模型

```
task = { "id": int, "text": str, "done": bool }
```

## 錯誤處理

- 無效 id → 印錯誤訊息、exit code 1
- `add` 空字串 → 拒絕並報錯
- `tasks.json` 不存在 → 視為空清單（不崩潰）

## 測試

- `pytest test_todo.py`，涵蓋 add / list / done / rm + 邊界（空清單、無效 id）

## 檔案結構

- `todo.py`（主程式）
- `test_todo.py`（測試）

## 完工定義

**pytest 全綠**
