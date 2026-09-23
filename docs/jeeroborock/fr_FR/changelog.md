# Changelog JeeRoborock

>**IMPORTANT**
>
>S'il n'y a pas d'information sur la mise à jour, c'est que celle-ci concerne uniquement de la mise à jour de documentation, de traduction ou de texte.

Le plugin est en version **0.x**. Il est développé et recetté sur un **Roborock Qrevo Curv**
(protocole V1) : les fonctionnalités ci-dessous sont opérationnelles sur ce matériel, et devraient
l'être sur les autres robots V1 du compte, chaque commande n'étant créée que si le robot déclare la
capacité correspondante.

Le plugin respecte les **quotas du cloud Roborock**, partagés avec l'application mobile : la
découverte des robots et les synchronisations (usages, pièces, cartes) se font **à la demande**, et
aucune tentative de connexion n'est rejouée automatiquement.

## Ce qui est fonctionnel

**Compte et installation**

- Installation de la dépendance `python-roborock` et démon dédié, avec surveillance de son état.
- Authentification au cloud Roborock par **code à usage unique reçu par e-mail** : aucun mot de
  passe n'est demandé ni stocké.
- Bouton « Tester la connexion », état du compte affiché sur la page de configuration, et message
  explicite « ré-authentification requise » quand la session est perdue.

**Équipements et états**

- Découverte des robots du compte et création d'un équipement par robot, illustré par la photo du
  modèle. Un robot ne correspond jamais qu'à un seul équipement Jeedom : toute tentative de
  duplication est refusée avec un message explicite.
- Informations remontées : état, batterie, en nettoyage, erreur (libellé et code), surface
  nettoyée, durée de nettoyage, avancement, en ligne, connecté, dernière mise à jour.
- Station d'accueil : vidage poussière, lavage serpillière, séchage serpillière, erreur station,
  manque d'eau.
- Consommables : usure restante en % pour la brosse principale, la brosse latérale, le filtre, les
  capteurs et le rouleau de serpillière.
- Réglages courants en lecture : puissance d'aspiration, débit d'eau, itinéraire de serpillère,
  mode de nettoyage.
- Mise à jour **en temps réel** par le démon (30 s en nettoyage, 60 s au repos), et bascule en
  « déconnecté » si la donnée vieillit.
- Tuile de tableau de bord (desktop et mobile) réunissant photo, état, batterie et actions de
  pilotage.

**Pilotage**

- Actions de base : Démarrer, Mettre en pause, Arrêter, Retour à la base, Localiser, Rafraîchir.
- Routines (« usages ») définies dans l'application mobile : une commande d'action par usage,
  gérées depuis le panneau « Usages » de l'onglet Équipement (liste des usages connus,
  synchronisation à la demande).
- Réglages : puissance d'aspiration, débit d'eau, itinéraire de serpillère, mode de nettoyage.
- Entretien à la station : laver la serpillière, la sécher, arrêter le séchage, vider le bac.
- Nettoyage par pièce (une commande par pièce, plus une commande générique par noms), nettoyage
  d'une zone rectangulaire et déplacement vers un point.
- Réinitialisation du compteur d'usure de chaque consommable, avec confirmation.

**Carte**

- Inventaire des pièces nommées et des cartes mémorisées (étages), changement de carte active,
  depuis l'onglet Équipement. Un changement d'étage fait depuis l'application mobile est aussi
  suivi automatiquement, sans action de votre part.
- Panneau « Carte » (menu **Accueil**) accessible aux utilisateurs non administrateurs :
  image de la carte, date de la dernière mise à jour, légende des pièces, rafraîchissement
  automatique.

**Journal, statistiques et programmations**

- Dernier nettoyage (début, durée, surface, motif de fin, erreur) et panneau d'historique des
  10 derniers nettoyages, avec bouton de rafraîchissement.
- Quatre compteurs cumulés historisés par défaut : durée totale, surface totale, nombre de
  nettoyages, nombre de vidages du bac.
- Programmations créées dans l'application mobile, consultables en lecture seule depuis l'onglet
  Équipement.

**Documentation**

- Page d'aide complète du plugin : installation, liaison du compte, équipements et commandes,
  usages, carte, pilotage fin, ré-authentification, quotas et guide de dépannage.
  Disponible en français, anglais, allemand et espagnol.

**Diagnostic et support**

- Rapport de diagnostic généré en un clic depuis la configuration du plugin, sans aucune donnée
  sensible, à copier ou télécharger pour une demande d'assistance.

## Ce qui n'est pas prévu

Le plugin n'affiche pas le canal utilisé pour joindre chaque robot (connexion locale ou cloud), et
ne suit ni ne met à jour le micrologiciel : ces deux fonctions ont été écartées. La mise à jour du
micrologiciel se fait depuis l'application Roborock.

# 23/09/2026

- Correctif : le bouton « Démarrer » reprend désormais un nettoyage mis en pause au lieu de relancer un cycle complet, y compris pour un nettoyage par pièce ou par zone.
- Correctif : une session Roborock expirée est désormais reconnue aussi lors de la synchronisation des usages, de leur exécution, de la lecture des pièces et du test de connexion : le plugin affiche « ré-authentification requise » au lieu d'une erreur générique. <!-- UC36 -->
- Ajout : nouveau rapport de diagnostic dans la configuration du plugin : état du démon, du compte et des robots, version de python-roborock et erreurs récentes, sans aucun identifiant, jeton, numéro de série ni adresse e-mail, à copier ou télécharger en un clic. <!-- UC30 -->
- Documentation : la documentation du plugin explique comment générer et transmettre un rapport de diagnostic pour une demande d'assistance. <!-- UC30 -->
- Documentation : la documentation précise que le plugin reste dépendant du cloud Roborock même quand une connexion locale au robot est tentée, indique ce qu'il faut joindre à une demande d'aide et ce qu'il ne faut jamais publier, et complète le guide de dépannage du rapport de diagnostic. <!-- UC59 -->
- Évolution : les usages ont leur panneau « Usages » dans l'onglet Équipement du robot : liste des usages connus, bouton de synchronisation et règle affichée avant le clic ; un usage supprimé dans l'application Roborock est désormais supprimé de Jeedom au lieu d'être marqué obsolète, et le compte rendu le nomme. <!-- UC35 -->
- Correctif : un nom d'usage personnalisé dans Jeedom n'est plus écrasé par le nom de l'application Roborock à la deuxième synchronisation. <!-- UC35 -->
- Documentation : section des usages réécrite (panneau « Usages », règle de synchronisation, cas où rien n'est supprimé). <!-- UC35 -->
- Documentation des usages complétée : quand lancer leur synchronisation, ce qu'elle coûte (aucun quota), ce qui se passe en cas d'échec, et rappel que le bouton de synchronisation des équipements ne synchronise pas les usages. <!-- UC89 -->
- Correctif : un changement d'étage fait depuis l'application mobile Roborock est désormais détecté par Jeedom dans la minute : la carte active est mise à jour, et la liste des pièces, l'image et le repère de coordonnées de l'ancien étage sont invalidés comme lors d'un changement fait depuis Jeedom. <!-- UC38 -->
- Documentation : la documentation décrit le suivi automatique d'un changement d'étage fait depuis l'application mobile et ses limites restantes. <!-- UC38 -->
- Correctif : le nom d'une commande de pièce contenant une apostrophe, une esperluette, un dièse ou un pourcentage suit désormais les renommages faits dans l'application Roborock, tout en conservant un nom personnalisé dans Jeedom. <!-- UC39 -->
- Correctif : un robot ne peut plus être associé à deux équipements Jeedom : le bouton « Dupliquer » est retiré et toute tentative est refusée avec un message qui nomme l'équipement existant. <!-- UC39 -->
- Correctif : les noms longs et accentués de pièces, d'usages, de cartes et de robots ne sont plus coupés au milieu d'un caractère. <!-- UC39 -->
- Documentation : la documentation précise qu'un robot correspond à un seul équipement Jeedom et que le nom des commandes de pièce suit les renommages faits dans l'application. <!-- UC39 -->
- Correctif : l'indicateur « En ligne » suit désormais réellement la perte et le retour de connexion du robot, une erreur de station inconnue s'affiche comme « Erreur de station non reconnue » au lieu de « Aucune », et les champs non poussés par le robot (station, surface, avancement) ne restent plus figés quand le robot envoie beaucoup de mises à jour. <!-- UC40 -->
- Documentation : la documentation distingue désormais les indicateurs « En ligne » et « Connecté » et mentionne le libellé « Erreur de station non reconnue ». <!-- UC40 -->
- Évolution : durcissement interne : le plugin refuse une mise à jour anormalement volumineuse venant de son démon, le fichier source du formulaire de configuration n'est plus accessible par le web, le démon signale au démarrage une version non validée de la bibliothèque de rendu de carte ou un journal non bridé de la bibliothèque Roborock, et la fenêtre d'exemple héritée du modèle de plugin est retirée. <!-- UC41 -->
- Correctif : deux clics rapprochés (ou deux onglets) sur un même bouton de synchronisation — usages, pièces, cartes, image de carte, journal, programmations — ne passent plus tous les deux : le second est refusé avec le message habituel de demande trop rapprochée. <!-- UC42 -->
- Documentation : les limites connues sont complétées (carte illisible en connexion locale seule, pièces lisibles uniquement robot en ligne, vue carte non rafraîchie au repos, pas de vue carte sur mobile, commandes de la tuile réaffichées jamais re-masquées, historisation de l'erreur réactivée après une ancienne mise à jour), le dépannage couvre l'échec partiel d'une synchronisation d'usages, et le résumé des fonctionnalités cite le panneau « Usages » et le suivi d'un changement d'étage fait sur mobile. <!-- UC99 -->
- Documentation : la page d'aide et le changelog sont désormais disponibles en anglais, en allemand et en espagnol. <!-- UC99 -->
- Correctif : tuile du robot : la mention d'un consommable à remplacer indique désormais lequel (brosse principale, filtre, capteurs…). <!-- UC15 -->

# 22/09/2026

- Évolution : sur la page de configuration du plugin, le code de connexion se saisit maintenant juste sous l'adresse e-mail, avant l'état du compte, dans l'ordre où la procédure se déroule. <!-- UC04 -->
- Évolution : un rappel indique qu'il faut enregistrer la configuration après avoir saisi l'e-mail, avant de demander un code. <!-- UC04 -->
- Documentation : page d'aide complète du plugin — installation, liaison du compte Roborock par code e-mail, équipements et commandes, usages, tuile de tableau de bord, carte et pièces, pilotage fin, temps réel, ré-authentification, quotas Roborock et guide de dépannage. <!-- UC49 -->
- Ajout : le dernier nettoyage (début, durée, surface, motif de fin et erreur éventuelle) est désormais remonté sur l'équipement, avec un historique des 10 derniers nettoyages consultable depuis la page du robot et un bouton pour le rafraîchir. <!-- UC26 -->
- Documentation : la documentation du plugin décrit le journal des nettoyages : les informations remontées, le panneau d'historique et la règle du bouton de rafraîchissement. <!-- UC26 -->
- Ajout : quatre statistiques cumulées par robot (durée totale de nettoyage, surface totale nettoyée, nombre de nettoyages, nombre de vidages du bac), historisées par défaut pour en suivre l'évolution dans le temps. <!-- UC27 -->
- Documentation : la documentation du plugin décrit les statistiques cumulées : les quatre compteurs, leur historisation par défaut et le comportement après une remise à zéro depuis l'application Roborock. <!-- UC27 -->
- Ajout : les programmations de nettoyage définies dans l'application Roborock sont consultables depuis Jeedom, en lecture seule : récurrence et état actif ou inactif de chacune. <!-- UC28 -->
- Documentation : le guide de dépannage de la page d'aide couvre désormais tous les messages qui demandent une action de votre part : compte non lié, adresse e-mail rejetée, délai dépassé, robot occupé, réglage indisponible sur le robot et changement de carte trop rapproché. <!-- UC49 -->

# 21/09/2026

**Documentation**

- La documentation et le changelog sont publiés sur
  [jeedomdocs.decastro.fr/jeeroborock](https://jeedomdocs.decastro.fr/jeeroborock/).
- Changelog unique pour toutes les versions : le changelog « beta » est supprimé.

**Carte et pièces**

- Inventaire des **pièces nommées** du compte, avec correspondance vers les segments du robot,
  dans un panneau « Pièces » de l'onglet Équipement.
- **Cartes multiples (étages)** : liste des cartes mémorisées, carte active et changement de
  carte. Un changement de carte invalide la liste des pièces et l'image, qui sont resynchronisées.
- **Image de la carte** récupérée et rafraîchie automatiquement par le démon.
- Nouveau panneau **« Carte »** (menu Accueil), première surface du plugin accessible aux
  utilisateurs non administrateurs : image de la carte, horodatage, légende des pièces et
  rafraîchissement toutes les 30 secondes. L'image n'est plus servie par URL directe : chaque
  accès vérifie les droits de l'utilisateur sur l'équipement.

**Pilotage fin**

- **Puissance d'aspiration** : information et commande de réglage, limitée aux paliers réellement
  supportés par le robot.
- **Débit d'eau** de la serpillière : information et commande de réglage.
- **Itinéraire de serpillère** et **mode de nettoyage** (aspiration seule, lavage seul, aspiration
  et lavage) : informations et commandes de réglage.
- **Entretien à la station** : « Laver la serpillière », « Sécher la serpillière », « Arrêter le
  séchage », « Vider le bac ». Ces actions ne sont créées que si la station le permet, et sont
  refusées avec un message clair si le robot n'est pas à sa base.
- **Nettoyage par pièce** : une commande par pièce du logement, plus une commande générique
  « Nettoyer des pièces (noms séparés par des virgules) ». Les commandes suivent le renommage des
  pièces dans l'application mobile.
- **Nettoyage d'une zone** (x1,y1,x2,y2 en mm) et **déplacement vers un point** (x,y en mm), avec
  validation des coordonnées avant envoi au robot.

**Identité visuelle**

- Icône du plugin dérivée du logo Roborock.

# 20/09/2026

- **Erreurs détaillées** : libellé d'erreur en français, code associé, valeur « Aucune » quand le
  robot ne signale rien, et historisation de l'erreur. Une erreur que la librairie ne connaît pas
  n'est plus présentée comme « aucune erreur ».
- **Tuile de tableau de bord** du robot (desktop et mobile) : photo, état, jauge de batterie et
  les cinq actions de pilotage, sans aucun appel au cloud à l'affichage. Les commandes reprises
  par la tuile sont masquées mais restent exécutables par les scénarios, vues et designs.
- **Photo du robot** en illustration de l'équipement (liste des équipements et page de
  configuration).
- Corrections sur la remontée des événements.

# 19/09/2026

- **Temps réel** : le démon porte la cadence de rafraîchissement (30 s en nettoyage, 60 s au
  repos) et reçoit les mises à jour poussées par le robot. Le cron Jeedom devient un chien de
  garde de fraîcheur et bascule le robot en « déconnecté » au-delà de 3 minutes sans donnée.
- **Robustesse et ré-authentification** : état « ré-authentification requise » explicite et
  persistant, temporisations progressives sur les sondes et sur la relance du démon, et
  durcissement de la journalisation (aucun secret dans les logs, quel que soit le niveau).
- **Consommables** : usure restante en % pour les cinq consommables réellement remontés par le
  robot, et une action de réinitialisation par consommable.
- **État de la station d'accueil** : vidage poussière, lavage serpillière, séchage serpillière,
  erreur station et code associé, manque d'eau. Ces informations ne sont créées que si la station
  les expose.
- Corrections du démon : démarrage, envoi du code par e-mail, ajout d'un équipement.

# 18/09/2026

- **Pont PHP vers le démon** : canal local unique, avec traduction en français des codes d'erreur
  du démon.
- **Authentification** au cloud Roborock par code à usage unique reçu par e-mail.
- Bouton **« Tester la connexion »** et affichage de l'état du compte sur la page de configuration
  du plugin.
- **Découverte des robots** du compte et création d'un équipement par robot.
- **Commandes d'information** : état, batterie, en nettoyage, erreur, surface nettoyée, durée de
  nettoyage, avancement, en ligne, connecté, dernière mise à jour.
- **Commandes d'action** : Démarrer, Mettre en pause, Arrêter, Retour à la base, Localiser,
  Rafraîchir.
- **Routines (« usages »)** : synchronisation des usages définis dans l'application mobile et une
  commande d'action par usage. Elles passent par le cloud Roborock, donc fonctionnent même quand
  le robot n'est pas joignable en direct.

# 17/09/2026

- Première version : page de configuration du plugin (e-mail du compte Roborock, port du canal
  local du démon), installation de la dépendance `python-roborock` et cycle de vie du démon.
