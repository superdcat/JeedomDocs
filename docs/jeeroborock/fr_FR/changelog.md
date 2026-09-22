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
  modèle.
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
- Routines (« usages ») définies dans l'application mobile : une commande d'action par usage.
- Réglages : puissance d'aspiration, débit d'eau, itinéraire de serpillère, mode de nettoyage.
- Entretien à la station : laver la serpillière, la sécher, arrêter le séchage, vider le bac.
- Nettoyage par pièce (une commande par pièce, plus une commande générique par noms), nettoyage
  d'une zone rectangulaire et déplacement vers un point.
- Réinitialisation du compteur d'usure de chaque consommable, avec confirmation.

**Carte**

- Inventaire des pièces nommées et des cartes mémorisées (étages), changement de carte active,
  depuis l'onglet Équipement.
- Panneau « Carte » (menu **Accueil**) accessible aux utilisateurs non administrateurs :
  image de la carte, date de la dernière mise à jour, légende des pièces, rafraîchissement
  automatique.

## Ce qui n'est pas encore disponible

Journal des nettoyages, statistiques cumulées, lecture des programmations, transport local (sans
passer par le cloud), page de diagnostic, mise à jour du firmware, et documentation utilisateur
détaillée.

# 22/09/2026

- Évolution : sur la page de configuration du plugin, le code de connexion se saisit maintenant juste sous l'adresse e-mail, avant l'état du compte, dans l'ordre où la procédure se déroule. <!-- UC04 -->
- Évolution : un rappel indique qu'il faut enregistrer la configuration après avoir saisi l'e-mail, avant de demander un code. <!-- UC04 -->
- Documentation : page d'aide complète du plugin — installation, liaison du compte Roborock par code e-mail, équipements et commandes, usages, tuile de tableau de bord, carte et pièces, pilotage fin, temps réel, ré-authentification, quotas Roborock et guide de dépannage. <!-- UC49 -->

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
