# Plugin Tesla BLE

Ce plugin permet de piloter la charge, la climatisation et quelques fonctions de base de vos véhicules **Tesla** depuis Jeedom, **en Bluetooth (BLE)** et sans passer par l'API cloud de Tesla.

Jeedom ne parle pas directement au véhicule : il s'appuie sur un proxy [TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy), installé sur un petit appareil équipé du Bluetooth (un Raspberry Pi Zero W par exemple) placé à portée du véhicule, typiquement dans le garage. Le plugin interroge ce proxy en HTTP sur votre réseau local.

```
Jeedom  --HTTP-->  TeslaBleHttpProxy (Raspberry Pi)  --Bluetooth-->  Véhicule
```

## Prérequis

- Jeedom 4.5 minimum, Debian 11 ou 12.
- **TeslaBleHttpProxy 2.3.0 minimum**, installé, fonctionnel et joignable depuis Jeedom.
- La **clé du proxy appairée avec le véhicule**. Cette étape se fait entièrement dans l'interface de TeslaBleHttpProxy (génération de la clé, puis validation avec votre carte-clé dans le véhicule) : reportez-vous à sa documentation.
- Le **VIN** de chaque véhicule à piloter (visible en bas de l'écran principal de l'application Tesla).

> **Astuce**
>
> Avant de configurer le plugin, vérifiez que le proxy répond en ouvrant dans un navigateur `http://<ip_du_proxy>:<port>/api/proxy/1/version` (version du proxy), puis `http://<ip_du_proxy>:<port>/api/1/vehicles/<VIN>/body_controller_state`. Vous devez obtenir une réponse JSON.

### Vérifier et mettre à jour la version du proxy

Le plugin exige **TeslaBleHttpProxy 2.3.0 minimum**. Suivez ces étapes pour connaître la version de votre proxy, puis la mettre à jour si besoin.

**1. Lire la version actuelle**

1. Sur un ordinateur du même réseau que le proxy, ouvrez un navigateur.
2. Dans la barre d'adresse, tapez `http://<ip_du_proxy>:<port>/api/proxy/1/version`, par exemple `http://192.168.1.50:8080/api/proxy/1/version`.
3. Lisez la réponse : elle ressemble à `{"version":"2.3.0"}`. Le nombre après `"version"` est la version du proxy.

Si cette version est **2.3.0 ou plus récente**, vous n'avez rien à faire. Sinon, passez à l'étape 2.

**2. Mettre à jour l'image du proxy**

1. Connectez-vous en SSH au Raspberry Pi qui héberge le proxy.
2. Placez-vous dans le dossier qui contient le fichier `docker-compose.yml` du proxy (le dossier `TeslaBleHttpProxy` si vous avez suivi la [documentation d'installation du proxy](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md)) :

   ```
   cd TeslaBleHttpProxy
   ```

3. Téléchargez la dernière image :

   ```
   docker pull wimaha/tesla-ble-http-proxy
   ```

4. Relancez le proxy avec cette nouvelle image :

   ```
   docker compose up -d
   ```

**3. Revérifier la version**

Rouvrez `http://<ip_du_proxy>:<port>/api/proxy/1/version` dans le navigateur (attendez quelques secondes que le proxy redémarre) et contrôlez que la version est bien 2.3.0 ou plus récente.

La clé appairée avec le véhicule est stockée dans le dossier `key` monté par le fichier `docker-compose.yml` : elle est **conservée** par la mise à jour, vous n'avez pas à refaire l'appairage.

> **IMPORTANT**
>
> Avec un proxy plus ancien que 2.1.1, le plugin ne peut pas lire l'état du véhicule : le verrouillage et l'état de veille ne sont plus mis à jour, la présence ne repasse plus à 1, et le log du plugin indique « Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour » (ligne en erreur).

### Choisir et installer le Raspberry Pi

Le proxy doit être **à portée Bluetooth du véhicule** (5 à 10 m, donc en général dans le garage). C'est le Raspberry Pi qui doit être proche de la voiture, pas Jeedom.

| Carte | Verdict |
|---|---|
| **Raspberry Pi Zero 2 W** | Recommandé : petit, peu gourmand, image Docker 64 bits officielle du proxy. |
| Raspberry Pi Zero W (première génération) | Déconseillé : processeur ARMv6 qui n'est plus pris en charge par les versions récentes de Docker, et adaptateur Bluetooth qui a tendance à se figer au bout de quelques heures. |
| Raspberry Pi 3, 4, 5 ou mini-PC avec Bluetooth | Convient, à condition d'être à portée du véhicule. |

En résumé, l'installation consiste à :

1. Installer Raspberry Pi OS **64 bits Lite** et Docker.
2. Lancer l'image `wimaha/tesla-ble-http-proxy` en suivant la [documentation d'installation du proxy](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md).
3. Ouvrir `http://<ip_du_pi>:8080/dashboard`, générer la clé, saisir le VIN, **réveiller le véhicule**, envoyer la clé puis poser la carte-clé sur la console centrale pour valider.
4. Donner une **adresse IP fixe** au Raspberry Pi (réservation DHCP sur votre box), puisque son adresse est enregistrée dans le plugin.

Quelques conseils pour un fonctionnement stable :

- Utilisez une alimentation de qualité (5 V, 2,5 A) : une alimentation faible provoque des déconnexions Bluetooth.
- N'utilisez pas le Bluetooth de ce Raspberry Pi pour autre chose : le proxy a besoin de l'adaptateur pour lui seul.
- Un véhicule n'accepte que **3 appareils Bluetooth connectés en même temps** (téléphones, montre, proxy). Au-delà, les connexions deviennent intermittentes.

### Rôle de la clé

Avec TeslaBleHttpProxy 2.3.0, la clé générée par défaut a le rôle **Charging Manager**. Elle suffit pour lire l'état du véhicule et piloter la charge, mais le véhicule **refuse** le verrouillage, le klaxon, les feux et le mode sentinelle, et probablement la climatisation. Pour utiliser ces commandes, générez et appairez une clé de rôle **Owner** depuis le dashboard du proxy.

> **IMPORTANT**
>
> Le proxy n'a **aucune authentification**. Avec une clé Owner, n'importe quel appareil de votre réseau local peut déverrouiller le véhicule. Gardez le proxy sur un réseau de confiance, idéalement isolé, et n'exposez **jamais** son port sur Internet. Si vous ne pilotez que la charge, préférez une clé Charging Manager.

## Configuration du plugin

Après installation, activez le plugin puis renseignez dans sa page de configuration l'**URL du proxy** TeslaBleHttpProxy.

Le format attendu est `http://<ip_du_proxy>:<port>/`, par exemple `http://192.168.1.50:8080/`.

> **IMPORTANT**
>
> L'URL doit se terminer par un `/`. Le plugin y ajoute directement `api/1/vehicles/...` : sans le slash final, toutes les requêtes échouent.

Un seul proxy est utilisé pour tous les véhicules.

## Configuration des équipements

Chaque véhicule est un équipement. Rendez-vous dans **Plugins > Communication des objets > Tesla BLE**, cliquez sur **Ajouter** et donnez un nom au véhicule.

Dans l'onglet **Equipement** :

- **Paramètres généraux** : nom, objet parent, catégorie, activation et visibilité, comme pour tout équipement Jeedom.
- **VIN** : le numéro de série du véhicule (17 caractères alphanumériques). Il doit être celui que vous avez déclaré dans TeslaBleHttpProxy.

À la sauvegarde, le plugin crée toutes les commandes de l'équipement puis lance un premier rafraîchissement.

## Mise à jour depuis la version 0.x

Vous mettez à jour le plugin depuis une version 0.x : rien n'est à refaire.

> **IMPORTANT**
>
> Vos **équipements, VIN, commandes, historiques, scénarios et réglages d'affichage sont conservés**. Les commandes gardent leurs identifiants : les scénarios, les widgets et les historiques qui les utilisent continuent de fonctionner sans modification.

### Autonomie et vitesse de charge

Les commandes **Autonomie** et **Vitesse de Charge** sont désormais converties en km et km/h (le véhicule les envoie en miles). Les valeurs déjà enregistrées dans l'historique restent en miles : le graphique de l'**Autonomie** montre donc un saut d'environ 1,6 au moment de la mise à jour.

### Heure de départ programmée

La commande **Heure Départ Programmée** affiche désormais l'heure au format `HH:MM` (par exemple `07:30`), et reste vide quand aucun départ n'est programmé. Elle donnait auparavant un horodatage numérique : adaptez les scénarios qui la comparaient à ce nombre.

Si vous avez activé l'historisation de cette commande, elle reste numérique et n'est plus mise à jour ; un message vous l'indique dans le centre de messages de Jeedom. Pour recevoir l'heure, changez son sous-type en **Autre** dans l'onglet **Commandes** de l'équipement.

### Commandes action

- L'option **« Aucun »** du **Mode sentinelle** est retirée (le proxy ne la comprenait pas). Un scénario qui l'envoyait reçoit désormais une erreur : utilisez **Activé** ou **Désactivé**. La mise à jour retire cette option des équipements existants, sans toucher aux autres réglages de la commande.
- Un **courant de charge hors des bornes** de la commande, ou non entier, est refusé au lieu d'être envoyé.
- Une commande qui échouait sans rien dire affiche désormais une **erreur** et alimente l'information **Dernière erreur**.

### Versions minimales

| Élément | Version |
|---|---|
| Jeedom | 4.5 minimum |
| Debian | 11 ou 12 |
| TeslaBleHttpProxy | 2.3.0 minimum (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)) |

Si votre Jeedom est en version inférieure à 4.5, Jeedom refuse la mise à jour avec le message « Version du core Jeedom non supportée ». L'ancienne version du plugin reste alors en place et continue de fonctionner. Mettez d'abord Jeedom à jour. Debian 10 n'est plus prise en charge.

### Ce qui est fait automatiquement

À la mise à jour, puis à l'activation du plugin, une mise à niveau des équipements existants s'exécute automatiquement, par niveaux successifs. Chaque niveau n'est appliqué qu'une seule fois. Selon les versions, elle corrige ou complète certains équipements (VIN, commandes manquantes, heure de départ programmée, retrait de l'option « Aucun » du mode sentinelle…) sans toucher à vos réglages (nom, visibilité, historisation).

Si la mise à niveau échoue sur un véhicule, elle est retentée automatiquement à la prochaine mise à jour ou activation du plugin.

### Constater la mise à niveau dans le log

Passez le log du plugin au moins en niveau **Info** (**Configuration du plugin > Logs**), puis mettez à jour ou réactivez le plugin et ouvrez son log. Les lignes concernées commencent par « Migrations : ».

| Situation | Message dans le log |
|---|---|
| Mise à niveau réussie | `Migrations : migration N (<description>) appliquée sur X équipement(s) sur Y.` pour chaque niveau appliqué, puis `Migrations : niveau de migration N atteint.` |
| Déjà à jour | `Migrations : aucune migration à appliquer, niveau de migration N.` (N = dernier niveau) |
| Aucun équipement (installation neuve) | `Migrations : aucun équipement à migrer, niveau de migration N (aucune migration exécutée).` (N = dernier niveau) |
| Échec sur un équipement | `Migrations : échec de la migration N (...) sur l'équipement « <nom> » (id <n>) : ...` suivi de `Elle sera retentée à la prochaine mise à jour ou activation du plugin.`, puis `Migrations : niveau de migration M conservé, X équipement(s) en échec ; les migrations restantes seront retentées à la prochaine mise à jour ou activation du plugin.` |

Si un message d'échec persiste après plusieurs mises à jour, notez-le et signalez-le avec le log du plugin.

## Fonctionnement

### Rafraîchissement des informations

Toutes les **5 minutes**, le plugin rafraîchit chaque véhicule actif en deux temps :

1. Il interroge l'état du **contrôleur de carrosserie** (`body_controller_state`). Cette requête ne réveille pas le véhicule. Elle met à jour la présence, le verrouillage et l'état de veille.
2. **Uniquement si le véhicule est réveillé**, il récupère les données complètes (`vehicle_data`) : charge, batterie, autonomie et climatisation.

Le plugin ne réveille donc jamais le véhicule de lui-même, afin de ne pas vider la batterie. Tant que le véhicule dort, les informations de charge et de climatisation conservent leur dernière valeur connue. Pour les actualiser, utilisez la commande **Réveiller**, puis **Rafraichir** quelques secondes plus tard.

Si le véhicule s'endort entre les deux requêtes, ce n'est pas une erreur : les informations de charge et de climatisation gardent leur dernière valeur et rien n'est affiché.

Si le véhicule est hors de portée Bluetooth du proxy, la commande **Présence véhicule** passe à 0. Si c'est le proxy qui ne répond pas, n'a pas de clé appairée ou répond trop lentement, la présence garde sa dernière valeur.

**Pourquoi les données ne bougent plus ?** L'information **Dernière erreur** donne la cause du dernier échec de lecture, suivie de la raison renvoyée par le proxy quand il en donne une (par exemple « Véhicule hors de portée — … » ou « Proxy sans clé : appairage à faire — … »). Elle revient à **Aucune** dès qu'un cycle de lecture réussit. Un véhicule qui dort n'est pas une erreur : **Dernière erreur** reste à **Aucune** et **Véhicule réveillé** vaut 0. L'information **Dernière lecture des données** indique depuis quand les données de charge et de climatisation datent.

Dans le log du plugin, un problème ne laisse que **deux lignes** : une quand il commence, une quand tout revient à la normale, même s'il dure des heures. Ces lignes apparaissent au niveau de log **Info** ; une erreur de configuration (VIN ou URL manquante) ou un proxy trop ancien est consigné au niveau **Erreur**. Tant que le problème dure, le détail de chaque cycle reste visible en **Debug**.

Les véhicules sont rafraîchis **l'un après l'autre**. Un véhicule hors de portée ou en erreur n'empêche pas la lecture des suivants, et l'erreur est consignée dans le log avec le nom du véhicule.

- Si le cycle précédent n'est pas terminé, le nouveau cycle est **sauté** (un avertissement par heure au plus dans le log) ; il reprend normalement dès que le précédent est fini, même s'il a été interrompu.
- Un cycle ne dépasse pas **4 minutes** : s'il y a beaucoup de véhicules ou si le proxy est lent, les véhicules restants sont lus au cycle suivant (avertissement nommant ces véhicules).
- Pendant qu'une commande est en cours vers le même proxy, la lecture du cycle est sautée sans erreur ; la lecture suivante rattrape.

### Exécution des commandes

Chaque commande action est transmise au proxy, qui attend la confirmation du véhicule avant de répondre. Le plugin n'a pas besoin de réveiller le véhicule avant une commande : le proxy s'en charge.

**Valeurs contrôlées avant l'envoi.** Une valeur invalide est refusée tout de suite, avec un message, sans rien envoyer au proxy :

- **Courant de charge** : un nombre entier compris entre le **Min** et le **Max** de la commande (0 à 32 A par défaut). Pour un véhicule qui accepte davantage, par exemple 48 A, augmentez le **Max** dans l'onglet **Commandes** de l'équipement. Une valeur décimale (`16,5`) ou un texte est refusé.
- **Limite de charge** : un nombre entier compris entre 50 et 100 %.
- **Mode sentinelle** : **Activé** ou **Désactivé** (l'ancienne option « Aucun » n'existe plus).

**En cas d'échec.** Si le proxy ou le véhicule refuse la commande, un message d'erreur apparaît en rouge dans l'interface de Jeedom (et dans le log du plugin en erreur), et il est aussi enregistré dans l'information **Dernière erreur**, où il reste affiché jusqu'au prochain cycle de lecture réussi (5 minutes au plus). Par exemple « Commande refusée par le véhicule (rôle de la clé du proxy insuffisant ?) » : voir [Rôle de la clé](#rôle-de-la-clé).

**Après une commande réussie.** La limite de charge, le courant de charge et le verrouillage sont mis à jour immédiatement, puis l'état du véhicule (présence, éveil) est relu sans le réveiller. Les autres informations de charge et de climatisation sont actualisées au cycle de 5 minutes suivant.

**Une commande ou une lecture à la fois.** Les échanges avec un même proxy se font l'un après l'autre : une commande attend la fin d'une autre commande ou d'une lecture vers le même proxy (jusqu'à 2 minutes environ). Si le proxy et le véhicule sont à la limite de leurs délais, la réponse peut prendre 3 à 4 minutes. Jeedom reste utilisable pendant ce temps.

## Commandes

### Informations

| Commande | Unité | Description |
|---|---|---|
| Présence véhicule | | 1 si le proxy joint le véhicule en Bluetooth, 0 s'il est hors de portée |
| Véhicule réveillé | | 1 si le véhicule est éveillé, 0 s'il dort ou si son état de veille est inconnu |
| Verrouillage du véhicule | | 1 si le véhicule est verrouillé, y compris de l'intérieur, 0 s'il est déverrouillé, même partiellement |
| Etat Charge | | État de la charge renvoyé par le véhicule (`Charging`, `Stopped`, `Complete`, `Disconnected`...) |
| Charge Batterie | % | Niveau de batterie utilisable |
| Limite Charge | % | Limite de charge configurée |
| Autonomie | km | Autonomie estimée, convertie en kilomètres (le véhicule la renvoie en miles) |
| Temps de charge | | Temps restant avant la fin de la charge, au format `HHhMM` |
| Temps de charge restant | min | Le même temps restant, en minutes (utilisable dans un scénario ou un graphique) |
| Vitesse de Charge | km/h | Autonomie récupérée par heure de charge, convertie en km/h (le véhicule la renvoie en miles par heure) |
| Tension Chargeur | V | Tension délivrée par la borne |
| Courant de Charge (A) | A | Courant de charge configuré |
| Courant Demande Charge | A | Courant demandé par le véhicule |
| Verrouillage Trappe Charge | | État du verrou du câble de charge |
| Mode Charge Programmée | | Mode de charge programmée |
| Heure Départ Programmée | | Heure de départ programmée au format `HH:MM` (heure du véhicule) ; vide si aucun départ n'est programmé |
| Trappe de charge ouverte | | 1 si la trappe de charge est ouverte, 0 si elle est fermée |
| Température intérieure | °C | Température dans l'habitacle, au dixième de degré |
| Température extérieure | °C | Température extérieure, au dixième de degré |
| Température conducteur | °C | Consigne de climatisation côté conducteur |
| Température passager | °C | Consigne de climatisation côté passager |
| Climatisation activée | | 1 si la climatisation fonctionne |
| Chauffage siège conducteur | | Niveau de chauffage du siège conducteur (0 à 3) |
| Chauffage siège passager | | Niveau de chauffage du siège passager (0 à 3) |
| Chauffage du volant | | 1 si le chauffage du volant est actif |
| Mode dégivrage | | État du dégivrage |
| Dernière erreur | | Cause du dernier échec de lecture ou de commande, suivie de la raison du proxy quand il en donne une ; **Aucune** quand tout va bien. Utilisable dans un scénario |
| Dernière lecture des données | | Date et heure (heure de Jeedom, `AAAA-MM-JJ HH:MM:SS`) de la dernière lecture réussie des données de charge et de climatisation |

Le niveau de batterie alimente aussi le suivi de batterie de Jeedom (page **Analyse > Equipements**).

Chaque information de charge et de climatisation est mise à jour indépendamment : si le véhicule ne renvoie pas l'une d'elles, elle garde sa dernière valeur et les autres sont tout de même actualisées.

### Actions

| Commande | Description |
|---|---|
| Rafraichir | Relance immédiatement la lecture des informations |
| Réveiller | Réveille le véhicule, pour lire ses données de charge et de climatisation. Inutile avant une commande : le proxy réveille le véhicule seul |
| Charge Start | Démarre la charge |
| Charge Stop | Arrête la charge |
| Courant de charge | Règle le courant de charge (entier, entre le Min et le Max de la commande ; 0 à 32 A par défaut, augmentez le Max pour un véhicule 48 A) |
| Limite de charge | Règle la limite de charge, de 50 à 100 % |
| Démarrer le climatiseur | Lance le préconditionnement |
| Arrêter le climatiseur | Arrête le préconditionnement |
| Ouvrir la trappe de charge | Ouvre la trappe de charge |
| Fermer la trappe de charge | Ferme la trappe de charge |
| Faire clignoter les feux | Fait clignoter les phares |
| Klaxonner | Actionne le klaxon |
| Verrouiller les portes | Verrouille le véhicule |
| Déverrouiller les portes | Déverrouille le véhicule |
| Mode sentinelle | Active ou désactive le mode sentinelle (**Activé** ou **Désactivé**) |

Certaines commandes sont masquées par défaut sur le widget (ouverture de la trappe, verrouillage des portes, feux, mode sentinelle...). Vous pouvez les rendre visibles depuis l'onglet **Commandes** de l'équipement.

## Exemples d'utilisation

- **Charge solaire** : dans un scénario, ajustez **Courant de charge** en fonction de la production photovoltaïque.
- **Heures creuses** : déclenchez **Charge Start** au début des heures creuses et **Charge Stop** à leur fin.
- **Préchauffage** : lancez **Démarrer le climatiseur** quelques minutes avant votre départ.
- **Alerte** : recevez une notification si **Verrouillage du véhicule** reste à 0 le soir.
- **Panne de liaison** : recevez une notification quand **Dernière erreur** passe à autre chose que **Aucune** (proxy injoignable, proxy sans clé appairée...). Un véhicule qui dort ne la déclenche pas.

## Limitations connues

Ces points concernent la version actuelle (0.1 beta) et sont corrigés en priorité pour la version 1.0 :

- **Trappe de charge** : l'information **Trappe de Charge Ouvert** et l'action **Ouvrir la trappe de charge** partagent le même identifiant. L'action remplace l'information à la sauvegarde de l'équipement.
- **Après une commande**, seuls la limite de charge, le courant de charge et le verrouillage sont mis à jour tout de suite. Les autres informations de charge et de climatisation sont à jour au cycle de 5 minutes suivant.

## Dépannage

Passez le log du plugin en niveau **Debug** (**Configuration du plugin > Logs**) pour voir chaque URL appelée et chaque réponse du proxy.

- **« URL invalide : … »** : l'URL du proxy est vide ou mal saisie dans la configuration du plugin. Renseignez-la (avec `http://` et le `/` final).
- **« Le VIN n'est pas configuré pour cet équipement »** : renseignez le VIN dans l'équipement puis sauvegardez.
- **« Proxy sans clé : appairage à faire »** (**Dernière erreur**) : le proxy n'a pas de clé appairée avec le véhicule. Suivez la procédure d'appairage du proxy.
- **« Véhicule hors de portée »** (**Dernière erreur**) : le proxy ne trouve pas le véhicule en Bluetooth. Voir **Présence véhicule reste à 0** ci-dessous.
- **« Délai dépassé »** ou **« Réponse invalide du proxy »** (**Dernière erreur**) : le proxy répond trop lentement ou renvoie une réponse inattendue. Vérifiez le Raspberry Pi (alimentation, Wi-Fi) et redémarrez le proxy si cela se répète.
- **« Demande refusée par le véhicule »** (**Dernière erreur**) : le véhicule a refusé la lecture ; la raison renvoyée suit le message.
- **« Fonction non supportée par ce proxy »** (**Dernière erreur**) : cette lecture n'existe pas dans votre version du proxy. Mettez-le à jour.
- **Présence véhicule reste à 0** : le proxy ne trouve pas le véhicule en Bluetooth. Rapprochez le Raspberry Pi du véhicule.
- **Les informations de charge ne bougent plus** : le véhicule dort. C'est le comportement normal, voir [Rafraîchissement des informations](#rafraîchissement-des-informations).
- **« Cycle de rafraîchissement sauté : le cycle précédent n'est pas terminé. »** : la lecture précédente dure plus de 5 minutes, en général parce que le proxy ou le Raspberry Pi répond très lentement. Vérifiez l'alimentation et la connexion Wi-Fi du Raspberry Pi, puis redémarrez le proxy si cela se répète.
- **« Cycle de rafraîchissement écourté… véhicule(s) non lu(s) à ce cycle »** : le cycle a atteint sa durée maximale de 4 minutes ; les véhicules cités seront lus au cycle suivant. Si cela se répète, c'est que le proxy répond trop lentement : voir ci-dessus.
- **Aucune requête n'aboutit** : vérifiez l'URL du proxy, notamment le `/` final, et testez-la depuis un navigateur.
- **« Commande refusée par le véhicule (rôle de la clé du proxy insuffisant ?) »** : votre clé a le rôle Charging Manager, qui n'autorise pas cette commande (verrouillage, klaxon, feux, sentinelle). Voir [Rôle de la clé](#rôle-de-la-clé).
- **« Commande refusée par le véhicule : … »** : le véhicule a refusé la commande, la raison renvoyée suit le message.
- **« Proxy injoignable, commande non envoyée »** : le proxy ne répond pas, la commande n'est pas partie. Vérifiez l'URL et l'alimentation du Raspberry Pi.
- **« Délai dépassé : la commande a pu être exécutée, vérifiez l'état du véhicule »** ou **« Liaison avec le proxy interrompue… »** : la commande a peut-être été exécutée malgré tout. Contrôlez l'état du véhicule avant de la renvoyer.
- **« Proxy occupé : commande non envoyée, réessayez dans un instant »** : une autre commande ou lecture occupe le proxy depuis plus de 2 minutes. Réessayez.
- **« Valeur invalide : … »** : la valeur envoyée (courant, limite, mode sentinelle) n'est pas acceptée. Corrigez-la, ou augmentez le **Max** de la commande **Courant de charge** si votre véhicule accepte davantage de 32 A.
- **Présence, verrouillage et veille ne changent plus, et le log indique en erreur « Version du proxy non prise en charge : 2.3.0 minimum… »** : votre proxy est antérieur à 2.1.1, mettez-le à jour (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)).
- **Le proxy ne répond plus au bout de quelques heures** : c'est un problème fréquent sur le Raspberry Pi Zero W de première génération. Redémarrez le proxy ou passez à un Raspberry Pi Zero 2 W.
