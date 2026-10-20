# Référence technique

Cette référence s'adresse aux utilisateurs avertis et aux contributeurs : compatibilité des lecteurs, protocole, fiche d'un lecteur, appairage, configuration du sketch, mode debug, banc de rejeu. Elle ne se lit pas de bout en bout : chaque section se consulte seule.

Vous installez votre premier lecteur ? Suivez plutôt le [tutoriel pas à pas](debuter.md), qui renvoie ici pour chaque détail.

<a id="sommaire-reference"></a>
## Sommaire des pages techniques

| Page | Contenu |
|---|---|
| [Cartes et sketch v1](cartes-et-sketch-v1.md) | Tableau des capacités par carte, câblage, bibliothèques, flash, garde de développement, console série, mise à jour à distance. |
| [Dépannage détaillé](depannage.md) | Chaque message ou symptôme, sa cause et l'action à mener. |
| [Protocole v1 des lecteurs](protocole-v1.md) | Contrat complet du protocole v1 (champs, signature, anti-rejeu, mode hors ligne, ordres). |
| [Configuration du plugin](configuration.md) | Matériel d'origine (v0), équipements, lecteurs, badges et codes. |
| [Fonctionnement et utilisation des équipements](fonctionement.md) | Scénarios, blocage après échecs, codes temporaires. |
| [Infos techniques](techtips.md) | Technologie Wiegand, clavier à code, sources et bibliothèques. |
| [Migration depuis Badger](migration.md) | Reprendre les équipements et les scénarios de l'ancien plugin. |

Sur cette page :

- [Compatibilité : lecteurs d'origine, relais et routes](#compatibilite-v0)
- [Protocole des lecteurs et versions](#protocole-versions)
- [Version, firmware et capacités de chaque lecteur](#fiche-lecteur)
- [Appairage d'un lecteur v1](#appairage)
- [Configuration du sketch d'un lecteur v1](#configuration-sketch)
- [Mode debug](#mode-debug)
- [Niveau de log](#niveau-de-log)
- [Banc de rejeu de compatibilité (contributeurs)](#banc-rejeu)
- [Limites connues](#limites-connues)

<a id="compatibilite-v0"></a>
## Compatibilité : lecteurs d'origine, relais et routes

**Votre lecteur actuel continue de fonctionner, sans rien changer.** Aucune mise à jour du sketch n'est jamais obligatoire.

### Comment savoir si un lecteur est un lecteur d'origine

Ouvrez sa fiche dans **Plugins > Sécurité > Badger Fork** : l'affichage « Protocole : v0 (sketch d'origine) » (sans firmware ni capacités) indique un lecteur d'origine, c'est-à-dire un des sketchs `BadgerW5100`, `BadgerENC28J60` ou `JeedouinoLAN`, ou ceux de l'ancien plugin Badger. Il n'annonce rien : c'est normal.

### Ce qui reste identique pour un lecteur d'origine (v0)

- Les commandes créées et leurs noms (`BadgerID`, `Presentation`, `TagTryLimit`, `PinTryLimit`) et les noms des badges (`BADGE <valeur>`).
- Le comptage des badges inconnus et des codes faux, le blocage du lecteur, les scénarios existants.
- Les deux adresses d'appel : l'ancienne `/plugins/badger/…` et la courante `/plugins/badger2/…`.
- Un appel **sans indication de version** est toujours un appel v0, quelle que soit l'adresse.

### Le relais de compatibilité

Les sketchs de l'ancien plugin Badger appellent l'adresse `/plugins/badger/…`, **figée dans leur firmware**. Le **relais** est un petit fichier que le plugin pose à cette adresse pour la faire répondre : il redirige l'appel vers le plugin actuel, qui le traite en v0. Il se pose et se retire dans **Plugins > Gestion des plugins > Badger Fork**, section **Migration depuis Badger** (voir la [procédure de migration](migration.md)). Les sketchs du dépôt appellent déjà `/plugins/badger2/…` et n'ont pas besoin de relais.

### Les deux versions côte à côte

| | v0 (sketchs d'origine) | v1 (sketch `Badger2`) |
|---|---|---|
| Cartes | Uno et autres cartes AVR, déjà installées | Mega 2560 ou ESP seulement |
| Appel | Adresse web (`GET`) | Requête `POST` dont le corps n'apparaît pas dans le journal du serveur web |
| Authentification | Aucune | Signature par secret partagé (facultative, par appairage) |
| Réponse lue par le lecteur | Non | Oui |
| Annonce version, firmware, capacités | Non | Oui (fiche du lecteur) |
| Maintenance | Gelé, jamais modifié, maintenu à vie | Évolue |

Le protocole v0 n'authentifie pas le lecteur : le plugin n'accepte que les appels venant d'une adresse du réseau local et refuse ceux qui passent par un proxy ou un tunnel. Isoler les lecteurs sur un réseau dédié reste conseillé. L'état de sécurité global de la v0 est traité par la documentation de la tranche sécurité.

<a id="protocole-versions"></a>
## Protocole des lecteurs et versions

Le plugin reconnaît la version du protocole de chaque appel d'un lecteur. Les lecteurs actuels (sketchs d'origine, qu'ils appellent l'ancienne adresse `/plugins/badger/…` ou la nouvelle `/plugins/badger2/…`) continuent de fonctionner exactement comme avant.

Les versions prises en charge sont visibles dans **Analyse > Santé**, ligne « Versions de protocole supportées » (aujourd'hui : « v0 : supportée ; v1 : supportée »).

Un appel qui annonce une version inconnue est refusé, et l'avertissement « version de protocole non supportée : mettre à jour le plugin » apparaît dans le log du plugin (voir [Dépannage](depannage.md#version-non-supportee)).

Le contrat complet de la v1 est publié dans la page [Protocole v1 des lecteurs](protocole-v1.md).

<a id="fiche-lecteur"></a>
## Version, firmware et capacités de chaque lecteur

La fiche de chaque lecteur affiche, en lecture seule, ce que le lecteur a annoncé de lui-même : **Protocole**, **Firmware**, **Carte**, **Transport**, **Capacités** et **Dernier hello**. Vous ne pouvez rien modifier à cet endroit. Aucun secret (clé, mot de passe, code) n'y est affiché.

| Affichage | Signification | Action |
|---|---|---|
| « Protocole : v0 (sketch d'origine) » seul | Le lecteur utilise le sketch d'origine, qui n'annonce rien. C'est normal : il fonctionne comme avant. | Aucune. |
| « En attente de l'annonce du lecteur » | Le lecteur a été créé par l'inclusion à son premier appel v1, qui ne sert qu'à le créer. Il est inactif et ne s'est pas encore annoncé. Même cas pour un lecteur désactivé au moment de son démarrage. | Activez le lecteur, puis redémarrez-le pour qu'il s'annonce. |
| Protocole, firmware, carte, transport, capacités et date renseignés | Le lecteur v1 s'est annoncé. | Aucune. |

Les valeurs se mettent à jour à chaque annonce (« hello »), envoyée au démarrage du lecteur. La date **Dernier hello** indique l'ancienneté de ce que vous voyez :

- Un lecteur reflashé avec le sketch d'origine garde l'affichage de sa dernière annonce v1 ; seule la date de « Dernier hello » trahit qu'elle est ancienne.
- Un lecteur créé en v0 puis reflashé en v1 reste affiché en v0 jusqu'à sa première annonce acceptée.

Les capacités s'affichent sous la forme « libellé (nom technique) », par exemple « Battement de cœur (hb) ». **Deux utilisateurs n'ont pas la même liste, et c'est normal** : elle dépend de la carte et des fonctions activées à la compilation. Une capacité que le plugin ne connaît pas apparaît sous son seul nom brut : ce n'est pas une erreur, le plugin est simplement plus ancien que le sketch du lecteur.

Une fonction de la fiche qui exige une capacité que le lecteur n'annonce pas est grisée, avec la raison affichée. Aucune fonction n'est concernée pour l'instant : ce mécanisme servira aux fonctions à venir.

<a id="appairage"></a>
## Appairage d'un lecteur v1

L'appairage lie un lecteur v1 (sketch Badger2) à un **secret** partagé avec Jeedom. Une fois appairé, seuls les appels signés avec ce secret sont acceptés au nom de ce lecteur : personne d'autre sur le réseau ne peut se faire passer pour lui.

L'appairage est **facultatif**. Un lecteur jamais appairé, dont tous les lecteurs déjà installés, fonctionne exactement comme avant. Un lecteur v0 (sketch d'origine, par exemple un Uno avec W5100) ne peut pas être appairé : le bouton n'apparaît pas et le message « Appairage réservé aux lecteurs v1 (sketch Badger2) » s'affiche à la place.

### Où le trouver

Dans la fiche du lecteur, le bloc **Version minimale** indique :

- « aucune (lecteur non appairé) » : tous les appels sont acceptés comme avant ;
- « v1 (lecteur appairé : appels v0 et non signés refusés) », suivi de « depuis le » et de la date d'appairage.

Trois boutons sont réservés aux administrateurs, un seul ou deux sont visibles selon l'état :

| Bouton | Visible quand | Effet |
|---|---|---|
| **Appairer le lecteur** | Lecteur v1 non appairé | Génère le secret et active la protection. |
| **Régénérer le secret** | Lecteur appairé | Génère un nouveau secret ; l'ancien cesse de valoir. |
| **Rabaisser à v0** | Lecteur appairé | Supprime l'appairage et le secret. |

Chaque bouton demande une confirmation avant d'agir.

<a id="appairage-appairer"></a>
### Appairer un lecteur

1. Cliquez sur **Appairer le lecteur** et confirmez.
2. Le message « Lecteur appairé : téléchargez maintenant la configuration du sketch, qui contient son secret » s'affiche.
3. Téléchargez la configuration du sketch (voir [Configuration du sketch d'un lecteur v1](#configuration-sketch)) et reportez-la sur le lecteur.

Le secret n'est **jamais affiché à l'écran** : il n'est fourni que dans le fichier de configuration du sketch, que vous pouvez retélécharger à tout moment sans changer le secret. Tant que le lecteur n'est pas reconfiguré avec ce secret, ses appels sont refusés. Le secret peut aussi être saisi à la [console série](cartes-et-sketch-v1.md#console-serie) du lecteur (commande `secret`).

Le secret est conservé chiffré par Jeedom. Il n'apparaît ni dans le log, ni dans l'export de l'équipement.

⚠️ Si votre Jeedom est en HTTP (sans HTTPS), le secret transite en clair sur le réseau au moment du téléchargement du fichier. Préférez HTTPS.

<a id="ce-qui-est-refuse"></a>
### Ce qui est refusé après l'appairage

Tout appel fait au nom d'un lecteur appairé est refusé, et un avertissement est écrit dans le log du plugin, dans ces cas :

- l'appel n'est pas signé, ou la signature est fausse ;
- l'appel est rejoué (un appel déjà reçu est renvoyé) ;
- l'appel arrive en v0 (c'est la **version minimale** du lecteur : voir [rétrogradation refusée](depannage.md#retrogradation-refusee)).

Un événement badge ou code qui arrive avec **plus de 30 secondes de retard** est accepté mais **sans effet** (aucune ouverture, aucune action) ; l'événement est journalisé. Cela protège d'un appel retenu puis renvoyé plus tard.

Le filtre d'adresse IP s'applique toujours à un lecteur appairé : si l'adresse du lecteur change (nouveau bail DHCP, par exemple) hors mode inclusion, ses appels sont refusés. Réservez une adresse fixe à chaque lecteur.

<a id="regenerer-secret"></a>
### Régénérer le secret

1. Cliquez sur **Régénérer le secret** et confirmez.
2. Le message « Secret régénéré : téléchargez la nouvelle configuration du sketch et reflashez le lecteur » s'affiche. Téléchargez la nouvelle configuration, puis reflashez le lecteur avec elle.

L'ancien secret est refusé immédiatement : le lecteur reste refusé jusqu'à sa reconfiguration. Le nouveau secret n'est pas affiché à l'écran, seulement fourni dans le fichier.

Régénérez aussi le secret :

- après la restauration d'une sauvegarde de Jeedom ;
- quand la fiche affiche « Secret absent ou illisible : tous les appels de ce lecteur sont refusés. Régénérez le secret. »

<a id="rabaisser-v0"></a>
### Rabaisser à v0

**Rabaisser à v0** supprime l'appairage et le secret. Les appels v0 ou non signés au nom du lecteur sont de nouveau acceptés. Le lecteur redevient « jamais appairé ».

⚠️ Tout appareil du réseau peut alors se faire passer pour ce lecteur. Réservez cette action à un lecteur reflashé avec un ancien sketch.

<a id="configuration-sketch"></a>
## Configuration du sketch d'un lecteur v1

Au lieu de renseigner à la main l'adresse de Jeedom, l'identifiant et le secret dans le sketch, téléchargez un fichier de configuration pré-rempli depuis la fiche du lecteur. Cette fonction est **réservée aux administrateurs**.

> **À confirmer : le sketch v1 n'a jamais été essayé sur matériel réel.**

### Où le trouver

Dans la fiche du lecteur, le bloc **Configuration du sketch** se trouve sous les boutons d'appairage.

- Lecteur **appairé** : le bouton **Télécharger la configuration du sketch** est proposé, avec l'avertissement « Ce fichier contient le secret du lecteur : ne le partagez pas ».
- Lecteur v1 **non appairé** : un message demande d'appairer d'abord le lecteur, car le fichier doit contenir son secret.
- Lecteur **jamais annoncé en v1** (lecteur d'origine, ou lecteur pas encore flashé) : le bouton **Configurer un lecteur v1 (reflash)** est proposé. Voir plus bas.

### Renseigner le formulaire

| Champ | Ce qu'il attend |
|---|---|
| **Carte** | La carte du lecteur, à choisir dans la liste (obligatoire). |
| **Adresse de Jeedom** et **Port** | Adresse IP de Jeedom sur le réseau local et son port HTTP. |
| **Réseau Wi-Fi (SSID)** | Cartes Wi-Fi seulement : nom du réseau (1 à 32 caractères ASCII). |
| **Mot de passe Wi-Fi** | Cartes Wi-Fi seulement : vide, 8 à 63 caractères ou 64 chiffres hexadécimaux. Utilisé seulement pour ce fichier, jamais conservé par Jeedom. |

Cartes proposées (6) :

- Arduino Mega 2560 avec Ethernet W5100, W5200 ou W5500 ;
- Arduino Mega 2560 avec Ethernet ENC28J60 (l'adresse de Jeedom doit alors être une adresse IP) ;
- ESP8266 (Wemos D1 mini, NodeMCU) en Wi-Fi ;
- ESP32 en Wi-Fi ;
- WT32-ETH01 (ESP32 avec Ethernet LAN8720) ;
- Olimex ESP32-POE (ESP32 avec Ethernet LAN8720).

⚠️ Arduino **Uno, Nano ou Pro Mini ne sont pas pris en charge en v1** : gardez le sketch d'origine (v0) sur ces cartes (voir le [tableau des capacités par carte](cartes-et-sketch-v1.md#tableau-capacites)).

L'adresse et le port sont proposés d'après l'adresse **interne** de Jeedom (Réglages > Système > Configuration > Réseaux). Si elle est vide, ou si c'est un nom d'hôte, ou si Jeedom est configuré en HTTPS en interne, le champ est laissé vide avec un avertissement : saisissez l'adresse IP de Jeedom sur le réseau local. Le lecteur parle en **HTTP** : indiquez le port HTTP de Jeedom. Aucun fichier n'est produit avec une adresse vide.

### Placer le fichier et flasher

1. Cliquez sur **Télécharger la configuration du sketch** : le navigateur enregistre un fichier `config.h`.
2. Placez-le dans le dossier `arduino/Badger2/` du sketch, **à la place** du `config.h` existant.
3. Compilez et flashez le lecteur (voir [Récupérer le sketch et le flasher](cartes-et-sketch-v1.md#flasher)). Il s'annonce à Jeedom et sa fiche affiche ses capacités.
4. **Supprimez le fichier téléchargé** une fois le lecteur flashé.

Le fichier contient le secret du lecteur : ne le partagez pas, ne le publiez pas, ne le versionnez pas.

**La garde de développement.** Le fichier d'un lecteur **appairé** (avec son secret) lève la garde de développement du sketch ; celui d'un lecteur **sans secret** la laisse à `0`, et le sketch refuse alors de compiler avec un message périmé. Voir [La garde de développement](cartes-et-sketch-v1.md#garde-developpement) et le [dépannage](depannage.md#compilation-refusee-garde).

<a id="rid-lecteur"></a>
### L'identifiant du lecteur

- Le lecteur doit avoir un identifiant composé de lettres, chiffres, tirets et soulignés (32 caractères au plus). Il apparaît comme identifiant de l'équipement dans Jeedom.
- **Le plugin ne vérifie pas que deux lecteurs physiques portent des identifiants différents** : c'est à vous de veiller à l'unicité. Deux lecteurs de même identifiant se partageraient le même équipement. Le plugin refuse seulement d'appairer un lecteur (et les appels à son nom) quand **deux équipements Badger Fork** de Jeedom portent le même identifiant, à la casse près.
- Pour qu'un lecteur reflashé **reprenne l'équipement existant**, son identifiant doit être **exactement l'ancien nom du lecteur** dans Jeedom (par exemple `BADGER1`) : réglez-le avant de reflasher, dans la configuration ou à la console série. Sans identifiant, il se déduit du dernier octet de l'adresse MAC ; un lecteur `JeedouinoLAN` d'origine, nommé d'après son adresse IP, demande de fixer l'identifiant à la main.

### Lecteur d'origine ou jamais annoncé en v1

Pour un lecteur qui n'a jamais annoncé le protocole v1, **Configurer un lecteur v1 (reflash)** demande une confirmation, puis télécharge un fichier **sans secret**. Le lecteur actuel n'est pas modifié et continue de fonctionner tant qu'il n'est pas reflashé.

Une fois le nouveau lecteur flashé et annoncé :

- appairez-le, puis téléchargez de nouveau sa configuration ;
- ou saisissez le secret à la console série du lecteur (commande `secret`).

⚠️ Pour une carte Mega, l'adresse MAC du fichier est reprise du lecteur d'origine de même numéro (identifiant `BADGER<n>`). **Ne branchez pas l'ancien et le nouveau lecteur en même temps** : ils auraient la même adresse MAC.

### À savoir

- Une valeur saisie à la console série du lecteur (identifiant, adresse, secret) **prime** sur celle du fichier ; la commande `config` l'indique et `<champ> -` l'efface.
- **Réservation DHCP** : le plugin mémorise l'adresse du lecteur et refuse ensuite ses appels si elle change hors mode inclusion. Réservez une adresse fixe au lecteur dans votre box.
- Un lecteur v1 **créé en inclusion est inactif**, et l'appel qui le crée reste **sans effet** (ni badge, ni annonce) : activez-le, puis redémarrez-le.
- En v1, un badge enrôlé en décimal (sketch `JeedouinoLAN`) ou lu en 24 ou 32 bits **n'est pas reconnu** : seules les trames de 26 et 34 bits le sont.
- Chaque téléchargement est inscrit au log du plugin (qui, quel lecteur), sans le secret.
- Un non-administrateur n'obtient pas le fichier.

<a id="mode-debug"></a>
## Mode debug

Le log du plugin n'écrit plus les badges ni les codes reçus : une présentation inconnue ou un code faux y apparaît sans sa valeur. Pour voir ces valeurs, utilisez le mode debug.

Le mode debug sert à mettre au point un lecteur ou un clavier : il montre, appel par appel, ce que le lecteur envoie au plugin et ce que le plugin en a fait.

> **Attention : en mode debug, les badges et les codes présentés sont affichés en clair.** Un bandeau rouge reste visible en haut de la page du plugin tant que le mode est actif. N'activez-le que le temps de la mise au point.

### Activer

1. Connectez-vous avec un compte **administrateur** et ouvrez la page du plugin.
2. Descendez à la section **Mode debug**, en bas de la page.
3. Choisissez le **lecteur** observé (un lecteur précis, ou « Tous les lecteurs »).
4. Choisissez la **durée** : 15 minutes, 30 minutes ou 1 heure (maximum).
5. Cochez si besoin **Observation seule (ne rien traiter)**, puis cliquez sur **Activer**.

> **Observation seule : la porte ne s'ouvre plus pour ce lecteur pendant la durée choisie.** Les appels sont montrés mais ne sont pas traités : aucune action, aucun badge ni code pris en compte. Cette option n'existe que pour un lecteur précis, pas pour « Tous les lecteurs ». Cliquez sur **Arrêter** pour revenir tout de suite au fonctionnement normal.

Les boutons **Arrêter** (coupe le mode debug) et **Effacer** (vide la liste des appels) sont dans la même section. La liste se met à jour toutes les 2 secondes.

### Ce qui est montré

Pour chaque appel reçu : l'heure, la route utilisée (ancienne ou courante), la version de protocole reconnue, le lecteur, l'adresse d'origine, l'adresse IP déclarée par le lecteur, le nom des en-têtes reçus, les paramètres envoyés (dont le badge ou le code tapé, en clair) et le résultat obtenu (badge ou code reconnu, code faux, lecteur bloqué, etc.).

- Les 200 derniers appels sont conservés.
- Les appels refusés parce que leur origine n'est pas autorisée sont regroupés : la section affiche leur nombre depuis l'activation et quelques exemples récents, sans les lister tous.
- Le contenu reçu est affiché comme du texte brut, jamais interprété.

### Ce qui n'est jamais montré

- Les codes et les badges **enregistrés** dans le plugin : seule la valeur présentée par le lecteur apparaît, jamais la liste de ce qui est enregistré.
- Les secrets : la clé `apikey` et la signature `sig` sont remplacées par « masqué » et leur nombre de caractères.
- Le contenu du mode debug n'est écrit ni dans le log, ni dans les sauvegardes de Jeedom.

### Arrêt automatique

Le mode debug s'arrête seul, et efface alors tout ce qu'il avait enregistré, dans chacun de ces cas :

- à l'échéance de la durée choisie ;
- quand vous cliquez sur **Arrêter** ;
- quand vous désactivez le plugin ou qu'il est mis à jour ;
- au redémarrage de Jeedom (il n'est jamais rétabli après un redémarrage).

Chaque activation et chaque arrêt sont notés dans le log du plugin (qui, jusqu'à quand, quel lecteur), sans aucune valeur de badge ou de code.

<a id="niveau-de-log"></a>
## Niveau de log

Le niveau de log du plugin est **Erreur** par défaut : les avertissements (refus d'un appel, signature invalide, rejeu…) et les informations (badge présenté) n'y sont **pas écrits**. Pour les voir, ouvrez **Plugins > Gestion des plugins > Badger Fork**, réglez le niveau de log sur **Avertissement** (ou **Info**), puis consultez **Analyse > Logs**, log `badger2`. Remettez le niveau par défaut ensuite. Le [dépannage](depannage.md) cite les messages tels qu'ils apparaissent dans ce log.

<a id="banc-rejeu"></a>
## Banc de rejeu de compatibilité (contributeurs)

Avant chaque publication du plugin, un banc **rejoue sur une vraie installation Jeedom** les appels de référence des lecteurs (v0 par l'ancienne route et par la route courante, v1 : valide, version inconnue, champ inconnu…) et vérifie que leurs effets n'ont pas changé. Il atteste ainsi qu'aucun lecteur en service ne casse.

- Il agit **sans toucher au réel** : seulement sur cinq équipements de test dont le nom commence par `BANC019-`, qu'aucun scénario ne doit utiliser. Il n'active jamais l'inclusion et n'utilise jamais le nom ni la valeur d'un lecteur ou d'un badge réel.
- **Prérequis** : le relais de compatibilité posé, l'inclusion désactivée, et le **niveau de log du plugin au moins Avertissement pendant l'exécution** (le banc refuse de démarrer sinon, sans modifier le niveau).
- **En fin d'exécution, les cinq équipements `BANC019-*` restent désactivés** sur la box ; vous pouvez les supprimer depuis la page du plugin.
- Il se lance depuis un poste du réseau local, avec la clé d'API d'un administrateur fournie dans une variable d'environnement : `python3 -B tests/harnais/rejeu_box.py --url http://<adresse de la box>`. Le rapport (une ligne par vecteur) ne contient aucun secret ; seul le secret de test public du dépôt est utilisé pour le vecteur signé. Code de sortie 0 : tout est conforme.
- Pendant le banc, présentez un badge réel : la porte doit s'ouvrir normalement.

<a id="limites-connues"></a>
## Limites connues

- **Le sketch v1 n'a jamais été recetté sur matériel réel** ; aucune carte v1 n'a été essayée. Les étapes propres à la v1 portent la mention « À confirmer ».
- **Le plugin n'envoie aucun ordre d'ouverture au lecteur v1** : la porte s'ouvre par un scénario Jeedom qui agit sur un autre équipement. Les ordres envoyés au lecteur (ouverture à distance, liste blanche hors ligne) ne sont pas encore livrés.
- **Le plugin ne vérifie pas l'unicité de l'identifiant des lecteurs physiques** (voir [L'identifiant du lecteur](#rid-lecteur)).
- **Un lecteur v1 créé en inclusion est inactif** et son premier appel reste sans effet : le premier badge d'un lecteur neuf n'est pas traité.
- **En v1, seules les trames de 26 et 34 bits sont reconnues** : un badge enrôlé en décimal ou lu en 24 ou 32 bits n'est pas reconnu.
- **Le secret n'est plus affiché** après l'appairage : il ne sort que dans le fichier de configuration téléchargé.
- **Le trafic reste en HTTP** : la signature protège l'authenticité et le rejeu, pas la confidentialité. Isolez les lecteurs sur un réseau dédié.
- **Mise à jour à distance** : `ota -` ne coupe l'écoute qu'au redémarrage suivant (voir [Mise à jour à distance](cartes-et-sketch-v1.md#mise-a-jour-distance)).
- **Pas de nouvelle tentative automatique côté plugin** : c'est le lecteur qui réémet un événement non acquitté ; le plugin n'a aucun service tiers à interroger.
- **Pas de démon ni de dépendance** : le plugin est entièrement en PHP.
- **Chiffrement facultatif des badges et des codes** : non réalisé.

---

[Protocole v1 des lecteurs : référence](protocole-v1.md) · [Infos techniques](techtips.md) · [Retour au tutoriel](debuter.md)
