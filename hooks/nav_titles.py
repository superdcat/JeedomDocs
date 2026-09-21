"""Titre d'affichage personnalise pour la rubrique d'un plugin.

La navigation est construite automatiquement a partir de l'arborescence de
docs/ : chaque dossier devient une rubrique, dont le titre par defaut derive du
nom du dossier ('mon-plugin' -> 'Mon plugin').

Pour afficher autre chose (sigles, majuscules, espaces), il suffit de poser un
fichier '.title' dans le dossier du plugin, contenant le libelle sur une ligne :

    docs/mqtt-manager/.title   ->   MQTT Manager

Le fichier commence par un point : MkDocs l'ignore, il n'est jamais publie.
"""

from __future__ import annotations

from pathlib import Path

TITLE_FILE = ".title"


def _read_title(directory: Path) -> str | None:
    candidate = directory / TITLE_FILE
    if not candidate.is_file():
        return None
    for line in candidate.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def _rename(items, docs_dir: Path) -> None:
    for item in items:
        children = getattr(item, "children", None)
        if not children:
            continue
        # La rubrique est localisee par le dossier de sa premiere page.
        pages = [child for child in children if getattr(child, "file", None)]
        if pages:
            directory = docs_dir / Path(pages[0].file.src_uri).parent
            title = _read_title(directory)
            if title:
                item.title = title
        _rename(children, docs_dir)


def on_nav(nav, config, files):
    """Applique les titres declares dans les fichiers .title."""
    _rename(nav.items, Path(config["docs_dir"]))
    return nav
