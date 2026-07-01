# Fix Plan — todo-cli（來源：.ralph/specs/ 的 GSD PLAN 01-01 / 01-02）

## Priority 1：Walking Skeleton（add + list）

- [x] 寫「會失敗」的 test_todo.py（用 subprocess 跑真 CLI，tmp_path 隔離）：add→list 顯示「[ ] 1 買牛奶」、連續 add 的 id 自動遞增、空字串 add 退出碼 1、缺 tasks.json 時 list 退出碼 0 不崩潰、資料模型 {id:int, text:str, done:bool}
- [x] 實作 todo.py：argparse 子命令 add/list、load_tasks/save_tasks（tasks.json 放 `Path(__file__).resolve().parent`）、cmd_add（strip 後空字串→stderr+exit 1）、cmd_list（格式 `[ ] {id} {text}` / `[x] {id} {text}`）
- [x] Plan-01 測試轉綠：`python3 -m pytest test_todo.py -q` 退出碼 0（Plan-01 的 5 支綠；Plan-02 的 6 支仍紅，待下一個優先級）

## Priority 2：補完命令（done + rm）

- [x] 擴充 test_todo.py：done 標成 [x] 且跨程序持久化、rm 移除且持久化、done 999 / rm 999（不存在的 id）→ 退出碼 1（P1 撰寫時已一併寫入，紅燈確認）
- [ ] 實作 cmd_done / cmd_rm（無效 id → stderr + exit 1；沿用 load_tasks/save_tasks），註冊子命令（id 用 type=int）
- [ ] 全套綠：`python3 -m pytest test_todo.py -q` 退出碼 0（4 命令 + 邊界全過）

## 硬約束（不可違反）

- todo.py 只 import argparse/json/pathlib/sys；pytest 只當測試執行器
- 恰好 4 命令：add/list/done/rm，不可加第 5 個命令或旗標
- tasks.json 放程式自己的目錄（Path(__file__).resolve().parent）
- done-gate = `python3 -m pytest test_todo.py -q` 全綠

## Completed

- [x] Project enabled for Ralph（ralph-enable-ci）

## Discovered
<!-- Ralph 自己把過程中發現的任務補在這 -->
