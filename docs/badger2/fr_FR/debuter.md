# Débuter pas à pas

Ce tutoriel vous mène du matériel acheté à votre première porte ouverte avec un badge. Il suppose que vous n'avez **jamais** programmé une carte Arduino ni branché un lecteur de badges. Suivez les huit étapes dans l'ordre : chacune se termine par un **Résultat attendu** que vous pouvez constater sans outil de développement. Si le résultat n'y est pas, n'allez pas plus loin : la ligne correspondante de l'[étape 7](#etape-7) dit quoi faire.

Pour le détail technique d'un point, les liens vous envoient vers la [référence technique](reference.md). Vous n'avez pas besoin de les lire pour réussir.

> **À confirmer** : la nouvelle génération de lecteurs décrite ici (« v1 ») n'a **jamais été essayée sur une carte réelle**. Les étapes 2 à 6 portent la mention « À confirmer » : elles sont écrites d'après les spécifications et le code, pas d'après une observation sur du matériel. Si une étape se passe autrement chez vous, notez-le : c'est une information précieuse.

## Les mots à connaître

- **Plugin** : le module installé dans Jeedom (Badger Fork).
- **Lecteur** : l'ensemble formé par le lecteur de badges et la petite carte électronique qui le relie à votre réseau.
- **Carte** : la petite carte électronique (Arduino, ESP) qui relie le lecteur de badges au réseau.
- **Sketch** : le petit programme que l'on copie dans la carte.
- **Flasher** : copier un sketch dans la carte.
- **IDE Arduino** : le logiciel gratuit qui permet de flasher.
- **Console série** : une fenêtre de texte où la carte écrit ce qu'elle fait.

<a id="etape-1"></a>
## Étape 1 — Ce qu'il faut acheter

Il vous faut :

- **Une carte** :
  - **conseillée** : une **Arduino Mega 2560** avec un **shield Ethernet** (la carte d'extension qui ajoute la prise réseau) ;
  - ou un **ESP32** ou un **ESP8266** (par exemple un Wemos D1 mini), qui se connectent en Wi-Fi.
  - Préférez une carte costaud : elle laisse de la marge pour les fonctions que vous activerez plus tard. Le choix complet (dont les versions Ethernet des ESP) est détaillé dans le [tableau des capacités par carte](cartes-et-sketch-v1.md#tableau-capacites).
- **Un lecteur de badges Wiegand** (le Wiegand est la façon dont ces lecteurs envoient les badges : deux fils de données, appelés D0 et D1). Prenez un lecteur qui sait envoyer en **26 ou 34 bits** (c'est écrit sur sa fiche) et des badges adaptés à sa fréquence (125 kHz ou 13,56 MHz). Un clavier à code est facultatif.
- **Une alimentation 12 V** pour le lecteur (au moins 9 V, 12 V s'il a un clavier).
- **Des fils** de liaison (type « Dupont ») et **un câble USB qui transporte les données** (certains câbles ne servent qu'à charger) pour relier la carte à votre ordinateur. Pour la Mega, un câble réseau.
- Facultatif : une **gâche** ou un **relais** pour la porte. Pour l'instant, c'est un **scénario Jeedom** qui ouvre la porte (étape 6) : la gâche se commande donc par un autre équipement Jeedom, pas par la carte.

> **Et l'Arduino Uno R3 ?** Elle continue de fonctionner avec les anciens programmes (version « v0 »), mais nous vous la **déconseillons pour une nouvelle installation** : le programme de la nouvelle génération est trop gros pour sa mémoire. Voir [pourquoi](cartes-et-sketch-v1.md#choix-carte).

**Résultat attendu** : vous avez sur la table la carte, le lecteur, son alimentation, les fils et le câble USB, et vous savez que votre lecteur envoie en 26 ou 34 bits.

<a id="etape-2"></a>
## Étape 2 — Câbler

> **À confirmer** (v1 non essayée sur matériel).

**Débranchez tout** avant de câbler. Le lecteur a quatre fils utiles : le **12 V** (alimentation), la **masse** (le fil de retour, noté GND), et **D0** et **D1** (les deux fils de données, en général vert et blanc).

| Fil du lecteur | Où le brancher |
|---|---|
| D0 (vert) | Broche de données 0 de la carte (voir le tableau de votre carte) |
| D1 (blanc) | Broche de données 1 de la carte |
| Masse (GND) | La masse de la carte **et** celle de l'alimentation |
| 12 V | L'alimentation 12 V (jamais la carte) |

**Où brancher D0 et D1 selon votre carte :**

| Carte | D0 (vert) | D1 (blanc) |
|---|---|---|
| Mega 2560 + shield Ethernet | broche 2 | broche 3 |
| ESP32 | GPIO 26 | GPIO 27 |
| ESP8266 (Wemos D1 mini) | GPIO 4 (marquée D2) | GPIO 5 (marquée D1) |

> Capture à fournir : `images/cablage-mega.png` — doit montrer une Mega 2560 avec son shield Ethernet, les fils D0 et D1 du lecteur sur les broches 2 et 3 et la masse commune.

> Capture à fournir : `images/cablage-esp32.png` — doit montrer un ESP32 avec D0 sur GPIO 26, D1 sur GPIO 27 et la masse commune.

> Capture à fournir : `images/cablage-esp8266.png` — doit montrer un Wemos D1 mini avec D0 sur GPIO 4, D1 sur GPIO 5 et la masse commune.

**Les erreurs qui coûtent cher :**

- **Masse commune obligatoire.** Reliez ensemble la masse du lecteur, celle de la carte et celle de l'alimentation. Sans cela, le lecteur lit n'importe quoi ou rien.
- **Ne mélangez jamais le 12 V avec la carte.** Un fil 12 V relié à une broche de la carte la détruit. Les cartes ESP supportent **3,3 V au maximum** sur leurs broches.
- **D0 et D1 inversés** : la carte reçoit des badges faux, vous le verrez à l'étape 6.
- N'alimentez pas le lecteur par la broche « VIN » de la carte quand elle est aussi branchée en USB : vous risquez de la griller. Branchez-le directement sur l'alimentation 12 V.

Pour tous les cas particuliers (autres cartes, second lecteur, autres broches), voir le [câblage détaillé](cartes-et-sketch-v1.md#cablage).

**Résultat attendu** : une fois l'alimentation 12 V branchée, le lecteur s'allume (voyant allumé ou petit bip) et la carte, reliée par USB à l'ordinateur, a son voyant d'alimentation allumé. Rien ne chauffe et aucune odeur de brûlé.

<a id="etape-3"></a>
## Étape 3 — Flasher le sketch

> **À confirmer** (v1 non essayée sur matériel).

1. **Installez l'IDE Arduino** : téléchargez-le (version 2) sur le site officiel d'Arduino, puis installez-le comme n'importe quel logiciel.
2. **Ajoutez ce qu'il faut à l'IDE**, selon votre carte : pour la Mega, la « bibliothèque » Ethernet (un morceau de programme prêt à l'emploi) ; pour un ESP, le « paquet de cartes » correspondant. Les adresses et les versions exactes sont dans [Préparer l'IDE Arduino](cartes-et-sketch-v1.md#bibliotheques).
3. **Récupérez le sketch** : le dossier `arduino/Badger2` du dépôt du plugin sur GitHub (bouton « Code », puis « Download ZIP »), ou le même dossier dans celui du plugin sur votre Jeedom. Ouvrez le fichier `Badger2.ino` : l'IDE charge tout le dossier.
4. **Réglez le fichier `config.h`** (le fichier de réglages du sketch, dans ce dossier). Ouvrez-le dans l'IDE et modifiez seulement ces lignes :

| Ligne à repérer | Ce qu'il faut écrire |
|---|---|
| `BADGER2_PROFIL` | Rien pour la Mega avec shield Ethernet. ESP32 : `BADGER2_PROFIL_ESP32_WIFI`. ESP8266 : `BADGER2_PROFIL_ESP8266_WIFI`. |
| `BADGER2_DEVELOPPEMENT_ACCEPTE` | `1` (cette ligne est une sécurité : vous confirmez que vous savez que la v1 n'a pas été essayée sur matériel réel). |
| `BADGER2_JEEDOM_HOTE` | L'adresse de votre Jeedom sur le réseau, par exemple `192.168.1.10`. Vous la trouverez dans Jeedom, Réglages > Système > Configuration > Réseaux. |
| `BADGER2_JEEDOM_PORT` | `80`, sauf si votre Jeedom répond sur un autre port « HTTP ». |
| `BADGER2_WIFI_SSID` et `BADGER2_WIFI_MOT_DE_PASSE` | ESP seulement : le nom de votre réseau Wi-Fi et son mot de passe, entre guillemets. |

   Ne partagez jamais ce fichier une fois rempli : il contient votre mot de passe Wi-Fi.

> Capture à fournir : `images/tuto-config-h.png` — doit montrer le fichier `config.h` ouvert dans l'IDE avec les lignes ci-dessus modifiées (valeurs d'exemple, mot de passe factice).

5. **Choisissez la carte et le port** : menu Outils > Type de carte (Mega : « Arduino Mega or Mega 2560 » ; ESP32 : « ESP32 Dev Module » ; ESP8266 : « LOLIN(WEMOS) D1 R2 & mini »), puis Outils > Port (le port qui apparaît quand vous branchez la carte).

> Capture à fournir : `images/tuto-arduino-ide-carte.png` — doit montrer le menu Outils de l'IDE avec le type de carte et le port choisis.

6. **Cliquez sur la flèche « Téléverser »** (en haut à gauche). Attendez la fin.

**Résultat attendu** : l'IDE affiche un message de fin de téléversement, sans texte en rouge. Si la compilation s'arrête sur un message d'erreur, voir [le sketch refuse de compiler](depannage.md#compilation-refusee-garde) (message sur « le plugin ne sert pas encore le protocole v1 ») ou [profil ou carte](depannage.md#compilation-refusee-profil).

<a id="etape-4"></a>
## Étape 4 — Configurer le lecteur

> **À confirmer** (v1 non essayée sur matériel).

Vous allez écouter ce que dit la carte avec la **console série**.

1. Dans l'IDE, ouvrez **Outils > Moniteur série**.
2. Réglez la vitesse sur **115200 bauds** (la vitesse de lecture) et la fin de ligne sur **« NL et CR »** (en bas de la fenêtre).
3. Appuyez sur le petit bouton **reset** de la carte, ou rebranchez-la.
4. Tapez `config` dans la zone de saisie et validez avec Entrée.

> Capture à fournir : `images/tuto-moniteur-serie.png` — doit montrer le moniteur série réglé sur 115200 bauds, avec les lignes de démarrage de la carte et le résultat de la commande `config`.

**Si l'adresse de Jeedom affichée est fausse**, corrigez-la sans reflasher : tapez par exemple `hote 192.168.1.10` (avec la bonne adresse), validez, puis appuyez sur reset. Vous pouvez aussi donner un nom au lecteur : `rid PORTE-ENTREE` (lettres, chiffres, tirets, 32 caractères au plus), puis reset. Ces commandes ne sont prises en compte qu'au **redémarrage** de la carte.

**Le secret du lecteur** (un long mot de passe partagé entre la carte et Jeedom, qui empêche un autre appareil de se faire passer pour le lecteur) est fabriqué par Jeedom à l'étape 5. Jeedom ne l'affiche **jamais à l'écran** : il n'apparaît que dans un fichier que vous téléchargerez. Il est facultatif mais conseillé. Pour tout savoir sur la console : [console série](cartes-et-sketch-v1.md#console-serie).

**Résultat attendu** : au démarrage, la console écrit une ligne commençant par « Réseau : adresse » suivie d'une adresse de votre réseau (par exemple 192.168.1.50), et la commande `config` affiche l'adresse de Jeedom que vous attendez.

<a id="etape-5"></a>
## Étape 5 — Installer le plugin et inclure le lecteur dans Jeedom

> **À confirmer** (v1 non essayée sur matériel).

### 5.1 Installer le plugin

1. Dans Jeedom, allez dans **Plugins > Gestion des plugins**.
2. Cliquez sur **Market**, recherchez **Badger Fork**, ouvrez sa fiche et cliquez sur **Installer**.
3. Ouvrez la page de configuration du plugin et **activez-le**. Il n'y a rien d'autre à installer.

### 5.2 Faire apparaître le lecteur (l'« inclusion »)

L'**inclusion** est un mode temporaire où Jeedom accepte de créer un nouvel équipement quand un appareil inconnu se présente.

1. Ouvrez **Plugins > Sécurité > Badger Fork**.
2. Cliquez sur **Mode inclusion** (la case devient « Arrêter inclusion »).
3. Appuyez sur le bouton **reset** de la carte.
4. Rechargez la page : le lecteur apparaît dans la liste **Lecteurs**, sous son nom (par exemple `BADGER1`).

> Capture à fournir : `images/tuto-inclusion.png` — doit montrer la page du plugin avec les boutons « Mode inclusion » / « Arrêter inclusion » et un lecteur dans la liste Lecteurs.

### 5.3 Activer le lecteur

Un lecteur créé de cette façon est **inactif** au début. Ouvrez-le, cochez **Activer**, choisissez le **Model** (« Lecteur RFID » ou « Lecteur RFID + PinPad »), cliquez sur **Sauvegarder la configuration**, puis appuyez de nouveau sur **reset** sur la carte pour qu'elle se présente.

### 5.4 Réserver l'adresse du lecteur dans votre box

Votre box (ou routeur) distribue les adresses du réseau avec un système appelé **DHCP**, et peut en changer. Or Jeedom retient l'adresse du lecteur et **refuse ses appels s'il en change** : le lecteur devient muet. Pour l'éviter, faites une **réservation DHCP** : dans l'interface de votre box, rubrique « DHCP », « baux » ou « appareils connectés », repérez le lecteur et choisissez « réserver cette adresse » (ou « adresse fixe »). Pourquoi et comment réparer : [le lecteur ne se fait plus entendre](depannage.md#lecteur-muet-adresse).

### 5.5 Protéger le lecteur (conseillé)

1. Sur la fiche du lecteur, cliquez sur **Appairer le lecteur** et confirmez.
2. Dans le bloc **Configuration du sketch**, choisissez votre **carte**, vérifiez l'**adresse de Jeedom** et le **port** (ajoutez le nom et le mot de passe du Wi-Fi pour un ESP) et cliquez sur **Télécharger la configuration du sketch**. Votre navigateur enregistre un fichier `config.h` qui **contient le secret** : ne le partagez pas.
3. Remplacez le `config.h` du dossier du sketch par ce fichier, refaites l'étape 3 (téléverser), puis **supprimez le fichier téléchargé**.

> Capture à fournir : `images/tuto-appairage.png` — doit montrer la fiche d'un lecteur avec les boutons « Appairer le lecteur » et « Télécharger la configuration du sketch » (sans aucun secret visible).

Tout le détail (régénérer, rabaisser, ce qui est refusé ensuite) : [appairage](reference.md#appairage) et [configuration du sketch](reference.md#configuration-sketch).

> Capture à fournir : `images/tuto-fiche-lecteur.png` — doit montrer la fiche du lecteur avec protocole « v1 », firmware, carte, capacités et « Dernier hello » renseignés.

**Résultat attendu** : la fiche du lecteur affiche « Protocole : v1 » avec son firmware, sa carte et sa date de dernier message ; si vous l'avez appairé, le bloc **Version minimale** affiche « v1 (lecteur appairé … ) ». Dans la console série, la commande `test` répond « Test d'envoi : Jeedom a accepté le battement (ok) ». Vous pouvez maintenant arrêter le mode inclusion. Si ce n'est pas le cas : [le lecteur n'apparaît pas dans Jeedom](depannage.md#lecteur-absent) ou [en attente d'annonce](depannage.md#lecteur-attente-hello).

<a id="etape-6"></a>
## Étape 6 — Premier badge, première ouverture

> **À confirmer** (v1 non essayée sur matériel).

1. Dans le plugin, cliquez de nouveau sur **Mode inclusion**.
2. **Présentez votre badge** devant le lecteur. Jeedom crée un équipement du nom `BADGE` suivi d'un numéro. Rechargez la page : il est dans la liste **Badges**.
3. Cliquez sur **Arrêter inclusion**.
4. Ouvrez l'équipement du badge, donnez-lui un nom parlant, choisissez un **objet parent**, cochez **Activer** (c'est ce qui **autorise** le badge) et **Sauvegarder la configuration**.

> Capture à fournir : `images/tuto-badge-cree.png` — doit montrer la liste des Badges avec un équipement « BADGE » suivi d'un numéro, et sa fiche avec la case « Activer » cochée.

5. **Présentez de nouveau le badge.** Sur le Dashboard, la commande **Presentation** de l'équipement affiche la date, l'heure et le nom du lecteur.
6. **Ouvrez la porte avec un scénario** : le plugin ne commande pas la porte lui-même. Créez un scénario (Outils > Scénarios) déclenché par la commande **Presentation** de votre badge, dont l'action commande votre gâche (ou, pour essayer, une lampe). Des exemples avec captures sont dans [Fonctionnement et utilisation des équipements](fonctionement.md).

> Capture à fournir : `images/tuto-scenario.png` — doit montrer un scénario dont le déclencheur est la commande Presentation du badge et dont l'action allume une lampe ou ouvre une porte.

**Résultat attendu** : quand vous présentez le badge, la commande **Presentation** se met à jour et, grâce au scénario, la lampe s'allume ou la porte s'ouvre. La présentation qui a créé le badge (point 2) ne déclenche rien, c'est normal : seules les présentations suivantes d'un badge activé comptent. Si rien ne se passe : [le badge est lu mais la porte reste fermée](depannage.md#badge-porte-fermee).

> **Attention** : un badge présenté à un lecteur v1 n'est reconnu que s'il est lu en 26 ou 34 bits. Un badge ajouté autrement (par exemple avec l'ancien sketch Jeedouino) n'est **pas reconnu**.

<a id="etape-7"></a>
## Étape 7 — « Ça ne marche pas ? »

Repérez votre symptôme, appliquez l'action, puis reprenez l'étape concernée.

| Ce que vous constatez | Cause probable | Quoi faire | Détail |
|---|---|---|---|
| Rien ne s'affiche dans la console série | Mauvaise vitesse ou mauvais port | Réglez 115200 bauds, choisissez le bon port, appuyez sur reset | [Rien à la console](depannage.md#rien-console) |
| L'IDE refuse de compiler | Ligne de sécurité à `0`, carte ou profil qui ne correspondent pas | Mettez `1` à la ligne `BADGER2_DEVELOPPEMENT_ACCEPTE`, vérifiez la carte choisie | [Garde](depannage.md#compilation-refusee-garde), [profil](depannage.md#compilation-refusee-profil) |
| Le lecteur n'apparaît pas dans Jeedom | Inclusion non activée, adresse de Jeedom fausse, câble réseau ou Wi-Fi | Activez le mode inclusion, corrigez l'adresse (`hote …`), contrôlez le réseau, appuyez sur reset | [Lecteur absent](depannage.md#lecteur-absent) |
| Le lecteur est là mais « En attente de l'annonce du lecteur » | Lecteur créé inactif | Cochez Activer, sauvegardez, appuyez sur reset | [En attente d'annonce](depannage.md#lecteur-attente-hello) |
| Le badge est lu mais la porte reste fermée | Badge inconnu ou désactivé, lecteur bloqué, aucun scénario | Activez le badge, créez le scénario, vérifiez le log | [Badge lu, porte fermée](depannage.md#badge-porte-fermee) |
| Le lecteur ne répond plus après un changement d'adresse | Jeedom refuse une adresse qu'il ne connaît pas | Activez l'inclusion le temps d'un appel, puis faites une réservation DHCP | [Muet après changement d'adresse](depannage.md#lecteur-muet-adresse) |
| La console écrit « refusé par le plugin » | Secret différent, adresse ou version refusée | Voir les messages du log du plugin | [Signature](depannage.md#signature-refusee), [version](depannage.md#version-non-supportee) |

Les messages du plugin se lisent dans **Analyse > Logs**, log `badger2`, à condition de régler son niveau sur « Avertissement » ou « Info » : voir [Niveau de log](reference.md#niveau-de-log). La liste complète des cas est dans le [dépannage détaillé](depannage.md).

**Résultat attendu** : vous avez trouvé votre symptôme dans le tableau, appliqué l'action, et retrouvé le résultat attendu de l'étape concernée.

<a id="etape-8"></a>
## Étape 8 — « Vous venez de Badger 1 ? »

Bonne nouvelle : **vos anciens lecteurs continuent de fonctionner sans rien reflasher**. Aucune mise à jour du programme n'est jamais obligatoire.

- **Pour le vérifier**, ouvrez la fiche d'un ancien lecteur : elle affiche « Protocole : v0 (sketch d'origine) » et rien d'autre, ce qui est normal. Pour comprendre pourquoi cela marche (le « relais » qui répond à l'ancienne adresse), voir [Compatibilité](reference.md#compatibilite-v0).
- **Pour reprendre vos équipements, scénarios et vues** de l'ancien plugin, suivez la [procédure de migration](migration.md) : l'ordre des opérations est important.
- Si vous **remplacez** un ancien lecteur par un lecteur v1, réglez son nom (`rid`) à l'**identique de l'ancien nom du lecteur dans Jeedom** avant de flasher : il reprend alors son équipement existant. Voir [L'identifiant du lecteur](reference.md#rid-lecteur). Ne branchez pas l'ancien et le nouveau lecteur en même temps.
- Un **Arduino Uno** reste sur l'ancien programme et continue d'être pris en charge.

**Résultat attendu** : la fiche de votre ancien lecteur affiche « Protocole : v0 (sketch d'origine) », et un badge présenté déclenche vos scénarios comme avant.

---

Pour aller plus loin : la [référence technique](reference.md), le [dépannage détaillé](depannage.md) et le [protocole v1](protocole-v1.md).
