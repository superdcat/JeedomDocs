# Changelog — Stellantis Cars

> **IMPORTANT**
>
> S'il n'y a pas d'information sur une mise à jour, c'est qu'elle ne concerne que de la documentation,
> de la traduction ou du texte.

> ⚠️ Le plugin est en **développement actif** et s'appuie sur une **API non officielle** (celle des
> applications mobiles MyPeugeot / MyCitroën / MyDS / MyOpel / MyVauxhall). Consultez l'avertissement
> en tête de la documentation avant utilisation.

# 22/09/2026

- **Renommage du plugin** : « Stellantis » devient **« Stellantis Cars »**, et son identifiant technique
  `stellantis` devient `stellantiscars`.
  ⚠️ **Changement cassant** : Jeedom considère qu'il s'agit d'un plugin **différent** (nouveau dossier,
  nouvelle configuration, nouveaux équipements). L'ancienne installation doit être supprimée et le
  plugin reconfiguré.
- **Migration facilitée** : un fichier de sauvegarde de la configuration d'authentification exporté
  sous l'ancien nom est désormais **accepté à la restauration**. Vous récupérez vos identifiants, votre
  activation OTP et vos jetons **sans consommer de nouveau SMS** (le quota de 20 activations par compte
  est définitif). Pensez à exporter votre configuration **avant** de supprimer l'ancienne installation.
- Liens de documentation et de changelog mis à jour ; les versions stable et bêta pointent désormais
  vers la même documentation.

# 21/09/2026

- **Temps de charge restant lisible** : nouvelle information « Temps restant » affichant « 5 h 55 » ou
  « 45 min », à côté de la durée en minutes déjà existante (véhicules rechargeables uniquement).
- **Batterie 12 V — correction d'unité** : la valeur est exposée en **%** et non plus en `V`. Le champ
  remonté par l'API est un **pourcentage de charge**, pas une tension.
  ⚠️ Un scénario qui comparait cette valeur à un seuil exprimé en volts (par exemple `< 12`) comparait
  déjà un pourcentage : il est à revoir. L'historique existant est simplement ré-étiqueté, rien n'est
  perdu. Un rafraîchissement de la page (F5) peut être nécessaire pour voir la nouvelle unité.
- **Alarme et température extérieure** : deux nouvelles informations, « Température extérieure » (°C,
  historisée) et « Alarme » (état de l'antivol du véhicule, quand le véhicule le remonte).
- Publication automatique de la documentation vers le site de documentation.

# 21/07/2026

- **Sauvegarde et restauration de la configuration d'authentification** : un nouveau bloc de la page de
  configuration permet d'exporter dans un **fichier chiffré** (AES-256-GCM, protégé par une phrase
  secrète de 12 caractères minimum) les identifiants OAuth de chaque compte, l'activation OTP, le
  numéro client et les paramètres du broker, puis de les restaurer sur une installation neuve **sans
  reconsommer de SMS d'activation**. Un fichier corrompu, forgé ou ouvert avec la mauvaise phrase
  secrète est refusé **sans aucune écriture**.
- Corrections : résolution du numéro client (CID) pour le pilotage à distance, statistiques d'appels,
  affichage du nom de marque, enregistrement des cases à cocher du formulaire véhicule.

# 20/07/2026

- Correction de l'authentification OAuth2.

# 18/07/2026

- **Internationalisation complète** : plugin entièrement traduit en **anglais, allemand et espagnol**
  (interface, messages, page Santé), description du plugin fournie dans les 4 langues.

# 17/07/2026

- **Statistiques d'usage de l'API** : nouvelle page « Statistiques d'usage » (bouton sur la page du
  plugin) et ligne dédiée en page Santé — nombre d'appels REST du jour, total sur 7 jours, détail par
  point d'entrée et ventilation par compte. Une alerte est journalisée en cas de dérive anormale.
- **Synchronisation sélective par véhicule** : nouvelle case « Inclure dans le rafraîchissement auto »
  (cochée par défaut). Un véhicule décoché reste visible avec ses dernières valeurs mais n'est plus
  interrogé automatiquement. Un véhicule disparu du compte est **désactivé** (jamais supprimé) et
  **réactivé automatiquement** s'il réapparaît ; une désactivation manuelle est toujours respectée.
- **Documentation utilisateur complétée** : avertissement sur l'API non officielle, procédure
  d'activation du pilotage à distance (OTP), comptes secondaires, limites et bonnes pratiques.
- **Recette fonctionnelle** : checklist de validation manuelle couvrant l'ensemble des fonctions.
- Correction de l'icône du plugin.

# 16/07/2026

- **Mode « privacy » du véhicule** : quand le partage de données est coupé côté voiture, le plugin le
  détecte, l'explique par un message dédié (ce n'est pas une panne), expose une information
  « Mode privacy » utilisable en scénario, et **réduit sa cadence d'interrogation** à ~30 minutes pour
  économiser le quota d'appels — tout en continuant à détecter la sortie du mode.
- **Alertes de renouvellement de jeton** : une session expirée ou révoquée déclenche désormais un
  message Jeedom explicite (en plus du bandeau et de la page Santé), sans boucle d'appels.
- **Protection de la batterie 12 V — réveil automatique adaptatif** (option, désactivée par défaut) :
  le plugin peut réveiller le véhicule à une cadence **adaptée à son état** (en roulage : jamais ; en
  charge : 5 min par défaut ; au repos : 60 min par défaut), dans le strict respect des garde-fous
  anti-blocage existants. ⚠️ Fonction à activer en connaissance de cause (risque de décharge de la
  batterie 12 V) ; elle n'est disponible que sur le compte principal.

# 15/07/2026

- **Multi-marques et multi-comptes (lecture seule)** : jusqu'à **3 comptes** peuvent être rattachés à la
  même installation, chacun avec sa marque. Le **compte principal** conserve le pilotage à distance ;
  les comptes secondaires sont en **lecture seule**. Un blocage ou une panne d'authentification sur un
  compte n'affecte plus les autres.
- **Page Santé complétée** : lien vers la documentation, état du démon, et dernier résultat de commande
  par véhicule.
- **Protection anti-blocage renforcée** : les véhicules ne sont plus tous interrogés à la même minute
  (répartition automatique), et tout blocage temporaire du compte (HTTP 429) génère désormais une
  **alerte visible**.
- **Image du véhicule** : chaque équipement reçoit une vignette — photo du modèle quand l'API la
  fournit, sinon badge de la marque. Une image posée manuellement n'est jamais écrasée.

# 14/07/2026

- **Identité du véhicule** : le libellé du véhicule (le surnom défini dans l'application mobile) est
  affiché en configuration et exposé comme information.
- **Alertes véhicule** : nouvelle information « Nombre d'alertes » (historisée, idéale comme
  déclencheur de scénario) et **une information par type d'alerte rencontré** (AdBlue, lave-glace,
  voyants, révision…), créées automatiquement au fil de l'eau.
- **Ouvrants détaillés** : état de chaque ouvrant (portes avant/arrière, coffre, lunette, toit ouvrant,
  capot) et agrégat « Un ouvrant est ouvert » utilisable en scénario.

# 13/07/2026

- **Alerte de pression des pneus** : nouvelle information « Alerte pneus ». ⚠️ L'API grand public ne
  fournit **aucune valeur numérique de pression** (ni en bar, ni par roue) : seul un état d'alerte est
  disponible.

# 12/07/2026

- **Kilométrage et entretien** : distance et délai avant la prochaine révision, plus une information
  « Révision proche » utilisable en scénario, avec des **seuils d'alerte réglables par véhicule**
  (1000 km / 30 jours par défaut). Fonction disponible selon le forfait du véhicule.
- **Zone domicile (geofencing)** : une zone domicile unique (latitude, longitude, rayon) se règle dans
  la configuration du plugin et produit, par véhicule, les informations « À la maison » (déclencheur de
  scénario) et « Distance du domicile ». Les coordonnées du domicile sont **stockées chiffrées**.
- **Historique des trajets** : les trajets sont reconstruits localement (départ, arrivée, distance,
  durée, positions) — les points d'entrée « trajets » de l'API n'étant plus accessibles.
- **Panneau carte « Mes véhicules »** : nouvelle page au menu d'accueil affichant la position de chaque
  véhicule sur une carte, plus un **widget carte** sur le tableau de bord. Les coordonnées, la fraîcheur
  et un lien OpenStreetMap restent affichés même si la tuile n'est pas disponible.

# 11/07/2026

- **Position GPS détaillée** : latitude, longitude, cap, qualité du signal et horodatage propre à la
  position, en complément de la position « lat,lon ».
- **Suivi et statistiques de charge** : à la fin de chaque session de charge, énergie estimée (kWh),
  durée et coût estimé. Deux réglages par véhicule ont été ajoutés : **capacité de la batterie** (kWh)
  et **tarif du kWh** (€).
- **Carburant et véhicules hybrides** : l'autonomie est désormais **séparée par énergie** — « Autonomie
  électrique », « Autonomie carburant » et « Autonomie totale » (hybrides).
  ⚠️ Sur un véhicule **thermique** déjà découvert, l'ancienne information « Autonomie » est masquée au
  profit de « Autonomie carburant » (aucune donnée n'est supprimée).
- **Programmation de la charge** : nouvelle commande permettant de fixer l'heure de charge différée
  (saisie au format `HHMM`, par exemple `2030`). ⚠️ Programmer une heure **interrompt une charge
  immédiate en cours**. Le réglage d'un seuil de charge en % n'est pas proposé : l'API grand public ne
  le permet pas.
- **Détail batterie et charge** : vitesse de charge (km/h), temps restant, mode de charge, prochaine
  heure de charge programmée et batterie 12 V.
- **Résilience de la connexion du démon MQTT** : reconnexion avec temporisation progressive, arrêt des
  tentatives après 5 échecs d'authentification consécutifs (le démon reste vivant et se réarme tout
  seul), et remontée de l'état de connexion en page Santé.

# 10/07/2026

- **Retour d'état des commandes à distance** : chaque commande envoyée produit un résultat lisible
  (« Acceptée », « Réussie », « Véhicule en veille », « Échec »…) dans une information
  « Dernier résultat de commande », visible aussi en page Santé. Un échec n'est jamais silencieux.
- **Klaxon et feux** : deux nouvelles commandes pour retrouver son véhicule.

# 09/07/2026

- **Activation du pilotage à distance (OTP)** : procédure en deux étapes depuis la page de configuration
  (envoi d'un SMS, puis saisie du code reçu et du code PIN de l'application mobile), avec garde-fous sur
  les quotas stricts imposés par le constructeur (6 codes par 24 h, 20 activations SMS par compte à
  vie). Le jeton distant se renouvelle ensuite **sans nouveau SMS**.
- **Réveil / rafraîchissement à la demande** : commande « Réveiller », strictement encadrée pour
  préserver la batterie 12 V (5 minutes minimum entre deux réveils d'un même véhicule, plafond global
  par compte). Les informations sont rafraîchies dès l'acquittement.
- **Charge** : commandes « Démarrer la charge » et « Arrêter la charge » (véhicules rechargeables).
- **Préconditionnement climatique** : commandes « Activer » et « Désactiver » (tous véhicules, y compris
  thermiques — chauffage de l'habitacle).
- **Verrouillage / déverrouillage des portes** : le **déverrouillage demande une confirmation** avant
  exécution, pour éviter toute fausse manipulation.

# 08/07/2026

- **Démon MQTT** : socle de communication temps réel avec le constructeur, nécessaire au pilotage à
  distance (dépendance Python `paho-mqtt`).
- **Extraction automatique des identifiants** : un bouton de la page de configuration récupère
  automatiquement le `Client ID` et le `Client Secret` depuis l'application mobile de votre marque —
  plus besoin d'outil externe. L'extraction manuelle reste possible en secours.
- **Robustesse** : temporisation anti-blocage sur dépassement de quota (HTTP 429), rejeu borné du jeton,
  mode dégradé explicite quand l'authentification est cassée.
- **État de connexion et fraîcheur** : bandeau d'état sur la page du plugin, page Santé dédiée, et
  indicateur de mode privacy par véhicule.
- Icône du plugin.

# 07/07/2026

- **Rafraîchissement périodique** : interrogation automatique toutes les 5 minutes par défaut, avec une
  cadence personnalisable par véhicule.
- **Télémétrie** : batterie/SOC, état et statut de charge, autonomie, niveau de carburant, position GPS,
  kilométrage, état des portes et du verrouillage.
- **Création automatique des équipements** : un équipement Jeedom par véhicule du compte, avec
  synchronisation.

# 06/07/2026

- **Découverte des véhicules** du compte.
- **Test de connexion** depuis la page de configuration.
- **Authentification OAuth2** (Authorization Code + PKCE) et gestion automatique du jeton d'accès.
- **Client HTTP** vers l'API grand public.
- **Configuration du plugin** : marque, identifiants, pays.

# 25/06/2026

- Initialisation du plugin.
