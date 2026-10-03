# Installer le proxy BLE sur un Raspberry Pi Zero 2 W

Le plugin Tesla BLE ne parle pas directement à la voiture : il passe par **TeslaBleHttpProxy**, un petit programme qui tourne sur un appareil équipé du Bluetooth placé près du véhicule. Cette page explique, pas à pas, comment installer ce proxy sur un **Raspberry Pi Zero 2 W**, la carte recommandée, puis comment l'appairer avec la voiture.

```
Jeedom  --Wi-Fi / réseau local-->  Raspberry Pi Zero 2 W (TeslaBleHttpProxy)  --Bluetooth-->  Véhicule
```

Comptez environ une heure, appairage compris. Vous n'avez besoin d'aucune connaissance de programmation, mais vous taperez quelques commandes dans un terminal.

> **IMPORTANT**
>
> Le plugin exige **TeslaBleHttpProxy 2.3.0 minimum**. En suivant cette page, vous installez automatiquement la dernière version.

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

3. Collez-y ce contenu, qui reprend la configuration officielle du proxy :

   ```yaml
   services:
     tesla-ble-http-proxy:
       image: wimaha/tesla-ble-http-proxy
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
   - `volumes` : le dossier `key` conserve la clé du véhicule en dehors du conteneur, elle survit aux mises à jour ; `/var/run/dbus` donne accès au Bluetooth du Raspberry Pi ;
   - `restart: always` : le proxy redémarre tout seul après une coupure de courant ;
   - `network_mode: host`, `privileged` et `cap_add` : le proxy a besoin d'un accès direct au réseau et à l'adaptateur Bluetooth.

4. Enregistrez avec `Ctrl + X`, puis `Y` et `Entrée`.
5. Démarrez le proxy :

   ```
   docker compose up -d
   ```

6. Vérifiez qu'il répond : depuis un navigateur de votre ordinateur, ouvrez `http://<ip_du_pi>:8080/api/proxy/1/version`. Vous devez obtenir une réponse JSON contenant la version, **2.3.0 ou plus récente**.

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

## 8. Générer la clé et l'appairer avec le véhicule

Le proxy agit comme une clé de voiture supplémentaire. Il faut donc générer cette clé, puis l'autoriser dans le véhicule avec votre **carte-clé** (la carte NFC).

### Choisir le rôle de la clé

| Rôle | Ce qu'il permet | Pour qui |
|---|---|---|
| **Charging Manager** (recommandé) | Lire l'état et les données du véhicule ; réveiller ; démarrer et arrêter la charge ; régler le courant de charge | Usage centré sur la charge (heures creuses, solaire) |
| **Owner** | Toutes les commandes, y compris verrouillage, déverrouillage, klaxon, feux, sentinelle et climatisation | Si vous voulez piloter autre chose que la charge |

Le proxy n'a **aucune authentification** : avec une clé Owner, n'importe quel appareil de votre réseau local peut déverrouiller le véhicule. Ne choisissez Owner que si vous en avez besoin, et lisez la section [Sécurité](#11-sécurité).

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
| Mettre à jour le proxy | `docker pull wimaha/tesla-ble-http-proxy` puis `docker compose up -d` |
| Redémarrer le proxy | `docker compose restart` |
| Redémarrer le Raspberry Pi | `sudo reboot` |

> **Astuce**
>
> **Sauvegardez le dossier `~/TeslaBleHttpProxy/key`** sur un autre appareil, par exemple avec `scp -r <utilisateur>@<ip_du_pi>:TeslaBleHttpProxy/key .` depuis votre ordinateur. Si la carte microSD tombe en panne, il suffira de réinstaller et de remettre ce dossier en place, sans refaire l'appairage.

## 11. Sécurité

- Le proxy **n'a ni mot de passe ni chiffrement** : quiconque accède à votre réseau local peut lui envoyer des commandes.
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
| Le véhicule n'est plus trouvé après l'installation d'un autre logiciel Bluetooth | Ce logiciel occupe l'adaptateur | Le proxy a besoin de l'adaptateur pour lui seul : retirez l'autre service Bluetooth de ce Raspberry Pi. |

## Références

- [TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy) : le proxy utilisé par le plugin.
- [Guide d'installation officiel du proxy](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md) (en anglais) : source des étapes 6 à 8.
- [Variables d'environnement du proxy](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/environment_variables.md) (en anglais) : détail des réglages facultatifs.
- [Image Docker `wimaha/tesla-ble-http-proxy`](https://hub.docker.com/r/wimaha/tesla-ble-http-proxy) : versions publiées.
- [SDK officiel Tesla `vehicle-command`](https://github.com/teslamotors/vehicle-command) : la bibliothèque sur laquelle repose le proxy (clés, rôles, protocole Bluetooth).
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/) : préparation de la carte microSD.
- [Fiche produit du Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) : caractéristiques et alimentation recommandée.
- [Installation de Docker sur Debian](https://docs.docker.com/engine/install/debian/) : documentation Docker, valable pour Raspberry Pi OS 64 bits (le script `get.docker.com` de l'étape 6 l'automatise).
