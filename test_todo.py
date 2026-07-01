"""End-to-end tests for todo.py — invoked as a subprocess with tmp_path isolation.

Each test copies todo.py into pytest's tmp_path so tasks.json (which lives
next to todo.py) is isolated per-test.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC = REPO_ROOT / "todo.py"


def _copy_todo(tmp_path: Path) -> Path:
    dst = tmp_path / "todo.py"
    shutil.copy2(SRC, dst)
    return dst


def run_todo(args, tmp_path):
    """Run `python todo.py <args...>` against the copy in tmp_path.

    Returns (exit_code, stdout, stderr).
    """
    todo = _copy_todo(tmp_path) if not (tmp_path / "todo.py").exists() else tmp_path / "todo.py"
    result = subprocess.run(
        [sys.executable, str(todo), *args],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


# -------- Plan 01: add / list / empty-string / missing-file / data model --------


def test_add_then_list(tmp_path):
    code, out, err = run_todo(["add", "買牛奶"], tmp_path)
    assert code == 0, f"add failed: {err}"
    code, out, err = run_todo(["list"], tmp_path)
    assert code == 0, f"list failed: {err}"
    assert "[ ] 1 買牛奶" in out


def test_add_increments_id(tmp_path):
    run_todo(["add", "買牛奶"], tmp_path)
    run_todo(["add", "洗衣服"], tmp_path)
    code, out, err = run_todo(["list"], tmp_path)
    assert code == 0
    assert "[ ] 1 買牛奶" in out
    assert "[ ] 2 洗衣服" in out


def test_add_empty_string_rejected(tmp_path):
    code, out, err = run_todo(["add", ""], tmp_path)
    assert code == 1, "empty add must exit 1"
    combined = (out + err).strip()
    assert combined != "", "expected an error message on empty add"
    tasks_json = tmp_path / "tasks.json"
    if tasks_json.exists():
        data = json.loads(tasks_json.read_text(encoding="utf-8"))
        assert data == [], "empty add must not persist any task"


def test_list_missing_tasks_json(tmp_path):
    code, out, err = run_todo(["list"], tmp_path)
    assert code == 0, f"list on empty must exit 0, got {code}: {err}"
    assert "Traceback" not in err
    assert "Traceback" not in out


def test_data_model_shape(tmp_path):
    code, _, err = run_todo(["add", "買牛奶"], tmp_path)
    assert code == 0, err
    tasks_json = tmp_path / "tasks.json"
    assert tasks_json.exists(), "tasks.json must be created on first add"
    data = json.loads(tasks_json.read_text(encoding="utf-8"))
    assert isinstance(data, list) and len(data) == 1
    task = data[0]
    assert set(task.keys()) == {"id", "text", "done"}
    assert isinstance(task["id"], int)
    assert isinstance(task["text"], str)
    assert isinstance(task["done"], bool)
    assert task["done"] is False


# -------- Plan 02: done / rm / invalid-id --------


def test_done_marks_task(tmp_path):
    run_todo(["add", "買牛奶"], tmp_path)
    code, _, err = run_todo(["done", "1"], tmp_path)
    assert code == 0, err
    code, out, _ = run_todo(["list"], tmp_path)
    assert code == 0
    assert "[x] 1 買牛奶" in out


def test_done_persists(tmp_path):
    run_todo(["add", "買牛奶"], tmp_path)
    run_todo(["done", "1"], tmp_path)
    # A fresh subprocess — same tmp_path/todo.py, so same tasks.json
    code, out, _ = run_todo(["list"], tmp_path)
    assert code == 0
    assert "[x] 1 買牛奶" in out


def test_rm_removes_task(tmp_path):
    run_todo(["add", "買牛奶"], tmp_path)
    run_todo(["add", "洗衣服"], tmp_path)
    code, _, err = run_todo(["rm", "1"], tmp_path)
    assert code == 0, err
    code, out, _ = run_todo(["list"], tmp_path)
    assert code == 0
    assert "買牛奶" not in out
    assert "[ ] 2 洗衣服" in out


def test_rm_persists(tmp_path):
    run_todo(["add", "買牛奶"], tmp_path)
    run_todo(["rm", "1"], tmp_path)
    code, out, _ = run_todo(["list"], tmp_path)
    assert code == 0
    assert "買牛奶" not in out


def test_done_invalid_id(tmp_path):
    run_todo(["add", "買牛奶"], tmp_path)
    code, out, err = run_todo(["done", "999"], tmp_path)
    assert code == 1, "done on nonexistent id must exit 1"
    assert (out + err).strip() != ""


def test_rm_invalid_id(tmp_path):
    run_todo(["add", "買牛奶"], tmp_path)
    code, out, err = run_todo(["rm", "999"], tmp_path)
    assert code == 1, "rm on nonexistent id must exit 1"
    assert (out + err).strip() != ""
