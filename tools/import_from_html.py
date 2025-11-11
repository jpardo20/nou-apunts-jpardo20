#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Scaneja un bolcat local del site antic i suggereix entrades per a data/modules.yml.
# - Detecta carpetes de mòdul pel patró de codi (ex: 0221, 0484, M1709...)
# - Cerca HTML dins subcarpetes 'presentacions' i 'activitats' i genera títols a partir de <title> o del nom de fitxer.
# - Per defecte NO copia fitxers a docs/, només genera YAML. Pots activar --copy-to-docs per copiar-los.
import argparse, re, shutil
from pathlib import Path
from bs4 import BeautifulSoup
import yaml

MOD_CODE_RE = re.compile(r'^(M?\d{3,4})')

def guess_title(html_path: Path) -> str:
    try:
        txt = html_path.read_text(encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(txt, 'lxml')
        if soup.title and soup.title.string:
            return soup.title.string.strip()
    except Exception:
        pass
    return html_path.stem.replace('-', ' ').replace('_', ' ').strip()

def rel_url_for_docs(target: Path) -> str:
    # URL relativa pensada per MkDocs (docs/ és l'arrel del site)
    # Converteix docs/xyz/file.html -> /xyz/file.html
    parts = list(target.parts)
    if parts and parts[0] == 'docs':
        parts = parts[1:]
    return '/' + '/'.join(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='legacy_site', help='Carpeta amb el bolcat del site antic')
    ap.add_argument('--write', choices=['modules'], default='modules', help='Què generar')
    ap.add_argument('--copy-to-docs', action='store_true', help='Copia HTML i assets detectats a docs/')
    ap.add_argument('--fix-fetch', action='store_true', help='Reescriu fetch(...) cap a /apunts-jpardo20/assets/...')
    args = ap.parse_args()

    site = Path(args.root)
    if not site.exists():
        print(f'⚠️  No trobo la carpeta: {site.resolve()}')
        return

    docs = Path('docs')
    (docs / 'moduls').mkdir(parents=True, exist_ok=True)
    assets_alumnes = docs / 'assets' / 'alumnes'
    assets_alumnes.mkdir(parents=True, exist_ok=True)

    data_path = Path('data/modules.yml')
    modules = {'modules': {}}
    if data_path.exists():
        modules = yaml.safe_load(data_path.read_text(encoding='utf-8')) or {'modules': {}}

    for child in site.iterdir():
        if not child.is_dir():
            continue
        m = MOD_CODE_RE.match(child.name)
        if not m:
            continue
        code = m.group(1)
        mod_entry = modules['modules'].setdefault(code, {'title': f'Mòdul {code}', 'theory': [], 'activities': []})

        # Busca subcarpetes
        for kind in ('presentacions', 'activitats', 'presentations', 'activities'):
            kpath = child / kind
            if not kpath.exists():
                continue
            for html in kpath.rglob('*.html'):
                title = guess_title(html)
                if args.copy_to_docs:
                    # Copia a docs/moduls/<code>/<kind>/
                    dest = docs / 'moduls' / code / kind / html.name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(html, dest)
                    url = rel_url_for_docs(dest)
                else:
                    # Manté la URL original relativa al site antic (serà avaluada a mà)
                    url = f'/apunts-jpardo20/{code}/{kind}/{html.name}'

                entry = {'title': title, 'desc': '', 'url': url}
                if 'act' in kind:  # activitats
                    mod_entry['activities'].append(entry)
                else:
                    mod_entry['theory'].append(entry)

    # Escriu modules.yml
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(yaml.safe_dump(modules, allow_unicode=True, sort_keys=True), encoding='utf-8')
    print(f'✅ Actualitzat {data_path}')

    if args.copy_to_docs and args.fix_fetch:
        # crida al fixer
        import subprocess, sys
        subprocess.run([sys.executable, 'tools/fix_fetch_paths.py', 'docs'], check=False)

if __name__ == '__main__':
    main()
