#!/usr/bin/env python3
"""todoscan - find TODO/FIXME/HACK/XXX comments in source trees.

Usage: todoscan [PATH] [--tags TODO,FIXME] [--summary]
Zero dependencies, single file, Python 3.8+.
"""
import argparse, os, re, sys

DEFAULT_TAGS = ("TODO", "FIXME", "HACK", "XXX")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
TEXT_EXT = {".py", ".js", ".ts", ".java", ".c", ".h", ".cpp", ".go", ".rs",
            ".rb", ".sh", ".md", ".txt", ".yaml", ".yml", ".toml", ".css", ".html"}

def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1] in TEXT_EXT:
                yield os.path.join(dirpath, fn)

def scan(path, tags):
    pat = re.compile(r"\b(" + "|".join(tags) + r")\b[:\s]?(.*)", re.IGNORECASE)
    hits = []
    for fp in iter_files(path):
        try:
            with open(fp, encoding="utf-8", errors="ignore") as f:
                for n, line in enumerate(f, 1):
                    m = pat.search(line)
                    if m:
                        hits.append((fp, n, m.group(1).upper(), m.group(2).strip()[:80]))
        except OSError:
            pass
    return hits

def main():
    ap = argparse.ArgumentParser(prog="todoscan")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--tags", default=",".join(DEFAULT_TAGS))
    ap.add_argument("--summary", action="store_true", help="counts per tag only")
    a = ap.parse_args()
    tags = [t.strip().upper() for t in a.tags.split(",") if t.strip()]
    hits = scan(a.path, tags)
    if a.summary:
        from collections import Counter
        for tag, c in sorted(Counter(h[2] for h in hits).items()):
            print(f"{tag:6} {c}")
        print(f"total  {len(hits)}")
    else:
        for fp, n, tag, text in sorted(hits):
            print(f"{fp}:{n}: {tag} {text}")
        print(f"\n{len(hits)} marker(s)", file=sys.stderr)
    return 1 if hits else 0

if __name__ == "__main__":
    sys.exit(main())
