# JeedomDocs

Site public de documentation des plugins Jeedom de **superdcat**, publié sur
GitHub Pages : <https://jeedomdocs.decastro.fr/>

Le code des plugins reste dans leurs dépôts privés. Seule la documentation
markdown est poussée ici, **telle quelle**, puis construite avec
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Organisation

Une rubrique par plugin, chaque rubrique contenant sa documentation et son
changelog, dans l'arborescence native des plugins Jeedom :

```
docs/
├── index.fr.md                page d'accueil du site (fr, en, de, es)
├── index.en.md
├── index.de.md
├── index.es.md
└── imou/                      une rubrique = un dossier plugin
    ├── .title                 libellé affiché (facultatif)
    ├── fr_FR/
    │   ├── index.md           la documentation
    │   ├── changelog.md       le journal des modifications
    │   └── images/            captures d'écran
    ├── en_US/
    ├── de_DE/
    └── es_ES/
```

C'est **exactement le dossier `docs/` du dépôt du plugin**, déposé sous
`docs/<plugin>/`. Rien n'est renommé à la réception : le hook
`hooks/jeedom_locales.py` prépare au moment du build une copie normalisée dans
`.mkdocs-staging/` (`imou/fr_FR/index.md` → `imou/index.fr.md`), qui est la
forme attendue par `mkdocs-static-i18n`. Les images d'un plugin sont
mutualisées entre les langues.

Points qui en découlent :

- **Toutes les pages sont reprises**, pas seulement `index` et `changelog` :
  un `changelog_beta.md` ou un `guide/avance.md` apparaît automatiquement.
- **Une page non traduite s'affiche en français.** Aucune obligation de tout
  traduire dans les quatre langues.
- **Ajouter un plugin = ajouter un dossier.** `mkdocs.yml` n'est jamais à
  modifier : la navigation est déduite de l'arborescence, et le tableau des
  pages d'accueil est généré au build (marqueur `<!-- liste-des-plugins -->`
  dans `docs/index.*.md`, rempli par `hooks/plugin_index.py`).
- Le lien « éditer cette page » pointe vers le vrai fichier du dépôt
  (`docs/imou/fr_FR/index.md`), pas vers la copie de build.

Le fichier `.title` sert uniquement à forcer un libellé différent du nom du
dossier (`mqtt-manager` → `MQTT Manager`). Il est écrit par le workflow de
publication.

## Publier la doc depuis un dépôt de plugin

Chaque dépôt privé de plugin pousse sa documentation ici via GitHub Actions.

1. Copier `templates/plugin-repo/publish-docs.yml` dans le dépôt du plugin,
   sous `.github/workflows/publish-docs.yml`.
2. Y adapter `PLUGIN_SLUG` (dossier et URL) et `PLUGIN_NAME` (libellé affiché).
3. Créer un [jeton fine-grained](https://github.com/settings/personal-access-tokens)
   limité à `superdcat/JeedomDocs` avec la permission **Contents : Read and
   write**, et l'enregistrer dans le dépôt du plugin comme secret
   `DOCS_PUSH_TOKEN`.

À chaque push touchant `docs/` dans le dépôt du plugin, le workflow recopie le
dossier ici et commite. Le déploiement GitHub Pages suit automatiquement. Une
page supprimée côté plugin disparaît du site.

Copie manuelle équivalente, depuis une copie locale du dépôt du plugin :

```bash
rm -rf docs/imou && cp -R ../JeedomIMOU/docs docs/imou
printf 'IMOU\n' > docs/imou/.title
```

## Créer une rubrique à la main

Pour démarrer une doc qui n'existe pas encore côté plugin :

```bash
python scripts/new_plugin.py mon-plugin --name "Mon Plugin"
```

Le script crée `docs/mon-plugin/{fr_FR,en_US,de_DE,es_ES}/{index,changelog}.md`
à partir de `templates/plugin/`. Rien d'autre à faire : navigation et tableau
d'accueil suivent tout seuls.

## Prévisualiser en local

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows ; sous Linux/macOS : source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Le site est disponible sur <http://127.0.0.1:8000/>. Les modifications de
`docs/` déclenchent bien une reconstruction (le hook remet les sources sous
surveillance).

Le build de production tourne en `--strict` : un lien cassé fait échouer la CI.

## Mise en service de GitHub Pages

Dans **Settings → Pages** du dépôt, la source doit être **GitHub Actions**, et
non « Deploy from a branch » : sinon GitHub lance son workflow Jekyll historique
(« pages build and deployment ») qui publie la racine du dépôt et écrase le
déploiement de `deploy.yml`.

Le domaine personnalisé est `jeedomdocs.decastro.fr`. Le fichier `CNAME` vit
**à la racine du dépôt** (c'est là que l'interface GitHub le gère) et
`deploy.yml` le recopie dans l'artefact publié. Ne pas en créer un second dans
`docs/` : il serait écrasé par celui de la racine, donc sans effet.
