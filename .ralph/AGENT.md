# Ralph Agent Configuration — todo-cli

## Build Instructions

No build step. Pure Python 3 standard library; nothing to compile or install for the app itself.

## Test Instructions

```bash
python3 -m pytest test_todo.py -q
```

This is the sole done-gate. Green (exit 0) = phase complete.

## Run Instructions

```bash
python3 todo.py add "買牛奶"
python3 todo.py list
python3 todo.py done 1
python3 todo.py rm 1
```

## Notes

- todo.py: standard library only (argparse, json, pathlib, sys). No third-party imports.
- tasks.json is created on first `add`, in the same directory as todo.py.
- pytest is the only dev dependency (test runner):
  `python3 -m pip install --user --break-system-packages pytest`
