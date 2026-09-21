"""Cree la rubrique d'un nouveau plugin dans docs/.

Usage :
    python scripts/new_plugin.py mon-plugin --name "Mon Plugin"

Genere docs/mon-plugin/{fr_FR,en_US,de_DE,es_ES}/{index,changelog}.md a
partir de templates/plugin/, dans l'arborescence native des plugins Jeedom.
Les fichiers deja presents ne sont pas ecrases.

Utile pour demarrer une rubrique a la main : en fonctionnement normal, c'est
le depot du plugin qui pousse son dossier docs/ ici.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jeedom_docs import (  # noqa: E402
    DOCS_DIR,
    check_slug,
    default_title,
    render_template,
    write_title,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="nom technique du plugin (dossier et URL)")
    parser.add_argument(
        "--name",
        help="nom affiche dans la navigation (par defaut : le slug capitalise)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="ecraser les fichiers existants",
    )
    args = parser.parse_args()

    slug = check_slug(args.slug)
    title = args.name or default_title(slug)
    plugin_dir = DOCS_DIR / slug

    created = render_template(plugin_dir, title, overwrite=args.force)
    write_title(plugin_dir, title)

    if created:
        print(f"Rubrique '{title}' creee dans {plugin_dir.relative_to(DOCS_DIR.parent)} :")
        for path in created:
            print(f"  - {path.relative_to(DOCS_DIR.parent)}")
    else:
        print(f"Rubrique deja presente dans {plugin_dir.relative_to(DOCS_DIR.parent)}.")
    print()
    print("Le tableau des pages d'accueil se met a jour tout seul au prochain build.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
