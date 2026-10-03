# Changelog plugin Tesla BLE

>**IMPORTANT**
>
>S'il n'y a pas d'information sur la mise à jour, c'est que celle-ci concerne uniquement de la mise à jour de documentation, de traduction ou de texte.

# 03/10/2026

- Documentation : choix et installation du Raspberry Pi, rôle de la clé (Charging Manager ou Owner), sécurité réseau du proxy et limitations connues de la version 0.1
- Évolution : le plugin requiert désormais Jeedom 4.5, Debian 11 ou 12 et TeslaBleHttpProxy 2.3.0 minimum : Jeedom 4.4 et Debian 10 ne sont plus pris en charge <!-- UC802 -->
- Correctif : sous PHP 8, une URL de proxy vide ou un VIN manquant n'interrompt plus le rafraîchissement des véhicules : l'anomalie est signalée dans le log du plugin <!-- UC802 -->
- Évolution : nettoyage interne du code du plugin, sans changement de fonctionnement : équipements, commandes et scénarios existants restent inchangés <!-- UC803 -->
- Évolution : lors des mises à jour du plugin, les équipements existants sont désormais mis à niveau automatiquement, une seule fois par évolution et sans toucher à vos réglages ; le niveau atteint est indiqué dans le log du plugin <!-- UC804 -->
- Documentation : nouvelles versions minimales, procédure pour vérifier et mettre à jour le proxy TeslaBleHttpProxy, et déroulement d'une mise à jour depuis la version 0.x (commandes, historiques et scénarios conservés) <!-- UC899 -->
- Ajout : l'URL du proxy est désormais nettoyée à l'enregistrement de la configuration : le slash final est ajouté, les espaces sont retirés, et une URL invalide ou contenant des identifiants est refusée avec un message explicite <!-- UC001 -->
- Évolution : les échanges avec le proxy ont désormais des délais maximums (5 secondes au plus quand le proxy est éteint, au lieu d'un blocage de 60 secondes) et les erreurs sont classées par cause dans le log du plugin (proxy injoignable, véhicule hors de portée ou endormi, proxy sans clé, demande refusée par le véhicule), avec le VIN masqué <!-- UC002 -->
- Ajout : un bouton « Tester » dans la configuration du plugin vérifie que le proxy répond et affiche sa version, avec un avertissement si elle est inférieure à 2.3.0, ainsi qu'un lien vers le tableau de bord du proxy pour l'appairage des clés <!-- UC003 -->
- Ajout : la VIN d'un véhicule est désormais mise en majuscules et débarrassée de ses espaces à l'enregistrement ; une VIN invalide ou déjà utilisée par un autre équipement est refusée avec un message explicite, et les VIN des équipements existants sont normalisées à la mise à jour (anomalies signalées dans le centre de messages) <!-- UC004 -->
- Évolution : l'enregistrement d'un équipement ne lance plus de rafraîchissement : la page répond immédiatement, même proxy éteint ; les données arrivent au prochain cycle ou avec la commande Rafraîchir <!-- UC004 -->
- Correctif : les réglages de vos commandes (nom, visibilité, historisation, unité, bornes) ne sont plus écrasés lors de l'enregistrement d'un équipement ou de la réactivation du plugin, et l'information « Trappe de charge ouverte » existe désormais à côté de l'action d'ouverture de la trappe ; sur un équipement existant, cette action peut s'appeler « Trappe de Charge Ouvert » : vous pouvez la renommer <!-- UC005 -->
- Ajout : les commandes d'un nouveau véhicule portent des libellés français corrigés (« Démarrer la charge », « Arrêter la charge », « Rafraîchir »…) ; à la mise à jour, les équipements existants gardent leurs noms et reçoivent en fin de liste les nouvelles informations « Temps de charge restant », « Dernière erreur » et « Dernière lecture des données » <!-- UC005 -->
- Correctif : avec TeslaBleHttpProxy 2.1.1 et plus récent (2.3.0 requis), l'état du véhicule est de nouveau lu sans le réveiller : éveillé ou endormi, verrouillé (y compris de l'intérieur) ou non ; les données de charge et de climatisation sont donc de nouveau lues quand le véhicule est éveillé <!-- UC006 -->
- Évolution : la présence du véhicule ne passe plus à 0 quand le proxy est arrêté, sans clé ou trop lent, mais seulement quand le véhicule est hors de portée ; avec un proxy antérieur à 2.1.1, les informations ne sont plus modifiées et le log du plugin indique une seule fois « Version du proxy non prise en charge : 2.3.0 minimum » <!-- UC006 -->
- Correctif : l'autonomie et la vitesse de charge sont désormais converties en km et km/h (le véhicule les envoie en miles), les températures gardent leur décimale, une information absente de la réponse du proxy n'empêche plus la mise à jour des autres, et un véhicule qui s'endort entre deux lectures ne produit plus d'erreur dans le log <!-- UC007 -->
- Évolution : l'information « Heure départ programmée » affiche désormais l'heure au format HH:MM, vide sans départ programmé, au lieu d'un horodatage : adaptez un scénario qui comparait l'ancienne valeur ; les informations « Temps de charge restant » (en minutes) et « Trappe de charge ouverte » sont désormais alimentées <!-- UC007 -->
- Correctif : les commandes envoyées au véhicule signalent désormais leur échec au lieu d'un faux succès : un refus du véhicule (par exemple une clé au rôle Charging Manager), un proxy injoignable ou un délai dépassé s'affiche en rouge et dans « Dernière erreur » ; après une commande réussie, la limite de charge, le courant et le verrouillage sont mis à jour immédiatement, et les commandes partent une par une vers le proxy sans figer l'interface <!-- UC008 -->
- Évolution : les valeurs des commandes sont contrôlées avant envoi : courant de charge entier dans les bornes Min/Max de la commande (0 à 32 A par défaut), limite de charge entière entre 50 et 100 %, mode sentinelle Activé ou Désactivé (l'option « Aucun » est retirée des équipements existants) ; un scénario qui envoie une autre valeur reçoit désormais une erreur, et la fonction executeCmd utilisable dans un bloc Code est supprimée <!-- UC008 -->
- Évolution : le rafraîchissement toutes les 5 minutes est plus robuste : un cycle encore en cours n'est plus doublé, sa durée est limitée à 4 minutes (les véhicules restants sont lus au cycle suivant), un véhicule en erreur n'empêche plus la lecture des autres et le log nomme le véhicule concerné. <!-- UC009 -->
- Ajout : les informations « Dernière erreur » et « Dernière lecture des données » indiquent désormais pourquoi les données ne bougent plus (proxy injoignable, proxy sans clé, véhicule hors de portée…) et depuis quand elles datent ; « Dernière erreur » revient à « Aucune » dès qu'un rafraîchissement réussit, et le log ne garde plus qu'une ligne au début et une à la fin d'un problème <!-- UC010 -->
- Évolution : une erreur interne du plugin lors de l'enregistrement d'un équipement ou de la configuration, ou pendant le test du proxy, affiche désormais un message lisible (le détail est écrit dans le log du plugin) au lieu de laisser la page sans réponse ; la fiche du plugin dispose aussi d'une description en anglais <!-- UC011 -->
- Documentation : guide complet de la version 1.0 : installation du proxy et du Raspberry Pi, configuration de l'URL et du bouton Tester, VIN unique, rôle de la clé (Charging Manager ou Owner), tableaux des commandes avec leurs identifiants, types et unités, et dépannage message par message <!-- UC099 -->
- Évolution : rappel pour la mise à jour : l'information « Heure départ programmée » passe du sous-type numérique au sous-type Autre (heure au format HH:MM) ; si elle était historisée, elle reste numérique et n'est plus mise à jour tant que vous ne changez pas son sous-type en Autre dans l'onglet Commandes de l'équipement <!-- UC099 -->
- Documentation : nouvelle page « Installer le proxy BLE », pas à pas sur un Raspberry Pi Zero 2 W (préparation de la carte, Docker, appairage de la clé, entretien, sécurité, dépannage, références)
- Correctif : un proxy éteint ou injoignable est de nouveau signalé comme « proxy injoignable », et non plus comme un simple délai dépassé

# 23/09/2026

- Documentation complète du plugin

# 31/03/2025

- Renommage du plugin en **Tesla BLE** (identifiant `TeslaBLE`)
- Ajout des compatibilités matérielles (Smart, Luna, Atlas, Raspberry Pi, Docker, DIY...)
- Visibilité par défaut des commandes sur le widget
- Correctifs divers

# 15/03/2025

- Version 0.1 beta, première version
- Lecture de l'état du véhicule (présence, verrouillage, veille) sans le réveiller
- Lecture de la charge, de la batterie, de l'autonomie et de la climatisation lorsque le véhicule est réveillé
- Commandes : réveil, démarrage et arrêt de la charge, courant et limite de charge, climatisation, trappe de charge, feux, klaxon, verrouillage des portes, mode sentinelle
- Rafraîchissement automatique toutes les 5 minutes
