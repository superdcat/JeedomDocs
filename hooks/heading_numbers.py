"""Neutralise la numerotation automatique sur les pages deja numerotees.

Le gabarit Jeedom numerote les titres ('1) Description', '1.1) Pre-requis').
Le site le fait en CSS, sans toucher au markdown ni aux ancres (voir
docs/assets/jeedom.css).

Certaines documentations numerotent deja leurs titres a la main :

    ## 1. A lire avant d'installer
    ### 1.1 Ce que fait ce plugin

Les compteurs CSS s'ajouteraient a cette numerotation ('1) 1. A lire...').
Ce hook detecte le cas et pose 'jeedom_numerotation: false' dans les
metadonnees de la page ; overrides/main.html desactive alors les compteurs
pour cette page uniquement.

Une page peut forcer le comportement en declarant elle-meme, dans son
entete YAML :

    ---
    jeedom_numerotation: false
    ---
"""

from __future__ import annotations

import re

META_KEY = "jeedom_numerotation"

# Blocs de code : '## ' y est du contenu, pas un titre.
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)

HEADING_RE = re.compile(r"^(#{2,3})\s+(.*)$", re.MULTILINE)

# '1.', '1)', '1.1', '2.3)', ou un numero de version seul ('1.0.0'),
# en tete de titre. Couvre aussi les changelogs, dont les sections sont
# des numeros de version.
NUMBERED_RE = re.compile(r"^\d+(\.\d+)*[.)]?(\s|$)")


def _numbering_wanted(markdown: str) -> bool:
    """Vrai si la numerotation automatique a un sens sur cette page."""
    text = FENCE_RE.sub("", markdown)
    headings = [
        (len(match.group(1)), match.group(2).strip())
        for match in HEADING_RE.finditer(text)
    ]
    # Page d'accueil, page courte : numeroter une section unique n'apporte rien.
    if sum(1 for level, _ in headings if level == 2) < 2:
        return False
    numbered = sum(1 for _, title in headings if NUMBERED_RE.match(title))
    # La page numerote deja la plupart de ses titres : on la laisse faire.
    return numbered * 2 < len(headings)


def on_page_markdown(markdown, page, config, files):
    """Renseigne la metadonnee lue par le gabarit, sans modifier la page."""
    if META_KEY not in page.meta:
        page.meta[META_KEY] = _numbering_wanted(markdown)
    return markdown
