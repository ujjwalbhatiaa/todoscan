# todoscan

Find TODO / FIXME / HACK / XXX markers hiding in a source tree. Zero dependencies, one file.

```
python3 todoscan.py [PATH]           # list every marker as file:line: TAG text
python3 todoscan.py --summary        # counts per tag
python3 todoscan.py --tags TODO,BUG  # custom tag set
```

Skips `.git`, `node_modules`, virtualenvs and build dirs; reads ~20 common text formats.
Exit code is 1 when markers are found (grep-style), so it drops into pre-commit hooks and CI.
