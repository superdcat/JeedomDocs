# Badger Fork

## Description

Ce plugin permet de connecter des lecteurs de badges (RFID/NFC) utilisant le protocole Wiegand (8/26/34). Ce plug-in nécessite un composant tiers (Arduino) comme interface entre le lecteur et le réseau local.

## Installation

Le plugin s'installe **depuis le Market Jeedom**.

1. Dans Jeedom, allez dans **Plugins > Gestion des plugins**.
2. Cliquez sur **Market**, en haut à gauche.
3. Recherchez **Badger Fork**, ouvrez sa fiche, puis cliquez sur **Installer** (version stable ou bêta).
4. Ouvrez la page de configuration du plugin et **activez-le**.

Il n'y a **ni dépendance ni démon** à installer : le plugin est entièrement en PHP.

> **Vous utilisez déjà l'ancien plugin Badger ?** Ne le désinstallez pas tout de suite : suivez d'abord
> la [procédure de migration](migration.md).

## Migration depuis Badger

---

[Migration depuis le plugin Badger](migration.md)

## Configuration

---

[Configuration du plugin](configuration.md)

## Fonctionnement

---

[Fonctionnement et utilisation des equipements](fonctionement.md)

Le log du plugin n'écrit plus les badges ni les codes reçus : une présentation inconnue ou un code faux y apparaît sans sa valeur. Pour voir ces valeurs, utilisez le [mode debug](#mode-debug).

### Mode debug

Le mode debug sert à mettre au point un lecteur ou un clavier : il montre, appel par appel, ce que le lecteur envoie au plugin et ce que le plugin en a fait.

> **Attention : en mode debug, les badges et les codes présentés sont affichés en clair.** Un bandeau rouge reste visible en haut de la page du plugin tant que le mode est actif. N'activez-le que le temps de la mise au point.

#### Activer

1. Connectez-vous avec un compte **administrateur** et ouvrez la page du plugin.
2. Descendez à la section **Mode debug**, en bas de la page.
3. Choisissez le **lecteur** observé (un lecteur précis, ou « Tous les lecteurs »).
4. Choisissez la **durée** : 15 minutes, 30 minutes ou 1 heure (maximum).
5. Cochez si besoin **Observation seule (ne rien traiter)**, puis cliquez sur **Activer**.

> **Observation seule : la porte ne s'ouvre plus pour ce lecteur pendant la durée choisie.** Les appels sont montrés mais ne sont pas traités : aucune action, aucun badge ni code pris en compte. Cette option n'existe que pour un lecteur précis, pas pour « Tous les lecteurs ». Cliquez sur **Arrêter** pour revenir tout de suite au fonctionnement normal.

Les boutons **Arrêter** (coupe le mode debug) et **Effacer** (vide la liste des appels) sont dans la même section. La liste se met à jour toutes les 2 secondes.

#### Ce qui est montré

Pour chaque appel reçu : l'heure, la route utilisée (ancienne ou courante), la version de protocole reconnue, le lecteur, l'adresse d'origine, l'adresse IP déclarée par le lecteur, le nom des en-têtes reçus, les paramètres envoyés (dont le badge ou le code tapé, en clair) et le résultat obtenu (badge ou code reconnu, code faux, lecteur bloqué, etc.).

- Les 200 derniers appels sont conservés.
- Les appels refusés parce que leur origine n'est pas autorisée sont regroupés : la section affiche leur nombre depuis l'activation et quelques exemples récents, sans les lister tous.
- Le contenu reçu est affiché comme du texte brut, jamais interprété.

#### Ce qui n'est jamais montré

- Les codes et les badges **enregistrés** dans le plugin : seule la valeur présentée par le lecteur apparaît, jamais la liste de ce qui est enregistré.
- Les secrets : la clé `apikey` et la signature `sig` sont remplacées par « masqué » et leur nombre de caractères.
- Le contenu du mode debug n'est écrit ni dans le log, ni dans les sauvegardes de Jeedom.

#### Arrêt automatique

Le mode debug s'arrête seul, et efface alors tout ce qu'il avait enregistré, dans chacun de ces cas :

- à l'échéance de la durée choisie ;
- quand vous cliquez sur **Arrêter** ;
- quand vous désactivez le plugin ou qu'il est mis à jour ;
- au redémarrage de Jeedom (il n'est jamais rétabli après un redémarrage).

Chaque activation et chaque arrêt sont notés dans le log du plugin (qui, jusqu'à quand, quel lecteur), sans aucune valeur de badge ou de code.

## Infos techniques

---

[Infos techniques](techtips.md)

## Protocole des lecteurs (référence technique)

Le plugin reconnaît la version du protocole de chaque appel d'un lecteur. Les lecteurs actuels (sketches d'origine, qu'ils appellent l'ancienne adresse `/plugins/badger/…` ou la nouvelle `/plugins/badger2/…`) continuent de fonctionner exactement comme avant.

Les versions prises en charge sont visibles dans **Analyse > Santé**, ligne « Versions de protocole supportées » (aujourd'hui : « v0 : supportée ; v1 : prévue (pas encore servie) »).

Un appel qui annonce une version inconnue est refusé, et l'avertissement « version de protocole non supportée : mettre à jour le plugin » apparaît dans le log du plugin.

---

[Protocole v1 des lecteurs : référence (en préparation)](protocole-v1.md)
