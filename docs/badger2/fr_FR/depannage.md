# Dépannage détaillé

Cette page recense les symptômes et les messages que vous pouvez rencontrer, leur cause et l'action à mener. Chaque entrée est atteignable depuis le [tutoriel](debuter.md) et la [référence technique](reference.md).

**Les messages du plugin cités ici se lisent dans Analyse > Logs, log `badger2`.** Les avertissements n'y sont écrits que si le niveau de log du plugin est au moins **Avertissement** : voir [Niveau de log](reference.md#niveau-de-log). Les messages de la console du lecteur se lisent dans le moniteur série de l'IDE Arduino (115 200 bauds, voir la [console série](cartes-et-sketch-v1.md#console-serie)).

> **À confirmer : les entrées propres au sketch v1 sont tirées du code, pas d'une observation sur matériel réel.**

## Tableau des symptômes

| Symptôme | Cause probable | Entrée détaillée |
|---|---|---|
| Rien ne s'affiche à la console série | Mauvaise vitesse ou mauvais port, console désactivée | [Rien à la console](#rien-console) |
| Le sketch refuse de compiler (« le plugin ne sert pas encore le protocole v1 ») | Garde de développement à `0` | [Compilation refusée : garde](#compilation-refusee-garde) |
| Le sketch refuse de compiler (autre message) | Carte ou profil incompatible, carte Uno | [Compilation refusée : profil](#compilation-refusee-profil) |
| Le lecteur n'apparaît pas dans Jeedom | Inclusion non activée, réseau, adresse de Jeedom | [Lecteur absent de Jeedom](#lecteur-absent) |
| Lecteur présent mais « En attente de l'annonce du lecteur » | Lecteur créé inactif | [Lecteur en attente d'annonce](#lecteur-attente-hello) |
| Le badge est lu mais la porte reste fermée | Badge inconnu ou désactivé, lecteur bloqué, aucun scénario | [Badge lu, porte fermée](#badge-porte-fermee) |
| Le lecteur ne se fait plus entendre après un changement d'adresse | Adresse enregistrée différente, réservation DHCP absente | [Lecteur muet après changement d'adresse](#lecteur-muet-adresse) |
| « version de protocole non supportée » | Le lecteur annonce une version que le plugin ne connaît pas | [Version non supportée](#version-non-supportee) |
| « signature invalide » | Secret du lecteur différent de celui de Jeedom | [Signature refusée](#signature-refusee) |
| « rejeu » | Compteur du lecteur remis à zéro, appel rejoué | [Rejeu refusé](#rejeu-refuse) |
| « rétrogradation » | Lecteur appairé reflashé avec un ancien sketch | [Rétrogradation refusée](#retrogradation-refusee) |
| « Secret absent ou illisible » | Secret perdu côté Jeedom | [Secret perdu](#secret-perdu) |
| Fonction grisée sur la fiche, capacité inconnue | Capacité non annoncée par le lecteur | [Capacité non annoncée](#capacite-non-annoncee) |
| Appel refusé : adresse d'origine non locale ou en-tête de proxy | Lecteur hors réseau local, tunnel ou proxy | [Origine refusée](#origine-refusee) |
| Autres refus d'un appel v1 | Identifiant, équipement en double, corps invalide, retard | [Autres refus d'un appel v1](#autres-refus-v1) |
| Mise à jour à distance sans effet | Mot de passe, port, révocation | [Mise à jour à distance](#depannage-ota) |

<a id="rien-console"></a>
## Rien ne s'affiche à la console série

- **Cause** : vitesse du moniteur différente de 115 200 bauds ; mauvais port série ; fin de ligne qui n'est pas « NL et CR » (les commandes ne passent pas) ; console désactivée dans le fichier de configuration du sketch (`BADGER2_CONSOLE` ou `BADGER2_TRACES` à `0`) ; carte sans puce USB (WT32-ETH01) qui demande un adaptateur série externe.
- **Action** : réglez 115 200 bauds, choisissez le bon port, appuyez sur le bouton reset de la carte (le démarrage se lit sur la console) et tapez `aide`. Si rien n'apparaît toujours, vérifiez la console dans le fichier de configuration. Le lecteur fonctionne sans console : son absence n'empêche pas de lire les badges.

<a id="compilation-refusee-garde"></a>
## Compilation refusée : « le plugin ne sert pas encore le protocole v1 »

- **Cause** : le fichier de configuration du dépôt laisse la garde de développement à `0`. **Le message est périmé** : le plugin sert bien la v1 ; la garde signale que le sketch v1 n'est pas recetté sur matériel réel.
- **Action** : utilisez le fichier de configuration **téléchargé depuis la fiche d'un lecteur appairé** (il lève la garde), ou passez `BADGER2_DEVELOPPEMENT_ACCEPTE` à `1` à la main dans votre fichier. Un fichier téléchargé pour un lecteur **sans secret** laisse la garde à `0` : même action. Voir [La garde de développement](cartes-et-sketch-v1.md#garde-developpement).

<a id="compilation-refusee-profil"></a>
## Compilation refusée : profil, carte ou réglage

- **Cause** : la carte choisie dans l'IDE ne correspond pas au profil du fichier de configuration (le message nomme la carte attendue) ; une Uno, une Nano ou une Pro Mini est refusée en v1 ; deux fonctions sont sur la même broche ; une valeur est hors limites. Chaque refus nomme le réglage à corriger.
- **Action** : corrigez le réglage nommé, ou choisissez la bonne entrée dans Outils > Type de carte (voir le [tableau des cartes](cartes-et-sketch-v1.md#tableau-capacites)). Pour une Uno, gardez le sketch d'origine (v0).

<a id="lecteur-absent"></a>
## Le lecteur n'apparaît pas dans Jeedom

Contrôlez dans l'ordre :

1. **Réseau du lecteur** : la console affiche « Réseau : adresse … » quand le lecteur a une adresse. « Réseau : lien absent » = câble ou Wi-Fi ; « Réseau : pas d'adresse, nouvel essai dans … » = le DHCP ne répond pas ; « Réseau : aucun module Ethernet détecté » = shield ou module mal enfiché, bibliothèque Ethernet non conforme.
2. **Adresse de Jeedom** : `config` à la console montre la cible. « Envoi : Jeedom injoignable, nouvel essai dans … » = adresse ou port faux, pare-feu, Jeedom arrêté. Le lecteur parle en **HTTP** : saisissez le port HTTP de Jeedom, pas celui du HTTPS.
3. **Inclusion** : un lecteur n'est créé que si le **mode inclusion** est actif. Sans lui, le log écrit « Appel v1 refusé : lecteur … inconnu (inclusion désactivée …) » (lecteur v1) ou « Lecteur inconnu detecté : … » (lecteur d'origine). Activez le mode inclusion, redémarrez le lecteur (ou présentez un badge pour un lecteur d'origine) et rechargez la page.
4. **Origine** : voir [Origine refusée](#origine-refusee).
5. **Test** : la commande `test` à la console répond « Jeedom a accepté le battement (ok) » quand tout est bon.

<a id="lecteur-attente-hello"></a>
## Lecteur présent mais « En attente de l'annonce du lecteur »

- **Cause** : un lecteur v1 créé par l'inclusion est **inactif** ; l'appel qui l'a créé n'a aucun autre effet. Même affichage pour un lecteur désactivé au moment de son démarrage.
- **Action** : ouvrez sa fiche, cochez **Activer**, sauvegardez, puis redémarrez le lecteur (bouton reset). Sa fiche affiche alors protocole, firmware, carte et capacités.

<a id="badge-porte-fermee"></a>
## Le badge est lu mais la porte reste fermée

Le plugin ne commande pas la porte tout seul : un badge **connu et actif** met à jour la commande `Presentation` de son équipement, et c'est **un scénario Jeedom** qui ouvre ensuite la porte. Vérifiez :

- **Badge inconnu** : le log écrit « Badge inconnu présenté sur le lecteur … » (niveau Erreur). Enregistrez-le par le mode inclusion, puis activez-le.
- **Badge ou lecteur désactivé** : cochez **Activer** sur l'équipement et sauvegardez.
- **Lecteur bloqué** : après trop de badges inconnus ou de codes faux, le log écrit « Lecteur bloqué » et le lecteur ignore tout pendant le temps de blocage de sa fiche (voir [Fonctionnement](fonctionement.md)).
- **Aucun scénario** : sans scénario déclenché par `Presentation`, rien ne s'ouvre. Voir [Fonctionnement et utilisation des équipements](fonctionement.md).
- **Format de badge non reconnu en v1** : seules les trames de 26 et 34 bits sont reconnues. Un badge enrôlé en décimal (sketch `JeedouinoLAN`) ou lu en 24 ou 32 bits est traité comme inconnu.
- **Premier badge d'un lecteur neuf** : l'appel qui crée un lecteur v1 n'est pas traité ; présentez le badge une seconde fois.
- **Événement en retard** : un événement reçu plus de 30 secondes après sa survenue par un lecteur appairé est accepté sans effet (log « événement … en retard de … s : accepté, sans effet »).
- **Mode debug en observation seule** : la porte n'est pas traitée pendant ce mode. Cliquez sur **Arrêter**.

Pour voir ce que le plugin reçoit, utilisez le [mode debug](reference.md#mode-debug).

<a id="lecteur-muet-adresse"></a>
## Le lecteur ne se fait plus entendre après un changement d'adresse

- **Cause** : le plugin mémorise l'adresse du lecteur. Si elle change (nouveau bail DHCP, redémarrage de la box) hors mode inclusion, les appels sont refusés (réponse 403). Le log écrit « Appel v1 refusé : lecteur … appelé depuis …, adresse enregistrée … : activer l'inclusion le temps d'un appel pour enregistrer la nouvelle adresse (une réservation DHCP évite ce refus) » ; la console du lecteur écrit « Envoi : refusé par le plugin (auth) ».
- **Action** : activez le mode inclusion, faites parler le lecteur (redémarrage ou badge), puis arrêtez l'inclusion : la nouvelle adresse est enregistrée. **Évitez le problème en réservant une adresse fixe au lecteur dans votre box** (réservation DHCP). Un lecteur d'origine met à jour son adresse tout seul.

<a id="version-non-supportee"></a>
## « version de protocole non supportée : mettre à jour le plugin »

- **Message** : « Appel refusé : version de protocole non supportée : mettre à jour le plugin (version reçue …, adresse …, versions servies : v0, v1) », réponse 400.
- **Cause** : le lecteur annonce une version de protocole que ce plugin ne connaît pas (sketch plus récent que le plugin).
- **Action** : mettez à jour le plugin, ou reflashez le lecteur avec un sketch de la version du plugin. Les versions servies s'affichent dans Analyse > Santé.

<a id="signature-refusee"></a>
## « signature invalide »

- **Message** : « Appel v1 refusé : signature invalide (lecteur …, adresse …) », réponse 403 ; console : « Envoi : refusé par le plugin (auth) ». Un lecteur appairé dont l'appel n'est **pas signé du tout** reçoit « Appel v1 refusé : rétrogradation, appel non signé au nom du lecteur appairé … ».
- **Cause** : le secret du lecteur n'est pas celui de Jeedom : secret régénéré après le flash, fichier de configuration ancien, valeur saisie à la console qui prime sur le fichier, sauvegarde Jeedom restaurée.
- **Action** : tapez `config` à la console (le secret est indiqué « défini (console) » ou « défini (config.h) »), puis régénérez le secret depuis la fiche et reconfigurez le lecteur (téléchargement du fichier et flash, ou commande `secret`). Voir [Régénérer le secret](reference.md#regenerer-secret).

<a id="rejeu-refuse"></a>
## « rejeu »

- **Message** : « Appel v1 refusé : rejeu (lecteur …, démarrage …, séquence …) », réponse 403 ; console : « Envoi : le plugin a déjà reçu ce démarrage (mémoire effacée ?) : nouvel appairage nécessaire ».
- **Cause** : le compteur de démarrages du lecteur est repassé en arrière (mémoire du lecteur effacée, effacement complet à l'ISP) ou un appel déjà reçu a été renvoyé. Un lecteur dont la mémoire est usée annonce « Mémoire non volatile : compteur de démarrages non enregistré » : ses badges sont refusés à chaque redémarrage jusqu'au remplacement de la carte.
- **Action** : régénérez le secret depuis la fiche (nouvel appairage) et reconfigurez le lecteur. Si le message revient à chaque redémarrage, changez la carte.

<a id="retrogradation-refusee"></a>
## « rétrogradation » : un lecteur appairé n'est plus entendu

- **Message** : « Appel refusé : rétrogradation : appel v0 (ancienne route|route courante) au nom du lecteur appairé … : seul « Rabaisser à v0 » le permet » ; ou « Appel v1 refusé : version inférieure au plancher du lecteur … ».
- **Cause** : un lecteur appairé a une **version minimale v1** : il n'accepte plus d'appel v0. Typique d'un lecteur reflashé avec un sketch d'origine.
- **Action** : si vous voulez garder le sketch d'origine sur ce lecteur, cliquez sur **Rabaisser à v0** dans sa fiche (le lecteur redevient non authentifié : voir [Rabaisser à v0](reference.md#rabaisser-v0)). Sinon, reflashez-le avec le sketch v1.

<a id="secret-perdu"></a>
## « Secret absent ou illisible »

- **Message** : la fiche affiche « Secret absent ou illisible : tous les appels de ce lecteur sont refusés. Régénérez le secret. » ; log : « lecteur … appairé mais secret absent ou illisible : régénérer le secret » ; ou « Secret de test public : régénérez le secret du lecteur ».
- **Cause** : le secret n'est plus lisible côté Jeedom (restauration d'une sauvegarde, migration).
- **Action** : cliquez sur **Régénérer le secret**, téléchargez la configuration et reconfigurez le lecteur.

Si c'est le **fichier téléchargé** qui est perdu, retéléchargez-le : le secret ne change pas. Le secret n'est jamais affiché à l'écran.

<a id="capacite-non-annoncee"></a>
## Capacité non annoncée ou inconnue

- **Fonction grisée dans la fiche** : elle exige une capacité que le lecteur n'annonce pas ; la raison est affichée. Aucune fonction n'est concernée pour l'instant.
- **Capacité affichée sous son seul nom brut** : le plugin est plus ancien que le sketch. Ce n'est pas une erreur.
- **Côté lecteur** : une réponse n'agit que pour une capacité annoncée. Sans secret, un lecteur n'ouvre pas sur une réponse du plugin (console : « Gâche : sans secret, la réponse du plugin n'ouvre pas »).
- **Deux lecteurs n'ont pas la même liste** : elle dépend de la carte et des fonctions compilées.

<a id="origine-refusee"></a>
## Appel refusé : origine

- « Appel refuse : adresse d'origine non locale … » : le plugin n'accepte que les adresses du réseau local. Un lecteur derrière un VPN ou un routage public est refusé.
- « Appel refusé : en-tête de proxy … présent (tunnel ou reverse proxy) » : le lecteur doit parler **directement** à Jeedom, sans proxy ni tunnel.
- « Appel v1 refusé : adresse d'origine … interdite pour un lecteur (bouclage, adresse du serveur ou adresse invalide) » : une adresse de Jeedom lui-même ou invalide ne peut pas être celle d'un lecteur.

<a id="autres-refus-v1"></a>
## Autres refus d'un appel v1

| Message du log | Cause | Action |
|---|---|---|
| « Appel v1 refusé (adresse …, lecteur …) : » suivi d'un motif (valeur hors bornes, champ absent…) | Corps d'appel invalide, réponse 400 ; console : « Envoi : refusé par le plugin (invalid) » | Vérifiez que le sketch et le plugin sont à jour ; utilisez le mode debug. |
| « identifiant … de casse différente de celui d'un équipement enregistré » | Le lecteur annonce `Porte` alors que l'équipement s'appelle `PORTE` | Alignez la casse de l'identifiant du lecteur. |
| « identifiant … désigne un équipement qui n'est pas un lecteur » | L'identifiant du lecteur est celui d'un badge ou d'un code | Changez l'identifiant du lecteur. |
| « plusieurs équipements portent l'identifiant … » | Deux équipements Badger Fork ont le même identifiant, à la casse près | Supprimez ou renommez le doublon. |
| « verrou d'appairage indisponible » ou « appairage … modifié pendant l'appel » | Appairage en cours de modification | Réessayez ; l'appel est réémis par le lecteur. |
| « réponse non signée (appairage modifié ou secret illisible) » | Appairage modifié ou secret illisible pendant l'appel | Régénérez le secret. |
| Console : « Envoi : réponse non authentifiée (signature absente ou fausse) » | Le lecteur a un secret mais la réponse du plugin n'est pas signée : lecteur non appairé côté plugin ou secrets différents | Appairez le lecteur depuis sa fiche et reconfigurez-le avec son secret. |
| Console : « Envoi : réponse non conforme (HTTP …) » | Réponse inattendue (erreur du serveur web, 503) | Contrôlez Jeedom et le plugin ; le lecteur réémet l'événement. |

<a id="depannage-ota"></a>
## Mise à jour à distance sans effet

- **Aucun port à l'écoute** : le mot de passe n'est pas enregistré ou le lecteur n'a pas redémarré après `ota mdp` (voir [Mise à jour à distance](cartes-et-sketch-v1.md#mise-a-jour-distance)). La console indique « inactive (aucun mot de passe) ».
- **Mega** : la fonction est refusée à la compilation ; elle n'existe que sur ESP8266 et ESP32.
- **Mot de passe refusé** : le port est refermé 10 secondes après un refus.
- **Après `ota -`** : l'ancien mot de passe reste valide **jusqu'au redémarrage suivant** (limite connue).
- **Lecteur injoignable après la mise à jour** : une configuration réseau fausse dans le binaire en est la cause ; reflashez par câble USB.

## Une question qui reste sans réponse ?

Consultez le [mode debug](reference.md#mode-debug) pour voir les appels reçus, puis ouvrez une discussion sur le forum communautaire de Jeedom en joignant le log `badger2` **sans** secret ni valeur de badge.
