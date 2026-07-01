"""todo-cli — single-file stdlib-only todo manager (add + list)."""

import argparse
import json
import pathlib
import sys

TASKS_PATH = pathlib.Path(__file__).resolve().parent / "tasks.json"


def load_tasks():
    if not TASKS_PATH.exists():
        return []
    try:
        with TASKS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"error: tasks.json is corrupt: {e}", file=sys.stderr)
        sys.exit(1)


def save_tasks(tasks):
    with TASKS_PATH.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def cmd_add(text):
    stripped = text.strip()
    if not stripped:
        print("error: task text must not be empty", file=sys.stderr)
        sys.exit(1)
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "text": stripped, "done": False})
    save_tasks(tasks)


def cmd_list():
    for t in load_tasks():
        mark = "x" if t["done"] else " "
        print(f"[{mark}] {t['id']} {t['text']}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("text")

    sub.add_parser("list", help="list all tasks")

    args = parser.parse_args(argv)
    if args.cmd == "add":
        cmd_add(args.text)
    elif args.cmd == "list":
        cmd_list()


if __name__ == "__main__":
    main()
