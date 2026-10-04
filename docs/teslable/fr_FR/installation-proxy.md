# Installer le proxy BLE sur un Raspberry Pi Zero 2 W

Le plugin Tesla BLE ne parle pas directement à la voiture : il passe par **TeslaBleHttpProxy** (ici l'image du fork maintenu pour ce plugin, voir [Image du fork ou image wimaha](#image-du-fork-ou-image-wimaha)), un petit programme qui tourne sur un appareil équipé du Bluetooth placé près du véhicule. Cette page explique, pas à pas, comment installer ce proxy sur un **Raspberry Pi Zero 2 W**, la carte recommandée, puis comment l'appairer avec la voiture.

```
Jeedom  --Wi-Fi / réseau local-->  Raspberry Pi Zero 2 W (TeslaBleHttpProxy)  --Bluetooth-->  Véhicule
```

Comptez environ une heure, appairage compris. Vous n'avez besoin d'aucune connaissance de programmation, mais vous taperez quelques commandes dans un terminal.

> **IMPORTANT**
>
> Le plugin exige **TeslaBleHttpProxy 2.3.0 minimum**. L'image du fork recommandée ci-dessous (`2.3.0-tb.2`) respecte ce minimum : le plugin ignore le suffixe `-tb.N` du numéro de version.

## 1. Pourquoi un Raspberry Pi Zero 2 W ?

Le Bluetooth d'une Tesla porte à **5 à 10 mètres**. Le proxy doit donc être dans le garage ou tout près de la place de stationnement, alors que Jeedom est souvent ailleurs dans la maison. Un Raspberry Pi Zero 2 W est petit, consomme très peu, et possède le Wi-Fi et le Bluetooth intégrés.

| Caractéristique | Raspberry Pi Zero 2 W |
|---|---|
| Processeur | 4 cœurs ARM Cortex-A53 64 bits à 1 GHz |
| Mémoire | 512 Mo |
| Bluetooth | 4.2, avec Bluetooth Low Energy (BLE) |
| Wi-Fi | 2,4 GHz uniquement (802.11 b/g/n) |
| Alimentation | 5 V, 2,5 A, prise micro-USB |

> **Astuce**
>
> N'achetez pas l'ancien **Raspberry Pi Zero W** (sans le « 2 ») : son processeur ARMv6 n'est plus pris en charge par les versions récentes de Docker, et son adaptateur Bluetooth a tendance à se figer au bout de quelques heures. Un Raspberry Pi 3, 4 ou 5 convient aussi, s'il est à portée du véhicule.

## 2. Matériel nécessaire

- Un **Raspberry Pi Zero 2 W**.
- Une **alimentation 5 V / 2,5 A** micro-USB de qualité, idéalement l'alimentation officielle. Une alimentation trop faible provoque des coupures Bluetooth difficiles à diagnostiquer.
- Une **carte microSD** de 16 Go ou plus, de bonne marque.
- Un **boîtier**, de préférence en plastique : un boîtier métallique réduit la portée radio.
- Un ordinateur avec un lecteur de carte microSD, pour préparer la carte.
- Le **Wi-Fi de votre box en 2,4 GHz** doit capter à l'endroit où vous installerez le Raspberry Pi.

## 3. Choisir l'emplacement

Avant d'installer quoi que ce soit, vérifiez l'emplacement :

1. Le Raspberry Pi doit être à **moins de 5 à 10 mètres** de l'endroit où la voiture se gare, sans mur épais ni porte de garage métallique entre les deux si possible.
2. Il doit recevoir correctement le **Wi-Fi 2,4 GHz** : vérifiez avec votre téléphone à cet endroit.
3. Il lui faut une **prise électrique** à proximité.

## 4. Préparer la carte microSD

On utilise l'outil officiel **Raspberry Pi Imager**, qui configure le Wi-Fi et l'accès à distance avant même le premier démarrage.

1. Téléchargez et installez [Raspberry Pi Imager](https://www.raspberrypi.com/software/) sur votre ordinateur.
2. Insérez la carte microSD dans l'ordinateur et lancez Raspberry Pi Imager.
3. **Modèle** : choisissez **Raspberry Pi Zero 2 W**.
4. **Système d'exploitation** : choisissez **Raspberry Pi OS (other)**, puis **Raspberry Pi OS Lite (64-bit)**. La version « Lite » n'a pas d'interface graphique : c'est voulu, elle laisse plus de mémoire au proxy.
5. **Stockage** : choisissez votre carte microSD.
6. Quand Imager propose de **personnaliser les réglages**, acceptez et renseignez :
   - le **nom d'hôte**, par exemple `teslaproxy` ;
   - un **nom d'utilisateur** et un **mot de passe** (notez-les) ;
   - le **réseau Wi-Fi** (nom et mot de passe) et le **pays du Wi-Fi** (FR) ;
   - le **fuseau horaire** ;
   - dans l'onglet **Services**, **activez SSH** (authentification par mot de passe).
7. Lancez l'écriture, attendez la fin de la vérification, puis retirez la carte.

## 5. Premier démarrage et connexion

1. Insérez la carte dans le Raspberry Pi, posez-le à son emplacement et branchez l'alimentation. Le premier démarrage prend quelques minutes.
2. Trouvez l'**adresse IP** du Raspberry Pi dans l'interface de votre box (liste des appareils connectés, nom `teslaproxy`).
3. **Fixez cette adresse** : dans votre box, créez une **réservation DHCP** (ou « bail statique ») pour le Raspberry Pi. C'est indispensable, car le plugin enregistre cette adresse.
4. Depuis votre ordinateur, ouvrez un terminal (PowerShell sous Windows, Terminal sous macOS ou Linux) et connectez-vous :

   ```
   ssh <utilisateur>@<ip_du_pi>
   ```

   Acceptez l'empreinte la première fois, puis tapez votre mot de passe.

5. Mettez le système à jour :

   ```
   sudo apt-get update && sudo apt-get upgrade -y
   ```

6. Vérifiez que le Bluetooth est actif :

   ```
   bluetoothctl list
   ```

   Une ligne `Controller XX:XX:XX:XX:XX:XX teslaproxy [default]` doit s'afficher. Si rien ne s'affiche, redémarrez le Raspberry Pi (`sudo reboot`) et réessayez.

> **Astuce**
>
> Pour éviter les coupures Wi-Fi, désactivez l'économie d'énergie du Wi-Fi. Repérez le nom de votre connexion avec `nmcli connection show`, puis tapez `sudo nmcli connection modify "<nom_de_la_connexion>" 802-11-wireless.powersave 2` et redémarrez.

## 6. Installer Docker

Le proxy est distribué sous forme d'image **Docker**, ce qui simplifie l'installation et les mises à jour.

1. Installez Docker avec le script officiel :

   ```
   curl -sSL https://get.docker.com | sh
   ```

2. Autorisez votre utilisateur à utiliser Docker :

   ```
   sudo usermod -aG docker $USER
   ```

3. **Déconnectez-vous** (`exit`) puis reconnectez-vous en SSH pour que ce droit soit pris en compte.
4. Vérifiez que Docker fonctionne :

   ```
   docker --version
   ```

## 7. Installer TeslaBleHttpProxy

1. Créez un dossier pour le proxy, avec un sous-dossier `key` qui contiendra la clé du véhicule :

   ```
   cd ~
   mkdir -p TeslaBleHttpProxy/key
   cd TeslaBleHttpProxy
   ```

2. Créez le fichier de configuration :

   ```
   nano docker-compose.yml
   ```

3. Collez-y ce contenu :

   ```yaml
   services:
     tesla-ble-http-proxy:
       image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2
       container_name: tesla-ble-http-proxy
       volumes:
         - ~/TeslaBleHttpProxy/key:/key
         - /var/run/dbus:/var/run/dbus
       restart: always
       privileged: true
       network_mode: host
       cap_add:
         - NET_ADMIN
         - SYS_ADMIN
   ```

   Ces lignes ont chacune un rôle :
   - `image` : l'image du fork, avec un **numéro de version précis** (recommandé : le proxy ne change que lorsque vous le décidez, voir [Mettre à jour l'image du proxy](#mettre-à-jour-limage-du-proxy)). Pour une version plus récente, consultez les [versions publiées](https://github.com/superdcat/TeslaBleHttpProxy/releases) ; `:latest` est possible, mais déconseillé comme réglage par défaut ;
   - `volumes` : le dossier `key` conserve la clé du véhicule en dehors du conteneur, elle survit aux mises à jour ; `/var/run/dbus` donne accès au Bluetooth du Raspberry Pi ;
   - `restart: always` : le proxy redémarre tout seul après une coupure de courant (sans changer d'image : voir [Mettre à jour l'image du proxy](#mettre-à-jour-limage-du-proxy)) ;
   - `network_mode: host`, `privileged` et `cap_add` : le proxy a besoin d'un accès direct au réseau et à l'adaptateur Bluetooth.

4. Enregistrez avec `Ctrl + X`, puis `Y` et `Entrée`.
5. Démarrez le proxy :

   ```
   docker compose up -d
   ```

6. Vérifiez qu'il répond : depuis un navigateur de votre ordinateur, ouvrez `http://<ip_du_pi>:8080/api/proxy/1/version`. Vous devez obtenir une réponse JSON contenant la version (`2.3.0-tb.2` avec l'image ci-dessus) et `"flavor":"superdcat"`.

### Image du fork ou image wimaha

Le proxy est un logiciel libre de **wimaha** ([TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy)). Cette page recommande le **fork** `ghcr.io/superdcat/tesla-ble-http-proxy`, qui reprend ses routes et ses réponses à l'identique : le plugin (et evcc) fonctionnent de la même façon avec l'un ou l'autre, sans rien changer à leur configuration.

Le fork ajoute notamment : une route `/api/proxy/1/capabilities` qui liste ce que le proxy sait faire (et le rôle de la clé active), des commandes et des données supplémentaires, un jeton d'accès facultatif (`apiToken`), le choix de l'adaptateur Bluetooth (`btAdapter`), le réglage de la durée de maintien de la connexion (`connectionTimeout`) et la libération de l'adaptateur Bluetooth au repos (`releaseAdapterWhenIdle`).

> **Astuce**
>
> L'image **wimaha** (`wimaha/tesla-ble-http-proxy`) reste utilisable **en alternative**, à partir de la version 2.3.0 : le plugin fonctionne avec. Il lui manque tout ce qui précède : pas de route `capabilities`, pas de jeton, pas de choix de l'adaptateur Bluetooth ni de réglage du maintien de la connexion. Pour l'utiliser, remplacez simplement la ligne `image:` du fichier `docker-compose.yml` par `image: wimaha/tesla-ble-http-proxy`. Le plugin n'en dépend pas : avec le fork, il lit la route `capabilities` pour savoir d'emblée quelles commandes votre proxy accepte ; avec l'image wimaha, il le découvre à l'usage, quand le proxy refuse une commande.

### Réglages facultatifs

Le proxy accepte quelques réglages, à ajouter dans `docker-compose.yml` sous `container_name`, puis à appliquer avec `docker compose up -d` :

```yaml
    environment:
      - scanTimeout=10
      - logLevel=info
```

| Réglage | Défaut | Quand le changer |
|---|---|---|
| `scanTimeout` | 5 s | Le véhicule n'est **pas toujours trouvé** : passez à 10 ou 15 secondes. |
| `logLevel` | `info` | Mettez `debug` le temps d'un diagnostic. |
| `vehicleDataCacheTime` | 30 s | Durée pendant laquelle le proxy resservit les mêmes données de charge et de climatisation. Gardez la valeur par défaut. |
| `httpListenAddress` | `:8080` | Changez le port seulement s'il est déjà pris ; reportez alors le nouveau port dans l'URL du plugin. |
| `apiToken` | vide (aucune authentification) | Protège le proxy par un jeton : saisissez la **même valeur** dans **Jeton d'API du proxy** (configuration du plugin). Générez-le par exemple avec `openssl rand -hex 32`. Utilisez le même jeton sur tous vos proxys. Voir l'encadré ci-dessous. |
| `btAdapter` | vide (adaptateur par défaut) | Le Raspberry Pi a **plusieurs adaptateurs Bluetooth** (par exemple une clé USB) et le proxy doit utiliser l'un d'eux : `hci0` à `hci15`, en minuscules (par exemple `hci1`). Disponible à partir de `2.3.0-tb.2`. |
| `connectionTimeout` | 29 s | Durée pendant laquelle la connexion Bluetooth reste ouverte après une commande, de 10 à 120 secondes. Le délai se compte **depuis l'ouverture** de la connexion : les commandes suivantes ne le relancent pas. Une valeur plus longue occupe plus longtemps l'un des 3 emplacements Bluetooth du véhicule. Une valeur invalide est remplacée par 29. Disponible à partir de `2.3.0-tb.2`. |
| `releaseAdapterWhenIdle` | `false` | Mettez `true` **seulement** si un autre service du Raspberry Pi doit pouvoir utiliser l'adaptateur Bluetooth quand le proxy ne travaille pas. Chaque première commande prend alors un peu plus de temps. Voir les limites dans les [variables d'environnement du fork](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md#releaseadapterwhenidle). Disponible à partir de `2.3.0-tb.2`. |

> **IMPORTANT**
>
> **Activer `apiToken` avec Jeedom**, dans cet ordre :
>
> 1. ajoutez la ligne `- apiToken=<votre jeton>` dans `docker-compose.yml`, puis `docker compose up -d` ;
> 2. dans Jeedom, **Plugins > Gestion des plugins > Tesla BLE**, saisissez le même jeton dans **Jeton d'API du proxy**, puis **Sauvegarder** ;
> 3. cliquez sur **Tester** : il doit afficher **« Jeton d'API accepté par le proxy »**.
>
> Le jeton : 1 à 256 caractères ASCII imprimables (lettres, chiffres, ponctuation), sans accent ni retour à la ligne. Une fois le jeton actif, le tableau de bord du proxy demande un identifiant dans le navigateur : nom d'utilisateur libre, mot de passe = le jeton. **evcc** ne sait pas envoyer ce jeton : ne l'activez pas si evcc utilise le même proxy. Le jeton circule en clair sur le réseau local : il ne remplace pas l'isolement du réseau (voir [Sécurité](#11-sécurité)).

## 8. Générer la clé et l'appairer avec le véhicule

Le proxy agit comme une clé de voiture supplémentaire. Il faut donc générer cette clé, puis l'autoriser dans le véhicule avec votre **carte-clé** (la carte NFC).

### Choisir le rôle de la clé

| Rôle | Ce qu'il permet | Pour qui |
|---|---|---|
| **Charging Manager** (recommandé) | Lire l'état et les données du véhicule ; réveiller ; démarrer et arrêter la charge ; régler le courant de charge | Usage centré sur la charge (heures creuses, solaire) |
| **Owner** | Toutes les commandes, y compris verrouillage, déverrouillage, klaxon, feux, sentinelle et climatisation | Si vous voulez piloter autre chose que la charge |

Le proxy n'a **aucune authentification par défaut** (le jeton d'API du fork est facultatif) : avec une clé Owner, n'importe quel appareil de votre réseau local peut déverrouiller le véhicule. Ne choisissez Owner que si vous en avez besoin, et lisez la section [Sécurité](#11-sécurité).

### Appairer

1. Ouvrez le tableau de bord du proxy dans un navigateur : `http://<ip_du_pi>:8080/dashboard`.
2. Cliquez sur **Generate** en face du rôle choisi. La clé est créée, enregistrée dans le dossier `key` et activée.
3. Dans **Setup Vehicle**, saisissez le **VIN** du véhicule (17 caractères, visible en bas de l'écran principal de l'application Tesla).
4. **Réveillez le véhicule** : ouvrez l'application Tesla sur votre téléphone ou ouvrez une portière. L'envoi de la clé échoue si la voiture dort.
5. Cliquez sur **Send key**.
6. Dans la voiture, **posez votre carte-clé** sur la console centrale, à l'emplacement de lecture du téléphone. Aucun message n'apparaît à l'écran avant ce geste.
7. Confirmez sur l'écran du véhicule si une demande d'ajout de clé s'affiche.

### Vérifier l'appairage

Ouvrez dans un navigateur `http://<ip_du_pi>:8080/api/1/vehicles/<VIN>/body_controller_state`. Une réponse JSON avec `"result":true` confirme que le proxy joint le véhicule en Bluetooth avec sa clé. Cette lecture **ne réveille pas** la voiture.

## 9. Configurer le plugin

Le proxy est prêt : passez à la [configuration du plugin](index.md#configuration-du-plugin). L'URL à saisir est `http://<ip_du_pi>:8080/`. Le bouton **Tester** de la page de configuration doit afficher la version du proxy.

Ajoutez ensuite un équipement par véhicule avec son VIN, comme décrit dans [Configuration des équipements](index.md#configuration-des-équipements).

## 10. Entretien

| Action | Commande (dans le dossier `~/TeslaBleHttpProxy`) |
|---|---|
| Voir les journaux du proxy | `docker logs --since 12h tesla-ble-http-proxy` |
| Mettre à jour le proxy | Voir [Mettre à jour l'image du proxy](#mettre-à-jour-limage-du-proxy) |
| Télécharger l'image de la version écrite dans `docker-compose.yml` | `docker compose pull` |
| Télécharger l'image du fork à la main | `docker pull ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` (remplacez le numéro) |
| Redémarrer le proxy | `docker compose restart` |
| Redémarrer le Raspberry Pi | `sudo reboot` |

> **Astuce**
>
> **Sauvegardez le dossier `~/TeslaBleHttpProxy/key`** sur un autre appareil, par exemple avec `scp -r <utilisateur>@<ip_du_pi>:TeslaBleHttpProxy/key .` depuis votre ordinateur. Si la carte microSD tombe en panne, il suffira de réinstaller et de remettre ce dossier en place, sans refaire l'appairage.

### Passer de l'image wimaha à l'image du fork

Si votre proxy tourne déjà avec l'image `wimaha/tesla-ble-http-proxy`, changez d'image **sans refaire l'appairage** : la clé reste dans le dossier `key`, que le nouveau conteneur reprend tel quel.

1. Connectez-vous en SSH au Raspberry Pi et placez-vous dans le dossier du proxy :

   ```
   cd ~/TeslaBleHttpProxy
   ```

2. Ouvrez le fichier : `nano docker-compose.yml`. Changez **uniquement** la ligne `image:` :

   ```yaml
       image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2
   ```

   Ne touchez ni à `volumes` ni au reste. Enregistrez avec `Ctrl + X`, puis `Y` et `Entrée`.
3. Téléchargez la nouvelle image et relancez le proxy :

   ```
   docker compose pull && docker compose up -d
   ```

   Le téléchargement peut prendre plusieurs minutes sur un Raspberry Pi Zero 2 W.
4. Contrôlez, dans un navigateur, `http://<ip_du_pi>:8080/api/proxy/1/version` : la réponse doit contenir `"flavor":"superdcat"` et la version `2.3.0-tb.2`.
5. Ouvrez aussi `http://<ip_du_pi>:8080/api/proxy/1/capabilities` : la réponse liste les commandes et les données du proxy, et `key_role` indique le rôle de votre clé (`owner` ou `charging_manager`). Si `key_role` est vide, aucune clé n'est reconnue : vérifiez que le dossier `key` est bien monté.
6. Dans Jeedom, cliquez sur **Tester** dans la configuration du plugin : il affiche la version du proxy. Rien d'autre n'est à modifier côté plugin ni côté evcc.

**Revenir en arrière** : remettez la ligne `image: wimaha/tesla-ble-http-proxy` dans `docker-compose.yml`, puis `docker compose pull && docker compose up -d`. La clé du dossier `key` fonctionne avec les deux images.

### Mettre à jour l'image du proxy

> **IMPORTANT**
>
> Un **redémarrage du Raspberry Pi**, `docker compose restart` ou `restart: always` **ne mettent pas l'image à jour** : Docker relance l'image déjà téléchargée. Une mise à jour est toujours une action volontaire (option 1) ou une tâche planifiée que vous avez créée (option 2).

**Option 1 (recommandée) : un numéro de version précis, mise à jour à la main**

Le proxy pilote votre voiture. Une mise à jour non contrôlée peut changer un comportement au mauvais moment (une charge programmée qui ne démarre plus, par exemple), et le téléchargement prend plusieurs minutes sur un Raspberry Pi Zero 2 W. Gardez donc un tag précis dans `docker-compose.yml` (`image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2`) et mettez à jour quand vous le décidez :

1. Lisez les notes de la nouvelle version sur la page des [versions du fork](https://github.com/superdcat/TeslaBleHttpProxy/releases).
2. Sur le Raspberry Pi, dans `~/TeslaBleHttpProxy`, changez le numéro de version à la fin de la ligne `image:` (`nano docker-compose.yml`).
3. Lancez `docker compose pull && docker compose up -d`.
4. Contrôlez `http://<ip_du_pi>:8080/api/proxy/1/version` : la version affichée doit être la nouvelle. Le dossier `key` est conservé, aucun nouvel appairage.

**Option 2 (facultative) : `latest` et mise à jour automatique la nuit**

Vous acceptez que le proxy suive chaque nouvelle version sans que vous l'ayez lue. À vos risques : une version défectueuse s'installe seule, et le proxy est coupé quelques instants pendant le redémarrage (une commande en cours peut échouer). Si vous la choisissez :

1. Dans `docker-compose.yml`, mettez `image: ghcr.io/superdcat/tesla-ble-http-proxy:latest`.
2. Ouvrez la table des tâches planifiées de votre utilisateur : `crontab -e`.
3. Ajoutez cette ligne, qui met à jour tous les jours à 4 h du matin (remplacez `<utilisateur>` par votre nom d'utilisateur : le chemin doit être **absolu**) :

   ```
   0 4 * * * cd /home/<utilisateur>/TeslaBleHttpProxy && docker compose pull -q && docker compose up -d && docker image prune -f
   ```

   `docker compose pull -q` télécharge la dernière image sans afficher de détail, `docker compose up -d` ne relance le proxy que si l'image a changé, et `docker image prune -f` supprime les anciennes images qui occupent la carte microSD.
4. Enregistrez et quittez. Vérifiez le lendemain `http://<ip_du_pi>:8080/api/proxy/1/version`.

Pour revenir à l'option 1, supprimez la ligne de `crontab -e` et remettez un numéro de version précis.

## 11. Sécurité

- Par défaut, le proxy **n'a ni mot de passe ni chiffrement** : quiconque accède à votre réseau local peut lui envoyer des commandes. Le fork sait demander un jeton (`apiToken`) : activez-le et saisissez-le dans la configuration du plugin (voir [Réglages facultatifs](#réglages-facultatifs)). Le jeton circule en clair sur le réseau : il complète l'isolement du réseau, il ne le remplace pas.
- N'ouvrez **jamais** le port 8080 vers Internet (pas de redirection de port sur la box).
- Si votre box le permet, placez le Raspberry Pi sur un réseau isolé, avec Jeedom comme seul appareil autorisé à le joindre.
- Préférez une clé **Charging Manager** si vous ne pilotez que la charge.
- Changez le mot de passe par défaut de tout appareil de ce réseau et gardez le Raspberry Pi à jour (`sudo apt-get update && sudo apt-get upgrade`).

## 12. Dépannage

| Symptôme | Cause probable | Que faire |
|---|---|---|
| La page `/api/proxy/1/version` ne s'ouvre pas | Proxy arrêté, mauvaise IP ou mauvais port | `docker ps` doit lister `tesla-ble-http-proxy` ; sinon `docker compose up -d`. Vérifiez l'IP dans la box. |
| `bluetoothctl list` n'affiche rien | Bluetooth du Raspberry Pi indisponible | `sudo reboot`. Vérifiez l'alimentation (5 V / 2,5 A). |
| « Vehicle is not in range » ou véhicule pas toujours trouvé | Portée Bluetooth insuffisante | Rapprochez le Raspberry Pi, évitez le boîtier métallique, augmentez `scanTimeout`. |
| L'envoi de la clé ne fait rien | Véhicule endormi, ou carte-clé non posée | Réveillez la voiture, renvoyez la clé, posez la carte sur la console. |
| Certaines commandes sont refusées | Clé **Charging Manager** | Normal pour le verrouillage, le klaxon, les feux, la sentinelle et la climatisation : générez une clé **Owner** si besoin. |
| Coupures régulières après quelques heures | Wi-Fi en économie d'énergie, alimentation faible, ou adaptateur Bluetooth figé | Désactivez l'économie d'énergie Wi-Fi, changez d'alimentation, redémarrez le proxy. |
| Connexions intermittentes avec la voiture | Trop d'appareils Bluetooth connectés | Le véhicule accepte **3 appareils connectés à la fois** (téléphones, montre, proxy). |
| Le conteneur redémarre en boucle (`docker ps` : « Restarting »), le plugin affiche **Proxy injoignable** ; `docker logs tesla-ble-http-proxy` indique `Cannot start with this Bluetooth adapter` | `btAdapter` invalide (autre chose que `hci0` à `hci15` en minuscules) ou adaptateur absent / impossible à ouvrir | Corrigez la valeur ou retirez la ligne `btAdapter`, puis `docker compose up -d`. Cherchez le nom de l'adaptateur avec `bluetoothctl list` ou `hciconfig -a`. |
| Toutes les lectures et commandes échouent avec **« Jeton d'API refusé par le proxy »** (dernière erreur, commande) ; **Tester** affiche « Le proxy exige un jeton d'API » ou « Jeton d'API refusé par le proxy » | `apiToken` est défini dans `docker-compose.yml`, et le plugin n'a pas de jeton ou un jeton différent | Saisissez dans **Jeton d'API du proxy** exactement la valeur de `apiToken`, **Sauvegarder**, puis **Tester**. |
| **« Commande refusée par le véhicule : invalid request body: … »** | Le proxy du fork a refusé le contenu de la commande (clé manquante, mauvais type, valeur hors limites) avant de l'envoyer | Le plugin vérifie ses valeurs avant l'envoi : si cela arrive, relevez le texte après les deux-points (il nomme la clé) et signalez-le avec le log du plugin en Debug. |
| **« Cette commande nécessite une clé de rôle Owner : la clé du proxy a probablement le rôle Charging Manager… »**, ou information **Rôle de clé** à **Charging Manager** | La clé a le rôle **Charging Manager** | Générez et appairez une clé **Owner** (voir [Choisir le rôle de la clé](#choisir-le-rôle-de-la-clé)). Le rôle de la clé active se lit dans `key_role` à l'adresse `http://<ip_du_pi>:8080/api/proxy/1/capabilities`. |
| Le véhicule n'est plus trouvé après l'installation d'un autre logiciel Bluetooth | Ce logiciel occupe l'adaptateur | Le proxy a besoin de l'adaptateur pour lui seul : retirez l'autre service Bluetooth de ce Raspberry Pi. |

## Références

- [TeslaBleHttpProxy, fork superdcat](https://github.com/superdcat/TeslaBleHttpProxy) : le proxy recommandé pour le plugin (README en anglais : commandes, données, dépannage).
- [Variables d'environnement du fork](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md) (en anglais) : détail des réglages facultatifs.
- [Versions du fork](https://github.com/superdcat/TeslaBleHttpProxy/releases) : notes et binaires de chaque version.
- Image Docker `ghcr.io/superdcat/tesla-ble-http-proxy` : image du fork, publiée sur le registre GitHub (`ghcr.io`).
- [TeslaBleHttpProxy de wimaha](https://github.com/wimaha/TeslaBleHttpProxy) : le projet d'origine, utilisable en alternative.
- [Guide d'installation du proxy de wimaha](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md) (en anglais) : source des étapes 6 à 8.
- [Image Docker `wimaha/tesla-ble-http-proxy`](https://hub.docker.com/r/wimaha/tesla-ble-http-proxy) : image de l'alternative wimaha.
- [SDK officiel Tesla `vehicle-command`](https://github.com/teslamotors/vehicle-command) : la bibliothèque sur laquelle repose le proxy (clés, rôles, protocole Bluetooth).
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/) : préparation de la carte microSD.
- [Fiche produit du Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) : caractéristiques et alimentation recommandée.
- [Installation de Docker sur Debian](https://docs.docker.com/engine/install/debian/) : documentation Docker, valable pour Raspberry Pi OS 64 bits (le script `get.docker.com` de l'étape 6 l'automatise).
