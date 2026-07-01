# Walking Skeleton — todo-cli

**Phase:** 1
**Generated:** 2026-07-02

## Capability Proven End-to-End

A user (or the autonomous Ralph loop) can run `python todo.py add "買牛奶"` and then `python todo.py list` to see `[ ] 1 買牛奶`, with the task persisted in `tasks.json` — proving the full stack (argv parsing -> command dispatch -> JSON persistence -> formatted output) works in a zero-dependency, standard-library-only CLI.

## Architectural Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Language / runtime | Python 3, standard library only (`argparse`, `json`, `pathlib`, `sys`) | REQUIREMENTS mandates zero third-party deps; these four modules cover parsing, persistence, paths, and exit codes |
| Structure | Single file `todo.py` + single test file `test_todo.py` | Spec-locked two-file layout; minimizes what Ralph must manage and keeps the done-gate trivial |
| Data layer | Single JSON file `tasks.json` | DATA-02 requires local JSON persistence; a list of `{"id":int,"text":str,"done":bool}` objects (DATA-01) |
| Store location | `Path(__file__).resolve().parent / "tasks.json"` | DATA-02 requires the program's OWN directory; resolving from `__file__` is portable (no hardcoded user path) and independent of cwd |
| Command dispatch | `argparse` subparsers: `add`, `list`, `done`, `rm` | Exactly the 4 locked commands; argparse gives free usage/error handling and int coercion for ids |
| Error contract | Print to stderr + `sys.exit(1)` on invalid id / empty text; missing store -> empty list | ERR-01/ERR-02/ERR-03; predictable exit codes are the machine-checkable signal for Ralph |
| Done-gate | `pytest test_todo.py` green | TEST-01 — the single objective completion criterion; pytest is the only dev dependency, never imported by `todo.py` |
| List format | `[ ] {id} {text}` pending, `[x] {id} {text}` done | CMD-02 exact format |

## Stack Touched in Phase 1

- [x] Project scaffold — `todo.py` with `argparse` dispatch + `if __name__ == "__main__"` entry (Plan 01)
- [x] Routing — command dispatch via argparse subparsers (`add`/`list` in Plan 01, `done`/`rm` in Plan 02)
- [x] Storage — real read (`load_tasks`) AND real write (`save_tasks`) against `tasks.json` (Plan 01)
- [x] User interaction — CLI add creates a task; list renders it; done/rm mutate it (Plans 01 + 02)
- [x] Run command — `python todo.py <cmd>`; full-stack test via `pytest test_todo.py` (both plans)

## Out of Scope (Deferred — do NOT re-litigate)

- Any third-party dependency (only stdlib in `todo.py`; pytest only as test runner)
- Any command beyond `add` / `list` / `done` / `rm` (no priority, due date, tags, edit-text)
- Multi-user, networking, database, TUI/GUI
- Concurrency / file locking on `tasks.json` (single-user, single-process assumption)

## Subsequent Slice Plan

This project is a single locked phase; there are no later phases. Within Phase 1 the slices are:

- Plan 01-01: `add` + `list` + JSON persistence + empty-string/missing-file handling (Walking Skeleton).
- Plan 01-02: `done` + `rm` + invalid-id error handling, extending the same load/save/dispatch contract to a fully green suite.
