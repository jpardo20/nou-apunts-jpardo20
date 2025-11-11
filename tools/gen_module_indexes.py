#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Opcional: genera docs/<modul>/index.md per a cada mòdul definit a data/modules.yml,
# amb una línia que crida la macro {{ module_index("<codi>") }}.
from pathlib import Path
import yaml

def main():
    data = Path('data/modules.yml')
    if not data.exists():
        print("⚠️  No trobo data/modules.yml")
        return
    modules = yaml.safe_load(data.read_text(encoding='utf-8')) or {}
    modules = modules.get('modules', {})
    for code in modules.keys():
        p = Path('docs') / code
        p.mkdir(parents=True, exist_ok=True)
        idx = p / 'index.md'
        idx.write_text('{{ module_index("%s") }}\n' % code, encoding='utf-8')
    print("✅ Índexs generats a docs/<modul>/index.md")

if __name__ == '__main__':
    main()
