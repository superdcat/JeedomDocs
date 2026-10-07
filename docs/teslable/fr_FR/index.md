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
| **Charging Manager** : fonctionne (fonctions de la charge avancée) | **Ajuster selon le surplus** et la **Charge aux heures creuses** n'envoient que **Courant de charge**, **Démarrer la charge** et **Arrêter la charge** : une clé Charging Manager suffit. |
| **Charging Manager** : non confirmé | **Ajouter une programmation de charge** et **Supprimer la programmation de charge** : le rôle minimal n'est pas confirmé (Charging Manager probable ; essayez, et passez à Owner si le véhicule refuse). Ces deux actions exigent aussi le proxy du fork (voir [Programmer la charge](#programmer-la-charge)). |
| **Charging Manager** : refusé | **Verrouiller les portes**, **Déverrouiller les portes**, **Klaxonner**, **Faire clignoter les feux**, **Mode sentinelle** ; probablement aussi **Démarrer le climatiseur** et **Arrêter le climatiseur** |
| **Charging Manager** : refusé (probable) | **Consigne conducteur** et **Consigne passager** : le rôle Owner est supposé nécessaire (non confirmé en usage réel). Ces deux actions exigent aussi le proxy du fork (voir [Régler la consigne de température](#régler-la-consigne-de-température)). |
| **Charging Manager** : refusé (probable) | Les six actions **Régler le chauffage du siège …** et **Régler le chauffage du volant** : le rôle Owner est supposé nécessaire (non confirmé en usage réel). Elles exigent aussi le proxy du fork (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| **Charging Manager** : refusé (probable) | **Dégivrage maximal** : le rôle Owner est supposé nécessaire (non confirmé en usage réel). Cette action exige aussi le proxy du fork (voir [Dégivrage maximal](#dégivrage-maximal)). |
| **Charging Manager** : refusé (probable) | **Mode de maintien de climat** : le rôle Owner est supposé nécessaire (non confirmé en usage réel). Cette action exige aussi le proxy du fork (voir [Mode chien, camp et maintien de climat](#mode-chien-camp-et-maintien-de-climat)). |
| **Charging Manager** : refusé (probable) | **Ouvrir le coffre arrière** et **Ouvrir le frunk** : le rôle Owner est supposé nécessaire (non confirmé en usage réel). Ces deux actions exigent aussi le proxy du fork (voir [Ouvrir le coffre arrière et le frunk](#ouvrir-le-coffre-arrière-et-le-frunk)). |
| **Charging Manager** : refusé (probable) | **Préconditionnement planifié par Jeedom** : il n'envoie que **Démarrer le climatiseur** et **Arrêter le climatiseur**, dont le rôle Owner est supposé nécessaire (non confirmé en usage réel). Avec une clé Charging Manager, un seul essai est fait par départ (voir [Préconditionnement planifié par Jeedom](#préconditionnement-planifié-par-jeedom)). |
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
| **Intervalle pendant la charge** | **Désactivé par défaut** (comportement inchangé), ou **1, 2, 5, 10 ou 15 minutes**. Pendant une charge, il remplace l'intervalle de rafraîchissement **quand il est plus court** ; la cadence normale reprend dès qu'une lecture ne constate plus la charge. Une minute au minimum : Jeedom lance le rafraîchissement chaque minute et le proxy garde les données 30 secondes en cache. Ne réveille jamais le véhicule. Voir [Lecture accélérée pendant la charge](#lecture-accélérée-pendant-la-charge). |
| **Laisser le véhicule s'endormir** (case **Activer**) | Coché par défaut (y compris sur les véhicules existants après la mise à jour). Quand le véhicule est éveillé mais inactif, le plugin cesse de lire les données de charge et de climatisation pendant une fenêtre, pour ne pas l'empêcher de s'endormir. Décoché : une lecture complète a lieu à chaque passage, comme avant. Voir [Laisser le véhicule s'endormir](#laisser-le-véhicule-sendormir). |
| **Lectures inchangées avant la fenêtre** | Nombre de lectures successives sans aucun changement (hors charge, sans occupant) avant d'ouvrir la fenêtre : **1, 2, 3, 4, 5, 10 ou 15**. Par défaut **3** (15 minutes d'inactivité à l'intervalle de 5 minutes). |
| **Durée de la fenêtre** | Durée pendant laquelle les données ne sont plus lues : **15, 20, 30, 45 minutes, 1 heure, 1 heure 30 ou 2 heures**. Par défaut **30 minutes**. Sans effet si elle ne dépasse pas l'intervalle de rafraîchissement : choisissez une durée supérieure à l'intervalle. |
| **Délai de relecture après commande** | Temps d'attente avant de relire le véhicule après une commande réussie : **30 secondes (par défaut), 45 secondes, 1 minute, 1 minute 30 ou 2 minutes**. 30 secondes est le minimum : c'est la durée pendant laquelle le proxy garde ses données en cache (voir [Relecture après une commande](#relecture-après-une-commande)). Allongez-le si vous avez allongé ce cache dans le proxy. |
| **Lire aussi la climatisation** | **Oui (par défaut)** : charge et climatisation sont lues, comme avant la mise à jour. **Non, charge seule** : seules les données de charge sont demandées au proxy, à chaque rafraîchissement comme à la demande (**Rafraîchir**, **Rafraîchir (avec réveil)**, relecture après commande). La requête est plus courte et sollicite moins la liaison Bluetooth (le gain est à mesurer sur votre installation). Les informations de climatisation gardent alors leur dernière valeur et ne sont plus mises à jour ; les commandes de climatisation restent utilisables. Repasser sur **Oui** reprend la lecture des deux familles au prochain passage, véhicule éveillé. |
| **Tension du réseau (V)** | Pilotage selon le surplus : tension entre phase et neutre utilisée pour convertir la puissance disponible en courant. Vide : **230 V**. Entier de 100 à 250. |
| **Phases** | Pilotage selon le surplus : **Monophasé (par défaut)** ou **Triphasé**. La puissance est divisée par la tension et par ce nombre pour obtenir le courant **par phase**. |
| **Pas d'ajustement (A)** | Pilotage selon le surplus : le courant calculé est arrondi **vers le bas** à un multiple de ce pas. Vide : **1 A**. Entier de 1 à 16. |
| **Hystérésis (A)** | Pilotage selon le surplus : aucune commande tant que le courant calculé s'écarte de **moins** de cette valeur de la dernière consigne envoyée. Vide : **2 A**. Entier de 0 à 16. |
| **Intervalle minimal entre commandes (s)** | Pilotage selon le surplus : délai minimal entre la **fin** d'une commande du pilotage et la suivante. Vide : **120 s**. Entier de 60 à 3600 (une commande peut durer jusqu'à 75 secondes et le proxy garde les données 30 secondes en cache). |
| **Courant minimal de démarrage (A)** | Pilotage selon le surplus : charge arrêtée, elle est relancée quand le courant calculé atteint cette valeur. Vide : **6 A**. Entier de 1 à 80. |
| **Seuil d'arrêt (A)** | Pilotage selon le surplus : pendant la charge, le courant n'est jamais réglé sous ce seuil ; s'il reste calculé en dessous pendant la durée de maintien, la charge est arrêtée. Vide : **5 A**. Entier de 1 à 80, **jamais supérieur au courant minimal de démarrage**. |
| **Durée de maintien avant arrêt (s)** | Pilotage selon le surplus : durée pendant laquelle le courant calculé doit rester sous le seuil d'arrêt avant l'arrêt de la charge. Vide : **300 s**. Entier de 0 à 3600. |
| **Pilotage de la charge** (case **Activer**, section **Charge aux heures creuses**) | **Décochée par défaut.** Cochée, Jeedom démarre et arrête la charge pendant la plage horaire ci-dessous (voir [Charge aux heures creuses](#charge-aux-heures-creuses)). Elle ne s'active que si le début, la fin et le SoC cible sont renseignés. |
| **Début de plage** | Charge aux heures creuses : heure de début de la plage, au format `HH:MM` (heure de Jeedom, par exemple `22:00` ; `22h00` est aussi accepté). |
| **Fin de plage** | Charge aux heures creuses : heure de fin de la plage, au format `HH:MM`, **différente** du début. Une fin plus tôt que le début donne une plage **à cheval sur minuit** (`22:00` à `06:00`). |
| **SoC cible (%)** | Charge aux heures creuses : niveau de batterie auquel la charge est arrêtée pendant la plage. Entier de **1 à 100**. |
| **Arrêter en fin de plage** | Charge aux heures creuses : **décochée par défaut**. Cochée, la charge encore en cours à la fin de la plage est arrêtée (à la première lecture du véhicule, dans l'heure qui suit). Décochée, elle continue jusqu'à la limite du véhicule. |
| **Pilotage de la climatisation** (case **Activer**, section **Préconditionnement planifié par Jeedom**) | **Décochée par défaut.** Cochée, Jeedom démarre la climatisation avant l'heure de départ puis l'arrête (voir [Préconditionnement planifié par Jeedom](#préconditionnement-planifié-par-jeedom)). Elle ne s'active que si l'heure de départ est renseignée, qu'au moins un jour est coché et que **Lire aussi la climatisation** reste sur **Oui**. |
| **Heure de départ** | Préconditionnement planifié : heure à laquelle le véhicule doit être prêt, au format `HH:MM` (heure de Jeedom, par exemple `07:30` ; `7h30` est aussi accepté). |
| **Jours** | Préconditionnement planifié : jours de **départ** concernés (cases **Lundi** à **Dimanche**). Le jour retenu est celui de l'heure de départ, même si la climatisation démarre la veille avant minuit. Aucune case cochée : fonction refusée à l'activation. |
| **Avance (min)** | Préconditionnement planifié : minutes avant l'heure de départ où la climatisation est démarrée. Entier de **1 à 60**. Vide : **15 minutes**. |
| **Durée maximale (min)** | Préconditionnement planifié : durée, **comptée depuis le démarrage prévu**, au bout de laquelle Jeedom arrête la climatisation. Entier de **1 à 120**, **au moins égal à l'avance**. Vide : **30 minutes** (ou l'avance plus 15 minutes si elle dépasse 15), soit un arrêt **15 minutes après le départ** avec l'avance par défaut. |
| **Seulement si branché** | Préconditionnement planifié : **décochée par défaut**. Cochée, la climatisation n'est pas démarrée si le véhicule est débranché ou si son état de charge est inconnu. Une borne qui ne fournit pas de courant compte comme branchée : la climatisation puise alors dans la batterie. |
| **Latitude** (section **Position du domicile**) | Position du domicile, pour calculer **À la maison** : degrés décimaux de -90 à 90, par exemple `48.8566` (virgule admise, 8 décimales au plus). **Vide : la position de Jeedom** (**Réglages > Système > Configuration**, onglet **Général**). À renseigner avec la **longitude** : une seule des deux est refusée. Voir [Position et confidentialité](#position-et-confidentialité). |
| **Longitude** (section **Position du domicile**) | Degrés décimaux de -180 à 180, par exemple `2.3522`. Vide avec la latitude vide : position de Jeedom. |
| **Rayon (m)** (section **Position du domicile**) | Distance maximale, en mètres, entre le véhicule et le domicile pour que **À la maison** vaille 1. Entier de **10 à 10000**. Vide : **100 m**. Sans effet si le proxy ne fournit pas la position du véhicule. |
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

À la mise à jour, les commandes absentes de votre équipement sont ajoutées **en fin de liste** : **Temps de charge restant**, **Trappe de charge ouverte**, **Dernière erreur**, **Dernière lecture des données**, **Proxy joignable**, **Version du proxy**, **Rôle de clé** (qui vaut **Indéterminé** jusqu'à la première commande réservée au rôle Owner), **Durée lecture état** et **Durée lecture données** (vides jusqu'à la première lecture réussie), puis **Âge des données (min)** (qui vaut 99999 jusqu'à la première lecture connue), puis **Limite de charge minimale**, **Limite de charge maximale** et **Courant de charge maximal** (masquées, vides jusqu'à la première lecture des données), enfin dix informations de charge étendues, masquées elles aussi (voir [Informations](#informations)). Un **Max** de curseur que vous aviez relevé à la main est conservé. Sur un équipement existant, l'action d'ouverture de la trappe peut s'appeler « Trappe de Charge Ouvert » : renommez-la si besoin.

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

À la mise à jour, puis à l'activation du plugin, une mise à niveau des équipements existants s'exécute automatiquement, par niveaux successifs. Chaque niveau n'est appliqué qu'une seule fois. Selon les versions, elle corrige ou complète certains équipements (VIN, commandes manquantes, heure de départ programmée, retrait de l'option « Aucun » du mode sentinelle, réglages de la fenêtre d'endormissement…) sans toucher à vos réglages (nom, visibilité, historisation). Les véhicules existants reçoivent la fenêtre d'endormissement **activée** (3 lectures inchangées, 30 minutes) ; décochez-la dans l'équipement si vous ne la souhaitez pas.

Les huit informations d'ouvrant (portes, coffres, trappe de charge, tonneau) sont créées **visibles et historisées** ; vos réglages existants ne sont jamais modifiés.

Les informations **Occupant présent** (visible, historisée) et **État de verrouillage détaillé** (visible, non historisée) sont créées de la même façon ; vos réglages existants ne sont jamais écrasés.

Les informations **Sentinelle** et **Provenance de la sentinelle** (visibles, non historisées) sont créées de la même façon, avec les valeurs **Inconnu** et **Aucune** tant que rien n'a été lu ni ordonné ; vos réglages existants ne sont jamais écrasés (voir [État du mode sentinelle](#état-du-mode-sentinelle)).

Les informations **Alerte ouvrants** et **Alerte déverrouillé sans occupant** (masquées, historisées) sont créées de la même façon, à **0** ; les alertes restent **désactivées** tant que vous ne les activez pas (voir [Alertes d'ouverture prolongée](#alertes-douverture-prolongée)).

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

### Veille du véhicule et fraîcheur des données

Une Tesla éveillée s'endort d'elle-même après **une quinzaine de minutes** sans sollicitation. Plusieurs choses la gardent éveillée : le **mode sentinelle**, un **occupant** à bord (ou une clé téléphone proche), une **charge** en cours, l'**application Tesla** ouverte, et toute lecture de ses données de charge et de climatisation. Un véhicule qui dort consomme très peu ; un véhicule maintenu éveillé consomme en permanence de la batterie.

C'est le compromis à connaître : **plus vous lisez souvent, plus les informations sont fraîches, mais plus le véhicule a de chances de ne jamais s'endormir**. Les réglages de cadence de ce plugin servent à choisir votre point d'équilibre (voir [Récapitulatif des réglages de cadence et de réveil](#récapitulatif-des-réglages-de-cadence-et-de-réveil) et [Recommandations par usage](#recommandations-par-usage)).

> **IMPORTANT**
>
> **Le plugin ne réveille jamais le véhicule de lui-même, sauf action explicite de votre part ou d'un scénario.** Ni le rafraîchissement périodique, ni la lecture accélérée pendant la charge, ni la relecture après une commande ne réveillent le véhicule : ils lisent l'état sans réveil, puis les données seulement si le véhicule est déjà éveillé. Pour lire les données d'un véhicule qui dort, il faut **le demander** avec la commande **Rafraîchir (avec réveil)** (voir [Rafraîchir avec réveil](#rafraîchir-avec-réveil)). **Réveiller** et les commandes d'action (charge, climatisation, verrouillage…) réveillent aussi le véhicule, via le proxy, puisque vous les avez demandées.

Pour savoir si les valeurs affichées sont récentes, regardez **Dernière lecture des données** et **Âge des données (min)** : un véhicule qui dort ou une fenêtre d'endormissement ouverte n'est pas une erreur, mais les valeurs de charge et de climatisation vieillissent alors (voir [Exemple pas à pas : n'agir que sur des données récentes](#exemple-pas-à-pas--nagir-que-sur-des-données-récentes)).

### Rafraîchissement des informations

À l'**intervalle de chaque véhicule** (5 minutes par défaut, réglable de 1 à 30 minutes dans l'équipement), le plugin rafraîchit ce véhicule en deux temps :

1. Il interroge l'état du **contrôleur de carrosserie** (`body_controller_state`). Cette requête ne réveille pas le véhicule. Elle met à jour la présence, le verrouillage et l'état de veille.
2. **Uniquement si le véhicule est réveillé**, il récupère les données du véhicule (`vehicle_data`) : charge, batterie, autonomie et, selon le réglage **Lire aussi la climatisation** de l'équipement (activé par défaut), climatisation.

Une tâche de Jeedom, **TeslaBLE::cycleRafraichissement**, se déclenche **chaque minute** et ne lit que les véhicules actifs dont l'intervalle est écoulé (mesuré depuis le début de leur dernière lecture) : avec un véhicule à 1 minute et un autre à 15 minutes, le premier est lu à chaque passage et le second environ toutes les 15 minutes. Un véhicule qui n'a encore jamais été lu l'est dès le passage suivant. Un proxy dont aucun véhicule n'est à lire n'est pas sollicité. Cette tâche est créée à l'activation et à la mise à jour du plugin (voir [Dépannage](#dépannage)).

Le plugin ne réveille donc jamais le véhicule de lui-même, afin de ne pas vider la batterie. Tant que le véhicule dort, les informations de charge et de climatisation conservent leur dernière valeur connue. Pour les actualiser à la demande, utilisez la commande **Rafraîchir (avec réveil)** (voir [Rafraîchir avec réveil](#rafraîchir-avec-réveil)).

Si le véhicule s'endort entre les deux requêtes, ce n'est pas une erreur : les informations de charge et de climatisation gardent leur dernière valeur et rien n'est affiché.

Avec **Lire aussi la climatisation** sur **Non, charge seule**, la requête de données ne demande que la charge (`vehicle_data?endpoints=charge_state`, visible dans le log du plugin en **Debug** et dans les logs du proxy). **Dernière lecture des données** et **Durée lecture données** datent alors la lecture de charge, et **Âge des données (min)** compte le temps écoulé depuis cette lecture de charge : les informations de climatisation, elles, restent figées.

Si le véhicule est hors de portée Bluetooth du proxy, la commande **Présence véhicule** passe à 0. Si c'est le proxy qui ne répond pas, n'a pas de clé appairée ou répond trop lentement, la présence garde sa dernière valeur.

**Plusieurs véhicules sur un même proxy.** Les véhicules d'un même proxy sont lus l'un après l'autre, chacun avec sa propre **Dernière erreur** et sa propre **Dernière lecture des données** : un véhicule hors de portée ou dont la clé n'est pas appairée n'empêche pas la lecture des autres. Le cycle dure au plus 4 minutes ; avec 3 véhicules ou moins sur un même proxy, il n'est jamais écourté, même au pire cas. Au-delà, les derniers véhicules peuvent ne pas être lus : vérifiez leur **Dernière lecture des données**. Quand un cycle est écourté, le log reçoit **un seul** avertissement par épisode (« Avertissement non répété jusqu'au prochain cycle complet. »), puis une ligne **Info** au premier cycle de nouveau complet.

**Pourquoi les données ne bougent plus ?** L'information **Dernière erreur** donne la cause du dernier échec de lecture, suivie de la raison renvoyée par le proxy quand il en donne une (par exemple « Véhicule hors de portée — … » ou « Proxy sans clé : appairage à faire — … »). Elle revient à **Aucune** dès qu'un cycle de lecture réussit. Un véhicule qui dort n'est pas une erreur : **Dernière erreur** reste à **Aucune** et **Véhicule réveillé** vaut 0. L'information **Dernière lecture des données** indique depuis quand les données de charge et de climatisation datent.

Dans le log du plugin, un problème ne laisse que **deux lignes** : une quand il commence, une quand tout revient à la normale (`Véhicule « <nom> » (id <n>) : retour à la normale après [<catégorie>].`), même s'il dure des heures. Le niveau de la ligne de début dépend de la cause : **Info** pour un véhicule hors de portée (situation normale), **Erreur** pour une erreur de configuration (VIN ou URL manquante) ou un proxy trop ancien, **Avertissement** pour les autres. La ligne de fin est toujours au niveau **Info**. **Pour voir ces lignes, le log du plugin doit être au moins en niveau Info** (**Configuration du plugin > Logs**). Tant que le problème dure, le détail de chaque cycle reste visible en **Debug**.

Les véhicules d'un même proxy sont rafraîchis **l'un après l'autre** ; les proxys différents sont lus **en parallèle**. Un véhicule hors de portée ou en erreur n'empêche pas la lecture des suivants, et l'erreur est consignée dans le log avec le nom du véhicule.

- Si un cycle dure plus longtemps que l'intervalle, Jeedom **saute** les passages suivants tant qu'il n'est pas terminé : les cycles ne se cumulent jamais. Le plugin l'écrit alors dans le log à la fin du cycle (un avertissement par heure au plus si l'intervalle réglé n'est pas tenu) ; la cadence reprend dès que le cycle est fini.
- Un cycle ne dépasse pas **4 minutes** : s'il y a beaucoup de véhicules ou si le proxy est lent, les véhicules restants sont lus au cycle suivant (avertissement nommant ces véhicules).
- Pendant qu'une commande, un **Rafraîchir**, un **Rafraîchir (avec réveil)** ou une vérification d'appairage est en cours ou attend le même proxy, la lecture du cycle est sautée sans erreur ; la lecture suivante rattrape.
- Avec plusieurs proxys, le cycle lit les proxys en parallèle : un proxy arrêté, éteint, figé ou lent ne retarde que ses propres véhicules (un proxy arrêté coûte quelques secondes, jusqu'à environ 5 s, par véhicule de ce proxy), jamais ceux des autres proxys. Le cycle dure autant que son proxy le plus lent. Deux proxys différents ne s'attendent jamais, y compris dans le cycle périodique ; les commandes et **Rafraîchir** des autres proxys ne sont pas retardés non plus.

### Rafraîchir avec réveil

La commande **Rafraîchir (avec réveil)** est la seule façon de lire les données de charge et de climatisation d'un véhicule qui dort. Elle lit d'abord l'état sans réveil, puis réveille le véhicule si besoin et lit ses données, en une seule action : à la fin, **Véhicule réveillé** vaut 1 et la charge et la climatisation sont à jour. Comptez en général 15 à 40 secondes ; le plugin attend jusqu'à 75 secondes pour la lecture après réveil, pendant lesquelles Jeedom reste utilisable.

- **Elle réveille le véhicule** à chaque exécution : l'usage répété consomme de la batterie. Après la lecture, la fenêtre d'endormissement (voir [Laisser le véhicule s'endormir](#laisser-le-véhicule-sendormir)) et la cadence normale reprennent leurs règles ; le véhicule peut se rendormir.
- **Hors de portée** : l'état sans réveil échoue en 5 à 25 secondes, le réveil n'est pas tenté et un message explicite s'affiche (voir [Dépannage](#dépannage)).
- **Scénarios** : la commande est utilisable dans un scénario et n'est pas bloquée par une fenêtre d'endormissement ouverte, qu'elle termine. Attention à ne pas la déclencher en boucle (par exemple sur le changement d'une information du véhicule) : chaque exécution réveille le véhicule. Sur un véhicule endormi, **Véhicule réveillé** passe brièvement à 0 (état lu avant le réveil) puis à 1.
- **Rafraîchir** garde son comportement : il ne réveille jamais le véhicule.

### Lecture accélérée pendant la charge

Pour suivre une charge de près (pilotage par surplus solaire, par exemple), réglez **Intervalle pendant la charge** dans l'équipement (désactivé par défaut) :

- **Déclenchement.** Dès qu'une lecture constate que le véhicule est **en charge** (état de charge Charging ou Starting), l'intervalle de charge remplace l'intervalle de rafraîchissement, à condition d'être plus court. Avec 5 minutes en normal et 1 minute en charge, les données sont relues chaque minute (observez **Dernière lecture des données**).
- **Retour à la normale.** Dès qu'une lecture ne constate plus la charge (fin de charge, câble débranché, charge suspendue), véhicule endormi, hors de portée ou proxy injoignable, l'intervalle normal est compté depuis cette lecture : aucun cycle de retard.
- **Plancher d'une minute.** Aucune valeur sous la minute n'est proposée : Jeedom lance le rafraîchissement chaque minute et le proxy garde les données 30 secondes en cache. Une valeur inférieure enregistrée par un script est ramenée à 1 minute (avertissement dans le log), une valeur inconnue désactive le réglage.
- **Aucun réveil.** Le contenu d'une lecture ne change pas : l'état sans réveil est lu, puis les données seulement si le véhicule est éveillé. Les données d'un véhicule endormi ne sont jamais lues du fait de ce réglage.

Pour suivre le mécanisme, passez le log du plugin en **Debug** : une ligne indique le passage à l'intervalle de charge, une autre le retour à l'intervalle normal.

Limites : la cadence de charge ne démarre qu'à la première lecture qui voit la charge (au plus un intervalle normal plus tard, ou tout de suite avec **Rafraîchir**) ; pendant une fenêtre d'endormissement ouverte, une charge lancée sans changement visible de l'état sans réveil n'est vue qu'à la lecture de contrôle ; si le proxy a été réglé avec une durée de cache des données d'au moins 60 secondes, les lectures à 1 minute lui sont servies depuis le cache ; une charge suspendue (état Stopped, câble branché) ne déclenche pas l'accélération, et sa reprise n'est vue qu'à l'intervalle normal ; un véhicule endormi en charge n'est pas lu plus vite ; un échec de lecture pendant la charge ramène l'intervalle normal jusqu'à la lecture suivante réussie.

### Laisser le véhicule s'endormir

Un véhicule éveillé s'endort de lui-même après une quinzaine de minutes sans sollicitation. Une lecture des données de charge et de climatisation toutes les quelques minutes peut l'en empêcher et consommer la batterie. Le plugin sait donc « se faire oublier » quand il n'y a rien de nouveau à lire :

- **Ouverture.** Quand le véhicule est éveillé, **hors charge** (état de charge Débranché, Terminée, Arrêtée ou Sans alimentation), **sans occupant**, et que ses données et son état sont **inchangés** sur le nombre de lectures réglé (3 par défaut), le plugin ouvre une **fenêtre d'endormissement** (30 minutes par défaut).
- **Pendant la fenêtre**, seule la lecture de l'état sans réveil est faite, à l'intervalle du véhicule (présence, verrouillage, veille, portières, coffres, trappe de charge, occupant). Les données de charge et de climatisation, la **Dernière lecture des données** et les durées de lecture des données ne sont plus mises à jour : elles gardent leur dernière valeur, comme pour un véhicule endormi. Le plugin ne réveille jamais le véhicule pour ces vérifications.
- **Fin de la fenêtre**, avec reprise de la lecture complète dès le passage suivant (au même passage pour une activité) : activité constatée sur l'état sans réveil (déverrouillage, portière, coffre ou trappe de charge, occupant), commande envoyée au véhicule (réveil explicite compris), bouton **Rafraîchir** ou **Rafraîchir (avec réveil)**, véhicule endormi, véhicule hors de portée, case décochée, ou fin de la durée. À la fin de la durée, une **lecture de contrôle** a lieu : si rien n'a changé, la fenêtre est prolongée.
- **Jamais en charge.** Un véhicule en charge, en démarrage de charge ou dans un état de charge inconnu n'ouvre jamais de fenêtre.
- **Maintien de climat actif.** Tant que **Maintien de climat (chien, camp)** vaut `On`, `Dog` ou `Party` (ou une autre valeur non prévue), aucune fenêtre ne s'ouvre : la lecture continue à l'intervalle du véhicule, pour que la **Température intérieure** reste à jour en mode chien ou camp. `Off`, `Unknown` ou une information absente (par exemple climatisation non lue) laissent la fenêtre s'ouvrir.
- **Climatisation non lue.** Avec **Lire aussi la climatisation** sur **Non, charge seule**, la fenêtre ne voit plus l'activité de la climatisation (ses informations ne sont pas lues). Basculer ce réglage remet à zéro le compte des lectures inchangées.

Pour suivre le mécanisme, passez le log du plugin en niveau **Info** : une ligne indique l'ouverture (« fenêtre d'endormissement ouverte pour … min … jusqu'à HH:MM environ ») et une autre la fin (« fin de la fenêtre d'endormissement après … min : … »). En **Debug**, chaque passage suspendu est noté. Pour vérifier l'effet, observez **Véhicule réveillé** : il devrait passer à 0 au bout du délai habituel (une quinzaine de minutes), alors qu'il pouvait rester à 1 sans fenêtre. C'est un effet attendu, non garanti : il dépend du véhicule. Si le véhicule ne s'endort pas, comparez avec la case décochée.

Limites : une charge démarrée sans aucun changement visible de l'état sans réveil (câble déjà branché, charge programmée ou lancée depuis l'application) n'est vue qu'à la lecture de contrôle, soit au plus la durée de la fenêtre plus un intervalle plus tard ; une climatisation lancée depuis l'application pendant la fenêtre, de même. Le brancher d'un câble depuis un état débranché est vu tout de suite (la trappe s'ouvre). Une clé téléphone proche qui garde l'occupant « présent » empêche l'ouverture de la fenêtre.

### Exécution des commandes

Chaque commande action est transmise au proxy, qui attend la confirmation du véhicule avant de répondre. Le plugin n'a pas besoin de réveiller le véhicule avant une commande : le proxy s'en charge.

**Valeurs contrôlées avant l'envoi.** Une valeur invalide est refusée tout de suite, avec un message, sans rien envoyer au proxy :

- **Courant de charge** : un nombre entier compris entre le **Min** et le **Max** de la commande (0 à 32 A tant que le véhicule n'a pas publié sa borne, puis le courant maximal qu'il annonce). Une valeur décimale (`16,5`) ou un texte est refusé.
- **Limite de charge** : un nombre entier compris entre le **Min** et le **Max** de la commande (50 à 100 % tant que le véhicule n'a pas publié ses bornes, puis ses limites minimale et maximale).
- **Mode sentinelle** : **Activé** ou **Désactivé** (l'ancienne option « Aucun » n'existe plus).

**Bornes suivies du véhicule.** À chaque lecture réussie des données, le plugin règle le **Min** et le **Max** des curseurs **Limite de charge** et **Courant de charge** sur ce que le véhicule accepte (informations **Limite de charge minimale**, **Limite de charge maximale** et **Courant de charge maximal**), et le curseur du widget suit sans recharger la page. Une valeur à 0, absente ou incohérente est ignorée : les bornes précédentes sont conservées, comme pendant que le véhicule dort. **Un réglage manuel prime** : si vous saisissez vous-même un **Min** ou un **Max** différent de celui que le plugin a posé, il n'est plus jamais modifié (même après plusieurs lectures ou un enregistrement de l'équipement) ; une valeur saisie égale à celle que le plugin a posée reste suivie (pour figer une borne, saisissez donc une valeur différente de celle posée par le plugin) ; toute autre valeur, même égale à celle du véhicule à cet instant, est un réglage manuel ; une borne que vous élargissez au-delà de celle du véhicule autorise une consigne que le véhicule pourra refuser. Pour revenir au suivi automatique, **videz** le champ : il est rétabli à la lecture suivante. Pour figer une borne (par exemple 48 A), réglez le **Max** à la main ; pour mettre les bornes à jour tout de suite, lancez **Rafraîchir (avec réveil)**. Le courant maximal peut dépendre de la borne branchée et n'est pas publié quand le véhicule est débranché : les bornes précédentes restent alors en place.

> **Changement de comportement** : une consigne **au-dessus du maximum annoncé par le véhicule** (par exemple 20 A quand il annonce 16 A) est désormais **refusée** avec un message, au lieu d'être acceptée puis ramenée silencieusement par le véhicule.

**En cas d'échec.** Si le proxy ou le véhicule refuse la commande, un message d'erreur apparaît en rouge dans l'interface de Jeedom (et dans le log du plugin en erreur), et il est aussi enregistré dans l'information **Dernière erreur**, où il reste affiché jusqu'au prochain cycle de lecture réussi (à la lecture suivante, 5 minutes au plus par défaut). Par exemple « Cette commande nécessite une clé de rôle Owner : la clé du proxy a probablement le rôle Charging Manager… » quand une commande réservée au rôle Owner est refusée : voir [Rôle de la clé](#rôle-de-la-clé).

**Après une commande réussie.** La limite de charge, le courant de charge et le verrouillage sont mis à jour immédiatement, puis l'état du véhicule (présence, éveil) est relu sans le réveiller. Le véhicule est ensuite **relu une fois** après un délai (30 secondes par défaut, réglable par véhicule), sans attendre la lecture périodique, pour afficher les valeurs réelles (voir [Relecture après une commande](#relecture-après-une-commande)). La commande, elle, rend la main tout de suite.

**Une commande ou une lecture à la fois.** Les échanges avec un même proxy se font l'un après l'autre : une commande, un **Rafraîchir** ou une vérification d'appairage n'attend que les échanges déjà en cours ou déjà en attente sur ce proxy (jusqu'à 2 minutes environ, 15 secondes pour la vérification) et passe avant les lectures périodiques, qui s'effacent et reprennent au cycle suivant. L'ordre de passage n'est pas garanti entre plusieurs demandes simultanées. Deux proxys différents ne s'attendent jamais, cycle périodique compris (le cycle lit les proxys en parallèle : voir Rafraîchissement). Si le proxy et le véhicule sont à la limite de leurs délais, la réponse peut prendre 3 à 4 minutes. Jeedom reste utilisable pendant ce temps.

### Relecture après une commande

Juste après une commande, le proxy renvoie encore ses données d'avant (il les garde **30 secondes** en cache). Plutôt que d'afficher une valeur périmée jusqu'au prochain rafraîchissement, le plugin **programme une relecture** du véhicule une fois ce cache expiré :

- **Déclenchement.** Après toute commande **réussie** (limite de charge, courant, démarrage ou arrêt de la charge, climatisation, verrouillage, trappe, etc.). Une commande en échec ne programme rien.
- **Délai.** Par défaut **30 secondes** après la fin de la commande, réglable par véhicule (**Délai de relecture après commande** : 30 secondes, 45 secondes, 1 minute, 1 minute 30 ou 2 minutes). Jamais moins de 30 secondes, la durée de cache du proxy : un délai plus court relirait la valeur d'avant la commande. Si vous avez allongé ce cache dans le proxy, choisissez un délai au moins égal.
- **La commande n'attend pas.** Elle rend la main dès qu'elle est exécutée ; la relecture part en arrière-plan.
- **Une seule relecture pour plusieurs commandes rapprochées.** Courant puis limite en quelques secondes : seule la relecture programmée après la **dernière** commande lit le véhicule, les précédentes abandonnent d'elles-mêmes.
- **Contenu de la relecture.** Celui d'un **Rafraîchir** : l'état sans réveil, puis les données de charge et de climatisation **seulement si le véhicule est éveillé**. **Elle ne réveille jamais le véhicule** : s'il s'est rendormi, ce n'est pas une erreur : les dernières valeurs sont conservées. S'il est hors de portée, la présence passe à « Non » ; si le proxy est injoignable, « Dernière erreur » est renseignée. Elle met fin à la fenêtre d'endormissement, comme une commande, et ne décale pas la cadence du rafraîchissement périodique.
- **Réveiller** relit donc aussi le véhicule ensuite, sans le réveiller de nouveau (la commande vient de le faire).
- **Coût.** Chaque commande réussie ajoute **une lecture Bluetooth** (état, puis données si éveillé) via le proxy. Un scénario qui règle le courant de charge chaque minute provoque une relecture par minute, en plus de la lecture périodique : espacez les commandes d'un scénario plutôt que de les répéter. Un klaxon ou un appel de phares déclenche aussi une relecture.
- **Processus.** Chaque relecture est une **tâche ponctuelle** du moteur de tâches de Jeedom (**Réglages > Système > Moteur de tâches**, **TeslaBLE::relectureApresCommande**) : elle y est visible quelques secondes à quelques minutes, puis disparaît seule. Une relecture remplacée par une commande plus récente disparaît au bout de quelques secondes. Ce n'est pas un démon et rien ne tourne en permanence. Si le moteur de tâches de Jeedom est désactivé, aucune relecture n'a lieu (comme pour le rafraîchissement périodique) et les valeurs sont mises à jour à la lecture suivante.

Pour suivre le mécanisme, passez le log du plugin en **Debug** : une ligne indique la programmation (« relecture programmée dans 30 s »), puis la relecture (« lecture sans réveil ») ou son abandon (« remplacée par une commande plus récente », « abandonnée : proxy occupé »).

### Pilotage selon le surplus

L'action **Ajuster selon le surplus** (`adjust_surplus`) suit un surplus photovoltaïque **sans saturer le véhicule de commandes Bluetooth** : chaque commande peut durer jusqu'à 75 secondes et réveille le véhicule. Votre scénario envoie la **puissance disponible pour la charge**, et le plugin décide s'il faut réellement agir. Les valeurs par défaut sont à valider en usage réel (voir [Limitations connues](#limitations-connues)).

**La valeur envoyée est une puissance absolue, en watts.** C'est ce que le véhicule peut consommer, pas une variation. Si votre compteur mesure l'**export réseau**, la puissance disponible est **l'export plus la puissance actuelle de charge** : sans cette addition, la consigne retomberait à chaque ajustement. Une valeur négative est ramenée à 0 W ; une valeur qui n'est pas un nombre de watts est refusée avec le message **« Valeur invalide : la puissance disponible doit être un nombre de watts »**.

**Du watt à l'ampère.** Le courant par phase vaut la puissance divisée par la **tension** et par le nombre de **phases** (deux réglages de l'équipement, jamais lus sur le véhicule), arrondi **vers le bas** au **pas d'ajustement**. ⚠️ Une borne triphasée réglée en monophasé donnerait **trois fois** le courant voulu : vérifiez le réglage **Phases**.

**Quand le plugin envoie une commande.** Au plus **une** commande par appel, parmi **Courant de charge**, **Démarrer la charge** et **Arrêter la charge** :

- le courant visé est borné par le **Max** du curseur **Courant de charge** (une valeur calculée plus haute est ramenée au Max ; à l'inverse, saisir à la main une valeur au-dessus du Max reste refusé) et n'est jamais réglé **sous le seuil d'arrêt** pendant la charge ;
- **rien n'est envoyé** si le courant visé est identique à la dernière consigne envoyée, ou s'en écarte de moins que l'**hystérésis** ;
- **au plus une commande par intervalle** : l'**intervalle minimal** est compté depuis la **fin** de la commande précédente, qu'elle ait réussi ou échoué ;
- **arrêt** : si le courant calculé reste sous le **seuil d'arrêt** pendant la **durée de maintien**, la charge est arrêtée ;
- **démarrage** : charge arrêtée, elle est relancée quand le courant calculé atteint le **courant minimal de démarrage**. Le démarrage se fait en **deux temps** quand la dernière consigne n'est pas connue, ou quand elle dépasse le courant visé d'au moins l'**hystérésis** : **Courant de charge** d'abord, **Démarrer la charge** à l'intervalle suivant (un intervalle de retard). Une fois **Courant de charge** envoyé à l'arrêt, la consigne reste tenue pour connue **tant que la charge n'a pas démarré**, quelle que soit la cadence de votre scénario : **Démarrer la charge** part alors directement. Sans cette poignée de main, la consigne n'est tenue pour connue que si la dernière commande du pilotage date de moins de 10 minutes ; elle est aussi oubliée dès que la charge est terminée, que la borne n'a plus de courant ou que le véhicule est débranché (le premier démarrage du lendemain commence donc par **Courant de charge**).

**Abstentions.** Aucune commande n'est envoyée, sans exception dans le scénario, et la raison apparaît dans **Dernière erreur** : **« Véhicule non branché : ajustement selon le surplus ignoré »**, **« Véhicule hors de portée du proxy : … »**, **« Charge terminée : … »**, **« La borne ne fournit pas de courant : … »** et **« État de charge inconnu : lancez Rafraîchir (avec réveil) »**. Ces messages ne remplacent jamais une vraie erreur du dernier cycle de lecture, et le cycle suivant réussi remet **Aucune**. Le pilotage se fonde sur le dernier **État charge** publié : après un démarrage ou un arrêt qu'il vient de commander, il considère l'état commandé jusqu'à la prochaine lecture (au plus 5 minutes). Activer l'**Intervalle pendant la charge** est recommandé.

**Aucun réveil.** Le pilotage ne réveille jamais le véhicule et ne lit rien pour décider ; un appel ignoré ne contacte pas le proxy. Une commande réellement envoyée réveille le véhicule comme toute commande.

**Heures creuses.** Pendant la plage de la **Charge aux heures creuses** d'un véhicule, l'appel de **Ajuster selon le surplus** est **ignoré** (sans erreur, sans commande, ligne Debug dans le log) : sans cela, un scénario solaire qui envoie 0 W la nuit arrêterait la charge des heures creuses. Hors plage, le pilotage selon le surplus fonctionne comme d'habitude (voir [Charge aux heures creuses](#charge-aux-heures-creuses)).

**Exemple de scénario.** Voir l'[exemple pas à pas : charge solaire avec Ajuster selon le surplus](#exemple-pas-à-pas--charge-solaire-avec-ajuster-selon-le-surplus). Ne multipliez pas les appels : le plugin ignore ceux qui n'apportent rien.

**Réglages invalides.** Un réglage hors bornes (pas à 0, intervalle sous 60 s, seuil d'arrêt supérieur au courant de démarrage…) est **refusé à l'enregistrement** de l'équipement, avec un message **« Pilotage selon le surplus : … »**.

### Programmer la charge

Les actions **Ajouter une programmation de charge** (`add_charge_schedule`) et **Supprimer la programmation de charge** (`remove_charge_schedule`) créent ou retirent dans le véhicule **une programmation de charge gérée par Jeedom**. Elles sont créées **masquées** : on les appelle depuis un scénario (ou on les rend visibles depuis l'onglet **Commandes**).

**Proxy du fork requis.** Le proxy officiel 2.3.0 ne sait pas programmer la charge : la route correspondante n'existe pas chez lui, elle a été ajoutée par le fork (versions de la forme `2.3.0-tb.N`). Tant que le proxy n'annonce pas ces deux commandes, elles sont **refusées sur-le-champ**, sans aucun échange avec le véhicule, avec le message **« Non supportée par votre version du proxy »** ; le reste de l'équipement fonctionne normalement. La disponibilité suit l'annonce du proxy (route `capabilities`), relue quand sa version change : après le passage au proxy du fork (version de la forme `2.3.0-tb.N`), les commandes deviennent disponibles sans réinstaller le plugin. Une mise à jour du fork **sans changement de numéro de version** n'est prise en compte que lorsque le numéro de version change.

**Paramètres.** Dans le scénario, l'action **Ajouter une programmation de charge** prend deux champs :

- **Jours de la programmation** (titre) : un ou plusieurs jours séparés par des virgules, des points-virgules ou des espaces, sans tenir compte de la casse : `lun`, `mar`, `mer`, `jeu`, `ven`, `sam`, `dim` (ou le nom entier, ou l'abréviation anglaise `mon`… `sun`), `tous` (tous les jours) ou `semaine` (du lundi au vendredi). Exemple : `lun,mar,mer,jeu,ven`.
- **Heure de début (HH:MM)** (message) : de `00:00` à `23:59`, par exemple `23:00` (`23h00` est aussi accepté). C'est l'**heure locale du véhicule**.

Tout paramètre invalide est refusé **avant** l'envoi, avec un message qui explique le format attendu ; rien n'est envoyé au véhicule.

**Coordonnées de Jeedom.** Le véhicule déclenche une programmation seulement s'il se trouve au lieu indiqué. Le plugin utilise les **coordonnées de Jeedom** (Réglages, Système, Configuration, onglet **Général**, rubrique **Coordonnées** : latitude et longitude) : renseignez-les, sinon la commande est refusée avec le message **« Coordonnées de Jeedom absentes ou invalides »**. Si le véhicule n'est pas stationné à ce lieu, la programmation existe mais ne se déclenche pas. Les coordonnées ne sont jamais écrites dans les logs.

**Une seule programmation, remplacée à chaque ajout.** Le plugin gère **une** programmation par véhicule et mémorise son identifiant : un nouvel ajout **remplace** la programmation précédente (mêmes jours et heure remplacés, sans doublon en principe : le remplacement par identifiant est à confirmer en usage réel). La programmation couvre la charge à partir de l'heure de début ; il n'y a ni heure de fin, ni courant, ni limite propres à la programmation. Les programmations créées dans l'application Tesla ne sont ni modifiées ni supprimées. Si vous changez la VIN de l'équipement, l'identifiant mémorisé n'est plus utilisé : le prochain ajout crée une nouvelle programmation.

**Suppression.** **Supprimer la programmation de charge** retire la programmation créée par Jeedom. Si Jeedom n'en a créé aucune (ou si elle est déjà supprimée), l'action ne fait rien et ne produit **aucune erreur**. Si le véhicule refuse la suppression pour une autre raison qu'un rôle de clé insuffisant (par exemple parce que la programmation a été supprimée dans l'application), le message de refus s'affiche et l'identifiant est oublié : une seconde suppression est silencieuse et un nouvel ajout crée une nouvelle programmation.

**Après la commande.** Une relecture est programmée comme après toute commande (voir [Relecture après une commande](#relecture-après-une-commande)) : les informations de programmation (**Heure de charge programmée**…) sont mises à jour **si le véhicule les renvoie** à la lecture des données ; la planification se vérifie aussi dans l'application Tesla.

**Rôle de la clé.** Le rôle minimal nécessaire n'est pas confirmé (**Charging Manager** probable). Un refus d'autorisation s'affiche avec l'indication « rôle de la clé du proxy insuffisant ? » (voir [Rôle de la clé](#rôle-de-la-clé)).

### Charge aux heures creuses

Le plugin peut **démarrer et arrêter la charge lui-même** pendant les heures creuses de votre contrat d'électricité, jusqu'à un **SoC cible** choisi. Cela fonctionne avec le proxy officiel 2.3.0 et **ne dépend pas des programmations stockées dans le véhicule** (voir [Programmer la charge](#programmer-la-charge) pour celles-ci). Les réglages sont dans la section **Charge aux heures creuses** de l'équipement ; cochez **Activer** (**Pilotage de la charge**), renseignez **Début de plage**, **Fin de plage** et **SoC cible (%)**, puis sauvegardez.

**Pas à pas : configurer la charge aux heures creuses.**

1. Ouvrez **Plugins > Communication des objets > Tesla BLE**, puis l'équipement du véhicule (onglet **Equipement**), section **Charge aux heures creuses**.
2. Cochez **Activer** (**Pilotage de la charge**).
3. Renseignez **Début de plage** et **Fin de plage** d'après votre contrat d'électricité, à l'heure de Jeedom, par exemple `22:00` et `06:00` (plage à cheval sur minuit acceptée ; la fin doit différer du début).
4. Renseignez **SoC cible (%)** : le niveau de batterie, de 1 à 100, auquel Jeedom arrête la charge. Choisissez une cible **inférieure ou égale à la limite de charge du véhicule**.
5. Cochez **Arrêter en fin de plage** si la charge ne doit pas se poursuivre au-delà des heures creuses (décochée : elle continue jusqu'à la limite du véhicule).
6. Pour un arrêt précis au SoC cible, réglez aussi **Intervalle pendant la charge** sur 1 ou 2 minutes (voir plus bas, **Précision**).
7. **Sauvegardez**. Un réglage invalide est refusé avec un message **« Charge aux heures creuses : … »** (voir [Dépannage](#dépannage)) : rien n'est enregistré.
8. Vérifiez : passez le log du plugin en **Info** (**Configuration du plugin > Logs**). À la première lecture du véhicule dans la plage, une ligne **« charge aux heures creuses : décision … »** indique ce que le plugin a décidé et pourquoi (`charge_start`, `charge_stop`, `aucune`…). Si rien ne démarre, consultez [Charge avancée : symptômes sans message](#charge-avancée--symptômes-sans-message).

**À retenir.** Deux comportements surprennent souvent :

- **Limite de charge du véhicule.** Si le **SoC cible** est **au-dessus** de la limite de charge du véhicule, la charge s'arrête à la limite du véhicule, sans erreur ni avertissement : le SoC cible n'est jamais atteint. À l'inverse, un SoC cible plus bas que la limite arrête la charge plus tôt.
- **Action manuelle.** Un **Démarrer la charge** ou un **Arrêter la charge** lancé depuis Jeedom (widget, scénario) pendant la plage **suspend le pilotage jusqu'à la plage suivante** : Jeedom ne contredit jamais votre action. Une charge relancée depuis l'application Tesla après l'arrêt au SoC cible suspend aussi le pilotage.

**Ce que fait le plugin.** À chaque lecture du véhicule par le cycle de rafraîchissement :

- **dans la plage**, véhicule **branché** et **sous le SoC cible** : **Démarrer la charge** ;
- **dans la plage**, charge en cours dont le niveau atteint le SoC cible : **Arrêter la charge**, **même si la limite de charge du véhicule est plus haute** (le SoC cible est comparé au **Niveau de batterie (brut)**, qui peut différer de quelques points de **Charge batterie**) ;
- **à la fin de la plage**, si **Arrêter en fin de plage** est coché : la charge encore en cours est arrêtée à la première lecture du véhicule, **dans l'heure qui suit** la fin (au-delà, la charge n'est plus interrompue) ;
- **aucune commande inutile** : pas de démarrage si la charge est déjà en cours ou si la cible est atteinte, pas d'arrêt si elle est déjà arrêtée. **Au plus une commande par lecture.**

**Heure de Jeedom.** La plage se lit à l'heure de Jeedom (son fuseau), pas à celle du véhicule. Une plage à cheval sur minuit (`22:00` à `06:00`) fonctionne ; le début est inclus, la fin est exclue.

**Précision.** La décision suit la **cadence de lecture** du véhicule : l'arrêt au SoC cible peut dépasser de quelques pour cent si la lecture est espacée. Pour un arrêt précis, activez l'**Intervalle pendant la charge** (1 ou 2 minutes, voir [Lecture accélérée pendant la charge](#lecture-accélérée-pendant-la-charge)). Un intervalle de rafraîchissement de **15 minutes au plus** est recommandé : avec un intervalle long, l'état publié peut être périmé.

**Veille du véhicule.** Le plugin **ne réveille jamais le véhicule de lui-même** pour décider : il s'appuie sur les informations déjà publiées. En revanche, **Démarrer la charge réveille le véhicule** (le proxy le fait seul) comme toute commande, et un véhicule vu **endormi** ne reçoit **jamais** de commande d'arrêt (une charge publiée par un véhicule endormi est un état périmé). Quand l'état affiché date d'un véhicule endormi, le message de **Dernière erreur** le précise (« état lu à HH:MM, véhicule endormi »).

**Aucune action dans ces cas.** La fonction est désactivée ; le véhicule est **débranché**, **hors de portée** ou n'a pas pu être lu ; la borne ne fournit pas de courant ; l'état de charge est inconnu ; la charge est **terminée** (limite du véhicule atteinte) ; le **SoC cible dépasse la limite du véhicule** (la charge s'arrête alors à cette limite, sans erreur ni avertissement : choisissez une cible inférieure ou égale à la limite). La raison est visible dans **Dernière erreur** : **« Véhicule non branché : charge aux heures creuses en attente »**, **« La borne ne fournit pas de courant : charge aux heures creuses en attente »** ou **« État de charge inconnu : lancez Rafraîchir (avec réveil) »**. Ces messages ne remplacent jamais une vraie erreur du dernier cycle de lecture, et le cycle suivant réussi remet **Aucune**.

**Commandes manuelles et scénarios (priorité).** **Démarrer la charge** et **Arrêter la charge** restent utilisables à tout moment. Un **Démarrer** ou un **Arrêter** lancé **depuis Jeedom** (widget, scénario) **pendant la plage**, ou dans l'heure qui suit sa fin, **suspend le pilotage jusqu'à la plage suivante** : Jeedom ne contredit jamais votre action, et n'arrête pas non plus la charge en fin de plage. Le lendemain, le pilotage reprend. Le message n'est qu'une ligne du log (aucune erreur). Deux cas sont traités à part :

- **charge relancée depuis l'application Tesla après l'arrêt au SoC cible** : constatée par une lecture au moins **2 minutes** après l'arrêt, elle suspend aussi le pilotage (**« Charge aux heures creuses suspendue jusqu'à la prochaine plage : charge relancée hors du pilotage »**) et n'est plus interrompue ;
- **charge arrêtée depuis l'application après un démarrage par Jeedom** : Jeedom **ne redémarre pas** la charge (un seul démarrage par branchement) ; si le démarrage n'est pas suivi d'une charge, le message **« Charge démarrée par Jeedom mais arrêtée ou non démarrée : aucun nouvel essai avant la prochaine plage »** s'affiche (voir [Dépannage](#dépannage)).

**Échecs de commande.** Une commande qui échoue (refus du véhicule, délai dépassé, rôle de clé insuffisant) affiche son message dans **Dernière erreur** et un avertissement apparaît dans le log ; la nouvelle tentative a lieu à la lecture suivante, **sans rafale**. Après **3 échecs de suite**, le pilotage est **suspendu jusqu'à la plage suivante** (**« Charge aux heures creuses suspendue jusqu'à la prochaine plage : échecs de commande répétés »**) ; un **débranchement** suivi d'un rebranchement le relance. Un proxy **injoignable** ou **occupé** n'est pas un échec : rien n'est envoyé, le plugin réessaie à la lecture suivante (un avertissement par heure au plus signale une commande reportée).

**Réglages invalides.** Une heure qui n'est pas au format `HH:MM`, un SoC cible hors de **1 à 100**, une plage vide (fin égale au début) ou une fonction activée sans début, fin ou SoC cible est **refusé à l'enregistrement** de l'équipement, avec un message **« Charge aux heures creuses : … »** ; rien n'est enregistré.

**Autres fonctions.** Le pilotage selon le surplus est **ignoré pendant la plage** (voir [Pilotage selon le surplus](#pilotage-selon-le-surplus)). Une programmation de charge du véhicule ([Programmer la charge](#programmer-la-charge)) ou de l'application Tesla peut **entrer en conflit** avec la plage : n'en gardez qu'une, la plage de Jeedom n'étant pas coordonnée avec elles. **Une seule plage** par véhicule.

### Régler la consigne de température

Les actions **Consigne conducteur** (`set_driver_temp`) et **Consigne passager** (`set_passenger_temp`) règlent, en °C, la température demandée côté conducteur et côté passager. Ce sont des curseurs, liés aux informations **Température conducteur** et **Température passager**.

**Proxy du fork requis, commandes masquées.** Le proxy officiel 2.3.0 ne sait pas régler la consigne de température : la commande correspondante a été ajoutée par le fork (version `2.3.0-tb.1` au minimum). Tant que le proxy n'annonce pas cette commande, les deux actions sont **refusées sur-le-champ**, sans aucun échange avec le véhicule, avec le message **« Non supportée par votre version du proxy »** ; le reste de l'équipement fonctionne normalement. Elles sont créées **masquées** : après le passage au proxy du fork, cochez **Afficher** sur chacune dans l'onglet **Commandes** de l'équipement, ou appelez-les depuis un scénario. La disponibilité suit l'annonce du proxy (route `capabilities`), relue quand sa version change : après le passage au fork, les commandes deviennent utilisables sans réinstaller le plugin.

**Plage et pas.** Le curseur va de **15 à 28 °C** par pas de **0,5 °C**. Une fois les données du véhicule lues, ses bornes suivent la température minimale et la température maximale réglables du véhicule, **arrondies vers l'intérieur** au degré entier (15,5 devient 16 ; 27,5 devient 27) et limitées à 15 à 28 °C, plage acceptée par le proxy. Un **Min** ou un **Max** que vous réglez à la main sur la commande n'est jamais réécrit. Une valeur hors plage, ou qui n'est pas un nombre, est refusée **avant** l'envoi avec le message **« Valeur invalide : la consigne doit être un nombre entre … et … °C »** ; rien n'est envoyé au véhicule. Une valeur entre deux demi-degrés est **arrondie au demi-degré le plus proche** (21,3 devient 21,5), car le véhicule règle par demi-degré.

**L'autre côté repart avec sa dernière valeur lue.** Le véhicule reçoit toujours les deux températures dans la même commande. Régler le côté conducteur renvoie donc aussi la consigne passager, avec la dernière valeur publiée par l'information **Température passager**, et inversement. Si cette valeur est inconnue (jamais lue, nulle ou hors de 15 à 28 °C), le véhicule reçoit la **même valeur des deux côtés**. Si vous avez réglé l'autre côté sur l'écran du véhicule depuis la dernière lecture de Jeedom, **cette consigne peut être écrasée** : lancez **Rafraîchir (avec réveil)** avant de régler un côté pour partir de la valeur à jour.

**Après la commande.** L'information liée est mise à jour tout de suite, puis l'état est relu et une relecture est programmée comme après toute commande (voir [Relecture après une commande](#relecture-après-une-commande)) : la consigne réellement appliquée apparaît à la relecture. Le véhicule est réveillé par le proxy si besoin.

**Rôle de la clé.** Le rôle **Owner** est supposé nécessaire (à confirmer en usage réel). Avec une clé Charging Manager, le refus du véhicule s'affiche avec le message de rôle insuffisant (voir [Rôle de la clé](#rôle-de-la-clé)).

### Chauffer les sièges et le volant

Six actions règlent le chauffage : **Régler le chauffage du siège avant gauche** (`set_seat_heater_left`), **avant droit** (`set_seat_heater_right`), **arrière gauche** (`set_seat_heater_rear_left`), **arrière droit** (`set_seat_heater_rear_right`), **arrière centre** (`set_seat_heater_rear_center`) et **Régler le chauffage du volant** (`set_steering_wheel_heater`). Ce sont des listes de choix.

**Proxy du fork requis (version `2.3.0-tb.2` au minimum), commandes masquées.** Le proxy officiel 2.3.0 ne sait pas régler le chauffage des sièges ni du volant : ces commandes ont été ajoutées par le fork. Tant que le proxy n'annonce pas la commande, les six actions sont **refusées sur-le-champ**, sans aucun échange avec le véhicule, avec le message **« Non supportée par votre version du proxy »** ; le reste de l'équipement fonctionne normalement. Elles sont créées **masquées**, y compris après le passage au fork : **à vous de les afficher** (cochez **Afficher** sur chacune dans l'onglet **Commandes** de l'équipement) ou de les appeler depuis un scénario. La disponibilité suit l'annonce du proxy (route `capabilities`), relue quand sa version change : après le passage au fork, les commandes deviennent utilisables sans réinstaller le plugin.

**Niveaux.** Pour un siège : **Arrêt** (0), **Bas** (1), **Moyen** (2), **Haut** (3). Une valeur envoyée par un scénario hors de 0 à 3, ou qui n'est pas un entier, est refusée **avant** l'envoi avec le message **« Valeur invalide : le niveau de chauffage doit être un entier entre 0 et 3 »**. Pour le volant : **Arrêt** (0) ou **Marche** (1) seulement, il n'y a pas de niveau ; le plugin n'écrit pas l'information **Niveau chauffage volant** après la commande, seule la relecture la met à jour. Une valeur hors de 0 ou 1 est refusée avec le message **« Valeur invalide : le chauffage du volant doit être 0 (arrêt) ou 1 (marche) »**.

**Quel siège ?** Les sièges se désignent par leur **position** : « avant gauche » et « avant droit » ne dépendent pas du côté du volant. Les informations existantes gardent leur nom : en conduite à gauche, **Chauffage siège conducteur** correspond à l'**avant gauche** et **Chauffage siège passager** à l'**avant droit** (l'inverse en conduite à droite). Les dossiers et la troisième rangée ne sont pas proposés. Un siège que le véhicule n'a pas peut être refusé par le véhicule, ou accepté sans effet et relu à 0 (à vérifier en usage réel).

**Climatisation.** Selon la documentation de Tesla, le chauffage des sièges demande que la climatisation soit en marche (préconditionnement ou maintien de climat) ; sans elle, la commande peut être refusée ou ignorée par le véhicule. De même, sur un véhicule à chauffage automatique du volant, la commande du volant peut rester sans effet. Ces comportements sont à valider en usage réel.

**Après la commande.** L'information liée (par exemple **Chauffage siège passager**) est mise à jour tout de suite avec le niveau demandé, puis l'état est relu et une relecture est programmée comme après toute commande (voir [Relecture après une commande](#relecture-après-une-commande)) : le niveau réellement appliqué apparaît à la relecture. Avec **Lire aussi la climatisation** sur **Non, charge seule**, ces informations ne sont pas relues : elles gardent la valeur annoncée. Le véhicule est réveillé par le proxy si besoin.

**Rôle de la clé.** Le rôle **Owner** est supposé nécessaire (à confirmer en usage réel). Avec une clé Charging Manager, le refus du véhicule s'affiche avec le message de rôle insuffisant (voir [Rôle de la clé](#rôle-de-la-clé)).

### Dégivrage maximal

Une action **Dégivrage maximal** (`set_preconditioning_max`) active ou arrête le dégivrage maximal du véhicule (désembuage et dégivrage des vitres et des rétroviseurs). C'est une liste de choix : **Arrêt** (0) ou **Marche** (1). Elle est liée à l'information **Mode dégivrage** (`defrost_mode`, valeurs `Off`, `Normal` ou `Max`), et les informations de dégivrage avant et arrière (`is_front_defroster_on`, `is_rear_defroster_on`) sont relues avec elle.

**Proxy du fork requis (version `2.3.0-tb.1` au minimum), commande masquée.** Le proxy officiel 2.3.0 ne sait pas commander le dégivrage maximal : la commande a été ajoutée par le fork. Tant que le proxy n'annonce pas la commande, l'action est **refusée sur-le-champ**, sans aucun échange avec le véhicule, avec le message **« Non supportée par votre version du proxy »** ; le reste de l'équipement fonctionne normalement. Elle est créée **masquée**, y compris après le passage au fork : **à vous de l'afficher** (cochez **Afficher** dans l'onglet **Commandes** de l'équipement) ou de l'appeler depuis un scénario. La disponibilité suit l'annonce du proxy (route `capabilities`), relue quand sa version change : après la mise à jour du proxy, la commande devient utilisable sans réinstaller le plugin.

> ⚠️ **Consommation et réveil.** Activer le dégivrage maximal **réveille le véhicule** (via le proxy) et **consomme de la batterie** tant qu'il fonctionne. Le plugin ne le lance **jamais** de lui-même : seule une action de votre part (widget ou scénario) l'envoie. Pensez à l'arrêter, par exemple avec un second scénario après la durée souhaitée.

**Valeurs.** Une valeur envoyée par un scénario autre que 0 ou 1 est refusée **avant** l'envoi avec le message **« Valeur invalide : le dégivrage maximal doit être 0 (arrêt) ou 1 (marche) »**.

**Après la commande.** **Mode dégivrage** passe tout de suite à `Max` (marche) ou `Off` (arrêt), puis l'état est relu et une relecture est programmée comme après toute commande (voir [Relecture après une commande](#relecture-après-une-commande)) : la valeur réelle apparaît à la relecture (à l'arrêt, le véhicule peut indiquer `Normal` si la climatisation tourne encore). Les dégivrages avant et arrière ne sont mis à jour qu'à cette relecture. Avec **Lire aussi la climatisation** sur **Non, charge seule**, ou si le véhicule se rendort, ces informations ne sont pas relues : elles gardent la valeur annoncée.

**Rôle de la clé.** Le rôle **Owner** est supposé nécessaire (à confirmer en usage réel). Avec une clé Charging Manager, le refus du véhicule s'affiche avec le message de rôle insuffisant et le badge **Rôle insuffisant** (voir [Rôle de la clé](#rôle-de-la-clé)).

### Mode chien, camp et maintien de climat

Une action **Mode de maintien de climat** (`set_climate_keeper_mode`) choisit le maintien de climatisation du véhicule garé : **Arrêt** (0), **Maintien** (1), **Mode chien** (2) ou **Mode camp** (3). Elle est liée à l'information **Maintien de climat (chien, camp)** (`climate_keeper_mode`, valeurs `Off`, `On`, `Dog`, `Party` ou `Unknown`) : le mode camp y apparaît sous le nom `Party` d'après le véhicule (à confirmer en usage réel).

**Proxy du fork requis (version `2.3.0-tb.1` au minimum), commande masquée.** Le proxy officiel 2.3.0 ne sait pas commander le maintien de climat : la commande a été ajoutée par le fork. Tant que le proxy n'annonce pas la commande, l'action est **refusée sur-le-champ**, sans aucun échange avec le véhicule, avec le message **« Non supportée par votre version du proxy »** ; le reste de l'équipement fonctionne normalement. Elle est créée **masquée**, y compris après le passage au fork : **à vous de l'afficher** (cochez **Afficher** dans l'onglet **Commandes** de l'équipement) ou de l'appeler depuis un scénario. La disponibilité suit l'annonce du proxy (route `capabilities`), relue quand sa version change : après la mise à jour du proxy, la commande devient utilisable sans réinstaller le plugin.

> ⚠️ **Batterie et réveil.** Choisir un maintien **réveille le véhicule** (via le proxy) et **consomme de la batterie sur une longue durée** ; le véhicule peut refuser (batterie faible, état du véhicule). Le plugin ne le lance **jamais** de lui-même et ne l'arrête jamais : seule une action de votre part (widget ou scénario) l'envoie.

> ⚠️ **Animal.** Ce mode **ne remplace pas une surveillance de la température** de l'habitacle pour un animal. La lecture suit l'intervalle de rafraîchissement du véhicule : une alerte doit s'appuyer sur la **Température intérieure** et sur un intervalle adapté.

**Valeurs.** Une valeur envoyée par un scénario hors de 0 à 3 est refusée **avant** l'envoi avec le message **« Valeur invalide : le mode de maintien de climat doit être 0 (arrêt), 1 (maintien), 2 (chien) ou 3 (camp) »**.

**Après la commande.** **Maintien de climat (chien, camp)** passe tout de suite à `Off`, `On`, `Dog` ou `Party`, puis l'état est relu et une relecture est programmée comme après toute commande (voir [Relecture après une commande](#relecture-après-une-commande)) : la valeur réelle apparaît à la relecture. Avec **Lire aussi la climatisation** sur **Non, charge seule** (laissez **Oui** pour ce mode), ou si le véhicule se rendort, l'information n'est pas relue : elle garde la valeur annoncée, et la fenêtre d'endormissement peut s'ouvrir (voir [Laisser le véhicule s'endormir](#laisser-le-véhicule-sendormir)).

**Rôle de la clé.** Le rôle **Owner** est supposé nécessaire (à confirmer en usage réel). Avec une clé Charging Manager, le refus du véhicule s'affiche avec le message de rôle insuffisant et le badge **Rôle insuffisant** (voir [Rôle de la clé](#rôle-de-la-clé)).

### Préconditionnement planifié par Jeedom

Le plugin peut **démarrer la climatisation avant l'heure de départ** puis l'arrêter, avec la température déjà réglée dans le véhicule. Cela fonctionne avec le proxy officiel 2.3.0 (commandes **Démarrer le climatiseur** et **Arrêter le climatiseur**), sans fork. Les réglages sont dans la section **Préconditionnement planifié par Jeedom** de l'équipement ; ne la confondez pas avec l'information **Préconditionnement planifié** (`scheduled_preconditioning_time`), qui **lit** la programmation faite dans le véhicule.

**Pas à pas : configurer le préconditionnement planifié.**

1. Ouvrez **Plugins > Communication des objets > Tesla BLE**, puis l'équipement du véhicule (onglet **Equipement**), section **Préconditionnement planifié par Jeedom**.
2. Renseignez l'**Heure de départ**, à l'heure de Jeedom, par exemple `07:30`.
3. Cochez les **Jours** de départ concernés.
4. Réglez l'**Avance (min)** (vide : 15 minutes) et la **Durée maximale (min)** (vide : 30 minutes, ou l'avance plus 15 minutes si l'avance dépasse 15). Avec 15 et 30, la climatisation démarre à `07:15` et s'arrête à `07:45`.
5. Cochez **Seulement si branché** si la climatisation ne doit pas puiser dans la batterie d'un véhicule débranché.
6. Cochez **Activer** (**Pilotage de la climatisation**), puis **sauvegardez**. Un réglage invalide est refusé avec un message **« Préconditionnement planifié : … »** (voir [Dépannage](#dépannage)) : rien n'est enregistré.
7. Vérifiez : passez le log du plugin en **Info**. À la première lecture du véhicule dans la fenêtre, une ligne **« préconditionnement planifié : décision … »** indique ce que le plugin a décidé et pourquoi.

**Exemple d'usage : départ en semaine à 7 h 30.** Réglez **Heure de départ** sur `07:30`, cochez **Lundi** à **Vendredi**, laissez **Avance** à 15 et **Durée maximale** à 30, cochez **Seulement si branché** et **Activer**. Le véhicule reste branché la nuit :

- Si vous utilisez aussi la [Charge aux heures creuses](#charge-aux-heures-creuses) (par exemple `22:00` à `06:00`), la charge se termine avant la fenêtre du préconditionnement, qui va de `07:15` à `07:45` : les deux fonctions ne se gênent pas.
- Du lundi au vendredi, à la première lecture du véhicule après `07:15`, la climatisation est démarrée si elle est arrêtée et si le véhicule est branché. Le log du plugin (niveau **Info**) affiche **« préconditionnement planifié : décision `auto_conditioning_start` (demarrage) »**, et l'information **Climatisation activée** passe à 1 à la lecture suivante.
- À la première lecture qui suit `07:45`, si la climatisation tourne encore après ce démarrage par Jeedom, elle est arrêtée (décision `auto_conditioning_stop`).
- Le samedi et le dimanche, rien ne se passe. Si vous partez avant `07:45`, arrêtez la climatisation vous-même depuis Jeedom : Jeedom ne la relance pas ensuite.

**La fenêtre.** Elle commence à l'heure de départ **moins l'avance** et dure la **durée maximale** à partir de ce début (début inclus, fin exclue). Le jour retenu est celui de l'**heure de départ** : un départ à `00:10` avec 20 minutes d'avance démarre la veille à `23:50`, et c'est le jour du lendemain qu'il faut cocher. Tout est à l'**heure de Jeedom** (son fuseau), pas celle du véhicule ; un départ qui tombe dans l'heure sautée du changement d'heure d'été est décalé d'une heure.

**Ce que fait le plugin.** À chaque lecture réussie du véhicule par le cycle de rafraîchissement, **dans la fenêtre** : si la climatisation est arrêtée (et, avec l'option, le véhicule branché), **Démarrer le climatiseur** (**un seul démarrage réussi par départ**) ; **à la première lecture qui suit la fin de la fenêtre** (dans l'heure), si la climatisation tourne encore après un démarrage de Jeedom, **Arrêter le climatiseur**. Au plus **une commande par lecture**, aucune commande inutile.

**Précision.** La décision suit la **cadence de lecture** du véhicule : le démarrage peut arriver quelques minutes après l'heure prévue, et l'arrêt dépasser la fin d'un intervalle. Un intervalle de rafraîchissement de **5 minutes au plus** est conseillé. Avec un intervalle plus long que la durée de la fenêtre, aucune lecture ne tombe dedans : ni démarrage ni arrêt. Un démarrage est encore possible **après l'heure de départ**, tant que la fenêtre n'est pas finie.

**Veille du véhicule.** Le plugin **ne réveille jamais le véhicule de lui-même** pour décider et n'envoie jamais de commande de réveil, mais **Démarrer le climatiseur réveille le véhicule** (le proxy le fait seul) et consomme de la batterie. Un véhicule vu **endormi** ne reçoit **jamais** de commande d'arrêt : sa climatisation est tenue pour arrêtée.

**Priorité à vos actions.** Jeedom ne contredit jamais votre action :

- un **Démarrer le climatiseur** ou **Arrêter le climatiseur** lancé **depuis Jeedom** (widget, scénario) pendant la fenêtre **suspend le préconditionnement jusqu'au départ suivant**, et la climatisation n'est pas arrêtée en fin de fenêtre ;
- une climatisation **déjà en marche** à l'arrivée dans la fenêtre (ou lancée depuis l'application Tesla, ou par la programmation du véhicule) n'est ni relancée ni arrêtée ;
- une climatisation **arrêtée depuis l'application** après le démarrage de Jeedom (constatée par une lecture au moins **2 minutes** après la commande) n'est pas relancée en boucle ;
- un **mode chien, camp, maintien** ou un **dégivrage maximal** en cours n'est jamais arrêté ni remplacé.

Désactiver la fonction ou modifier ses réglages **pendant la fenêtre n'arrête pas** une climatisation déjà démarrée.

**Rôle de la clé.** Le rôle **Owner** est supposé nécessaire (à confirmer en usage réel). Avec une clé Charging Manager, le véhicule refuse la commande : le message de rôle insuffisant s'affiche dans **Dernière erreur**, l'information **Rôle de clé** passe à **Charging Manager**, et **un seul essai est fait par départ** (voir [Rôle de la clé](#rôle-de-la-clé)).

**Échecs de commande.** Une commande qui échoue (refus du véhicule, délai dépassé) affiche son message dans **Dernière erreur** et un avertissement apparaît dans le log ; la nouvelle tentative a lieu à la lecture suivante, **sans rafale**. Après **3 échecs de suite**, le pilotage est **suspendu jusqu'au départ suivant**. Un proxy **injoignable** ou **occupé** n'est pas un échec : rien n'est envoyé, le plugin réessaie à la lecture suivante.

**Aucune action dans ces cas.** La fonction est désactivée ou le jour n'est pas coché ; le véhicule n'a pas pu être lu ou est **hors de portée** ; avec l'option, le véhicule est **débranché** ou son état de charge est inconnu ; l'état de la climatisation est inconnu ; la climatisation tourne déjà. La raison est visible dans **Dernière erreur** pour les cas utiles (**« Véhicule non branché : préconditionnement planifié non lancé »**, **« État de charge inconnu : lancez Rafraîchir (avec réveil) »**), sans jamais remplacer une vraie erreur du dernier cycle de lecture.

**Autres fonctions.** Le préconditionnement planifié est **indépendant** de la programmation faite dans le véhicule ([Préconditionnement planifié](#informations) lu par le plugin) : si le véhicule préconditionne déjà, la climatisation est vue active et Jeedom n'intervient pas. Il peut s'enchaîner, au même passage, avec la [Charge aux heures creuses](#charge-aux-heures-creuses) : les deux commandes partent l'une après l'autre. Le plugin ne tient pas compte de la présence d'un occupant : une climatisation démarrée par Jeedom et encore en marche à la première lecture qui suit la fin de la fenêtre est arrêtée.

### Confirmation des actions sensibles

Cinq actions demandent une **confirmation** avant l'envoi, sur le dashboard et sur mobile : **Déverrouiller les portes** (`door_unlock`), **Ouvrir la trappe de charge** (`charge_port_door_open`), **Mode sentinelle** (`set_sentry_mode`), **Ouvrir le coffre arrière** (`open_trunk_rear`) et **Ouvrir le frunk** (`open_trunk_front`). Les autres actions (verrouiller, klaxonner, feux, charge, climat…) partent au premier clic.

- **Un clic ouvre une fenêtre de confirmation.** Rien n'est envoyé tant que vous n'avez pas confirmé.
- **Case « Confirmer l'action ».** Elle se trouve dans les paramètres avancés de la commande (onglet **Commandes** de l'équipement, roue crantée de la commande). Elle est **cochée à la création** ; décochez-la pour retirer la confirmation d'une commande, cochez-la sur une autre pour en ajouter une. Votre choix n'est jamais réécrit par le plugin (mise à jour comprise : sur un équipement existant, la mise à jour pose la confirmation une seule fois, sauf là où vous l'aviez déjà réglée).
- **Un scénario n'est pas concerné.** Une action appelée depuis un scénario s'exécute **sans confirmation**. Un appel par l'API JSON-RPC de Jeedom doit passer `confirmAction=1`, sinon Jeedom le refuse.

> **IMPORTANT : ce n'est pas une protection de sécurité.** La confirmation est un garde-fou d'interface contre le clic accidentel, rien de plus. Le proxy n'a **aucune authentification** par défaut : toute machine de votre réseau qui peut le joindre peut déverrouiller ou ouvrir le véhicule **sans passer par Jeedom**, donc sans confirmation. Gardez le proxy sur un réseau de confiance, jamais exposé sur Internet (voir [Rôle de la clé](#rôle-de-la-clé)).

Pour **Mode sentinelle**, l'état affiché après l'ordre est décrit dans [État du mode sentinelle](#état-du-mode-sentinelle) (provenance **Réel** ou **Dernier ordre**).

### Ouvrir le coffre arrière et le frunk

Deux actions ouvrent un coffre à distance : **Ouvrir le coffre arrière** (`open_trunk_rear`) et **Ouvrir le frunk** (`open_trunk_front`, le coffre avant). Elles envoient la même commande du proxy, `actuate_trunk`, avec le coffre visé. L'état se lit dans les informations **Coffre arrière** (`trunk_rear`) et **Coffre avant (frunk)** (`trunk_front`).

**Proxy du fork requis (version `2.3.0-tb.2` au minimum), commandes masquées.** Le proxy officiel 2.3.0 n'a pas cette commande : elle a été ajoutée par le fork. Tant que le proxy n'annonce pas la commande, les deux actions sont **refusées sur-le-champ**, sans aucun échange avec le véhicule, avec le message **« Non supportée par votre version du proxy »**. Elles sont créées **masquées**, y compris après le passage au fork : **à vous de les afficher** (cochez **Afficher** dans l'onglet **Commandes** de l'équipement) ou de les appeler depuis un scénario. La disponibilité suit l'annonce du proxy (route `capabilities`), relue quand sa version change : après la mise à jour du proxy, les actions deviennent utilisables sans réinstaller le plugin ni recréer l'équipement. Pour ces deux actions, le plugin n'affiche ni le badge **Fonction indisponible**, ni le badge **Rôle insuffisant** : le refus s'affiche au clic.

**Confirmation.** Un clic demande une **confirmation** avant l'envoi, comme pour les autres actions sensibles : voir [Confirmation des actions sensibles](#confirmation-des-actions-sensibles) (case **Confirmer l'action**, scénario sans confirmation, JSON-RPC `confirmAction=1`).

**Vérification avant l'ouverture du coffre arrière.** Pour le coffre arrière, le véhicule traite la commande comme une **bascule** : sur un hayon motorisé déjà ouvert, elle le **refermerait**. Le plugin relit donc d'abord l'état du véhicule (sans le réveiller) et n'envoie la commande que si le coffre arrière est lu **fermé**. Trois refus possibles, aucun envoi, et **Dernière erreur** n'est pas modifiée :

- **« Coffre déjà ouvert ou en mouvement : commande non envoyée »** : le coffre arrière est ouvert, entrouvert, en train de s'ouvrir ou de se fermer ;
- **« État du coffre inconnu : commande non envoyée »** : le véhicule ne donne pas d'état exploitable pour ce coffre ;
- **« État du coffre illisible, commande non envoyée : … »** : la relecture a échoué (proxy injoignable, véhicule hors de portée…), la cause suit le message.

L'état relu est publié dans les informations avant le refus : si le coffre était déjà ouvert, **Coffre arrière** passe à 1. Le **frunk** n'est pas relu : il ne se referme pas à distance, la commande ne peut que l'ouvrir. **Le plugin ne referme jamais un coffre.**

> ⚠️ **Réveil.** Ces commandes **réveillent le véhicule** (via le proxy), et le plugin ne les lance jamais de lui-même : seule une action de votre part (widget ou scénario) les envoie.

**Après la commande.** Aucune valeur n'est supposée : l'état est relu, puis une relecture est programmée comme après toute commande (voir [Relecture après une commande](#relecture-après-une-commande)). **Coffre arrière** ou **Coffre avant (frunk)** passe à 1 quand le véhicule annonce le coffre ouvert, parfois à la relecture suivante.

**Rôle de la clé.** Le rôle **Owner** est supposé nécessaire (à confirmer en usage réel). Avec une clé Charging Manager, le refus du véhicule s'affiche avec le message de rôle insuffisant (voir [Rôle de la clé](#rôle-de-la-clé)).

### État du mode sentinelle

Deux informations disent si le mode sentinelle est actif : **Sentinelle** (`sentry_mode`) vaut **Activée**, **Désactivée** ou **Inconnu**, et **Provenance de la sentinelle** (`sentry_mode_source`) dit d'où vient cette valeur. La commande qui l'active ou la désactive est **Mode sentinelle** (`set_sentry_mode`).

| Provenance | Ce que cela signifie |
|---|---|
| **Réel** | La valeur a été **lue sur le véhicule**. Disponible avec le **proxy du fork en version `2.3.0-tb.2` au minimum** et un véhicule **éveillé** : un véhicule endormi n'est pas lu, l'information garde alors la **dernière valeur lue** (voir [Veille du véhicule et fraîcheur des données](#veille-du-véhicule-et-fraîcheur-des-données)). Un changement fait depuis l'application Tesla ou l'écran du véhicule est vu à la lecture suivante. |
| **Dernier ordre** | Le plugin ne peut pas lire la sentinelle (proxy officiel 2.3.0, ou fork plus ancien) : la valeur est celle du **dernier ordre réussi envoyé par Jeedom**. Un changement fait depuis l'application, l'écran du véhicule ou une **coupure automatique** n'est **pas vu**. |
| **Aucune** | Rien n'a encore été lu ni ordonné : **Sentinelle** vaut **Inconnu** (jamais un faux « Désactivée »). |

**Après un ordre.** Un ordre **réussi** publie tout de suite la valeur ordonnée avec la provenance **Dernier ordre**, même si le proxy sait lire la sentinelle ; à la relecture suivante, la provenance repasse à **Réel**. Pendant la durée de la **relecture après une commande** (30 secondes par défaut, voir [Relecture après une commande](#relecture-après-une-commande)), une lecture réelle qui contredit l'ordre est ignorée : le proxy sert encore l'ancien état. Un ordre **refusé** ou en erreur ne change rien.

**États du véhicule.** Seul `Off` donne **Désactivée**. Les autres états (`Idle`, `Armed`, `Aware`, `Panic`, `Quiet`) donnent **Activée** : `Idle`, la sentinelle au repos, est comptée **Activée** (à confirmer en usage réel). Une valeur inconnue ou absente laisse l'information inchangée.

**Redémarrage de Jeedom.** La dernière valeur connue et sa provenance sont **conservées** et reprises au démarrage, y compris après une coupure d'alimentation.

> **Dans un scénario.** Les libellés **Activée**, **Désactivée**, **Inconnu**, **Réel**, **Dernier ordre** et **Aucune** **suivent la langue de Jeedom** : comparez-les dans la langue courante de votre Jeedom. Pour savoir si la valeur est fiable, testez **Provenance de la sentinelle** (par exemple **Réel**) en plus de **Sentinelle**.

### Alertes d'ouverture prolongée

Le plugin peut vous **prévenir** quand un ouvrant (porte, coffre arrière, frunk, tonneau, trappe de charge) reste ouvert, ou quand le véhicule reste **déverrouillé sans occupant**, plus longtemps que la durée que vous choisissez. Les alertes sont **désactivées par défaut** et se règlent **par véhicule**, dans le bloc **Alertes d'ouverture prolongée** de la page de l'équipement :

| Réglage | Rôle |
|---|---|
| **Ouvrant resté ouvert** : **Activer** | Active l'alerte des ouvrants. |
| **Durée avant alerte (min)** | De 1 à 1440 minutes. **Obligatoire** pour activer l'alerte ; une durée invalide est refusée à l'enregistrement. |
| **Véhicule déverrouillé sans occupant** : **Activer** | Active l'alerte du verrouillage, avec **sa propre durée** (**Durée avant alerte (min)**). |

Les deux alertes sont indépendantes. Une alerte, c'est :

- **un message** dans le centre de messages de Jeedom, qui nomme le véhicule et l'ouvrant (par exemple « Ma Tesla : ouvrant « Coffre avant (frunk) » ouvert depuis plus de 10 min »), **une seule fois par épisode** ; **plusieurs ouvrants ouverts en même temps donnent plusieurs messages**, un par ouvrant ;
- **l'info à 1** : **Alerte ouvrants** (`closures_alert`) tant qu'au moins un ouvrant est resté ouvert au-delà de la durée, **Alerte déverrouillé sans occupant** (`unlocked_alert`) pour le verrouillage. Utilisez-les comme déclencheur d'un scénario pour être notifié par le moyen de votre choix ; elles sont **masquées** et **historisées** : affichez-les si vous le souhaitez.

Quand tout est refermé (ou reverrouillé, ou qu'un occupant est présent), l'info repasse à **0** et une nouvelle ouverture prolongée alertera de nouveau. **Le message reste dans le centre de messages** après la fermeture : Jeedom ne le retire pas, supprimez-le vous-même.

**Précision.** Les alertes sont évaluées **à chaque lecture réussie de l'état du véhicule**, donc à la cadence de rafraîchissement (5 minutes par défaut, voir [Rafraîchissement des informations](#rafraîchissement-des-informations)). La durée se compte depuis la **première lecture qui voit l'anomalie** : l'alerte part **entre la durée choisie et cette durée plus deux intervalles de rafraîchissement** après l'ouverture réelle ; « ouvert depuis plus de 10 min » est donc toujours vrai.

**Jamais d'alerte sur une valeur périmée.** Quand le proxy est injoignable, que le véhicule est hors de portée ou que la lecture échoue, **rien n'est évalué** et la durée ne s'accumule pas. Si l'interruption dépasse **deux intervalles de rafraîchissement plus deux minutes**, le chronomètre **repart de zéro** au retour des lectures ; une alerte déjà émise reste émise, sans nouveau message.

**Trappe de charge.** La trappe ouverte compte comme une anomalie **seulement si le véhicule a été vu débranché** (dernier **État charge** lu : `Disconnected`). Branché, en charge, ou état inconnu : aucune alerte pour la trappe.

**Présence inconnue.** « Déverrouillé sans occupant » n'est évalué que si le véhicule est **déverrouillé** et que l'**Occupant présent** vaut **0** : une présence inconnue ne déclenche rien (voir [Informations](#informations)).

### Position et confidentialité

La position du véhicule est une **donnée personnelle** : elle dit où vous êtes et quand vous n'y êtes pas. Le plugin la protège par défaut, mais quelques précautions restent à votre charge.

**Ce qui est lu, et quand.** La position n'est fournie que par le **proxy du fork** (`2.3.0-tb.2` au minimum) : le proxy officiel 2.3.0 ne la sert pas, et les informations n'existent alors pas (voir [Données étendues : ce qui est disponible](#données-étendues--ce-qui-est-disponible)). Elle est lue au plus **toutes les 15 minutes**, seulement quand le véhicule est **éveillé et à portée Bluetooth** du proxy, jamais en le réveillant. Le proxy étant dans votre garage, la position lue est en pratique celle du domicile. Une position absente, à 0/0, hors plage ou **plus ancienne d'une heure** est ignorée : les informations gardent leur dernière valeur.

**Non visible et non historisée par défaut.** **Latitude** et **Longitude** sont créées **masquées** et **non historisées** : elles n'apparaissent ni sur le widget ni dans un graphique, et rien n'est conservé. Pour les utiliser :

1. Ouvrez l'onglet **Commandes** de l'équipement.
2. Sur **Latitude** et **Longitude**, cochez **Afficher** pour les voir sur le widget, et **Historiser** pour en conserver les valeurs.
3. **Sauvegardez**. Ce choix n'est jamais écrasé ensuite.

Attention : une position historisée est stockée dans la base de Jeedom et dans ses sauvegardes, comme n'importe quel historique. N'historisez que si vous en avez besoin.

**Le domicile et le rayon.** L'information **À la maison** vaut **1** quand le véhicule est à moins de **Rayon (m)** du domicile, **0** au-delà. Le domicile se règle dans l'onglet **Equipement**, section **Position du domicile** (voir [Configuration des équipements](#configuration-des-équipements)) :

| Réglage | Valeur |
|---|---|
| **Latitude** et **Longitude** | Les coordonnées de votre domicile. **Vides tous les deux : la position de Jeedom** (**Réglages > Système > Configuration**, onglet **Général**). Une seule renseignée est refusée. |
| **Rayon (m)** | Entier de **10 à 10000**. Vide : **100 m**. Un GPS imprécis ou un garage en sous-sol peut demander un rayon plus large. |

À l'enregistrement de l'équipement, **À la maison** est recalculée tout de suite à partir de la dernière position lue (si **Latitude** et **Longitude** existent sur l'équipement), sans attendre la lecture suivante.

**Limites de À la maison.** C'est une information binaire qui ne sait pas dire « inconnu » :

- Elle n'est **jamais écrite** tant que le **domicile** (aucune coordonnée renseignée, aucune position dans Jeedom) ou la **position** (jamais lue, ignorée) sont inconnus. **Avant tout calcul, la tuile affiche 0** : elle ne prouve donc pas que le véhicule est parti.
- Elle **ne repasse pas à 0** quand le véhicule part : hors de portée Bluetooth, plus aucune position n'est lue et l'information garde sa **dernière valeur** (1). Elle garde aussi sa valeur si vous effacez le domicile ou si la position devient trop ancienne.
- **Dans un scénario**, testez `== 1` (jamais `== 0` ou « différent de 1 »), et **combinez avec Présence véhicule** : « À la maison vaut 1 **et** Présence véhicule vaut 1 » signifie que le véhicule est chez vous et joignable. **Présence véhicule à 0** signale qu'il n'est plus à portée du proxy, c'est-à-dire en pratique parti.

**Le log `event` de Jeedom.** Le plugin n'écrit **jamais** de coordonnée (véhicule ou domicile) ni de distance dans son propre log, à aucun niveau, même en **Debug**. Mais Jeedom enregistre lui-même chaque nouvelle valeur d'une information dans son log **`event`** (**Analyse > Logs**) : **Latitude** et **Longitude** y apparaissent, **même masquées et non historisées**. Pour vous en protéger, au choix : baissez le niveau du log `event` dans les réglages de logs de Jeedom (**Réglages > Système > Configuration**, onglet **Logs**), ou supprimez les informations **Latitude** et **Longitude** de l'équipement (**À la maison** reste calculée). Le plugin recrée les commandes manquantes à chaque sauvegarde de l'équipement : supprimez-les de nouveau si elles reviennent. Relisez aussi une capture du log avant de la publier sur un forum.

**Le proxy doit rester protégé.** Le proxy officiel n'a **aucune authentification** : n'importe quel appareil de votre réseau local peut lui demander la position du véhicule. Le proxy du fork, seul à servir la position, **peut** exiger un **jeton d'API** (facultatif : réglage **Jeton d'API du proxy** de la configuration du plugin), qui protège aussi la position. Dans tous les cas, gardez le proxy sur un réseau de confiance et n'exposez **jamais** son port sur Internet (voir [Rôle de la clé](#rôle-de-la-clé) et [Configuration du plugin](#configuration-du-plugin)).

### Pourquoi les appels sont séquentiels

Un proxy n'a qu'**un seul adaptateur Bluetooth** et une seule file d'échanges avec les véhicules : deux demandes envoyées en même temps se gêneraient. Le plugin fait donc passer les échanges d'un même proxy **l'un après l'autre**, tous véhicules confondus (lectures du cycle, commandes, **Rafraîchir**, **Vérifier l'appairage**).

- **Un même proxy** : un seul échange à la fois. Si une commande est en cours, la lecture du cycle s'efface et reprend au passage suivant (la minute d'après) ; une commande ou un **Rafraîchir** attend son tour. Quand l'attente dure trop longtemps (environ 2 minutes), le plugin renonce et affiche **Proxy occupé** : relancez dans un instant (voir [Dépannage](#dépannage)).
- **Des proxys différents** : ils sont lus **en parallèle** et ne s'attendent jamais. Un proxy lent ou arrêté ne retarde que ses propres véhicules ; le cycle dure autant que son proxy le plus lent.
- **Au pire cas** (proxy très lent, chaque lecture allant à son délai maximal), un cycle de 4 minutes lit **3 véhicules par proxy** au plus ; au-delà, les derniers peuvent ne pas être lus à ce cycle. En pratique, une lecture dure quelques secondes.

### Récapitulatif des réglages de cadence et de réveil

Tous ces réglages se trouvent dans l'onglet **Equipement** de chaque véhicule (voir [Configuration des équipements](#configuration-des-équipements)). Les défauts s'appliquent aussi aux véhicules existants après la mise à jour.

| Réglage | Défaut | Valeurs possibles | Effet sur la batterie du véhicule |
|---|---|---|---|
| **Intervalle de rafraîchissement** | 5 minutes | 1, 2, 5, 10, 15 ou 30 minutes | Plus il est long, moins le véhicule est sollicité. À lui seul, il ne réveille jamais le véhicule. |
| **Intervalle pendant la charge** | Désactivé | Désactivé, ou 1, 2, 5, 10 ou 15 minutes | Sans effet hors charge ; pendant la charge le véhicule est de toute façon éveillé. |
| **Laisser le véhicule s'endormir** | Coché | Coché ou décoché | Coché : le plugin cesse de lire les données quand le véhicule est inactif, pour qu'il puisse s'endormir. |
| **Lectures inchangées avant la fenêtre** | 3 | 1, 2, 3, 4, 5, 10 ou 15 | Plus il est bas, plus la fenêtre s'ouvre vite. |
| **Durée de la fenêtre** | 30 minutes | 15, 20, 30, 45 minutes, 1 h, 1 h 30 ou 2 h | Plus elle est longue, plus le véhicule a de temps pour s'endormir, mais plus les données restent figées. |
| **Délai de relecture après commande** | 30 secondes | 30 secondes, 45 secondes, 1 minute, 1 minute 30 ou 2 minutes | Une lecture par commande réussie, sans réveil. |
| **Lire aussi la climatisation** | Oui | Oui, ou Non (charge seule) | « Charge seule » raccourcit la requête de données (gain à mesurer sur votre installation). |
| **Rafraîchir (avec réveil)** (commande `refresh_wakeup`) | | Action, à lancer à la main ou depuis un scénario | **Réveille** le véhicule à chaque exécution. |
| **Âge des données (min)** (information `data_age`) | | Minutes écoulées depuis la dernière lecture réussie des données ; **99999** = aucune lecture connue (ou plus de 69 jours) | Aucun : calcul local, le proxy n'est pas interrogé. |

La **durée de la fenêtre** n'a d'effet que si elle dépasse l'intervalle de rafraîchissement. Détail de chaque réglage : [Rafraîchissement des informations](#rafraîchissement-des-informations), [Lecture accélérée pendant la charge](#lecture-accélérée-pendant-la-charge), [Laisser le véhicule s'endormir](#laisser-le-véhicule-sendormir) et [Relecture après une commande](#relecture-après-une-commande).

### Recommandations par usage

Les valeurs ci-dessous sont des **points de départ indicatifs, à ajuster d'après vos propres mesures** : l'effet réel sur la batterie dépend du modèle, du logiciel du véhicule et de son environnement, et le plugin ne garantit pas que le véhicule s'endorme. Aucun pourcentage de batterie n'est annoncé ici faute de mesure fiable ; le tableau chiffre ce que le plugin fait réellement : le nombre de lectures de données par heure et le temps laissé au véhicule pour s'endormir.

| Usage | Intervalle de rafraîchissement | Intervalle pendant la charge | Fenêtre d'endormissement | Lire aussi la climatisation | Lectures de données (véhicule éveillé, inactif, hors charge) |
|---|---|---|---|---|---|
| **Supervision simple** (présence, verrouillage, niveau de batterie) | 10 à 15 minutes | Désactivé | Cochée, 3 lectures inchangées, 30 minutes (défauts) | Oui | 4 à 6 par heure au plus ; **aucune** pendant les 30 minutes d'une fenêtre ouverte |
| **Pilotage solaire** (ajuster le courant selon la production) | 5 minutes | **1 minute** | Cochée, 3 lectures inchangées, 30 minutes (défauts) | Non (charge seule), si vous n'utilisez pas la climatisation | 12 par heure hors charge ; **60 par heure pendant la charge** (la fenêtre ne s'ouvre jamais en charge) |
| **Suivi rapproché** (charge ou préconditionnement surveillés de près) | 1 à 2 minutes | 1 minute | Cochée, 3 lectures inchangées, 30 minutes | Oui | 30 à 60 par heure : le véhicule ne dort pas tant que la fenêtre n'est pas ouverte ; réservez ce profil à une période précise |
| **Plusieurs véhicules sur un proxy** (3 au plus) | 10 à 15 minutes | Désactivé, sauf pour le véhicule piloté | Cochée | Oui | Les lectures d'un même proxy passent l'une après l'autre : gardez des intervalles longs |

Pour le pilotage solaire, gardez aussi le **Délai de relecture après commande** à 30 secondes et espacez les ordres de **Courant de charge** de votre scénario (une relecture est lancée après chaque commande réussie).

**Mesurer l'effet chez vous.** Relevez le niveau de **Charge batterie** le soir et le matin, véhicule garé et sans occupant, pendant quelques nuits avec **Laisser le véhicule s'endormir** coché, puis quelques nuits décoché. Historisez **Véhicule réveillé** pour voir combien de temps le véhicule est resté éveillé : comparez les deux séries avant d'ajuster l'intervalle ou la durée de la fenêtre.

## Commandes

Les tableaux ci-dessous donnent, pour chaque commande, son **identifiant** (`logicalId`, stable : c'est lui que les scénarios retrouvent), son type et son sous-type, et son unité. Les libellés sont ceux d'un **nouvel équipement** ; un équipement migré depuis la 0.x garde ses anciens noms (voir [Mise à jour depuis la version 0.x](#mise-à-jour-depuis-la-version-0x)).

### Charge avancée : ce qui est disponible

Récapitulatif de ce qu'ajoute la charge avancée. Les informations sont créées **masquées** (affichez-les depuis l'onglet **Commandes**) ; le détail de chacune est dans les tableaux [Informations](#informations) et [Actions](#actions).

| Libellé | Identifiant | Unité | Rôle | Détail |
|---|---|---|---|---|
| Limite de charge minimale | `charge_limit_soc_min` | % | Plus basse limite acceptée par le véhicule ; règle le **Min** du curseur **Limite de charge** | [Bornes suivies du véhicule](#exécution-des-commandes) |
| Limite de charge maximale | `charge_limit_soc_max` | % | Plus haute limite acceptée ; règle le **Max** du même curseur | [Bornes suivies du véhicule](#exécution-des-commandes) |
| Courant de charge maximal | `charge_current_request_max` | A | Courant maximal annoncé par le véhicule ; règle le **Max** du curseur **Courant de charge** | [Bornes suivies du véhicule](#exécution-des-commandes) |
| État de charge (traduit) | `charging_state_label` | | État de charge en français, pour l'affichage | [Informations](#informations) |
| Autonomie nominale | `battery_range` | km | Autonomie nominale | [Informations](#informations) |
| Autonomie estimée | `est_battery_range` | km | Autonomie d'après votre conduite récente | [Informations](#informations) |
| Niveau de batterie (brut) | `battery_level` | % | Niveau de batterie tel que le véhicule le rapporte | [Informations](#informations) |
| Puissance de charge | `charger_power` | kW | Puissance délivrée au véhicule | [Informations](#informations) |
| Courant de charge réel | `charger_actual_current` | A | Courant réellement délivré | [Informations](#informations) |
| Phases de charge | `charger_phases` | | Nombre de phases utilisées | [Informations](#informations) |
| Énergie ajoutée | `charge_energy_added` | kWh | Énergie ajoutée pendant la session en cours (ou la dernière) | [Informations](#informations) |
| Câble de charge | `conn_charge_cable` | | Type de câble connecté | [Informations](#informations) |
| Charge rapide | `fast_charger_present` | | 1 si branché sur une borne de charge rapide | [Informations](#informations) |
| Énergie cumulée de charge | `charge_energy_total` | kWh | Index qui ne fait que croître, pour le suivi d'énergie | [Compteurs d'énergie de charge](#compteurs-dénergie-de-charge) |
| Heure de charge programmée | `scheduled_charging_start_time` | | Heure de début de la charge différée (`HH:MM`) | [Programmations lues dans le véhicule](#informations) |
| Fin des heures creuses | `off_peak_hours_end_time` | | Fin des heures creuses du véhicule (`HH:MM`) | [Programmations lues dans le véhicule](#informations) |
| Préconditionnement planifié | `scheduled_preconditioning_time` | | Heure de départ visée par le préconditionnement (`HH:MM`) | [Programmations lues dans le véhicule](#informations) |
| Ajuster selon le surplus | `adjust_surplus` | W | Action : reçoit la puissance disponible et décide d'envoyer ou non une commande | [Pilotage selon le surplus](#pilotage-selon-le-surplus) |
| Ajouter une programmation de charge | `add_charge_schedule` | | Action : crée ou remplace la programmation gérée par Jeedom (proxy du fork) | [Programmer la charge](#programmer-la-charge) |
| Supprimer la programmation de charge | `remove_charge_schedule` | | Action : supprime cette programmation (proxy du fork) | [Programmer la charge](#programmer-la-charge) |

Les actions de la charge avancée sont masquées aussi. Deux fonctions se règlent dans l'équipement plutôt que par une commande :

| Réglages d'équipement | Fonction | Détail |
|---|---|---|
| **Tension du réseau**, **Phases**, **Pas d'ajustement**, **Hystérésis**, **Intervalle minimal entre commandes**, **Courant minimal de démarrage**, **Seuil d'arrêt**, **Durée de maintien avant arrêt** | Pilotage selon le surplus (défauts : 230 V, monophasé, 1 A, 2 A, 120 s, 6 A, 5 A, 300 s) | [Configuration des équipements](#configuration-des-équipements) et [Pilotage selon le surplus](#pilotage-selon-le-surplus) |
| **Pilotage de la charge**, **Début de plage**, **Fin de plage**, **SoC cible (%)**, **Arrêter en fin de plage** | Charge aux heures creuses (désactivée par défaut) | [Charge aux heures creuses](#charge-aux-heures-creuses) |

### Climat et confort : ce qui est disponible

Récapitulatif de ce que permet la climatisation et le confort. Le proxy officiel 2.3.0 lit tout, mais ne sait pas régler la consigne de température, les sièges, le volant, le dégivrage maximal ni le maintien de climat : ces commandes exigent le **proxy du fork** (versions `2.3.0-tb.N`) et sont créées **masquées**. Le rôle de clé **Owner** est **supposé** nécessaire pour les actions (non confirmé en usage réel : « à confirmer »).

| Fonction | Identifiant | Disponibilité | Rôle de clé | Effet sur le véhicule | Détail |
|---|---|---|---|---|---|
| Informations de climatisation (de **Climatisation automatique** à **Chauffage batterie**, dont **Maintien de climat (chien, camp)**) | `is_auto_conditioning_on`… `battery_heater` | Proxy officiel 2.3.0 | Charging Manager suffit (lecture) | Lecture seule, aucun réveil : elles gardent leur dernière valeur tant que le véhicule dort. Créées masquées | [Informations](#informations) |
| Consigne conducteur, Consigne passager | `set_driver_temp`, `set_passenger_temp` | Proxy du fork, `2.3.0-tb.1` au minimum | Owner supposé | Règle la température demandée ; les deux côtés partent ensemble ; le proxy réveille le véhicule | [Régler la consigne de température](#régler-la-consigne-de-température) |
| Chauffage des cinq sièges, chauffage du volant | `set_seat_heater_left`, `set_seat_heater_right`, `set_seat_heater_rear_left`, `set_seat_heater_rear_right`, `set_seat_heater_rear_center`, `set_steering_wheel_heater` | Proxy du fork, `2.3.0-tb.2` au minimum | Owner supposé | Chauffe le siège ou le volant ; demande en principe la climatisation en marche ; le proxy réveille le véhicule | [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant) |
| Dégivrage maximal | `set_preconditioning_max` | Proxy du fork, `2.3.0-tb.1` au minimum | Owner supposé | **Réveille** le véhicule et **consomme de la batterie** tant qu'il fonctionne ; ne s'arrête pas tout seul | [Dégivrage maximal](#dégivrage-maximal) |
| Mode de maintien de climat (maintien, chien, camp) | `set_climate_keeper_mode` | Proxy du fork, `2.3.0-tb.1` au minimum | Owner supposé | **Réveille** le véhicule et **consomme de la batterie sur une longue durée** ; ne s'arrête pas tout seul | [Mode chien, camp et maintien de climat](#mode-chien-camp-et-maintien-de-climat) |
| Démarrer le climatiseur, Arrêter le climatiseur | `auto_conditioning_start`, `auto_conditioning_stop` | Proxy officiel 2.3.0 | Owner supposé (refus probable avec Charging Manager) | Démarre ou arrête le préconditionnement ; le démarrage réveille le véhicule et consomme de la batterie | [Actions](#actions) |
| Préconditionnement planifié par Jeedom (réglage de l'équipement) | Aucun : section **Préconditionnement planifié par Jeedom** | Proxy officiel 2.3.0 | Owner supposé (un seul essai par départ avec Charging Manager) | Jeedom démarre la climatisation avant l'heure de départ puis l'arrête ; le démarrage réveille le véhicule et consomme de la batterie | [Préconditionnement planifié par Jeedom](#préconditionnement-planifié-par-jeedom) |

> ⚠️ **Batterie.** Le dégivrage maximal, le maintien de climat et la climatisation démarrée à l'avance **réveillent le véhicule** et **puisent dans sa batterie**. Aucune consommation chiffrée n'est annoncée ici faute de mesure fiable. Le **mode chien** ne remplace pas une surveillance de la température de l'habitacle pour un animal.

**Pourquoi certaines commandes sont refusées ou masquées.** Le proxy officiel 2.3.0 n'a pas les commandes de consigne, de sièges, de volant, de dégivrage maximal ni de maintien de climat : le fork les ajoute et les **annonce** par sa route `capabilities`. Tant que le proxy n'annonce pas la commande, le plugin la refuse sur-le-champ avec **« Non supportée par votre version du proxy »**, sans rien envoyer au véhicule. Ces commandes sont créées **masquées**, y compris après le passage au fork : cochez **Afficher** dans l'onglet **Commandes**, ou appelez-les depuis un scénario. Après le passage au fork, **aucune réinstallation du plugin** n'est nécessaire : la disponibilité est relue quand la version du proxy change. Si le véhicule refuse ensuite la commande faute de droits, il faut une clé **Owner** : voir [Rôle de la clé](#rôle-de-la-clé) et la procédure d'appairage [Générer la clé et l'appairer avec le véhicule](installation-proxy.md#8-générer-la-clé-et-lappairer-avec-le-véhicule). Les symptômes sans message sont décrits dans [Climat et confort : symptômes sans message](#climat-et-confort--symptômes-sans-message).

### Ouvrants et sécurité : ce qui est disponible

Récapitulatif des ouvrants, de la présence, du verrouillage, de la sentinelle et des alertes. Les lectures marchent avec le **proxy officiel 2.3.0** et une clé **Charging Manager**. Les commandes d'ouverture des coffres exigent le **proxy du fork** (versions `2.3.0-tb.N`) et sont créées **masquées**. Le rôle de clé **Owner** est nécessaire pour verrouiller, déverrouiller et piloter la sentinelle, et **supposé** nécessaire pour les coffres (non confirmé en usage réel : « à confirmer »).

| Fonction | Identifiant | Disponibilité | Rôle de clé | Confirmation demandée | Détail |
|---|---|---|---|---|---|
| Les huit ouvrants (quatre portes, **Coffre arrière**, **Coffre avant (frunk)**, **Trappe de charge (ouvrant)**, **Tonneau**) | `door_front_driver`, `door_front_passenger`, `door_rear_driver`, `door_rear_passenger`, `trunk_rear`, `trunk_front`, `charge_port_closure`, `tonneau` | Proxy officiel 2.3.0 | Charging Manager suffit (lecture) | Sans objet | [Informations](#informations) |
| **Occupant présent** | `user_present` | Proxy officiel 2.3.0 | Charging Manager suffit (lecture) | Sans objet | [Informations](#informations) |
| **Verrouillage du véhicule**, **État de verrouillage détaillé** | `vehicule_lock`, `lock_state` | Proxy officiel 2.3.0 | Charging Manager suffit (lecture) | Sans objet | [Informations](#informations) |
| **Sentinelle**, **Provenance de la sentinelle** | `sentry_mode`, `sentry_mode_source` | Proxy officiel 2.3.0 : valeur du **dernier ordre**. Proxy du fork `2.3.0-tb.2` au minimum : valeur **réelle** (véhicule éveillé) | Charging Manager suffit (lecture) | Sans objet | [État du mode sentinelle](#état-du-mode-sentinelle) |
| **Alerte ouvrants**, **Alerte déverrouillé sans occupant** et les réglages **Alertes d'ouverture prolongée** | `closures_alert`, `unlocked_alert` | Proxy officiel 2.3.0 (réglages dans l'équipement, alertes désactivées par défaut) | Charging Manager suffit (lecture) | Sans objet | [Alertes d'ouverture prolongée](#alertes-douverture-prolongée) |
| Verrouiller les portes, Déverrouiller les portes | `door_lock`, `door_unlock` | Proxy officiel 2.3.0 | **Owner** (refusé avec Charging Manager) | Déverrouiller : **oui** | [Actions](#actions) |
| Ouvrir la trappe de charge, Fermer la trappe de charge | `charge_port_door_open`, `charge_port_door_close` | Proxy officiel 2.3.0 | Non confirmé (voir [Rôle de la clé](#rôle-de-la-clé)) | Ouvrir : **oui** | [Actions](#actions) |
| Mode sentinelle | `set_sentry_mode` | Proxy officiel 2.3.0 | **Owner** (refusé avec Charging Manager) | **Oui** | [État du mode sentinelle](#état-du-mode-sentinelle) |
| Ouvrir le coffre arrière, Ouvrir le frunk | `open_trunk_rear`, `open_trunk_front` | Proxy du fork, `2.3.0-tb.2` au minimum | Owner supposé | **Oui** | [Ouvrir le coffre arrière et le frunk](#ouvrir-le-coffre-arrière-et-le-frunk) |

Les actions qui demandent une confirmation sont décrites dans [Confirmation des actions sensibles](#confirmation-des-actions-sensibles). La différence **Réel** / **Dernier ordre** de la sentinelle est expliquée dans [État du mode sentinelle](#état-du-mode-sentinelle) : testez **Provenance de la sentinelle** avant de vous fier à **Sentinelle**.

> **IMPORTANT : réseau de confiance.** Le proxy n'a **ni authentification ni chiffrement (TLS)** par défaut ; le fork peut exiger un jeton d'API, facultatif. Avec une clé Owner, toute machine de votre réseau local peut déverrouiller le véhicule ou ouvrir un coffre sans passer par Jeedom, et la confirmation de Jeedom ne la retient pas. Gardez le proxy sur un réseau de confiance, idéalement isolé, et n'exposez **jamais** son port sur Internet (voir [Rôle de la clé](#rôle-de-la-clé)).

**Pourquoi les commandes de coffre sont refusées ou masquées.** Le proxy officiel 2.3.0 n'a pas la commande qui actionne un coffre : le fork l'ajoute et l'**annonce** par sa route `capabilities`. Tant que le proxy ne l'annonce pas, le plugin refuse **Ouvrir le coffre arrière** et **Ouvrir le frunk** sur-le-champ avec **« Non supportée par votre version du proxy »**, sans rien envoyer au véhicule. Pour les activer : installez ou mettez à jour le proxy du fork (`2.3.0-tb.2` au minimum), sans réinstaller le plugin ni recréer l'équipement (la disponibilité est relue quand la version du proxy change). Les deux commandes sont créées **masquées**, y compris après le passage au fork : cochez **Afficher** dans l'onglet **Commandes**, ou appelez-les depuis un scénario. Si le véhicule refuse ensuite faute de droits, il faut une clé **Owner**. Les symptômes sans message sont décrits dans [Ouvrants et sécurité : symptômes sans message](#ouvrants-et-sécurité--symptômes-sans-message).

### Données étendues : ce qui est disponible

Récapitulatif des informations de la tranche « données étendues » : modèle, kilométrage et conduite, pression des pneus, mise à jour logicielle et position. Le détail de chaque information (libellé, identifiant, visibilité, historisation) est dans le tableau [Informations](#informations). Toutes sont des **lectures seules**, sans réveil du véhicule.

| Donnée | Identifiants | Unité | Prérequis du proxy | Cadence de lecture |
|---|---|---|---|---|
| Modèle et année | `model`, `model_year` | | **Aucun** : décodés de la VIN, sans interroger le proxy | À l'enregistrement de l'équipement, à la mise à jour du plugin et au démarrage de Jeedom |
| Kilométrage et conduite | `odometer`, `shift_state`, `speed`, `power` | km, km/h, kW | Le proxy doit **annoncer** `drive_state` | À chaque lecture des données (véhicule éveillé) |
| Pression des pneus | `tpms_pressure_fl`, `_fr`, `_rl`, `_rr` | bar | Le proxy doit **annoncer** `tire_pressure` | Au plus toutes les **15 minutes**, véhicule éveillé |
| Mise à jour logicielle | `software_update_status`, `software_update_version`, `software_update_progress` | % (progression) | Le proxy doit **annoncer** `software_update` | Au plus toutes les **15 minutes**, véhicule éveillé |
| Position | `latitude`, `longitude`, `at_home` | ° | Le proxy doit **annoncer** `location_data` | Au plus toutes les **15 minutes**, véhicule éveillé |

**Quel proxy ?** Un proxy « annonce » une donnée quand sa route `capabilities` la liste (`http://<ip_du_proxy>:<port>/api/proxy/1/capabilities`, voir [Rôle de la clé](#rôle-de-la-clé)). Le **proxy du fork** `2.3.0-tb.2` au minimum annonce ces quatre catégories ; le **proxy officiel 2.3.0 ne les sert pas**. Pour le kilométrage, la fonction est fusionnée dans le projet de wimaha mais sans version publiée à la date de cette documentation : elle ne sera lue qu'avec une version qui l'**annonce**. Le plugin ne se fie jamais à un numéro de version, seulement à cette annonce : vérifiez **Version du proxy** et, au besoin, l'adresse ci-dessus.

**Pourquoi une donnée étendue est absente.** Sur un proxy qui n'annonce pas une catégorie, les informations correspondantes **ne sont pas créées** : elles n'apparaissent pas dans l'onglet **Commandes** (il n'existe pas de valeur « Non supporté » affichée). Seuls **Modèle** et **Année modèle** sont toujours présentes. Pour les obtenir :

1. Vérifiez **Version du proxy** de l'équipement, puis installez ou mettez à jour le **proxy du fork** (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)).
2. Attendez le cycle de rafraîchissement suivant (une minute au plus) : à la **re-détection**, quand la version du proxy change, le plugin relit ce que le proxy annonce et **crée seul** les informations devenues disponibles. Aucune réinstallation du plugin ni recréation de l'équipement n'est nécessaire. Un **Sauvegarder** sur l'équipement fait aussi créer les informations manquantes si le proxy les annonce.
3. Vérifiez qu'elles se remplissent : elles restent vides jusqu'à la première lecture, **véhicule éveillé** (lancez **Rafraîchir (avec réveil)** pour la provoquer). Les pressions, la mise à jour et la position attendent en plus que 15 minutes se soient écoulées depuis la tentative précédente.

Si un proxy **annonce** une catégorie mais que le véhicule ou le proxy la **refuse** (**« Fonction non supportée par ce proxy — … »**), le plugin cesse de la demander jusqu'au prochain changement de version du proxy : voir [Données étendues : symptômes sans message](#données-étendues--symptômes-sans-message).

**Valeurs et unités.**

- **Kilométrage** : converti de miles en kilomètres, au dixième. Un compteur nul ou aberrant est ignoré. Historisé par défaut.
- **Rapport** : `P`, `R`, `N` ou `D`. **Vide** veut dire « non communiqué » : le plugin écrit alors une chaîne vide, un test `== "D"` ne reste donc pas vrai après l'arrêt.
- **Vitesse** et **Puissance** : le plugin suppose une vitesse en mph (convertie en km/h) et une puissance en kW, négative admise. Ces deux unités ne sont pas confirmées par une documentation du véhicule : comparez avec l'écran de votre véhicule avant de vous en servir. Créées masquées, car le proxy étant au garage, elles ne valent presque jamais autre chose que 0 ou la puissance de charge.
- **Pression des pneus** : en **bar**, sans conversion. Une valeur nulle, négative ou supérieure à 10 bar est ignorée (l'information garde sa dernière valeur ou reste vide). Les pneus ne sont lus que sur un véhicule éveillé : les dernières valeurs restent affichées quand il dort.
- **Mise à jour** : quatre libellés, **Aucune**, **Disponible** (aussi une installation programmée), **Téléchargement en cours** (aussi en attente du Wi-Fi) et **Installation en cours**. **Version proposée** vaut **Aucune** hors mise à jour, et **Inconnue** quand une mise à jour est active sans version rapportée. **Progression** vaut 0 hors téléchargement et installation. Ces libellés suivent la langue de Jeedom : dans un scénario, testez de préférence **Progression** ou comparez dans la langue courante.
- **Modèle** et **Année modèle** : décodés de la VIN (modèle : 4e caractère ; année : 10e caractère, de 2008 à 2037). Une VIN vide, non Tesla ou non décodable donne **Inconnu**. Elles sont **visibles** et **non historisées**.
- **Position** : voir [Position et confidentialité](#position-et-confidentialité).

Les données étendues sont lues avec les données de charge : elles suivent donc la **fenêtre d'endormissement** (aucune lecture pendant la fenêtre, voir [Laisser le véhicule s'endormir](#laisser-le-véhicule-sendormir)) et gardent leur dernière valeur tant que le véhicule dort. Un refus d'une seule catégorie n'empêche pas les autres lectures, et ne modifie jamais **Dernière erreur** pour les pressions, la mise à jour et la position.

### Informations

« H » : historisée par défaut. « V » : visible par défaut sur le widget. Vous pouvez changer ces deux réglages dans l'onglet **Commandes**.

| Libellé | Identifiant | Type / sous-type | Unité | H | V | Description |
|---|---|---|---|---|---|---|
| Présence véhicule | `isPresent` | info / binaire | | oui | oui | 1 si le proxy joint le véhicule en Bluetooth, 0 s'il est hors de portée |
| Véhicule réveillé | `vehicule_isAwake` | info / binaire | | oui | oui | 1 si le véhicule est éveillé, 0 s'il dort ou si son état de veille est inconnu |
| Verrouillage du véhicule | `vehicule_lock` | info / binaire | | oui | oui | 1 si le véhicule est verrouillé, y compris de l'intérieur, 0 s'il est déverrouillé, même partiellement |
| Porte avant conducteur | `door_front_driver` | info / binaire | | oui | oui | 1 si la porte est ouverte, y compris entrouverte, en cours d'ouverture ou de fermeture, 0 si elle est fermée |
| Porte avant passager | `door_front_passenger` | info / binaire | | oui | oui | Même règle que la porte avant conducteur |
| Porte arrière conducteur | `door_rear_driver` | info / binaire | | oui | oui | Même règle que la porte avant conducteur |
| Porte arrière passager | `door_rear_passenger` | info / binaire | | oui | oui | Même règle que la porte avant conducteur |
| Coffre arrière | `trunk_rear` | info / binaire | | oui | oui | 1 si le coffre est ouvert (y compris entrouvert ou en mouvement), 0 s'il est fermé |
| Coffre avant (frunk) | `trunk_front` | info / binaire | | oui | oui | 1 si le coffre avant est ouvert (y compris entrouvert ou en mouvement), 0 s'il est fermé |
| Trappe de charge (ouvrant) | `charge_port_closure` | info / binaire | | oui | oui | 1 si la trappe de charge est ouverte (y compris entrouverte ou en mouvement), 0 si elle est fermée. Lue même véhicule endormi, contrairement à **Trappe de charge ouverte** |
| Tonneau | `tonneau` | info / binaire | | oui | oui | 1 si le tonneau (Cybertruck) est ouvert, 0 s'il est fermé ; 0 aussi sur un véhicule qui n'en a pas |
| Occupant présent | `user_present` | info / binaire | | oui | oui | 1 si le véhicule détecte une personne à bord, 0 sinon ; état inconnu = dernière valeur |
| État de verrouillage détaillé | `lock_state` | info / texte | | non | oui | Libellé du verrouillage : **Déverrouillé**, **Verrouillé**, **Verrouillé de l'intérieur** ou **Déverrouillage sélectif** ; une valeur inconnue est affichée telle quelle. Il suit la langue de Jeedom : dans un scénario, testez **Verrouillage du véhicule** et **Occupant présent**, un libellé comparé dépend de la langue |
| Sentinelle | `sentry_mode` | info / texte | | non | oui | **Activée**, **Désactivée** ou **Inconnu** (aucune lecture ni ordre connus). Voir [État du mode sentinelle](#état-du-mode-sentinelle). Elle suit la langue de Jeedom : dans un scénario, comparez dans la langue courante de Jeedom, et testez **Provenance de la sentinelle** pour savoir d'où vient la valeur |
| Provenance de la sentinelle | `sentry_mode_source` | info / texte | | non | oui | **Réel** (lue sur le véhicule), **Dernier ordre** (déduite de la dernière commande réussie du plugin) ou **Aucune** (rien n'a encore été lu ni ordonné). Même règle de langue que **Sentinelle** |
| Alerte ouvrants | `closures_alert` | info / binaire | | oui | non | 1 tant qu'un ouvrant est resté ouvert plus longtemps que la durée réglée (alerte activée seulement), 0 sinon. Voir [Alertes d'ouverture prolongée](#alertes-douverture-prolongée). |
| Alerte déverrouillé sans occupant | `unlocked_alert` | info / binaire | | oui | non | 1 tant que le véhicule est resté déverrouillé sans occupant plus longtemps que la durée réglée (alerte activée seulement), 0 sinon. Voir [Alertes d'ouverture prolongée](#alertes-douverture-prolongée). |
| État charge | `charging_state` | info / texte | | non | oui | État de la charge renvoyé par le véhicule, sans traduction : `Charging`, `Disconnected`, `Complete`, `Stopped`, `Starting`, `NoPower`, `Calibrating` ou `Unknown`. C'est cette valeur qu'il faut tester dans un scénario |
| État de charge (traduit) | `charging_state_label` | info / texte | | non | non | L'état de charge en français (**En charge**, **Déconnecté**, **Terminée**, **Arrêtée**, **Démarrage**, **Pas de courant**, **Étalonnage**, **Inconnu**), pour l'affichage. Un état que le plugin ne connaît pas est affiché tel que le véhicule l'envoie. Il suit la langue de Jeedom : dans un scénario, testez **État charge**, jamais ce libellé |
| Limite charge | `charge_limit_soc` | info / numérique | % | oui | oui | Limite de charge configurée |
| Limite de charge minimale | `charge_limit_soc_min` | info / numérique | % | non | non | Limite de charge la plus basse que le véhicule accepte (sert de **Min** au curseur **Limite de charge**) |
| Limite de charge maximale | `charge_limit_soc_max` | info / numérique | % | non | non | Limite de charge la plus haute que le véhicule accepte (sert de **Max** au curseur **Limite de charge**) |
| Charge batterie | `usable_battery_level` | info / numérique | % | oui | oui | Niveau de batterie utilisable |
| Niveau de batterie (brut) | `battery_level` | info / numérique | % | non | non | Niveau de batterie tel que le véhicule le rapporte, de 0 à 100 %. Il peut différer de quelques points de **Charge batterie** (niveau utilisable) |
| Autonomie | `ideal_battery_range` | info / numérique | km | oui | non | Autonomie dite idéale, convertie en kilomètres (le véhicule la renvoie en miles) |
| Autonomie nominale | `battery_range` | info / numérique | km | non | non | Autonomie nominale, convertie en kilomètres. Elle est généralement identique à l'autonomie dite idéale |
| Autonomie estimée | `est_battery_range` | info / numérique | km | non | non | Autonomie estimée d'après votre conduite récente, convertie en kilomètres |
| Tension chargeur | `charger_voltage` | info / numérique | V | non | non | Tension délivrée par la borne |
| Vitesse de charge | `charge_rate` | info / numérique | km/h | non | non | Autonomie récupérée par heure de charge, convertie en km/h (le véhicule la renvoie en miles par heure) |
| Puissance de charge | `charger_power` | info / numérique | kW | non | non | Puissance délivrée au véhicule, en kilowatts (le véhicule la renvoie en général sous forme de valeur entière) |
| Courant de charge réel | `charger_actual_current` | info / numérique | A | non | non | Courant réellement délivré, à ne pas confondre avec le courant configuré (**Courant de charge (A)**) |
| Phases de charge | `charger_phases` | info / numérique | | non | non | Nombre de phases utilisées par la charge ; généralement 0 quand le véhicule ne charge pas |
| Énergie ajoutée | `charge_energy_added` | info / numérique | kWh | non | non | Énergie ajoutée à la batterie pendant la session de charge en cours (ou la dernière) ; le véhicule la remet à zéro à chaque nouvelle session, une valeur négative est ignorée |
| Énergie cumulée de charge | `charge_energy_total` | info / numérique | kWh | oui | non | Compteur qui ne fait que croître : somme des énergies de session, calculée par le plugin (voir [Compteurs d'énergie de charge](#compteurs-dénergie-de-charge)) |
| Courant de charge (A) | `charge_amps` | info / numérique | A | oui | oui | Courant de charge configuré |
| Courant demande charge | `charge_current_request` | info / numérique | A | oui | oui | Courant demandé par le véhicule |
| Courant de charge maximal | `charge_current_request_max` | info / numérique | A | non | non | Courant maximal que le véhicule annonce pouvoir demander à la borne (sert de **Max** au curseur **Courant de charge**) |
| Temps de charge | `minutes_to_full_charge` | info / texte | | non | oui | Temps restant avant la fin de la charge, au format `HHhMM` |
| Temps de charge restant | `charge_minutes_remaining` | info / numérique | min | non | non | Le même temps restant, en minutes (utilisable dans un scénario ou un graphique) |
| Trappe de charge ouverte | `charge_port_door_state` | info / binaire | | non | non | 1 si la trappe de charge est ouverte, 0 si elle est fermée |
| Verrouillage trappe charge | `charge_port_latch` | info / texte | | non | non | État du verrou du câble de charge, tel que renvoyé par le véhicule |
| Câble de charge | `conn_charge_cable` | info / texte | | non | non | Type de câble connecté, tel que renvoyé par le véhicule, par exemple `IEC` (Type 2, Europe), `SAE` (Amérique du Nord), `GB_AC` ou `GB_DC` (Chine) ; `SNA` quand aucun câble n'est détecté |
| Charge rapide | `fast_charger_present` | info / binaire | | non | non | 1 si le véhicule est branché sur une borne de charge rapide |
| Mode charge programmée | `scheduled_charging_mode` | info / texte | | non | non | Mode de charge programmée, tel que renvoyé par le véhicule : `ScheduledChargingModeOff` (aucune programmation), `ScheduledChargingModeStartAt` (charge différée) ou `ScheduledChargingModeDepartBy` (départ programmé) |
| Heure départ programmée | `scheduled_departure_time` | info / texte | | non | non | Heure de départ programmée au format `HH:MM` (heure du véhicule) ; vide si aucun départ n'est programmé |
| Heure de charge programmée | `scheduled_charging_start_time` | info / texte | | non | non | Heure de début de la charge différée au format `HH:MM` (heure de Jeedom) ; vide hors mode charge différée. Masquée par défaut |
| Fin des heures creuses | `off_peak_hours_end_time` | info / texte | | non | non | Heure de fin des heures creuses au format `HH:MM` ; renseignée en mode départ programmé seulement, vide sinon ou quand le véhicule indique minuit. Masquée par défaut |
| Préconditionnement planifié | `scheduled_preconditioning_time` | info / texte | | non | non | Heure de départ visée par le préconditionnement, au format `HH:MM` ; renseignée en mode départ programmé quand le préconditionnement est activé, vide sinon. Masquée par défaut |
| Température intérieure | `inside_temp` | info / numérique | °C | oui | oui | Température dans l'habitacle, au dixième de degré |
| Température extérieure | `outside_temp` | info / numérique | °C | oui | oui | Température extérieure, au dixième de degré |
| Température conducteur | `driver_temp_setting` | info / numérique | °C | non | non | Consigne de climatisation côté conducteur |
| Température passager | `passenger_temp_setting` | info / numérique | °C | non | non | Consigne de climatisation côté passager |
| Climatisation activée | `is_climate_on` | info / binaire | | non | non | 1 si la climatisation fonctionne |
| Chauffage siège conducteur | `seat_heater_left` | info / numérique | | non | non | Niveau de chauffage du siège conducteur (0 à 3) |
| Chauffage siège passager | `seat_heater_right` | info / numérique | | non | non | Niveau de chauffage du siège passager (0 à 3) |
| Chauffage du volant | `steering_wheel_heater` | info / binaire | | non | non | 1 si le chauffage du volant est actif |
| Mode dégivrage | `defrost_mode` | info / texte | | non | non | État du dégivrage |
| Climatisation automatique | `is_auto_conditioning_on` | info / binaire | | non | non | 1 si la climatisation automatique est active |
| Préconditionnement en cours | `is_preconditioning` | info / binaire | | non | non | 1 pendant un préconditionnement de l'habitacle ou de la batterie (à ne pas confondre avec **Préconditionnement planifié**, l'heure programmée) |
| Dégivrage avant | `is_front_defroster_on` | info / binaire | | non | non | 1 si le dégivrage du pare-brise est actif |
| Dégivrage arrière | `is_rear_defroster_on` | info / binaire | | non | non | 1 si le dégivrage de la lunette arrière est actif |
| Vitesse de ventilation | `fan_status` | info / numérique | | non | non | Palier de ventilation, valeur brute du véhicule (échelle non documentée par Tesla) |
| Maintien de climat (chien, camp) | `climate_keeper_mode` | info / texte | | non | non | Mode de maintien de climat, tel que renvoyé par le véhicule : `Off`, `On` (maintien), `Dog` (mode chien), `Party` (mode camp), `Unknown` |
| Protection surchauffe | `cabin_overheat_protection` | info / texte | | non | non | Protection contre la surchauffe de l'habitacle, telle que renvoyée par le véhicule : `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly` (ventilation seule) |
| Chauffage siège arrière gauche | `seat_heater_rear_left` | info / numérique | | non | non | Niveau de chauffage du siège arrière gauche (0 à 3) ; 0 aussi si le véhicule n'en est pas équipé |
| Chauffage siège arrière droit | `seat_heater_rear_right` | info / numérique | | non | non | Niveau de chauffage du siège arrière droit (0 à 3) ; 0 aussi si le véhicule n'en est pas équipé |
| Chauffage siège arrière centre | `seat_heater_rear_center` | info / numérique | | non | non | Niveau de chauffage du siège arrière central (0 à 3) ; 0 aussi si le véhicule n'en est pas équipé |
| Niveau chauffage volant | `steering_wheel_heat_level` | info / numérique | | non | non | Niveau de chauffage du volant : **0 inconnu, 1 arrêt, 2 bas, 3 haut** (voir l'avertissement ci-dessous) |
| Température min. réglable | `min_avail_temp` | info / numérique | °C | non | non | Température minimale réglable dans le véhicule, au dixième |
| Température max. réglable | `max_avail_temp` | info / numérique | °C | non | non | Température maximale réglable dans le véhicule, au dixième |
| Chauffage batterie | `battery_heater` | info / binaire | | non | non | 1 si le chauffage de la batterie est actif |
| Dernière erreur | `last_error` | info / texte | | non | oui | Cause du dernier échec de lecture ou de commande, suivie de la raison du proxy quand il en donne une ; **Aucune** quand tout va bien. Utilisable dans un scénario |
| Dernière lecture des données | `last_data_update` | info / texte | | non | oui | Date et heure (heure de Jeedom, `AAAA-MM-JJ HH:MM:SS`) de la dernière lecture réussie des données de charge et de climatisation |
| Âge des données (min) | `data_age` | info / numérique | min | non | oui | Minutes écoulées depuis la **Dernière lecture des données**, recalculées chaque minute sans interroger le proxy. Vaut 0 après chaque lecture réussie et augmente tant qu'aucune lecture n'aboutit (véhicule endormi, proxy injoignable, fenêtre d'endormissement). **99999** = aucune lecture connue, ou plus de 69 jours |
| Proxy joignable | `proxy_reachable` | info / binaire | | non | oui | 1 si le proxy a répondu au dernier cycle de rafraîchissement, 0 s'il est éteint, injoignable, ne répond pas dans les délais ou renvoie autre chose qu'une réponse valide du proxy (adresse erronée, proxy trop ancien). Un véhicule hors de portée ou endormi ne le fait pas passer à 0. Utilisable dans un scénario |
| Version du proxy | `proxy_version` | info / texte | | non | oui | Version renvoyée par le proxy au dernier cycle (**inconnue** si elle est illisible) ; garde sa dernière valeur quand le proxy ne répond pas |
| Rôle de clé | `key_role` | info / texte | | non | oui | Rôle probable de la clé du proxy pour ce véhicule : **Charging Manager** après le refus d'une commande réservée au rôle Owner faute de droits, **Owner** dès qu'une de ces commandes réussit, **Indéterminé** tant qu'aucune n'a été envoyée (voir [Rôle de la clé](#rôle-de-la-clé)). Dans un scénario, testez `Owner` ou `Charging Manager` (jamais traduits) ; « Indéterminé » suit la langue de Jeedom |
| Durée lecture état | `state_read_duration` | info / numérique | s | non | oui | Temps, en secondes au dixième, de la dernière lecture réussie de l'état du véhicule (présence, verrouillage, veille) au cycle de rafraîchissement ou par **Rafraîchir**. Un échec ne la modifie pas : elle garde la durée du dernier succès. Historisez-la pour suivre la santé de la liaison Bluetooth (voir [Lecture lente du proxy](#lecture-lente-du-proxy)) |
| Durée lecture données | `data_read_duration` | info / numérique | s | non | oui | Temps de la dernière lecture réussie des données de charge et de climatisation. Inchangée tant que le véhicule dort (aucune lecture). Une valeur proche de 0 est normale juste après une autre lecture : le proxy garde ces données en mémoire 30 secondes |
| Modèle | `model` | info / texte | | non | oui | Modèle décodé de la VIN, sans interroger le proxy : **Model S**, **Model X**, **Model 3**, **Model Y**, **Cybertruck**, **Semi** ou **Roadster** ; **Inconnu** si la VIN n'est pas celle d'un Tesla reconnu. Voir [Données étendues : ce qui est disponible](#données-étendues--ce-qui-est-disponible) |
| Année modèle | `model_year` | info / texte | | non | oui | Année modèle décodée de la VIN (par exemple `2023`) ; **Inconnu** si elle n'est pas décodable |
| Kilométrage | `odometer` | info / numérique | km | oui | oui | Compteur kilométrique, converti en kilomètres (le véhicule le renvoie en miles). Créée seulement si le proxy annonce `drive_state` |
| Rapport | `shift_state` | info / texte | | non | non | Rapport engagé : `P`, `R`, `N` ou `D` ; **vide** quand le véhicule ne le communique pas. Créée seulement si le proxy annonce `drive_state` |
| Vitesse | `speed` | info / numérique | km/h | non | non | Vitesse, supposée en mph côté véhicule et convertie en km/h (à confirmer en usage réel). Créée seulement si le proxy annonce `drive_state` |
| Puissance | `power` | info / numérique | kW | non | non | Puissance instantanée, valeur du véhicule en kilowatts, négative admise (à confirmer en usage réel). Créée seulement si le proxy annonce `drive_state` |
| Pression pneu avant gauche | `tpms_pressure_fl` | info / numérique | bar | non | oui | Pression du pneu, en bar, sans conversion. Créée seulement si le proxy annonce `tire_pressure` |
| Pression pneu avant droit | `tpms_pressure_fr` | info / numérique | bar | non | oui | Idem, pneu avant droit |
| Pression pneu arrière gauche | `tpms_pressure_rl` | info / numérique | bar | non | oui | Idem, pneu arrière gauche |
| Pression pneu arrière droit | `tpms_pressure_rr` | info / numérique | bar | non | oui | Idem, pneu arrière droit |
| Mise à jour | `software_update_status` | info / texte | | non | oui | **Aucune**, **Disponible**, **Téléchargement en cours** ou **Installation en cours** (un statut inattendu du proxy est affiché tel quel). Créée seulement si le proxy annonce `software_update` |
| Version proposée | `software_update_version` | info / texte | | non | oui | Version de la mise à jour proposée ; **Aucune** hors mise à jour, **Inconnue** si une mise à jour est active sans version rapportée |
| Progression | `software_update_progress` | info / numérique | % | non | non | Avancement du téléchargement ou de l'installation ; 0 hors de ces deux phases |
| Latitude | `latitude` | info / numérique | ° | non | non | Latitude du véhicule en degrés décimaux. **Masquée et non historisée** : donnée personnelle (voir [Position et confidentialité](#position-et-confidentialité)). Créée seulement si le proxy annonce `location_data` |
| Longitude | `longitude` | info / numérique | ° | non | non | Longitude du véhicule, mêmes règles que la latitude |
| À la maison | `at_home` | info / binaire | | non | oui | 1 si le véhicule est dans le rayon du domicile, 0 au-delà ; **jamais écrite** tant que le domicile ou la position sont inconnus |

L'information **Charge batterie** alimente aussi le suivi de batterie de Jeedom (page **Analyse > Équipements**) ; **Niveau de batterie (brut)** ne l'alimente pas.

Chaque information de charge et de climatisation est mise à jour indépendamment : si le véhicule ne renvoie pas l'une d'elles, elle garde sa dernière valeur et les autres sont tout de même actualisées.

**Informations de charge étendues.** Les dix informations de charge supplémentaires (**État de charge (traduit)**, **Autonomie nominale**, **Autonomie estimée**, **Niveau de batterie (brut)**, **Puissance de charge**, **Courant de charge réel**, **Phases de charge**, **Énergie ajoutée**, **Câble de charge** et **Charge rapide**) sont créées **masquées**, y compris sur un équipement existant lors de la mise à jour : affichez celles qui vous intéressent depuis l'onglet **Commandes**, votre choix d'affichage et d'historisation n'est jamais écrasé. Elles restent vides jusqu'à la première lecture des données d'un véhicule éveillé, puis gardent leur dernière valeur tant qu'il dort (voir **Âge des données (min)**) : en fin de charge, la puissance et le courant réel peuvent donc rester sur leur dernière valeur jusqu'à la prochaine lecture. Le détail de chaque état de charge reste porté par **État charge**.

**Ouvrants.** Les huit informations d'ouvrant (**Porte avant conducteur** à **Tonneau**) sont lues **sans réveiller le véhicule**, à chaque rafraîchissement des informations, comme la présence et le verrouillage. Un état que le véhicule ne sait pas donner (inconnu, échec de déverrouillage) laisse la **dernière valeur** en place, sans message. **Trappe de charge (ouvrant)** (lue même endormi) et **Trappe de charge ouverte** (lue seulement véhicule éveillé) peuvent différer quelques instants, y compris juste après une commande d'ouverture ou de fermeture de la trappe : la valeur converge après la relecture différée. Si le véhicule ne fournit pas du tout l'état de ses ouvrants, le proxy les transmet comme fermés : ils apparaissent alors **fermés** (seul un état explicitement inconnu laisse la dernière valeur). Avec un proxy antérieur à 2.3.0, une mise à jour du proxy est nécessaire : les ouvrants ne sont pas publiés (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)).

**Occupant et verrouillage détaillé.** Ces deux informations, **Occupant présent** et **État de verrouillage détaillé**, sont lues **sans réveiller le véhicule**, à chaque rafraîchissement des informations, en même temps que la présence et le verrouillage. Une présence inconnue laisse la **dernière valeur** en place : véhicule endormi, l'information peut rester figée, ne vous y fiez pas seule pour une sécurité. Un véhicule **verrouillé de l'intérieur** laisse **Verrouillage du véhicule** à 1. Après une commande de verrouillage, l'état détaillé suit dès que le véhicule confirme. Un état de verrouillage que le plugin ne connaît pas est affiché tel que le véhicule l'envoie. Ne confondez pas **Occupant présent** avec **Présence véhicule** (véhicule à portée Bluetooth du proxy). Avec un proxy antérieur à 2.3.0, une mise à jour du proxy est nécessaire : ces informations ne sont pas publiées (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)).

**Programmations lues dans le véhicule.** Trois informations texte `HH:MM`, créées **masquées**, reflètent la programmation du véhicule à chaque lecture des données (y compris en lecture « charge seule ») : **Heure de charge programmée** (mode charge différée), **Fin des heures creuses** et **Préconditionnement planifié** (mode départ programmé). Avec le mode **Off**, ou hors du mode concerné, elles sont **vides** (jamais `00:00`) : testez `== ""` dans un scénario. Le mode lui-même reste dans **Mode charge programmée**, inchangé. Elles gardent leur dernière valeur tant que le véhicule dort et se vident à la première lecture qui suit la désactivation de la programmation. Précisions : l'**heure de charge** est affichée dans le fuseau horaire de Jeedom ; **Fin des heures creuses** est la valeur du réglage, que l'option soit active ou non, et reste vide quand le véhicule indique minuit ; **Préconditionnement planifié** est l'heure de départ visée, affichée même les jours où la programmation ne s'applique pas ; les jours concernés et les programmations à plusieurs plages ne sont pas lus. Une donnée illisible laisse l'information inchangée (mention dans le log en mode debug).

**Informations de climatisation étendues.** Les quatorze informations ci-dessus, de **Climatisation automatique** à **Chauffage batterie**, sont créées **masquées** et non historisées, y compris sur un équipement existant lors de la mise à jour : affichez celles qui vous intéressent depuis l'onglet **Commandes**, votre choix n'est jamais écrasé. Elles sont lues avec les données de charge et de climatisation, sans requête supplémentaire et sans jamais réveiller le véhicule : elles gardent leur dernière valeur tant qu'il dort. Un champ que le véhicule ne renvoie pas laisse l'information inchangée sans empêcher les autres de se mettre à jour. Les valeurs sont celles du véhicule, sans transformation.

- **Échelle du chauffage du volant.** Attention : elle n'est pas celle des sièges. C'est l'échelle du protocole Tesla : relevez les valeurs sur votre véhicule avant de l'utiliser dans un scénario.

  | Valeur | Signification |
  |---|---|
  | 0 | inconnu (ou volant non équipé) |
  | 1 | arrêt |
  | 2 | bas |
  | 3 | haut |

  **Un test « supérieur à 0 » est donc faux** : la valeur 1 signifie que le chauffage est à l'arrêt. Pour savoir si le volant chauffe, testez `>= 2`. L'information existante **Chauffage du volant** (`steering_wheel_heater`) reste le simple indicateur actif / inactif. Pour les sièges, 0 est « arrêt » et 3 « haut ».
- **Équipement absent.** Un siège arrière ou un volant que le véhicule n'a pas est rapporté à 0, comme un équipement à l'arrêt : l'information ne permet pas de les distinguer.
- **Températures min. et max. réglables.** Ce sont les bornes de réglage de la climatisation du véhicule (par exemple 15 et 28 °C). Une valeur absente, nulle ou hors de la plage 5 à 40 °C est ignorée ; si le minimum n'est pas strictement inférieur au maximum, les deux sont ignorées (mention dans le log en mode debug). Elles garderont alors leur dernière valeur.
- **Chauffage batterie.** Il est lu dans les données de climatisation du véhicule. Le champ équivalent des données de charge n'est pas fourni par le proxy 2.3.0 et resterait toujours à 0 : il n'est pas utilisé.
- **Maintien de climat (chien, camp).** Valeurs possibles : `Off`, `On`, `Dog` (mode chien), `Party` (mode camp), `Unknown`. L'association de `Party` au mode camp est à confirmer sur votre véhicule. Une valeur illisible laisse l'information inchangée.
- **Protection surchauffe.** Valeurs possibles : `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly`. Un véhicule qui ne renseigne pas le réglage est rapporté `CabinOverheatProtectionOff`.
- **Vitesse de ventilation.** Valeur brute dont l'échelle n'est pas documentée : relevez-la sur votre véhicule avant de l'utiliser dans un scénario.
- **Préconditionnement et dégivrages.** Ils passent à 1 à la lecture des données qui suit leur déclenchement ; un cycle n'a lieu que si le véhicule est éveillé, et le proxy garde ses données 30 secondes en mémoire. Ce n'est pas une lecture déclenchée par l'événement.

**Mise à jour du plugin.** Les trois informations de programmation sont créées **masquées** sur chaque équipement existant et restent vides jusqu'à la première lecture des données d'un véhicule éveillé. L'information **Énergie cumulée de charge** est créée **masquée** et **historisée** sur chaque équipement existant lors de la mise à jour. Elle reste vide jusqu'à la première lecture des données d'un véhicule éveillé, puis démarre à 0 : l'énergie déjà chargée avant la mise à jour n'est pas rattrapée. De même, les actions **Ajuster selon le surplus**, **Ajouter une programmation de charge** et **Supprimer la programmation de charge** sont ajoutées **masquées** à chaque équipement existant ; ses réglages gardent leurs valeurs par défaut tant que vous ne les modifiez pas, et aucune commande existante n'est modifiée. Les quatorze informations de climatisation étendues sont elles aussi créées **masquées** sur chaque équipement existant, sans modifier aucune information de climatisation déjà présente.

### Compteurs d'énergie de charge

Pour suivre votre consommation de charge, le plugin tient un **index qui ne fait que croître** : l'information **Énergie cumulée de charge** (kWh). Le véhicule, lui, remet **Énergie ajoutée** à zéro à chaque nouvelle session de charge ; ce n'est donc pas un compteur utilisable tel quel.

- **Il démarre à 0** à la création de l'information (activation de la fonction), sans rattrapage de l'historique.
- **Calcul par différence** : à chaque lecture des données, le plugin ajoute au cumul l'énergie gagnée depuis la lecture précédente. Une session qui retombe sous **90 %** de la valeur précédemment vue (seuil de 10 %) est une nouvelle session : elle est ajoutée en entier. Une petite baisse isolée est ignorée. Une valeur négative, illisible ou supérieure à 1000 kWh (jugée aberrante) est ignorée. Une nouvelle session qui atteint déjà 90 % de la précédente dès la première lecture est sous-comptée.
- **Précision limitée par la cadence de lecture** : le plugin ne connaît l'énergie qu'aux moments où il lit les données, donc seulement véhicule éveillé et à la cadence réglée (voir [Lecture accélérée pendant la charge](#lecture-accélérée-pendant-la-charge)). Une charge entière commencée et terminée entre deux lectures peut être sous-comptée, et une charge faite hors de portée du proxy n'est comptée qu'en partie, au retour. À l'inverse, une lecture aberrante peut parfois faire compter une énergie en double : le cumul ne diminue jamais, mais il n'est pas garanti exact.
- **Énergie côté batterie** : c'est l'énergie ajoutée à la batterie, inférieure à celle du compteur ou de la borne (pertes de charge).
- **Plugin Énergie de Jeedom** : déclarez **Énergie cumulée de charge** comme commande de consommation ; en principe : index absolu, sans cocher « Consommation par jour » (à vérifier selon la version du plugin Énergie).
- **Jamais remis à zéro** par un clic sur **Sauvegarder** ni par une mise à jour du plugin. Il n'existe pas de remise à zéro manuelle. Supprimer l'information remet le cumul à 0 (elle est recréée vide au prochain enregistrement) ; un équipement dupliqué repart du cumul de l'original.

### Actions

Les actions marquées « masquée » ne sont pas affichées sur le widget par défaut ; rendez-les visibles depuis l'onglet **Commandes** de l'équipement.

| Libellé | Identifiant | Type / sous-type | Unité | Description |
|---|---|---|---|---|
| Rafraîchir | `refresh` | action / autre | | Relance immédiatement la lecture des informations (une éventuelle erreur apparaît dans **Dernière erreur**) |
| Rafraîchir (avec réveil) | `refresh_wakeup` | action / autre | | Réveille le véhicule si besoin, puis lit ses données de charge et de climatisation et les publie, en une seule action (voir [Rafraîchir avec réveil](#rafraîchir-avec-réveil)). Seule une action de votre part ou d'un scénario peut le faire : la lecture périodique ne réveille jamais le véhicule |
| Réveiller | `wake_up` | action / autre | | Réveille le véhicule, sans lire ses données. Inutile avant une commande : le proxy réveille le véhicule seul. Une relecture sans réveil suit la commande (voir [Relecture après une commande](#relecture-après-une-commande)) ; pour obtenir des valeurs fraîches tout de suite, préférez **Rafraîchir (avec réveil)** |
| Démarrer la charge | `charge_start` | action / autre | | Démarre la charge |
| Arrêter la charge | `charge_stop` | action / autre | | Arrête la charge |
| Courant de charge | `set_charging_amps` | action / curseur | A | Règle le courant de charge (entier, entre le Min et le Max de la commande ; 0 à 32 A tant que le véhicule n'a pas publié sa borne, puis son courant maximal ; réglez le Max à la main pour le figer, ou lancez une lecture avec réveil pour mettre à jour les bornes) |
| Limite de charge | `set_charge_limit` | action / curseur | % | Règle la limite de charge, entre le Min et le Max de la commande (50 à 100 % tant que le véhicule n'a pas publié ses bornes, puis ses limites) |
| Ajuster selon le surplus | `adjust_surplus` | action / curseur | W | Reçoit la **puissance disponible pour la charge** (en watts, valeur **absolue**, pas une variation) et décide seule s'il faut envoyer une commande (voir [Pilotage selon le surplus](#pilotage-selon-le-surplus)). Créée **masquée** : elle s'appelle depuis un scénario. |
| Ajouter une programmation de charge | `add_charge_schedule` | action / message | | Crée ou remplace la programmation de charge gérée par Jeedom : le **titre** porte les jours (`lun,mar,mer,jeu,ven`), le **message** l'heure de début (`23:00`). **Proxy du fork requis**, coordonnées de Jeedom renseignées (voir [Programmer la charge](#programmer-la-charge)). Créée **masquée**. |
| Supprimer la programmation de charge | `remove_charge_schedule` | action / autre | | Supprime la programmation créée par Jeedom ; sans effet ni erreur s'il n'y en a pas. **Proxy du fork requis** (voir [Programmer la charge](#programmer-la-charge)). Créée **masquée**. |
| Démarrer le climatiseur | `auto_conditioning_start` | action / autre | | Lance le préconditionnement |
| Arrêter le climatiseur | `auto_conditioning_stop` | action / autre | | Arrête le préconditionnement |
| Consigne conducteur | `set_driver_temp` | action / curseur | °C | Règle la température demandée côté conducteur, de 15 à 28 °C par pas de 0,5 °C ; le côté passager repart avec sa dernière valeur lue. **Proxy du fork requis**. Créée **masquée** (voir [Régler la consigne de température](#régler-la-consigne-de-température)). |
| Consigne passager | `set_passenger_temp` | action / curseur | °C | Règle la température demandée côté passager, de 15 à 28 °C par pas de 0,5 °C ; le côté conducteur repart avec sa dernière valeur lue. **Proxy du fork requis**. Créée **masquée** (voir [Régler la consigne de température](#régler-la-consigne-de-température)). |
| Régler le chauffage du siège avant gauche | `set_seat_heater_left` | action / liste | | Règle le chauffage du siège avant gauche : Arrêt, Bas, Moyen ou Haut (0 à 3). **Proxy du fork requis**. Créée **masquée** (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| Régler le chauffage du siège avant droit | `set_seat_heater_right` | action / liste | | Règle le chauffage du siège avant droit : Arrêt, Bas, Moyen ou Haut (0 à 3). **Proxy du fork requis**. Créée **masquée** (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| Régler le chauffage du siège arrière gauche | `set_seat_heater_rear_left` | action / liste | | Règle le chauffage du siège arrière gauche : Arrêt, Bas, Moyen ou Haut (0 à 3). **Proxy du fork requis**. Créée **masquée** (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| Régler le chauffage du siège arrière droit | `set_seat_heater_rear_right` | action / liste | | Règle le chauffage du siège arrière droit : Arrêt, Bas, Moyen ou Haut (0 à 3). **Proxy du fork requis**. Créée **masquée** (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| Régler le chauffage du siège arrière centre | `set_seat_heater_rear_center` | action / liste | | Règle le chauffage du siège arrière centre : Arrêt, Bas, Moyen ou Haut (0 à 3). **Proxy du fork requis**. Créée **masquée** (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| Régler le chauffage du volant | `set_steering_wheel_heater` | action / liste | | Allume ou éteint le chauffage du volant (Arrêt ou Marche, sans niveau). **Proxy du fork requis**. Créée **masquée** (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| Dégivrage maximal | `set_preconditioning_max` | action / liste | | Active (Marche) ou arrête (Arrêt) le dégivrage maximal du véhicule ; réveille le véhicule et consomme de la batterie. **Proxy du fork requis**. Créée **masquée** (voir [Dégivrage maximal](#dégivrage-maximal)). |
| Mode de maintien de climat | `set_climate_keeper_mode` | action / liste | | Choisit le maintien de climat : Arrêt (0), Maintien (1), Mode chien (2) ou Mode camp (3) ; réveille le véhicule et consomme de la batterie. **Proxy du fork requis**. Créée **masquée** (voir [Mode chien, camp et maintien de climat](#mode-chien-camp-et-maintien-de-climat)). |
| Ouvrir la trappe de charge | `charge_port_door_open` | action / autre | | Ouvre la trappe de charge (masquée) |
| Fermer la trappe de charge | `charge_port_door_close` | action / autre | | Ferme la trappe de charge (masquée) |
| Faire clignoter les feux | `flash_lights` | action / autre | | Fait clignoter les phares (masquée) |
| Klaxonner | `honk_horn` | action / autre | | Actionne le klaxon |
| Verrouiller les portes | `door_lock` | action / autre | | Verrouille le véhicule (masquée) |
| Déverrouiller les portes | `door_unlock` | action / autre | | Déverrouille le véhicule (masquée) |
| Ouvrir le coffre arrière | `open_trunk_rear` | action / autre | | Ouvre le coffre arrière, après une relecture de l'état : refusée si le coffre est lu ouvert, en mouvement ou inconnu ; réveille le véhicule. **Proxy du fork requis**, confirmation demandée. Créée **masquée** (voir [Ouvrir le coffre arrière et le frunk](#ouvrir-le-coffre-arrière-et-le-frunk)). |
| Ouvrir le frunk | `open_trunk_front` | action / autre | | Ouvre le coffre avant ; réveille le véhicule. **Proxy du fork requis**, confirmation demandée. Créée **masquée** (voir [Ouvrir le coffre arrière et le frunk](#ouvrir-le-coffre-arrière-et-le-frunk)). |
| Mode sentinelle | `set_sentry_mode` | action / liste | | Active ou désactive le mode sentinelle (**Activé** ou **Désactivé**) (masquée). L'état se lit dans **Sentinelle** et **Provenance de la sentinelle** (voir [État du mode sentinelle](#état-du-mode-sentinelle)) |

## Exemples d'utilisation

- **Charge solaire** : dans un scénario, envoyez la puissance disponible à **Ajuster selon le surplus** (voir l'[exemple pas à pas : charge solaire](#exemple-pas-à-pas--charge-solaire-avec-ajuster-selon-le-surplus) et [Pilotage selon le surplus](#pilotage-selon-le-surplus)).
- **Heures creuses** : activez la **Charge aux heures creuses** de l'équipement (plage, SoC cible) : Jeedom démarre et arrête la charge lui-même (voir le [pas à pas pour configurer la charge aux heures creuses](#charge-aux-heures-creuses)). Vous pouvez aussi, sans cette fonction, déclencher **Démarrer la charge** au début des heures creuses et **Arrêter la charge** à leur fin depuis un scénario.
- **Préchauffage** : activez le **Préconditionnement planifié par Jeedom** de l'équipement (heure de départ, jours, avance) : Jeedom démarre et arrête la climatisation lui-même (voir l'[exemple d'usage](#préconditionnement-planifié-par-jeedom)). Vous pouvez aussi, sans cette fonction, lancer **Démarrer le climatiseur** depuis un scénario quelques minutes avant votre départ.
- **Alerte** : recevez une notification si **Verrouillage du véhicule** reste à 0 le soir.
- **Panne de liaison** : recevez une notification quand **Dernière erreur** passe à autre chose que **Aucune** (proxy injoignable, proxy sans clé appairée...). Un véhicule qui dort ne la déclenche pas.
- **Garde de fraîcheur** : n'ajustez le courant de charge que si les données ont moins de 5 minutes, sinon ne faites rien (voir l'exemple pas à pas « n'agir que sur des données récentes » ci-dessous).
- **Coffre resté ouvert** : activez l'alerte d'ouverture prolongée et déclenchez une notification (voir l'[exemple pas à pas : être alerté quand le coffre reste ouvert](#exemple-pas-à-pas--être-alerté-quand-le-coffre-reste-ouvert)).

### Exemple pas à pas : charge solaire avec Ajuster selon le surplus

Ce scénario envoie régulièrement à **Ajuster selon le surplus** la puissance que votre production solaire peut consacrer à la charge ; le plugin décide seul s'il faut vraiment changer le courant, démarrer ou arrêter la charge (voir [Pilotage selon le surplus](#pilotage-selon-le-surplus)).

**Prérequis**

- Le véhicule est **branché** (sinon le plugin s'abstient : **« Véhicule non branché : ajustement selon le surplus ignoré »**).
- **Intervalle pendant la charge** réglé sur **1 minute** dans l'équipement : le pilotage décide d'après le dernier **État charge** lu, donc d'après la fraîcheur des lectures.
- Une mesure de votre **export réseau** en watts (compteur, passerelle de l'onduleur), ou à défaut la **Puissance de charge** du véhicule.
- L'action **Ajuster selon le surplus** n'a pas besoin d'être visible : elle est appelée depuis le scénario (la clé du proxy Charging Manager suffit, voir [Rôle de la clé](#rôle-de-la-clé)).

**Réglages de départ.** Dans la section **Pilotage selon le surplus** de l'équipement, les champs laissés vides prennent ces valeurs. Ce sont des **points de départ indicatifs, à valider sur votre installation** : aucune mesure n'a encore été faite pour les confirmer.

| Réglage | Valeur de départ | À adapter si |
|---|---|---|
| **Tension du réseau (V)** | 230 | votre tension phase-neutre est différente |
| **Phases** | Monophasé | votre borne est **triphasée** : choisissez Triphasé, sinon le courant visé est trois fois trop haut |
| **Pas d'ajustement (A)** | 1 | vous voulez moins de variations (pas plus grand) |
| **Hystérésis (A)** | 2 | le courant change trop souvent (valeur plus grande) |
| **Intervalle minimal entre commandes (s)** | 120 (60 au minimum) | le véhicule est trop sollicité (valeur plus grande) |
| **Courant minimal de démarrage (A)** | 6 | votre véhicule ou votre borne exige un courant plus élevé pour démarrer |
| **Seuil d'arrêt (A)** | 5 (jamais supérieur au démarrage) | vous voulez arrêter plus tôt ou plus tard |
| **Durée de maintien avant arrêt (s)** | 300 | les passages nuageux arrêtent trop souvent la charge (valeur plus grande) |

**Créer le scénario**

1. Ouvrez **Outils > Scénarios**, cliquez sur **Ajouter** et nommez le scénario, par exemple « Charge solaire Tesla ». Dans **Mode du scénario**, choisissez **Programmé** et indiquez une exécution **toutes les 2 à 5 minutes** (par exemple `*/2 * * * *` pour toutes les 2 minutes). Appeler plus souvent ne sert à rien : le plugin ignore les appels qui n'apportent rien.
2. Ouvrez l'onglet **Scénario**, cliquez sur **+ Bloc** et choisissez **Si/Alors/Sinon**.
3. Dans **SI**, saisissez une garde de fraîcheur, par exemple `#[Garage][Tesla][Âge des données (min)]# <= 5` (voir l'[exemple pas à pas : n'agir que sur des données récentes](#exemple-pas-à-pas--nagir-que-sur-des-données-récentes)). Cette garde est **facultative**.
4. Dans **ALORS**, ajoutez une **Action** d'affectation de variable : nom `puissance_dispo`, valeur = **export réseau + puissance de charge**, en **watts**. Par exemple `#[Garage][Compteur][Export réseau]# + #[Garage][Tesla][Puissance de charge]# * 1000`.
5. Toujours dans **ALORS**, ajoutez une **Action** : la commande **Ajuster selon le surplus** du véhicule, avec la valeur `variable(puissance_dispo)` (lecture de la variable affectée à l'étape précédente).
6. **Sauvegardez**, puis lancez le scénario une première fois à la main.

**Pourquoi « export + puissance de charge ».** La valeur envoyée est la puissance **absolue** que le véhicule peut consommer. L'export mesuré par le compteur est déjà **diminué** de ce que le véhicule consomme : sans ajouter la puissance de charge actuelle, la consigne retomberait à chaque ajustement. Si votre compteur donne l'export avec un signe négatif, corrigez le signe pour obtenir des watts positifs. Une valeur négative est de toute façon ramenée à 0 W.

**Si la seule source est la Puissance de charge du véhicule.** Elle est en **kilowatts** et souvent **entière** : multipliez par 1000 (comme ci-dessus) et attendez-vous à une valeur grossière. Préférez, si vous en avez, la mesure d'un compteur ou de la borne.

**Vérifier que ça fonctionne.** Passez le log du plugin en **Debug** (**Configuration du plugin > Logs**) et lancez le scénario : chaque appel écrit une ligne **« pilotage selon le surplus : … W, courant calculé … A, cible … A, décision … (motif) »**. Les décisions possibles sont notamment `set_charging_amps`, `charge_start`, `charge_stop`, `aucune` et `ignorer` ; le motif explique pourquoi (hystérésis, intervalle minimal, courant déjà à la cible…). Une abstention du plugin apparaît aussi dans **Dernière erreur**.

**Ce qui se passe la nuit.**

- Sans production, la puissance disponible tombe à **0 W** : le courant calculé passe sous le **Seuil d'arrêt**, et la charge est **arrêtée** une fois la **Durée de maintien avant arrêt** écoulée (300 s par défaut). Le lendemain, elle redémarre quand le courant calculé atteint le **Courant minimal de démarrage**.
- Si vous utilisez aussi la [Charge aux heures creuses](#charge-aux-heures-creuses), l'appel de **Ajuster selon le surplus** est **ignoré pendant la plage** (sans erreur) : le scénario solaire n'arrête donc pas la charge des heures creuses. Hors plage, le pilotage selon le surplus reprend la main.

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

### Exemple pas à pas : n'agir que sur des données récentes

L'information **Âge des données (min)** donne le nombre de minutes écoulées depuis la dernière lecture réussie des données de charge et de climatisation. Elle vaut 0 juste après une lecture et augmente tant qu'aucune lecture n'aboutit : véhicule endormi, fenêtre d'endormissement ouverte, proxy injoignable. Elle vaut **99999** tant qu'aucune lecture n'est connue (équipement neuf, plugin juste mis à jour). Le scénario suivant, pour un pilotage solaire, n'ajuste le **Courant de charge** que si cette valeur est récente :

1. Ouvrez **Outils > Scénarios**, cliquez sur **Ajouter** et nommez le scénario, par exemple « Charge solaire Tesla ». Dans **Mode du scénario**, choisissez **Programmé** et indiquez une exécution toutes les 5 minutes.
2. Ouvrez l'onglet **Scénario**, cliquez sur **+ Bloc** et choisissez **Si/Alors/Sinon**.
3. Dans le champ **SI**, saisissez la condition `#[Objet][Véhicule][Âge des données (min)]# <= 5` (par exemple `#[Garage][Tesla][Âge des données (min)]# <= 5`), ou choisissez la commande avec le bouton de sélection puis ajoutez `<= 5`.
4. Dans **ALORS**, ajoutez une **Action** : la commande **Courant de charge** du véhicule, avec la valeur calculée par votre scénario à partir de la production solaire.
5. Dans **SINON**, ne mettez **rien** (le courant de charge reste ce qu'il était), ou ajoutez une notification, par exemple « Données Tesla trop anciennes : courant de charge inchangé ».
6. **Sauvegardez**, puis réglez **Intervalle pendant la charge** sur **1 minute** dans l'équipement : pendant la charge, l'âge des données reste à 1 minute au plus et la condition est vraie.

Pourquoi **5** ? C'est l'intervalle de rafraîchissement par défaut : au-delà, au moins une lecture a manqué. Adaptez le seuil à votre cadence (un peu plus que l'intervalle utilisé pendant la charge).

Pourquoi **99999** est une bonne chose ici : tant qu'aucune lecture n'est connue, la condition `<= 5` est **fausse**, le scénario s'abstient et n'envoie aucun courant. Il est prudent par construction.

> **Attention**
>
> N'utilisez **pas** **Âge des données (min)** comme **déclencheur** d'un scénario en mode **Provoqué** : cette information est recalculée **chaque minute** et change donc sans cesse, le scénario se lancerait en boucle (et une notification partirait à chaque fois).

**Variante : alerte « données de plus de 2 heures ».** Créez un scénario en mode **Programmé** (par exemple toutes les heures) avec la condition `#[Objet][Véhicule][Âge des données (min)]# >= 120 ET #[Objet][Véhicule][Âge des données (min)]# < 99999` et une notification dans **ALORS**. La borne `< 99999` évite une fausse alerte quand aucune lecture n'est connue ; préférez `>= 120` à une égalité exacte (`== 120`), qui n'est vraie qu'une minute et peut être sautée. Un véhicule qui dort longtemps déclenche cette alerte sans qu'il y ait de panne : c'est un simple constat de fraîcheur. Pour obtenir des données fraîches, lancez **Rafraîchir (avec réveil)**.

### Exemple pas à pas : être alerté quand le coffre reste ouvert

Ce scénario vous prévient quand un ouvrant (coffre arrière, frunk, porte, trappe de charge) reste ouvert plus de 10 minutes. Il repose sur l'alerte d'ouverture prolongée (voir [Alertes d'ouverture prolongée](#alertes-douverture-prolongée)) ; une clé Charging Manager suffit, ce sont des lectures.

1. Ouvrez la page de votre véhicule (**Plugins > Communication > Tesla BLE**) et allez au bloc **Alertes d'ouverture prolongée**.
2. Dans **Ouvrant resté ouvert**, cochez **Activer** et saisissez **Durée avant alerte (min)** : `10`. La durée est obligatoire, de 1 à 1440 minutes.
3. **Sauvegardez**. Un message d'erreur à l'enregistrement signale une durée vide ou invalide (voir [Messages à l'enregistrement](#messages-à-lenregistrement)).
4. Ouvrez l'onglet **Commandes** et cochez **Afficher** sur **Alerte ouvrants** (elle est masquée par défaut, mais déjà historisée). **Sauvegardez**.
5. Ouvrez **Outils > Scénarios**, cliquez sur **Ajouter** et nommez le scénario, par exemple « Alerte coffre ouvert ». Dans **Mode du scénario**, choisissez **Provoqué**.
6. Dans **Déclencheur(s)**, ajoutez la commande **Alerte ouvrants** de votre véhicule, par exemple `#[Garage][Tesla][Alerte ouvrants]#`.
7. Dans l'onglet **Scénario**, ajoutez un bloc **Si/Alors/Sinon** avec la condition `#[Garage][Tesla][Alerte ouvrants]# == 1`. Le scénario se lance aussi au retour à 0 : sans cette condition, vous seriez prévenu à la fermeture.
8. Dans **ALORS**, ajoutez une **Action** de notification de votre installation (application mobile, Telegram, e-mail…) avec un texte comme « Un ouvrant de la Tesla est resté ouvert depuis plus de 10 minutes ». Le centre de messages de Jeedom reçoit de son côté un message qui nomme l'ouvrant, sans rien configurer.
9. **Sauvegardez**, puis testez : ouvrez le coffre arrière à la main et attendez la durée choisie **plus deux intervalles de rafraîchissement** (jusqu'à 20 minutes avec 10 minutes et l'intervalle par défaut de 5 minutes). **Alerte ouvrants** passe à 1, le message apparaît dans le centre de messages et la notification part.
10. Fermez le coffre : à la lecture suivante, **Alerte ouvrants** repasse à 0 et le scénario se lance sans notifier. Le message reste dans le centre de messages : supprimez-le.

Pour un véhicule laissé déverrouillé, procédez de même avec **Véhicule déverrouillé sans occupant** et l'information **Alerte déverrouillé sans occupant**.

**Conseils d'usage de la présence d'un occupant.** **Occupant présent** (`user_present`) vaut 1 quand le véhicule détecte une personne à bord.

- **Condition « personne à bord ».** Dans un scénario, testez `#[Garage][Tesla][Occupant présent]# == 0` avant une action qui n'a de sens que véhicule vide (par exemple relancer un verrouillage). Associez-la à **Verrouillage du véhicule** et testez ces deux informations plutôt que le libellé **État de verrouillage détaillé**, qui change avec la langue de Jeedom.
- **Présence inconnue = dernière valeur.** Quand le véhicule ne donne pas l'état (il dort), l'information garde sa dernière valeur : elle peut afficher « personne » alors qu'une personne est restée à bord, ou l'inverse. Contrôlez **Âge des données (min)** si la décision compte.
- **Ce n'est pas une sécurité.** Ne vous en servez jamais pour protéger une personne ou un animal (par exemple pour décider de couper la climatisation : un enfant ou un animal resté à bord peut ne pas être détecté). Ne la confondez pas avec **Présence véhicule**, qui dit seulement que le véhicule est à portée Bluetooth du proxy.

## Limitations connues

- **Après une commande**, seuls la limite de charge, le courant de charge et le verrouillage sont mis à jour tout de suite. Les autres informations sont à jour après la **relecture programmée** (30 secondes par défaut, voir [Relecture après une commande](#relecture-après-une-commande)), ou à la lecture suivante si le proxy est occupé. Si le véhicule s'est rendormi, les dernières valeurs sont conservées (aucune erreur, aucun réveil) ; hors de portée, la présence passe à « Non » ; si le proxy est injoignable, « Dernière erreur » est renseignée.
- **Véhicule endormi** : les informations de charge et de climatisation ne sont lues que véhicule réveillé (le plugin ne le réveille jamais de lui-même). Utilisez **Rafraîchir (avec réveil)**.
- **Fenêtre d'endormissement** : pendant la fenêtre, les informations de charge et de climatisation et la **Dernière lecture des données** sont figées (durée par défaut 30 minutes). Une charge ou une climatisation lancée depuis l'application sans changement visible de l'état sans réveil n'est vue qu'à la lecture de contrôle. Décochez **Laisser le véhicule s'endormir** dans l'équipement pour une lecture complète à chaque passage.
- **Clé Charging Manager** : le verrouillage, le klaxon, les feux et le mode sentinelle sont refusés par le véhicule. Le plugin le détecte (information **Rôle de clé**) mais ne grise pas ces commandes sur le dashboard (voir [Rôle de la clé](#rôle-de-la-clé)).
- **Climatisation en charge seule** : avec **Lire aussi la climatisation** sur **Non, charge seule**, toutes les informations de climatisation (températures, chauffages, dégivrage, ventilation, maintien de climat, climatisation active, etc.) ne sont plus mises à jour et gardent leur dernière valeur ; les commandes de climatisation restent disponibles.
- **Compteur d'énergie de charge** : sa précision dépend de la cadence de lecture, il peut sous-compter une charge courte ou faite hors de portée et il n'est pas remis à zéro ; il n'est lu qu'à la cadence des lectures, donc une cadence espacée le rend moins précis (voir [Compteurs d'énergie de charge](#compteurs-dénergie-de-charge)).
- **Pilotage selon le surplus** : les seuils par défaut (démarrage 6 A, arrêt 5 A, maintien 300 s) sont à valider avec votre véhicule ; la référence est la **dernière consigne envoyée par le pilotage** (un réglage manuel concurrent n'est vu qu'après un écart supérieur à l'hystérésis, un arrêt ou un débranchement) ; un appel de scénario peut attendre jusqu'à environ 210 secondes ; la décision repose sur le dernier **État charge** lu, donc sur la fraîcheur des lectures (voir [Lecture accélérée pendant la charge](#lecture-accélérée-pendant-la-charge)).
- **Pilotage solaire : sollicitation Bluetooth et veille.** Pendant la charge, le véhicule est éveillé de toute façon, mais le pilotage selon le surplus le sollicite : avec **Intervalle pendant la charge** à 1 minute, une lecture a lieu **chaque minute**, **chaque commande réellement envoyée réveille le véhicule** et **une relecture suit chaque commande réussie** (voir [Relecture après une commande](#relecture-après-une-commande)). Un véhicule qui reçoit des commandes toute la journée a donc peu de chances de s'endormir. Espacez les appels (**Intervalle minimal entre commandes**, hystérésis, scénario toutes les 2 à 5 minutes). **Aucune mesure d'usure de la liaison Bluetooth ou de la batterie n'est publiée** : n'en déduisez ni garantie ni risque chiffré.
- **Charge aux heures creuses** : la décision suit la cadence de lecture (arrêt au SoC cible approximatif sans **Intervalle pendant la charge**) ; un véhicule endormi n'est jamais arrêté, et son état publié peut être périmé ; **démarrer la charge réveille le véhicule** ; un démarrage non suivi d'une charge n'est **pas relancé** avant la plage suivante (un seul démarrage par branchement) ; un **Démarrer** ou **Arrêter** lancé depuis Jeedom pendant la plage suspend le pilotage jusqu'à la plage suivante ; une plage qui commence dans l'heure sautée au **changement d'heure d'été** ne démarre qu'à la fin de cette heure, et une action manuelle faite pendant cette heure peut être ignorée ; une seule plage par véhicule ; le délai de 2 minutes pour constater le résultat d'une commande est à valider en usage réel (voir [Charge aux heures creuses](#charge-aux-heures-creuses)).
- **Préconditionnement planifié par Jeedom** : le rôle Owner (supposé) est à confirmer en usage réel ; la décision suit la cadence de lecture (démarrage et arrêt à quelques minutes près, rien si aucune lecture ne tombe dans la fenêtre ; un intervalle de 5 minutes au plus est conseillé) ; **démarrer le climatiseur réveille le véhicule** et consomme de la batterie ; un véhicule vu endormi n'est jamais arrêté ; une climatisation qui tourne encore à la première lecture suivant la fin de la fenêtre est arrêtée, même avec un occupant ; désactiver la fonction pendant la fenêtre n'arrête pas une climatisation déjà démarrée ; la température utilisée est celle déjà réglée dans le véhicule ; une seule fenêtre par véhicule, la programmation du véhicule n'est pas lue pour décider ; nécessite **Lire aussi la climatisation** sur **Oui** (voir [Préconditionnement planifié par Jeedom](#préconditionnement-planifié-par-jeedom)).
- **Programmations de charge** : **Heure de charge programmée** suppose que le véhicule renvoie, en mode charge différée, un horodatage valide par Bluetooth (à confirmer en usage réel : sinon l'information reste vide) ; **Fin des heures creuses** est publiée même si l'option heures creuses est décochée (le proxy ne transmet pas son état) ; les jours d'application et les plages multiples ne sont pas lus.
- **Programmer la charge** : réservé au proxy du fork (refus immédiat avec le proxy 2.3.0, dont la version officielle n'a pas la route de programmation : le fork l'ajoute, versions `2.3.0-tb.N`) ; une seule programmation gérée par Jeedom par véhicule, avec heure de début seulement ; elle suit les coordonnées de Jeedom, qui doivent correspondre au lieu de stationnement ; l'heure est celle du véhicule ; le remplacement sans doublon, le rôle de clé minimal et la mise à jour des informations de programmation après la commande sont à confirmer en usage réel (voir [Programmer la charge](#programmer-la-charge)).
- **Consigne de température** : réservée au proxy du fork (refus immédiat avec le proxy 2.3.0) ; les deux côtés sont toujours envoyés ensemble, l'autre côté avec sa dernière valeur lue (une consigne réglée sur l'écran du véhicule depuis la dernière lecture peut être écrasée) ; le curseur est limité à 15 à 28 °C, par demi-degré ; le rôle Owner supposé nécessaire et le niveau de température (une consigne qui ne passe pas en « HI ») sont à confirmer en usage réel (voir [Régler la consigne de température](#régler-la-consigne-de-température)).
- **Chauffage des sièges et du volant** : réservé au proxy du fork, version `2.3.0-tb.2` au minimum (refus immédiat avec le proxy 2.3.0) ; les six actions restent **masquées** : à afficher soi-même après le passage au fork ; pas de dossiers ni de troisième rangée ; volant en marche/arrêt seulement ; le comportement avec la climatisation coupée, avec un siège absent et avec un volant à chauffage automatique est à valider en usage réel.
- **Dégivrage maximal** : réservé au proxy du fork, version `2.3.0-tb.1` au minimum (refus immédiat avec le proxy 2.3.0) ; l'action reste **masquée** : à afficher soi-même après le passage au fork ; elle réveille le véhicule et consomme de la batterie, et ne s'arrête pas toute seule ; avec **Lire aussi la climatisation** sur **Non, charge seule**, ou si le véhicule se rendort, **Mode dégivrage** garde la valeur optimiste (un `Off` affiché peut être faux si le véhicule dit `Normal`) ; le rôle Owner et le comportement à l'arrêt (`Off` ou `Normal`) sont à valider en usage réel.
- **Mode chien, camp et maintien de climat** : réservé au proxy du fork, version `2.3.0-tb.1` au minimum (refus immédiat avec le proxy 2.3.0) ; l'action reste **masquée** : à afficher soi-même après le passage au fork ; elle réveille le véhicule, consomme de la batterie sur une longue durée, ne s'arrête pas toute seule et ne remplace pas une surveillance de la température pour un animal ; avec **Lire aussi la climatisation** sur **Non, charge seule**, ou si le véhicule se rendort, **Maintien de climat (chien, camp)** garde la valeur annoncée ; la fenêtre d'endormissement ne s'ouvre pas tant qu'un maintien (`On`, `Dog`, `Party`) est lu ; le rôle Owner, le nom `Party` du mode camp et la valeur relue après un arrêt sont à valider en usage réel.
- **Ouvrir le coffre arrière et le frunk** : réservé au proxy du fork, version `2.3.0-tb.2` au minimum (refus immédiat avec le proxy 2.3.0) ; les deux actions restent **masquées** : à afficher soi-même après le passage au fork ; elles réveillent le véhicule ; le coffre arrière n'est ouvert que s'il est lu fermé (la relecture peut manquer une ouverture récente, et un hayon motorisé peut alors se refermer) ; un loquet signalé « non lâché » (échec d'ouverture précédent) est traité comme fermé et la commande est renvoyée, comportement à valider en usage réel ; le frunk n'est pas relu ; le plugin ne referme jamais un coffre ; le rôle Owner supposé nécessaire et le comportement sur un coffre motorisé (ou un frunk motorisé) sont à valider en usage réel.
- **État du mode sentinelle** : la lecture réelle exige le proxy du fork en version `2.3.0-tb.2` au minimum et un véhicule **éveillé** ; sinon l'information suit le **dernier ordre** envoyé par Jeedom et ne voit ni un changement fait depuis l'application, l'écran du véhicule ou une coupure automatique, ni une valeur lue sur un véhicule endormi (dernière valeur lue conservée) ; l'état `Idle` est compté **Activée** (à confirmer en usage réel) ; les libellés suivent la langue de Jeedom (voir [État du mode sentinelle](#état-du-mode-sentinelle)).
- **Alertes d'ouverture prolongée** : la durée n'est comptée que sur des lectures réussies, à la cadence de rafraîchissement (alerte entre la durée et la durée plus deux intervalles). Si le **cache de Jeedom est vidé** pendant une alerte, l'épisode est oublié : l'info repasse à 0 puis à 1 après une durée complète, avec un second message. Un **État charge** figé sur un véhicule endormi (par exemple « Stopped » ou « Complete » périmé après un débranchement) masque une trappe de charge oubliée ouverte. Sans l'information d'ouvrants du véhicule (huit états fermés ou absents), l'épisode est considéré comme clos. Le message n'est pas retiré du centre de messages à la fermeture.
- **Données étendues** (modèle, kilométrage et conduite, pneus, mise à jour logicielle, position) : à l'exception du modèle et de l'année, elles exigent le **proxy du fork** (`2.3.0-tb.2` au minimum) qui les **annonce** ; sinon elles ne sont pas créées. Elles ne sont lues que **véhicule éveillé** et à portée Bluetooth (les pressions, la mise à jour et la position au plus toutes les 15 minutes, pas pendant une fenêtre d'endormissement). Les unités de **Vitesse** (mph) et de **Puissance** (kW) sont supposées et à confirmer en usage réel. **À la maison** est binaire : jamais écrite sans domicile ni position (la tuile affiche 0 avant le premier calcul), elle ne repasse pas à 0 quand le véhicule part ; testez `== 1` avec **Présence véhicule**. Le log `event` de Jeedom enregistre latitude et longitude même masquées (voir [Position et confidentialité](#position-et-confidentialité)).
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
| Rôle de la clé | **Charging Manager** par défaut : lectures et charge seulement, y compris le pilotage selon le surplus et la charge aux heures creuses ; **Owner** pour le verrouillage, le déverrouillage, le klaxon, les feux, la sentinelle, les coffres (supposé) et le préconditionnement planifié (voir [Rôle de la clé](#rôle-de-la-clé)). |
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
- **« Charge aux heures creuses : l'heure de début (ou de fin) doit être au format HH:MM, de 00:00 à 23:59 »**, **« … le SoC cible doit être un entier entre 1 et 100 % »**, **« … la plage horaire est vide, l'heure de fin doit différer de l'heure de début »** et **« … renseignez l'heure de début, l'heure de fin et le SoC cible pour activer la fonction »** : réglage de la **Charge aux heures creuses** invalide ; corrigez-le (rien n'a été enregistré).
- **« Pilotage selon le surplus : … »** : réglage du pilotage selon le surplus hors bornes (voir [Pilotage selon le surplus](#pilotage-selon-le-surplus)).
- **« Préconditionnement planifié : l'heure de départ doit être au format HH:MM, de 00:00 à 23:59 »**, **« … l'avance doit être un entier entre 1 et 60 minutes »**, **« … la durée maximale doit être un entier entre 1 et 120 minutes »**, **« … la durée maximale doit être au moins égale à l'avance »**, **« … renseignez l'heure de départ pour activer la fonction »**, **« … cochez au moins un jour pour activer la fonction »** et **« … « Lire aussi la climatisation » doit rester à Oui pour activer la fonction »** : réglage du **Préconditionnement planifié par Jeedom** invalide ; corrigez-le (rien n'a été enregistré).
- **« Alertes d'ouverture prolongée : la durée avant alerte … doit être un entier entre 1 et 1440 minutes, obligatoire pour activer l'alerte »** : la durée de l'alerte (ouvrant resté ouvert, ou véhicule déverrouillé sans occupant) est vide alors que l'alerte est activée, ou n'est pas un entier de 1 à 1440 (voir [Alertes d'ouverture prolongée](#alertes-douverture-prolongée)). Rien n'est enregistré.
- **« Position du domicile invalide : renseignez la latitude (de -90 à 90) et la longitude (de -180 à 180) en degrés décimaux, 8 décimales au plus, ou laissez les deux vides pour utiliser la position de Jeedom »** : une seule des deux coordonnées du domicile est renseignée, ou l'une est hors plage, non numérique, avec trop de décimales, ou le couple vaut 0/0. Corrigez-les (ou videz les deux champs pour utiliser la position de Jeedom) ; rien n'a été enregistré. La valeur saisie n'est jamais recopiée dans le message (voir [Position et confidentialité](#position-et-confidentialité)).
- **« Rayon du domicile invalide : nombre entier de mètres, de 10 à 10000 »** : le **Rayon (m)** n'est pas un entier de 10 à 10000. Corrigez-le (ou videz le champ pour 100 m) ; rien n'a été enregistré.
- **« Erreur interne du plugin : consultez le log TeslaBLE »** : erreur imprévue lors de l'enregistrement ; le détail est dans le log du plugin.

### Centre de messages de Jeedom (après une mise à jour)

- **« La VIN de l'équipement … est invalide : corrigez-la dans sa page de configuration… »** : la VIN enregistrée par une ancienne version n'est pas valable. Corrigez-la.
- **« L'équipement … a la même VIN que l'équipement … »** : deux équipements pour un même véhicule. Supprimez le doublon ou corrigez sa VIN.
- **« L'information … est historisée : elle reste numérique et n'est plus mise à jour… »** : voir [Heure de départ programmée](#heure-de-départ-programmée).
- **« Adaptateur Bluetooth du proxy probablement figé — … »** : voir [Alerte adaptateur Bluetooth figé](#alerte-adaptateur-bluetooth-figé). Redémarrez le Raspberry Pi.
- **« … : ouvrant « … » ouvert depuis plus de … min »** et **« … : véhicule déverrouillé sans occupant depuis plus de … min »** : alertes d'ouverture prolongée, un message par ouvrant et par épisode (voir [Alertes d'ouverture prolongée](#alertes-douverture-prolongée)). Le message n'est pas retiré à la fermeture : supprimez-le.

### Information « Dernière erreur » (lecture)

| Texte affiché | Cause | Action |
|---|---|---|
| **Aucune** | Le dernier cycle de lecture a réussi (ou le véhicule dort, ce qui n'est pas une erreur). | Rien à faire. |
| **Proxy injoignable** | Le proxy ne répond pas à l'adresse configurée. | Vérifiez l'URL, que le proxy est démarré, l'alimentation et le Wi-Fi du Raspberry Pi. |
| **Délai dépassé** | Le proxy ou le véhicule répond trop lentement. | Vérifiez le Raspberry Pi (alimentation, Wi-Fi), redémarrez le proxy si cela se répète. |
| **Adaptateur Bluetooth du proxy probablement figé : redémarrez le Raspberry Pi** | Plusieurs lectures de suite ont dépassé leur délai alors que le proxy répond : voir [Alerte adaptateur Bluetooth figé](#alerte-adaptateur-bluetooth-figé). | Redémarrez le Raspberry Pi. |
| **Proxy sans clé : appairage à faire — …** | Aucune clé sur le proxy : il n'en a encore généré ou installé aucune. | Générez une clé (**Generate**) dans le tableau de bord du proxy, envoyez-la au véhicule et validez avec la carte-clé (lien dans la configuration du plugin ou dans **Appairer ma clé**). |
| **Véhicule hors de portée — …** | Le proxy ne trouve pas le véhicule en Bluetooth. La **Présence véhicule** passe à 0. | Rapprochez le Raspberry Pi du véhicule ; vérifiez que le proxy a le Bluetooth pour lui seul et que le véhicule n'a pas déjà 3 appareils connectés. |
| **Véhicule non branché / hors de portée du proxy / Charge terminée / La borne ne fournit pas de courant : ajustement selon le surplus ignoré** ou **État de charge inconnu : lancez Rafraîchir (avec réveil)** | Le pilotage selon le surplus n'a envoyé aucune commande pour cette raison (voir [Pilotage selon le surplus](#pilotage-selon-le-surplus)). | Branchez le véhicule, rapprochez le proxy, ou lancez **Rafraîchir (avec réveil)** pour l'état inconnu. |
| **Véhicule non branché / La borne ne fournit pas de courant : charge aux heures creuses en attente** (éventuellement suivi de **(état lu à HH:MM, véhicule endormi)**) ou **État de charge inconnu : lancez Rafraîchir (avec réveil)** | La charge aux heures creuses n'a envoyé aucune commande pour cette raison. Suffixe « véhicule endormi » : l'état affiché date de la dernière lecture avant son endormissement et peut être périmé. | Branchez le véhicule, ou lancez **Rafraîchir (avec réveil)** pour un état inconnu ou périmé (voir [Charge aux heures creuses](#charge-aux-heures-creuses)). |
| **Charge aux heures creuses suspendue jusqu'à la prochaine plage : charge relancée hors du pilotage** | La charge a été relancée depuis l'application Tesla après l'arrêt au SoC cible : Jeedom ne l'interrompt plus. | Rien à faire : le pilotage reprend à la plage suivante. |
| **Charge aux heures creuses suspendue jusqu'à la prochaine plage : échecs de commande répétés** | Trois commandes de suite ont échoué (voir le message d'erreur de la commande dans le log, avertissement). | Corrigez la cause (clé, portée, proxy) ; un débranchement suivi d'un rebranchement relance le pilotage, sinon il reprend à la plage suivante. |
| **Charge démarrée par Jeedom mais arrêtée ou non démarrée : aucun nouvel essai avant la prochaine plage** | Une charge démarrée par Jeedom n'a pas été constatée (arrêtée depuis l'application, borne qui refuse, démarrage trop lent). **Aucun nouvel essai** n'est fait pour ne pas réveiller le véhicule en boucle. | Vérifiez la borne et le véhicule ; démarrez la charge à la main si besoin (cela suspend le pilotage jusqu'à la plage suivante). |
| **Véhicule non branché : préconditionnement planifié non lancé** (éventuellement suivi de **(état lu à HH:MM, véhicule endormi)**) ou **État de charge inconnu : lancez Rafraîchir (avec réveil)** | Avec l'option **Seulement si branché**, le préconditionnement planifié n'a pas démarré la climatisation pour cette raison. Le message d'état inconnu apparaît aussi, même sans l'option, quand l'état de la climatisation du véhicule éveillé est inconnu. | Branchez le véhicule, décochez l'option, ou lancez **Rafraîchir (avec réveil)** pour un état inconnu ou périmé (voir [Préconditionnement planifié par Jeedom](#préconditionnement-planifié-par-jeedom)). |
| **Préconditionnement planifié suspendu jusqu'au prochain départ : rôle Owner requis pour la clé du proxy** | Le véhicule a refusé **Démarrer le climatiseur** : la clé du proxy a probablement le rôle Charging Manager. Un seul essai est fait par départ. | Appairez une clé **Owner** (voir [Rôle de la clé](#rôle-de-la-clé)) ; le pilotage reprend au départ suivant. |
| **Préconditionnement planifié suspendu jusqu'au prochain départ : échecs de commande répétés** | Trois commandes de suite ont échoué (voir le message d'erreur de la commande dans le log, avertissement). | Corrigez la cause (clé, portée, proxy) ; le pilotage reprend au départ suivant. |
| **Demande refusée par le véhicule : clé du proxy non appairée avec ce véhicule** | La clé active du proxy n'est pas appairée avec ce véhicule (avec plusieurs véhicules, la même clé doit être appairée sur chacun). Les autres véhicules ne sont pas touchés. | Utilisez **Appairer ma clé** puis **Vérifier l'appairage** sur l'équipement de ce véhicule. |
| **Demande refusée par le véhicule — …** | Le véhicule a refusé la lecture ; la raison du proxy suit le message. | Lisez la raison indiquée après le message ; vérifiez aussi l'appairage de la clé. |
| **Fonction non supportée par ce proxy — …** | La lecture demandée n'existe pas dans votre version du proxy (par exemple le kilométrage `drive_state` demandé à un proxy qui le refuse). | Mettez le proxy à jour (proxy du fork pour les données étendues : voir [Données étendues : ce qui est disponible](#données-étendues--ce-qui-est-disponible)). |
| **Réponse invalide du proxy** | Le proxy a renvoyé une réponse inattendue. | Vérifiez l'adresse, mettez le proxy à jour, redémarrez-le si cela se répète. |
| **Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour** | Le proxy est antérieur à 2.1.1 : l'état du véhicule n'est plus lisible. | Mettez le proxy à jour (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)). Le log signale aussi cette ligne en erreur. |
| **Proxy occupé : lecture du véhicule non effectuée, réessayez dans un instant** | Un **Rafraîchir** a attendu plus de 110 secondes : le proxy était occupé par une commande ou une lecture. Aucune lecture n'a eu lieu. | Relancez **Rafraîchir** dans un instant ; la lecture automatique suivante rattrape aussi. |
| **Rafraîchissement avec réveil en échec : …** | La commande **Rafraîchir (avec réveil)** a échoué : la cause (véhicule hors de portée, proxy injoignable, véhicule qui refuse de se réveiller…) suit le message. Les informations de charge et de climatisation gardent leur dernière valeur (**Présence véhicule** passe à 0 si le véhicule est hors de portée). | Lisez la cause indiquée ; rapprochez le Raspberry Pi du véhicule si besoin, puis relancez. |
| **Délai dépassé pendant le réveil du véhicule : il a pu se réveiller, relancez dans un instant** | Le réveil et la lecture ont dépassé 75 secondes. Le véhicule a pu se réveiller malgré tout. | Relancez **Rafraîchir (avec réveil)** dans un instant. |
| **Le VIN n'est pas configuré pour cet équipement** | La VIN de l'équipement est vide. | Renseignez la VIN dans l'équipement puis sauvegardez. |
| **URL invalide : …** | L'URL du proxy est vide ou invalide dans la configuration du plugin. | Renseignez-la (voir [Configuration du plugin](#configuration-du-plugin)). |

Le texte est tronqué à 127 caractères. Un véhicule qui dort n'est pas une erreur : voir [Rafraîchissement des informations](#rafraîchissement-des-informations).

### Erreur à l'envoi d'une commande

Ces messages s'affichent en rouge dans Jeedom et sont aussi copiés dans **Dernière erreur**.

| Message | Cause | Action |
|---|---|---|
| **« Cette commande nécessite une clé de rôle Owner : la clé du proxy a probablement le rôle Charging Manager… »** | Le véhicule a refusé faute de droits une commande réservée au rôle Owner (verrouillage, déverrouillage, klaxon, feux, sentinelle, coffres, climatisation) : votre clé a très probablement le rôle Charging Manager. | Voir [Rôle de la clé](#rôle-de-la-clé) : appairez une clé Owner. |
| **« Commande refusée par le véhicule (rôle de la clé du proxy insuffisant ?) : … »** | Défaut d'autorisation sur une autre commande : rôle de clé insuffisant ou état du véhicule. | Voir [Rôle de la clé](#rôle-de-la-clé) ; avec une clé Owner, vérifiez l'état du véhicule. |
| **« Commande refusée par le véhicule : … »** | Le véhicule a refusé la commande ; la raison renvoyée suit le message. | Corrigez selon la raison indiquée. |
| **« Proxy injoignable, commande non envoyée »** | Le proxy ne répond pas : la commande n'est pas partie. | Vérifiez l'URL et l'alimentation du Raspberry Pi. |
| **« Délai dépassé : la commande a pu être exécutée, vérifiez l'état du véhicule »** ou **« Liaison avec le proxy interrompue : la commande a pu être exécutée… »** | Le véhicule a peut-être exécuté la commande malgré tout. | Contrôlez l'état du véhicule avant de la renvoyer. |
| **« Proxy occupé : commande non envoyée, réessayez dans un instant »** | Une autre commande ou lecture occupe le proxy depuis près de 2 minutes. | Réessayez. |
| **« Coffre déjà ouvert ou en mouvement : commande non envoyée »** | Avant d'ouvrir le coffre arrière, le plugin l'a lu ouvert, entrouvert ou en mouvement : une commande de bascule le refermerait peut-être. | Rien à faire : fermez le coffre si besoin, puis relancez l'action (voir [Ouvrir le coffre arrière et le frunk](#ouvrir-le-coffre-arrière-et-le-frunk)). |
| **« État du coffre inconnu : commande non envoyée »** | Le véhicule ne donne pas d'état exploitable pour le coffre arrière : le plugin n'envoie rien par prudence. | Relancez **Rafraîchir** puis l'action ; si l'état reste inconnu, ouvrez le coffre à la main. |
| **« État du coffre illisible, commande non envoyée : … »** | La relecture de l'état avant l'ouverture a échoué : la cause suit le message. | Corrigez la cause (proxy, portée Bluetooth) et relancez. |
| **« Valeur invalide : le courant doit être un entier entre … et … A »** | Le courant est décimal, texte ou hors des bornes Min/Max de la commande. | Corrigez la valeur. Le **Max** suit le courant maximal annoncé par le véhicule ; pour le figer plus haut, réglez-le à la main (le véhicule pourra refuser la consigne). |
| **« Valeur invalide : la limite doit être un entier entre X et Y % »** | Limite hors des bornes de la commande (celles du véhicule, ou 50 à 100 % tant qu'il n'en a pas publié) ou non entière. | Corrigez la valeur. |
| **« Valeur invalide : le mode sentinelle doit être activé ou désactivé »** | Valeur autre que **Activé** ou **Désactivé** (l'ancienne option « Aucun » n'existe plus). | Utilisez **Activé** ou **Désactivé**. |
| **« Valeur invalide : le niveau de chauffage doit être un entier entre 0 et 3 »** ou **« Valeur invalide : le chauffage du volant doit être 0 (arrêt) ou 1 (marche) »** | Un scénario envoie une valeur hors de la liste de la commande de chauffage d'un siège ou du volant. | Utilisez les niveaux de la liste (voir [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant)). |
| **« Valeur invalide : le dégivrage maximal doit être 0 (arrêt) ou 1 (marche) »** | Un scénario envoie une valeur hors de la liste de la commande **Dégivrage maximal**. | Utilisez 0 (Arrêt) ou 1 (Marche) (voir [Dégivrage maximal](#dégivrage-maximal)). |
| **« Valeur invalide : le mode de maintien de climat doit être 0 (arrêt), 1 (maintien), 2 (chien) ou 3 (camp) »** | Un scénario envoie une valeur hors de la liste de la commande **Mode de maintien de climat**. | Utilisez 0 (Arrêt), 1 (Maintien), 2 (Mode chien) ou 3 (Mode camp) (voir [Mode chien, camp et maintien de climat](#mode-chien-camp-et-maintien-de-climat)). |
| **« Échec de la commande : … »** | Autre cause (proxy sans clé, véhicule hors de portée, réponse invalide…) : la cause suit le message. | Voir le tableau **Dernière erreur** ci-dessus. |
| **« Non supportée par votre version du proxy »** | La commande (par exemple **Ouvrir le coffre arrière**, **Ouvrir le frunk**, **Ajouter une programmation de charge**, **Consigne conducteur**, **Régler le chauffage du siège avant gauche**, **Dégivrage maximal** ou **Mode de maintien de climat**) n'existe pas dans votre proxy : rien n'a été envoyé. | Installez le proxy du fork (voir [Programmer la charge](#programmer-la-charge), [Régler la consigne de température](#régler-la-consigne-de-température), [Chauffer les sièges et le volant](#chauffer-les-sièges-et-le-volant), [Dégivrage maximal](#dégivrage-maximal) et [Mode chien, camp et maintien de climat](#mode-chien-camp-et-maintien-de-climat)). |
| **« Valeur invalide : la consigne doit être un nombre entre … et … °C »** | La valeur de **Consigne conducteur** ou **Consigne passager** n'est pas un nombre, ou sort de la plage du curseur (15 à 28 °C, ou les bornes du véhicule). | Envoyez un nombre dans la plage indiquée par le message. |
| **« Jours de la programmation invalides : … »** ou **« Heure de début invalide : … »** | Les jours ou l'heure de **Ajouter une programmation de charge** n'ont pas le format attendu. | Corrigez-les (`lun,mar,mer,jeu,ven` ; `23:00`). |
| **« Coordonnées de Jeedom absentes ou invalides : … »** | La latitude et la longitude de Jeedom ne sont pas renseignées (ou valent 0 et 0). | Renseignez-les dans Réglages, Système, Configuration, onglet **Général**. |
| **« Valeur invalide : la puissance disponible doit être un nombre de watts »** | La valeur envoyée à **Ajuster selon le surplus** n'est pas un nombre (texte, variable vide ou inconnue, calcul qui échoue). | Vérifiez la valeur du scénario : un nombre de watts, par exemple `1800` ; une valeur négative est ramenée à 0 W (voir [Pilotage selon le surplus](#pilotage-selon-le-surplus)). |
| **« Commande non prise en charge par le plugin »** | La commande n'est pas l'une de celles du plugin (commande ajoutée à la main, ou identifiant modifié). | Ne modifiez pas l'identifiant des commandes du plugin. |

### Tâche du cycle de rafraîchissement

Dans **Réglages > Système > Moteur de tâches**, la tâche **TeslaBLE::cycleRafraichissement** (chaque minute, délai de 5 minutes) lance le rafraîchissement des véhicules. Elle est créée à l'activation et à la mise à jour du plugin, et remise en place dans l'heure si elle a été supprimée ; une tâche que vous désactivez vous-même le reste.

- **Plus aucun véhicule n'est rafraîchi** : vérifiez que la tâche existe et qu'elle est activée. Si elle manque, **désactivez puis réactivez le plugin** pour la recréer. Un message d'erreur « Tâche de rafraîchissement non installée » dans le log du plugin signale un échec de création. Un message « Tâche de rafraîchissement non supprimée » à la désactivation du plugin demande de supprimer **TeslaBLE::cycleRafraichissement** à la main dans le moteur de tâches.
- **Désactiver** le plugin supprime la tâche (sans quoi le moteur de tâches journaliserait une erreur chaque minute) ; la réactiver la recrée. Vos équipements, commandes et réglages ne sont pas touchés.
- **Retour à une version antérieure du plugin** (par exemple de la bêta vers la stable) : cette version ne connaît pas la tâche et le log **cron** de Jeedom affiche une erreur « Classe ou fonction non trouvée » chaque minute. Supprimez alors la tâche **TeslaBLE::cycleRafraichissement** à la main dans le moteur de tâches.

### Tâches ponctuelles de relecture

Dans **Réglages > Système > Moteur de tâches**, vous pouvez voir passer des tâches **TeslaBLE::relectureApresCommande** : une par commande réussie (voir [Relecture après une commande](#relecture-après-une-commande)). Elles se suppriment seules une fois la relecture faite ou abandonnée ; n'y touchez pas. Une tâche restée là (Jeedom redémarré pendant l'attente) est retirée par la commande réussie suivante. **Désactiver** le plugin retire toutes ces tâches. Un message « Tâches de relecture non supprimées » dans le log demande de les supprimer à la main.

### Réveil et cadence

| Symptôme | Cause | Action |
|---|---|---|
| **Le véhicule ne s'endort plus** | Une des causes suivantes le garde éveillé : la case **Laisser le véhicule s'endormir** est décochée ; la **Durée de la fenêtre** ne dépasse pas l'intervalle de rafraîchissement (la fenêtre est alors sans effet) ; un occupant ou une clé téléphone proche ; une charge en cours (la fenêtre ne s'ouvre jamais en charge) ; le mode sentinelle ; un autre service qui interroge le véhicule (application Tesla, evcc, autre intégration) ; un intervalle très court ; un scénario qui lance **Rafraîchir (avec réveil)** ou **Réveiller** en boucle. | Cochez la case, choisissez une durée de fenêtre supérieure à l'intervalle, allongez l'intervalle, coupez la sentinelle si possible, vérifiez les scénarios. Passez le log en **Info** : la ligne « fenêtre d'endormissement ouverte pour … min » confirme que la fenêtre s'ouvre ; sinon un des critères ci-dessus l'en empêche. L'effet sur la veille n'est pas garanti : il dépend du véhicule. |
| **Les valeurs de charge et de climatisation ne bougent pas pendant la nuit** | C'est normal : le véhicule dort (le plugin ne le réveille pas) ou la fenêtre d'endormissement est ouverte. **Dernière lecture des données** reste figée et **Âge des données (min)** augmente. **Dernière erreur** reste à **Aucune**. | Rien à faire. Pour des valeurs à jour tout de suite, lancez **Rafraîchir (avec réveil)** (il réveille le véhicule). Si vous voulez des lectures permanentes, décochez **Laisser le véhicule s'endormir**, en acceptant l'impact sur la batterie. |
| **La valeur affichée après une commande est l'ancienne** | Le proxy garde ses données **30 secondes** en cache : la relecture programmée après la commande attend ce délai. Autres causes : le proxy était occupé (relecture abandonnée, la lecture périodique rattrape), le véhicule s'est rendormi (les dernières valeurs sont conservées), le cache du proxy a été allongé au-delà du **Délai de relecture après commande**, ou le moteur de tâches de Jeedom est désactivé. | Patientez 30 secondes. Si le cache de votre proxy est plus long, allongez le **Délai de relecture après commande** d'autant. Sinon lancez **Rafraîchir** (ou **Rafraîchir (avec réveil)** pour un véhicule endormi). Voir [Relecture après une commande](#relecture-après-une-commande). |
| **« Rafraîchissement avec réveil en échec : … »** dans **Dernière erreur** | La cause (véhicule hors de portée, proxy injoignable, véhicule qui refuse de se réveiller…) suit le message. Les valeurs gardent leur dernier état. | Lisez la cause, corrigez-la, relancez. Voir le tableau **Dernière erreur** ci-dessus. |
| **« Délai dépassé pendant le réveil du véhicule : il a pu se réveiller, relancez dans un instant »** | Le réveil et la lecture ont dépassé 75 secondes. | Relancez **Rafraîchir (avec réveil)** dans un instant. |
| **« Proxy occupé : lecture du véhicule non effectuée, réessayez dans un instant »** | Le proxy était occupé par une commande ou une lecture pendant plus de 110 secondes. | Relancez **Rafraîchir** (ou **Rafraîchir (avec réveil)**) dans un instant. |
| **Âge des données (min)** vaut **99999** | Aucune lecture réussie des données n'est connue (équipement neuf, plugin mis à jour, véhicule endormi depuis l'installation). | Lancez **Rafraîchir (avec réveil)** une première fois ; l'information passe à 0. |
| **L'intervalle pendant la charge n'est pas respecté** | L'accélération ne démarre qu'à la première lecture qui voit la charge ; un véhicule endormi en charge, une charge suspendue ou un proxy dont le cache dépasse 60 secondes limitent aussi l'effet (voir [Lecture accélérée pendant la charge](#lecture-accélérée-pendant-la-charge)). | Attendez un intervalle normal, ou lancez **Rafraîchir**. |

Les avertissements du log liés à ces réglages (valeur d'**Intervalle pendant la charge** ramenée à 1 minute ou désactivée, **Délai de relecture après commande** ramené à 30 secondes, cycle plus long que l'intervalle réglé, tâches de rafraîchissement ou de relecture non installées ou non supprimées) sont décrits dans [Messages du log du plugin](#messages-du-log-du-plugin) et [Tâche du cycle de rafraîchissement](#tâche-du-cycle-de-rafraîchissement). Les lignes **Info** d'ouverture et de fin de la fenêtre d'endormissement sont décrites dans [Laisser le véhicule s'endormir](#laisser-le-véhicule-sendormir).

### Messages du log du plugin

- **« Cycle de rafraîchissement sauté : le cycle précédent n'est pas terminé. »** : vous avez lancé la tâche à la main (**Réglages > Système > Moteur de tâches**) pendant qu'un cycle tournait. Jeedom, lui, ne relance jamais de lui-même une tâche en cours (voir les deux messages suivants).
- **« … pilotage selon le surplus : … courant calculé N A, cible M A, décision `…` (motif) »** (Debug) : le détail de chaque appel de **Ajuster selon le surplus** (aucune VIN) ; **« appel ignoré, un ajustement est déjà en cours »** : un autre appel du même véhicule n'était pas terminé. **« pilotage selon le surplus impossible, aucune commande envoyée : … »** (Avertissement, une fois par heure au plus) : panne interne avant l'envoi, par exemple du cache de Jeedom ; le scénario n'est pas interrompu.
- **« … charge aux heures creuses : décision `…` (motif) »** (Info au changement de motif, Debug ensuite ; aucune VIN) : ce que le plugin a décidé après la lecture (`charge_start`, `charge_stop`, `aucune` ou `ignorer`, avec le motif : `demarrage`, `cible_atteinte`, `fin_plage`, `en_charge`, `charge_perimee`, `limite_vehicule`, `suspendue_manuel`…). **« commande `…` en échec (N sur 3) »** (Avertissement au premier échec et à la suspension) ; **« commande `…` reportée au prochain passage (proxy occupé | budget du cycle atteint) »** (Avertissement, une fois par heure au plus) : rien n'a été envoyé, le plugin réessaie à la lecture suivante ; **« pilotage impossible, aucune commande envoyée : … »** (Avertissement, une fois par heure au plus) : panne interne avant l'envoi, par exemple du cache de Jeedom.
- **« Cycle de rafraîchissement de N s, plus long que l'intervalle de rafraîchissement le plus court (M min) : Jeedom a sauté le passage suivant… »** (Avertissement, une fois par heure au plus) : un cycle a duré plus que l'intervalle réglé, en général parce que le proxy ou le Raspberry Pi répond lentement ; la cadence réglée n'est pas tenue. Allongez l'intervalle du véhicule concerné (ou son intervalle pendant la charge), répartissez les véhicules entre plusieurs proxys, ou vérifiez l'alimentation et la connexion Wi-Fi du Raspberry Pi.
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
- **« Véhicule … : fenêtre d'endormissement ouverte pour … min après … lecture(s) inchangée(s), hors charge… »** (Info) : le plugin cesse de lire les données de charge et de climatisation jusqu'à l'heure indiquée ; voir [Laisser le véhicule s'endormir](#laisser-le-véhicule-sendormir). **« fin de la fenêtre d'endormissement après … min : … »** (Info) donne la raison de la reprise (activité constatée avec le champ modifié, commande, rafraîchissement demandé, réglage désactivé, durée écoulée, véhicule hors de portée) ; **« … : véhicule endormi après … min de fenêtre. »** signale que le véhicule s'est endormi. En Debug : « lecture des données suspendue », « lecture de contrôle », « prolongée ».
- **« Véhicule … en charge (Charging), intervalle pendant la charge appliqué : N min au lieu de M. »** et **« Véhicule … : état de charge …, intervalle normal rétabli : M min. »** (Debug) : début et fin de la lecture accélérée, voir [Lecture accélérée pendant la charge](#lecture-accélérée-pendant-la-charge). Un **avertissement** « intervalle pendant la charge inférieur au plancher d'une minute » ou « … invalide, réglage désactivé » signale une valeur corrigée à l'enregistrement.
- **« Véhicule … : relecture programmée dans N s (commande …). »**, **« … : lecture sans réveil. »**, **« Relecture du véhicule … remplacée par une commande plus récente. »**, **« … abandonnée : proxy occupé… »** et **« Relecture ignorée : … »** (Debug) : déroulé d'une relecture après commande, voir [Relecture après une commande](#relecture-après-une-commande). Rien à faire.
- **« Véhicule … : relecture non programmée : … »** (avertissement, une fois par heure au plus) : la tâche de relecture n'a pas pu être créée ; la commande a réussi et les valeurs seront à jour à la lecture suivante. Si le message revient, vérifiez le moteur de tâches de Jeedom.
- **« Équipement … : délai de relecture après commande invalide, ramené à 30 secondes. »** (avertissement) : une valeur hors liste a été enregistrée (par un script, une API ou une restauration) ; choisissez un délai dans la liste de l'équipement.
- **« Véhicule … : le proxy annonce désormais … ; information(s) créée(s) : … »** (Info) : après un changement de version du proxy, le plugin a créé les informations de données étendues devenues disponibles (voir [Données étendues : ce qui est disponible](#données-étendues--ce-qui-est-disponible)). **« … informations de données étendues non créées …, nouvel essai à la prochaine lecture de ces données »** (avertissement, une fois par heure au plus) : la création a échoué (erreur d'enregistrement Jeedom) ; elle est retentée seule, ou par **Sauvegarder** sur l'équipement.
- **« Véhicule … : fonction `donnees:…` refusée par le proxy (not supported), indisponible jusqu'au prochain changement de version du proxy. »** (Info) : le proxy a refusé une catégorie qu'il annonçait ; le plugin ne la demande plus avant une mise à jour du proxy. **« Capacités du proxy du véhicule … : version …, origine …, action(s) indisponible(s) : … »** (Info) : lecture de ce que le proxy annonce, au changement de version.
- **« Lecture de la position (ou des pressions des pneus, ou de la mise à jour logicielle) du véhicule … en échec : … »** (avertissement, une fois par épisode) et **« … rétablie. »** (Info) : le véhicule ou le proxy a refusé cette lecture. Les autres lectures ne sont pas affectées et **Dernière erreur** n'est pas modifiée. En Debug, **« Position (ou Pressions des pneus, ou Mise à jour logicielle) du véhicule … non lue(s) : … »** donne la raison d'une lecture non faite (véhicule endormi, hors de portée, budget de lecture atteint, aucune information sur l'équipement) et **« Position du véhicule … inchangée : … »** celle d'une position ignorée (périmée, 0/0, hors plage) ; aucune coordonnée n'y figure jamais.
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

### Charge avancée : symptômes sans message

Passez le log du plugin en **Debug** : les lignes **« pilotage selon le surplus : … décision … (motif) »** et **« charge aux heures creuses : décision … (motif) »** donnent la raison de chaque décision (voir [Messages du log du plugin](#messages-du-log-du-plugin)).

| Symptôme | Causes possibles | Action |
|---|---|---|
| **Le courant de charge ne change pas** (pilotage selon le surplus) | Le courant visé est identique à la dernière consigne, ou s'en écarte de moins que l'**Hystérésis** (motifs `identique`, `hysteresis`) ; l'**Intervalle minimal entre commandes** n'est pas écoulé (compté depuis la **fin** de la commande précédente) ; le courant visé est ramené au **Max** du curseur **Courant de charge** (borne du véhicule ou valeur réglée à la main) ; le véhicule n'est pas branché, hors de portée ou la charge est terminée (voir **Dernière erreur**) ; **Intervalle pendant la charge** désactivé : l'**État charge** lu est ancien ; la plage de **Charge aux heures creuses** est en cours (l'appel est ignoré) ; **Phases** réglé sur Monophasé avec une borne triphasée. | Lisez la ligne Debug « décision … (motif) » ; réduisez l'hystérésis ou l'intervalle minimal si les changements sont trop rares ; réglez **Intervalle pendant la charge** sur 1 minute ; contrôlez **Tension du réseau** et **Phases** ; vérifiez le **Max** du curseur dans l'onglet **Commandes**. |
| **La charge s'arrête la nuit** (pilotage selon le surplus) | Sans production, la puissance envoyée tombe à 0 W : le courant calculé passe sous le **Seuil d'arrêt** et la charge est arrêtée après la **Durée de maintien avant arrêt**. | Normal. Pour charger la nuit, utilisez la **Charge aux heures creuses** (le pilotage selon le surplus est alors ignoré pendant la plage). |
| **La charge ne redémarre pas le matin** (pilotage selon le surplus) | Le courant calculé n'atteint pas le **Courant minimal de démarrage** ; le démarrage se fait en deux temps (**Courant de charge** puis **Démarrer la charge**, à l'intervalle suivant) ; le véhicule est débranché ou son état de charge est inconnu ; le scénario n'est plus programmé ou sa garde de fraîcheur (**Âge des données (min)**) est fausse. | Contrôlez la puissance envoyée dans la ligne Debug, attendez un ou deux intervalles, vérifiez le scénario. Pour un état de charge inconnu : **Rafraîchir (avec réveil)**. |
| **La charge aux heures creuses ne démarre pas** | La fonction n'est pas cochée ou un champ manque ; l'heure actuelle (**heure de Jeedom**, pas celle du véhicule) est hors de la plage ; le véhicule n'est pas branché, ou la borne ne fournit pas de courant (voir **Dernière erreur**) ; le **SoC cible** est inférieur ou égal au niveau de batterie actuel (cible déjà atteinte) ; la **limite de charge du véhicule** est inférieure ou égale au niveau actuel (charge terminée) ; le pilotage est **suspendu jusqu'à la plage suivante** (action manuelle depuis Jeedom, charge relancée depuis l'application, 3 échecs de commande, ou démarrage déjà tenté sans charge constatée) ; un véhicule endormi n'est vu qu'avec un état périmé ; l'intervalle de rafraîchissement est long (la décision n'est prise qu'à une lecture). | Vérifiez les réglages et le fuseau de Jeedom ; lisez la ligne Info « charge aux heures creuses : décision … (motif) » (par exemple `suspendue_manuel`, `limite_vehicule`, `cible_atteinte`, `hors_plage`) ; relevez **Dernière erreur** ; lancez **Rafraîchir (avec réveil)** pour un état périmé ; un débranchement suivi d'un rebranchement relance un pilotage suspendu après des échecs. |
| **Une commande est refusée ou ignorée** | **Refusée** : **« Cette commande nécessite une clé de rôle Owner… »** ou **« Commande refusée par le véhicule (rôle de la clé du proxy insuffisant ?) … »** (voir [Rôle de la clé](#rôle-de-la-clé) : le pilotage selon le surplus et les heures creuses n'exigent que Charging Manager) ; **« Non supportée par votre version du proxy »** (programmation de charge : proxy du fork requis) ; **« Valeur invalide : … »** (valeur hors bornes ou non numérique). **Ignorée** (aucune erreur, aucune commande) : abstentions du pilotage selon le surplus ou de la charge aux heures creuses (**Dernière erreur** donne la raison : véhicule non branché, hors de portée, charge terminée, borne sans courant, état de charge inconnu) et appel de **Ajuster selon le surplus** pendant la plage des heures creuses. | Voir les tableaux **Dernière erreur** et **Erreur à l'envoi d'une commande** ci-dessus. |

### Climat et confort : symptômes sans message

Passez le log du plugin en **Debug** : la ligne **« préconditionnement planifié : décision … (motif) »** donne la raison de chaque décision du préconditionnement planifié (voir [Messages du log du plugin](#messages-du-log-du-plugin)).

| Symptôme | Causes possibles | Action |
|---|---|---|
| **Une commande de confort est absente du widget** (consigne, sièges, volant, dégivrage maximal, maintien de climat) | Ces commandes sont créées **masquées**, même avec le proxy du fork. | Cochez **Afficher** sur chacune dans l'onglet **Commandes** de l'équipement (voir [Climat et confort : ce qui est disponible](#climat-et-confort--ce-qui-est-disponible)). |
| **La commande est refusée tout de suite avec « Non supportée par votre version du proxy »** | Le proxy ne l'annonce pas : proxy officiel 2.3.0, ou version du fork trop ancienne (`2.3.0-tb.1` au minimum pour la consigne de température, le dégivrage maximal et le maintien de climat, `2.3.0-tb.2` pour les sièges et le volant). | Installez ou mettez à jour le proxy du fork ; aucune réinstallation du plugin n'est nécessaire. Vérifiez **Version du proxy** puis relancez la commande. |
| **La commande est acceptée mais rien ne change** | **Siège** absent du véhicule, accepté sans effet (relu à 0) ; **climatisation coupée** : le chauffage des sièges la demande en principe ; **volant à chauffage automatique** ; **Lire aussi la climatisation** sur **Non, charge seule** : les informations ne sont pas relues et gardent la valeur annoncée ; le véhicule s'est rendormi avant la relecture. | Mettez la climatisation en marche, laissez **Lire aussi la climatisation** sur **Oui**, lancez **Rafraîchir (avec réveil)**, puis relisez la valeur (ces comportements sont à valider en usage réel). |
| **La commande est refusée avec un message de rôle** | Clé du proxy de rôle Charging Manager : le véhicule refuse les actions de confort. | Appairez une clé **Owner** (voir [Rôle de la clé](#rôle-de-la-clé)). |
| **Le préconditionnement planifié ne démarre pas** | Fonction non cochée ; **jour** de départ non coché (c'est le jour de l'heure de départ qui compte) ; **intervalle de rafraîchissement** plus long que la durée de la fenêtre (aucune lecture n'y tombe) ; avec **Seulement si branché**, véhicule débranché ; climatisation **déjà en marche** (motif `deja_active`) ; **Lire aussi la climatisation** sur **Non, charge seule** (refusé à l'enregistrement) ; véhicule hors de portée ou non lu ; pilotage **suspendu** jusqu'au départ suivant (action manuelle depuis Jeedom, 3 échecs de commande, ou clé Charging Manager : un seul essai par départ). | Vérifiez les réglages et le fuseau de Jeedom ; réduisez l'intervalle de rafraîchissement (5 minutes au plus conseillé) ; lisez la ligne **Info** « préconditionnement planifié : décision … (motif) » (par exemple `hors_fenetre`, `deja_active`, `suspendue_manuel`) et **Dernière erreur** ; appairez une clé **Owner** si besoin. |
| **La climatisation démarre en retard ou ne s'arrête pas à l'heure** | La décision n'est prise qu'à une lecture du véhicule : le démarrage et l'arrêt suivent la cadence de lecture. Un véhicule vu endormi ne reçoit jamais d'arrêt. | Réduisez l'intervalle de rafraîchissement ; arrêtez la climatisation depuis Jeedom si besoin. |
| **Un dégivrage maximal ou un maintien de climat ne s'arrête pas** | Le plugin ne les arrête jamais de lui-même ; le préconditionnement planifié ne les remplace ni ne les arrête non plus. | Envoyez **Arrêt** depuis le widget ou un scénario. |

Les messages affichés pour ces fonctions (**Valeur invalide : …**, **Préconditionnement planifié : …**, **Véhicule non branché : préconditionnement planifié non lancé**, **Non supportée par votre version du proxy**) sont décrits dans [Messages à l'enregistrement](#messages-à-lenregistrement), [Information « Dernière erreur » (lecture)](#information--dernière-erreur--lecture) et [Erreur à l'envoi d'une commande](#erreur-à-lenvoi-dune-commande).

### Ouvrants et sécurité : symptômes sans message

Messages de cette fonction : **« Coffre déjà ouvert ou en mouvement… »**, **« État du coffre inconnu… »**, **« État du coffre illisible… »** et **« Non supportée par votre version du proxy »** dans [Erreur à l'envoi d'une commande](#erreur-à-lenvoi-dune-commande) ; le refus d'une durée d'alerte dans [Messages à l'enregistrement](#messages-à-lenregistrement) ; les messages d'alerte dans [Centre de messages de Jeedom (après une mise à jour)](#centre-de-messages-de-jeedom-après-une-mise-à-jour) ; le refus de rôle dans [Rôle de la clé](#rôle-de-la-clé).

| Symptôme | Causes possibles | Action |
|---|---|---|
| **Un ouvrant reste à 0 alors qu'il est ouvert** | Le véhicule dort : l'état n'est pas relu et la dernière valeur reste ; un état inconnu laisse la dernière valeur ; proxy antérieur à 2.3.0 (ouvrants non publiés) ; le proxy transmet les ouvrants comme fermés quand le véhicule ne les fournit pas. | Contrôlez **Âge des données (min)** et **Présence véhicule** ; lancez **Rafraîchir** ; vérifiez **Version du proxy** (voir [Vérifier et mettre à jour la version du proxy](#vérifier-et-mettre-à-jour-la-version-du-proxy)). |
| **Sentinelle en « Dernier ordre » qui ne suit pas l'application** | Proxy officiel 2.3.0 ou fork trop ancien : la valeur est celle du dernier ordre de Jeedom. Avec le fork `2.3.0-tb.2`, un véhicule endormi garde aussi sa dernière valeur lue. | Passez au proxy du fork (`2.3.0-tb.2` au minimum) et lancez **Rafraîchir (avec réveil)** ; voir [État du mode sentinelle](#état-du-mode-sentinelle). |
| **L'alerte ne part pas** | Alerte non activée ou durée vide (refusée à l'enregistrement) ; durée pas encore écoulée (l'alerte part entre la durée et la durée plus deux intervalles de rafraîchissement) ; proxy injoignable, véhicule hors de portée ou lecture en échec (rien n'est évalué) ; trappe de charge ouverte alors que le véhicule est branché ou en charge (aucune alerte pour la trappe) ; présence d'un occupant ou présence inconnue (alerte « déverrouillé sans occupant ») ; cache de Jeedom vidé pendant l'épisode ; scénario qui ne teste pas **Alerte ouvrants** `== 1`. | Vérifiez le bloc **Alertes d'ouverture prolongée**, **Dernière erreur** et **Âge des données (min)** ; voir [Alertes d'ouverture prolongée](#alertes-douverture-prolongée). |
| **Le message d'alerte est toujours dans le centre de messages** | Jeedom ne retire pas le message à la fermeture. | Supprimez-le à la main. |
| **Aucune confirmation ne s'affiche avant une action sensible** | La case **Confirmer l'action** est décochée sur la commande ; l'action est lancée depuis un scénario ou l'API (jamais de confirmation) ; la commande n'est pas l'une des cinq actions concernées. | Cochez la case dans les paramètres avancés de la commande ; voir [Confirmation des actions sensibles](#confirmation-des-actions-sensibles). |
| **Le coffre n'apparaît pas sur le widget** | **Ouvrir le coffre arrière** et **Ouvrir le frunk** sont créées **masquées**, même avec le proxy du fork. | Cochez **Afficher** dans l'onglet **Commandes** (voir [Ouvrants et sécurité : ce qui est disponible](#ouvrants-et-sécurité--ce-qui-est-disponible)). |
| **Le coffre arrière ne s'ouvre pas** | Un hayon motorisé déjà ouvert est refusé par le plugin pour ne pas le refermer ; le véhicule a refusé faute de droits (**Rôle de clé**) ; proxy officiel 2.3.0. | Lisez **Dernière erreur** et le message affiché ; voir [Ouvrir le coffre arrière et le frunk](#ouvrir-le-coffre-arrière-et-le-frunk). |

### Données étendues : symptômes sans message

Messages de cette fonction : le refus du domicile et du rayon dans [Messages à l'enregistrement](#messages-à-lenregistrement), **« Fonction non supportée par ce proxy — … »** dans [Information « Dernière erreur » (lecture)](#information--dernière-erreur--lecture), les lignes de log dans [Messages du log du plugin](#messages-du-log-du-plugin).

| Symptôme | Causes possibles | Action |
|---|---|---|
| **Kilométrage, Rapport, Vitesse, Puissance, pressions, Mise à jour ou position absents** de l'onglet **Commandes** | Le proxy n'annonce pas la catégorie (proxy officiel 2.3.0, ou version du fork trop ancienne) : les informations ne sont **pas créées**. | Vérifiez **Version du proxy**, installez le proxy du fork (`2.3.0-tb.2` au minimum), attendez un cycle (re-détection) ou **Sauvegardez** l'équipement : voir [Données étendues : ce qui est disponible](#données-étendues--ce-qui-est-disponible). |
| **Les informations existent mais restent vides** | Aucune lecture n'a encore eu lieu : le véhicule dort ou est hors de portée, ou une **fenêtre d'endormissement** est ouverte ; pour les pressions, la mise à jour et la position, moins de 15 minutes depuis la tentative précédente. | Lancez **Rafraîchir (avec réveil)** ; contrôlez **Âge des données (min)** et **Présence véhicule**. |
| **Les informations ne sont plus mises à jour** après être passées au fork | Le proxy a refusé la catégorie (ligne Info « refusée par le proxy (not supported) » dans le log) ; le plugin ne la redemande qu'au prochain changement de version du proxy. | Mettez le proxy du fork à jour ; un changement de version relance la détection. |
| **Kilométrage figé** | Véhicule endormi (aucune lecture, dernière valeur gardée) ou fenêtre d'endormissement ouverte. | Normal. **Rafraîchir (avec réveil)** pour une lecture immédiate. |
| **Pression à 0 ou absente** | Une valeur nulle, négative ou supérieure à 10 bar est ignorée : l'information garde sa dernière valeur, ou reste vide si elle n'a jamais été lue ; le véhicule ne communique pas la pression d'un pneu. | Attendez la lecture suivante, véhicule éveillé ; contrôlez sur l'écran du véhicule. |
| **Vitesse ou Puissance semblent fausses** | Unités supposées (mph et kW), non confirmées ; le proxy étant au garage, ces valeurs ne sont presque jamais significatives. | Comparez avec l'écran du véhicule ; ne vous en servez pas pour une décision critique. |
| **Mise à jour affiche « Inconnue » ou un libellé brut** | Une mise à jour est active sans version rapportée par le véhicule (« Inconnue »), ou le proxy renvoie un statut que le plugin ne connaît pas (affiché tel quel). | Rien à faire ; la version apparaît dès que le véhicule la communique. |
| **Modèle ou Année modèle valent « Inconnu »** | La VIN est vide, ou n'est pas celle d'un Tesla reconnu, ou son 10e caractère n'est pas une année décodable. | Vérifiez la **VIN** de l'équipement et **sauvegardez**. |
| **À la maison reste à 0 (ou n'apparaît pas)** | Avant le premier calcul, la tuile affiche 0 : l'information n'est **jamais écrite** tant que le domicile ou la position sont inconnus. Aucune coordonnée de domicile renseignée et aucune position dans Jeedom ; position jamais lue (proxy officiel, véhicule endormi) ; **Rayon (m)** trop petit. | Renseignez le **domicile** et le **rayon** dans l'équipement, ou la position de Jeedom ; attendez une lecture de la position (15 minutes au plus). Voir [Position et confidentialité](#position-et-confidentialité). |
| **À la maison reste à 1 alors que le véhicule est parti** | Hors de portée Bluetooth, plus aucune position n'est lue : l'information garde sa dernière valeur. | Combinez `À la maison == 1` avec **Présence véhicule** dans vos scénarios. |
| **La position ne se met pas à jour** | Véhicule endormi ou hors de portée ; position jugée trop ancienne (plus d'une heure) ou à 0/0, ignorée ; moins de 15 minutes depuis la lecture précédente ; **Latitude** et **Longitude** supprimées (seule **À la maison** reste calculée). | Lancez **Rafraîchir (avec réveil)** ; contrôlez **Présence véhicule** et **Âge des données (min)**. |
| **La latitude et la longitude apparaissent dans un log de Jeedom** | Le log `event` de Jeedom enregistre chaque nouvelle valeur d'une information, même masquée ; ce n'est pas le log du plugin. | Voir [Position et confidentialité](#position-et-confidentialité) : baissez le niveau du log `event` ou supprimez ces deux informations. |
| **Je ne vois pas Latitude et Longitude sur le widget** | Elles sont créées **masquées** et **non historisées**, volontairement. | Cochez **Afficher** (et **Historiser** si besoin) dans l'onglet **Commandes**. |

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
