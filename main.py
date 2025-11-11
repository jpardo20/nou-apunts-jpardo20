import yaml
from pathlib import Path
from html import escape

def define_env(env):
    data_path = Path("data/modules.yml")
    modules = {}
    if data_path.exists():
        with data_path.open("r", encoding="utf-8") as f:
            try:
                modules = yaml.safe_load(f) or {}
            except Exception:
                modules = {}
    modules = modules.get("modules", {})

    def cards(items, kind):
        # kind: 'theory' o 'activities' => classes diferents
        buf = []
        buf.append('<div class="grid cards {}">'.format("cards-theory" if kind == "theory" else "cards-activities"))
        for it in items or []:
            title = escape(str(it.get("title", "")))
            desc  = escape(str(it.get("desc", "")))
            url   = escape(str(it.get("url", "#")))
            icon  = "book-open" if kind == "theory" else "beaker"
            buf.append(f"""
- <article>
  <h3>:octicons-{icon}-16: {title}</h3>
  <p>{desc}</p>
  <p><a href="{url}" class="md-button md-button--primary">Obrir</a></p>
</article>
""")
        buf.append("</div>")
        return "\\n".join(buf)

    @env.macro
    def module_index(module_id):
        m = modules.get(str(module_id))
        if not m:
            return f'> **No trobat**: mòdul {escape(str(module_id))}'
        title = escape(m.get("title", f"Mòdul {module_id}"))
        theory = m.get("theory", [])
        activities = m.get("activities", [])
        return f"""
# {title}

=== "Teoria"
{cards(theory, "theory")}

=== "Activitats"
{cards(activities, "activities")}
"""

    env.macro(module_index)
