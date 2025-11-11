# nou-apunts-jpardo20

Repositori base amb **MkDocs + Material**, indexos centralitzats per mòdul i **cards diferenciades** per *Teoria* i *Activitats*.

## Què inclou
- **Macros (`main.py`)**: `{{ module_index("<codi>") }}` pinta l'índex del mòdul amb dues pestanyes (Teoria/Activitats) i targetes diferenciades.
- **`data/modules.yml`**: fitxer **únic** on hi ha totes les entrades (títol, descripció, URL) de tots els mòduls.
- **CSS** (`docs/assets/stylesheets/extra.css`): estil diferenciat molt clar per Teoria i Activitats.
- **Eines** a `tools/`:
  - `import_from_html.py`: llegeix un **bolcat local** del teu site antic (carpeta `legacy_site/`) i genera/actualitza `data/modules.yml` extraient títols de `<title>` o del nom de fitxer.
  - `fix_fetch_paths.py`: reescriu `fetch('alumnes/...')` a `fetch('/apunts-jpardo20/assets/alumnes/...')` i mou els JSON d'alumnes a `docs/assets/alumnes/`.
  - `gen_module_indexes.py` (opcional): genera `docs/<modul>/index.md` si prefereixes fitxers físics en lloc d'usar la macro (no cal si uses `{{ module_index() }}`).

## Instal·lació i ús
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (Opcional) Col·loca el bolcat del site antic aquí:
# nou-apunts-jpardo20/legacy_site/  <-- contingut HTML/CSS/JS del lloc antic

# Importa continguts a data/modules.yml (no mou fitxers HTML per defecte, només referències)
python tools/import_from_html.py --root legacy_site --write modules

# (Opcional) Copia HTML i assets dels mòduls a docs/ i arregla rutes fetch(...)
# - Això crearà docs/moduls/<code>/** i actualitzarà rutes de JSON d'alumnes
python tools/import_from_html.py --root legacy_site --copy-to-docs --fix-fetch
python tools/fix_fetch_paths.py docs

# Serveix en local
mkdocs serve

# Publica a GitHub Pages
mkdocs gh-deploy --force
```

## Com afegir un mòdul nou
1. Afegeix una entrada a `data/modules.yml` amb el codi del mòdul.
2. Crea `docs/<codi>/index.md` amb només:
   ```
   {{ '{{ module_index("<codi>") }}' }}
   ```
3. Afegeix presentacions/activitats al YAML; les targetes es pinten soles.

## Estructura
```
nou-apunts-jpardo20/
├─ data/
│  └─ modules.yml
├─ docs/
│  ├─ index.md
│  ├─ smx/index.md
│  ├─ dam/index.md
│  └─ assets/stylesheets/extra.css
├─ tools/
│  ├─ import_from_html.py
│  ├─ fix_fetch_paths.py
│  └─ gen_module_indexes.py
├─ main.py
├─ mkdocs.yml
├─ requirements.txt
└─ .github/workflows/deploy.yml
```
