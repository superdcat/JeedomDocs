# Cartes et sketch v1 (référence)

Cette page s'adresse aux utilisateurs avertis et aux contributeurs. Elle décrit les cartes que le sketch v1 (`Badger2`) sait piloter, leur câblage, la préparation de l'IDE Arduino, le flash, la console série et la mise à jour à distance.

Vous débutez ? Suivez plutôt le [tutoriel pas à pas](debuter.md). Retour à la [page d'entrée de la référence](reference.md).

> **À confirmer : le sketch v1 n'a jamais été essayé sur une carte réelle.** La recette sur Mega 2560 et sur ESP n'est pas faite. Tout ce qui suit est tiré du code et des essais de compilation automatiques, pas d'une observation sur matériel. Les broches par défaut des ESP et du second lecteur sont des **valeurs à confirmer** sur votre câblage.

<a id="choix-carte"></a>
## Choisir sa carte

- **Mega 2560 ou ESP** : seules cartes acceptées par le sketch v1. Préférez une carte costaud : elle laisse de la marge pour les fonctions facultatives.
- **Uno, Nano, Pro Mini** (ATmega328P, 32 Ko de mémoire de programme) : **refusées à la compilation** en v1. Le sketch v1 pèse environ 33 Ko pour une Uno de base, 36,8 Ko avec tout activé et 39,4 Ko avec un module ENC28J60, pour 32,25 Ko disponibles.
- **L'Uno reste en protocole v0, maintenu à vie** : sketchs d'origine `BadgerW5100` et `BadgerENC28J60` (gelés, jamais modifiés). Elle est **déconseillée pour une nouvelle installation**. Un lecteur Uno déjà en service continue de fonctionner sans rien changer : voir [Compatibilité](reference.md#compatibilite-v0).

<a id="tableau-capacites"></a>
## Tableau des capacités par carte

Le profil de la carte se choisit dans le fichier de configuration du sketch. La carte sélectionnée dans l'IDE doit correspondre, sinon la compilation s'arrête en le disant.

| Carte (profil) | Réseau | Version testée en compilation | Lecteur D0 / D1 | Second lecteur D0 / D1 | Mise à jour à distance | Liste blanche hors ligne | Serveur d'ordres | Entrées analogiques |
|---|---|---|---|---|---|---|---|---|
| Mega 2560 + Ethernet W5100, W5200, W5500 (`MEGA_W5X00`, défaut) | Ethernet | bibliothèque `Ethernet` 2.0.2 | 2 / 3 | 18 / 19 (à confirmer) | non (refusée) | oui | oui | 5 (`a1` à `a5`) |
| Mega 2560 + Ethernet ENC28J60 (`MEGA_ENC28J60`) | Ethernet | bibliothèque `EthernetENC` 2.0.5 | 2 / 3 | 18 / 19 (à confirmer) | non (refusée) | oui | **non** (refusé avec ce module) | 5 |
| ESP8266 : Wemos D1 mini, NodeMCU (`ESP8266_WIFI`) | Wi-Fi | cœur ESP8266 3.1.2 | GPIO 4 / 5 | GPIO 12 / 13 (à confirmer) | oui | **non** (refusée) | oui | 1 (`a1` sur `A0`) |
| ESP32 en Wi-Fi (`ESP32_WIFI`) | Wi-Fi | cœur ESP32 3.3.12 | GPIO 26 / 27 | GPIO 32 / 33 (à confirmer) | oui | oui | oui | 4 |
| WT32-ETH01 (`WT32_ETH01`) | Ethernet (LAN8720) | cœur ESP32 3.3.12 | GPIO 32 / 33 | à définir dans la configuration | oui | oui | oui | 3 |
| Olimex ESP32-POE (`ESP32_POE`) | Ethernet (LAN8720) | cœur ESP32 3.3.12 | GPIO 4 / 13 (à confirmer) | à définir dans la configuration | oui | oui | oui | 1 |
| Uno, Nano, Pro Mini | — | **refusées en v1** | — | — | — | — | — | v0 : `Analog1` à `Analog5` |

Autres points communs aux profils :

- La puce Ethernet W5100, W5200 ou W5500 est détectée au démarrage.
- Le lecteur Wiegand est lu par interruption : aucune bibliothèque Wiegand à installer.
- La signature des appels (voir [Appairage](reference.md#appairage)), le chien de garde matériel, le repli sur une adresse fixe quand le DHCP échoue, la console série et la LED d'état existent sur tous les profils.
- Le chiffrement facultatif des badges et des codes **n'existe pas** : aucune carte ne l'annonce.
- Sur la Mega, la broche 10 (sélection du module Ethernet W5X00) et la broche 4 (carte SD du shield) sont réservées.
- Un lecteur compte au plus deux ports Wiegand ; le second est facultatif.

### Broches par défaut des fonctions facultatives

Toutes ces fonctions sont **désactivées par défaut** et à confirmer sur votre câblage. Elles se règlent dans le fichier de configuration du sketch.

| Profil | Gâche | Contact de porte | Bouton de sortie | Autoprotection | Sonnette |
|---|---|---|---|---|---|
| Mega (W5X00 et ENC28J60) | 5 | 6 | 7 | 8 | 9 |
| ESP8266 | 14 | 12 | 13 | — | — |
| ESP32 en Wi-Fi | 25 | 18 | 19 | 23 | 13 |
| WT32-ETH01 | 4 | — | 17 | — | — |
| ESP32-POE | 32 | — | 33 | — | — |

La LED et le buzzer du lecteur n'ont **aucune broche par défaut**. Le détail de chaque réglage (plus de cent lignes) est dans le [guide du sketch](https://github.com/superdcat/JeedomBadger2/blob/master/arduino/Badger2/README.md).

> **Aujourd'hui, le plugin n'envoie aucun ordre d'ouverture au lecteur.** Une gâche câblée sur la carte ne s'ouvre que sur une décision locale du lecteur (bouton de sortie configuré pour ouvrir, politique hors ligne choisie à la compilation). L'ouverture de la porte à la présentation d'un badge passe par un scénario Jeedom qui agit sur un autre équipement. Les ordres envoyés par le plugin au lecteur ne sont pas encore livrés.

<a id="cablage"></a>
## Câblage

Les trois pièges qui détruisent le plus de matériel :

1. **Masse commune.** Reliez ensemble la masse (GND) du lecteur, de la carte et de l'alimentation. Sans elle, le lecteur lit des trames parasites ou rien du tout.
2. **12 V et 5 V (ou 3,3 V) ne se mélangent pas.** Un lecteur RFID demande au moins 9 V, 12 V s'il a un clavier ; une tension plus basse réduit sa portée. Ne reliez **jamais** un fil 12 V à une broche de la carte. N'alimentez pas le lecteur par la broche VIN de la carte quand elle est aussi branchée en USB : vous risquez de la griller. Prenez le 12 V en amont de la carte, sur une alimentation commune.
3. **D0 et D1 inversés.** La carte lit alors des badges faux ou inconnus. Les deux fils sont en général vert (D0) et blanc (D1).

Sur un ESP, ses broches n'acceptent **jamais plus de 3,3 V**. Si les sorties D0 et D1 de votre lecteur montent à 5 V, mesurez-les et intercalez un adaptateur de niveau logique. À confirmer : ce point n'a pas été vérifié avec un lecteur réel.

| Carte | D0 (vert) | D1 (blanc) | Remarque |
|---|---|---|---|
| Mega 2560 + shield Ethernet W5100/W5200/W5500 | 2 | 3 | Le shield se pose sur la Mega ; ne câblez rien sur 4, 10 et 50 à 53. |
| Mega 2560 + module ENC28J60 | 2 | 3 | Module sur le bus SPI de la Mega (50, 51, 52), sélection de puce sur 53 (à confirmer), alimentation selon la fiche du module. |
| ESP8266 (D1 mini, NodeMCU) | GPIO 4 (repérée D2) | GPIO 5 (repérée D1) | À confirmer. |
| ESP32 en Wi-Fi | GPIO 26 | GPIO 27 | À confirmer selon votre carte. |
| WT32-ETH01 | GPIO 32 | GPIO 33 | |
| Olimex ESP32-POE | GPIO 4 | GPIO 13 | À confirmer. |

> Capture à fournir : `images/cablage-mega.png` — doit montrer une Mega 2560 avec son shield Ethernet, les fils D0 et D1 du lecteur sur les broches 2 et 3, et la masse commune.

> Capture à fournir : `images/cablage-esp32.png` — doit montrer un ESP32 avec un lecteur Wiegand (D0 sur GPIO 26, D1 sur GPIO 27) et la masse commune.

> Capture à fournir : `images/cablage-esp8266.png` — doit montrer un Wemos D1 mini avec un lecteur Wiegand (D0 sur GPIO 4, D1 sur GPIO 5) et la masse commune.

Les entrées analogiques (boutons poussoirs, sonnette de digicode) se câblent vers le 5 V avec `A0` à la masse sur les cartes AVR, comme avec les sketchs d'origine ; sur ESP, **jamais plus de 3,3 V**.

**Uno (v0 seulement).** Les schémas de câblage des sketchs d'origine (W5100 et ENC28J60) sont dans la page [Configuration du plugin](configuration.md).

<a id="bibliotheques"></a>
## Préparer l'IDE Arduino

1. Installez l'IDE Arduino (version 2 conseillée) depuis le site officiel d'Arduino.
2. **Mega 2560** : rien à ajouter pour la carte. Installez la bibliothèque `Ethernet` (version testée 2.0.2) avec le gestionnaire de bibliothèques, ou `EthernetENC` (2.0.5) pour un module ENC28J60 : **jamais les deux**.
3. **ESP8266** : dans Fichier > Préférences, ajoutez l'adresse `https://arduino.esp8266.com/stable/package_esp8266com_index.json` aux gestionnaires de cartes supplémentaires, puis installez le paquet `esp8266` (version testée 3.1.2) dans le gestionnaire de cartes.
4. **ESP32** : ajoutez `https://espressif.github.io/arduino-esp32/package_esp32_index.json`, puis installez le paquet `esp32` d'Espressif en version **3.x** (testée : 3.3.12). Le sketch refuse un cœur plus ancien.
5. Aucune bibliothèque Wiegand : elle est intégrée au sketch.

<a id="flasher"></a>
## Récupérer le sketch et le flasher

1. Récupérez le dossier `arduino/Badger2` du dépôt [JeedomBadger2](https://github.com/superdcat/JeedomBadger2) (bouton Code > Download ZIP), ou prenez-le dans le dossier du plugin sur votre Jeedom (`plugins/badger2/arduino/Badger2`). Ouvrez `Badger2.ino` : l'IDE charge tout le dossier.
2. Remplacez le fichier `config.h` du dossier par le fichier de configuration généré (voir [Configuration du sketch d'un lecteur v1](reference.md#configuration-sketch)), ou modifiez-le à la main (voir ci-dessous).
3. Dans Outils > Type de carte, choisissez la carte (ci-dessous), puis le port série.
4. Cliquez sur Téléverser.

| Carte | Entrée du menu « Type de carte » |
|---|---|
| Mega 2560 | Arduino AVR Boards > Arduino Mega or Mega 2560 (processeur ATmega2560) |
| ESP8266 | LOLIN(WEMOS) D1 R2 & mini (essayé en compilation) ; NodeMCU non essayée |
| ESP32 Wi-Fi | ESP32 Dev Module |
| WT32-ETH01 | WT32-ETH01 Ethernet Module |
| Olimex ESP32-POE | OLIMEX ESP32-POE |

Le menu peut nommer ces cartes un peu différemment selon la version du cœur.

<a id="garde-developpement"></a>
### La garde de développement

Le fichier de configuration du dépôt laisse le réglage de garde (`BADGER2_DEVELOPPEMENT_ACCEPTE`) à `0`. Dans ce cas **le sketch refuse de compiler**, avec un message qui dit « le plugin ne sert pas encore le protocole v1 (réponse 503) ». **Ce message est périmé** : le plugin sert la v1. La garde existe parce que la v1 n'est pas recettée sur matériel réel.

- Le fichier généré par le plugin pour un lecteur **appairé** (avec son secret) lève la garde (`1`).
- Le fichier généré pour un lecteur **sans secret** (premier flash, lecteur d'origine) laisse la garde à `0` : passez-la à `1` à la main, en connaissance de cause.
- Le fichier du dépôt, modifié à la main, demande la même modification.

<a id="config-manuelle"></a>
### Remplir le fichier de configuration à la main

Une ligne par réglage ; une ligne commentée (`//`) est facultative, retirez les deux barres pour l'activer. Valeurs à renseigner pour un premier flash :

| Réglage | Valeur à saisir |
|---|---|
| `BADGER2_PROFIL` | Le profil de votre carte (tableau plus haut), par exemple `BADGER2_PROFIL_ESP32_WIFI`. |
| `BADGER2_DEVELOPPEMENT_ACCEPTE` | `1` (voir la garde ci-dessus). |
| `BADGER2_JEEDOM_HOTE` | Adresse IP de Jeedom sur votre réseau, sans zéro de tête (`192.168.1.10`), ou nom DNS de 63 caractères au plus. Ni `http://`, ni port, ni chemin. Un nom en `.local` n'est pas pris en charge. **Avec un module ENC28J60, une adresse IP seulement.** |
| `BADGER2_JEEDOM_PORT` | Port HTTP de Jeedom (80 par défaut). Le lecteur parle en HTTP, pas en HTTPS. |
| `BADGER2_RID` | Identifiant du lecteur dans Jeedom : 1 à 32 caractères parmi lettres, chiffres, `_` et `-`. Facultatif : sans lui, le lecteur s'appelle `BADGER` suivi du dernier octet de son adresse MAC. |
| `BADGER2_WIFI_SSID` et `BADGER2_WIFI_MOT_DE_PASSE` | Cartes Wi-Fi seulement : nom du réseau et mot de passe. |
| `BADGER2_MAC` | Cartes Ethernet de type Mega seulement : une adresse MAC **par lecteur**. Deux lecteurs de même adresse MAC se perturbent : changez le dernier octet de l'un. |

Ne publiez jamais un fichier de configuration rempli (adresses, mot de passe Wi-Fi, secret).

<a id="console-serie"></a>
## Console série (provisionnement et diagnostic)

La console permet de changer l'identifiant, l'adresse de Jeedom, l'adresse de repli et le secret **sans recompiler**, de tester un envoi et d'analyser un lecteur ou un clavier inconnu. Elle n'est **jamais nécessaire** : le lecteur démarre et fonctionne sans câble USB.

Ouvrez le moniteur série de l'IDE, réglez **115 200 bauds** et la fin de ligne sur **« NL et CR »**. Une commande par ligne, sans accent, 80 caractères au plus.

| Commande | Effet |
|---|---|
| `aide` | Liste les commandes. |
| `config` | Affiche l'identifiant, l'adresse et le port de Jeedom, l'adresse de repli, l'état du réseau, la liaison avec Jeedom, les versions, les capacités, la mémoire libre et le niveau de détail. Le secret n'apparaît que comme « défini » ou « non défini », jamais en clair. Chaque valeur dit si elle vient de la console ou du fichier de configuration. |
| `rid <identifiant>` ou `rid -` | Identifiant du lecteur. |
| `hote <adresse ou nom>` ou `hote -` | Adresse de Jeedom (mêmes règles que dans le fichier ; une adresse IP seulement avec un module ENC28J60). |
| `ip <adresse> [<masque> [<passerelle> [<dns>]]]` ou `ip -` | Adresse de **repli** quand le DHCP échoue (masque /24, passerelle `x.y.z.1` et DNS = passerelle par défaut). |
| `secret`, puis le secret seul sur la ligne suivante ; `secret -` | Secret du lecteur : 64 chiffres hexadécimaux minuscules, à coller dans les 60 secondes. Rien ne s'affiche. |
| `traces aucune`, `traces erreurs` ou `traces detail` | Niveau de détail des messages, tout de suite, jusqu'au prochain redémarrage. |
| `test` | Envoie un battement et affiche le résultat : « Jeedom a accepté le battement (ok) », refusé, injoignable ou non conforme, avec le code HTTP, la signature et le délai. |
| `analyse`, puis `fin` | Mode d'analyse des trames Wiegand (voir plus bas). |

À savoir :

- `-` efface la valeur de la console : celle du fichier de configuration s'appliquera au prochain démarrage.
- `rid`, `hote`, `ip` et `secret` ne sont pris en compte **qu'au prochain démarrage** (bouton reset ou coupure du courant) ; `traces` agit tout de suite.
- Une valeur saisie à la console **prime** sur le fichier de configuration. Un fichier généré par le plugin ne l'écrase donc pas : une valeur oubliée à la console peut surprendre ; `config` l'indique.
- Une valeur invalide est refusée par un message fixe qui nomme le champ ; rien n'est modifié. Aucune ligne reçue n'est renvoyée en écho.
- **Pendant la saisie du secret (60 secondes au plus), la porte est hors service** : les événements attendent et les badges présentés n'ouvrent rien.
- Le mode analyse affiche les trames en clair (nombre de bits, valeur, parité, site et carte) et un résumé avec une hypothèse (« une touche par trame », « badge ou clavier qui envoie le code entier »…). **Rien n'est envoyé à Jeedom et aucun badge n'ouvre la porte** pendant l'analyse ; il s'arrête seul au bout de 5 minutes.
- **Sécurité** : une console active permet de changer l'identité et le secret par le port USB. Sur un lecteur physiquement exposé, désactivez-la dans le fichier de configuration (`BADGER2_CONSOLE` à `0`).
- **LED d'état** (facultative, `BADGER2_AVEC_LED_ETAT` à `1`) : clignotement lent = réseau absent ; deux éclats brefs = Jeedom injoignable ; un éclat bref = tout va bien. Sur Mega, c'est la LED intégrée de la broche 13 : vérifiez que rien d'autre n'y est câblé.

<a id="mise-a-jour-distance"></a>
## Mise à jour à distance (ESP8266 et ESP32 seulement)

Le firmware peut être poussé par le réseau depuis votre poste (ArduinoOTA : IDE Arduino, `arduino-cli` ou `espota.py`). Le lecteur ne va jamais chercher de firmware lui-même. La fonction est **coupée par défaut**, **refusée à la compilation sur Mega** et **inactive sans mot de passe**.

> **Sécurité : c'est de l'exécution de code à distance.** Un mot de passe faible ou réutilisé permet à toute machine du réseau d'installer son propre firmware. Le mot de passe protège la session, pas l'image : un intermédiaire sur le réseau local pendant une mise à jour légitime peut la remplacer. Réseau de confiance, mot de passe long, aléatoire et propre à chaque lecteur.

Pour l'activer, dans l'ordre :

1. Dans le fichier de configuration, activez la mise à jour à distance (`BADGER2_OTA` à `1`) et flashez **par câble** une première fois.
2. À la console : `ota mdp`, puis, sur la ligne suivante et dans les 60 secondes, le mot de passe (16 à 64 caractères imprimables sans espace, dont 8 différents au moins). Une chaîne de 64 chiffres hexadécimaux est refusée : c'est la forme du secret du lecteur. Seule l'empreinte du mot de passe est conservée.
3. Redémarrez le lecteur. La console affiche « OTA : active (mot de passe enregistré) » puis « OTA : à l'écoute sur le port … ».

| Commande | Effet |
|---|---|
| `ota` | Affiche l'état : active (avec le port), inactive (aucun mot de passe) ou mémoire illisible. |
| `ota mdp` | Enregistre le mot de passe ; actif au prochain redémarrage. |
| `ota -` | Efface le mot de passe. **L'ancien mot de passe reste valide jusqu'au prochain redémarrage** : la révocation n'est pas immédiate (limite connue, non corrigée). |

Pendant un transfert (10 à 60 secondes environ) :

- la gâche reste verrouillée et le **bouton de sortie n'ouvre pas** : prévoyez une sortie de secours ;
- aucun badge n'est traité ; les événements encore en attente au redémarrage sont perdus ;
- le lecteur redémarre seul à la fin ; son secret, sa configuration de console et son mot de passe sont conservés ;
- un transfert interrompu ou une image refusée laisse l'ancien firmware en place. Gardez un câble USB sous la main : un binaire à la configuration réseau fausse rend le lecteur injoignable.

Sur le poste, visez l'adresse IP du lecteur (réservation DHCP conseillée) : le lecteur n'apparaît pas comme « port réseau » dans l'IDE. Ports : UDP 8266 (ESP8266) ou UDP 3232 (ESP32), puis une connexion de retour du lecteur vers votre poste (ouvrez son pare-feu). Évitez d'écrire le mot de passe dans la ligne de commande : il resterait dans l'historique du shell.

Après un refus de mot de passe, le port est refermé 10 secondes. La vraie protection reste la longueur du mot de passe.
