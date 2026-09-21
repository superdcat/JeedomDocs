# Changelog plugin IMOU

>**IMPORTANT**
>
>S'il n'y a pas d'information sur la mise à jour, c'est que celle-ci concerne uniquement de la mise à jour de documentation, de traduction ou de texte.

# 1.0

Première version complète, par domaine fonctionnel :

- **Socle** : configuration (appId/appSecret/datacenter chiffrés), test de connexion, découverte et
  synchronisation des caméras (personnalisations préservées, synchronisation sélective par commande).
- **Pilotage** : marche/arrêt, surveillance (détection de mouvement), projecteur/lumière, sirène (via le
  modèle IoT « Things »), PTZ (pavé directionnel + zoom), vision nocturne, réglages d'image
  (retournement, WDR, OSD, LED).
- **Vidéo & images** : flux live (images du direct), affichage plein écran, page « panneau caméras »,
  miniature de caméra (source au choix).
- **Alarmes & détection** : dernier événement (mouvement/humain), sensibilité de détection, plans
  d'armement (préréglages), détection humaine/IA.
- **Gestion des appareils** : affichage du code modèle (code technique uniquement), redémarrage, suivi de
  batterie & réveil des appareils dormants.
- **Contrôle d'accès** : sonnette vidéo, ouverture de porte (matériel compatible).
- **Stockage** : état de la carte SD (présence, occupation, capacité) + formatage ; état de l'abonnement
  cloud (lecture seule, désactivé par défaut — à activer si vous avez un abonnement cloud IMOU).
- **Supervision & robustesse** : état en ligne / santé, gestion des erreurs et nouvelles tentatives,
  statistiques et quota d'appels avec alerte, régulation automatique de la cadence de rafraîchissement,
  estimation de la consommation data du flux live.

# 0.1

- Version initiale (en cours de développement).
