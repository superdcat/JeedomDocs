# Plugin Tesla BLE

Ce plugin permet de piloter la charge, la climatisation et quelques fonctions de base de vos véhicules **Tesla** depuis Jeedom, **en Bluetooth (BLE)** et sans passer par l'API cloud de Tesla.

Jeedom ne parle pas directement au véhicule : il s'appuie sur un proxy [TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy), installé sur un petit appareil équipé du Bluetooth (un Raspberry Pi, voir [Choisir et installer le Raspberry Pi](#choisir-et-installer-le-raspberry-pi)) placé à portée du véhicule, typiquement dans le garage. Le plugin interroge ce proxy en HTTP sur votre réseau local.

```
Jeedom  --HTTP-->  TeslaBleHttpProxy (Raspberry Pi)  --Bluetooth-->  Véhicule
```

## Prérequis

- Jeedom 4.5 minimum, sur Debian 11 ou 12.
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

Avec TeslaBleHttpProxy 2.3.0, la clé générée par défaut a le rôle **Charging Manager**. Elle suffit pour lire l'état du véhicule et piloter la charge, mais le véhicule **refuse** certaines commandes. Pour les utiliser, générez et appairez une clé de rôle **Owner** depuis le dashboard du proxy (lien dans la configuration du plugin).

| Rôle de la clé | Commandes concernées (liste indicative) |
|---|---|
| **Charging Manager** : fonctionne | Lectures (présence, verrouillage, charge, climatisation), **Rafraîchir**, **Réveiller**, **Démarrer la charge**, **Arrêter la charge**, **Courant de charge**, **Limite de charge** |
| **Charging Manager** : refusé | **Verrouiller les portes**, **Déverrouiller les portes**, **Klaxonner**, **Faire clignoter les feux**, **Mode sentinelle** ; probablement aussi **Démarrer le climatiseur** et **Arrêter le climatiseur** |
| **Owner** | Toutes les commandes |

Cette liste est indicative : le véhicule décide. Le refus se reconnaît au message « Commande refusée par le véhicule (rôle de la clé du proxy insuffisant ?) ». Le comportement de l'ouverture et de la fermeture de la trappe de charge avec une clé Charging Manager n'est pas confirmé.

> **IMPORTANT**
>
> Le proxy n'a **aucune authentification**. Avec une clé Owner, n'importe quel appareil de votre réseau local peut déverrouiller le véhicule. Gardez le proxy sur un réseau de confiance, idéalement isolé, et n'exposez **jamais** son port sur Internet. Si vous ne pilotez que la charge, préférez une clé Charging Manager.

## Configuration du plugin

Après installation, activez le plugin puis ouvrez sa page de configuration (**Plugins > Gestion des plugins > Tesla BLE**). Elle ne comporte qu'un réglage.

| Champ | Valeur attendue |
|---|---|
| **URL du proxy** | L'adresse de TeslaBleHttpProxy avec son port, par exemple `http://192.168.1.50:8080/`. Elle doit commencer par `http://` ou `https://`. Un seul proxy est utilisé pour tous les véhicules. |
| **Tester** (bouton) | Vérifie que le proxy répond et affiche sa version. Il teste la valeur saisie, **même non enregistrée**. |
| **Ouvrir le tableau de bord du proxy (appairage des clés)** (lien) | Ouvre le tableau de bord du proxy dans un nouvel onglet, pour générer et appairer la clé. |
| **Version minimale du proxy** | Information en lecture seule : la version minimale de TeslaBleHttpProxy prise en charge (2.3.0). |

### L'URL est normalisée à l'enregistrement

Vous n'avez pas à vous soucier de la forme exacte de l'adresse : à l'enregistrement, le plugin retire les espaces autour de l'URL, met `http`/`https` en minuscules et **ajoute le `/` final** si besoin. Après l'enregistrement, le champ affiche l'adresse corrigée.

L'URL est refusée, avec un message en rouge et sans que l'ancienne valeur soit modifiée, dans les cas suivants :

- elle est vide ou ne commence pas par `http://` ou `https://` ;
- elle contient des identifiants (`utilisateur:motdepasse@`) ;
- elle contient des caractères non admis (espaces au milieu, accents, paramètres `?...`, ancre `#...`), un port invalide, ou dépasse 255 caractères.

### Tester le proxy

Cliquez sur **Tester** : le plugin interroge la version du proxy (10 secondes au plus) et affiche le résultat sous le champ. Le test ne vérifie ni la clé appairée ni le véhicule : il prouve seulement que le proxy est joignable. Voir [Dépannage](#dépannage) pour le sens de chaque message.

### Lien vers le tableau de bord du proxy

Le lien apparaît dès qu'une URL valide est enregistrée (ou testée). Il pointe vers `<URL du proxy>dashboard`. Si vous avez déclaré le proxy par un **nom de service Docker** (par exemple `http://teslablehttpproxy:8080/`), Jeedom sait le joindre mais **votre navigateur non** : le lien ne s'ouvrira pas. Ouvrez alors le tableau de bord avec l'adresse IP du Raspberry Pi (`http://<ip_du_pi>:8080/dashboard`).

## Configuration des équipements

Chaque véhicule est un équipement. Rendez-vous dans **Plugins > Communication des objets > Tesla BLE**, cliquez sur **Ajouter** et donnez un nom au véhicule.

Dans l'onglet **Equipement** :

| Champ | Valeur attendue |
|---|---|
| **Nom de l'équipement** | Le nom du véhicule, au choix. |
| **Objet parent** | L'objet Jeedom dans lequel ranger le véhicule (ou **Aucun**). |
| **Catégorie** | Les catégories Jeedom de l'équipement (case à cocher). |
| **Activer** | Coché : le véhicule est rafraîchi toutes les 5 minutes. Décoché : il n'est plus lu. |
| **Visible** | Coché : le widget du véhicule est affiché sur le dashboard. |
| **VIN** | Le numéro de série du véhicule : **17 caractères**, chiffres et lettres **sauf I, O et Q** (exemple factice : `5YJ3E1EA7KF000000`). Il doit être celui déclaré dans TeslaBleHttpProxy. |
| **Description** | Texte libre, facultatif. |

Les boutons en haut de page sont ceux de tout équipement Jeedom : **Configuration avancée**, **Dupliquer**, **Sauvegarder** et **Supprimer**. L'onglet **Commandes** liste les commandes du véhicule (voir [Commandes](#commandes)).

À la sauvegarde :

- Le plugin crée les commandes manquantes de l'équipement. **Il ne lance aucun rafraîchissement** : la page répond tout de suite, même si le proxy est éteint. Les informations arrivent au prochain cycle de 5 minutes, ou immédiatement avec la commande **Rafraîchir**.
- La VIN est **normalisée** : espaces retirés, lettres mises en majuscules. Elle peut être laissée vide, mais le véhicule n'est alors pas lu (voir [Dépannage](#dépannage)).
- La VIN est **unique** : un véhicule ne peut avoir qu'un seul équipement. Une VIN invalide, ou déjà utilisée par un autre équipement, est refusée avec un message.
- **Dupliquer** un véhicule est donc **refusé** : la copie porte la même VIN. Pour un second véhicule, utilisez **Ajouter**.

## Mise à jour depuis la version 0.x

Vous mettez à jour le plugin depuis une version 0.x : rien n'est à refaire.

> **IMPORTANT**
>
> Vos **équipements, VIN, commandes, historiques, scénarios et réglages d'affichage sont conservés**. Les commandes gardent leurs identifiants : les scénarios, les widgets et les historiques qui les utilisent continuent de fonctionner sans modification.

### Noms des commandes

Un équipement **migré depuis la version 0.x garde les noms de ses commandes** (par exemple « Etat Charge », « Charge Start », « Rafraichir ») : seuls les identifiants comptent pour les scénarios. Les commandes d'un **nouvel équipement** portent les libellés du tableau de la section [Commandes](#commandes). Vous pouvez renommer librement une commande.

À la mise à jour, les commandes absentes de votre équipement sont ajoutées **en fin de liste** : **Temps de charge restant**, **Trappe de charge ouverte**, **Dernière erreur** et **Dernière lecture des données**. Sur un équipement existant, l'action d'ouverture de la trappe peut s'appeler « Trappe de Charge Ouvert » : renommez-la si besoin.

### Autonomie et vitesse de charge

Les commandes **Autonomie** et **Vitesse de Charge** sont désormais converties en km et km/h (le véhicule les envoie en miles). Les valeurs déjà enregistrées dans l'historique restent en miles : le graphique de l'**Autonomie** montre donc une **rupture** (un saut d'un facteur d'environ 1,6) au moment de la mise à jour. Les valeurs antérieures ne sont pas converties.

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

Le plugin ne réveille donc jamais le véhicule de lui-même, afin de ne pas vider la batterie. Tant que le véhicule dort, les informations de charge et de climatisation conservent leur dernière valeur connue. Pour les actualiser, utilisez la commande **Réveiller**, puis **Rafraîchir** quelques secondes plus tard.

Si le véhicule s'endort entre les deux requêtes, ce n'est pas une erreur : les informations de charge et de climatisation gardent leur dernière valeur et rien n'est affiché.

Si le véhicule est hors de portée Bluetooth du proxy, la commande **Présence véhicule** passe à 0. Si c'est le proxy qui ne répond pas, n'a pas de clé appairée ou répond trop lentement, la présence garde sa dernière valeur.

**Pourquoi les données ne bougent plus ?** L'information **Dernière erreur** donne la cause du dernier échec de lecture, suivie de la raison renvoyée par le proxy quand il en donne une (par exemple « Véhicule hors de portée — … » ou « Proxy sans clé : appairage à faire — … »). Elle revient à **Aucune** dès qu'un cycle de lecture réussit. Un véhicule qui dort n'est pas une erreur : **Dernière erreur** reste à **Aucune** et **Véhicule réveillé** vaut 0. L'information **Dernière lecture des données** indique depuis quand les données de charge et de climatisation datent.

Dans le log du plugin, un problème ne laisse que **deux lignes** : une quand il commence, une quand tout revient à la normale (`Véhicule « <nom> » (id <n>) : retour à la normale après [<catégorie>].`), même s'il dure des heures. Le niveau de la ligne de début dépend de la cause : **Info** pour un véhicule hors de portée (situation normale), **Erreur** pour une erreur de configuration (VIN ou URL manquante) ou un proxy trop ancien, **Avertissement** pour les autres. La ligne de fin est toujours au niveau **Info**. **Pour voir ces lignes, le log du plugin doit être au moins en niveau Info** (**Configuration du plugin > Logs**). Tant que le problème dure, le détail de chaque cycle reste visible en **Debug**.

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

Les tableaux ci-dessous donnent, pour chaque commande, son **identifiant** (`logicalId`, stable : c'est lui que les scénarios retrouvent), son type et son sous-type, et son unité. Les libellés sont ceux d'un **nouvel équipement** ; un équipement migré depuis la 0.x garde ses anciens noms (voir [Mise à jour depuis la version 0.x](#mise-à-jour-depuis-la-version-0x)).

### Informations

« H » : historisée par défaut. « V » : visible par défaut sur le widget. Vous pouvez changer ces deux réglages dans l'onglet **Commandes**.

| Libellé | Identifiant | Type / sous-type | Unité | H | V | Description |
|---|---|---|---|---|---|---|
| Présence véhicule | `isPresent` | info / binaire | | oui | oui | 1 si le proxy joint le véhicule en Bluetooth, 0 s'il est hors de portée |
| Véhicule réveillé | `vehicule_isAwake` | info / binaire | | oui | oui | 1 si le véhicule est éveillé, 0 s'il dort ou si son état de veille est inconnu |
| Verrouillage du véhicule | `vehicule_lock` | info / binaire | | oui | oui | 1 si le véhicule est verrouillé, y compris de l'intérieur, 0 s'il est déverrouillé, même partiellement |
| État charge | `charging_state` | info / texte | | non | oui | État de la charge renvoyé par le véhicule (`Charging`, `Stopped`, `Complete`, `Disconnected`...) |
| Limite charge | `charge_limit_soc` | info / numérique | % | oui | oui | Limite de charge configurée |
| Charge batterie | `usable_battery_level` | info / numérique | % | oui | oui | Niveau de batterie utilisable |
| Autonomie | `ideal_battery_range` | info / numérique | km | oui | non | Autonomie estimée, convertie en kilomètres (le véhicule la renvoie en miles) |
| Tension chargeur | `charger_voltage` | info / numérique | V | non | non | Tension délivrée par la borne |
| Vitesse de charge | `charge_rate` | info / numérique | km/h | non | non | Autonomie récupérée par heure de charge, convertie en km/h (le véhicule la renvoie en miles par heure) |
| Courant de charge (A) | `charge_amps` | info / numérique | A | oui | oui | Courant de charge configuré |
| Courant demande charge | `charge_current_request` | info / numérique | A | oui | oui | Courant demandé par le véhicule |
| Temps de charge | `minutes_to_full_charge` | info / texte | | non | oui | Temps restant avant la fin de la charge, au format `HHhMM` |
| Temps de charge restant | `charge_minutes_remaining` | info / numérique | min | non | non | Le même temps restant, en minutes (utilisable dans un scénario ou un graphique) |
| Trappe de charge ouverte | `charge_port_door_state` | info / binaire | | non | non | 1 si la trappe de charge est ouverte, 0 si elle est fermée |
| Verrouillage trappe charge | `charge_port_latch` | info / texte | | non | non | État du verrou du câble de charge, tel que renvoyé par le véhicule |
| Mode charge programmée | `scheduled_charging_mode` | info / texte | | non | non | Mode de charge programmée, tel que renvoyé par le véhicule |
| Heure départ programmée | `scheduled_departure_time` | info / texte | | non | non | Heure de départ programmée au format `HH:MM` (heure du véhicule) ; vide si aucun départ n'est programmé |
| Température intérieure | `inside_temp` | info / numérique | °C | oui | oui | Température dans l'habitacle, au dixième de degré |
| Température extérieure | `outside_temp` | info / numérique | °C | oui | oui | Température extérieure, au dixième de degré |
| Température conducteur | `driver_temp_setting` | info / numérique | °C | non | non | Consigne de climatisation côté conducteur |
| Température passager | `passenger_temp_setting` | info / numérique | °C | non | non | Consigne de climatisation côté passager |
| Climatisation activée | `is_climate_on` | info / binaire | | non | non | 1 si la climatisation fonctionne |
| Chauffage siège conducteur | `seat_heater_left` | info / numérique | | non | non | Niveau de chauffage du siège conducteur (0 à 3) |
| Chauffage siège passager | `seat_heater_right` | info / numérique | | non | non | Niveau de chauffage du siège passager (0 à 3) |
| Chauffage du volant | `steering_wheel_heater` | info / binaire | | non | non | 1 si le chauffage du volant est actif |
| Mode dégivrage | `defrost_mode` | info / texte | | non | non | État du dégivrage |
| Dernière erreur | `last_error` | info / texte | | non | oui | Cause du dernier échec de lecture ou de commande, suivie de la raison du proxy quand il en donne une ; **Aucune** quand tout va bien. Utilisable dans un scénario |
| Dernière lecture des données | `last_data_update` | info / texte | | non | oui | Date et heure (heure de Jeedom, `AAAA-MM-JJ HH:MM:SS`) de la dernière lecture réussie des données de charge et de climatisation |

Le niveau de batterie alimente aussi le suivi de batterie de Jeedom (page **Analyse > Equipements**).

Chaque information de charge et de climatisation est mise à jour indépendamment : si le véhicule ne renvoie pas l'une d'elles, elle garde sa dernière valeur et les autres sont tout de même actualisées.

### Actions

Les actions marquées « masquée » ne sont pas affichées sur le widget par défaut ; rendez-les visibles depuis l'onglet **Commandes** de l'équipement.

| Libellé | Identifiant | Type / sous-type | Unité | Description |
|---|---|---|---|---|
| Rafraîchir | `refresh` | action / autre | | Relance immédiatement la lecture des informations (une éventuelle erreur apparaît dans **Dernière erreur**) |
| Réveiller | `wake_up` | action / autre | | Réveille le véhicule, pour lire ses données de charge et de climatisation. Inutile avant une commande : le proxy réveille le véhicule seul |
| Démarrer la charge | `charge_start` | action / autre | | Démarre la charge |
| Arrêter la charge | `charge_stop` | action / autre | | Arrête la charge |
| Courant de charge | `set_charging_amps` | action / curseur | A | Règle le courant de charge (entier, entre le Min et le Max de la commande ; 0 à 32 A par défaut, augmentez le Max pour un véhicule 48 A) |
| Limite de charge | `set_charge_limit` | action / curseur | % | Règle la limite de charge, de 50 à 100 % |
| Démarrer le climatiseur | `auto_conditioning_start` | action / autre | | Lance le préconditionnement |
| Arrêter le climatiseur | `auto_conditioning_stop` | action / autre | | Arrête le préconditionnement |
| Ouvrir la trappe de charge | `charge_port_door_open` | action / autre | | Ouvre la trappe de charge (masquée) |
| Fermer la trappe de charge | `charge_port_door_close` | action / autre | | Ferme la trappe de charge (masquée) |
| Faire clignoter les feux | `flash_lights` | action / autre | | Fait clignoter les phares (masquée) |
| Klaxonner | `honk_horn` | action / autre | | Actionne le klaxon |
| Verrouiller les portes | `door_lock` | action / autre | | Verrouille le véhicule (masquée) |
| Déverrouiller les portes | `door_unlock` | action / autre | | Déverrouille le véhicule (masquée) |
| Mode sentinelle | `set_sentry_mode` | action / liste | | Active ou désactive le mode sentinelle (**Activé** ou **Désactivé**) (masquée) |

## Exemples d'utilisation

- **Charge solaire** : dans un scénario, ajustez **Courant de charge** en fonction de la production photovoltaïque.
- **Heures creuses** : déclenchez **Démarrer la charge** au début des heures creuses et **Arrêter la charge** à leur fin.
- **Préchauffage** : lancez **Démarrer le climatiseur** quelques minutes avant votre départ.
- **Alerte** : recevez une notification si **Verrouillage du véhicule** reste à 0 le soir.
- **Panne de liaison** : recevez une notification quand **Dernière erreur** passe à autre chose que **Aucune** (proxy injoignable, proxy sans clé appairée...). Un véhicule qui dort ne la déclenche pas.

## Limitations connues

- **Après une commande**, seuls la limite de charge, le courant de charge et le verrouillage sont mis à jour tout de suite. Les autres informations de charge et de climatisation sont à jour au cycle de 5 minutes suivant.
- **Véhicule endormi** : les informations de charge et de climatisation ne sont lues que véhicule réveillé (le plugin ne le réveille jamais de lui-même). Utilisez **Réveiller** puis **Rafraîchir**.
- **Clé Charging Manager** : le verrouillage, le klaxon, les feux et le mode sentinelle sont refusés par le véhicule (voir [Rôle de la clé](#rôle-de-la-clé)).
- **Un seul proxy** pour tous les véhicules, et **un seul équipement par véhicule** (VIN unique).
- **Heure de départ programmée historisée** : si elle était historisée avant la mise à jour, elle reste numérique et n'est plus mise à jour tant que son sous-type n'est pas changé en **Autre**.
- **Proxy déclaré par un nom de service Docker** : le lien vers le tableau de bord ne s'ouvre pas dans le navigateur (voir [Lien vers le tableau de bord du proxy](#lien-vers-le-tableau-de-bord-du-proxy)).

## Dépannage

Passez le log du plugin en niveau **Debug** (**Configuration du plugin > Logs**) pour voir chaque URL appelée et chaque réponse du proxy. Les lignes de début et de fin de panne exigent au moins le niveau **Info**.

Les messages sont classés selon l'endroit où vous les voyez.

### Messages du bouton Tester

| Message | Cause | Action |
|---|---|---|
| **« URL du proxy non renseignée »** | Le champ est vide. | Saisissez l'adresse du proxy. |
| **« URL invalide : elle doit commencer par http:// ou https://… »** | L'adresse est mal saisie (schéma absent, caractères non admis, port invalide). | Corrigez-la, par exemple `http://192.168.1.50:8080/`. Le `/` final est ajouté seul. |
| **« URL invalide : les identifiants (utilisateur:motdepasse@) ne sont pas pris en charge »** | L'adresse contient un identifiant. | Retirez `utilisateur:motdepasse@` : le proxy n'a pas d'authentification. |
| **« Proxy joignable — version X »** (vert) | Tout va bien. | Rien à faire. |
| **« Proxy joignable — version X »** + **« Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour »** (orange) | Le proxy répond mais sa version est trop ancienne. | Mettez-le à jour (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)). |
| **« Proxy joignable — version inconnue »** (vert) | Le proxy répond mais ne donne pas de numéro de version exploitable (installation manuelle par exemple). | Vérifiez la version à la main avec l'adresse de l'Astuce des prérequis. |
| **« Version du proxy non communiquée : proxy antérieur à 2.1.3, ou URL incorrecte »** (orange) | Le proxy répond « introuvable » à la question de version. | Vérifiez l'adresse et le port ; sinon mettez le proxy à jour. |
| **« Proxy injoignable »** (rouge, détail `cURL …`) | Rien ne répond à cette adresse. | Vérifiez l'adresse, le port, que le proxy est démarré et que le Raspberry Pi est allumé. |
| **« Délai dépassé »** (rouge) | Le proxy ne répond pas dans les 10 secondes. | Vérifiez le Raspberry Pi (alimentation, Wi-Fi), redémarrez le proxy. |
| **« Réponse invalide du proxy »** (rouge) | Ce qui répond n'est pas TeslaBleHttpProxy (mauvais port, autre service). | Vérifiez l'adresse et le port. |
| **« Aucune réponse du serveur Jeedom : consultez le log TeslaBLE »** | Jeedom n'a pas répondu au test au bout de 45 secondes. | Réessayez, puis consultez le log du plugin. |
| **« Erreur interne du plugin : consultez le log TeslaBLE »** | Erreur imprévue du plugin. | Consultez le log du plugin et signalez-la avec ce log. |

Le test n'interroge que la version du proxy : un test vert ne prouve ni que la clé est appairée, ni que le véhicule est à portée.

### Messages à l'enregistrement

- **« URL invalide : … »** (configuration du plugin) : mêmes causes que pour le bouton **Tester**. L'ancienne URL est conservée.
- **« VIN invalide : 17 caractères attendus, chiffres et lettres sauf I, O et Q »** : corrigez la VIN de l'équipement (les espaces sont retirés tout seuls).
- **« Cette VIN est déjà utilisée par l'équipement … »** : un autre équipement porte déjà cette VIN, ce qui arrive aussi avec **Dupliquer**. Supprimez le doublon ou corrigez la VIN.
- **« Erreur interne du plugin : consultez le log TeslaBLE »** : erreur imprévue lors de l'enregistrement ; le détail est dans le log du plugin.

### Centre de messages de Jeedom (après une mise à jour)

- **« La VIN de l'équipement … est invalide : corrigez-la dans sa page de configuration… »** : la VIN enregistrée par une ancienne version n'est pas valable. Corrigez-la.
- **« L'équipement … a la même VIN que l'équipement … »** : deux équipements pour un même véhicule. Supprimez le doublon ou corrigez sa VIN.
- **« L'information … est historisée : elle reste numérique et n'est plus mise à jour… »** : voir [Heure de départ programmée](#heure-de-départ-programmée).

### Information « Dernière erreur » (lecture)

| Texte affiché | Cause | Action |
|---|---|---|
| **Aucune** | Le dernier cycle de lecture a réussi (ou le véhicule dort, ce qui n'est pas une erreur). | Rien à faire. |
| **Proxy injoignable** | Le proxy ne répond pas à l'adresse configurée. | Vérifiez l'URL, que le proxy est démarré, l'alimentation et le Wi-Fi du Raspberry Pi. |
| **Délai dépassé** | Le proxy ou le véhicule répond trop lentement. | Vérifiez le Raspberry Pi (alimentation, Wi-Fi), redémarrez le proxy si cela se répète. |
| **Proxy sans clé : appairage à faire — …** | Le proxy n'a pas de clé appairée avec le véhicule. | Appairez la clé depuis le tableau de bord du proxy (lien dans la configuration du plugin). |
| **Véhicule hors de portée — …** | Le proxy ne trouve pas le véhicule en Bluetooth. La **Présence véhicule** passe à 0. | Rapprochez le Raspberry Pi du véhicule ; vérifiez que le proxy a le Bluetooth pour lui seul et que le véhicule n'a pas déjà 3 appareils connectés. |
| **Demande refusée par le véhicule — …** | Le véhicule a refusé la lecture ; la raison du proxy suit le message. | Lisez la raison indiquée après le message ; vérifiez aussi l'appairage de la clé. |
| **Fonction non supportée par ce proxy — …** | La lecture demandée n'existe pas dans votre version du proxy. | Mettez le proxy à jour. |
| **Réponse invalide du proxy** | Le proxy a renvoyé une réponse inattendue. | Vérifiez l'adresse, mettez le proxy à jour, redémarrez-le si cela se répète. |
| **Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour** | Le proxy est antérieur à 2.1.1 : l'état du véhicule n'est plus lisible. | Mettez le proxy à jour (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)). Le log signale aussi cette ligne en erreur. |
| **Le VIN n'est pas configuré pour cet équipement** | La VIN de l'équipement est vide. | Renseignez la VIN dans l'équipement puis sauvegardez. |
| **URL invalide : …** | L'URL du proxy est vide ou invalide dans la configuration du plugin. | Renseignez-la (voir [Configuration du plugin](#configuration-du-plugin)). |

Le texte est tronqué à 127 caractères. Un véhicule qui dort n'est pas une erreur : voir [Rafraîchissement des informations](#rafraîchissement-des-informations).

### Erreur à l'envoi d'une commande

Ces messages s'affichent en rouge dans Jeedom et sont aussi copiés dans **Dernière erreur**.

| Message | Cause | Action |
|---|---|---|
| **« Commande refusée par le véhicule (rôle de la clé du proxy insuffisant ?) : … »** | Votre clé a le rôle Charging Manager, qui n'autorise pas cette commande. | Voir [Rôle de la clé](#rôle-de-la-clé) : appairez une clé Owner. |
| **« Commande refusée par le véhicule : … »** | Le véhicule a refusé la commande ; la raison renvoyée suit le message. | Corrigez selon la raison indiquée. |
| **« Proxy injoignable, commande non envoyée »** | Le proxy ne répond pas : la commande n'est pas partie. | Vérifiez l'URL et l'alimentation du Raspberry Pi. |
| **« Délai dépassé : la commande a pu être exécutée, vérifiez l'état du véhicule »** ou **« Liaison avec le proxy interrompue : la commande a pu être exécutée… »** | Le véhicule a peut-être exécuté la commande malgré tout. | Contrôlez l'état du véhicule avant de la renvoyer. |
| **« Proxy occupé : commande non envoyée, réessayez dans un instant »** | Une autre commande ou lecture occupe le proxy depuis près de 2 minutes. | Réessayez. |
| **« Valeur invalide : le courant doit être un entier entre … et … A »** | Le courant est décimal, texte ou hors des bornes Min/Max de la commande. | Corrigez la valeur, ou augmentez le **Max** de **Courant de charge** si votre véhicule accepte plus de 32 A. |
| **« Valeur invalide : la limite doit être un entier entre 50 et 100 % »** | Limite hors bornes ou non entière. | Corrigez la valeur. |
| **« Valeur invalide : le mode sentinelle doit être activé ou désactivé »** | Valeur autre que **Activé** ou **Désactivé** (l'ancienne option « Aucun » n'existe plus). | Utilisez **Activé** ou **Désactivé**. |
| **« Échec de la commande : … »** | Autre cause (proxy sans clé, véhicule hors de portée, réponse invalide…) : la cause suit le message. | Voir le tableau **Dernière erreur** ci-dessus. |
| **« Commande non prise en charge par le plugin »** | La commande n'est pas l'une de celles du plugin (commande ajoutée à la main, ou identifiant modifié). | Ne modifiez pas l'identifiant des commandes du plugin. |

### Messages du log du plugin

- **« Cycle de rafraîchissement sauté : le cycle précédent n'est pas terminé. »** : la lecture précédente dure plus de 5 minutes, en général parce que le proxy ou le Raspberry Pi répond très lentement. Vérifiez l'alimentation et la connexion Wi-Fi du Raspberry Pi, puis redémarrez le proxy si cela se répète.
- **« Cycle de rafraîchissement écourté… véhicule(s) non lu(s) à ce cycle »** : le cycle a atteint sa durée maximale de 4 minutes ; les véhicules cités seront lus au cycle suivant. Si cela se répète, c'est que le proxy répond trop lentement : voir ci-dessus.
- **« Lecture du véhicule … reportée : proxy occupé… »** : une commande longue occupe le proxy ; la lecture est reportée au cycle suivant.
- **« Verrou du proxy indisponible… »** ou **« Verrou du cycle de rafraîchissement indisponible… »** : le plugin ne peut pas écrire dans le dossier temporaire de Jeedom. Vérifiez les droits de ce dossier ; le plugin continue de fonctionner sans la protection contre les échanges simultanés.
- **« Commandes : … le nom … est déjà pris… »** : le plugin n'a pas pu donner le libellé prévu à une commande parce qu'une autre commande de l'équipement le porte. Renommez l'une des deux, puis sauvegardez l'équipement.
- **« Migrations : … »** : voir [Constater la mise à niveau dans le log](#constater-la-mise-à-niveau-dans-le-log).

### Symptômes sans message

- **Présence véhicule reste à 0** : le proxy ne trouve pas le véhicule en Bluetooth. Rapprochez le Raspberry Pi du véhicule.
- **Les informations de charge ne bougent plus alors que Dernière erreur vaut Aucune** : le véhicule dort. C'est le comportement normal, voir [Rafraîchissement des informations](#rafraîchissement-des-informations).
- **Aucune requête n'aboutit** : testez l'URL avec le bouton **Tester** (le `/` final est géré par le plugin), puis depuis un navigateur.
- **Le lien du tableau de bord ne s'ouvre pas** alors que le proxy fonctionne : l'URL contient un nom de service Docker que votre navigateur ne connaît pas. Ouvrez `http://<ip_du_pi>:8080/dashboard`.
- **Le graphique de l'Autonomie fait un saut** : normal après la mise à jour depuis la 0.x (miles puis km), voir [Autonomie et vitesse de charge](#autonomie-et-vitesse-de-charge).
- **Je ne vois pas les lignes de début et de fin de panne dans le log** : passez le log du plugin au moins en niveau **Info**.
- **Le proxy ne répond plus au bout de quelques heures** : c'est un problème fréquent sur le Raspberry Pi Zero W de première génération. Redémarrez le proxy ou passez à un Raspberry Pi Zero 2 W.
- **Connexions Bluetooth intermittentes** : le véhicule n'accepte que 3 appareils connectés à la fois ; déconnectez un téléphone ou une montre.
