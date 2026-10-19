# Protocole v1 des lecteurs : référence technique

> **Statut : le plugin reçoit la v1 ; le sketch et la signature sont en préparation.** Le plugin sert
> désormais ce protocole : il valide chaque appel, identifie le lecteur par son `rid`, applique aux `tag` et
> `pin` les mêmes effets qu'un badge ou un code v0 et répond `ok=1` sans clé d'action. La signature, l'appairage
> et la détection du rejeu sont en préparation, comme le sketch unifié `Badger2` (non publié). **Vos
> lecteurs actuels ne sont pas concernés** : ils continuent d'appeler le plugin exactement comme avant
> (voir « Le protocole v0 reste inchangé »). Cette page fixe le contrat que le sketch unifié `Badger2` et le
> plugin respectent tous les deux ; elle s'adresse aux utilisateurs avancés et aux contributeurs.

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
  (désactivé par défaut). Pour la même raison, tant qu'aucun secret n'est configuré, le sketch applique
  `hb`, `led` et `buzz` non authentifiés, mais **ignore** `cfg` et n'applique pas `t` (voir « Côté
  lecteur »). Un lecteur muni d'un secret n'applique aucune clé d'une réponse non signée.

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
   inclusion), un `rid` de casse différente ou qui désigne un équipement qui n'est pas un lecteur, une adresse
   de connexion interdite (bouclage ou adresse du serveur, **même en inclusion**), une adresse de connexion
   différente de celle enregistrée pour le lecteur (hors inclusion), un lecteur sous son plancher de version,
   une signature fausse. Tant que l'appairage n'existe pas (UC 017), le plugin contrôle l'adresse enregistrée
   du lecteur ; un appel v0 sous le même nom peut aujourd'hui mettre cette adresse à jour (la verrouiller relève de
   l'UC 101, le secret de l'UC 017) : ce contrôle n'est donc pas une authentification. Prévoyez une réservation
   d'adresse (DHCP) pour chaque lecteur. En inclusion, un `rid` inconnu crée un lecteur **inactif** et l'appel qui le
   crée n'a aucun autre effet ; les appels suivants restent sans effet jusqu'à son activation.
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
| `offp` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`deny`, `list`, `open`) : politique du lecteur quand Jeedom est injoignable | — | `hello` |
| `oport` | entier 1 à 65535 : port du serveur d'ordres du lecteur ; présent si et seulement si `caps` contient `srv` | — | `hello` |
| `wl` | entier 0 à 65535 : capacité de la liste blanche locale (nombre d'entrées au plus) ; présent si et seulement si `caps` contient `wl` | — | `hello` |
| `mem` | entier 0 à 4294967295 : mémoire libre en octets | — | `hb` |
| `q` | entier 0 à 65535 : événements en file d'attente | — | `hb` |
| `lost` | entier 0 à 4294967295 : événements écartés d'une file pleine, refusés définitivement ou impossibles à émettre depuis le démarrage ; un `hb` écarté n'est pas compté ; absent : aucune perte connue | — | `hb` |
| `door` | jeton `^[a-z][a-z0-9_]{0,15}$`, liste ouverte (`open`, `closed`) | `door`, `offline` (`oev=door`) | `hb` |
| `rssi` | entier -127 à 0 (Wi-Fi seulement) | — | `hb` |
| `wlv` | `^[0-9a-f]{8}$` : version de la liste blanche active ; absent : aucune liste active | — | `hb` |
| `wlr` | entier 0 à 65535 : prochain rang attendu d'une liste en cours de réception ; absent : rang 0 | — | `hb` |
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
| `oseq` | entier 0 à 4294967295 : `seq` de l'ordre accusé (`0` : ordre non authentifié) | `ack` | — |
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
- `ack` : accusé d'un ordre reçu du plugin (UC 012, voir « Ordres ») ;
- `offline` : événement direct (`tag`, `pin`, `tagpin`, `input`, `door`) qui n'a pas pu être délivré à temps, rejoué
  avec son âge.

**Écart à la spécification initiale** : le contact de porte produit **seulement** l'événement `door`,
jamais `input`, pour éviter deux événements pour un même contact. L'entrée analogique reste dans `input`,
avec `st` (état logique) et `val` (lecture brute).

**Champs sensibles** : `raw`, `fac`, `card`, `code`, `key` et leurs copies dans un événement `offline` ne figurent
jamais dans l'adresse ni, en clair, dans un journal (hors mode de débogage explicite). Un refus nomme le
champ, jamais sa valeur.

**Hors du contrat initial** (ajouts compatibles, définis par leur propre UC de la feuille de route) : champs `loc`, `net`, `qmax`, `wfmt`.

Ajouté depuis (compatible, `v=1` inchangé) : champ `port` (UC 005), facultatif pour `tag` ; événements `tagpin`
(badge puis code) et `key` (touche par touche), champ `key`, et `port` facultatif pour `pin` (UC 006) ; champ
`lost`, facultatif pour `hb` (UC 008) ; champs `offp` et `wl` facultatifs du `hello`, champs `wlv` et `wlr` facultatifs du `hb`,
capacité et clé de réponse `wl`, et l'émission en `offline` d'un passage décidé par le lecteur (UC 011, voir « Mode hors
ligne et liste blanche ») ; champ `oport` facultatif du `hello`, jeton `srv`, format des ordres du plugin vers le lecteur et
émission de l'événement `ack` (UC 012, voir « Ordres ») ; jetons informatifs `console` et `status_led` du `hello` (UC 013, voir
« Capacités du sketch Badger2 ») ; jeton informatif `ota` du `hello` (UC 014, voir « Capacités du sketch Badger2 »).

**Capacités du sketch Badger2** (UC 008, 009, 010, 011, 012, 013 et 014) : le `hello` d'un lecteur Badger2 annonce des jetons
**normatifs**, qui autorisent chacun une clé de réponse : `hb` (clé `hb`), `hs256` (clé `sig`, avec un secret),
`time` (clé `t`, avec un secret seulement), `relay` (clé `act` : gâche câblée **et** secret, ou accusé explicite de
l'installateur pour des réponses non signées), `led` et `buzz` (clés `led` et `buzz`, sortie câblée) et, depuis l'UC 011, `wl` (clé `wl`, la liste blanche locale :
politique hors ligne « liste » et secret seulement). Il annonce aussi
des jetons **informatifs**, que le plugin affiche et n'exploite pas : `wdt` (chien de garde matériel), `wg_26`, `wg_34`, `wg_37` (décodage du site et de la carte),
`wg_port2` (second lecteur Wiegand), `kp` (clavier), `kp_burst` (code en une trame), `kp_tagpin` (badge puis
code), `kp_key` (touche par touche), `bootnp` (UC 009 : le compteur de démarrages `boot` n'a pas pu être
enregistré, un rejeu est possible au démarrage suivant), `srv` (UC 012 : le lecteur écoute les ordres du plugin, port dans le champ
`oport`), `console` (UC 013 : la console de provisionnement du lecteur est compilée ; elle permet de changer l'identité et le secret
par le port série du lecteur), `status_led` (UC 013 : une LED d'état est câblée), `ota` (UC 014 : la mise à jour à distance du lecteur est active, c'est-à-dire compilée
et protégée par un mot de passe ; elle se pilote depuis l'outil du développeur, jamais par le protocole ; carte ESP seulement), puis un jeton `io_*` par entrée ou sortie câblée (`io_strike`, `io_led`,
`io_buzz`, `io_door`, `io_exit`, `io_exit_open`, `io_tamper`, `io_bell`, `io_a1` à `io_a5`). Aucun jeton
informatif n'autorise une clé de réponse. Le `rst` d'un lecteur Badger2 vaut `power` (mise sous tension), `ext` (bouton reset),
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
| `wl` | `wl` |

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
| `wl` | fragment de la liste blanche locale du lecteur ; seulement avec `hs256`, pour un lecteur qui annonce `wl` | `<version>,<total>,<rang>` puis 0 à 3 `,<empreinte>` : version 8 chiffres hexadécimaux, empreintes de 16, total et rang de 0 à 65535, `rang` + nombre d'empreintes au plus égal à `total`, aucune empreinte seulement si `total` vaut 0 | `wl` |
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
  `ok=1` non signé **ou à signature invalide** retire l'événement **sans appliquer aucune clé** (plugin pas encore appairé). À la
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
- **Clé `wl`** (capacité `wl`, UC 011) : un fragment de la liste blanche locale (voir « Mode hors ligne et liste
  blanche »). Valable en réponse à n'importe quel événement acquitté (`200` et `ok=1`), **seulement dans une réponse
  signée valide** d'un lecteur muni d'un secret, comme toute clé. La première ligne `wl=` fait foi, valide ou non ; une
  réponse coupée en cours de ligne ne donne aucun fragment. Absente, hors motif ou hors bornes, elle ne change rien.

## Signature de la requête

Algorithme : **HMAC-SHA256** (capacité `hs256` ; le sketch Badger2 qui l'implémente exige une Mega 2560 ou un ESP : une
Uno, restée en protocole v0, ne l'embarque pas, voir « À confirmer »), secret propre au lecteur de **32 octets** (64 chiffres
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

Toute autre utilisation du secret, interne au lecteur ou au plugin, signe un message `badger2:<usage>` (ASCII,
sans `=` ni saut de ligne) : ce n'est jamais une chaîne canonique de requête (qui contient `=`) ni de réponse
(qui commence par `req=`). Usage réservé : `badger2:appairage`.

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
  secondes après sa survenue est émis en `offline`. Le sketch Badger2 (UC 011) émet aussi en `offline`, **quel que soit son
  âge**, un passage dont il a pris la décision seul, hors ligne (voir « Mode hors ligne et liste blanche »). Le plugin compare, dans un même `boot`, l'écart des
  `up` à l'écart des heures de réception **par rapport au dernier événement accepté du même `boot`**
  (jamais le `hello` seul) ; au-delà de la tolérance (à confirmer), l'événement n'est jamais traité
  comme un événement direct. Le `hello` n'est soumis à aucun contrôle de fraîcheur.
- `offline` n'appelle **aucune** clé d'action et ne modifie **aucun** compteur d'échecs ; un `age` au-delà
  de 4294967 secondes est écarté et compté comme perdu. Le plugin accepte un `offline` de tout âge (le lecteur a décidé
  du passage) ; il n'en déduit **aucune décision d'accès ni aucun compteur**. L'`age` est calculé par le lecteur, en
  secondes entières (`up` de l'émission moins la date de survenue) : sa précision est d'une seconde plus la dérive de
  son oscillateur.

## Mode hors ligne et liste blanche

Ajout compatible de l'UC 011 (`v=1` inchangé). Un plugin qui ignore `offp`, `wl`, `wlv` et `wlr` répond `ok=1` et le
lecteur reste nominal en ligne ; l'UC 309 constitue et envoie la liste. L'ordre `sync` de l'UC 012 ne transporte aucun fragment : il provoque un battement
immédiat (qui porte `wlv` et `wlr`), et le plugin répond par la clé `wl`.

**Politique hors ligne** (champ `offp` du `hello`). Ce que le lecteur fait d'un badge ou d'un code quand Jeedom est
injoignable, choisi à la compilation du sketch et annoncé à chaque démarrage :

- `deny` (défaut) : rien ne s'ouvre. Le passage est gardé dans la file et rejoué en `offline` ; le lecteur joue le motif
  d'erreur.
- `list` : ouvre seulement pour un badge ou un code dont l'**empreinte** figure dans la liste blanche locale (capacité `wl`,
  qui exige un secret). Une liste vide ou absente refuse tout.
- `open` : **DANGEREUX, toute présentation ouvre la porte** quand Jeedom est injoignable, y compris un badge inconnu. Réservé à la
  sécurité incendie, accepté par écrit dans la configuration du lecteur. Le plugin doit afficher ce choix (UC 309). Tant
  qu'un plugin répond `503` à la v1, le lecteur croit Jeedom injoignable : chaque badge ouvre.

Dans les trois cas, la réponse de Jeedom reste la seule règle en ligne : le mode hors ligne n'ouvre **jamais sur une
réponse**, seulement par une décision locale du lecteur.

**Détection.** Le lecteur se croit hors ligne après 2 échecs consécutifs (Jeedom injoignable, réponse non conforme ou non
authentifiée) ou 10 secondes sans réponse alors qu'un événement attend ; il revient en ligne à la première réponse
définitive (`ok=1`, `replay`, refus). Ces deux seuils se règlent à la compilation.

**Décision locale.** Pour le dernier passage seulement, une fois, tant qu'il a moins de 10 secondes : si le lecteur est
hors ligne, ou si le passage attend depuis 5 secondes sans être en cours d'envoi **et** qu'au moins un échec n'a pas été
résolu par une réponse depuis sa survenue, il décide seul : toute décision locale exige une preuve que Jeedom est
injoignable. Sans cette preuve (un seul délai dépassé, un plugin lent), les 5 secondes ne décident rien et le comportement
reste celui d'avant (motif d'erreur, événement direct). Un échec isolé d'une tentative ne décide rien. Tant qu'une ouverture
locale reste possible, le motif d'erreur n'est pas joué au premier échec (pas de signal contradictoire). Ouvrir donne la gâche pendant 3 secondes par défaut (au plus le plafond d'ouverture), la LED verte
et le motif `accept` ; refuser donne le motif d'erreur. Jamais d'ouverture sur une trame Wiegand dont la parité est fausse.
Dans les deux cas, le passage est converti sans attendre en `offline` (il part ensuite, dans l'ordre, avec son âge).

**Empreinte** (normative). Les 8 premiers octets, en 16 chiffres hexadécimaux minuscules, de HMAC-SHA256 avec la clé du
lecteur (les 32 octets du secret) d'un message ASCII dont les valeurs s'écrivent comme dans les champs du même nom (le port
Wiegand n'y entre pas) :

| Passage | Message |
|---|---|
| `tag` | `badger2:wl:tag:<bits>:<raw>` |
| `pin` | `badger2:wl:pin:<code>` |
| `tagpin` | `badger2:wl:tagpin:<bits>:<raw>:<code>` |

Avec le secret de test public ci-dessus : `badger2:wl:tag:26:2f47e58` donne `b53c6e4c805d7d77`, `badger2:wl:pin:1234`
donne `1be3a834e9a43a5e` et `badger2:wl:tagpin:26:2f47e58:1234` donne `42b954195edd72ab`. L'outil
`tests/harnais/protocole_v1.py empreinte <message>` (secret sur l'entrée standard) les recalcule. Un badge inscrit en
v0 est reconstitué par le plugin avec sa parité pour obtenir `raw`.

**Clé de réponse `wl`** (capacité `wl`, avec `hs256`) : `wl=<version>,<total>,<rang>` puis 0 à 3 `,<empreinte>`. La
version a 8 chiffres hexadécimaux, `total` et `rang` valent de 0 à 65535, `rang` plus le nombre d'empreintes ne dépasse pas
`total`, et il n'y a aucune empreinte seulement si `total` vaut 0 (liste vide). La ligne fait 74 octets au plus et la clé
n'apparaît qu'une fois. Le `hello` annonce `wl=<capacité>` (nombre d'entrées au plus, 128 par défaut, 200 au maximum) ; le `hb`
annonce `wlv=<version>` de la liste active (absent : aucune) et `wlr=<rang>` quand une réception est en cours (absent : rang 0).

**Règles du lecteur.** Un fragment n'est lu que dans une réponse signée valide à un événement acquitté, la première ligne fait
foi. Rang 0 : la réception recommence, refusée en bloc si `total` dépasse la capacité annoncée (la liste en place est
conservée, jamais tronquée). Le rang attendu (`wlr`) de la même version est rangé ; un autre rang de la même version est
ignoré ; une autre version à un rang non nul abandonne la réception. Une version égale à celle de la liste active est
ignorée sans aucune écriture. Au dernier fragment, la nouvelle liste remplace l'ancienne **d'un bloc** (deux banques en
mémoire non volatile, bascule atomique, un en-tête avec CRC-16), liée au secret : un autre secret efface la liste. Après un
redémarrage, la réception en cours recommence au rang 0 ; la liste active, elle, est conservée.

**Règles du plugin** (UC 309). N'envoyer `wl` qu'à un lecteur appairé qui annonce `wl` et `hs256`, jamais plus d'entrées que
la capacité `wl`, au rang `wlr` (0 sans `wlr`), et s'arrêter quand `wlv` égale la version envoyée. Ne jamais envoyer `wl`
pour une version égale au `wlv` annoncé, et ne relancer une liste que si son contenu a changé. Utiliser une version strictement croissante (jamais réutilisée : le lecteur ne compare pas les versions, voir « Limites
à connaître »). Ne pas journaliser les
empreintes. Un fragment par réponse : 3 empreintes par événement acquitté (le battement, par défaut toutes les 60 secondes,
en est le plus régulier), soit environ 43 battements pour 128 entrées.

**Limites à connaître.**

- « Jamais en clair » n'est pas « confidentiel » : avec la carte en main (secret et liste dans la même puce), un badge de 26
  bits ou un code court se retrouve par force brute. L'empreinte protège le transit et l'export côté plugin.
- Après 5 codes faux consécutifs hors ligne (politique `list`), les codes sont refusés pendant 60 secondes, durée doublée à
  chaque nouveau blocage (3600 secondes au plus). Un code accepté ou le retour en ligne ne remettent pas le compteur à zéro :
  compteur et doublement retombent à zéro après une heure sans aucun refus. Le compteur est perdu au redémarrage. Préférer
  un code de 6 chiffres ou plus.
- **Aucun anti-force-brute pour un badge seul** : le blocage ne compte que les codes. Une injection de trames Wiegand sur le
  câble, réseau coupé, peut essayer des valeurs sans limite. Pour un accès sensible, inscrire des passages badge + code.
- **Aucune monotonie de version côté lecteur** : il range toute version différente de la sienne. Une ancienne réponse signée
  rejouée pourrait réinstaller une ancienne liste (un badge retiré depuis y figurerait). Le plugin (UC 309) doit utiliser une
  version strictement croissante et ne jamais en réutiliser une ; le format ne change pas. Un clavier qui envoie le code en une seule trame perd les zéros de tête
  (`0123` devient `123`).
- Un badge retiré reste accepté hors ligne jusqu'à l'envoi de la liste suivante.
- La bascule atomique est garantie sur Mega (EEPROM) ; sur ESP32 elle repose sur l'enregistrement du bloc par le cœur (à
  confirmer en recette) ; la politique `list` est refusée à la compilation sur ESP8266, dont `commit()` efface un secteur.

## Ordres

Ajout compatible de l'UC 012 (`v=1` inchangé) : le plugin peut envoyer au lecteur des **ordres signés** (ouvrir la
gâche, commander la LED ou le buzzer, demander un battement, resynchroniser la liste blanche, redémarrer). Un plugin qui
n'en envoie aucun laisse le lecteur nominal : le port d'ordres reste muet. Le sketch Badger2 n'écoute que s'il a un
**secret** (sans secret, aucun port n'est ouvert), si son compteur de démarrages `boot` est enregistré, si le serveur
n'est pas coupé dans sa configuration et si le module réseau le permet (Mega avec W5100, W5200 ou W5500, ESP ; **jamais**
avec un module ENC28J60). Quand il écoute, il annonce le jeton informatif `srv` dans `caps` et le champ `oport` du `hello`
(l'un ne va pas sans l'autre).

**Le port d'ordres ne doit jamais être joignable depuis Internet** (aucune redirection de port du routeur) : isolez le
réseau des lecteurs. L'ordre voyage en clair : il ne contient aucun secret, mais une écoute du réseau montre l'opération
demandée (la signature empêche seulement de l'inventer, de le modifier ou de le rejouer).

### Transport

- `POST /ordre HTTP/1.1` (`HTTP/1.0` accepté) sur le port `oport` (80 par défaut), avec `Content-Length` exact de 1 à
  192 et `Connection: close`. Ni `Transfer-Encoding: chunked`, ni chaîne de requête ; les autres en-têtes sont ignorés.
- Le corps est `<message>:<sig>`, un saut de ligne (`\n` ou `\r\n`) final toléré.

### Message signé

Message ASCII : `badger2:ordre:<rid>:<boot>:<seq>:<t>:<op>[:<arg>]`.

- `rid` : celui du lecteur, **casse comprise**. `boot` : le `boot` du dernier événement reçu du lecteur ; un ordre n'est valable
  que pour un démarrage donné. `seq` : de 0 à 4294967295, **strictement croissant** par (`rid`, `boot`), à partir de 1
  (le `seq` 0 est refusé : `oseq=0` est réservé à « ordre non authentifié »). `t` : l'heure Unix UTC du plugin.
- Les nombres suivent `(0|[1-9][0-9]{0,9})` et tiennent sur 32 bits.
- `sig` = HMAC-SHA256 des 32 octets du secret du lecteur et du message, en 64 chiffres hexadécimaux minuscules, comparée
  par le lecteur **en temps constant**. Le préfixe `badger2:ordre:` sépare ce domaine de signature de ceux des requêtes
  (chaîne canonique), des réponses (`req=`), de `badger2:appairage` et de `badger2:wl:`.

| Opération | Argument | Capacité annoncée qu'elle exige |
|---|---|---|
| `open` | durée en millisecondes, 100 à 60000 | `relay` |
| `led` | `<couleur>,<ms>` (couleurs de la clé `led`, durée de 1 à 60000) | `led` |
| `buzz` | `<motif>` (motifs de la clé `buzz`) | `buzz` |
| `hb` | aucun | `hb` |
| `sync` | aucun | `wl` |
| `reboot` | aucun | `wdt` |

L'argument reprend le motif de la clé de réponse homonyme. **Durée effective de `open`** : le plus petit de l'argument et du
**plafond d'ouverture du lecteur** (`BADGER2_OUVERTURE_MAX_MS`, 10 secondes par défaut) ; le plugin ne suppose jamais plus que ce
plafond. Une ouverture ne se cumule jamais avec une autre en cours : la plus longue des fins l'emporte. `hb` provoque un
battement immédiat, et `sync` aussi (le `hb` porte `wlv` et `wlr` : le plugin répond par la clé `wl`, aucun fragment de liste ne
voyage dans l'ordre). `reboot` répond 200 et un `ack`, puis le lecteur redémarre dès que sa file est vide et que l'envoi, le
serveur et la gâche sont au repos, **au plus 10 secondes après l'ordre et jamais pendant une impulsion de gâche** ; les
événements encore en file à ce moment sont perdus. Les badges présentés pendant l'attente du chien de garde (environ 2 secondes)
et le redémarrage ne sont pas lus. Le `hello` qui suit porte `rst=sw` et un `boot` augmenté de un.

Exemple, avec le secret de test public (lecteur `TEST-V1-SIGNE`, `boot` 5, `seq` 1, heure `1792310400`, ouvrir 3 secondes) :

<!-- debut:exemple-ordre -->
```
badger2:ordre:TEST-V1-SIGNE:5:1:1792310400:open:3000:8220f9d1a0ea0bf55071d2b667063a02a708f2547a53275c46459d450c8ddd4f
```
<!-- fin:exemple-ordre -->

L'outil `tests/harnais/protocole_v1.py ordre <message>` (secret sur l'entrée standard) signe un message et recalcule cet exemple.

### Ordre d'évaluation (côté lecteur)

| # | Contrôle | Refus `why` | HTTP | `ack` |
|---|---|---|---|---|
| 0 | une connexion acceptée par 250 ms au plus (la suivante attend dans la file d'écoute) | — | — | — |
| 1 | moins de 1000 ms depuis le dernier ordre traité | `busy` | 503 | non |
| 2 | requête HTTP lisible : ligne, `Content-Length` jusqu'à 192, en-têtes jusqu'à 1024 octets, complète en 2 secondes | `param` | 400 | non |
| 3 | le dernier `:` est suivi de 64 chiffres hexadécimaux minuscules | `sig` | 403 | oui, `oseq=0` |
| 4 | syntaxe du message | `param` | 400 | oui, `oseq=0` |
| 5 | HMAC | `sig` | 403 | oui, `oseq=0` |
| 6 | `rid` identique, `seq` non nul (l'ordre est authentifié dès ici) | `param` | 400 | oui |
| 7 | `boot` différent du démarrage courant | `stale` | 403 | oui |
| 8 | `seq` inférieur ou égal au dernier accepté de ce démarrage | `replay` | 403 | oui |
| 9 | heure du lecteur inconnue, ou écart avec `t` de plus de 10 secondes ; **sauf `hb` et `sync`** (effet bénin, ils servent à resynchroniser l'heure) | `stale` | 403 | oui |
| 10 | opération inconnue, ou capacité non annoncée | `unknown` | 400 | oui |
| 11 | argument hors motif ou bornes : `param` ; couleur ou motif inconnu : `unknown` | `param` ou `unknown` | 400 | oui |
| — | accepté | — | 200 `ok=1` | oui |

- Un refus répond `ok=0` puis `why=<motif>` ; la réponse HTTP **n'est pas signée** et reste informative : seul l'`ack` (signé par le
  canal du lecteur) fait foi. Le `seq` n'avance que pour un ordre accepté. L'heure du lecteur est celle de la clé de réponse `t`
  (signée) : sans elle, `open`, `led`, `buzz` et `reboot` sont refusés `stale`.
- Le rejeu est évalué avant la fraîcheur : le rejeu d'un ordre accepté est `replay` quel que soit le délai ; un ordre **neuf** dont
  l'heure est périmée est `stale`, comme tout ordre d'un autre démarrage.
- **Un refus ne produit un `ack` qu'une fois par 10 secondes** (deux fenêtres : refus authentifiés, refus non authentifiés ; un flot
  de signatures bidon ne fait pas taire un `stale` ou un `replay` légitime). Un `ack` n'entre dans la file que s'il reste au moins
  deux places : sinon le lecteur répond 503 `busy`, n'exécute rien et n'avance pas `seq`. **Pas d'`ack`, pas d'action.**
- `busy` n'est jamais dans un `ack`. Tout ordre lisible traité arme l'intervalle de 1000 ms, authentifié ou non : un flot de requêtes
  peut rendre le canal d'ordres indisponible (503), il ne gêne jamais la lecture des badges. Le canal d'ordres n'est donc pas un chemin
  de sûreté : l'ouverture d'urgence d'une porte ne doit pas en dépendre.

### Accusé `ack`

Chaque ordre authentifié ou refusé (dans la limite des fenêtres ci-dessus) est accusé par un événement `ack` signé comme les autres
événements : `oseq` est le `seq` de l'ordre authentifié, **`0` sinon** (le lecteur ne renvoie jamais une valeur choisie par un tiers) ;
`res` vaut `acc` ou `ref` ; `why` n'accompagne que `ref` (`sig`, `replay`, `stale`, `unknown`, `param`). Le motif `nosecret` n'est pas
émis par Badger2 (sans secret, aucun serveur). Un `ack` ne se perd jamais au détriment d'un badge : en file pleine, il est écarté
avant tout événement d'accès (et compté dans `lost`).

### Règles du plugin (UC 305 et 309)

N'envoyer un ordre qu'à un lecteur appairé qui annonce `srv` et `hs256` ; envoyer l'heure `t` signée dans la réponse au `hello` et à
chaque `hb` ; espacer les ordres d'au moins une seconde ; ne considérer un ordre exécuté que sur un `ack res=acc` portant le bon `oseq`
(la réponse HTTP ne vaut rien seule) ; sur `stale`, envoyer `hb` puis recommencer avec un nouveau `seq` ; ne jamais exposer le port d'ordres
à Internet. Après la restauration de la base du plugin, les `seq` repartent bas : le lecteur répond `replay` jusqu'à son redémarrage.

### Évolution

Une nouvelle opération est un ajout compatible (`v=1`). Changer la grammaire du message impose un autre préfixe : une v2 des ordres.

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

- **HMAC-SHA256** (étape « Algorithme » de la signature) : il tient en mémoire flash et en RAM sur une Arduino Mega 2560 avec une
  carte W5100 (sketch Badger2 0.7.0, UC 009) ; il ne tient pas dans les 32 Ko d'une Uno, qui reste en protocole v0
  (décision du 2026-10-19). Aucun algorithme allégé n'est prévu. Son temps de calcul sur la
  carte (quelques dizaines de millisecondes par requête) reste à confirmer au banc.
- Les tolérances : fraîcheur de 30 secondes, conversion en `offline` à 30 secondes, `act` appliqué au plus
  10 secondes après la survenue. Ajuster ces tolérances reste compatible v1 (ni bornes de champ ni
  ordre d'anti-rejeu).
- La méthode de calcul de l'empreinte `cfg` (UC 018 de la feuille de route).
- Mode hors ligne (UC 011) : le coût du calcul d'une empreinte (une dizaine de millisecondes sur une Mega), la dérive de
  l'`age` d'un `offline` sur 24 heures, et la bascule atomique de la liste sur ESP32.
- Ordres (UC 012) : la tolérance de 10 secondes sur l'heure `t` d'un ordre ; les débits (une connexion par 250 millisecondes, un
  ordre par seconde, un `ack` de refus par 10 secondes) et le temps de traitement d'un ordre (un calcul HMAC, quelques dizaines
  de millisecondes sur une Mega) ; le serveur avec un module ENC28J60, non pris en charge faute de matériel de recette ; la prise
  en charge du port par les ESP après une reconnexion Wi-Fi ; le redémarrage logiciel d'une Mega selon son chargeur d'amorçage
  (délai de 2 secondes du chien de garde). **Exposition** : le port d'ordres ne doit jamais être joignable depuis Internet, et
  le canal d'ordres peut être rendu indisponible (503) par un flot de requêtes sans jamais gêner les badges.

## Vecteurs de référence

Le fichier `.claude/compat/vecteurs-v1.json` du dépôt contient des requêtes et des réponses exactes que le
sketch et le plugin doivent tous deux reproduire : un cas valide par événement, des requêtes signées
(avec chaîne canonique et signature calculées), un rejeu, une version inconnue, un champ inconnu, des
appels invalides, une réponse signée, (UC 011) un `hello` et un `hb` de liste blanche avec leur réponse `wl` signée et (UC 012)
un `hello` annonçant le serveur d'ordres et un `ack` de refus signé. Ces vecteurs
sont **figés** : on en ajoute, on n'en modifie ni n'en
retire jamais.
