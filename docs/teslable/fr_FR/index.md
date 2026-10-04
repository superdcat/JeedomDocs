# Plugin Tesla BLE

Ce plugin permet de piloter la charge, la climatisation et quelques fonctions de base de vos véhicules **Tesla** depuis Jeedom, **en Bluetooth (BLE)** et sans passer par l'API cloud de Tesla.

Jeedom ne parle pas directement au véhicule : il s'appuie sur un proxy [TeslaBleHttpProxy](https://github.com/superdcat/TeslaBleHttpProxy) (le fork maintenu pour ce plugin, dérivé du projet de [wimaha](https://github.com/wimaha/TeslaBleHttpProxy)), installé sur un petit appareil équipé du Bluetooth (un Raspberry Pi, voir [Choisir et installer le Raspberry Pi](#choisir-et-installer-le-raspberry-pi)) placé à portée du véhicule, typiquement dans le garage. Le plugin interroge ce proxy en HTTP sur votre réseau local.

```
Jeedom  --HTTP-->  TeslaBleHttpProxy (Raspberry Pi)  --Bluetooth-->  Véhicule
```

## Prérequis

- Jeedom 4.5 minimum, sur Debian 11 ou 12.
- **TeslaBleHttpProxy 2.3.0 minimum**, installé, fonctionnel et joignable depuis Jeedom. L'**image du fork** `ghcr.io/superdcat/tesla-ble-http-proxy` est recommandée ; l'image de wimaha (2.3.0 ou plus récente) reste acceptée. Le plugin ignore le suffixe `-tb.N` des versions du fork : `2.3.0-tb.2` est jugée conforme à « 2.3.0 minimum ». Procédure complète pas à pas, sur un Raspberry Pi Zero 2 W : [Installer le proxy BLE](installation-proxy.md).
- La **clé du proxy appairée avec le véhicule**. Cette étape se fait entièrement dans l'interface de TeslaBleHttpProxy (génération de la clé, puis validation avec votre carte-clé dans le véhicule) : voir [Installer le proxy BLE](installation-proxy.md#8-générer-la-clé-et-lappairer-avec-le-véhicule).
- Le **VIN** de chaque véhicule à piloter (visible en bas de l'écran principal de l'application Tesla).

> **Astuce**
>
> Avant de configurer le plugin, vérifiez que le proxy répond en ouvrant dans un navigateur `http://<ip_du_proxy>:<port>/api/proxy/1/version` (version du proxy), puis `http://<ip_du_proxy>:<port>/api/1/vehicles/<VIN>/body_controller_state`. Vous devez obtenir une réponse JSON.

### Vérifier et mettre à jour la version du proxy

Le plugin exige **TeslaBleHttpProxy 2.3.0 minimum**. Suivez ces étapes pour connaître la version de votre proxy, puis la mettre à jour si besoin. Avec l'image du fork, la version est de la forme `2.3.0-tb.2` (version de base de wimaha, puis numéro de version du fork).

**1. Lire la version actuelle**

1. Sur un ordinateur du même réseau que le proxy, ouvrez un navigateur.
2. Dans la barre d'adresse, tapez `http://<ip_du_proxy>:<port>/api/proxy/1/version`, par exemple `http://192.168.1.50:8080/api/proxy/1/version`.
3. Lisez la réponse : elle contient `"version"` suivi de la version du proxy, par exemple `2.3.0` avec l'image de wimaha. Avec l'image du fork, la réponse contient aussi `"flavor":"superdcat"` et une version comme `2.3.0-tb.2`.

Si cette version est **2.3.0 ou plus récente**, vous n'avez rien à faire pour le plugin. Sinon, passez à l'étape 2.

**2. Mettre à jour l'image du proxy**

1. Connectez-vous en SSH au Raspberry Pi qui héberge le proxy.
2. Placez-vous dans le dossier qui contient le fichier `docker-compose.yml` du proxy (le dossier `TeslaBleHttpProxy` si vous avez suivi [Installer le proxy BLE](installation-proxy.md)) :

   ```
   cd TeslaBleHttpProxy
   ```

3. Dans `docker-compose.yml`, vérifiez la ligne `image:` : elle doit être `image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` (ou une version plus récente du fork). Si elle pointe vers l'image de wimaha, voir [Passer de l'image wimaha à l'image du fork](installation-proxy.md#passer-de-limage-wimaha-à-limage-du-fork). Si elle porte un numéro de version précis, changez ce numéro.
4. Téléchargez l'image puis relancez le proxy avec elle :

   ```
   docker compose pull && docker compose up -d
   ```

   Un redémarrage du Raspberry Pi ou `restart: always` **ne mettent pas l'image à jour** : voir [Mettre à jour l'image du proxy](installation-proxy.md#mettre-à-jour-limage-du-proxy).

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
| **Raspberry Pi Zero 2 W** | Recommandé : petit, peu gourmand, image Docker du proxy disponible pour ce processeur. |
| Raspberry Pi Zero W (première génération) | Déconseillé : processeur ARMv6 qui n'est plus pris en charge par les versions récentes de Docker, et adaptateur Bluetooth qui a tendance à se figer au bout de quelques heures. |
| Raspberry Pi 3, 4, 5 ou mini-PC avec Bluetooth | Convient, à condition d'être à portée du véhicule. |

La procédure détaillée, avec les commandes, les réglages et le dépannage, est sur la page [Installer le proxy BLE](installation-proxy.md). En résumé, l'installation consiste à :

1. Installer Raspberry Pi OS **64 bits Lite** et Docker.
2. Lancer l'image `ghcr.io/superdcat/tesla-ble-http-proxy` (fork recommandé ; l'image `wimaha/tesla-ble-http-proxy` reste une alternative).
3. Ouvrir `http://<ip_du_pi>:8080/dashboard`, générer la clé, saisir le VIN, **réveiller le véhicule**, envoyer la clé puis poser la carte-clé sur la console centrale pour valider.
4. Donner une **adresse IP fixe** au Raspberry Pi (réservation DHCP sur votre box), puisque son adresse est enregistrée dans le plugin.

Quelques conseils pour un fonctionnement stable :

- Utilisez une alimentation de qualité (5 V, 2,5 A) : une alimentation faible provoque des déconnexions Bluetooth.
- N'utilisez pas le Bluetooth de ce Raspberry Pi pour autre chose : le proxy a besoin de l'adaptateur pour lui seul.
- Un véhicule n'accepte que **3 appareils Bluetooth connectés en même temps** (téléphones, montre, proxy). Au-delà, les connexions deviennent intermittentes.

### Rôle de la clé

Avec TeslaBleHttpProxy (fork ou wimaha 2.3.0), la clé générée par défaut a le rôle **Charging Manager**. Elle suffit pour lire l'état du véhicule et piloter la charge, mais le véhicule **refuse** certaines commandes. Pour les utiliser, générez et appairez une clé de rôle **Owner** depuis le dashboard du proxy (lien dans la configuration du plugin).

| Rôle de la clé | Commandes concernées (liste indicative) |
|---|---|
| **Charging Manager** : fonctionne | Lectures (présence, verrouillage, charge, climatisation), **Rafraîchir**, **Réveiller**, **Démarrer la charge**, **Arrêter la charge**, **Courant de charge** |
| **Charging Manager** : refusé | **Verrouiller les portes**, **Déverrouiller les portes**, **Klaxonner**, **Faire clignoter les feux**, **Mode sentinelle** ; probablement aussi **Démarrer le climatiseur** et **Arrêter le climatiseur** |
| **Owner** | Toutes les commandes |

Cette liste est indicative : le véhicule décide.

**Le plugin reconnaît ce refus.** Quand l'une des commandes de la ligne « refusé » ci-dessus est refusée par le véhicule faute de droits :

- le message « Cette commande nécessite une clé de rôle Owner : la clé du proxy a probablement le rôle Charging Manager… » s'affiche (il est aussi copié dans **Dernière erreur**) ;
- l'information **Rôle de clé** de l'équipement passe à **Charging Manager** ;
- dans l'onglet **Commandes** de l'équipement, ces commandes portent un badge gris **Rôle insuffisant**.

Les commandes restent présentes et utilisables : un scénario qui les appelle reçoit le même message. Elles ne sont **pas grisées sur le dashboard** : fiez-vous à l'information **Rôle de clé**. Le plugin ne vous prévient pas à l'avance : c'est le premier refus qui révèle le rôle.

**Passer à une clé Owner.** Générez et appairez une clé de rôle **Owner** en suivant [Générer la clé et l'appairer avec le véhicule](installation-proxy.md#8-générer-la-clé-et-lappairer-avec-le-véhicule) (choix du rôle : [Choisir le rôle de la clé](installation-proxy.md#choisir-le-rôle-de-la-clé)). Relancez ensuite l'une de ces commandes : dès qu'elle réussit, **Rôle de clé** repasse à **Owner** et le badge disparaît au rechargement de la page.

Avec l'image du fork, le rôle de la clé active se lit aussi à la main : ouvrez `http://<ip_du_proxy>:<port>/api/proxy/1/capabilities` et regardez `key_role` (`owner` ou `charging_manager`, vide si aucune clé n'est installée) ; le plugin n'utilise pas cette information. Le comportement de la **Limite de charge** et de l'ouverture et de la fermeture de la trappe de charge avec une clé Charging Manager n'est pas confirmé : la [documentation du proxy](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md#step-3-generate-key-for-vehicle) ne cite que le réveil, le démarrage et l'arrêt de la charge et le courant de charge.

> **IMPORTANT**
>
> Le proxy n'a **aucune authentification** par défaut. Le fork peut exiger un jeton (`apiToken`) : saisissez alors le même dans **Jeton d'API du proxy** (voir [Configuration du plugin](#configuration-du-plugin)). Avec une clé Owner, n'importe quel appareil de votre réseau local peut déverrouiller le véhicule. Gardez le proxy sur un réseau de confiance, idéalement isolé, et n'exposez **jamais** son port sur Internet. Si vous ne pilotez que la charge, préférez une clé Charging Manager.

## Configuration du plugin

Après installation, activez le plugin puis ouvrez sa page de configuration (**Plugins > Gestion des plugins > Tesla BLE**). Elle comporte trois réglages : l'URL du proxy, le jeton d'API du proxy (facultatif) et le seuil d'alerte Bluetooth figé.

| Champ | Valeur attendue |
|---|---|
| **URL du proxy** | L'adresse de TeslaBleHttpProxy avec son port, par exemple `http://192.168.1.50:8080/`. Elle doit commencer par `http://` ou `https://`. Un seul proxy est utilisé pour tous les véhicules. |
| **Jeton d'API du proxy** | Facultatif : à renseigner seulement si le proxy du fork a un `apiToken` (même valeur). Le même jeton sert pour tous les proxys. Il est enregistré **chiffré** et **n'est jamais réaffiché** : le champ reste vide et indique « Jeton enregistré : laissez vide pour le conserver ». Laissez-le vide pour garder le jeton enregistré ; **Supprimer le jeton** l'efface. |
| **Tester** (bouton) | Vérifie que le proxy répond et affiche sa version. Il teste l'URL et le jeton saisis, **même non enregistrés** (champ jeton vide : le jeton enregistré). Il indique aussi l'authentification : **« Proxy sans authentification : aucun jeton requis »**, **« Jeton d'API accepté par le proxy »**, **« Le proxy exige un jeton d'API »** (aucun jeton saisi ni enregistré) ou **« Jeton d'API refusé par le proxy »** (jeton différent de `apiToken`). |
| **Ouvrir le tableau de bord du proxy (appairage des clés)** (lien) | Ouvre le tableau de bord du proxy dans un nouvel onglet, pour générer et appairer la clé. |
| **Logs du proxy** (bouton, ligne **Diagnostic**) | Affiche les dernières lignes de logs du proxy dans une fenêtre, sans session SSH sur le Raspberry Pi. Utilise l'URL **enregistrée**. |
| **Seuil d'alerte Bluetooth figé** | Nombre de lectures consécutives en délai dépassé, alors que le proxy répond, avant de vous prévenir que l'adaptateur Bluetooth du Raspberry Pi est probablement figé. Entier de 2 à 288 (une lecture a lieu à l'intervalle de rafraîchissement du véhicule, 5 minutes par défaut : 288 = un jour de lectures à ce défaut) ; laissez vide pour la valeur par défaut, **3**, affichée en grisé. Voir [Alerte adaptateur Bluetooth figé](#alerte-adaptateur-bluetooth-figé). |
| **Version minimale du proxy** | Information en lecture seule : la version minimale de TeslaBleHttpProxy prise en charge (2.3.0). |

### L'URL est normalisée à l'enregistrement

Vous n'avez pas à vous soucier de la forme exacte de l'adresse : à l'enregistrement, le plugin retire les espaces autour de l'URL, met `http`/`https` en minuscules et **ajoute le `/` final** si besoin : le `/` final et la casse de `http://` n'ont donc aucune importance, `HTTP://192.168.1.50:8080` et `http://192.168.1.50:8080/` désignent le même proxy. Après l'enregistrement, le champ affiche l'adresse corrigée.

L'URL est refusée, avec un message en rouge et sans que l'ancienne valeur soit modifiée, dans les cas suivants :

- elle est vide ou ne commence pas par `http://` ou `https://` ;
- elle contient des identifiants (`utilisateur:motdepasse@`) ;
- elle contient des caractères non admis (espaces au milieu, accents, paramètres `?...`, ancre `#...`), un port invalide, ou dépasse 255 caractères.

### Tester le proxy

Cliquez sur **Tester** : le plugin interroge la version du proxy (10 secondes au plus) et affiche le résultat sous le champ. Le test ne vérifie ni la clé appairée ni le véhicule : il prouve seulement que le proxy est joignable. Voir [Dépannage](#dépannage) pour le sens de chaque message.

### Lien vers le tableau de bord du proxy

Le lien apparaît dès qu'une URL valide est enregistrée (ou testée). Il pointe vers `<URL du proxy>dashboard`. Si vous avez déclaré le proxy par un **nom de service Docker** (par exemple `http://teslablehttpproxy:8080/`), Jeedom sait le joindre mais **votre navigateur non** : le lien ne s'ouvrira pas. Ouvrez alors le tableau de bord avec l'adresse IP du Raspberry Pi (`http://<ip_du_pi>:8080/dashboard`).

### Consulter les logs du proxy

Le bouton **Logs du proxy** ouvre une fenêtre qui affiche les **200 dernières lignes** de logs du proxy (la plus récente en bas), avec leur heure dans le fuseau de Jeedom et leur niveau (`[DEBUG]`, `[INFO]`, `[WARN]`, `[ERROR]`). Le bouton **Rafraîchir** relit les logs. La lecture ne sollicite pas le véhicule et répond en 10 secondes au plus, même pendant qu'une commande occupe le proxy.

- La fonction demande le proxy **2.3.0** ou plus récent et utilise l'URL **enregistrée** : après avoir changé l'URL, sauvegardez avant d'ouvrir les logs.
- Les lignes sont affichées **telles quelles**, en texte brut : un contenu comme `<script>` ou `&` apparaît littéralement, sans aucun effet. Chaque ligne est limitée à 1000 caractères.
- Les VIN sont masquées (seuls les 4 derniers caractères restent visibles). Les lignes peuvent contenir l'adresse IP des clients du proxy et le contenu des commandes envoyées : relisez une capture avant de la publier sur un forum.
- Le proxy conserve aussi ses lignes **Debug**, quel que soit son niveau de log : les 200 lignes couvrent donc souvent moins d'une heure d'activité. Ses logs sont effacés à chaque redémarrage du proxy.
- Les lignes du proxy ne sont jamais recopiées dans le log du plugin. Fonction réservée aux administrateurs Jeedom.

Voir [Messages de la fenêtre Logs du proxy](#messages-de-la-fenêtre-logs-du-proxy) en cas de message d'erreur.

### Alerte adaptateur Bluetooth figé

Sur certains Raspberry Pi (notamment le Zero W de première génération), l'adaptateur Bluetooth se fige au bout de quelques heures : le proxy répond toujours (le bouton **Tester** est vert, **Proxy joignable** vaut 1) mais chaque lecture du véhicule expire. Le plugin repère cette situation et vous prévient :

- quand la lecture de l'état d'un véhicule dépasse son délai **3 fois de suite** (ou le seuil réglé) alors que le proxy répond, un message **« Adaptateur Bluetooth du proxy probablement figé — … »** apparaît dans le centre de messages de Jeedom, **une seule fois** tant que la situation dure ;
- pendant ce temps, **Dernière erreur** affiche **« Adaptateur Bluetooth du proxy probablement figé : redémarrez le Raspberry Pi »** ;
- dès qu'une lecture réussit à nouveau (y compris un véhicule endormi qui répond), le log note le retour à la normale (niveau **Info**) et l'alerte est réarmée : une nouvelle série déclenchera un nouveau message, qui remplace l'ancien.

Un délai dépassé isolé, un véhicule hors de portée ou un proxy éteint ne déclenchent pas l'alerte. Le message reste dans le centre de messages après le retour à la normale : supprimez-le vous-même. Avec plusieurs véhicules sur le même proxy, chaque véhicule a son propre message. Les clics sur **Rafraîchir** comptent comme des lectures.

Que faire : redémarrez le Raspberry Pi qui héberge le proxy. Si cela se répète, passez à un Raspberry Pi Zero 2 W et utilisez une alimentation de qualité (5 V, 2,5 A).

## Configuration des équipements

Chaque véhicule est un équipement. Rendez-vous dans **Plugins > Communication des objets > Tesla BLE**, cliquez sur **Ajouter** et donnez un nom au véhicule.

Dans l'onglet **Equipement** :

| Champ | Valeur attendue |
|---|---|
| **Nom de l'équipement** | Le nom du véhicule, au choix. |
| **Objet parent** | L'objet Jeedom dans lequel ranger le véhicule (ou **Aucun**). |
| **Catégorie** | Les catégories Jeedom de l'équipement (case à cocher). |
| **Activer** | Coché : le véhicule est rafraîchi à son **intervalle de rafraîchissement** (5 minutes par défaut). Décoché : il n'est plus lu, quel que soit son intervalle. |
| **Visible** | Coché : le widget du véhicule est affiché sur le dashboard. |
| **VIN** | Le numéro de série du véhicule : **17 caractères**, chiffres et lettres **sauf I, O et Q** (exemple factice : `5YJ3E1EA7KF000000`). Il doit être celui déclaré dans TeslaBleHttpProxy. |
| **URL du proxy de ce véhicule** | Facultatif. L'adresse du proxy du garage de ce véhicule, avec son port (par exemple `http://192.168.1.51:8080/`). **Vide : le véhicule utilise l'URL de la configuration du plugin.** |
| **Tester ce proxy** (bouton) | Affiche la version du proxy que ce véhicule utilise. Il teste la valeur saisie, **même non enregistrée** ; champ vide : c'est l'URL de la configuration du plugin qui est testée. |
| **Intervalle de rafraîchissement** | Fréquence de lecture de ce véhicule : **1, 2, 5, 10, 15 ou 30 minutes**. Par défaut **5 minutes** (les véhicules existants gardent ce comportement après la mise à jour). Plus l'intervalle est court, plus les informations sont fraîches, mais plus le proxy est sollicité et, véhicule éveillé, plus sa mise en veille peut être retardée ; un intervalle long ménage le Raspberry Pi. **1 minute** convient à un ou deux véhicules par proxy (recommandé ; à ajuster selon votre installation) : au-delà, une lecture lente peut dépasser la minute. Une valeur inconnue est ramenée à 5 minutes. Un changement prend effet à la lecture suivante, sans redémarrage. Cette lecture ne réveille jamais le véhicule. |
| **Description** | Texte libre, facultatif. |

Les boutons en haut de page sont ceux de tout équipement Jeedom : **Configuration avancée**, **Dupliquer**, **Sauvegarder** et **Supprimer**. L'onglet **Commandes** liste les commandes du véhicule (voir [Commandes](#commandes)).

À la sauvegarde :

- Le plugin crée les commandes manquantes de l'équipement. **Il ne lance aucun rafraîchissement** : la page répond tout de suite, même si le proxy est éteint. Les informations arrivent à la prochaine lecture (dans la minute qui suit pour un véhicule neuf), ou immédiatement avec la commande **Rafraîchir**.
- La VIN est **normalisée** : espaces retirés, lettres mises en majuscules. Elle peut être laissée vide, mais le véhicule n'est alors pas lu (voir [Dépannage](#dépannage)).
- La VIN est **unique** : un véhicule ne peut avoir qu'un seul équipement. Une VIN invalide, ou déjà utilisée par un autre équipement, est refusée avec un message.
- **Dupliquer** un véhicule est donc **refusé** : la copie porte la même VIN. Pour un second véhicule, utilisez **Ajouter**.
- L'**URL du proxy de ce véhicule** est normalisée comme celle de la configuration du plugin (voir [L'URL est normalisée à l'enregistrement](#lurl-est-normalisée-à-lenregistrement)) ; une URL invalide est refusée avec le même message.

### Un proxy par véhicule (plusieurs garages)

Si vos véhicules sont garés à des endroits différents, chacun avec son Raspberry Pi, renseignez sur chaque équipement l'**URL du proxy de ce véhicule**. Toutes ses lectures et commandes passent alors par ce proxy, et le lien **Ouvrir le tableau de bord du proxy** de la section d'appairage pointe vers lui. Si un proxy s'arrête, seuls les véhicules qui l'utilisent passent en erreur. Vider le champ ramène le véhicule sur l'URL de la configuration du plugin au cycle suivant ; ses commandes et son historique ne changent pas.

- Écrivez un même proxy **toujours avec la même URL** (même adresse IP ou même nom, même port) : le plugin reconnaît un proxy à son URL.
- Le bouton **Logs du proxy** de la configuration du plugin affiche les logs du proxy de la **configuration du plugin** seulement.

### Appairer ma clé et vérifier l'appairage

Sous le champ **VIN**, la section **Appairer ma clé** rappelle les étapes de l'appairage, qui se fait dans le tableau de bord du proxy (détail : [Générer la clé et l'appairer avec le véhicule](installation-proxy.md#8-générer-la-clé-et-lappairer-avec-le-véhicule)). Une fois la VIN enregistrée et l'URL du proxy renseignée, elle affiche aussi le lien **Ouvrir le tableau de bord du proxy** (nouvel onglet), la VIN à recopier dans **Setup Vehicle**, et le bouton **Vérifier l'appairage**.

**Vérifier l'appairage** lit l'état du véhicule par le proxy **sans le réveiller** (50 secondes au plus) et n'envoie aucune commande. Le plugin ne génère ni ne supprime jamais de clé : seul le tableau de bord du proxy le fait.

| Message | Ce qu'il faut faire |
|---|---|
| **Appairage vérifié : le véhicule répond à la clé du proxy** | Rien. Avec l'image du fork, la ligne **Rôle de la clé active du proxy** indique en plus Owner ou Charging Manager. L'information **Rôle de clé** de l'équipement, elle, ne change qu'à la prochaine commande réservée (voir [Rôle de la clé](#rôle-de-la-clé)). |
| **Proxy sans clé : …** | Aucune clé sur le proxy : générez-en une (**Generate**), puis envoyez-la au véhicule. |
| **Clé non appairée avec ce véhicule : …** | Réveillez le véhicule, envoyez la clé (**Send key**), puis posez la carte-clé sur la console centrale. |
| **Véhicule hors de portée Bluetooth du proxy : …** | Rapprochez le véhicule ou le Raspberry Pi, vérifiez la VIN. |
| **Proxy injoignable : …** | Vérifiez que le proxy est démarré, puis son adresse avec le bouton **Tester ce proxy** de l'équipement. |
| **Proxy occupé par une commande ou une lecture : …** | Relancez la vérification dans un instant. |

La vérification utilise la VIN **enregistrée** : sauvegardez l'équipement après l'avoir modifiée.

## Topologies : un ou plusieurs proxys, un ou plusieurs véhicules

Le plugin sait piloter plusieurs véhicules, avec un seul proxy ou avec plusieurs. Une URL de proxy se saisit à deux endroits : dans la **configuration du plugin** (l'adresse par défaut, utilisée par tous les véhicules qui n'ont pas la leur) et, facultativement, dans le champ **URL du proxy de ce véhicule** de chaque équipement.

### Schémas

Un Raspberry Pi, plusieurs véhicules (même garage) : l'URL se saisit **une seule fois**, dans la configuration du plugin ; le champ de chaque véhicule reste vide.

```
Jeedom ---> Proxy du garage (Raspberry Pi A) --BLE--> Véhicule 1 (VIN 1)
                                             --BLE--> Véhicule 2 (VIN 2)

URL : configuration du plugin  = http://192.168.1.50:8080/
URL : champ de chaque véhicule = vide
```

Plusieurs Raspberry Pi, plusieurs garages : l'URL de chaque proxy se saisit **dans l'équipement de chaque véhicule**. La configuration du plugin peut rester sur le proxy principal (elle sert de valeur par défaut et au bouton **Logs du proxy**).

```
Jeedom ---> Proxy du garage A (Raspberry Pi A) --BLE--> Véhicule 1
       |
       +--> Proxy du garage B (Raspberry Pi B) --BLE--> Véhicule 2

URL : configuration du plugin  = http://192.168.1.50:8080/   (proxy A, par défaut)
URL : champ du véhicule 1      = vide (ou http://192.168.1.50:8080/)
URL : champ du véhicule 2      = http://192.168.1.51:8080/
```

### Ajouter un second véhicule sur le même proxy

Le proxy, le Raspberry Pi et l'URL de la configuration du plugin sont déjà en place pour le premier véhicule. Pour le second :

1. Dans **Plugins > Communication des objets > Tesla BLE**, cliquez sur **Ajouter** (et non **Dupliquer**, refusé : la VIN est unique), nommez le véhicule, saisissez sa **VIN** et laissez **URL du proxy de ce véhicule** vide. **Sauvegardez**.
2. Dans la section **Appairer ma clé** de ce nouvel équipement, cliquez sur **Ouvrir le tableau de bord du proxy**.
3. Dans le tableau de bord, saisissez la VIN du second véhicule dans **Setup Vehicle**, réveillez ce véhicule, cliquez sur **Send key**, puis posez la carte-clé sur sa console centrale pour valider. C'est **la même clé** du proxy qui doit être appairée sur chaque véhicule : ne générez pas une seconde clé. Voir [Rôle de la clé](#rôle-de-la-clé) pour le choix du rôle.
4. Revenez dans l'équipement et cliquez sur **Vérifier l'appairage** : attendez **Appairage vérifié : le véhicule répond à la clé du proxy**. Sinon, voir le tableau de [Appairer ma clé et vérifier l'appairage](#appairer-ma-clé-et-vérifier-lappairage).
5. Cliquez sur **Rafraîchir** (ou attendez une minute) : les informations du second véhicule apparaissent.

Un véhicule n'accepte que **3 appareils Bluetooth connectés en même temps** (téléphones, montre, proxy) : au-delà, les connexions deviennent intermittentes. Chaque véhicule garde sa propre **Dernière erreur** : un véhicule hors de portée ou dont la clé n'est pas appairée ne gêne pas l'autre. Ils partagent en revanche le même Raspberry Pi : les échanges se font l'un après l'autre (voir [Pourquoi les appels sont séquentiels](#pourquoi-les-appels-sont-séquentiels)).

### Ajouter un second proxy pour un autre garage

1. Installez le proxy du second garage sur son propre Raspberry Pi, avec une adresse IP fixe (voir [Installer le proxy BLE](installation-proxy.md)), puis générez la clé et appairez-la avec le véhicule de ce garage.
2. Dans l'équipement de ce véhicule, saisissez dans **URL du proxy de ce véhicule** l'adresse du second proxy, avec son port, par exemple `http://192.168.1.51:8080/`.
3. Cliquez sur **Tester ce proxy** : le message **Proxy joignable — version X** confirme que **ce** proxy répond (le test porte sur la valeur saisie, même non enregistrée). Sinon, voir [Messages du bouton Tester](#messages-du-bouton-tester).
4. **Sauvegardez**, puis utilisez **Vérifier l'appairage** pour contrôler la clé de ce véhicule.
5. Le lien **Ouvrir le tableau de bord du proxy** de cet équipement ouvre alors le tableau de bord du second proxy.

La fenêtre **Logs du proxy** de la configuration du plugin ne montre que le proxy de la **configuration du plugin** : pour lire les logs du second proxy, ouvrez le sien dans un navigateur (`http://<ip_du_second_pi>:8080/dashboard`). Chaque véhicule a sa propre information **Proxy joignable**, et l'alerte d'adaptateur figé est propre à chaque véhicule. Le même jeton d'API sert pour tous les proxys.

## Mise à jour depuis la version 0.x

Vous mettez à jour le plugin depuis une version 0.x : rien n'est à refaire.

> **IMPORTANT**
>
> Vos **équipements, VIN, commandes, historiques, scénarios et réglages d'affichage sont conservés**. Les commandes gardent leurs identifiants : les scénarios, les widgets et les historiques qui les utilisent continuent de fonctionner sans modification.

### Noms des commandes

Un équipement **migré depuis la version 0.x garde les noms de ses commandes** (par exemple « Etat Charge », « Charge Start », « Rafraichir ») : seuls les identifiants comptent pour les scénarios. Les commandes d'un **nouvel équipement** portent les libellés du tableau de la section [Commandes](#commandes). Vous pouvez renommer librement une commande.

À la mise à jour, les commandes absentes de votre équipement sont ajoutées **en fin de liste** : **Temps de charge restant**, **Trappe de charge ouverte**, **Dernière erreur**, **Dernière lecture des données**, **Proxy joignable**, **Version du proxy**, **Rôle de clé** (qui vaut **Indéterminé** jusqu'à la première commande réservée au rôle Owner), **Durée lecture état** et **Durée lecture données** (vides jusqu'à la première lecture réussie). Sur un équipement existant, l'action d'ouverture de la trappe peut s'appeler « Trappe de Charge Ouvert » : renommez-la si besoin.

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

À l'**intervalle de chaque véhicule** (5 minutes par défaut, réglable de 1 à 30 minutes dans l'équipement), le plugin rafraîchit ce véhicule en deux temps :

1. Il interroge l'état du **contrôleur de carrosserie** (`body_controller_state`). Cette requête ne réveille pas le véhicule. Elle met à jour la présence, le verrouillage et l'état de veille.
2. **Uniquement si le véhicule est réveillé**, il récupère les données complètes (`vehicle_data`) : charge, batterie, autonomie et climatisation.

Une tâche de Jeedom, **TeslaBLE::cycleRafraichissement**, se déclenche **chaque minute** et ne lit que les véhicules actifs dont l'intervalle est écoulé (mesuré depuis le début de leur dernière lecture) : avec un véhicule à 1 minute et un autre à 15 minutes, le premier est lu à chaque passage et le second environ toutes les 15 minutes. Un véhicule qui n'a encore jamais été lu l'est dès le passage suivant. Un proxy dont aucun véhicule n'est à lire n'est pas sollicité. Cette tâche est créée à l'activation et à la mise à jour du plugin (voir [Dépannage](#dépannage)).

Le plugin ne réveille donc jamais le véhicule de lui-même, afin de ne pas vider la batterie. Tant que le véhicule dort, les informations de charge et de climatisation conservent leur dernière valeur connue. Pour les actualiser, utilisez la commande **Réveiller**, puis **Rafraîchir** quelques secondes plus tard.

Si le véhicule s'endort entre les deux requêtes, ce n'est pas une erreur : les informations de charge et de climatisation gardent leur dernière valeur et rien n'est affiché.

Si le véhicule est hors de portée Bluetooth du proxy, la commande **Présence véhicule** passe à 0. Si c'est le proxy qui ne répond pas, n'a pas de clé appairée ou répond trop lentement, la présence garde sa dernière valeur.

**Plusieurs véhicules sur un même proxy.** Les véhicules d'un même proxy sont lus l'un après l'autre, chacun avec sa propre **Dernière erreur** et sa propre **Dernière lecture des données** : un véhicule hors de portée ou dont la clé n'est pas appairée n'empêche pas la lecture des autres. Le cycle dure au plus 4 minutes ; avec 3 véhicules ou moins sur un même proxy, il n'est jamais écourté, même au pire cas. Au-delà, les derniers véhicules peuvent ne pas être lus : vérifiez leur **Dernière lecture des données**. Quand un cycle est écourté, le log reçoit **un seul** avertissement par épisode (« Avertissement non répété jusqu'au prochain cycle complet. »), puis une ligne **Info** au premier cycle de nouveau complet.

**Pourquoi les données ne bougent plus ?** L'information **Dernière erreur** donne la cause du dernier échec de lecture, suivie de la raison renvoyée par le proxy quand il en donne une (par exemple « Véhicule hors de portée — … » ou « Proxy sans clé : appairage à faire — … »). Elle revient à **Aucune** dès qu'un cycle de lecture réussit. Un véhicule qui dort n'est pas une erreur : **Dernière erreur** reste à **Aucune** et **Véhicule réveillé** vaut 0. L'information **Dernière lecture des données** indique depuis quand les données de charge et de climatisation datent.

Dans le log du plugin, un problème ne laisse que **deux lignes** : une quand il commence, une quand tout revient à la normale (`Véhicule « <nom> » (id <n>) : retour à la normale après [<catégorie>].`), même s'il dure des heures. Le niveau de la ligne de début dépend de la cause : **Info** pour un véhicule hors de portée (situation normale), **Erreur** pour une erreur de configuration (VIN ou URL manquante) ou un proxy trop ancien, **Avertissement** pour les autres. La ligne de fin est toujours au niveau **Info**. **Pour voir ces lignes, le log du plugin doit être au moins en niveau Info** (**Configuration du plugin > Logs**). Tant que le problème dure, le détail de chaque cycle reste visible en **Debug**.

Les véhicules d'un même proxy sont rafraîchis **l'un après l'autre** ; les proxys différents sont lus **en parallèle**. Un véhicule hors de portée ou en erreur n'empêche pas la lecture des suivants, et l'erreur est consignée dans le log avec le nom du véhicule.

- Si un cycle dure plus longtemps que l'intervalle, Jeedom **saute** les passages suivants tant qu'il n'est pas terminé : les cycles ne se cumulent jamais. Le plugin l'écrit alors dans le log à la fin du cycle (un avertissement par heure au plus si l'intervalle réglé n'est pas tenu) ; la cadence reprend dès que le cycle est fini.
- Un cycle ne dépasse pas **4 minutes** : s'il y a beaucoup de véhicules ou si le proxy est lent, les véhicules restants sont lus au cycle suivant (avertissement nommant ces véhicules).
- Pendant qu'une commande, un **Rafraîchir** ou une vérification d'appairage est en cours ou attend le même proxy, la lecture du cycle est sautée sans erreur ; la lecture suivante rattrape.
- Avec plusieurs proxys, le cycle lit les proxys en parallèle : un proxy arrêté, éteint, figé ou lent ne retarde que ses propres véhicules (un proxy arrêté coûte quelques secondes, jusqu'à environ 5 s, par véhicule de ce proxy), jamais ceux des autres proxys. Le cycle dure autant que son proxy le plus lent. Deux proxys différents ne s'attendent jamais, y compris dans le cycle périodique ; les commandes et **Rafraîchir** des autres proxys ne sont pas retardés non plus.

### Exécution des commandes

Chaque commande action est transmise au proxy, qui attend la confirmation du véhicule avant de répondre. Le plugin n'a pas besoin de réveiller le véhicule avant une commande : le proxy s'en charge.

**Valeurs contrôlées avant l'envoi.** Une valeur invalide est refusée tout de suite, avec un message, sans rien envoyer au proxy :

- **Courant de charge** : un nombre entier compris entre le **Min** et le **Max** de la commande (0 à 32 A par défaut). Pour un véhicule qui accepte davantage, par exemple 48 A, augmentez le **Max** dans l'onglet **Commandes** de l'équipement. Une valeur décimale (`16,5`) ou un texte est refusé.
- **Limite de charge** : un nombre entier compris entre 50 et 100 %.
- **Mode sentinelle** : **Activé** ou **Désactivé** (l'ancienne option « Aucun » n'existe plus).

**En cas d'échec.** Si le proxy ou le véhicule refuse la commande, un message d'erreur apparaît en rouge dans l'interface de Jeedom (et dans le log du plugin en erreur), et il est aussi enregistré dans l'information **Dernière erreur**, où il reste affiché jusqu'au prochain cycle de lecture réussi (à la lecture suivante, 5 minutes au plus par défaut). Par exemple « Cette commande nécessite une clé de rôle Owner : la clé du proxy a probablement le rôle Charging Manager… » quand une commande réservée au rôle Owner est refusée : voir [Rôle de la clé](#rôle-de-la-clé).

**Après une commande réussie.** La limite de charge, le courant de charge et le verrouillage sont mis à jour immédiatement, puis l'état du véhicule (présence, éveil) est relu sans le réveiller. Les autres informations de charge et de climatisation sont actualisées à la lecture suivante du véhicule (5 minutes par défaut).

**Une commande ou une lecture à la fois.** Les échanges avec un même proxy se font l'un après l'autre : une commande, un **Rafraîchir** ou une vérification d'appairage n'attend que les échanges déjà en cours ou déjà en attente sur ce proxy (jusqu'à 2 minutes environ, 15 secondes pour la vérification) et passe avant les lectures périodiques, qui s'effacent et reprennent au cycle suivant. L'ordre de passage n'est pas garanti entre plusieurs demandes simultanées. Deux proxys différents ne s'attendent jamais, cycle périodique compris (le cycle lit les proxys en parallèle : voir Rafraîchissement). Si le proxy et le véhicule sont à la limite de leurs délais, la réponse peut prendre 3 à 4 minutes. Jeedom reste utilisable pendant ce temps.

### Pourquoi les appels sont séquentiels

Un proxy n'a qu'**un seul adaptateur Bluetooth** et une seule file d'échanges avec les véhicules : deux demandes envoyées en même temps se gêneraient. Le plugin fait donc passer les échanges d'un même proxy **l'un après l'autre**, tous véhicules confondus (lectures du cycle, commandes, **Rafraîchir**, **Vérifier l'appairage**).

- **Un même proxy** : un seul échange à la fois. Si une commande est en cours, la lecture du cycle s'efface et reprend au passage suivant (la minute d'après) ; une commande ou un **Rafraîchir** attend son tour. Quand l'attente dure trop longtemps (environ 2 minutes), le plugin renonce et affiche **Proxy occupé** : relancez dans un instant (voir [Dépannage](#dépannage)).
- **Des proxys différents** : ils sont lus **en parallèle** et ne s'attendent jamais. Un proxy lent ou arrêté ne retarde que ses propres véhicules ; le cycle dure autant que son proxy le plus lent.
- **Au pire cas** (proxy très lent, chaque lecture allant à son délai maximal), un cycle de 4 minutes lit **3 véhicules par proxy** au plus ; au-delà, les derniers peuvent ne pas être lus à ce cycle. En pratique, une lecture dure quelques secondes.

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
| Proxy joignable | `proxy_reachable` | info / binaire | | non | oui | 1 si le proxy a répondu au dernier cycle de rafraîchissement, 0 s'il est éteint, injoignable, ne répond pas dans les délais ou renvoie autre chose qu'une réponse valide du proxy (adresse erronée, proxy trop ancien). Un véhicule hors de portée ou endormi ne le fait pas passer à 0. Utilisable dans un scénario |
| Version du proxy | `proxy_version` | info / texte | | non | oui | Version renvoyée par le proxy au dernier cycle (**inconnue** si elle est illisible) ; garde sa dernière valeur quand le proxy ne répond pas |
| Rôle de clé | `key_role` | info / texte | | non | oui | Rôle probable de la clé du proxy pour ce véhicule : **Charging Manager** après le refus d'une commande réservée au rôle Owner faute de droits, **Owner** dès qu'une de ces commandes réussit, **Indéterminé** tant qu'aucune n'a été envoyée (voir [Rôle de la clé](#rôle-de-la-clé)). Dans un scénario, testez `Owner` ou `Charging Manager` (jamais traduits) ; « Indéterminé » suit la langue de Jeedom |
| Durée lecture état | `state_read_duration` | info / numérique | s | non | oui | Temps, en secondes au dixième, de la dernière lecture réussie de l'état du véhicule (présence, verrouillage, veille) au cycle de rafraîchissement ou par **Rafraîchir**. Un échec ne la modifie pas : elle garde la durée du dernier succès. Historisez-la pour suivre la santé de la liaison Bluetooth (voir [Lecture lente du proxy](#lecture-lente-du-proxy)) |
| Durée lecture données | `data_read_duration` | info / numérique | s | non | oui | Temps de la dernière lecture réussie des données de charge et de climatisation. Inchangée tant que le véhicule dort (aucune lecture). Une valeur proche de 0 est normale juste après une autre lecture : le proxy garde ces données en mémoire 30 secondes |

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

### Exemple pas à pas : être alerté quand le proxy est injoignable

L'information **Proxy joignable** vaut 1 tant que le proxy répond au cycle de rafraîchissement (publiée à chaque passage où un véhicule de ce proxy est lu, selon son intervalle) et passe à 0 quand il est éteint, injoignable ou ne répond pas dans les délais. Un véhicule hors de portée ou endormi ne la fait pas passer à 0. Créez un scénario qui vous prévient :

1. Ouvrez **Outils > Scénarios**, cliquez sur **Ajouter** et nommez le scénario, par exemple « Alerte proxy Tesla ». Dans **Mode du scénario**, choisissez **Provoqué** (le scénario se lance quand son déclencheur change).
2. Dans **Déclencheur(s)**, cliquez sur **+ Déclencheur** et choisissez la commande **Proxy joignable** de votre véhicule. Elle s'écrit `#[Objet][Véhicule][Proxy joignable]#` (par exemple `#[Garage][Tesla][Proxy joignable]#`). Avec plusieurs véhicules ou plusieurs proxys, ajoutez le **Proxy joignable** de chaque véhicule.
3. Ouvrez l'onglet **Scénario**, cliquez sur **+ Bloc** et choisissez **Si/Alors/Sinon**.
4. Dans le champ **SI**, saisissez la condition `#[Objet][Véhicule][Proxy joignable]# == 0` (ou choisissez la commande avec le bouton de sélection, puis ajoutez `== 0`).
5. Dans **ALORS**, ajoutez une **Action** : une commande de notification de votre installation (application mobile, Telegram, e-mail…) ou la commande **Ajouter un message** du centre de messages de Jeedom. Saisissez le texte, par exemple « Le proxy Tesla ne répond plus : vérifiez le Raspberry Pi du garage ».
6. Pour être aussi prévenu du retour, ajoutez dans **SINON** une seconde notification, par exemple « Le proxy Tesla répond de nouveau ».
7. **Sauvegardez**, puis testez en éteignant le Raspberry Pi : à la lecture suivante (au plus à l'intervalle le plus court des véhicules de ce proxy, 5 minutes par défaut), **Proxy joignable** passe à 0 et la notification part. Rallumez-le : au cycle suivant, l'information repasse à 1 et la notification de retour part.

Le scénario est déclenché à chaque changement de la valeur, donc à la panne puis au retour, pas à chaque cycle. Pour la cause précise (clé, portée, adaptateur figé), consultez **Dernière erreur**.

## Limitations connues

- **Après une commande**, seuls la limite de charge, le courant de charge et le verrouillage sont mis à jour tout de suite. Les autres informations de charge et de climatisation sont à jour à la lecture suivante du véhicule (5 minutes par défaut).
- **Véhicule endormi** : les informations de charge et de climatisation ne sont lues que véhicule réveillé (le plugin ne le réveille jamais de lui-même). Utilisez **Réveiller** puis **Rafraîchir**.
- **Clé Charging Manager** : le verrouillage, le klaxon, les feux et le mode sentinelle sont refusés par le véhicule. Le plugin le détecte (information **Rôle de clé**) mais ne grise pas ces commandes sur le dashboard (voir [Rôle de la clé](#rôle-de-la-clé)).
- **Un seul équipement par véhicule** (VIN unique).
- **Heure de départ programmée historisée** : si elle était historisée avant la mise à jour, elle reste numérique et n'est plus mise à jour tant que son sous-type n'est pas changé en **Autre**.
- **Proxy déclaré par un nom de service Docker** : le lien vers le tableau de bord ne s'ouvre pas dans le navigateur (voir [Lien vers le tableau de bord du proxy](#lien-vers-le-tableau-de-bord-du-proxy)).

### Limites chiffrées

| Limite | Valeur |
|---|---|
| Appareils Bluetooth par véhicule | **3** en même temps (téléphones, montre, proxy). Au-delà, connexions intermittentes. |
| Véhicules par proxy | **3 au plus** pour que le cycle ne soit jamais écourté au pire cas ; au-delà, vérifiez la **Dernière lecture des données** de chaque véhicule. |
| Durée d'un cycle | Lancé **chaque minute** pour les véhicules échus (5 minutes d'intervalle par défaut), 4 minutes au plus ; il dure autant que son proxy le plus lent (les proxys sont lus en parallèle). |
| Attente d'un proxy occupé | Environ 2 minutes (110 secondes pour une lecture, 15 secondes pour la vérification d'appairage), puis **Proxy occupé**. |
| Rôle de la clé | **Charging Manager** par défaut : lectures et charge seulement ; **Owner** pour le verrouillage, le klaxon, les feux, la sentinelle (voir [Rôle de la clé](#rôle-de-la-clé)). |
| Authentification du proxy | **Aucune par défaut** : gardez-le sur un réseau de confiance, jamais exposé sur Internet. Le proxy du fork peut exiger un **jeton d'API** (facultatif, même jeton pour tous les proxys), qui protège l'accès mais ne remplace pas un réseau de confiance. |
| Équipements par véhicule | Un seul (VIN unique). |
| Logs du proxy | Proxy **2.3.0** minimum ; seul le proxy de la configuration du plugin est affiché. |

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

Le test n'interroge que la version du proxy : un test vert ne prouve ni que la clé est appairée, ni que le véhicule est à portée. Pour cela, utilisez le bouton **Vérifier l'appairage** de l'équipement (voir [Appairer ma clé et vérifier l'appairage](#appairer-ma-clé-et-vérifier-lappairage)).

### Messages à l'enregistrement

- **« URL invalide : … »** (configuration du plugin ou URL du proxy d'un véhicule) : mêmes causes que pour le bouton **Tester**. L'ancienne URL est conservée.
- **« Aucune URL de proxy configurée : … »** (dernière erreur d'un véhicule ou bouton **Tester ce proxy**) : ni le véhicule ni la configuration du plugin n'ont d'URL de proxy. Renseignez l'une des deux.
- **« VIN invalide : 17 caractères attendus, chiffres et lettres sauf I, O et Q »** : corrigez la VIN de l'équipement (les espaces sont retirés tout seuls).
- **« Cette VIN est déjà utilisée par l'équipement … »** : un autre équipement porte déjà cette VIN, ce qui arrive aussi avec **Dupliquer**. Supprimez le doublon ou corrigez la VIN.
- **« Erreur interne du plugin : consultez le log TeslaBLE »** : erreur imprévue lors de l'enregistrement ; le détail est dans le log du plugin.

### Centre de messages de Jeedom (après une mise à jour)

- **« La VIN de l'équipement … est invalide : corrigez-la dans sa page de configuration… »** : la VIN enregistrée par une ancienne version n'est pas valable. Corrigez-la.
- **« L'équipement … a la même VIN que l'équipement … »** : deux équipements pour un même véhicule. Supprimez le doublon ou corrigez sa VIN.
- **« L'information … est historisée : elle reste numérique et n'est plus mise à jour… »** : voir [Heure de départ programmée](#heure-de-départ-programmée).
- **« Adaptateur Bluetooth du proxy probablement figé — … »** : voir [Alerte adaptateur Bluetooth figé](#alerte-adaptateur-bluetooth-figé). Redémarrez le Raspberry Pi.

### Information « Dernière erreur » (lecture)

| Texte affiché | Cause | Action |
|---|---|---|
| **Aucune** | Le dernier cycle de lecture a réussi (ou le véhicule dort, ce qui n'est pas une erreur). | Rien à faire. |
| **Proxy injoignable** | Le proxy ne répond pas à l'adresse configurée. | Vérifiez l'URL, que le proxy est démarré, l'alimentation et le Wi-Fi du Raspberry Pi. |
| **Délai dépassé** | Le proxy ou le véhicule répond trop lentement. | Vérifiez le Raspberry Pi (alimentation, Wi-Fi), redémarrez le proxy si cela se répète. |
| **Adaptateur Bluetooth du proxy probablement figé : redémarrez le Raspberry Pi** | Plusieurs lectures de suite ont dépassé leur délai alors que le proxy répond : voir [Alerte adaptateur Bluetooth figé](#alerte-adaptateur-bluetooth-figé). | Redémarrez le Raspberry Pi. |
| **Proxy sans clé : appairage à faire — …** | Aucune clé sur le proxy : il n'en a encore généré ou installé aucune. | Générez une clé (**Generate**) dans le tableau de bord du proxy, envoyez-la au véhicule et validez avec la carte-clé (lien dans la configuration du plugin ou dans **Appairer ma clé**). |
| **Véhicule hors de portée — …** | Le proxy ne trouve pas le véhicule en Bluetooth. La **Présence véhicule** passe à 0. | Rapprochez le Raspberry Pi du véhicule ; vérifiez que le proxy a le Bluetooth pour lui seul et que le véhicule n'a pas déjà 3 appareils connectés. |
| **Demande refusée par le véhicule : clé du proxy non appairée avec ce véhicule** | La clé active du proxy n'est pas appairée avec ce véhicule (avec plusieurs véhicules, la même clé doit être appairée sur chacun). Les autres véhicules ne sont pas touchés. | Utilisez **Appairer ma clé** puis **Vérifier l'appairage** sur l'équipement de ce véhicule. |
| **Demande refusée par le véhicule — …** | Le véhicule a refusé la lecture ; la raison du proxy suit le message. | Lisez la raison indiquée après le message ; vérifiez aussi l'appairage de la clé. |
| **Fonction non supportée par ce proxy — …** | La lecture demandée n'existe pas dans votre version du proxy. | Mettez le proxy à jour. |
| **Réponse invalide du proxy** | Le proxy a renvoyé une réponse inattendue. | Vérifiez l'adresse, mettez le proxy à jour, redémarrez-le si cela se répète. |
| **Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour** | Le proxy est antérieur à 2.1.1 : l'état du véhicule n'est plus lisible. | Mettez le proxy à jour (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)). Le log signale aussi cette ligne en erreur. |
| **Proxy occupé : lecture du véhicule non effectuée, réessayez dans un instant** | Un **Rafraîchir** a attendu plus de 110 secondes : le proxy était occupé par une commande ou une lecture. Aucune lecture n'a eu lieu. | Relancez **Rafraîchir** dans un instant ; la lecture automatique suivante rattrape aussi. |
| **Le VIN n'est pas configuré pour cet équipement** | La VIN de l'équipement est vide. | Renseignez la VIN dans l'équipement puis sauvegardez. |
| **URL invalide : …** | L'URL du proxy est vide ou invalide dans la configuration du plugin. | Renseignez-la (voir [Configuration du plugin](#configuration-du-plugin)). |

Le texte est tronqué à 127 caractères. Un véhicule qui dort n'est pas une erreur : voir [Rafraîchissement des informations](#rafraîchissement-des-informations).

### Erreur à l'envoi d'une commande

Ces messages s'affichent en rouge dans Jeedom et sont aussi copiés dans **Dernière erreur**.

| Message | Cause | Action |
|---|---|---|
| **« Cette commande nécessite une clé de rôle Owner : la clé du proxy a probablement le rôle Charging Manager… »** | Le véhicule a refusé faute de droits une commande réservée au rôle Owner (verrouillage, klaxon, feux, sentinelle, climatisation) : votre clé a très probablement le rôle Charging Manager. | Voir [Rôle de la clé](#rôle-de-la-clé) : appairez une clé Owner. |
| **« Commande refusée par le véhicule (rôle de la clé du proxy insuffisant ?) : … »** | Défaut d'autorisation sur une autre commande : rôle de clé insuffisant ou état du véhicule. | Voir [Rôle de la clé](#rôle-de-la-clé) ; avec une clé Owner, vérifiez l'état du véhicule. |
| **« Commande refusée par le véhicule : … »** | Le véhicule a refusé la commande ; la raison renvoyée suit le message. | Corrigez selon la raison indiquée. |
| **« Proxy injoignable, commande non envoyée »** | Le proxy ne répond pas : la commande n'est pas partie. | Vérifiez l'URL et l'alimentation du Raspberry Pi. |
| **« Délai dépassé : la commande a pu être exécutée, vérifiez l'état du véhicule »** ou **« Liaison avec le proxy interrompue : la commande a pu être exécutée… »** | Le véhicule a peut-être exécuté la commande malgré tout. | Contrôlez l'état du véhicule avant de la renvoyer. |
| **« Proxy occupé : commande non envoyée, réessayez dans un instant »** | Une autre commande ou lecture occupe le proxy depuis près de 2 minutes. | Réessayez. |
| **« Valeur invalide : le courant doit être un entier entre … et … A »** | Le courant est décimal, texte ou hors des bornes Min/Max de la commande. | Corrigez la valeur, ou augmentez le **Max** de **Courant de charge** si votre véhicule accepte plus de 32 A. |
| **« Valeur invalide : la limite doit être un entier entre 50 et 100 % »** | Limite hors bornes ou non entière. | Corrigez la valeur. |
| **« Valeur invalide : le mode sentinelle doit être activé ou désactivé »** | Valeur autre que **Activé** ou **Désactivé** (l'ancienne option « Aucun » n'existe plus). | Utilisez **Activé** ou **Désactivé**. |
| **« Échec de la commande : … »** | Autre cause (proxy sans clé, véhicule hors de portée, réponse invalide…) : la cause suit le message. | Voir le tableau **Dernière erreur** ci-dessus. |
| **« Commande non prise en charge par le plugin »** | La commande n'est pas l'une de celles du plugin (commande ajoutée à la main, ou identifiant modifié). | Ne modifiez pas l'identifiant des commandes du plugin. |

### Tâche du cycle de rafraîchissement

Dans **Réglages > Système > Moteur de tâches**, la tâche **TeslaBLE::cycleRafraichissement** (chaque minute, délai de 5 minutes) lance le rafraîchissement des véhicules. Elle est créée à l'activation et à la mise à jour du plugin, et remise en place dans l'heure si elle a été supprimée ; une tâche que vous désactivez vous-même le reste.

- **Plus aucun véhicule n'est rafraîchi** : vérifiez que la tâche existe et qu'elle est activée. Si elle manque, **désactivez puis réactivez le plugin** pour la recréer. Un message d'erreur « Tâche de rafraîchissement non installée » dans le log du plugin signale un échec de création.
- **Désactiver** le plugin supprime la tâche (sans quoi le moteur de tâches journaliserait une erreur chaque minute) ; la réactiver la recrée. Vos équipements, commandes et réglages ne sont pas touchés.
- **Retour à une version antérieure du plugin** (par exemple de la bêta vers la stable) : cette version ne connaît pas la tâche et le log **cron** de Jeedom affiche une erreur « Classe ou fonction non trouvée » chaque minute. Supprimez alors la tâche **TeslaBLE::cycleRafraichissement** à la main dans le moteur de tâches.

### Messages du log du plugin

- **« Cycle de rafraîchissement sauté : le cycle précédent n'est pas terminé. »** : vous avez lancé la tâche à la main (**Réglages > Système > Moteur de tâches**) pendant qu'un cycle tournait. Jeedom, lui, ne relance jamais de lui-même une tâche en cours (voir les deux messages suivants).
- **« Cycle de rafraîchissement de N s, plus long que l'intervalle de rafraîchissement le plus court (M min) : Jeedom a sauté le passage suivant… »** (Avertissement, une fois par heure au plus) : un cycle a duré plus que l'intervalle réglé, en général parce que le proxy ou le Raspberry Pi répond lentement ; la cadence réglée n'est pas tenue. Allongez l'intervalle du véhicule concerné, répartissez les véhicules entre plusieurs proxys, ou vérifiez l'alimentation et la connexion Wi-Fi du Raspberry Pi.
- **« Cycle de rafraîchissement de N s : Jeedom a sauté le passage de la minute suivante, sans cumul de cycles. »** (Debug) : un cycle a dépassé une minute alors que tous les intervalles réglés sont plus longs ; rien à faire.
- **« Cycle de rafraîchissement écourté… véhicule(s) non lu(s) à ce cycle »** : le cycle a atteint sa durée maximale de 4 minutes ; les véhicules cités n'ont pas été lus à ce cycle. Ils le seront au cycle suivant si le proxy répond normalement ; jusqu'à 3 véhicules par proxy, le cycle n'est pas écourté, au-delà vérifiez la **Dernière lecture des données** de chaque véhicule. L'avertissement n'est émis qu'**une fois par épisode** (il précise « Avertissement non répété jusqu'au prochain cycle complet. »), même si l'épisode dure plusieurs heures ; si cela se répète, le proxy répond trop lentement : voir ci-dessus.
- **« Cycle de rafraîchissement de nouveau complet : … »** (Info) : fin d'un épisode de cycle écourté ; tous les véhicules ont été lus.
- **« Véhicule … traité en … s. »** (Debug) : durée de la lecture de chaque véhicule dans le cycle, y compris un véhicule sauté (proxy occupé, la ligne « sautée » la précède) ou en erreur. Les lignes **Requête** et **Réponse HTTP … en … ms** donnent le détail des appels ; la ligne Réponse rappelle sa requête (méthode et adresse), car les lignes de plusieurs proxys lus en parallèle s'entremêlent dans le log.
- **« Lecture du véhicule … reportée : proxy occupé… »** : un **Rafraîchir** a attendu plus de 110 secondes un proxy occupé par une commande ou une lecture ; la lecture n'a pas eu lieu et le message **Proxy occupé : lecture du véhicule non effectuée…** apparaît dans **Dernière erreur**.
- **« Lecture du véhicule … sautée : une commande ou une lecture est en cours vers le proxy. »** (Debug) : le cycle automatique s'efface devant l'échange en cours ; la lecture est faite au cycle suivant.
- **« Proxy obtenu pour le véhicule … après … s d'attente… »** (Debug) : une commande ou une lecture attendait le proxy depuis au moins une seconde.
- **« Verrou du proxy indisponible… »** ou **« Verrou du cycle de rafraîchissement indisponible… »** : le plugin ne peut pas écrire dans le dossier temporaire de Jeedom. Vérifiez les droits de ce dossier ; le plugin continue de fonctionner sans la protection contre les échanges simultanés.
- **« Commandes : … le nom … est déjà pris… »** : le plugin n'a pas pu donner le libellé prévu à une commande parce qu'une autre commande de l'équipement le porte. Renommez l'une des deux, puis sauvegardez l'équipement.
- **« Adaptateur Bluetooth du proxy probablement figé pour le véhicule … »** (avertissement) et **« Adaptateur Bluetooth du proxy de nouveau opérationnel pour le véhicule … »** (Info) : début et fin d'un épisode, voir [Alerte adaptateur Bluetooth figé](#alerte-adaptateur-bluetooth-figé).
- **« Migrations : … »** : voir [Constater la mise à niveau dans le log](#constater-la-mise-à-niveau-dans-le-log).

### Lecture lente du proxy

Le plugin mesure la durée de chaque lecture, sans aucune requête supplémentaire, et la publie dans **Durée lecture état** et **Durée lecture données**. Quand une lecture réussie dépasse **10 secondes** (état) ou **20 secondes** (données), le log reçoit **un seul** avertissement **« Lecture lente du proxy pour le véhicule … »**, qui n'est pas répété tant que la lecture reste lente. Quand la durée redescend à **7 secondes** (état) ou **14 secondes** (données), une ligne **Info** « Lecture du proxy redevenue normale… » le signale. Ces seuils sont fixes.

Causes habituelles : Raspberry Pi trop éloigné du véhicule (mur, sol en béton, voiture garée loin), Raspberry Pi saturé (autre client du proxy, comme evcc, qui l'occupe) ou mal alimenté. Rapprochez le Raspberry Pi ou changez son alimentation, puis observez la durée aux cycles suivants.

Une lecture en échec (proxy injoignable, délai dépassé) ne modifie pas ces informations : sa durée apparaît dans le message d'échec du log (« … après 25.0 s : … »). La durée d'une commande est écrite dans le log en niveau **Debug** (« Commande … exécutée en 3.2 s. »).

### Proxy du fork : jeton, adaptateur, corps refusé

| Ce que vous voyez | Cause | Action |
|---|---|---|
| **« Jeton d'API refusé par le proxy »** dans **Dernière erreur**, ou **« Jeton d'API refusé par le proxy : commande non envoyée »** à l'envoi d'une commande | Le proxy du fork a un `apiToken`, et le plugin n'a pas de jeton ou un jeton différent. La présence du véhicule n'est pas modifiée ; le log reçoit **une seule** ligne **Erreur** par épisode. | Saisissez la valeur exacte de `apiToken` dans **Jeton d'API du proxy**, **Sauvegarder**, puis **Tester** (« Jeton d'API accepté par le proxy »). |
| **« Jeton d'API invalide : … »** ou **« Jeton d'API non pris en charge par Jeedom … »** | Le jeton saisi contient un caractère non admis (accent, retour à la ligne, plus de 256 caractères), ou une forme que Jeedom ne sait pas stocker. | Générez un autre jeton (`openssl rand -hex 32`), reportez-le dans `apiToken` et dans le plugin. |
| **Proxy injoignable** alors que le Raspberry Pi est allumé | Le proxy du fork s'arrête au démarrage si `btAdapter` est invalide ou si l'adaptateur n'existe pas ; Docker le relance en boucle. | Sur le Raspberry Pi, `docker logs tesla-ble-http-proxy` : cherchez `Cannot start with this Bluetooth adapter`. Corrigez ou retirez `btAdapter` (voir [Installer le proxy BLE](installation-proxy.md#12-dépannage)). |
| **« Commande refusée par le véhicule : invalid request body: … »** | Le proxy du fork a refusé le contenu de la commande avant de l'envoyer. | Le texte après les deux-points nomme la clé en cause ; signalez-le avec le log du plugin en Debug. |

### Messages de la fenêtre Logs du proxy

| Message | Cause | Action |
|---|---|---|
| **« Logs indisponibles (proxy ≥ 2.3.0 requis) »** | Le serveur à l'URL enregistrée ne fournit pas de logs : proxy antérieur à 2.3.0, ou URL qui ne désigne pas le proxy. | Vérifiez l'URL avec le bouton **Tester**, puis mettez le proxy à jour si sa version est inférieure à 2.3.0. |
| **« Proxy injoignable : vérifiez qu'il est démarré, puis son adresse avec le bouton Tester »** | Le proxy est arrêté, le Raspberry Pi éteint, ou l'adresse est fausse. | Démarrez le proxy, puis vérifiez l'URL avec **Tester**. |
| **« URL du proxy absente ou invalide : renseignez-la, sauvegardez, puis rouvrez les logs »** | Aucune URL valide n'est enregistrée. | Renseignez l'URL, sauvegardez, puis rouvrez la fenêtre. |
| **« Jeton d'API refusé par le proxy »** | Le proxy du fork a un `apiToken` que le plugin n'envoie pas ou qui diffère. | Saisissez le jeton (voir le tableau ci-dessus). |
| Message d'échec suivi de **« réponse HTTP 500 au lieu de 200 : Failed to encode logs »** | Le proxy n'arrive plus à relire sa propre mémoire de logs (défaut connu du proxy). | Redémarrez le proxy (`docker compose restart` sur le Raspberry Pi). |
| **« Aucune ligne de log sur le proxy »** | Le proxy n'a encore rien journalisé. | Rafraîchissez après un cycle du plugin. |

### Symptômes sans message

- **Proxy joignable vaut 0 alors que le proxy est allumé** : le proxy répond « introuvable » à la question de santé si sa version est antérieure à 2.1.3, ou si l'adresse ne désigne pas le proxy. Contrôlez la version et l'adresse avec **Tester** ou **Tester ce proxy**, puis mettez le proxy à jour (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)).
- **Présence véhicule reste à 0** : le proxy ne trouve pas le véhicule en Bluetooth. Rapprochez le Raspberry Pi du véhicule.
- **Les informations de charge ne bougent plus alors que Dernière erreur vaut Aucune** : le véhicule dort. C'est le comportement normal, voir [Rafraîchissement des informations](#rafraîchissement-des-informations).
- **Aucune requête n'aboutit** : testez l'URL avec le bouton **Tester** (le `/` final est géré par le plugin), puis depuis un navigateur.
- **Le lien du tableau de bord ne s'ouvre pas** alors que le proxy fonctionne : l'URL contient un nom de service Docker que votre navigateur ne connaît pas. Ouvrez `http://<ip_du_pi>:8080/dashboard`.
- **Le graphique de l'Autonomie fait un saut** : normal après la mise à jour depuis la 0.x (miles puis km), voir [Autonomie et vitesse de charge](#autonomie-et-vitesse-de-charge).
- **Je ne vois pas les lignes de début et de fin de panne dans le log** : passez le log du plugin au moins en niveau **Info**.
- **Le proxy ne répond plus au bout de quelques heures** : c'est un problème fréquent sur le Raspberry Pi Zero W de première génération. Redémarrez le proxy ou passez à un Raspberry Pi Zero 2 W. Si le proxy répond encore mais que les lectures expirent, le plugin vous prévient : voir [Alerte adaptateur Bluetooth figé](#alerte-adaptateur-bluetooth-figé).
- **Connexions Bluetooth intermittentes** : le véhicule n'accepte que 3 appareils connectés à la fois ; déconnectez un téléphone ou une montre.
