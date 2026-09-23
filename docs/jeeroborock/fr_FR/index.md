# JeeRoborock

JeeRoborock pilote vos aspirateurs robots Roborock depuis Jeedom, en passant par le cloud Roborock : état
en temps réel, commandes de nettoyage, pilotage fin (aspiration, eau, itinéraire, entretien de la
station), nettoyage par pièce ou par zone, cartes multiples, et exécution des routines (« usages »)
définies dans l'application mobile Roborock.

## Ce que le plugin fait, et ce qu'il ne fait pas

- Le pilotage passe par le **cloud Roborock** : Jeedom doit avoir accès à Internet, et votre robot doit
  être connecté à votre réseau et au cloud Roborock pour répondre. Certaines opérations dépendent
  strictement du cloud et **ne fonctionnent pas sans Internet** : la connexion au compte, l'inventaire des
  robots, l'exécution des usages, la lecture des programmations et la récupération de la photo du robot.
- La bibliothèque utilisée par le plugin **peut**, quand votre robot est sur le même réseau local que
  Jeedom, tenter une connexion directe à l'appareil pour accélérer certains échanges. Ce comportement
  n'est ni réglable ni désactivable depuis Jeedom, et il ne change rien aux points ci-dessus : le plugin
  reste dépendant du cloud Roborock pour fonctionner.
- Le plugin s'adresse aux robots compatibles avec le protocole **V1** de Roborock. Le matériel de
  référence, sur lequel tout est testé, est le **Roborock Qrevo Curv**. D'autres robots V1 peuvent
  fonctionner, mais leurs commandes disponibles varient selon les capacités que le robot annonce
  lui-même — voir plus bas.
- Un robot **partagé** avec vous par un autre compte Roborock apparaît normalement dans la liste, mais
  certaines actions peuvent lui être refusées par le cloud Roborock.

## Prérequis et installation

1. **Jeedom 4.2 minimum**, installé sur un serveur sous **Debian 12 ou 13**. Cette version de Debian est
   nécessaire pour que la dépendance du plugin fonctionne ; en dessous (Debian 11 par exemple),
   l'activation du plugin est refusée.
2. Depuis la page du plugin, laissez Jeedom installer sa dépendance Python. L'indicateur de dépendances de
   la page « Plugins » passe au vert une fois l'installation terminée ; comptez jusqu'à une quinzaine de
   minutes selon la machine.
3. **Activez le plugin** puis démarrez son démon (l'interface le fait automatiquement à l'activation).
   Sans démon démarré, le plugin ne peut ni se connecter à Roborock ni relire l'état d'un robot : la page
   de configuration l'indique par « Le démon ne répond pas ».

## Lier votre compte Roborock

L'authentification se fait par un **code à usage unique envoyé par e-mail** : il n'y a pas de champ mot
de passe, et le mot de passe de votre compte Roborock n'est jamais demandé ni stocké.

Depuis la page de configuration du plugin (menu Plugins > JeeRoborock > Configuration) :

1. Renseignez votre **adresse e-mail** de compte Roborock dans le champ « E-mail du compte Roborock ».
2. **Enregistrez la configuration** (bouton de sauvegarde de la page) avant de demander un code : c'est
   cette valeur enregistrée que le démon utilise.
3. Cliquez sur **« Envoyer un code »**. Roborock vous envoie un code numérique par e-mail (jusqu'à 12
   caractères).
4. Saisissez ce code dans le champ prévu et cliquez sur **« Valider le code »**.
5. L'état du compte passe de « Compte Roborock non lié » à « Compte Roborock lié ».

Un bouton **« Tester la connexion »** permet de vérifier à tout moment que la session enregistrée est
toujours valide, sans consommer votre quota de connexions.

Ce que le plugin conserve : votre adresse e-mail et un jeton de session chiffré (délivré par Roborock lors
de la validation du code). Le mot de passe de votre compte, les clés propres à chaque robot et les jetons
de session bruts ne quittent jamais le démon et ne sont jamais visibles depuis l'interface Jeedom.

### Canal local avec le démon

Le champ **« Port du canal local »** (61350 par défaut) est le port TCP utilisé sur la machine Jeedom
elle-même pour dialoguer avec le démon. Ne le changez qu'en cas de conflit avec un autre logiciel installé
sur le même serveur. Le bouton **« Vérifier le canal »** confirme que le démon répond et que le canal de
retour vers Jeedom (les mises à jour spontanées) fonctionne.

## Synchronisation des équipements

Le bouton **« Synchroniser les équipements »**, sur la page d'accueil du plugin, interroge votre compte
Roborock pour découvrir vos robots et créer les équipements Jeedom correspondants.

Ce n'est **pas** un bouton de rafraîchissement : l'inventaire des robots liés à votre compte est soumis à
un quota Roborock strictement limité et partagé avec l'application mobile (voir plus bas). Ne cliquez sur
ce bouton que lorsque vous ajoutez ou retirez un robot de votre compte Roborock, pas pour actualiser
l'état d'un robot déjà connu — cet état se met à jour tout seul (voir « Temps réel et fraîcheur »).

Un robot partagé par un autre compte est repéré par une étiquette **« Robot partagé »** sur sa carte, dans
la liste des équipements.

Ce bouton ne synchronise **pas** les usages : un robot fraîchement découvert n'en a encore aucun. Les
usages se synchronisent robot par robot, depuis le panneau **« Usages »** de l'onglet « Équipement »
(bouton « Synchroniser les usages », voir « Routines (« usages ») » ci-dessous).

## Ce que contient un équipement

Chaque robot devient un équipement Jeedom. La liste des commandes qu'il porte **dépend des capacités que
le robot annonce réellement** : deux robots, même de modèles proches, n'ont pas forcément exactement la
même liste. Une commande absente signifie une capacité non détectée sur ce robot, pas un défaut du
plugin.

### Informations générales

L'onglet « Équipement » affiche en lecture seule le modèle, le micrologiciel, la version de protocole, le
numéro de série, l'identifiant Roborock et le nom donné au robot dans l'application Roborock. Ces
informations viennent du compte Roborock et sont mises à jour par la synchronisation des équipements.

### État et pilotage de base

| Commande | Ce qu'elle indique ou fait |
|---|---|
| État | Le libellé d'état courant du robot (en nettoyage, en pause, en erreur…) |
| Batterie | Niveau de charge en % |
| En nettoyage | Oui/non |
| Erreur | Libellé de l'erreur en cours, « Aucune » sinon |
| Surface nettoyée | En m², pour le nettoyage en cours |
| Durée de nettoyage | En minutes, pour le nettoyage en cours |
| Avancement | En %, pour le nettoyage en cours |
| En ligne / Connecté | Joignabilité du robot côté cloud, et fraîcheur de la donnée côté plugin |
| Dernière mise à jour | Date et heure de la dernière donnée reçue |
| Démarrer / Mettre en pause / Arrêter | Pilotage du nettoyage. « Démarrer » **reprend** un nettoyage mis en pause ou interrompu (y compris un nettoyage par pièce ou par zone) plutôt que d'en relancer un nouveau ; sans nettoyage en cours, il lance un nettoyage complet |
| Retour à la base | Envoie le robot se recharger |
| Localiser | Fait émettre un signal sonore au robot |
| Rafraîchir | Relit immédiatement l'état du robot |

### Station d'accueil, consommables et entretien

Ces commandes n'apparaissent **que si votre station le permet** :

- état de vidage de la poussière, de lavage et de séchage de la serpillière, erreur station, manque
  d'eau ;
- actions correspondantes : laver la serpillière, sécher la serpillière, arrêter le séchage, vider le
  bac — disponibles uniquement quand le robot est **à sa base** (chargement compris) ; en dehors de cet
  état, le plugin refuse l'action avec un message explicite.

L'usure des consommables détectés par votre robot (brosse principale, brosse latérale, filtre, capteurs,
rouleau de serpillière) est publiée en pourcentage restant, chacune avec une action « Réinitialiser… » à
utiliser après un remplacement physique. Cette action demande une confirmation avant de s'exécuter.

### Journal des nettoyages

Sept commandes en lecture seule renseignent le **dernier nettoyage** connu :

| Commande | Ce qu'elle indique |
|---|---|
| Dernier nettoyage | Synthèse en une ligne, par exemple « Terminé — 42 min, 31,5 m² » ; vaut « Aucun nettoyage connu » tant qu'aucun nettoyage n'a été rapporté |
| Début du dernier nettoyage | Horodatage du début (masquée par défaut) — c'est la seule des sept qui se compare arithmétiquement, à utiliser dans un scénario du type « le robot n'est pas passé depuis trois jours » |
| Durée du dernier nettoyage | En minutes, arrondie à la minute la plus proche (écart possible de ±30 s avec l'application mobile) |
| Surface du dernier nettoyage | En m², arrondie à 0,1 m² |
| Motif de fin du dernier nettoyage | Par exemple « Terminé » ou « Nettoyage interrompu » |
| Clé de motif de fin du dernier nettoyage | Valeur technique stable associée au motif (masquée par défaut) — à préférer au libellé pour tester une condition dans un scénario |
| Erreur du dernier nettoyage | Libellé de l'erreur associée à ce nettoyage, « Aucune » si tout s'est bien passé |

L'onglet « Équipement » propose aussi un panneau **« Journal des nettoyages »** qui liste les 10 derniers
nettoyages connus (début, fin, durée, surface, motif de fin, erreur), avec la date de la dernière
synchronisation. Un bouton **« Rafraîchir le journal »** relit cet historique auprès de Roborock :

- il est protégé par la même garde anti-rafale d'une minute que les autres boutons de resynchronisation du
  plugin — recliquer trop tôt affiche « Le journal vient d'être rafraîchi : patientez une minute avant de
  relancer. » ;
- le premier rafraîchissement peut ne ramener que quelques enregistrements et se compléter au clic
  suivant : c'est un fonctionnement normal, pas une panne, la récupération étant bornée dans le temps ;
- le journal se met aussi à jour tout seul à la fin de chaque nettoyage, sans action de votre part.

Si le cloud Roborock est injoignable au moment de la consultation, les valeurs déjà connues du dernier
nettoyage et de l'historique restent affichées telles quelles — elles ne sont jamais remises à zéro. C'est
la date de dernière synchronisation du panneau qui indique si la donnée est encore fraîche.

### Statistiques cumulées

Quatre commandes en lecture seule renseignent l'usage **global** de votre robot depuis sa mise en
service :

| Commande | Ce qu'elle indique |
|---|---|
| Durée totale de nettoyage | En heures, arrondie au dixième |
| Surface totale nettoyée | En m², arrondie au dixième |
| Nombre total de nettoyages | Nombre entier |
| Nombre total de vidages du bac | Nombre entier ; n'apparaît que si votre station sait vider le bac |

Ce sont des compteurs **cumulés** tenus par le robot lui-même, pas un calcul fait par Jeedom : ils
correspondent à ce qu'affiche l'application mobile Roborock. Contrairement à la plupart des autres
commandes du plugin, elles sont **historisées par défaut**, pour que vous puissiez suivre une courbe
d'usage dans le temps sans réglage préalable.

Leur mise à jour est automatique : à la fin de chaque nettoyage, et au plus une fois par heure sinon.
Il n'y a aucun bouton à cliquer, et aucune conséquence sur les quotas Roborock — la donnée arrive par
le même canal que le journal des nettoyages ci-dessus.

Si vous remettez ces compteurs à zéro depuis l'application Roborock (ou après un reset usine), les
commandes Jeedom suivront cette baisse : elles recopient fidèlement le robot, elles ne mémorisent pas
un maximum. Une chute visible dans l'historique après une telle remise à zéro est donc normale, pas une
anomalie. Si une valeur n'est pas exploitable au moment du relevé (robot injoignable, donnée
aberrante), la commande garde simplement sa valeur précédente plutôt que de retomber à zéro.

### Programmations de l'application

L'onglet « Équipement » propose un panneau **« Programmations de l'application »**, sous forme de
tableau (Récurrence / Répétition / État). Cette liste ne se remplit pas toute seule : cliquez sur
**« Lire les programmations »** pour la peupler. Un horodatage sous le tableau indique la date de la
dernière lecture ; sans clic préalable, le tableau invite à cliquer sur le bouton.

Chaque ligne correspond à une programmation créée dans l'application mobile Roborock et indique :

- sa **récurrence**, affichée **telle que le cloud la renvoie**, sans traduction en jours de semaine
  ni en heure lisible. Ce n'est pas un défaut d'affichage : la forme exacte de cette information n'est
  pas garantie identique selon les modèles de robot, le plugin la restitue donc brute plutôt que de
  risquer une interprétation fausse ;
- si elle est **répétée** ou non (Oui / Non) ;
- si elle est **Active** ou **Désactivée**.

Cette lecture est **seule** : aucune création, modification ni suppression de programmation n'est
possible depuis Jeedom. Tout se gère dans l'application Roborock, qui reste la seule source de vérité.
Après une modification faite dans l'application mobile (désactivation, changement d'horaire...),
recliquez sur « Lire les programmations » pour voir l'état à jour côté Jeedom — il ne se met pas à jour
tout seul.

Deux lectures à moins d'une minute d'intervalle affichent un message invitant à patienter une minute :
ce n'est pas une erreur, c'est la même protection anti-rafale que les autres boutons de resynchronisation
du plugin.

Si le panneau affiche **« Programmations non disponibles pour ce robot »**, c'est un résultat normal, pas
une panne : tous les modèles de robot ne fournissent pas cette information au cloud Roborock. Le reste du
plugin continue de fonctionner normalement dans ce cas.

Ne confondez pas ces programmations avec les **routines (« usages »)** décrites ci-dessous : les routines
sont des scénarios de nettoyage exécutables à la demande depuis Jeedom, les programmations sont des
déclenchements horaires gérés par l'application mobile et seulement consultables ici. Ces programmations
ne créent aucune commande et ne peuvent donc pas être utilisées dans un scénario Jeedom — c'est un
affichage pour information, un choix assumé plutôt qu'un oubli.

## Routines (« usages »)

Les « usages » sont les routines de nettoyage que vous avez créées dans l'application mobile Roborock.
Une fois synchronisées, chacune devient une commande d'action sur l'équipement, exécutable depuis Jeedom
comme n'importe quelle autre commande, ou depuis un scénario.

Ces routines s'exécutent en passant par le cloud Roborock et fonctionnent donc **même si le canal direct
avec le robot est indisponible** — seule une connexion Internet côté Jeedom et un robot connu de votre
compte sont nécessaires.

### Le panneau « Usages »

L'onglet « Équipement » d'un robot comporte une section **« Usages »**, sous le bloc « Inventaire
Roborock ». Elle affiche :

- la **liste des usages que Jeedom connaît** pour ce robot, un par ligne ; quand le nom de la commande a
  été personnalisé dans Jeedom, le nom d'origine dans l'application Roborock est rappelé dans une
  seconde colonne, pour faire le rapprochement ;
- le bouton **« Synchroniser les usages »** — c'est le **seul** endroit où il se trouve, il n'est plus
  dans la barre d'outils de la page ;
- la **règle de synchronisation**, rappelée en clair avant tout clic : elle conserve les usages encore
  présents dans l'application (mêmes commandes, mêmes scénarios), supprime ceux qui n'y sont plus, et
  ajoute les nouveaux.

Si aucun usage n'est encore connu, le panneau l'indique explicitement plutôt que d'afficher une liste
vide : lancez une synchronisation, ou créez d'abord un usage dans l'application Roborock.

Afficher ce panneau ne déclenche aucun appel au démon ni au cloud Roborock : la liste vient de ce que
Jeedom sait déjà, sans consommer de quota.

### Ce que fait une synchronisation

- **Usage encore présent dans l'application** → rien n'est touché : même commande, même identifiant,
  utilisable à l'identique dans un scénario. Seul le nom suit celui de l'application s'il a changé — et
  uniquement si vous ne l'avez pas personnalisé dans Jeedom, auquel cas votre nom est conservé.
- **Usage disparu de l'application** (supprimé côté mobile) → sa commande Jeedom est **supprimée**.
  ⚠️ Un scénario qui la référençait perd sa référence, sans avertissement de Jeedom au moment où cela se
  produit : c'est pourquoi le compte rendu affiché après la synchronisation **nomme** chaque usage
  supprimé, pour que vous sachiez quoi corriger.
- **Usage nouveau dans l'application** → une commande est ajoutée, sans toucher aux autres.

Une commande d'usage ne se supprime **pas à la main** depuis Jeedom : masquez-la si elle vous gêne, ou
supprimez l'usage correspondant dans l'application puis relancez une synchronisation.

Deux synchronisations à moins d'une minute d'intervalle affichent un message invitant à patienter : ce
n'est pas une erreur, c'est la même protection anti-rafale que les autres boutons de resynchronisation du
plugin. Une synchronisation sans aucun changement côté application est une opération neutre, et le dit
(« Aucun changement : vos usages sont déjà à jour. »).

Si la liste reçue du cloud Roborock est **incomplète** (réponse tronquée, ou plus de 64 usages sur ce
robot), la synchronisation applique quand même les ajouts et les renommages, mais **ne supprime rien** :
par précaution, une liste incomplète n'est jamais interprétée comme « ces usages ont disparu ».

Si vous mettez à jour le plugin depuis une version antérieure qui marquait certains usages
« obsolètes », la première synchronisation qui suit les supprime, comme n'importe quel usage absent de
l'application — plus aucun usage ne peut rester durablement dans cet état.

### Quand la lancer, et ce qu'elle coûte

Il n'y a **aucune synchronisation automatique** : un usage créé, renommé ou supprimé dans l'application
Roborock n'apparaît (ou ne disparaît) côté Jeedom qu'après un clic sur « Synchroniser les usages ».
Lancez-la donc chaque fois que vous modifiez vos usages dans l'application.

Elle ne consomme **ni** le quota de connexion **ni** celui d'inventaire des appareils (voir « Quotas
Roborock » plus bas) — mais deux clics à moins d'une minute d'intervalle sont refusés, avec une invitation
à patienter.

Conseil préventif : avant de supprimer un usage dans l'application, repérez les scénarios Jeedom qui
utilisent sa commande. Ils perdront leur référence dès la synchronisation suivante.

Si le compte n'est pas lié, si le démon est arrêté ou si une ré-authentification est requise, le panneau
continue d'afficher la liste des usages déjà connus, et le bouton affiche un message explicite : dans tous
ces cas, **aucun usage n'est supprimé**.

## Tuile de tableau de bord

Chaque robot dispose d'une tuile de tableau de bord regroupant sa photo (ou, à défaut, l'icône du
plugin), son état, une jauge de batterie et les actions de pilotage courantes (démarrer, pause, arrêt,
retour à la base, localiser).

Les commandes que la tuile réunit ainsi n'apparaissent plus **séparément** dans la liste standard des
commandes du dashboard : elles restent néanmoins pleinement utilisables dans un scénario, dans une vue ou
dans un design personnalisé, exactement comme avant. Elles ne sont pas supprimées, seulement masquées de
cet affichage groupé.

## Carte et pièces

### Panneaux de la page d'équipement

L'onglet « Équipement » d'un robot propose deux panneaux supplémentaires :

- **Pièces** — la correspondance entre les segments détectés par le robot et les noms de pièces que vous
  avez donnés dans l'application Roborock. Un bouton **« Resynchroniser les pièces »** relit cette
  correspondance ; faites-le après avoir ajouté, supprimé ou renommé une pièce côté Roborock.
- **Cartes** — la liste des cartes mémorisées par le robot (utile si votre logement a plusieurs étages),
  avec la carte active, un sélecteur pour en choisir une autre et un bouton **« Changer de carte »**. Le
  changement de carte est une opération lente (le robot doit recharger la carte demandée) : le plugin
  refuse une nouvelle demande de changement pendant deux minutes après la précédente. **Changer de carte
  invalide automatiquement la liste des pièces et l'image de la carte affichées**, qui sont ensuite
  resynchronisées.

Le même onglet propose deux blocs distincts, chacun avec son propre bouton :

- **Image de la carte** — l'image de la carte active, reconstruite automatiquement pendant les
  nettoyages (au maximum une fois toutes les 30 secondes) et rafraîchissable manuellement via
  « Rafraîchir l'image de la carte ».
- **Zone et point** — un bloc **purement informatif** (aucune saisie ici) qui affiche le repère de
  coordonnées de la dernière carte récupérée : la zone utilisable en millimètres, la position de la
  base de charge et celle du robot au moment de la carte, ainsi qu'une aide de conversion depuis un
  pixel de l'image. Il sert à préparer les valeurs à saisir dans les commandes « Nettoyer une zone » et
  « Se déplacer vers un point » (voir « Pilotage fin » ci-dessous), qui restent des **commandes de
  l'équipement**, pas des champs de ce panneau. Sans image de carte récupérée, seules des bornes
  générales sont connues.

### Panneau « Carte » (Accueil > JeeRoborock)

La carte est un **panneau**, pas une page du menu Plugins : elle s'ouvre depuis le menu
**Accueil > JeeRoborock**, et elle est accessible à tout utilisateur ayant les droits de lecture sur au
moins un robot (pas seulement les administrateurs). Elle affiche la carte active du robot sélectionné,
son horodatage et la légende des pièces détectées (numéro de segment / nom), et se rafraîchit d'elle-même
toutes les 30 secondes tant que la page reste ouverte.

Si l'entrée n'apparaît pas dans **Accueil**, vérifiez que la case **Afficher le panneau desktop** est
cochée sur la page de gestion du plugin (**Plugins > Gestion des plugins > JeeRoborock**) : elle est
cochée automatiquement à l'installation, mais reste modifiable.

## Pilotage fin

Selon les capacités détectées sur votre robot, les commandes suivantes peuvent apparaître :

- **Puissance d'aspiration** et **débit d'eau** — une commande d'information indique le palier courant,
  une commande d'action (liste déroulante) permet d'en choisir un autre parmi ceux réellement supportés
  par votre robot.
- **Itinéraire de serpillère** et **mode de nettoyage** (aspiration seule / lavage seul / aspiration et
  lavage) — même principe : information + liste déroulante d'action.
- **Nettoyer des pièces** — une commande par pièce détectée (« Nettoyer <nom de la pièce> »), plus une
  commande générique « Nettoyer des pièces (noms séparés par des virgules) » qui accepte une liste de
  noms en texte libre.
- **Nettoyer une zone** — reçoit quatre coordonnées `x1,y1,x2,y2` en millimètres et nettoie le
  rectangle correspondant.
- **Se déplacer vers un point** — reçoit deux coordonnées `x,y` en millimètres.

Les coordonnées de zone et de point sont exprimées dans le même repère que celui utilisé pour la carte
(voir « Carte et pièces »).

## Temps réel et fraîcheur

Une fois un robot synchronisé, son état se met à jour automatiquement, sans action de votre part :
- toutes les **30 secondes** pendant un nettoyage ;
- toutes les **60 secondes** au repos.

La commande **« Dernière mise à jour »** indique l'horodatage de la donnée la plus récente reçue. Si
aucune donnée n'a pu être obtenue depuis plus de **3 minutes**, le plugin bascule les indicateurs
« En ligne » / « Connecté » sur **déconnecté** : c'est un signal de robot injoignable (hors tension, hors
réseau, ou cloud Roborock indisponible), pas une erreur du plugin lui-même.

## Ré-authentification requise

Quand la session enregistrée auprès de Roborock a expiré ou a été révoquée, le plugin affiche
« ré-authentification requise » (message visible sur les commandes concernées, et sur les tentatives
d'action).

**Le plugin ne tente jamais de se reconnecter tout seul.** Cette étape exige de lire un code reçu sur
votre boîte e-mail, ce qu'aucun automatisme ne peut faire à votre place. Pour en sortir :

1. Ouvrez la configuration du plugin.
2. Cliquez sur **« Envoyer un code »**, récupérez le code reçu par e-mail.
3. Saisissez-le et cliquez sur **« Valider le code »**.

Une fois la validation réussie, tout reprend normalement, sans autre intervention.

## Quotas Roborock

Les serveurs Roborock imposent des quotas **stricts et partagés avec l'application mobile de votre
compte** : un nombre limité de connexions par minute/heure/jour, et un nombre limité d'appels
d'inventaire de vos appareils sur les mêmes fenêtres de temps.

Quand un message indique qu'un quota est atteint, **patientez** : ce n'est pas une erreur du plugin, et
retenter aussitôt ne fait qu'aggraver la situation — vous pénaliseriez aussi l'usage de l'application
mobile sur ce même compte, le temps que le compteur se réinitialise. Le plugin ne relance jamais
automatiquement une tentative après un refus de quota.

La synchronisation et l'exécution des usages n'entrent pas dans ces quotas.

## Dépannage

### Rapport de diagnostic

Avant de demander de l'aide, générez un rapport de diagnostic : depuis la **configuration du plugin**,
bloc **« Diagnostic et support »**, cliquez sur **« Générer un rapport de diagnostic »**. Le rapport
apparaît dans une zone de texte, prêt à transmettre.

Il rassemble l'état de l'environnement (versions du plugin, de Jeedom et du démon, y compris la version
de la bibliothèque Roborock utilisée), l'état de la connexion au compte, la liste des robots — chacun
identifié par son numéro d'équipement Jeedom et un identifiant d'appareil partiellement masqué —, les
erreurs récentes remontées par Jeedom et le démon, et une annexe technique. Il ne contient **jamais**
d'identifiant de connexion, de jeton, de clé de robot, de numéro de série ni d'adresse e-mail, quel que
soit le contenu ; les noms que vous avez donnés à vos robots ou à vos pièces n'y figurent pas non plus.

Deux boutons permettent de le récupérer : **« Copier le rapport »** (presse-papiers) et
**« Télécharger le rapport »** (fichier texte). Si la copie automatique ne fonctionne pas — c'est le cas
le plus courant quand Jeedom est servi en HTTP plutôt qu'en HTTPS — le texte reste sélectionné : copiez-le
avec Ctrl+C. Si un forum de support limite la longueur d'un message, joignez plutôt le fichier téléchargé.

Si le démon est arrêté au moment de la génération, le rapport le signale en tête (« Démon injoignable :
rapport partiel ») et reste malgré tout utilisable : les informations encore connues côté Jeedom (dernier
état, horodatage de dernière communication) y figurent quand même. S'il est démarré mais que la section
technique n'a pas pu être produite, le rapport l'indique par un bandeau différent (« Diagnostic du démon
indisponible : rapport partiel ») ; là aussi, le reste du rapport reste exploitable.

Cette action est réservée aux administrateurs de Jeedom.

### Ce qu'il faut joindre à une demande d'aide

En plus du rapport, décrivez dans votre message : le **symptôme précis** (ce que vous observez, et sur
quelle commande ou quel écran), **ce que vous avez déjà essayé**, et l'**heure approximative** à laquelle
le problème est survenu. Ces trois informations permettent de retrouver l'incident dans un rapport ou un
journal, le rapport seul ne suffit pas à deviner le contexte.

**Ne publiez jamais tel quel**, sur un forum ou dans un ticket public :

- votre **adresse e-mail** de compte Roborock ou le **code** reçu par e-mail ;
- un **jeton**, un identifiant de session ou toute valeur qui ressemble à une clé technique ;
- le **contenu brut** des journaux du plugin ou du démon (menu Jeedom « Analyse » > « Logs », ou fichiers
  sous `log/`) : contrairement au rapport de diagnostic, ces journaux **ne sont pas expurgés** ;
- une **capture d'écran** qui laisserait voir l'un de ces éléments.

Le rapport de diagnostic généré depuis la page de configuration est, lui, conçu pour être transmis tel
quel (voir ci-dessus).

| Symptôme | Cause probable | Que faire |
|---|---|---|
| L'indicateur de dépendances reste bloqué / rouge | Installation de la dépendance Python non terminée ou en échec | Patientez la durée d'installation indiquée par Jeedom ; en cas d'échec persistant, vérifiez l'accès Internet du serveur et relancez l'installation depuis la page « Plugins » |
| « Le démon ne répond pas » | Le démon n'est pas démarré, ou vient d'être arrêté | Démarrez (ou redémarrez) le démon depuis la configuration du plugin |
| « Le robot est hors ligne : il ne répond pas au cloud Roborock » | Le robot est éteint, hors réseau, ou n'a pas de connexion au cloud Roborock | Vérifiez que le robot est allumé et connecté à votre réseau Wi-Fi, comme depuis l'application mobile |
| « Le compte Roborock n'est pas lié » | Une action a été demandée alors qu'aucun compte n'a encore été lié | Suivez la procédure de liaison du compte, section « Lier votre compte Roborock » |
| « L'adresse e-mail du compte Roborock est invalide » ou « Aucun compte Roborock ne correspond à cette adresse e-mail » | L'adresse saisie comporte une faute, ou n'est pas celle du compte Roborock | Saisissez l'adresse exacte utilisée dans l'application mobile Roborock, enregistrez la configuration, puis redemandez un code |
| Code de connexion jamais reçu par e-mail | Adresse e-mail incorrecte, ou message filtré par votre messagerie | Vérifiez l'adresse enregistrée, vérifiez vos courriers indésirables, réessayez « Envoyer un code » après quelques minutes |
| « Code de connexion invalide ou expiré » | Le code a été mal recopié ou a expiré | Redemandez un nouveau code et validez-le rapidement |
| « Trop de demandes de code de connexion » | Trop de demandes de code rapprochées | Patientez quelques minutes avant de redemander un code |
| « Session Roborock expirée » / « ré-authentification requise » | La session enregistrée n'est plus valide côté Roborock | Suivez la procédure « Ré-authentification requise » ci-dessus |
| « Quota d'appels Roborock atteint » | Le quota, partagé avec l'application mobile, est temporairement épuisé | Patientez avant de réessayer ; ne relancez pas l'action en boucle |
| Une commande attendue n'apparaît pas sur l'équipement | Le robot n'annonce pas la capacité correspondante | C'est normal : la liste des commandes dépend de ce que le robot déclare savoir faire, pas un bug |
| « Cette carte n'existe pas (ou plus) sur ce robot » | La liste des cartes affichée est périmée | Cliquez sur « Rafraîchir la liste des cartes » puis réessayez |
| « Un changement de carte vient d'être effectué : patientez deux minutes avant d'en relancer un autre » | Le changement de carte est une opération lente, protégée par une garde de deux minutes | Patientez deux minutes avant de relancer un changement de carte |
| « La carte du robot n'a pas pu être décodée » | La donnée reçue de la station est illisible (incident ponctuel côté robot ou cloud) | Réessayez plus tard ; consultez le journal du démon si le problème persiste |
| « L'image de la carte est trop volumineuse pour être transférée » | La carte produite par le robot dépasse la taille que le plugin accepte de stocker | Réessayez plus tard ; si le problème persiste, ce robot n'est pas compatible avec cette fonction |
| « Le robot doit être à la base pour lancer cette opération » | Une action d'entretien de la station a été demandée alors que le robot n'est pas à sa base | Attendez que le robot retourne à sa base, ou lancez « Retour à la base » d'abord |
| « Cette opération d'entretien n'est pas disponible sur la station de ce robot » | La station de ce robot ne prend pas en charge cette action | C'est normal : la commande ne devrait pas apparaître si la station ne le permet pas ; rafraîchissez l'état du robot |
| « La liste des usages reçue du cloud Roborock est incomplète : par précaution, aucun usage n'a été supprimé. » | La réponse du cloud a été tronquée, ou ce robot a plus de 64 usages | Relancez la synchronisation plus tard ; rien n'a été perdu entre-temps |
| « Les conditions d'utilisation Roborock n'ont pas été acceptées » (ou « ont changé ») | Roborock demande de valider (ou revalider) ses conditions d'utilisation | Ouvrez l'application mobile Roborock, acceptez les conditions proposées, puis réessayez depuis Jeedom |
| « Robot inconnu du démon » | L'équipement Jeedom n'est plus reconnu par le démon (redémarrage, robot retiré du compte…) | Relancez « Synchroniser les équipements » |
| « Le cloud Roborock est injoignable » | Jeedom n'arrive pas à joindre les serveurs Roborock | Vérifiez l'accès à Internet du serveur Jeedom |
| Un message évoquant un **délai imparti** dépassé, une **connexion échouée** ou « plusieurs tentatives de communication ont échoué » | Le robot ou le cloud Roborock a mis trop de temps à répondre : incident réseau passager, ou robot très sollicité | Réessayez après une minute ; si cela se répète, vérifiez la connexion Wi-Fi du robot et l'accès à Internet du serveur Jeedom |
| « Le robot est occupé », « Le robot a refusé l'action dans son état actuel » ou « Le robot a signalé une erreur » | Le robot ne peut pas exécuter cette demande dans son état du moment (nettoyage en cours, bac plein, incident mécanique…) | Vérifiez l'état du robot (commande « État », ou application mobile), traitez l'incident signalé puis relancez l'action |
| « Cette fonction n'est pas disponible sur ce modèle de robot » ou « Le robot ne reconnaît pas cette commande » | Le robot n'implémente pas cette fonction, bien que la commande existe dans Jeedom | Aucune manipulation ne débloquera la situation : cette fonction n'existe pas sur ce matériel, masquez la commande si elle vous gêne |
| « Aucune demande de code en cours » | Le démon a redémarré entre l'envoi et la validation du code | Cliquez de nouveau sur « Envoyer un code », puis validez le nouveau code reçu |
| Un réglage (aspiration, débit d'eau, itinéraire, mode de nettoyage) n'est pas appliqué | Le robot refuse ce réglage dans son état actuel (en général : pas au repos) | Réessayez une fois le robot au repos ou à sa base |
| « Cette puissance d'aspiration / ce débit d'eau / cet itinéraire / ce mode de nettoyage n'est pas disponible sur ce robot » | La liste des paliers connue par Jeedom est périmée (le robot n'annonce plus cette valeur) | Rafraîchissez l'état du robot puis réessayez |
| « Pièce inconnue », « aucune pièce connue » ou « plusieurs pièces portent ce nom » | Le nom saisi ne correspond à aucune pièce détectée, aucune pièce n'a encore été synchronisée, ou le nom est ambigu | Resynchronisez les pièces depuis l'onglet Équipement, utilisez le nom exact de l'application Roborock, ou la commande dédiée à cette pièce plutôt que la commande générique |
| « Ces coordonnées sortent des limites de la carte connue » | La zone ou le point saisi dépasse la carte actuellement connue du robot | Vérifiez les coordonnées dans le bloc « Zone et point » de l'onglet Équipement, ou rafraîchissez l'image de la carte |
| « Ce consommable n'est pas suivi pour ce robot » | La commande de réinitialisation a été utilisée avant que l'usure de ce consommable ait été remontée au moins une fois | Rafraîchissez l'état du robot avant de réinitialiser ce consommable |
| « Une synchronisation (ou une lecture) vient d'être effectuée, patientez » (usages, pièces ou programmations) | Une resynchronisation a déjà eu lieu il y a moins d'une minute | Patientez une minute avant de relancer la même resynchronisation |
| « Le journal vient d'être rafraîchi : patientez une minute avant de relancer. » | Le bouton « Rafraîchir le journal » a déjà été utilisé il y a moins d'une minute | Patientez une minute avant de recliquer |
| « La génération du rapport a échoué. » | La requête vers Jeedom n'a pas abouti : délai de 20 secondes dépassé, connexion interrompue ou erreur du serveur Jeedom (un démon arrêté, lui, donne un rapport partiel, pas cet échec) | Rechargez la page de configuration et réessayez ; si cela persiste, consultez le log `jeeroborock` (menu « Analyse » > « Logs ») |
| « 401 - Accès non autorisé » au clic sur « Générer un rapport de diagnostic » | Votre session Jeedom a expiré, ou votre compte n'a pas les droits administrateur | Reconnectez-vous à Jeedom avec un compte administrateur puis réessayez |
| « Diagnostic du démon indisponible : rapport partiel » | Le démon est démarré, mais n'a pas pu fournir la partie technique du rapport (incident ponctuel) | Le reste du rapport reste exploitable ; réessayez plus tard pour obtenir la section technique complète |

Pour tout autre message, le texte affiché par le plugin donne directement la cause et, le cas échéant,
le geste à faire — il n'est jamais nécessaire d'ouvrir les journaux techniques pour le comprendre.

## Limites connues

- Le plugin ne pilote que des robots compatibles avec le protocole V1 de Roborock, via le cloud. Les
  robots plus anciens (protocole A01) ne sont pas pris en charge.
- Les libellés produits par le robot lui-même (état, erreur, état de la station, noms de consommables)
  restent **toujours en français**, quelle que soit la langue choisie pour l'interface Jeedom.
- La carte active affichée dans la configuration d'un équipement ne se met à jour que lors d'un
  changement fait depuis Jeedom, ou détecté au prochain contrôle : un changement de carte fait
  uniquement depuis l'application mobile peut rester affiché comme périmé jusqu'à la synchronisation
  suivante, même si l'image, elle, se met à jour automatiquement.
- La connexion locale évoquée plus haut (« Ce que le plugin fait, et ce qu'il ne fait pas ») ne peut pas
  être désactivée depuis Jeedom.
- Le plugin affiche la version du **micrologiciel** du robot (onglet « Équipement », mise à jour à la
  synchronisation des équipements), mais ne signale pas qu'une mise à jour est disponible et ne la
  déclenche pas : la mise à jour du micrologiciel se fait depuis l'application mobile Roborock.
- Au-delà de **64 usages** enregistrés pour un même robot, la synchronisation des usages continue
  d'ajouter et de renommer, mais ne supprime plus automatiquement les usages disparus de l'application.

Cette page est mise à jour à chaque nouvelle fonctionnalité livrée par le plugin.
