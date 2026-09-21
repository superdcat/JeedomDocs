"""Genere le tableau des plugins sur les pages d'accueil.

Les pages d'accueil (docs/index.<langue>.md) contiennent un marqueur :

    <!-- liste-des-plugins -->

Ce hook le remplace, au build, par un tableau liste des rubriques presentes
dans docs/ : libelle du plugin, lien vers sa documentation, lien vers son
changelog. Un plugin qui arrive dans le depot apparait donc tout seul, sans
edition des quatre pages d'accueil.

Le tableau est traduit dans la langue de la page en cours de construction.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from jeedom_docs import default_title, read_title  # noqa: E402

log = logging.getLogger("mkdocs.hooks.plugin_index")

MARKER = "<!-- liste-des-plugins -->"

# En-tetes et textes du tableau, par langue.
LABELS = {
    "fr": ("Plugin", "Documentation", "Changelog", "Aucun plugin documenté pour le moment."),
    "en": ("Plugin", "Documentation", "Changelog", "No plugin documented yet."),
    "de": ("Plugin", "Dokumentation", "Changelog", "Noch kein Plugin dokumentiert."),
    "es": ("Plugin", "Documentación", "Changelog", "Aún no hay ningún plugin documentado."),
}


def _page_language(page, config) -> str:
    """Langue du build en cours, telle que positionnee par static-i18n."""
    locale = getattr(page.file, "locale", None) or config["theme"].get("language")
    return locale if locale in LABELS else "fr"


def _plugins(config, source_docs: Path) -> list[tuple[str, str, bool]]:
    """(libelle, slug, a_un_changelog) pour chaque rubrique, triees par libelle."""
    staging = Path(config["docs_dir"])
    found = []
    for directory in sorted(staging.iterdir()):
        if not directory.is_dir():
            continue
        if not list(directory.glob("index.*.md")):
            log.warning("%s : pas de page index, rubrique ignoree dans le tableau",
                        directory.name)
            continue
        slug = directory.name
        title = read_title(source_docs / slug) or default_title(slug)
        found.append((title, slug, bool(list(directory.glob("changelog.*.md")))))
    return sorted(found, key=lambda item: item[0].lower())


def on_page_markdown(markdown: str, page, config, files) -> str:
    """Remplace le marqueur par le tableau des plugins."""
    if MARKER not in markdown:
        return markdown

    plugin_label, doc_label, changelog_label, empty_label = LABELS[
        _page_language(page, config)
    ]

    # Les sources reelles portent les .title ; le staging n'a que les pages.
    source_docs = Path(__file__).resolve().parent.parent / "docs"
    plugins = _plugins(config, source_docs)

    if not plugins:
        return markdown.replace(MARKER, f"*{empty_label}*")

    lines = [
        f"| {plugin_label} | {doc_label} | {changelog_label} |",
        "| --- | --- | --- |",
    ]
    for title, slug, has_changelog in plugins:
        changelog = f"[{changelog_label}]({slug}/changelog.md)" if has_changelog else "—"
        lines.append(f"| **{title}** | [{doc_label}]({slug}/index.md) | {changelog} |")

    return markdown.replace(MARKER, "\n".join(lines))
