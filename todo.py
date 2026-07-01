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


def cmd_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            return
    print(f"error: no task with id {task_id}", file=sys.stderr)
    sys.exit(1)


def cmd_rm(task_id):
    tasks = load_tasks()
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        print(f"error: no task with id {task_id}", file=sys.stderr)
        sys.exit(1)
    save_tasks(remaining)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("text")

    sub.add_parser("list", help="list all tasks")

    p_done = sub.add_parser("done", help="mark a task as done")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="remove a task")
    p_rm.add_argument("id", type=int)

    args = parser.parse_args(argv)
    if args.cmd == "add":
        cmd_add(args.text)
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "done":
        cmd_done(args.id)
    elif args.cmd == "rm":
        cmd_rm(args.id)


if __name__ == "__main__":
    main()
