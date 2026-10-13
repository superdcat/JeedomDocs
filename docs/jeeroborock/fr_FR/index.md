# JeeRoborock

JeeRoborock pilote vos aspirateurs robots Roborock depuis Jeedom, en passant par le cloud Roborock : état
en temps réel, commandes de nettoyage, pilotage fin (aspiration, eau, itinéraire, entretien de la
station), nettoyage par pièce ou par zone, cartes multiples, et exécution des routines (« usages »)
définies dans l'application mobile Roborock.

## Ce que le plugin fait, et ce qu'il ne fait pas

JeeRoborock est un logiciel libre, publié sous licence **GPL v3 ou ultérieure**.

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

1. **Jeedom 4.4.7 minimum**, installé sur un serveur sous **Debian 12 ou 13**. Cette version de Debian est
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

Un robot ne correspond jamais qu'à **un seul équipement Jeedom** : la page de configuration d'un
équipement JeeRoborock ne propose pas le bouton natif « Dupliquer », et toute tentative de créer un
second équipement pour un robot déjà connu (y compris par une autre voie que l'interface, comme l'API)
est refusée, avec un message qui nomme l'équipement existant. Si un doublon a été créé avant cette
protection, il n'est pas supprimé automatiquement : c'est à vous de supprimer celui des deux qui ne sert
plus, un avertissement étant écrit dans le journal du plugin pour vous aider à le repérer.

## Ce que contient un équipement

Chaque robot devient un équipement Jeedom. La liste des commandes qu'il porte **dépend des capacités que
le robot annonce réellement** : deux robots, même de modèles proches, n'ont pas forcément exactement la
même liste. Une commande absente signifie une capacité non détectée sur ce robot, pas un défaut du
plugin.

### Commandes selon le modèle

Le plugin ne connaît pas de liste de commandes « par modèle ». Il crée une commande quand le robot ou sa
station **déclare** la capacité correspondante, ou **répond** quand le plugin l'interroge. Une commande
absente veut donc dire « ce matériel ne l'annonce pas (ou pas encore) », pas « le plugin est en panne ».
Un robot avec une station complète n'a pas la même liste qu'un robot sans station, ni qu'un robot plus
ancien du même fabricant.

**Faire apparaître une commande qui manque :**

1. Vérifiez que le démon est démarré, que le compte est lié et que le robot est **en ligne** : tant que
   le robot n'a pas répondu une première fois, aucune commande dépendant de ses capacités n'est créée.
2. Lancez la commande **« Rafraîchir »** de l'équipement, ou patientez : l'état est relu tout seul
   toutes les 60 secondes au repos (30 secondes pendant un nettoyage). Les commandes se créent à cette
   relecture. Rechargez ensuite la page de l'équipement.
3. Après une mise à jour du micrologiciel du robot (depuis l'application Roborock) ou du plugin, faites
   la même chose. N'utilisez **pas** « Synchroniser les équipements » pour cela : ce bouton sert à
   découvrir les robots du compte et consomme du quota Roborock.
4. Si le robot a répondu qu'il ne connaît pas un réglage lu par interrogation (ne pas déranger, volume),
   le plugin ne réinterroge qu'**une fois par heure** ; en cas d'échec de lecture (robot injoignable), il
   réessaie au bout de 5 minutes. La commande « Rafraîchir » force une lecture immédiate.
5. Juste après « Rafraîchir », les derniers réglages de la liste (volume, modes de la station) peuvent
   manquer si la relecture a manqué de temps : relancez « Rafraîchir » ou attendez une minute.

Le plugin ne supprime pas de lui-même une commande déjà créée.

| Capacité | Commandes concernées | Condition d'apparition |
|---|---|---|
| Consommables de la station | « Usure filtre station », « Usure brosse de nettoyage », « Usure sac à poussière » et, sauf pour le sac, leur action « Réinitialiser… » | La station possède l'équipement (lavage de la serpillière pour le filtre, brosse de nettoyage, vidage automatique pour le sac) **et** le robot remonte le compteur. Relus environ toutes les heures, ou à « Rafraîchir » |
| Bacs et serpillière | « Réservoir d'eau propre vide », « Bac d'eau sale plein ou absent », « Serpillière installée » | Réservoir et bac : la station lave les serpillières. Serpillière : le robot déclare gérer le mode eau. Créées à la relecture suivante de l'état |
| Verrou enfant | « Verrou enfant », « Activer… », « Désactiver… » | Le robot déclare gérer ce réglage. Créées à la relecture suivante de l'état |
| Ne pas déranger | Information, début, fin, trois actions | Le robot répond à la lecture du mode. Relu toutes les minutes ; à « Rafraîchir » immédiatement |
| Heures creuses | Information, début, fin, trois actions | Le robot déclare la fonction. Créées à la relecture suivante de l'état |
| Volume | « Volume », « Régler le volume » | Le robot répond à la lecture du volume. Relu toutes les minutes ; à « Rafraîchir » immédiatement |
| Modes de la station | « Mode de vidage » et « Régler le mode de vidage » ; « Mode de lavage serpillère » et « Régler le mode de lavage » | La station déclare le vidage automatique (mode de vidage) ou le lavage de la serpillière (mode de lavage). Créées à la relecture suivante de l'état |
| Nombre de passages | Aucune commande propre : un paramètre des actions « Nettoyer des pièces » et « Nettoyer une zone » | Le robot indique, dans son état, gérer la répétition. Alors le champ est libellé « Nombre de passages (1 à 3) » ; sans cela, le champ n'est pas libellé et un nombre de 2 ou 3 est en principe refusé par le plugin |
| Pièce courante | « Pièce courante » | Une image de la carte a été lue, la carte est découpée en pièces et la position du robot est exploitable. Première image : à la première relecture, puis pendant un nettoyage ou après un changement d'état |

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
| En ligne / Connecté | « En ligne » : le robot a répondu à la dernière relecture (bascule à « hors ligne » dès qu'une relecture échoue faute de réponse du robot). « Connecté » : fraîcheur de la donnée côté plugin (canal avec le démon) |
| Dernière mise à jour | Date et heure de la dernière donnée reçue |
| Démarrer / Mettre en pause / Arrêter | Pilotage du nettoyage. « Démarrer » **reprend** un nettoyage mis en pause ou interrompu (y compris un nettoyage par pièce ou par zone) plutôt que d'en relancer un nouveau ; sans nettoyage en cours, il lance un nettoyage complet |
| Retour à la base | Envoie le robot se recharger |
| Localiser | Fait émettre un signal sonore au robot |
| Rafraîchir | Relit immédiatement l'état du robot |

**Pendant le vidage du bac à poussière.** Quand la station vide le bac (état du robot « Vidage du bac à poussière »), le robot ne prend pas en compte un ordre de nettoyage. Le plugin le refuse alors, au lieu de répondre « ok » sans effet : c'est le cas de « Démarrer », de « Nettoyer des pièces », des commandes « Nettoyer <nom de la pièce> » et de « Nettoyer une zone ». Le message affiché est « Le robot vide son bac à poussière : l'ordre de nettoyage n'a pas été envoyé. Réessayez dans un instant, quand le vidage sera terminé (robot de nouveau en charge). » Dans un scénario, l'action échoue de la même façon. Les autres commandes (pause, arrêt, retour à la base, localiser, se déplacer vers un point) ne sont pas concernées, ni les usages (routines), exécutés par le cloud Roborock. Si le plugin ne parvient pas à relire l'état du robot juste avant l'ordre, l'ordre part normalement.

### Station d'accueil, consommables et entretien

Ces commandes n'apparaissent **que si votre station le permet** :

- état de vidage de la poussière, de lavage et de séchage de la serpillière, erreur station, manque
  d'eau. Si le code d'erreur remonté par la station n'est pas reconnu, le libellé affiché est
  « Erreur de station non reconnue » (le code brut reste visible dans la commande de code d'erreur
  station) ;
- actions correspondantes : laver la serpillière, sécher la serpillière, arrêter le séchage, vider le
  bac — disponibles uniquement quand le robot est **à sa base** (chargement compris) ; en dehors de cet
  état, le plugin refuse l'action avec un message explicite.

L'usure des consommables détectés par votre robot (brosse principale, brosse latérale, filtre, capteurs,
rouleau de serpillière) est publiée en pourcentage restant, chacune avec une action « Réinitialiser… » à
utiliser après un remplacement physique. Cette action demande une confirmation avant de s'exécuter.

Selon l'équipement de votre station, et si le robot remonte le compteur, trois usures supplémentaires
apparaissent, elles aussi en pourcentage restant :

- « Usure filtre station » : stations qui lavent la serpillière ;
- « Usure brosse de nettoyage » : stations qui en possèdent une (en pratique, certaines stations haut de
  gamme) ;
- « Usure sac à poussière » : stations à vidage automatique.

Sans station, ou avec une station basique, ces commandes n'apparaissent pas. Le filtre de la station et la
brosse de nettoyage ont chacun une action « Réinitialiser le filtre station » ou « Réinitialiser la brosse
de nettoyage », avec confirmation, comme les autres. Le sac à poussière n'a pas de réinitialisation dans le
plugin (lecture seule) : si vous le remettez à zéro ailleurs (application Roborock), la valeur suit à la
relecture suivante.

Ces valeurs sont relues environ une fois par heure, immédiatement avec la commande « Rafraîchir », et après
une réinitialisation. Les pourcentages peuvent différer légèrement de ceux de l'application Roborock.

**Exemple de scénario** : déclencheur sur la commande « Usure filtre station », condition « inférieure à
10 », action « Envoyer une notification » (« Pensez à remplacer le filtre de la station »). Après le
remplacement, lancez l'action « Réinitialiser le filtre station » (elle demande confirmation) : ne la
mettez pas dans un scénario automatique, le compteur reviendrait à 100 % sans que la pièce ait été changée.

Trois informations oui/non, utilisables dans un scénario, décrivent aussi l'état de l'eau et de la
serpillière :

- « Réservoir d'eau propre vide » et « Bac d'eau sale plein ou absent » : uniquement si votre station lave
  les serpillières. « Oui » signale une situation à vérifier (remplir le réservoir, vider ou remettre en
  place le bac). Le robot ne distingue pas un bac sale plein d'un bac absent, d'où le libellé ;
- « Serpillière installée » : uniquement si votre robot est équipé d'une serpillière.

Ces informations sont distinctes de « Manque d'eau » : le robot les remonte séparément, et elles peuvent
se signaler en même temps. Elles sont rafraîchies avec l'état du robot (environ une minute au repos),
ou immédiatement avec « Rafraîchir ». Si une valeur est momentanément indisponible, la dernière valeur
connue est conservée.

**Exemple de scénario** : déclencheur sur « Réservoir d'eau propre vide » ou « Bac d'eau sale plein ou
absent » (valeur « Oui »), action « Envoyer une notification » (« Vérifiez le réservoir ou le bac de la
station »). Une condition sur « Serpillière installée » (valeur « Non ») permet de ne pas lancer un
nettoyage avec lavage quand la serpillière n'est pas posée.

### Réglages de l'appareil

Le **verrou enfant** désactive les boutons physiques du robot (pratique contre un enfant ou un animal trop curieux). Trois commandes lui sont consacrées :

- « Verrou enfant » : information oui/non, utilisable en condition de scénario (par exemple pour n'activer le verrou que s'il ne l'est pas déjà) ;
- « Activer le verrou enfant » et « Désactiver le verrou enfant » : deux actions.

Ces commandes n'apparaissent **que si votre robot déclare gérer ce réglage**. Sinon, aucune des trois n'existe : ce n'est pas une panne, deux robots n'ont pas la même liste de commandes.

Après un ordre, le plugin relit l'état du robot pour vérifier qu'il l'a bien pris, comme pour les réglages décrits dans « Pilotage fin » (jusqu'à une douzaine de secondes, sans renvoyer l'ordre). La commande « Verrou enfant » n'affiche que ce que le robot a réellement adopté, jamais la valeur demandée. Les messages possibles :

| Message | Signification |
| --- | --- |
| « Verrou enfant activé. » / « Verrou enfant désactivé. » | Le robot a pris l'ordre : l'état relu correspond. |
| « Activation (ou Désactivation) du verrou enfant transmise au robot (application non confirmée). » | L'ordre est parti, mais l'état n'a pas pu être relu, ou un autre ordre de verrou enfant l'a remplacé pendant la vérification. L'état affiché reste l'ancien. |
| « Le robot n'a pas appliqué l'ordre de verrou enfant : l'état relu ne correspond pas à la demande. » | Le robot répond, mais n'a pas adopté le réglage au bout du délai. L'état affiché est celui relu sur le robot. |
| Refus du robot | Le robot a refusé l'ordre ; le message l'indique. |
| Robot hors ligne | Le robot ne répond pas (éteint, hors de portée) ; l'ordre n'est pas pris. |

Le plugin ne renvoie jamais un ordre tout seul : en cas d'échec, relancez-le vous-même.

**Exemple de scénario** : à la fin du nettoyage (« En nettoyage » passe à « Non »), si la condition « Verrou enfant » vaut « Non », lancez l'action « Activer le verrou enfant ».

Un changement fait depuis l'application Roborock (ou la touche du robot) n'est pas signalé au plugin : il apparaît dans « Verrou enfant » sous environ une minute, ou immédiatement avec la commande « Rafraîchir ».

**Patientez quelques secondes entre deux ordres de verrou enfant.** Un ordre envoyé moins de 5 secondes après la fin du précédent (vérification comprise), sur le même robot, est refusé avec le message « Un ordre de verrou enfant vient d'être envoyé à ce robot : patientez quelques secondes avant d'en envoyer un autre. » Dans un scénario, prévoyez une pause d'au moins 5 secondes entre deux actions de verrou enfant.

#### Ne pas déranger

Le mode **ne pas déranger** empêche le robot de démarrer ou de parler pendant une plage horaire (la nuit, par exemple). Six commandes lui sont consacrées :

| Commande | Type | Rôle |
| --- | --- | --- |
| Ne pas déranger | Information oui/non | Indique si le mode est activé, utilisable en condition de scénario |
| Début ne pas déranger | Information texte | Heure de début de la plage, au format HH:MM |
| Fin ne pas déranger | Information texte | Heure de fin de la plage, au format HH:MM |
| Activer ne pas déranger | Action | Active le mode avec la plage enregistrée par le robot |
| Désactiver ne pas déranger | Action | Désactive le mode |
| Définir la plage ne pas déranger | Action avec deux champs, Début et Fin | Enregistre la plage et active le mode |

Ces commandes n'apparaissent **que si le robot répond à la lecture du mode**. Elles sont créées au plus tard environ une minute après que le robot est joignable, ou immédiatement avec « Rafraîchir ». Si elles manquent, ce n'est pas une panne : deux robots n'ont pas la même liste de commandes.

Les heures sont exprimées dans l'**heure locale du robot**, comme dans l'application Roborock.

**Définir la plage** : renseignez les champs Début et Fin au format HH:MM, entre 00:00 et 23:59. Une heure sur un chiffre comme 7:30 est acceptée et normalisée en 07:30. L'action est utilisable dans un scénario : le champ **Titre** reçoit le début, le champ **Message** la fin (leurs aides de saisie sont libellées « Début (HH:MM) » et « Fin (HH:MM) »). Une plage qui franchit minuit est acceptée (par exemple 22:00 → 07:00). Un début égal à la fin est refusé. Définir la plage **active aussi le mode**.

| Saisie (début → fin) | Résultat |
|---|---|
| 22:00 → 07:00, ou 7:30 → 22:15 | Valide (plage qui franchit minuit, ou heure sur un chiffre normalisée en 07:30) |
| 00:00 → 23:59 | Valide |
| 24:00 → 07:00, 22:60 → 07:00 | Refusée : heure ou minute hors bornes |
| 22h00 → 07h00, 2200 → 0700, 22:5 → 07:00 | Refusée : le format doit être HH:MM (minutes sur deux chiffres, séparateur « : ») |
| (champ vide) → 07:00 | Refusée : un champ est vide |
| 22:00 → 22:00 | Refusée : début égal à la fin |

**Exemple de scénario** : tous les soirs à 21 h, lancez l'action « Définir la plage ne pas déranger » avec le début 22:00 et la fin 07:00. Pour couper les annonces en journée, utilisez plutôt « Activer ne pas déranger » / « Désactiver ne pas déranger » sur la plage déjà enregistrée.

**Activer** réapplique la plage déjà enregistrée par le robot. Si le robot n'en renvoie aucune, l'action est refusée : utilisez alors « Définir la plage ». **Désactiver** conserve normalement la plage enregistrée, mais ce comportement dépend du robot et reste à confirmer : si vous comptez sur « Activer » ensuite, contrôlez « Début ne pas déranger » et « Fin ne pas déranger ».

Après un ordre, le plugin relit l'état du robot pour vérifier qu'il l'a bien pris (quelques secondes, sans renvoyer l'ordre). Les commandes d'information n'affichent que ce que le robot a réellement adopté. Les messages possibles :

| Message | Signification |
| --- | --- |
| « Ne pas déranger activé. » / « Ne pas déranger désactivé. » / « Plage ne pas déranger appliquée. » | Le robot a pris l'ordre : l'état relu correspond. |
| « Activation (ou Désactivation) de ne pas déranger transmise au robot (application non confirmée). » / « Plage ne pas déranger transmise au robot (application non confirmée). » | L'ordre est parti, mais l'état n'a pas pu être relu. L'état affiché reste l'ancien. |
| « Le robot n'a pas appliqué l'ordre ne pas déranger : l'état relu ne correspond pas à la demande. » | Le robot répond, mais n'a pas adopté le réglage au bout du délai. |
| « Plage horaire invalide : indiquez un début et une fin au format HH:MM, entre 00:00 et 23:59. » | Un champ est vide ou mal formé. Corrigez-le. |
| « Plage horaire invalide : le début et la fin de la plage ne pas déranger doivent être différents. » | Début et fin identiques. |
| « Le robot n'a renvoyé aucune plage ne pas déranger exploitable : définissez la plage, ce qui active aussi le mode. » | « Activer » n'a aucune plage à réappliquer : utilisez « Définir la plage ». |
| « Un ordre ne pas déranger vient d'être envoyé à ce robot : patientez quelques secondes avant d'en envoyer un autre. » | Deux ordres trop rapprochés. |
| Refus du robot / robot hors ligne | Le robot a refusé l'ordre ou ne répond pas ; l'ordre n'est pas pris. |

Le plugin ne renvoie jamais un ordre tout seul : en cas d'échec, relancez-le vous-même.

Un changement fait depuis l'application Roborock n'est pas signalé au plugin : il apparaît dans Jeedom sous environ une minute, ou immédiatement avec « Rafraîchir ».

**Patientez au moins 5 secondes entre deux ordres ne pas déranger** sur le même robot, sinon le dernier est refusé (message « patientez »). Dans un scénario, prévoyez une pause d'au moins 5 secondes entre deux actions ne pas déranger.

#### Heures creuses

La **recharge en heures creuses** fait attendre au robot la plage horaire choisie (la nuit, par exemple, en tarif réduit d'électricité) pour **recharger sa batterie**. Elle retarde la recharge uniquement : elle ne bloque pas un nettoyage que vous demandez. Six commandes lui sont consacrées :

| Commande | Type | Rôle |
| --- | --- | --- |
| Recharge en heures creuses | Information oui/non | Indique si la fonction est activée, utilisable en condition de scénario |
| Début des heures creuses | Information texte | Heure de début de la plage, au format HH:MM |
| Fin des heures creuses | Information texte | Heure de fin de la plage, au format HH:MM |
| Activer la recharge en heures creuses | Action | Active la fonction avec la plage enregistrée par le robot |
| Désactiver la recharge en heures creuses | Action | Désactive la fonction |
| Définir la plage des heures creuses | Action avec deux champs, Début (HH:MM) et Fin (HH:MM) | Enregistre la plage et active la fonction |

Ces commandes n'apparaissent **que si le robot déclare la fonction**. Elles sont créées au plus tard environ une minute après que le robot est joignable, ou immédiatement avec « Rafraîchir ». Si elles manquent, ce n'est pas une panne : deux robots n'ont pas la même liste de commandes.

Les heures sont exprimées dans l'**heure locale du robot**, comme dans l'application Roborock.

**Définir la plage** : renseignez les champs Début et Fin au format HH:MM, entre 00:00 et 23:59. Une heure sur un chiffre comme 7:30 est acceptée et normalisée en 07:30. L'action est utilisable dans un scénario, avec ces deux champs. Une plage qui franchit minuit est acceptée (par exemple 23:00 → 07:00). Un début égal à la fin est refusé. Définir la plage **active aussi la recharge en heures creuses**. Dans un scénario, le champ **Titre** reçoit le début et le champ **Message** la fin (aides de saisie « Début (HH:MM) » et « Fin (HH:MM) »). Mêmes règles de saisie que « Ne pas déranger » :

| Saisie (début → fin) | Résultat |
|---|---|
| 23:00 → 07:00, ou 7:30 → 22:15 | Valide (la seconde est normalisée en 07:30) |
| 24:00 → 07:00, 23:60 → 07:00 | Refusée : heure ou minute hors bornes |
| 23h00 → 07h00, 2300 → 0700, 23:5 → 07:00 | Refusée : le format doit être HH:MM |
| (champ vide) → 07:00 | Refusée : un champ est vide |
| 23:00 → 23:00 | Refusée : début égal à la fin |

**Exemple de scénario** : une fois par semaine, lancez « Définir la plage des heures creuses » avec le début 23:00 et la fin 07:00 pour réaligner la plage sur votre contrat d'électricité ; ou déclenchez « Activer la recharge en heures creuses » quand votre scénario de départ du domicile s'exécute.

**Activer** réapplique la plage déjà enregistrée par le robot. Si le robot n'en renvoie aucune, l'action est refusée : utilisez alors « Définir la plage des heures creuses ». **Désactiver** conserve normalement la plage enregistrée, mais ce comportement dépend du robot et reste à confirmer : si vous comptez sur « Activer » ensuite, contrôlez « Début des heures creuses » et « Fin des heures creuses ».

Après un ordre, le plugin relit l'état du robot pour vérifier qu'il l'a bien pris (quelques secondes, sans renvoyer l'ordre). Les commandes d'information n'affichent que ce que le robot a réellement adopté. Les messages possibles :

| Message | Signification |
| --- | --- |
| « Recharge en heures creuses activée. » / « Recharge en heures creuses désactivée. » / « Plage des heures creuses appliquée. » | Le robot a pris l'ordre : l'état relu correspond. |
| « Activation (ou Désactivation) de la recharge en heures creuses transmise au robot (application non confirmée). » / « Plage des heures creuses transmise au robot (application non confirmée). » | L'ordre est parti, mais l'état n'a pas pu être relu. L'état affiché reste l'ancien. |
| « Le robot n'a pas appliqué l'ordre de recharge en heures creuses : l'état relu ne correspond pas à la demande. » | Le robot répond, mais n'a pas adopté le réglage au bout du délai. |
| « Plage horaire invalide : indiquez un début et une fin au format HH:MM, entre 00:00 et 23:59. » | Un champ est vide ou mal formé. Corrigez-le. |
| « Plage horaire invalide : le début et la fin des heures creuses doivent être différents. » | Début et fin identiques. |
| « Le robot n'a renvoyé aucune plage d'heures creuses exploitable : définissez la plage, ce qui active aussi la recharge en heures creuses. » | « Activer » n'a aucune plage à réappliquer : utilisez « Définir la plage des heures creuses ». |
| « Un ordre de recharge en heures creuses vient d'être envoyé à ce robot : patientez quelques secondes avant d'en envoyer un autre. » | Deux ordres trop rapprochés. |
| Refus du robot / robot hors ligne | Le robot a refusé l'ordre ou ne répond pas ; l'ordre n'est pas pris. |

Le plugin ne renvoie jamais un ordre tout seul : en cas d'échec, relancez-le vous-même.

Un changement fait depuis l'application Roborock n'est pas signalé au plugin : il apparaît dans Jeedom sous environ une minute, ou immédiatement avec « Rafraîchir ».

**Patientez au moins 5 secondes entre deux ordres d'heures creuses** sur le même robot, sinon le dernier est refusé (message « patientez »). Cette pause est indépendante de celle de « Ne pas déranger » : un ordre ne pas déranger ne retarde pas un ordre heures creuses. Dans un scénario, prévoyez une pause d'au moins 5 secondes entre deux actions heures creuses.

#### Volume

Le **volume** est celui des annonces vocales du robot (« Début du nettoyage », « Retour à la station »…), de 0 à 100 %. Deux commandes lui sont consacrées :

| Commande | Type | Rôle |
| --- | --- | --- |
| Volume | Information numérique (%) | Volume relu sur le robot, utilisable en condition de scénario |
| Régler le volume | Action avec curseur de 0 à 100 | Envoie le volume demandé au robot |

Dans un scénario, « Régler le volume » accepte une valeur (par exemple 40) ou une expression (par exemple un calcul à partir d'une autre commande).

Ces commandes n'apparaissent **que si le robot répond à la lecture du volume**. Elles sont créées au plus tard environ une minute après que le robot est joignable, ou immédiatement avec « Rafraîchir ». Si elles manquent, ce n'est pas une panne : deux robots n'ont pas la même liste de commandes.

**Valeurs acceptées** : un nombre entier de 0 à 100, 0 compris (0 coupe les annonces). Une valeur vide, décimale (50.5) ou hors bornes (-1, 101) est refusée avec le message « Volume invalide : indiquez un nombre entier entre 0 et 100. », sans rien envoyer au robot.

Après un ordre, le plugin relit le volume du robot pour vérifier qu'il l'a bien pris (quelques secondes, sans renvoyer l'ordre). La commande « Volume » n'affiche que ce que le robot a réellement adopté. Les messages possibles :

| Message | Signification |
| --- | --- |
| « Volume appliqué. » | Le robot a pris l'ordre : le volume relu correspond. |
| « Réglage du volume transmis au robot (application non confirmée). » | L'ordre est parti, mais le volume n'a pas pu être relu. La valeur affichée reste l'ancienne. |
| « Le robot n'a pas appliqué le volume demandé : le volume relu ne correspond pas à la demande. » | Le robot répond, mais a retenu une autre valeur. « Volume » affiche la valeur relue. |
| « Un réglage du volume vient d'être envoyé à ce robot : patientez quelques secondes avant d'en envoyer un autre. » | Deux réglages trop rapprochés. |
| Refus du robot / robot hors ligne | Le robot a refusé l'ordre ou ne répond pas ; l'ordre n'est pas pris. |

Le plugin ne renvoie jamais un ordre tout seul : en cas d'échec, relancez-le vous-même. Pour entendre le nouveau volume, lancez la commande « Localiser ».

**Exemple de scénario** : à 22 h, lancez « Régler le volume » avec la valeur 20 ; à 8 h, avec la valeur 50. Pour baisser le volume de moitié, passez une expression à partir de la commande d'information « Volume » (par exemple `round(#[Salon][Robot][Volume]#/2)`, nom d'équipement fictif : le résultat doit être un nombre entier de 0 à 100, sinon l'ordre est refusé, d'où le `round`).

**La position du curseur de « Régler le volume » montre la dernière valeur envoyée depuis Jeedom, pas forcément le volume réel du robot, et ne suit pas un changement fait dans l'application Roborock. La référence est l'information « Volume ».**

Un changement fait depuis l'application Roborock n'est pas signalé au plugin : il apparaît dans « Volume » sous environ une minute, ou immédiatement avec « Rafraîchir ».

**Patientez au moins 5 secondes entre deux réglages du volume** sur le même robot, sinon le dernier est refusé (message « patientez »). Dans un scénario, prévoyez une pause d'au moins 5 secondes entre deux actions « Régler le volume ».

#### Mode de vidage

Le **mode de vidage** règle l'intensité avec laquelle la station vide le bac à poussière du robot. Deux commandes lui sont consacrées :

| Commande | Type | Rôle |
| --- | --- | --- |
| Mode de vidage | Information texte | Mode relu sur la station, utilisable en condition de scénario |
| Régler le mode de vidage | Action de type liste | Envoie le mode choisi à la station |

Ces commandes n'apparaissent **que si la station déclare ce réglage** (vidage automatique du bac) : un robot sans station, ou avec une station qui ne vide pas le bac, n'en a aucune. Elles sont créées au plus tard environ une minute après que le robot est joignable, ou immédiatement avec « Rafraîchir ». Si elles manquent, ce n'est pas une panne : deux robots n'ont pas la même liste de commandes.

**Modes proposés** : Intelligent, Léger, Équilibré, Max. Cette liste vient de la bibliothèque utilisée par le plugin et est identique pour toutes les stations : comparez-la avec celle de l'application Roborock. Si la station renvoie un code que le plugin ne connaît pas, « Mode de vidage » affiche « Mode inconnu (N) », où N est ce code.

Dans un scénario, « Régler le mode de vidage » se choisit par le **code du mode** (et non par son libellé), comme pour les autres commandes de type liste du plugin.

Après un ordre, le plugin relit le mode de la station pour vérifier qu'il a été pris (quelques secondes, sans renvoyer l'ordre). « Mode de vidage » n'affiche que ce que la station a réellement adopté. Les messages possibles :

| Message | Signification |
| --- | --- |
| « Mode de vidage réglé sur « … ». » | La station a pris l'ordre : le mode relu correspond. |
| « Mode de vidage « … » transmis au robot (application non confirmée). » | L'ordre est parti, mais le mode n'a pas pu être relu. La valeur affichée reste l'ancienne. |
| « La station n'a pas appliqué le mode de vidage demandé : le mode relu ne correspond pas à la demande. » | La station répond, mais a retenu un autre mode. « Mode de vidage » affiche le mode relu. |
| « Ce mode de vidage n'est pas disponible sur la station de ce robot : rafraîchissez son état avant de réessayer. » | Le mode demandé n'est pas connu pour cette station. |
| « Un réglage du mode de vidage vient d'être envoyé à ce robot : patientez quelques secondes avant d'en envoyer un autre. » | Deux réglages trop rapprochés. |
| Refus du robot / robot hors ligne | Le robot a refusé l'ordre ou ne répond pas ; l'ordre n'est pas pris. |

Le plugin ne renvoie jamais un ordre tout seul : en cas d'échec, relancez-le vous-même. Le réglage du vidage n'a pas pu être vérifié sur tous les robots : si votre station ne l'accepte pas, le message de refus ci-dessus vous l'indique.

**Exemple de scénario** : déclencheur « Mode de vidage » qui vaut « Max » ; action « Régler le mode de vidage » avec le code du mode « Équilibré » (les codes sont ceux de la liste de la commande), pour repasser en mode courant.

Un changement fait depuis l'application Roborock n'est pas signalé au plugin : il apparaît dans « Mode de vidage » sous environ une minute, ou immédiatement avec « Rafraîchir ».

**Patientez au moins 5 secondes entre deux réglages du mode de vidage** sur le même robot, sinon le dernier est refusé (message « patientez »). Dans un scénario, prévoyez une pause d'au moins 5 secondes entre deux actions « Régler le mode de vidage ».

#### Mode de lavage de la serpillère

Le **mode de lavage** règle l'intensité du lavage de la serpillère par la station. Deux commandes lui sont consacrées :

| Commande | Type | Rôle |
| --- | --- | --- |
| Mode de lavage serpillère | Information texte | Mode relu sur la station, utilisable en condition de scénario |
| Régler le mode de lavage | Action de type liste | Envoie le mode choisi à la station |

Ces commandes n'apparaissent **que si la station déclare ce réglage** : un robot sans station de lavage n'en a aucune. Elles sont créées au plus tard environ une minute après que le robot est joignable, ou immédiatement avec « Rafraîchir ». Si elles manquent, ce n'est pas une panne.

**Modes proposés** : Léger, Équilibré, Profond, plus **Très profond** ou **Intelligent** selon le robot. Comme pour le vidage, comparez avec l'application Roborock. Un code non reconnu s'affiche « Mode inconnu (N) ».

Dans un scénario, « Régler le mode de lavage » se choisit par le **code du mode**, pas par son libellé.

Après un ordre, le plugin relit le mode de la station. Les messages possibles sont les mêmes que pour le vidage, avec « lavage » à la place de « vidage » : « Mode de lavage réglé sur « … ». », « Mode de lavage « … » transmis au robot (application non confirmée). », « La station n'a pas appliqué le mode de lavage demandé… », « Ce mode de lavage n'est pas disponible sur la station de ce robot… » et « Un réglage du mode de lavage vient d'être envoyé à ce robot : patientez quelques secondes… ». Le plugin ne renvoie jamais un ordre tout seul. Ce réglage n'a pas été vérifié sur tous les robots : en cas de refus, le message l'indique.

**Exemple de scénario** : après un nettoyage avec lavage, si « Mode de lavage serpillère » vaut « Léger », lancez « Régler le mode de lavage » avec le code du mode « Équilibré » avant le prochain nettoyage programmé.

Un changement fait depuis l'application Roborock apparaît sous environ une minute, ou immédiatement avec « Rafraîchir ».

**Patientez au moins 5 secondes entre deux réglages du mode de lavage** sur le même robot, sinon le dernier est refusé. Cette pause est indépendante de celle du mode de vidage.

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
- le dernier nettoyage se met aussi à jour tout seul, sans action de votre part : le plugin relit le
  journal dès que le robot a terminé son nettoyage (lavage et vidage à la station compris), puis, tant que
  ce nettoyage n'y apparaît pas, environ 1, 3, 8 et 18 minutes plus tard (au moins 5 minutes d'écart après
  une relecture en échec). Comptez de quelques secondes à quelques minutes, 30 minutes au plus ; si le
  robot est resté injoignable pendant tout ce temps, une dernière relecture a lieu à son retour. Le plugin
  cesse ensuite d'insister jusqu'au nettoyage suivant ; le bouton « Rafraîchir le journal » reste
  disponible.

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

Les noms de cartes s'affichent **en clair**, y compris sur les robots qui les transmettent codés (Roborock
S7 : « %20 » à la place des espaces, « %E9 » à la place de « é »). Si un nom déjà enregistré apparaît
encore codé, cliquez une fois sur **« Rafraîchir la liste des cartes »** (ou changez de carte) : il est
réécrit en clair, sans autre manipulation.

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

### Pièce où se trouve le robot

La commande d'information **« Pièce courante »** indique le nom de la pièce où se trouve le robot.

- **D'où vient la valeur** : elle est déduite de la position du robot sur l'image de la carte déjà
  lue par le plugin. Elle ne demande aucun appel supplémentaire au robot ni au cloud Roborock.
- **Délai** : pendant un nettoyage, la valeur est recalculée environ toutes les 30 secondes. Au repos,
  elle est relue au plus une minute environ après un changement d'état (par exemple le retour à la
  base).
- **Valeurs particulières** (fixes, toujours en français, utilisables telles quelles comme constantes
  dans une condition de scénario) :
  - **« Aucune pièce »** : le robot est hors de toute pièce connue (couloir non découpé, base placée
    hors d'une pièce…).
  - **« Pièce inconnue »** : la position ou la carte active n'est pas connue, les pièces n'ont pas
    encore été synchronisées, ou la carte vient de changer.
- **Ancienneté** : survolez la tuile pour lire les deux dates. La date de valeur est celle de l'entrée
  dans la pièce ; la date de collecte est celle de la dernière image de carte traitée. Un robot
  immobile paraît donc « ancien » : c'est normal.
- **Scénarios** : un scénario ne se déclenche que sur un **vrai changement de pièce**, pas à chaque
  relecture.
  **Exemple de scénario** : déclencheur sur la commande « Pièce courante », condition « vaut Cuisine »
  (nom fictif : utilisez le nom exact de votre pièce), action « Envoyer une notification ». Le scénario
  ne part qu'à l'entrée du robot dans la pièce.
- **Commande absente** : elle n'est pas créée si la carte n'est pas découpée en pièces ou si la
  position du robot n'est pas exploitable. Elle apparaît d'elle-même dès la première image exploitable.
- **Robot hors ligne** : la dernière valeur connue est conservée.
- **Après un changement de carte**, la valeur passe à « Pièce inconnue » jusqu'à un clic sur
  **« Resynchroniser les pièces »**. Faites de même après avoir redécoupé vos pièces dans l'application
  Roborock.

### Panneau « Carte » (Accueil > JeeRoborock)

La carte est un **panneau**, pas une page du menu Plugins : elle s'ouvre depuis le menu
**Accueil > JeeRoborock**, et elle est accessible à tout utilisateur ayant les droits de lecture sur au
moins un robot (pas seulement les administrateurs). Elle affiche la carte active du robot sélectionné,
son horodatage et la légende des pièces détectées (numéro de segment / nom), et se rafraîchit d'elle-même
toutes les 30 secondes tant que la page reste ouverte.

Si l'entrée n'apparaît pas dans **Accueil**, vérifiez que la case **Afficher le panneau desktop** est
cochée sur la page de gestion du plugin (**Plugins > Gestion des plugins > JeeRoborock**) : elle est
cochée automatiquement à l'installation, mais reste modifiable.

La page comporte trois onglets : **Carte et pilotage** (ouvert par défaut), **Station et entretien** et
**Déroulé de la journée**.

#### Panneau de pilotage

À droite de la carte, un panneau permet de **piloter le robot sélectionné** sans quitter la page.
Il se met à jour sans recharger la page et ne fait aucune requête supplémentaire au cloud Roborock.

- **État** : état du robot, batterie et, pendant un nettoyage, avancement.
- **Onglets Total, Pièce et Zone** : changer d'onglet ne lance rien.
  - **Total** : nettoie tout le logement.
  - **Pièce** : cochez une ou plusieurs pièces. Une pièce n'est pas proposée si son nom est absent, en
    double ou contient une virgule : renommez-la dans l'application Roborock, puis resynchronisez les
    pièces. Le nombre de pièces par ordre est limité : au-delà, lancez le nettoyage en plusieurs fois.
  - **Zone** : cliquez et glissez sur la carte pour tracer un rectangle. Une zone trop petite ou qui
    sort de la carte est refusée avant l'envoi. L'onglet est inactif si la carte est indisponible.
- **Réglages** : puissance d'aspiration, débit d'eau et parcours. Seules les valeurs de **votre** robot
  sont proposées, et un réglage qu'il ne gère pas n'est pas affiché. La valeur affichée est celle que le
  robot a réellement adoptée.
- **Bouton principal** : « Nettoyer tout », « Nettoyer N pièces » ou « Nettoyer la zone », selon
  l'onglet. Pendant un nettoyage, il laisse place à **Pause** (ou **Reprendre**), **Arrêter** et
  **Retourner à la base**.
- **Robot hors ligne** : les commandes sont inactives, avec une mention. La dernière carte reste visible.

**Nettoyer une pièce, pas à pas.**

1. Ouvrez **Accueil > JeeRoborock**. Si l'entrée manque, voir plus haut la case **Afficher le panneau
   desktop**.
2. Si vous avez plusieurs robots, choisissez le vôtre dans la liste **Robot**, en haut de la page. Avec un
   seul robot, il n'y a pas de liste.
3. Attendez que la carte et l'état s'affichent. Si une mention signale que le robot est hors ligne ou que
   vous n'avez pas le droit de le piloter, les boutons resteront inactifs (voir Dépannage).
4. Dans le panneau de pilotage, ouvrez l'onglet **Pièce**.
5. Cochez la pièce dans la liste, ou touchez-la sur la carte : elle est mise en évidence. Cochez-en
   plusieurs si besoin. Rien n'est envoyé au robot à cette étape.
6. Si vous le souhaitez, réglez la puissance d'aspiration, le débit d'eau et le parcours.
7. Cliquez sur le bouton principal, **Nettoyer 1 pièce** (ou **Nettoyer N pièces**). C'est ce clic, et lui
   seul, qui envoie l'ordre.
8. Suivez l'état et l'avancement en haut du panneau. Utilisez **Pause**, **Arrêter** ou **Retourner à la
   base** si nécessaire.

Si la pièce n'apparaît pas dans la liste, ou si le bouton reste inactif, consultez le tableau de
Dépannage.

**Carte interactive.** La carte elle-même sert à choisir et à tracer. Rien n'est envoyé au robot tant que
vous n'avez pas cliqué sur le bouton principal.

- **Noms des pièces** : chaque pièce porte son nom, écrit sur la carte. Une pièce sans nom s'affiche
  « Pièce sans nom ». Si la carte ne permet pas de délimiter les pièces, un message l'indique : choisissez
  alors les pièces dans la liste de l'onglet Pièce.
- **Choisir une pièce** : touchez ou cliquez une pièce pour la sélectionner (elle est mise en évidence),
  touchez-la de nouveau pour la désélectionner. La sélection est la même que celle de la liste de l'onglet
  Pièce : cocher ou décocher d'un côté met l'autre à jour. Vous pouvez choisir plusieurs pièces.
- **Pièces non choisissables** : une pièce sans nom, en double ou dont le nom contient une virgule garde son
  étiquette, mais la sélectionner est refusée, avec une explication. Renommez-la dans l'application
  Roborock, puis resynchronisez les pièces depuis la page de l'équipement.
- **Pièce inconnue de la carte actuelle** : après un redécoupage des pièces ou un changement d'étage, une
  pièce déjà cochée peut ne plus exister sur la carte. Elle est signalée « Pièce inconnue de la carte
  actuelle » et le bouton de lancement reste inactif tant qu'elle est cochée. Décochez-la, ou
  resynchronisez les pièces depuis la page de l'équipement.
- **Carte ancienne** : si la carte affichée est une ancienne image (robot injoignable), la sélection sur la
  carte est impossible (« Carte ancienne : sélection impossible »). Sans carte du tout, les onglets Pièce
  et Zone sont inactifs.
- **Tracer une zone** (onglet Zone) : cliquez et glissez pour tracer un rectangle. Faites-le glisser pour le
  déplacer, tirez un de ses coins pour le redimensionner, ou cliquez sur **Effacer la zone** pour le
  supprimer. Le rectangle est conservé quand la carte se rafraîchit, sauf si le robot change d'étage de
  carte ou si vous changez de robot.
- **Zones interdites et murs virtuels** : ceux que vous avez définis dans l'application Roborock sont
  dessinés sur la carte, avec une légende. Ils sont en **lecture seule** : on ne les crée ni ne les modifie
  ici. Une modification faite dans l'application n'apparaît qu'à la prochaine récupération de la carte.
  Si votre robot n'en a pas, ou n'en fournit pas, rien n'est dessiné et aucun message n'apparaît. Une zone
  que vous tracez sur une zone interdite n'est pas bloquée par le plugin.
- **Écran tactile** : toucher, tracer et déplacer fonctionnent sur tablette et téléphone.

**Droits.** Un ordre n'est envoyé qu'à votre clic, et seulement si Jeedom vous autorise à exécuter les
commandes du robot. Les droits se règlent dans la gestion des utilisateurs de Jeedom, robot par robot.
Le profil « utilisateur » a tous les droits par défaut : pour limiter, utilisez un profil restreint. Un
code d'accès ou une confirmation posés sur une commande sont respectés.

| Votre situation | Ce que vous voyez | Ce que vous pouvez faire |
|---|---|---|
| Administrateur | Tous les robots activés | Tout |
| Droit d'exécution sur le robot | Le robot, sa carte, son état, la station et le déroulé | Tout : sélectionner, tracer, lancer, pause, arrêt, station |
| Lecture seule | Le robot, sa carte, son état, la station et le déroulé, avec la mention « Vous n'avez pas le droit de piloter ce robot. » | Consulter, sélectionner des pièces et tracer une zone (rien n'est envoyé). Tous les boutons d'action sont inactifs. |
| Aucun droit sur le robot | Rien : le robot n'est pas dans la liste | Rien. Sans aucun robot accessible, la page affiche « Aucun robot Roborock accessible avec votre compte. » |

Un robot **désactivé** dans Jeedom n'est proposé à personne, administrateur compris. Un lien direct vers un
robot que vous n'avez pas le droit de lire est ignoré. L'affichage de la carte, du panneau et de la frise
ne coûte aucun appel au cloud Roborock.

**Robot mémorisé.** Le robot choisi est retenu dans votre navigateur (pas d'un appareil à l'autre). Un
lien direct vers un robot précis (paramètre de l'adresse) l'emporte sur ce choix.

**Précaution.** Si vous venez d'arrêter un nettoyage par pièce, évitez de lancer aussitôt « Nettoyer
tout » : le robot peut reprendre le nettoyage interrompu au lieu de repartir sur tout le logement.
Vérifiez ce qu'il fait ; au besoin, arrêtez-le puis relancez.

**Aspirer puis laver.** Ce bloc enchaîne deux nettoyages sur la même portée : un **premier passage en
aspiration seule**, puis un **second passage en lavage seul**. Il n'apparaît que si votre robot sait laver
(sinon, ni le bloc ni les commandes correspondantes ne sont créés).

- **Lancer** : dans l'onglet **Total**, le bouton **Aspirer puis laver** traite tout le logement ; dans
  l'onglet **Pièce**, il traite les pièces cochées. Il n'existe pas pour l'onglet Zone. Le nombre de
  passages demandé (voir « Pilotage fin ») s'applique aux deux passages.
- **État affiché** : la ligne **Séquence** indique où en est l'enchaînement : « Passage 1 sur 2 :
  aspiration », « En attente de la base », « Passage 2 sur 2 : lavage », puis, à la fin, « Séquence
  terminée », « Séquence annulée », « Séquence interrompue », « Le second passage n'a pas pu démarrer » ou
  « Séquence abandonnée ». Quand la séquence s'arrête sans aller au bout, le **motif** est affiché dessous
  (voir Dépannage).
- **Annuler** : le bouton **Annuler la séquence** apparaît tant qu'une séquence est active. Il arrête le
  robot, rétablit ses réglages d'origine et empêche le second passage.
- **Fermer le panneau n'interrompt rien** : la séquence est suivie en arrière-plan par le plugin, pas par
  votre navigateur. Rouvrez le panneau pour retrouver l'état.
- Avec le seul droit de lecture, l'état est visible mais les boutons sont inactifs.

#### Onglet « Station et entretien »

Cet onglet regroupe, pour le robot sélectionné, la station d'accueil et l'entretien. Il se met à jour
comme le panneau de pilotage et **ne consomme aucun quota** du cloud Roborock. Le détail de chaque
commande est dans la section « Station d'accueil, consommables et entretien » plus haut.
Il se compose de trois blocs ; **seul ce que votre robot sait faire apparaît**.

- **Actions** : **Vider le bac**, **Laver la serpillère**, **Sécher la serpillère** et **Arrêter le
  séchage**, ainsi que les listes **Mode de vidage** et **Mode de lavage de la serpillère**.
- **État** : vidage du bac, lavage et séchage de la serpillère, eau propre, eau sale, serpillère
  installée, manque d'eau et **incident de la station**. Cet incident est distinct de l'erreur du robot :
  une erreur du robot ne s'y affiche pas. Il est aussi rappelé en bandeau rouge, et la **dernière mise à
  jour** est indiquée en haut de l'onglet.
- **Consommables** : durée de vie restante en pourcentage. À **10 % ou moins**, la mention **À changer**
  apparaît, avec un bandeau d'alerte. Le bouton **Réinitialiser** remet le compteur à zéro après
  confirmation, à faire une fois la pièce remplacée. Il n'existe pas pour le sac.

Si le robot n'a pas de station, l'onglet affiche **Ce robot n'a pas de station.**

**Opération en cours.** Tant qu'une opération de station est en cours, **Vider**, **Laver** et **Sécher**
sont inactifs et portent la mention « Opération en cours ». Il en va de même juste après l'envoi d'un
ordre : le bouton reste inactif jusqu'à ce que l'état change, et au plus pendant **2 minutes**.
**Arrêter le séchage** n'est actif que **pendant un séchage**.

**Refus « robot pas à la base ».** Une opération de station exige que le robot soit à sa base. Sinon, le
plugin la refuse et l'indique (voir le tableau de dépannage). Il ne relance **jamais** l'ordre de
lui-même : ramenez le robot à la base, puis recommencez.

**Robot hors ligne.** Les boutons sont inactifs, avec une mention. Les derniers états connus restent
affichés, avec la date de leur dernière mise à jour.

**Droits.** Avec le seul droit de lecture, l'onglet est en consultation : aucun bouton n'est actif et une
mention l'explique.

#### Onglet « Déroulé de la journée »

Cet onglet montre, sur une **frise horaire**, ce que le robot a fait au fil d'une journée : une bande de
couleur, une couleur par état. Il est en **lecture seule** et **ne consomme aucun quota** du cloud
Roborock : il relit seulement ce que le plugin a déjà enregistré. Il n'est visible que si vous avez le
droit de **lecture** sur le robot.

**Légende.** Chaque couleur correspond à une catégorie :

| Catégorie | Signification |
|---|---|
| **Nettoyage** | Le robot aspire ou lave. |
| **Retour à la base** | Le robot rentre à sa base. |
| **En charge** | Le robot est posé sur sa base. |
| **Vidage du bac** | La station vide le bac. |
| **Lavage de la serpillère** | La station lave la serpillère. |
| **Séchage de la serpillère** | La station sèche la serpillère. |
| **En erreur** | Le robot est en erreur. |
| **Hors ligne** | Le robot ne répond pas. |
| **Autre état** | Tout état qui n'a pas sa propre couleur. |
| **Inconnu** | Aucune information reçue pendant cette période. |

**« Inconnu ».** Cette zone hachurée couvre une période **sans donnée** : démon arrêté, Jeedom éteint. Le
plugin ne prolonge **jamais** le dernier état connu. Une période est « Inconnue » au-delà de **15
minutes** sans nouvelle du robot.

**Nettoyages terminés.** Sous la frise, une fine bande sombre (**Nettoyage terminé**) surligne les
nettoyages du **journal des nettoyages** qui rencontrent la journée affichée.

**Détail.** Survolez (souris) ou touchez (écran tactile) une période pour afficher son détail sous la
frise.

**Navigation.** Les boutons **Jour précédent** et **Jour suivant** changent de jour. Les **7 derniers
jours** sont conservés ; les plus anciens sont supprimés automatiquement. Les heures sont celles du
**fuseau horaire de Jeedom**. Un jour sans enregistrement affiche **Aucune donnée ce jour-là.**

**L'historique commence à l'installation de la mise à jour.** Le plugin n'a aucun moyen de reconstituer
le passé : les journées antérieures n'ont pas de donnée.

#### Panneau mobile (application et version mobile de Jeedom)

Le panneau de pilotage est aussi disponible sur téléphone, dans l'application mobile Jeedom et dans la
version mobile web de Jeedom.

**Où le trouver.** Ouvrez **Accueil**, puis **Plugins**, puis **JeeRoborock**. L'onglet dédié du menu
personnalisé de l'application mobile est réservé aux **administrateurs** : c'est une limite de Jeedom, pas
du plugin. Après la mise à jour du plugin, si l'entrée n'apparaît pas, **resynchronisez l'application**.
L'administrateur peut masquer ce panneau dans la configuration du plugin, côté Jeedom.

**Ce qu'il contient :**

- le choix du robot (si vous en avez plusieurs) ;
- la carte, avec les pièces cliquables et les zones interdites ;
- les onglets **Total**, **Pièce** et **Zone** : pour une zone, tracez le rectangle au doigt sur la carte,
  puis déplacez-le ou redimensionnez-le par ses coins ;
- les réglages (aspiration, débit d'eau, parcours) quand le robot les propose ;
- les boutons **Pause**, **Reprendre**, **Arrêter** et **Retourner à la base** ;
- **Aspirer puis laver**, quand le robot le permet.

**Ce qu'il ne contient pas.** La page **Station et entretien**, le **déroulé de la journée** et le tableau
des pièces détectées ne sont pas disponibles sur mobile : ouvrez la page Carte de Jeedom sur un ordinateur.

**Droits.** Ce sont les mêmes qu'au bureau : avec le seul droit de lecture, le panneau est en consultation.

**Mises à jour.** L'affichage se met à jour tout seul tant que le panneau est à l'écran. Il est suspendu
quand l'application passe en arrière-plan et reprend à votre retour.

**Après une mise à jour du plugin.** Si le panneau se comporte bizarrement, fermez complètement
l'application puis rouvrez-la : une ancienne version est peut-être restée en cache.

## Pilotage fin

Selon les capacités détectées sur votre robot, les commandes suivantes peuvent apparaître :

- **Puissance d'aspiration** et **débit d'eau** — une commande d'information indique le palier courant,
  une commande d'action (liste déroulante) permet d'en choisir un autre parmi ceux réellement supportés
  par votre robot.
- **Itinéraire de serpillère** et **mode de nettoyage** (aspiration seule / lavage seul / aspiration et
  lavage) — même principe : information + liste déroulante d'action.
- **Nettoyer des pièces** — une commande par pièce détectée (« Nettoyer <nom de la pièce> »), plus une
  commande générique « Nettoyer des pièces (noms séparés par des virgules) » qui accepte une liste de
  noms en texte libre. Comme pour les usages, le nom de la commande suit les renommages faits dans
  l'application Roborock à la synchronisation suivante — y compris quand le nom de la pièce contient une
  apostrophe, une esperluette, un dièse ou un pourcentage (« Salle d'eau », par exemple) — sauf si vous
  avez personnalisé ce nom à la main dans Jeedom, auquel cas votre nom personnalisé est conservé.
  Pour nettoyer en plusieurs passages, voir « Nombre de passages » ci-dessous.
- **Nettoyer une zone** — reçoit quatre coordonnées `x1,y1,x2,y2` en millimètres et nettoie le
  rectangle correspondant. Le nombre de passages se règle comme pour les pièces (voir ci-dessous).
- **Nombre de passages** (commandes « Nettoyer des pièces » et « Nettoyer une zone ») — renseignez le
  champ **Message** de la commande, puis indiquez 1, 2 ou 3 (en chiffres) dans le champ **Titre**.
  - **C'est un paramètre de l'ordre en cours, pas un réglage.** Il n'existe aucune commande « Nombre de
    passages » à régler une fois pour toutes : indiquez-le à chaque ordre, sinon c'est un seul passage.
    Il n'est jamais mémorisé par le robot ni par le plugin.
  - Champ Titre vide : un seul passage, comme avant.
  - Un nombre de trois chiffres ou plus (« 100 », « 2024 ») ou du texte (« deux ») est ignoré : le
    nettoyage se fait en un passage, sans message.
  - 0, un nombre de 4 à 99, un nombre signé ou décimal sont refusés (voir Dépannage).
  - Le même nombre s'applique à chaque pièce de l'ordre ; pour une zone, il s'applique à la zone.

  | Champ Titre | Résultat |
  |---|---|
  | (vide), 1 | Un passage |
  | 2, 3 | Deux ou trois passages |
  | 0, 4, 10, 99 | Refusé : nombre entier de 1 à 3 attendu |
  | -1, +2, 2.5, 2,5 | Refusé : nombre signé ou décimal |
  | 100, 2024, deux, x2 | Ignoré : un seul passage, sans message |

  **Exemple de scénario** : action « Nettoyer des pièces » avec, dans le champ Message, « Cuisine,
  Salon » (noms fictifs) et, dans le champ Titre, 2 : les deux pièces sont nettoyées en deux passages.
  Pour la zone, le champ Message reçoit `x1,y1,x2,y2` et le champ Titre 2 ou 3.
  - Les boutons « Nettoyer <pièce> » font toujours un seul passage.
  - Quand le champ Message est vide, le champ Titre garde son rôle habituel (noms de pièces ou
    coordonnées), malgré son libellé.
  - Le champ est libellé « Nombre de passages (1 à 3) » seulement si le robot déclare gérer la
    répétition.
  - Le réglage de répétition de l'application Roborock n'est jamais modifié. Sans nombre de passages,
    le robot applique son propre réglage, comme avant.
  - Un nombre de passages de 2 ou 3 est refusé par le plugin si le robot, relu juste avant l'ordre, ne
    déclare pas gérer la répétition. Si la relecture échoue, l'ordre part et c'est le robot qui décide.
- **Se déplacer vers un point** — reçoit deux coordonnées `x,y` en millimètres.
- **Aspirer puis laver** — enchaîne un passage en aspiration seule puis un passage en lavage seul. Quatre
  commandes, créées seulement si le robot sait laver :
  - **Aspirer puis laver (pièces séparées par des virgules, vide pour tout le logement)** (action) :
    champ **Message** vide = tout le logement ; sinon, noms de pièces séparés par des virgules (comme
    « Nettoyer des pièces »). Le **nombre de passages** se met dans le champ **Titre** (1 à 3), pour la
    portée « pièces » seulement ; il s'applique aux deux passages. Pour tout le logement, il n'y a pas
    de nombre de passages : un seul passage par étape.
  - **Annuler la séquence** (action) : arrête la séquence en cours. Sans séquence active, elle répond
    qu'il n'y a rien à annuler.
  - **État de la séquence** (information) : « Aucune séquence », « Passage 1 sur 2 : aspiration », « En
    attente de la base », « Passage 2 sur 2 : lavage », « Séquence terminée », « Séquence annulée »,
    « Séquence interrompue », « Le second passage n'a pas pu démarrer » ou « Séquence abandonnée ».
  - **Motif de fin de séquence** (information) : « Aucun », ou la raison pour laquelle la séquence s'est
    arrêtée (voir Dépannage). Ces deux informations ne sont pas historisées.

  **Exemple de scénario** : action « Aspirer puis laver » avec « Cuisine, Salon » (noms fictifs) dans le
  champ Message ; un second bloc peut attendre que « État de la séquence » vaille « Séquence terminée ».

  **Comment la séquence se déroule.**
  - Le second passage ne part que lorsque la **fin normale du premier passage est confirmée par le
    journal du robot** et que le robot est **en charge de façon stable depuis 30 secondes** à sa base
    (le temps du vidage ou du lavage éventuel). Un robot en vidage n'est jamais relancé : le plugin
    attend.
  - **Attente maximale de la base : 15 minutes** après la fin du premier passage. Au-delà, le second
    passage n'est pas lancé.
  - Le plugin vérifie que le robot **a bien démarré** : sans démarrage constaté sous **2 minutes**, le
    passage est déclaré sans effet.
  - **Durée maximale d'un passage : 6 heures.** Au-delà, la séquence est arrêtée.
  - À chaque fin (réussie, annulée ou interrompue), les **réglages d'origine** du robot (aspiration,
    débit d'eau, itinéraire) sont **rétablis**. Pendant la séquence, le plugin les remplace par des
    réglages « aspiration seule » puis « lavage seul ».
  - **Pendant une séquence, les autres nettoyages sont refusés** : nettoyer des pièces, une zone, lancer
    un usage, ou « Démarrer » (sauf pour **reprendre** un nettoyage mis en pause). Annulez d'abord la
    séquence.
  - **Arrêter** ou **Retour à la base**, depuis Jeedom ou depuis l'application mobile, mettent fin à la
    séquence : le second passage n'est pas lancé.
  - **Aucune nouvelle tentative automatique** : si le second passage ne peut pas démarrer, rien n'est
    renvoyé. Relancez la séquence vous-même.
  - Lancer une séquence sur un robot qui nettoie déjà (ou est en pause) est refusé.

Après un réglage de puissance d'aspiration, de débit d'eau, d'itinéraire de serpillère ou de mode de
nettoyage, le plugin relit l'état du robot pour vérifier qu'il l'a bien pris. Il lui laisse jusqu'à une
douzaine de secondes, sans renvoyer l'ordre : si le robot le prend tout de suite, la réponse n'est pas
ralentie. Le message « non appliqué » n'apparaît que si le robot n'a toujours pas la valeur au bout de ce
délai. Si vous enchaînez deux réglages très vite sur le même robot, seul le dernier est vérifié : le
précédent est signalé « transmis au robot (application non confirmée) », sans erreur. Le même message
apparaît si le robot ne répond plus pendant la vérification.

Les coordonnées de zone et de point sont exprimées dans le même repère que celui utilisé pour la carte
(voir « Carte et pièces »).

## Temps réel et fraîcheur

Une fois un robot synchronisé, son état se met à jour automatiquement, sans action de votre part :
- toutes les **30 secondes** pendant un nettoyage ;
- toutes les **60 secondes** au repos.

La commande **« Dernière mise à jour »** indique l'horodatage de la donnée la plus récente reçue.

L'indicateur **« En ligne »** réagit vite : il bascule sur **hors ligne** dès qu'une relecture périodique
échoue faute de réponse du robot (au repos, une relecture a lieu environ toutes les minutes ; environ
toutes les 40 secondes en nettoyage), et revient **en ligne** dès qu'une lecture réussit, qu'une mise à
jour est reçue spontanément du robot, ou qu'une action lui est confirmée. Le retour « en ligne » peut
prendre quelques secondes seulement (le robot envoie une mise à jour) ou, dans le pire cas où le robot
est resté injoignable longtemps, jusqu'à une dizaine de minutes (les relectures s'espacent
progressivement après plusieurs échecs).

Indépendamment de ce mécanisme, si **aucune** donnée n'a pu être obtenue depuis plus de **3 minutes**, le
plugin bascule les deux indicateurs « En ligne » **et** « Connecté » sur **déconnecté** : c'est un signal
de robot injoignable (hors tension, hors réseau, ou cloud Roborock indisponible), pas une erreur du
plugin lui-même.

### Plusieurs robots sur le même compte

Un robot éteint, déchargé ou hors Wi-Fi n'empêche plus de piloter et de suivre les autres robots de
votre compte : il s'affiche simplement **hors ligne**. Les tentatives de reconnexion à ce robot ne
consomment **pas** le quota Roborock (voir « Quotas Roborock »).

Une fois rallumé, le robot redevient pilotable **de lui-même**, sans nouvelle authentification ni
réinstallation. Comptez **6 minutes au plus** après le retour de sa connexion : l'attente entre deux
tentatives s'allonge progressivement, jusqu'à **5 minutes**.

Pendant ce court intervalle, le robot peut déjà apparaître **en ligne** alors que ses commandes sont
encore refusées comme **hors ligne**. Patientez quelques minutes, puis réessayez.

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
| « Le robot vide son bac à poussière : l'ordre de nettoyage n'a pas été envoyé… » | Un ordre de nettoyage (« Démarrer », « Nettoyer des pièces », « Nettoyer <pièce> », « Nettoyer une zone ») a été donné pendant que la station vide le bac ; le robot l'aurait ignoré | Patientez la fin du vidage (quelques secondes à une minute), puis relancez l'ordre. Dans un scénario, attendez que l'état du robot soit revenu à « En charge » avant de relancer |
| « Une séquence « aspirer puis laver » est en cours sur ce robot : annulez-la avant de lancer un autre nettoyage. » | Un nettoyage (pièces, zone, usage, « Démarrer ») a été demandé pendant une séquence | Cliquez sur « Annuler la séquence », ou attendez sa fin, puis relancez |
| « Le robot a déjà un nettoyage en cours ou en pause : arrêtez-le avant de lancer « aspirer puis laver ». » | La séquence a été lancée alors que le robot nettoyait ou était en pause | Arrêtez le nettoyage, puis relancez la séquence |
| Séquence interrompue : « Le robot a été arrêté ou renvoyé à la base pendant la séquence… » | Vous (ou l'application mobile) avez utilisé Arrêter ou Retour à la base | Normal : le second passage n'est pas lancé. Relancez la séquence si besoin |
| Séquence interrompue : « Le robot s'est arrêté en erreur pendant la séquence… » | Le robot a signalé une erreur (bloqué, bac manquant…) | Consultez l'état du robot, traitez l'incident, relancez |
| « Le robot a accepté l'ordre de nettoyage mais n'a pas démarré. » | Aucun démarrage constaté sous 2 minutes | Vérifiez l'état du robot (bac, vidage en cours…), puis relancez |
| « Le premier passage ne s'est pas terminé normalement selon le journal du robot… » | Le journal du robot ne classe pas le premier passage comme terminé normalement | Le second passage n'est pas lancé par précaution : consultez le journal des nettoyages, relancez si besoin |
| « La fin normale du premier passage n'a pas pu être confirmée par le journal du robot dans le délai d'attente… » (« Le second passage n'a pas pu démarrer ») | Le journal du robot n'a pas confirmé la fin du premier passage dans les 15 minutes | Le plugin ne lance jamais le lavage sans cette confirmation : relancez la séquence, ou lancez un lavage seul à la main |
| « Le robot n'est pas redevenu disponible dans le délai maximal d'attente… » | Après le premier passage, le robot n'est pas revenu en charge à sa base (stable depuis au moins 30 secondes) en 15 minutes (retiré de la base, vidage bloqué…) | Remettez le robot à sa base, puis relancez la séquence |
| « Le robot a été relancé en dehors de la séquence… » | Un nettoyage a été lancé (par exemple depuis l'application mobile) pendant l'attente de la base | Le second passage n'est pas lancé : relancez la séquence une fois le robot à la base |
| « Le passage en cours n'a pas abouti dans la durée maximale prévue… » | Un passage dure plus de 6 heures | La séquence est arrêtée : vérifiez le robot |
| « Le plugin n'a pas pu suivre le robot pendant plusieurs minutes… » | Robot ou réseau injoignable pendant plusieurs minutes | Le robot a pu continuer son passage ; ses réglages d'origine ne sont pas rétablis : vérifiez son mode de nettoyage |
| « Les réglages d'origine du robot n'ont pas pu être rétablis… » | Le rétablissement a échoué en fin de séquence | Vérifiez et corrigez le mode de nettoyage du robot |
| « Séquence abandonnée » : « La séquence n'est plus suivie par le démon… » | Le démon a été arrêté ou redémarré pendant la séquence (ou le démon est mort) | Le second passage ne sera pas lancé ; le robot a pu poursuivre son passage, et ses réglages d'origine ne sont pas rétablis : vérifiez-les, puis relancez si besoin |
| « La session Roborock du plugin a changé pendant la séquence… » | Le compte a été changé ou retiré pendant la séquence | Même conséquence : réglages non rétablis, à vérifier |
| « Aucune séquence « aspirer puis laver » en cours sur ce robot : rien à annuler. » | **Annuler la séquence** a été demandé alors qu'aucune séquence n'est active (elle s'était déjà terminée) | Rien à faire : consultez la ligne **Séquence** |
| « Annulation enregistrée : le robot sera arrêté… » | L'annulation est prise en compte, mais un ordre est encore en cours d'envoi | Normal : patientez quelques secondes ; l'état passe à « Séquence annulée » |
| « Séquence annulée, mais l'arrêt du robot a échoué… » ou « Séquence annulée ; les réglages d'origine du robot n'ont pas pu être rétablis. » | Le robot n'a pas confirmé l'arrêt, ou le rétablissement de ses réglages a échoué | Vérifiez l'état du robot, arrêtez-le depuis le panneau si besoin, et contrôlez ses réglages |
| Bouton « Aspirer puis laver » absent | Le robot ne sait pas laver, ou l'onglet Zone est ouvert (la séquence n'existe que pour Total et Pièce) | Normal : ouvrez l'onglet Total ou Pièce ; sur un robot sans lavage, la fonction n'existe pas |
| « Nombre de passages invalide : indiquez un nombre entier de 1 à 3… » | Le champ Titre d'un nettoyage de pièces ou de zone (avec le champ Message rempli) contient un nombre refusé : 0, 4 à 99, signé ou décimal | Saisissez 1, 2 ou 3 en chiffres, ou laissez le champ vide pour un seul passage |
| « Nombre de passages non supporté par ce robot… » | Un nombre de passages de 2 ou 3 a été donné, mais le robot ne déclare pas gérer la répétition | Videz le champ du nombre de passages : le nettoyage se fait alors en un seul passage |
| « Plage horaire invalide : indiquez un début et une fin au format HH:MM, entre 00:00 et 23:59. » (ne pas déranger, heures creuses) | Un des deux champs de « Définir la plage… » est vide, mal formé (22h00, 2200, 22:5) ou hors bornes (24:00, 22:60) | Saisissez les deux heures au format HH:MM (7:30 est accepté), entre 00:00 et 23:59, puis relancez |
| « Plage horaire invalide : le début et la fin … doivent être différents. » | Le début et la fin de la plage sont identiques | Choisissez deux heures différentes (une plage qui franchit minuit, comme 22:00 → 07:00, est acceptée) |
| « Le robot n'a renvoyé aucune plage … exploitable : définissez la plage… » | « Activer » (ne pas déranger ou heures creuses) n'a aucune plage enregistrée à réappliquer | Lancez « Définir la plage… » avec un début et une fin : cela active aussi la fonction |
| « Volume invalide : indiquez un nombre entier entre 0 et 100. » | La valeur est vide, décimale (50.5), négative ou supérieure à 100 | Indiquez un entier de 0 à 100 ; dans une expression de scénario, arrondissez avec `round(...)` |
| « Ce mode de vidage (ou de lavage) n'est pas disponible sur la station de ce robot : rafraîchissez son état avant de réessayer. » | Le code de mode demandé n'est pas connu pour cette station (liste périmée, ou code erroné dans un scénario) | Lancez « Rafraîchir », rechargez la page de l'équipement, puis choisissez un mode dans la liste de la commande |
| « Un ordre (ou un réglage) … vient d'être envoyé à ce robot : patientez quelques secondes avant d'en envoyer un autre. » (verrou enfant, ne pas déranger, heures creuses, volume, mode de vidage, mode de lavage) | Deux ordres du même type sur le même robot à moins de 5 secondes d'intervalle | Patientez au moins 5 secondes ; dans un scénario, intercalez une pause de 5 secondes entre les deux actions |
| « Le robot (ou la station) n'a pas appliqué … : l'état relu ne correspond pas à la demande. » (verrou enfant, ne pas déranger, heures creuses, volume, mode de vidage, mode de lavage) | Le robot répond mais n'a pas adopté le réglage au bout du délai de vérification (quelques secondes, jusqu'à une douzaine) | Contrôlez la valeur affichée par la commande d'information correspondante (elle montre ce que le robot a réellement adopté), relancez l'ordre ; si cela se répète, essayez robot au repos ou à sa base |
| « Cette opération d'entretien n'est pas disponible sur la station de ce robot » | La station de ce robot ne prend pas en charge cette action | C'est normal : la commande ne devrait pas apparaître si la station ne le permet pas ; rafraîchissez l'état du robot |
| « La liste des usages reçue du cloud Roborock est incomplète : par précaution, aucun usage n'a été supprimé. » | La réponse du cloud a été tronquée, ou ce robot a plus de 64 usages | Relancez la synchronisation plus tard ; rien n'a été perdu entre-temps |
| « Les conditions d'utilisation Roborock n'ont pas été acceptées » (ou « ont changé ») | Roborock demande de valider (ou revalider) ses conditions d'utilisation | Ouvrez l'application mobile Roborock, acceptez les conditions proposées, puis réessayez depuis Jeedom |
| « Robot inconnu du démon » | L'équipement Jeedom n'est plus reconnu par le démon (redémarrage, robot retiré du compte…) | Relancez « Synchroniser les équipements » |
| « Le cloud Roborock est injoignable » | Jeedom n'arrive pas à joindre les serveurs Roborock | Vérifiez l'accès à Internet du serveur Jeedom |
| Un message évoquant un **délai imparti** dépassé, une **connexion échouée** ou « plusieurs tentatives de communication ont échoué » | Le robot ou le cloud Roborock a mis trop de temps à répondre : incident réseau passager, ou robot très sollicité | Réessayez après une minute ; si cela se répète, vérifiez la connexion Wi-Fi du robot et l'accès à Internet du serveur Jeedom |
| « Le robot est occupé », « Le robot a refusé l'action dans son état actuel » ou « Le robot a signalé une erreur » | Le robot ne peut pas exécuter cette demande dans son état du moment (nettoyage en cours, bac plein, incident mécanique…) | Vérifiez l'état du robot (commande « État », ou application mobile), traitez l'incident signalé puis relancez l'action |
| « Cette fonction n'est pas disponible sur ce modèle de robot » ou « Le robot ne reconnaît pas cette commande » | Le robot n'implémente pas cette fonction, bien que la commande existe dans Jeedom | Aucune manipulation ne débloquera la situation : cette fonction n'existe pas sur ce matériel, masquez la commande si elle vous gêne |
| « Aucune demande de code en cours » | Le démon a redémarré entre l'envoi et la validation du code | Cliquez de nouveau sur « Envoyer un code », puis validez le nouveau code reçu |
| « … transmis au robot (application non confirmée). » après un réglage | Le plugin n'a pas pu vérifier que le robot a pris la valeur : un autre réglage a été envoyé juste après sur le même robot, ou le robot ne répondait plus pendant la vérification. Ce n'est pas une erreur | Contrôlez la valeur affichée par la commande d'information correspondante ; renvoyez le réglage si elle n'est pas la bonne |
| Un réglage (aspiration, débit d'eau, itinéraire, mode de nettoyage) n'est pas appliqué | Le robot n'a toujours pas pris la valeur une douzaine de secondes après l'avoir reçue : il refuse ce réglage dans son état actuel (en général : pas au repos) | Réessayez une fois le robot au repos ou à sa base |
| « Cette puissance d'aspiration / ce débit d'eau / cet itinéraire / ce mode de nettoyage n'est pas disponible sur ce robot » | La liste des paliers connue par Jeedom est périmée (le robot n'annonce plus cette valeur) | Rafraîchissez l'état du robot puis réessayez |
| « Vous n'avez pas le droit de piloter ce robot. » (panneau de pilotage et onglet Station et entretien), boutons grisés | Votre compte Jeedom n'a que le droit de lecture sur ce robot | Demandez à un administrateur de vous accorder le droit d'exécution sur ce robot (gestion des utilisateurs de Jeedom) |
| « Aucun robot Roborock accessible avec votre compte. » (ou « Équipement introuvable ou inaccessible. ») | Aucun robot activé sur lequel votre compte a le droit de lecture ; le même message sert aussi pour un robot inexistant ou désactivé | Demandez le droit de lecture à un administrateur, ou vérifiez que le robot est activé |
| « 401 - Accès non autorisé » à l'ouverture de la page Carte | Votre session Jeedom a expiré | Reconnectez-vous à Jeedom |
| L'entrée JeeRoborock n'apparaît pas dans Accueil | La case **Afficher le panneau desktop** est décochée dans la gestion du plugin | Cochez-la (voir « Panneau « Carte » (Accueil > JeeRoborock) ») |
| « Robot hors ligne : les commandes sont inactives jusqu'à son retour. » | Le robot ne répond pas au cloud Roborock | Vérifiez son alimentation et son Wi-Fi ; les boutons redeviennent actifs au retour du robot, sans rien recharger |
| « Fonction indisponible pour ce robot. » ou un bouton absent du panneau | Le robot ne gère pas ce réglage ou cette action | Normal : le panneau ne propose que ce que votre robot sait faire |
| « Ordre refusé par le robot. » (sans autre précision) | L'ordre a été refusé sans message plus précis | Vérifiez l'état du robot (bac, erreur, pas à la base), puis relancez |
| Le bouton principal reste inactif, onglet Pièce : « Aucune pièce disponible pour ce robot : synchronisez ses pièces depuis la page de l'équipement. » | Aucune pièce n'a encore été synchronisée | Cliquez sur « Resynchroniser les pièces » dans l'onglet Équipement |
| « Trop de pièces choisies : lancez le nettoyage en plusieurs fois. » | Le nombre de pièces par ordre est limité | Décochez des pièces, lancez en plusieurs fois |
| « Certaines pièces ne peuvent pas être choisies ici… » ou « Cette pièce ne peut pas être choisie ici… » | La pièce n'a pas de nom, son nom est en double ou contient une virgule | Renommez-la dans l'application Roborock, puis resynchronisez les pièces |
| « Pièce inconnue de la carte actuelle : resynchronisez les pièces depuis la page de l'équipement. » | Une pièce cochée n'existe plus sur la carte (redécoupage, changement d'étage) | Décochez-la, ou resynchronisez les pièces ; le bouton de lancement reste inactif tant qu'elle est cochée |
| « Carte ancienne : sélection impossible. » ou « La carte ne permet pas de délimiter les pièces : choisissez-les dans la liste. » | La carte affichée est une ancienne image, ou ne contient pas de contours de pièces | Choisissez les pièces dans la liste de l'onglet Pièce ; la carte se renouvelle pendant les nettoyages |
| « Carte indisponible : tracé de zone impossible. », « Zone trop petite : tracez un rectangle plus grand. » ou « La zone doit être entièrement sur la carte. » | Aucune carte exploitable, ou le rectangle est trop petit ou dépasse de la carte | Tracez un rectangle plus grand, entièrement sur la carte ; sans carte, nettoyez par pièce ou en Total |
| « Ce robot n'a pas de station. » (onglet Station et entretien) | Le robot n'a pas de station d'accueil | Normal : rien à faire |
| Boutons **Vider**, **Laver**, **Sécher** inactifs, mention « Opération en cours » | Une opération de station est en cours, ou un ordre vient d'être envoyé (au plus 2 minutes) | Patientez ; **Arrêter le séchage** n'est actif que pendant un séchage |
| « Incident de la station » ou « Un ou plusieurs consommables sont à changer. » | La station signale un incident, ou un consommable est à 10 % ou moins | Traitez l'incident ; remplacez la pièce puis utilisez **Réinitialiser** |
| « Aucune donnée ce jour-là. » ou « Déroulé indisponible pour le moment. » (frise) | Aucun état enregistré ce jour-là (plugin installé depuis moins longtemps, ou jour hors des 7 derniers) ; ou la lecture a échoué | Changez de jour ; pour l'indisponibilité, rechargez la page. Le message « Jour invalide ou hors de la période conservée. » signifie qu'un jour de plus de 7 jours a été demandé |
| Mobile : « Le panneau ne peut pas être chargé : revenez à l'accueil puis rouvrez-le. » ou « Le panneau de commandes ne peut pas être chargé. Rechargez la page. » | La liste des robots ou les scripts du panneau n'ont pas pu être chargés (réseau, session, ancienne version en cache) | Rouvrez le panneau ; au besoin, fermez complètement l'application Jeedom puis rouvrez-la |
| Mobile : « Non disponible sur mobile » | La page Station et entretien, le déroulé et le tableau des pièces détectées n'existent pas sur mobile | Normal : ouvrez la page Carte de Jeedom sur un ordinateur |
| « Pièce inconnue », « aucune pièce connue » ou « plusieurs pièces portent ce nom » | Le nom saisi ne correspond à aucune pièce détectée, aucune pièce n'a encore été synchronisée, ou le nom est ambigu | Resynchronisez les pièces depuis l'onglet Équipement, utilisez le nom exact de l'application Roborock, ou la commande dédiée à cette pièce plutôt que la commande générique |
| La commande « Pièce courante » reste sur « Pièce inconnue » | Les pièces n'ont jamais été synchronisées, ou la carte active a changé | Cliquez sur « Resynchroniser les pièces » dans l'onglet Équipement |
| « Ces coordonnées sortent des limites de la carte connue » | La zone ou le point saisi dépasse la carte actuellement connue du robot | Vérifiez les coordonnées dans le bloc « Zone et point » de l'onglet Équipement, ou rafraîchissez l'image de la carte |
| « Ce consommable n'est pas suivi pour ce robot » | La commande de réinitialisation a été utilisée avant que l'usure de ce consommable ait été remontée au moins une fois | Rafraîchissez l'état du robot avant de réinitialiser ce consommable |
| « Une synchronisation (ou une lecture) vient d'être effectuée, patientez » (usages, pièces ou programmations) | Une resynchronisation a déjà eu lieu il y a moins d'une minute | Patientez une minute avant de relancer la même resynchronisation |
| « Le journal vient d'être rafraîchi : patientez une minute avant de relancer. » | Le bouton « Rafraîchir le journal » a déjà été utilisé il y a moins d'une minute | Patientez une minute avant de recliquer |
| « La génération du rapport a échoué. » | La requête vers Jeedom n'a pas abouti : délai de 20 secondes dépassé, connexion interrompue ou erreur du serveur Jeedom (un démon arrêté, lui, donne un rapport partiel, pas cet échec) | Rechargez la page de configuration et réessayez ; si cela persiste, consultez le log `jeeroborock` (menu « Analyse » > « Logs ») |
| « … usage(s) n'ont pas pu être enregistrés dans Jeedom. Consultez le log du plugin. » (dans le compte rendu du panneau « Usages ») | Un usage particulier n'a pas pu être créé ou mis à jour côté Jeedom pendant la synchronisation, alors que le reste s'est déroulé normalement | Consultez le log `jeeroborock` (menu « Analyse » > « Logs ») pour identifier l'usage concerné, puis relancez une synchronisation |
| « 401 - Accès non autorisé » au clic sur « Générer un rapport de diagnostic » | Votre session Jeedom a expiré, ou votre compte n'a pas les droits administrateur | Reconnectez-vous à Jeedom avec un compte administrateur puis réessayez |
| « Diagnostic du démon indisponible : rapport partiel » | Le démon est démarré, mais n'a pas pu fournir la partie technique du rapport (incident ponctuel) | Le reste du rapport reste exploitable ; réessayez plus tard pour obtenir la section technique complète |

Pour tout autre message, le texte affiché par le plugin donne directement la cause et, le cas échéant,
le geste à faire — il n'est jamais nécessaire d'ouvrir les journaux techniques pour le comprendre.

## Mise à jour du plugin

Les fonctions de pilotage manuel (panneau, carte interactive, station, « aspirer puis laver », déroulé de
la journée, panneau mobile) ne demandent **aucune action de votre part** après la mise à jour : aucune
configuration à refaire, aucun équipement à recréer. Deux gestes peuvent toutefois être utiles :
redémarrer le démon (sinon les états apparaissent en « Autre état » sur la frise) et, sur mobile,
resynchroniser ou fermer complètement l'application.

## Limites connues

- Le plugin ne pilote que des robots compatibles avec le protocole V1 de Roborock, via le cloud. Les
  robots plus anciens (protocole A01) ne sont pas pris en charge.
- Les libellés produits par le robot lui-même (état, erreur, état de la station, noms de consommables)
  restent **toujours en français**, quelle que soit la langue choisie pour l'interface Jeedom. Il en va
  de même des valeurs « Aucune pièce » et « Pièce inconnue » de la commande « Pièce courante ».
- Un changement de carte fait depuis l'application mobile est désormais détecté automatiquement, en
  tâche de fond, dans la minute environ : la carte active, l'image et le repère de la carte se mettent
  à jour sans action de votre part (la liste des pièces, elle, est vidée et attend un clic sur
  « Resynchroniser les pièces »). Pendant ce court délai, la configuration peut encore afficher
  l'ancien étage, et une page Équipement déjà ouverte ne se rafraîchit pas seule : rechargez-la. De même,
  la commande « Pièce courante » peut brièvement (une minute au plus) désigner une pièce de l'ancien
  étage, puis passe à « Pièce inconnue » jusqu'à la resynchronisation des pièces.
- La connexion locale évoquée plus haut (« Ce que le plugin fait, et ce qu'il ne fait pas ») ne peut pas
  être désactivée depuis Jeedom.
- Le plugin affiche la version du **micrologiciel** du robot (onglet « Équipement », mise à jour à la
  synchronisation des équipements), mais ne signale pas qu'une mise à jour est disponible et ne la
  déclenche pas : la mise à jour du micrologiciel se fait depuis l'application mobile Roborock.
- Au-delà de **64 usages** enregistrés pour un même robot, la synchronisation des usages continue
  d'ajouter et de renommer, mais ne supprime plus automatiquement les usages disparus de l'application.
- L'image de la carte peut rester **illisible** quand le robot n'est joignable que par la connexion
  locale évoquée plus haut, sans passer par le canal MQTT du cloud (message « La carte du robot n'a
  pas pu être décodée »).
- Un robot éteint ou hors Wi-Fi qui se reconnecte redevient pilotable de lui-même, mais après un délai
  qui peut atteindre **6 minutes** (voir « Plusieurs robots sur le même compte ») : ce délai n'est pas
  réglable.
- Le refus d'un ordre de nettoyage pendant le vidage du bac ne vise que l'état « Vidage du bac à
  poussière » : les autres états de la station (lavage, séchage) ne déclenchent pas ce refus. Il ne vise ni
  les usages (routines), ni « Se déplacer vers un point ». Aucun ordre n'est mis en attente : c'est à
  vous (ou à votre scénario) de le renvoyer.
- La mise à jour automatique du dernier nettoyage est **bornée** : cinq relectures au plus, sur 30
  minutes après la fin du nettoyage. Au-delà, le plugin n'insiste plus ; utilisez « Rafraîchir le
  journal ».
- Un nom de carte déjà enregistré sous forme codée (avant la mise à jour du plugin) reste codé jusqu'au
  premier « Rafraîchir la liste des cartes » ou changement de carte.
- La lecture des noms de pièces (panneau « Pièces » de l'onglet Équipement) exige que le robot soit
  **en ligne** : elle échoue si le robot est injoignable au moment du clic.
- La vue carte (panneau « Accueil > JeeRoborock ») ne déclenche rien d'elle-même (un ordre ne part que
  sur votre clic dans le panneau de pilotage) et ne lance aucune mise à jour : elle se
  contente d'afficher, toutes les 30 secondes, la dernière image déjà connue. Cette image n'est
  reconstruite que pendant les nettoyages ; au repos, elle peut donc dater du dernier passage du
  robot.
- Panneau mobile : version **réduite** du panneau de pilotage. Ni la page Station et entretien, ni le
  déroulé de la journée, ni le tableau des pièces détectées ne sont disponibles sur mobile : ils ne le
  sont que sur ordinateur. L'onglet dédié du menu personnalisé de l'application Jeedom est réservé aux
  administrateurs. Le panneau n'a pas été éprouvé sur tous les téléphones : un appareil peut présenter
  des défauts d'affichage.
- **Zones interdites et murs virtuels** : affichés sur la carte en **lecture seule**. Pour en créer, les
  déplacer ou les supprimer, utilisez l'application Roborock ; le plugin ne bloque pas une zone tracée
  sur une zone interdite.
- **Robot hors ligne** : le panneau, la page Station et entretien et l'enchaînement « aspirer puis
  laver » n'acceptent aucun nouvel ordre. Seul **Annuler la séquence** reste possible pendant une
  séquence. Les derniers états et la dernière carte restent affichés.
- **Deux robots, deux séquences** : chaque robot a sa propre séquence « aspirer puis laver », suivie et
  annulée indépendamment de l'autre.
- **Station et entretien** : sur un robot **sans station**, l'onglet n'affiche que « Ce robot n'a pas de
  station. ». Sur un robot avec station, seules les actions et les états que ce robot sait faire
  apparaissent.
- **Déroulé de la journée** : la frise est reconstituée à partir des états que le **plugin a lui-même
  enregistrés** (rien n'est demandé au cloud Roborock). Elle ne contient aucune donnée antérieure à
  l'installation de la mise à jour. Seuls les **7 derniers jours** sont conservés ; les plus anciens sont
  supprimés. Au-delà d'un volume d'enregistrements très élevé pour une même journée, l'enregistrement de
  cette journée s'arrête : la fin de la frise de ce jour-là reste vide.
- Frise « Déroulé de la journée » : **« Hors ligne »** signifie que le robot **ne répond pas** ; un seul
  délai dépassé suffit, ce n'est pas forcément une coupure longue.
- Sur la frise, une **pause** en cours de nettoyage, le **déplacement vers une cible**, la
  **cartographie** et la **pose ou le retrait de la serpillère** apparaissent en **Autre état**. Le
  **séchage** qui a lieu pendant la charge apparaît **En charge** : « Séchage de la serpillère » ne
  couvre que le séchage signalé comme tel par le robot.
- Après une mise à jour du plugin, tant que le **démon n'a pas redémarré**, les états apparaissent en
  **Autre état** sur la frise. Redémarrez le démon.
- La précision d'**« Inconnu »** est de l'ordre de **quelques minutes** : le début peut précéder l'arrêt
  réel de quelques minutes. Une coupure de **moins de 15 minutes** sans redémarrage du démon n'apparaît
  pas.
- Seuls les **10 derniers nettoyages** du journal peuvent être surlignés sur la frise.
- Les commandes reprises par la tuile de tableau de bord (batterie, en nettoyage, erreur, connecté,
  en ligne et les cinq actions de pilotage) sont masquées une seule fois, à la création de la tuile.
  Si vous en réaffichez une manuellement, le plugin ne la re-masque jamais : votre choix est conservé.
- Sur une installation mise à jour depuis une version ancienne du plugin, une migration technique
  ponctuelle a pu réactiver l'historisation de la commande « Erreur » : si vous ne souhaitez pas
  historiser cette commande, désactivez-le manuellement sur sa configuration.
- Seul le **Roborock Qrevo Curv** est testé. Les capacités ajoutées par la parité avec Home Assistant
  (consommables et bacs de la station, verrou enfant, ne pas déranger, heures creuses, volume, modes de
  la station, nombre de passages, pièce courante) n'ont **aucune garantie** sur un autre modèle, le
  Roborock S7 compris : le plugin crée les commandes que le robot déclare ou auxquelles il répond, sans
  avoir pu vérifier leur effet réel sur chaque matériel. Un ordre accepté peut être refusé par le robot ;
  c'est alors signalé (voir Dépannage).
- L'usure du **sac à poussière** de la station est en lecture seule : le plugin n'a pas d'action pour la
  réinitialiser. Les pourcentages des consommables peuvent différer légèrement de ceux de l'application.
- Les réglages de l'appareil (verrou enfant, ne pas déranger, heures creuses, volume, modes de la
  station) ne sont **pas poussés** au plugin : un changement fait depuis l'application Roborock ou la
  touche du robot n'apparaît dans Jeedom qu'à la relecture suivante (environ une minute, ou « Rafraîchir »).
- Le plugin ne renvoie **jamais** un ordre de réglage tout seul après un refus ou un échec : relancez-le
  vous-même. Deux ordres du même type sur le même robot doivent être espacés d'au moins 5 secondes.
- « Désactiver » ne pas déranger ou les heures creuses conserve normalement la plage enregistrée, mais
  ce comportement dépend du robot et n'est pas confirmé.
- Le nombre de passages est un paramètre de chaque ordre de nettoyage par pièce ou par zone, jamais un
  réglage mémorisé. Pour une zone, la façon dont le robot interprète la valeur de répétition n'a pas pu
  être confirmée sur tous les modèles : si « 2 » ne donne pas deux passages sur votre robot, signalez-le.
  Les boutons « Nettoyer <pièce> » restent à un seul passage.
- Les listes de modes de vidage et de lavage viennent de la bibliothèque utilisée par le plugin, pas de
  la station : un mode de l'application Roborock peut manquer, un mode proposé peut être refusé par la
  station. Un code de mode inconnu s'affiche « Mode inconnu (N) ».
- La commande « Pièce courante » dépend de la dernière image de carte lue : elle peut avoir un retard
  d'une minute environ au repos, et garde sa dernière valeur si le robot est hors ligne. Après un
  changement de carte fait depuis l'application, elle peut brièvement désigner une pièce de l'ancien
  étage avant de passer à « Pièce inconnue » (voir plus haut).

- **Aspirer puis laver** : si vous modifiez un réglage du robot (aspiration, débit d'eau, itinéraire) pendant
  une séquence, le rétablissement de fin l'**écrase**. Si le plugin cesse de suivre la séquence
  (« Séquence abandonnée », redémarrage du démon) ou si le compte est changé, les réglages d'origine ne
  sont **pas rétablis** : vérifiez-les. Un nettoyage lancé depuis l'**application mobile** pendant un
  passage n'est pas refusé par le plugin : il est constaté après coup et la séquence s'arrête sans
  lancer le second passage. Si le robot ne signale pas l'état de nettoyage, une fin de passage peut ne
  pas être détectée : la séquence s'arrête alors à 6 heures. Un mode d'origine personnalisé ou
  « intelligent » est rétabli sur le réglage standard le plus proche.

Cette page est mise à jour à chaque nouvelle fonctionnalité livrée par le plugin.
