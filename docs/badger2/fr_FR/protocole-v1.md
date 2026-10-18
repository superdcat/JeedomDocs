# Protocole v1 des lecteurs : référence technique

> **Statut : prévu (en préparation).** Ni le plugin ni un sketch ne servent encore ce protocole. **Vos
> lecteurs actuels ne sont pas concernés** : ils continuent d'appeler le plugin exactement comme avant
> (voir « Le protocole v0 reste inchangé »). Cette page fixe le contrat que le futur sketch unifié
> `Badger2` et le plugin devront respecter tous les deux ; elle s'adresse aux utilisateurs avancés et
> aux contributeurs.

Le protocole v1 remplace l'appel par adresse web du protocole d'origine (v0) par une requête `POST`
signée, que le plugin peut authentifier, dont il peut détecter le rejeu et à laquelle il **répond**.
Tout y est défini sans ambiguïté : les champs et leurs bornes, les clés de réponse, la signature, les
règles d'évolution.

## Transport

- Requête `POST /plugins/badger2/core/api/jeebadger.php HTTP/1.1`, avec les en-têtes `Host`,
  `Content-Type: application/x-www-form-urlencoded`, `Content-Length` exact et `Connection: close`.
  Pas de `Transfer-Encoding: chunked`, aucun en-tête de proxy.
- **La chaîne de requête est vide.** Aucun champ v1 n'est lu dans l'adresse. Un appel v1 (`POST` dont le
  corps porte `v`) dont l'adresse porte un paramètre `v` est refusé (`err=invalid`). Un appel sans `v`
  dans le corps (`GET`, ou `POST` sans `v`) est un appel v0, traité à l'identique, même si son adresse
  porte un `v` : voir « Reconnaître la version ».
- **Pourquoi `POST` : badge et code PIN ne doivent plus figurer dans le journal d'accès du serveur
  web.** Ce journal garde la ligne de requête (chemin et chaîne de requête), jamais le corps. Avec la
  v0, chaque badge et chaque code y apparaissent en clair ; avec la v1 ils n'y sont plus. Aucun champ
  sensible ne figure jamais dans l'adresse.
- L'adresse du lecteur est l'adresse de connexion : il n'y a pas de champ `ip`.
- **Limite connue** : le trafic reste en HTTP, donc lisible sur le réseau local. La signature protège
  l'authenticité et le rejeu, pas la confidentialité (chiffrement facultatif : UC 009 et 110 de la feuille de route) ; isolez
  les lecteurs sur un réseau dédié. Une réponse non signée peut être falsifiée : un lecteur sans secret
  n'annonce la capacité `relay` que si l'installateur a explicitement autorisé les actions non signées
  (désactivé par défaut). Pour la même raison, tant qu'aucun secret n'est appairé, le sketch applique
  `hb`, `led` et `buzz` non authentifiés, mais **ignore** `cfg` et n'applique pas `t` (voir « Côté
  lecteur »).

## Reconnaître la version

Le plugin décide de la version d'un appel avant toute autre chose :

| Route | Paramètre de version | Traité en |
|---|---|---|
| `/plugins/badger/…` (relais de l'ancienne route) | n'importe lequel ou aucun | **v0**, toujours. Un `v` présent est journalisé en débogage et ignoré. |
| `/plugins/badger2/…` | aucun `v` dans le corps (`GET`, ou `POST` sans `v`) | **v0**, à l'identique |
| `/plugins/badger2/…` | `v=1` dans le corps d'un `POST` | v1 |
| `/plugins/badger2/…` | `v` inconnu dans le corps (par exemple `v=7`) | refusé : 400 `err=version`, jamais de repli sur la v0 |
| `/plugins/badger2/…` | `v` dans la chaîne de requête | sans `v` dans le corps : appel v0 inchangé ; appel v1 : refusé `err=invalid` (aucun champ v1 n'est lu dans l'adresse) |

Refuser un appel v0 conforme parce que son adresse porte un `v` le casserait : la v0 n'a jamais eu de
`v`, et la v1 ne le connaît que dans le corps.

## Encodage du corps

- Paires `nom=valeur` séparées par un seul `&`. Chaque paire contient `=` ; pas de paire vide, pas de
  `&` en tête ni en fin.
- Le nom suit `^[a-z][a-z0-9_]{0,15}$` et n'est jamais encodé. La valeur est décodée comme un formulaire
  web : `+` devient une espace, puis `%XX` devient l'octet correspondant.
- **Appel invalide** (`err=invalid`) : nom répété (`v` compris) ; `%` mal formé ; nom hors motif ; corps
  de plus de **1024 octets** ; nom **réservé de la v0**, à vie : `name`, `ip`, `cmd`, `value`, `model`,
  `apikey`. Réserver ces noms garantit qu'une requête v1 qui atteindrait par erreur un traitement v0
  (plugin pas encore à jour) n'a aucun effet d'accès.
- **Motifs ancrés** : un motif s'applique à la valeur **entière** (`\A…\z` ; en PHP `/\A…\z/D`, jamais
  `^…$` seul, qui tolère un saut de ligne final). Un octet de contrôle dans un nom ou dans une valeur à
  motif est invalide (`err=invalid`).
- Un champ inconnu, ou connu mais étranger à son événement, est **ignoré** : l'appel est accepté et le
  champ reste couvert par la signature.
- **Énumérations ouvertes** : une valeur de bonne syntaxe mais inconnue est acceptée, affichée, et ne
  déclenche rien. Seuls `v` et `st` sont fermés.
- Les nombres décimaux n'ont pas de zéro de tête (sauf `0`). L'hexadécimal est en minuscules.

## Ordre d'évaluation (côté plugin)

1. Le corps d'un `POST` porte un seul `v` différent de `1` : réponse 400 `err=version`. **Jamais de repli
   sur la v0.** Un appel sans `v` dans le corps n'entre pas dans cet ordre : c'est un appel v0.
2. Syntaxe (taille, paires, noms, doublons, `%`, noms réservés et, pour un appel v1 seulement, `v` dans
   la chaîne de requête), puis champs (obligatoires, bornes) : 400 `err=invalid`.
3. Identité et authentification : 403 `err=auth`, réponse non signée, pour un `rid` inconnu (hors
   inclusion), un `rid` de casse différente, un lecteur sous son plancher de version, une signature
   fausse.
4. Rejeu : 403 `err=replay` (réponse signée).
5. Fraîcheur : jamais un refus, mais un message non frais n'est pas traité comme un événement direct.

Imposé au plugin : toute valeur est validée à l'étape 2, avant tout journal, toute création
d'équipement et tout affichage ; un motif s'applique à la valeur entière et un octet de contrôle est
refusé (voir « Encodage du corps »).

**Lecteur appairé** : lecteur pour lequel le plugin a enregistré un secret, pour ce `rid`. Un `sig` reçu
pour un `rid` sans secret connu est ignoré : l'appel est traité comme non signé et la réponse n'est pas
signée. Limite assumée : sans secret, le plugin ne détecte pas les doublons (`boot`, `seq`) ; un
événement réémis peut être traité deux fois.

**Identité** : le plugin rattache un `rid` sans tenir compte de la casse (comme la base Jeedom) et
n'accepte l'appel que si la casse est **identique** ; sinon 403 `auth`, et jamais de création, y compris
en inclusion. **Plancher** : dès qu'un secret est enregistré pour un lecteur, le plugin refuse (403 `auth`) tout
appel v0 ou v1 sans `sig` valide rattaché à ce lecteur, rattachement insensible à la casse compris.
Le plancher est un **indicateur persistant** posé à l'appairage, distinct du secret : indicateur posé et
secret absent ou indéchiffrable = 403 `auth` et erreur journalisée, jamais un retour à « non appairé ».
Seule l'action « Rabaisser à v0 » lève ce plancher.

## Champs

Les champs sont décrits dans **un seul tableau** : type, bornes, et événements pour lesquels le champ
est obligatoire ou facultatif. Un événement se compose des champs communs (obligatoires pour tous), de
ses propres champs et, pour `offline`, de ceux de l'événement d'origine `oev`. Un nom en minuscules,
sans guillemets, désigne un champ ; `sig` est facultatif parce que seul un lecteur muni d'un secret
signe.

<!-- debut:tableau-champs -->
| Champ | Type et bornes | Obligatoire pour | Facultatif pour |
|---|---|---|---|
| `v` | entier 1 à 999 ; `1` pour ce protocole | tous les événements | — |
| `fw` | semver `MAJ.MIN.CORR[-pre]`, nombres 0 à 65535 sans zéro de tête, `pre` de 1 à 16 caractères `[0-9A-Za-z.-]`, 32 caractères au plus, pas de `+build` | tous les événements | — |
| `board` | `^[a-z0-9][a-z0-9_-]{0,23}$`, liste ouverte `<carte>-<transport>` (ex. `uno-w5100`, `uno-enc28j60`, `mega-w5100`, `esp32-eth`, `esp8266-wifi`) | tous les événements | — |
| `rid` | `^[A-Za-z0-9_-]{1,32}$`, défaut `BADGER<n>` (continuité v0) | tous les événements | — |
| `boot` | entier 0 à 4294967295, persistant, +1 à chaque démarrage | tous les événements | — |
| `seq` | entier 0 à 4294967295, remis à 0 à chaque démarrage | tous les événements | — |
| `up` | entier 0 à 4294967295 : secondes depuis le démarrage, à la première émission de l'événement, reprises à l'identique à chaque réémission ; un événement converti en `offline` reçoit un `up` neuf | tous les événements | — |
| `ev` | `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`hello`, `hb`, `tag`, `pin`, `tagpin`, `key`, `input`, `door`, `ack`, `offline`) | tous les événements | — |
| `sig` | `^[0-9a-f]{64}$` ; présent si et seulement si le lecteur a un secret ; jamais journalisé en entier | — | tous les événements |
| `caps` | 0 à 32 jetons `^[a-z0-9_]{1,16}$` séparés par `,`, 255 caractères au plus ; `caps=` vide permis | `hello` | — |
| `rst` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`power`, `ext`, `wdt`, `brown`, `sw`, `unk`) | `hello` | — |
| `cfg` | `^[0-9a-f]{8}$`, empreinte opaque de la configuration du lecteur | — | `hello` |
| `mem` | entier 0 à 4294967295 : mémoire libre en octets | — | `hb` |
| `q` | entier 0 à 65535 : événements en file d'attente | — | `hb` |
| `lost` | entier 0 à 4294967295 : événements écartés d'une file pleine, refusés définitivement ou impossibles à émettre depuis le démarrage ; un `hb` écarté n'est pas compté ; absent : aucune perte connue | — | `hb` |
| `door` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`open`, `closed`) | `door`, `offline` (`oev=door`) | `hb` |
| `rssi` | entier -127 à 0 (Wi-Fi seulement) | — | `hb` |
| `bits` | entier 1 à 256 : nombre de bits de la trame | `tag`, `tagpin`, `offline` (`oev=tag`), `offline` (`oev=tagpin`) | — |
| `raw` | `^[0-9a-f]{1,64}$`, exactement ⌈bits/4⌉ chiffres, valeur strictement inférieure à 2^bits ; bits dans l'ordre de réception, premier reçu en poids fort, complétés à gauche | `tag`, `tagpin`, `offline` (`oev=tag`), `offline` (`oev=tagpin`) | — |
| `par` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`ok`, `bad`, `na`) | `tag`, `tagpin`, `offline` (`oev=tag`), `offline` (`oev=tagpin`) | — |
| `fac` | entier 0 à 4294967295 : code de site décodé | — | `tag`, `tagpin`, `offline` (`oev=tag`), `offline` (`oev=tagpin`) |
| `card` | entier 0 à 4294967295 : numéro de carte décodé | — | `tag`, `tagpin`, `offline` (`oev=tag`), `offline` (`oev=tagpin`) |
| `port` | entier 1 à 255 : port Wiegand d'origine ; absent pour un lecteur à un seul port (équivaut au port 1), émis seulement par un firmware à deux ports | — | `tag`, `pin`, `tagpin`, `key`, `offline` (`oev=tag`), `offline` (`oev=pin`), `offline` (`oev=tagpin`) |
| `code` | `^[0-9]{1,32}$` : code saisi | `pin`, `tagpin`, `offline` (`oev=pin`), `offline` (`oev=tagpin`) | — |
| `key` | jeton `^[0-9a-z][0-9a-z_]{0,15}$`, liste ouverte (`0` à `9`, `star`, `hash`, `f1` à `f4`) : touche reconnue par le clavier | `key` | — |
| `in` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`exit`, `bell`, `tamper`, `a1` à `a5`) | `input`, `offline` (`oev=input`) | — |
| `st` | `0` ou `1` (fermé) : état logique, après seuil et hystérésis pour `a1` à `a5` | `input`, `offline` (`oev=input`) | — |
| `val` | entier 0 à 65535 : lecture analogique brute au changement d'état, dans l'unité de la carte (`a1` à `a5`) | — | `input`, `offline` (`oev=input`) |
| `oseq` | entier 0 à 4294967295 : `seq` de l'ordre accusé | `ack` | — |
| `res` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`acc`, `ref`) | `ack` | — |
| `why` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`sig`, `replay`, `nosecret`, `unknown`, `param`, `busy`, `stale`) | — | `ack` |
| `oev` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`tag`, `pin`, `tagpin`, `input`, `door`) : événement d'origine | `offline` | — |
| `age` | entier 0 à 4294967 : secondes écoulées depuis la survenue de l'événement d'origine | `offline` | — |
<!-- fin:tableau-champs -->

Les événements :

- `hello` : premier événement après chaque démarrage (version du firmware, carte, capacités, cause du
  redémarrage) ;
- `hb` : battement de cœur (uptime, mémoire libre, file d'attente, événements perdus depuis le démarrage, état
  de la porte, RSSI si Wi-Fi). Les mesures sont figées à la création du battement : une réémission est
  identique octet pour octet. `lost` est absent tant qu'aucune perte n'est connue ; un `hb` écarté n'est pas
  une perte ;
- `tag` : badge présenté (nombre de bits, trame brute, parité, valeurs décodées, port Wiegand sur un lecteur
  à deux ports). Le firmware décode `fac` et `card` seulement quand la parité est bonne et que le format
  est connu (26 et 34 bits) : `raw` reste la référence, `fac` et `card` une indication ;
- `pin` : code saisi (port Wiegand sur un lecteur à deux ports) ;
- `tagpin` : un badge suivi d'un code saisi dans le délai réglé du lecteur (option « badge puis code »),
  en **un seul** événement : champs de `tag` plus `code`. **Sûr par défaut** : un plugin qui ne le connaît
  pas répond `ok=1` sans rien faire (il n'ouvre rien : ni le badge seul, ni le code seul ne décident) ;
- `key` : une touche du clavier, envoyée seulement avec l'option « touche par touche » du lecteur, **en
  plus** du `pin` final. Jeton : `0` à `9`, `star`, `hash`, `f1` à `f4`. **Aucun effet d'accès** : un plugin
  qui l'ignore répond `ok=1` ; le `pin` final décide ;
- `input` : entrée logique (bouton de sortie, sonnette, autoprotection, entrée analogique). `st=1` signifie
  **contact fermé** : bouton de sortie ou sonnette appuyés, boucle d'autoprotection fermée (au repos) ; **l'ouverture
  de l'autoprotection donne `st=0`**, y compris au démarrage du lecteur si la boucle est déjà ouverte. Chaque
  changement est un événement, le relâchement d'un bouton compris (`st=0`). Pour `a1` à `a5`, `st=1` signifie
  au-dessus du seuil haut réglé du lecteur et `val` porte la lecture brute qui a confirmé le changement ;
- `door` : changement d'état de la porte, `open` ou `closed` ;
- `ack` : accusé d'un ordre reçu du plugin (les ordres sont définis plus tard, voir « Ordres ») ;
- `offline` : événement direct (`tag`, `pin`, `tagpin`, `input`, `door`) qui n'a pas pu être délivré à temps, rejoué
  avec son âge.

**Écart à la spécification initiale** : le contact de porte produit **seulement** l'événement `door`,
jamais `input`, pour éviter deux événements pour un même contact. L'entrée analogique reste dans `input`,
avec `st` (état logique) et `val` (lecture brute).

**Champs sensibles** : `raw`, `fac`, `card`, `code`, `key` et leurs copies dans un événement `offline` ne figurent
jamais dans l'adresse ni, en clair, dans un journal (hors mode de débogage explicite). Un refus nomme le
champ, jamais sa valeur.

**Hors du contrat initial** (ajouts compatibles, définis par leur propre UC de la feuille de route) : champs `loc`, `net`, `qmax`, `wfmt`, `offp`, `wl`, `oport`, format des ordres.

Ajouté depuis (compatible, `v=1` inchangé) : champ `port` (UC 005), facultatif pour `tag` ; événements `tagpin`
(badge puis code) et `key` (touche par touche), champ `key`, et `port` facultatif pour `pin` (UC 006) ; champ
`lost`, facultatif pour `hb` (UC 008).

**Capacités informatives du sketch Badger2** (UC 008) : outre `hb` (seul jeton normatif, il autorise la clé de
réponse `hb`), le `hello` d'un lecteur Badger2 annonce des jetons **informatifs**, que le plugin affiche et
n'exploite pas : `wdt` (chien de garde matériel), `wg_26`, `wg_34`, `wg_37` (décodage du site et de la carte),
`wg_port2` (second lecteur Wiegand), `kp` (clavier), `kp_burst` (code en une trame), `kp_tagpin` (badge puis
code), `kp_key` (touche par touche), puis un jeton `io_*` par entrée ou sortie câblée (`io_strike`, `io_led`,
`io_buzz`, `io_door`, `io_exit`, `io_exit_open`, `io_tamper`, `io_bell`, `io_a1` à `io_a5`). Aucun n'autorise
une clé de réponse. Le `rst` d'un lecteur Badger2 vaut `power` (mise sous tension), `ext` (bouton reset),
`wdt` (chien de garde), `brown` (baisse de tension), `sw` (redémarrage logiciel) ou `unk` (inconnue).

## Capacités

Le champ `caps` du `hello` liste ce que le lecteur sait faire. **Le plugin n'envoie jamais une clé de
réponse dont la capacité n'a pas été annoncée.** Les capacités valent dès le `hello` qui les annonce
(sa réponse comprise) jusqu'au `hello` suivant.

| Capacité normative | Clé de réponse qu'elle autorise |
|---|---|
| `hs256` | `sig` |
| `time` | `t` |
| `relay` | `act` |
| `led` | `led` |
| `buzz` | `buzz` |
| `hb` | `hb` |
| `cfg` | `cfg` |

Toute autre capacité est **informative** : affichée, ignorée par le plugin, définie par l'UC de la feuille de
route qui l'introduit. Un lecteur peut annoncer une capacité que le plugin ne connaît pas encore.

## Réponse

- `text/plain; charset=us-ascii`, corps de **256 octets** au plus, 16 lignes au plus, ligne de 80 octets
  au plus, ASCII imprimable ; fin de ligne `\n` (`\r\n` toléré) ; aucune ligne vide.
- Une ligne par clé : `clé=valeur`, clé conforme à `^[a-z][a-z0-9_]{0,15}$`.
- **La première ligne est `ok=`**, et `sig=` est la dernière quand elle est présente.
- **`ok` concerne le protocole, pas la décision d'accès** : un badge refusé donne `ok=1` sans `act`.

<!-- debut:tableau-cles -->
| Clé | Définition | Valeurs permises | Capacité qui l'autorise |
|---|---|---|---|
| `ok` | accusé **protocolaire** ; **réponse minimale**, toujours comprise ; première ligne | `1` acceptée ; `0` refusée définitivement | base (aucune) |
| `err` | motif de refus, seulement avec `ok=0` | `version`, `invalid`, `auth`, `replay` (liste ouverte) | base (aucune) |
| `t` | heure du serveur | secondes Unix UTC, 0 à 4294967295 | `time` |
| `act` | ouvrir la gâche pendant N millisecondes ; seulement en réponse à `tag`, `pin`, `tagpin` ou `input` | 100 à 60000 | `relay` |
| `led` | commande de la LED ; mêmes événements que `act` | `<couleur>,<ms>` : `green`, `red`, `amber`, `off` (liste ouverte) ; 1 à 60000 | `led` |
| `buzz` | commande du buzzer ; mêmes événements que `act` | `accept`, `deny`, `error` (liste ouverte) | `buzz` |
| `hb` | période de battement voulue | 10 à 86400 secondes | `hb` |
| `cfg` | empreinte de configuration attendue par le plugin | `^[0-9a-f]{8}$`, opaque | `cfg` |
| `sig` | signature de la réponse ; dernière ligne quand elle est présente | 64 chiffres hexadécimaux minuscules | `hs256` |
<!-- fin:tableau-cles -->

**Codes HTTP** : `200` avec `ok=1` ; `400` avec `ok=0` et `err=invalid` ou `err=version` ; `403` avec
`ok=0` et `err=auth` ou `err=replay`. Le plugin signe toute réponse à une requête qui a franchi l'étape 3 de l'ordre
d'évaluation (identité et authentification), `replay` compris ; `auth`, `invalid` et `version` ne sont
pas signées. Un `rid` de casse différente n'a pas franchi l'étape 3 : 403 `auth`, non signé.
Un plugin qui reconnaît la version 1 sans la servir encore (version au statut « prévue ») répond `503`
**sans corps** (aucune ligne `ok`) : le lecteur le traite comme un échec transitoire (réémission, jamais
d'ouverture), comme le prévoit « Côté lecteur ». Une erreur interne du plugin pendant le traitement d'un
appel v1 répond `500` sans corps, avec le même traitement côté lecteur.

**Côté lecteur**

- **200 et `ok=1`** : l'événement est retiré de la file. `act` n'est appliqué que si la réponse arrive
  au plus 10 secondes après la survenue de l'événement, et seulement en réponse à `tag`, `pin`, `tagpin` ou `input`.
- **Lecteur sans secret** : `ok=0` avec `err=replay` : « déjà reçu », l'événement est retiré, ce n'est
  pas une perte. **Tout autre `ok=0`** : refus définitif, l'événement est retiré et compté comme perdu.
  Le refus définitif ne vaut que pour un lecteur sans secret.
- **Lecteur muni d'un secret** : tant qu'il n'a jamais reçu de réponse signée valide avec ce secret, un
  `ok=1` non signé retire l'événement **sans appliquer aucune clé** (plugin pas encore appairé). À la
  première réponse signée valide, il mémorise « plugin appairé » (effacé quand le secret change). Avant
  cette première réponse signée, tout `ok=0` non signé est déjà un échec **transitoire** (règle ci-après).
  Ensuite, **seules les réponses signées valides sont définitives** : `ok=1` signé (l'événement est
  retiré) et `ok=0` `err=replay` signé (retiré, pas une perte). Toute autre réponse, dont tout `ok=0`
  non signé (`auth`, `invalid`, `version`) et tout `ok=1` non signé ou mal signé, est un échec
  **transitoire** : l'événement est réémis à l'identique avec un délai croissant, jamais d'ouverture, et
  le lecteur signale l'état (compteur ou voyant « refus non authentifié »). Sans secret appairé, le
  lecteur ignore `cfg` et n'applique pas `t` (« Limite connue »). Un intermédiaire peut
  retarder un événement, plus le supprimer. Conséquence : un refus déterministe (secret régénéré,
  « Rabaisser à v0 ») bloque la file de façon visible jusqu'à la reconfiguration du lecteur.
- **Autre cas** (délai dépassé, erreur 5xx, corps illisible, pas de `ok`) : échec transitoire, réémission
  à l'identique avec un délai croissant, **jamais d'ouverture**.
- Sont ignorés : une clé inconnue, une clé connue de valeur invalide, une clé dont la capacité n'a pas été
  annoncée, une clé d'action en réponse à un autre événement que `tag`, `pin`, `tagpin` ou `input`, et toute ligne
  après `sig`.
- **Clé `hb`** (capacité `hb`) : valable en réponse à n'importe quel événement acquitté (`200` et `ok=1`) ; un
  lecteur muni d'un secret ne l'applique, comme toute clé, que dans une réponse signée valide. La première
  ligne `hb=` fait foi. Absente, illisible ou hors
  de 10 à 86400 secondes, la période en cours ne change pas. La période demandée vaut jusqu'au redémarrage du
  lecteur, qui la ramène à sa valeur de configuration : le plugin la renvoie en réponse au `hello`. Le
  prochain battement reste dû une période après la création du précédent. Un plugin, ou un intermédiaire
  HTTP non signé, peut ainsi repousser le battement de 24 heures au plus, jamais le supprimer.

## Signature de la requête

Algorithme : **HMAC-SHA256** (capacité `hs256` ; son empreinte sur un Uno R3 n'est pas mesurée, voir
« À confirmer »), secret propre au lecteur de **32 octets** (64 chiffres
hexadécimaux). Pas à pas :

1. Décoder le corps selon « Encodage du corps ». Un appel invalide n'est pas signable.
2. Retirer le champ `sig`.
3. Trier les champs par nom, **octet par octet** (`strcmp` ; en PHP `ksort($champs, SORT_STRING)`).
4. Encoder chaque valeur **décodée**, octet par octet : `A-Z a-z 0-9 - . _ ~ ,` restent tels quels, tout
   autre octet devient `%XX` avec l'hexadécimal en **MAJUSCULES**. (En Python :
   `urllib.parse.quote_from_bytes(valeur, safe=',')` ; en PHP :
   `str_replace('%2C', ',', rawurlencode($valeur))`.)
5. Joindre les paires `nom=valeur` par `&`. Un champ absent n'apparaît pas ; un champ présent et vide
   donne `nom=` ; les champs inconnus sont inclus.
6. La clé est formée des **32 octets** décodés des 64 chiffres hexadécimaux du secret (pas de la chaîne
   ASCII).
7. `sig` = HMAC-SHA256(clé, chaîne canonique en ASCII), en **64 chiffres hexadécimaux minuscules, sans
   troncature**.
8. Le récepteur compare en temps constant (`hash_equals`).

Le lecteur émet ses champs dans l'ordre canonique, `sig` en dernier : le corps privé de `&sig=…` est alors
la chaîne canonique. Le récepteur, lui, reconstruit la chaîne canonique et n'exige aucun ordre.

### Exemple travaillé

Secret de test, **public** (SECRET DE TEST PUBLIC : jamais sur un lecteur réel). Exigence normative : le
secret d'un lecteur est généré par le plugin avec un générateur cryptographique (`random_bytes(32)`),
et le plugin **refuse** cette valeur de test à l'appairage, à la régénération et à l'import ; seul le
banc de test (UC 019 de la feuille de route) peut l'installer, sur `TEST-V1-SIGNE`, par un réglage
explicite.

```
000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
```

Un badge 26 bits est présenté au lecteur `TEST-V1-SIGNE` (données `0x7a3f2c`, site 122, carte 16172). Chaîne
canonique (champs triés, `sig` exclu) :

```
bits=26&board=uno-w5100&boot=3&card=16172&ev=tag&fac=122&fw=1.0.0&par=ok&raw=2f47e58&rid=TEST-V1-SIGNE&seq=1&up=42&v=1
```

HMAC-SHA256 de cette chaîne avec la clé ci-dessus :

```
b764c79fd9e4156c1c771c4820a286a39d34dacc1c560b3e4c9bc23cb8de638d
```

Corps envoyé : la chaîne canonique suivie de `&sig=` et de la signature.

Un vecteur d'encodage (`v1-encodage`) exerce toutes les règles de l'étape 4 de la signature : la valeur décodée
`a b,c~d%é` (avec `é` sur deux octets UTF-8) s'écrit `a+b%2Cc~d%25%C3%A9` dans le corps, mais
`a%20b,c~d%25%C3%A9` dans la chaîne canonique ; un champ vide donne `xvide=`.

## Signature de la réponse

La chaîne canonique d'une réponse est `req=<sig de la requête>` suivie d'un saut de ligne, puis de chaque
ligne du corps jusqu'à la première ligne commençant par `sig=` (exclue), sans son fin de ligne, chacune
terminée par `\n`. Même clé, même HMAC, même encodage. Pour une réponse `ok=1` à la requête de l'exemple :

```
req=b764c79fd9e4156c1c771c4820a286a39d34dacc1c560b3e4c9bc23cb8de638d
ok=1
```

donne `sig=f4950563554fc4707894dde9f3fc8b97516fa14389d55f069a25a361cde1f325`. La réponse est signée
seulement si la requête l'était. Une chaîne canonique de requête ne contient jamais de saut de ligne :
les deux domaines de signature sont distincts.

## Anti-rejeu, fraîcheur et événements différés

- Le couple (`boot`, `seq`) croît **strictement** par lecteur ; des trous sont permis. Le premier
  événement après un démarrage est un `hello`. Une réémission est identique octet pour octet ; un
  événement converti en `offline` garde son `boot` et son `seq`.
- **File strictement FIFO** : un événement n'est émis qu'après la réponse définitive du précédent (au
  sens de « Côté lecteur »), ou sa conversion en `offline`. Exception : un `hb` jamais acquitté et hors envoi
  peut être abandonné, jamais réémis, quand un autre événement attend derrière lui ; il laisse un trou de
  `seq`. Le `hello` n'est jamais abandonné.
- Côté plugin, pour un lecteur appairé : un appel n'est accepté que si son couple est supérieur au
  dernier couple accepté ; un refus n'avance pas le compteur ; un nouvel appairage le remet à zéro.
- **Remise à zéro de `boot`** (nouveau flash complet) : le secret, `boot` et l'indicateur d'appairage
  sont effacés, et la seule sortie est un **nouvel appairage**. Un `replay` en réponse à un `hello`
  signale un `boot` régressé.
- **Fraîcheur sans horloge** : un lecteur n'a pas d'heure fiable. Un événement direct non délivré 30
  secondes après sa survenue est émis en `offline`. Le plugin compare, dans un même `boot`, l'écart des
  `up` à l'écart des heures de réception **par rapport au dernier événement accepté du même `boot`**
  (jamais le `hello` seul) ; au-delà de la tolérance (à confirmer), l'événement n'est jamais traité
  comme un événement direct. Le `hello` n'est soumis à aucun contrôle de fraîcheur.
- `offline` n'appelle **aucune** clé d'action et ne modifie **aucun** compteur d'échecs ; un `age` au-delà
  de 4294967 secondes est écarté et compté comme perdu.

## Ordres

Les ordres du plugin vers le lecteur (serveur d'ordres, capacité informative `srv`) seront définis par
une UC ultérieure de la feuille de route, qui précisera leur format, la séparation de leur domaine de signature et les
motifs `t` et `stale`. L'accusé `ack` (`oseq`, `res`, `why`) est déjà défini ici.

## Règles d'évolution

Un récepteur **ignore tout champ ou toute clé inconnu**, dans les deux sens (du lecteur vers le plugin et
du plugin vers le lecteur).

**Gardent `v=1`** (ajouts compatibles) : un champ facultatif ; un type d'événement (un plugin qui
l'ignore répond `ok=1` et ne fait rien : l'événement doit donc être sûr par défaut) ; une capacité ; une
clé de réponse (envoyée seulement si la capacité est annoncée) ; une valeur d'énumération ouverte ; un
algorithme de signature **sous une nouvelle capacité**, fixé à l'appairage ; un vecteur de référence.

**Imposent `v=2`** (liste exhaustive), la v1 restant servie :

1. changer le sens, l'unité, l'encodage ou les bornes (tailles maximales comprises) d'un champ, d'une clé
   ou d'une valeur existants ;
2. rendre obligatoire un champ facultatif, rendre facultatif ou retirer un champ obligatoire ;
3. renommer ou retirer un champ, un événement, une clé, une capacité normative ou une valeur ;
4. faire déclencher une action par une valeur ou un événement qu'un récepteur v1 ignore ;
5. modifier la signature : algorithme d'une capacité existante, longueur du secret, chaîne canonique
   (ordre, encodage, séparateurs, champs absents, exclusion de `sig`), encodage ou troncature de `sig`,
   liaison `req=` ;
6. modifier l'anti-rejeu ;
7. modifier le transport : méthode, type de contenu, route, place des champs, règles d'analyse, ordre
   d'évaluation ;
8. modifier le format de réponse : lignes, `ok` en tête et son sens, place de `sig` ;
9. utiliser un nom de paramètre de la v0.

## Le protocole v0 reste inchangé

La v1 ne modifie en rien la v0 : requêtes `GET` sur la route d'origine `/plugins/badger/…` (relayée) ou
sur la route courante sans paramètre de version, paramètres `name`, `ip`, `cmd`, `value` et `model`,
badge en hexadécimal, en décimal ou `Analog1` à `Analog5`, réponse jamais lue par le lecteur. Un appel
sans paramètre de version, ou venant de l'ancienne route, est traité en v0 à l'identique, pour toujours.
Son contrat figé est conservé dans le dépôt du plugin (`.claude/compat/vecteurs-v0.json` et
`.memory/analyse/badger-protocole-versions.md`, § 3).

## À confirmer

Ces points ne sont **pas normatifs** : ils se lèvent à la mesure ou à la recette, sans casser le reste.

- **HMAC-SHA256** (étape « Algorithme » de la signature) : son empreinte en mémoire flash et en RAM sur un Arduino Uno R3 avec une carte W5100
  n'est **pas encore mesurée** (UC 008 et 009 de la feuille de route). Si elle ne tient pas, un
  algorithme allégé sera **ajouté** sous une capacité distincte ; HMAC-SHA256 et ses vecteurs restent
  valides.
- Les tolérances : fraîcheur de 30 secondes, conversion en `offline` à 30 secondes, `act` appliqué au plus
  10 secondes après la survenue. Ajuster ces tolérances reste compatible v1 (ni bornes de champ ni
  ordre d'anti-rejeu).
- La méthode de calcul de l'empreinte `cfg` (UC 018 de la feuille de route).

## Vecteurs de référence

Le fichier `.claude/compat/vecteurs-v1.json` du dépôt contient des requêtes et des réponses exactes que le
sketch et le plugin doivent tous deux reproduire : un cas valide par événement, des requêtes signées
(avec chaîne canonique et signature calculées), un rejeu, une version inconnue, un champ inconnu, des
appels invalides, une réponse signée. Ces vecteurs sont **figés** : on en ajoute, on n'en modifie ni n'en
retire jamais.
