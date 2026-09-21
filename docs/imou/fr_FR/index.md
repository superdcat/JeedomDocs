# Plugin IMOU

Le plugin **IMOU** pilote vos caméras IMOU depuis Jeedom via l'**IMOU Open API** (cloud), **en PHP natif**
(sans démon, sans Python). Selon les capacités de chaque caméra : marche/arrêt, surveillance, PTZ,
projecteur/sirène, vision nocturne, réglages d'image, flux live, miniature, redémarrage, batterie, sonnette
& ouverture de porte, remontée des alarmes, état de la carte SD et de l'abonnement cloud, supervision.

> L'API IMOU ne propose pas de notifications « temps réel » : l'état des caméras est rafraîchi par
> **interrogation périodique** (polling). Un changement fait depuis l'application IMOU peut donc mettre
> quelques minutes à apparaître dans Jeedom.

## Pré-requis

- Un compte **développeur IMOU** sur [open.imoulife.com](https://open.imoulife.com).
- Une application créée dans la console développeur, fournissant un **`appId`** et un **`appSecret`**, avec
  le mode d'intégration **`accessType = PaaS`** (requis pour piloter les appareils).
- Vos caméras déjà associées à ce compte via l'application **IMOU Life**.
- **`ffmpeg`** : installé **automatiquement** par Jeedom à l'activation du plugin (onglet « Dépendances »).
  Il sert à extraire les images du flux live. Sur une installation Docker, vérifiez que `ffmpeg` est
  disponible dans l'image.

> ℹ️ **Nombre d'appareils pilotables (tier gratuit).** En théorie, le compte développeur IMOU gratuit est
> limité à **~5 appareils** : au-delà, les commandes *devraient* échouer avec une **erreur de licence**
> renvoyée par IMOU (ce n'est pas une limite du plugin). **En pratique, IMOU semble laisser piloter plus de
> caméras** en gratuit — dans nos tests, tout fonctionne normalement au-delà de 5. Ce comportement dépend
> d'IMOU et peut changer sans préavis : si une commande finit par renvoyer une erreur de licence, c'est
> cette limite qui s'applique, et il faut alors une offre IMOU adaptée. Dans tous les cas, les caméras sont
> découvertes et affichées ; seules leurs commandes seraient affectées.

## Configuration du plugin

1. Activez le plugin (Plugins → Gestion des plugins → IMOU) et laissez Jeedom installer les dépendances.
2. Dans la configuration du plugin, renseignez :
   - **App ID** : l'identifiant de votre application IMOU ;
   - **App Secret** : le secret associé (**stocké chiffré**, jamais affiché en clair) ;
   - **Datacenter** : la région de votre compte (Europe par défaut).
3. Cliquez sur **Tester la connexion** pour valider vos identifiants.

### Réglages avancés (facultatifs)

- **Quota d'appels** : `quotaMensuel` (plafond mensuel d'appels API, ~30 000 sur le tier gratuit),
  seuil d'alerte. Le quota se réinitialise **le 1er de chaque mois**. Le plugin **compte ses appels** et
  vous alerte à l'approche du plafond.
- **Régulation automatique de la cadence** : bornes `refreshIntervalMin`/`refreshIntervalMax`. Le plugin
  ajuste tout seul la fréquence de rafraîchissement pour tenir dans le budget d'appels du mois.
- **Flux live concurrents** : `liveMaxConcurrent` (nombre de flux live affichés en même temps).
- **Estimation de la consommation data** : `dataQuotaGo` / `dataBitrateKbps` (voir « Quota & supervision »).

## Ajout des caméras

- Cliquez sur **Synchroniser** : le plugin récupère les caméras du compte et crée **un équipement par
  caméra** (un par canal pour les appareils multi-canaux).
- Renommez et rangez les équipements dans vos objets comme d'habitude : **vos personnalisations sont
  préservées** lors des synchronisations suivantes.
- **Synchronisation sélective** : chaque commande d'état peut être exclue du rafraîchissement automatique
  (case « Exclure du rafraîchissement automatique »), pour économiser des appels sur ce qui ne vous sert pas.

> 💡 **Les commandes sont conditionnelles aux capacités de la caméra.** Le plugin ne crée que les commandes
> réellement supportées par chaque modèle. Si une commande (PTZ, sirène, vision nocturne, carte SD…)
> **n'apparaît pas**, c'est que votre caméra ne déclare pas cette capacité — c'est **normal**, pas un bug.

## Commandes disponibles (selon la caméra)

- **Marche / Arrêt** de la caméra.
- **Surveillance** (détection de mouvement) : activer / désactiver.
- **Projecteur / lumière** et **sirène** (sur les modèles compatibles, via le modèle IoT « Things »).
- **PTZ** : pavé directionnel (haut/bas/gauche/droite) et zoom sur les caméras motorisées.
- **Vision nocturne** : mode (auto / infrarouge / couleur selon le modèle).
- **Réglages d'image** : retournement, WDR, incrustation date/heure (OSD), voyant LED…
- **Flux live** : image rafraîchie du direct, **affichable en plein écran** d'un clic.
- **Miniature** de la caméra (source au choix : cliché du live ou image de couverture).
- **Modèle (code)** : code technique de la caméra, affiché en **champ lecture seule** dans la
  configuration de l'équipement (à côté de l'identifiant), pas comme commande.
- **Redémarrage** de l'appareil (action protégée par confirmation).
- **Batterie & réveil** : niveau de batterie (remonté dans la supervision Santé de Jeedom) ; les appareils
  dormants sont réveillés pour lire leur état.
- **Sonnette vidéo & ouverture de porte** (sur serrures/sonnettes compatibles ; ouverture protégée par
  confirmation).
- **Alarmes & détection** : dernier événement (mouvement/humain), **sensibilité** de détection, **plans
  d'armement** (préréglages jour/nuit/permanent), **détection humaine / IA**.
- **Carte SD** : présence, taux d'occupation, capacité, et **formatage** (action protégée par confirmation).
- **Enregistrement cloud** : état de l'abonnement (actif, expiration, forfait). **Désactivé par défaut**
  (option à activer si vous avez un abonnement — voir ci-dessous).
- **En ligne (état)** : joignabilité de la caméra, utilisée aussi pour économiser les appels (une caméra
  hors ligne n'est pas interrogée).

### Activer le suivi de l'abonnement cloud

Les commandes cloud sont créées **masquées et non interrogées** par défaut (la plupart des comptes n'ont
pas d'abonnement). Si vous avez un abonnement cloud : rendez la commande **Cloud actif** visible et
décochez sa case « Exclure du rafraîchissement automatique » pour activer le suivi (vérifié une fois par
heure).

## Le panneau « mur de caméras »

Le plugin ajoute une **page dédiée** au menu Jeedom affichant une grille des flux live de vos caméras (avec
PTZ, sirène, projecteur selon les modèles). Activez-la dans la **gestion du plugin** (case « Afficher le
panneau desktop »), puis choisissez par caméra si elle apparaît sur le mur (case « Visible sur le panneau
caméras » de l'équipement).

## Rafraîchissement, quota & supervision

Le plugin interroge le cloud IMOU périodiquement (cron). Deux budgets **distincts** sont à connaître :

- **Quota d'APPELS API** (~30 000/mois sur le tier gratuit) : **compté exactement** par le plugin. La
  cadence de rafraîchissement est **régulée automatiquement** pour tenir dans ce budget, et une alerte est
  remontée à l'approche du plafond. Les états « lents » (carte SD, abonnement cloud) sont rafraîchis à
  faible fréquence (une fois par heure) — et l'abonnement cloud n'est interrogé que si vous l'avez activé
  (voir « Activer le suivi de l'abonnement cloud »).
- **Quota de DATA** (volume du flux live, ~3 Go/mois sur le tier gratuit) : le plugin en donne une
  **estimation** (temps de visionnage × débit configuré `dataBitrateKbps`, comparée à `dataQuotaGo`).
  C'est un **indicateur informatif** : la valeur **réelle** est celle du **portail développeur IMOU**, qui
  fait foi. L'API IMOU n'expose pas la consommation data réelle.

L'écran **Santé** du plugin résume la joignabilité des caméras, le quota d'appels, la cadence régulée et
l'estimation de consommation data.

## Vie privée & localisation des données

Les **flux vidéo** et les **commandes** transitent par les **serveurs cloud IMOU** (datacenter selon votre
région — choisissez « Europe » pour la France). **Aucune vidéo ne transite par Jeedom** : le plugin envoie
des commandes de pilotage et reçoit des métadonnées d'état ainsi que des images extraites du flux live.

## Dépannage

- **La synchronisation ne trouve aucune caméra** → vérifiez `appId`/`appSecret`/`Datacenter`, le bouton
  **Tester la connexion**, et que vos caméras sont bien associées au compte dans l'application IMOU Life.
- **Une commande n'existe pas sur ma caméra** → la capacité n'est pas supportée par ce modèle. C'est normal.
- **Le flux live ne s'affiche pas** → vérifiez que les **dépendances** du plugin sont installées (`ffmpeg`),
  que la caméra est en ligne, puis consultez les logs `imou` en niveau *debug*.
- **Les commandes échouent avec une erreur de licence** → vous atteignez peut-être la limite d'appareils
  pilotables du tier gratuit IMOU (en théorie ~5, mais IMOU en autorise souvent davantage en pratique ;
  voir Pré-requis). Il faut alors une offre IMOU adaptée — ce n'est pas une limite du plugin.
- **« Horloge désynchronisée » / erreur de signature** → synchronisez l'heure du serveur Jeedom (NTP) :
  un écart de plus de 5 minutes fait rejeter les requêtes par IMOU.
- **Un changement fait dans l'app IMOU n'apparaît pas tout de suite** → normal, le rafraîchissement est
  périodique (pas de notification temps réel).

## Limites connues

- **Pas d'alarmes en temps réel (push)** : les événements sont remontés par interrogation périodique, pas
  par notification instantanée.
- **Pas de relecture des enregistrements** : l'API IMOU n'expose pas d'URL de lecture des vidéos
  enregistrées (SD ou cloud) ; la relecture se fait dans l'application IMOU.
- **Pas de nom commercial du modèle** : seul le code technique du modèle est affiché (il n'existe pas de
  base de correspondance fiable code → nom commercial).
- **Zones de détection, mise à jour du firmware, association/renommage côté IMOU** : non gérés.

## Désinstallation

Désactiver puis supprimer le plugin dans Jeedom retire les équipements et leurs commandes. Vos
**identifiants IMOU** (`appId`/`appSecret`) restent **valides** sur votre compte développeur IMOU et peuvent
être réutilisés ; ils ne sont pas supprimés côté IMOU par cette opération.
