"""Accepte l'arborescence de documentation native des plugins Jeedom.

Les depots de plugins poussent leur dossier docs/ tel quel, avec la convention
Jeedom : un sous-dossier par langue.

    docs/imou/fr_FR/index.md
    docs/imou/fr_FR/changelog.md
    docs/imou/en_US/index.md
    docs/imou/fr_FR/images/capture.png

Le plugin mkdocs-static-i18n, lui, attend des noms suffixes
(docs/imou/index.fr.md). Ce hook prepare donc, avant chaque build, une copie
normalisee de docs/ dans .mkdocs-staging/ et pointe MkDocs dessus :

    imou/fr_FR/index.md          ->  imou/index.fr.md
    imou/fr_FR/guide/avance.md   ->  imou/guide/avance.fr.md
    imou/fr_FR/images/x.png      ->  imou/images/x.png   (partage entre langues)

Le depot, lui, conserve exactement les fichiers recus : rien n'est renomme
dans docs/. Un plugin qui pousserait deja des noms suffixes fonctionne aussi,
ses fichiers sont recopies sans modification.

En mode 'mkdocs serve', on_serve remet docs/ sous surveillance pour que les
modifications des sources declenchent bien une reconstruction.
"""

from __future__ import annotations

import logging
import shutil
import sys
from pathlib import Path

from mkdocs.plugins import event_priority

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from jeedom_docs import LANGUAGES, normalize_locale  # noqa: E402

log = logging.getLogger("mkdocs.hooks.jeedom_locales")

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = REPO_ROOT / ".mkdocs-staging"

# Dossier des sources reelles, memorise pour 'mkdocs serve'.
_source_docs_dir: Path | None = None

# Copie normalisee -> fichier reel du depot, pour le lien "editer cette page".
_sources: dict[str, str] = {}


def _target_for(relative: Path) -> tuple[Path | None, str | None]:
    """Chemin de la copie normalisee, ou (None, avertissement) si a ecarter."""
    parts = relative.parts
    # Seul <plugin>/<langue>/... est traduit ; les pages racines du site
    # (index.fr.md) sont deja au format attendu.
    if len(parts) < 3:
        return relative, None

    plugin, folder, *rest = parts
    language = normalize_locale(folder)
    if language is None:
        return relative, None
    if language not in LANGUAGES:
        return None, f"{relative.as_posix()} : langue '{folder}' non construite, ignore"

    if rest[-1].endswith(".md"):
        rest[-1] = f"{rest[-1][: -len('.md')]}.{language}.md"
    # Les fichiers non-markdown (images, pieces jointes) sont mutualises :
    # le dossier de langue disparait et la premiere langue rencontree gagne.

    return Path(plugin, *rest), None


def _build_staging(source: Path) -> None:
    """Reconstruit .mkdocs-staging/ a partir du contenu de docs/."""
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)

    _sources.clear()
    written: dict[Path, Path] = {}
    for item in sorted(source.rglob("*")):
        if not item.is_file():
            continue
        relative = item.relative_to(source)
        target, warning = _target_for(relative)
        if warning:
            log.warning(warning)
            continue
        if target in written:
            log.info(
                "Ressource partagee %s : %s ignore au profit de %s",
                target.as_posix(), relative.as_posix(), written[target].as_posix(),
            )
            continue
        written[target] = relative
        _sources[target.as_posix()] = relative.as_posix()
        destination = STAGING_DIR / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, destination)


@event_priority(100)
def on_config(config):
    """Construit la copie normalisee et fait travailler MkDocs dessus."""
    global _source_docs_dir

    source = Path(config["docs_dir"])
    if source == STAGING_DIR:  # deja redirige (rechargement de 'mkdocs serve')
        source = _source_docs_dir or REPO_ROOT / "docs"

    _source_docs_dir = source
    _build_staging(source)
    config["docs_dir"] = str(STAGING_DIR)
    return config


def on_page_context(context, page, config, nav):
    """Fait pointer "editer cette page" vers le fichier reel du depot."""
    if page.edit_url and page.file.abs_src_path:
        staged = Path(page.file.abs_src_path)
        try:
            key = staged.relative_to(STAGING_DIR).as_posix()
        except ValueError:
            return context
        source = _sources.get(key)
        if source:
            page.edit_url = page.edit_url.replace(key, source)
    return context


def on_serve(server, config, builder):
    """Surveille les sources reelles, pas seulement la copie normalisee."""
    if _source_docs_dir is not None:
        server.watch(str(_source_docs_dir))
    return server
