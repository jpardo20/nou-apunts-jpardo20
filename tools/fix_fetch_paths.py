#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Cerca 'fetch('alumnes/...')' o rutes similars dins HTML i les reescriu cap a '/apunts-jpardo20/assets/alumnes/...'
# També pot moure JSON d'alumnes a docs/assets/alumnes/ si els detectes manualment.
import sys, re
from pathlib import Path

FETCH_RE = re.compile(r"fetch\(['\"](?!https?://)([^'\"\)]*alumnes/[^'\"\)]*)['\"]\)")

BASE = "/apunts-jpardo20"

def fix_file(p: Path) -> bool:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    def repl(m):
        tail = m.group(1).split('alumnes/', 1)[1]
        return f"fetch('{BASE}/assets/alumnes/{tail}')"
    new = FETCH_RE.sub(repl, txt)
    if new != txt:
        p.write_text(new, encoding='utf-8')
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Ús: fix_fetch_paths.py <carpeta>")
        sys.exit(1)
    base = Path(sys.argv[1])
    changed = 0
    for html in base.rglob('*.html'):
        if fix_file(html):
            changed += 1
    print(f"✅ Fitxers HTML actualitzats: {changed}")

if __name__ == '__main__':
    main()
