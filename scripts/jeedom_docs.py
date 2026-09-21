"""Fonctions partagees par les scripts de gestion de la documentation.

Les depots de plugins poussent leur dossier docs/ tel quel, avec la
convention Jeedom :

    docs/<plugin>/fr_FR/index.md      documentation, francais
    docs/<plugin>/fr_FR/changelog.md  changelog, francais
    docs/<plugin>/en_US/index.md      documentation, anglais
    docs/<plugin>/fr_FR/images/...    ressources (mutualisees entre langues)
    docs/<plugin>/.title              libelle affiche dans la navigation

Aucun fichier recu n'est renomme : c'est hooks/jeedom_locales.py qui presente
cette arborescence a mkdocs-static-i18n au moment du build. LOCALE_ALIASES
recense les noms de dossiers de langue reconnus.

La navigation est deduite de l'arborescence : un dossier = une rubrique. Le
fichier .title ne sert qu'a forcer un libelle different du nom du dossier.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
TEMPLATE_DIR = REPO_ROOT / "templates" / "plugin"

# Langues construites par le site, dans l'ordre d'affichage.
LANGUAGES = ("fr", "en", "de", "es")

# Nom de dossier rencontre cote plugin -> langue du site.
LOCALE_ALIASES = {
    "fr": "fr", "fr_fr": "fr", "fr-fr": "fr", "french": "fr", "francais": "fr",
    "en": "en", "en_us": "en", "en-us": "en", "en_gb": "en", "en-gb": "en", "english": "en",
    "de": "de", "de_de": "de", "de-de": "de", "german": "de", "deutsch": "de",
    "es": "es", "es_es": "es", "es-es": "es", "spanish": "es", "espanol": "es",
}

TITLE_FILE = ".title"

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def normalize_locale(name: str) -> str | None:
    """Retourne la langue du site correspondant a un nom de dossier, ou None."""
    return LOCALE_ALIASES.get(name.strip().lower())


def check_slug(slug: str) -> str:
    """Valide le nom technique d'un plugin (celui du dossier et de l'URL)."""
    slug = slug.strip()
    if not SLUG_RE.match(slug):
        raise SystemExit(
            f"Nom de plugin invalide : {slug!r}. "
            "Utilisez des minuscules, chiffres, tirets ou underscores "
            "(exemple : mon-plugin)."
        )
    return slug


def default_title(slug: str) -> str:
    """Libelle par defaut d'une rubrique, identique a celui de MkDocs."""
    return slug.replace("-", " ").replace("_", " ").capitalize()


def read_title(plugin_dir: Path) -> str | None:
    """Lit le libelle force dans docs/<plugin>/.title, s'il existe."""
    candidate = plugin_dir / TITLE_FILE
    if not candidate.is_file():
        return None
    for line in candidate.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def write_title(plugin_dir: Path, title: str) -> None:
    """Ecrit docs/<plugin>/.title, sauf si le nom du dossier suffit deja."""
    candidate = plugin_dir / TITLE_FILE
    if title == default_title(plugin_dir.name):
        candidate.unlink(missing_ok=True)
        return
    candidate.write_text(title + "\n", encoding="utf-8")


def render_template(plugin_dir: Path, title: str, overwrite: bool = False) -> list[Path]:
    """Copie templates/plugin/ dans docs/<plugin>/ en substituant le titre."""
    created: list[Path] = []
    for source in sorted(TEMPLATE_DIR.rglob("*")):
        if source.is_dir():
            continue
        target = plugin_dir / source.relative_to(TEMPLATE_DIR)
        if target.exists() and not overwrite:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8").replace("__PLUGIN_NAME__", title)
        target.write_text(text, encoding="utf-8")
        created.append(target)
    return created
