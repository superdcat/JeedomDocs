# Plugin Tesla BLE

Ce plugin permet de piloter la charge, la climatisation et quelques fonctions de base de vos véhicules **Tesla** depuis Jeedom, **en Bluetooth (BLE)** et sans passer par l'API cloud de Tesla.

Jeedom ne parle pas directement au véhicule : il s'appuie sur un proxy [TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy), installé sur un petit appareil équipé du Bluetooth (un Raspberry Pi Zero W par exemple) placé à portée du véhicule, typiquement dans le garage. Le plugin interroge ce proxy en HTTP sur votre réseau local.

```
Jeedom  --HTTP-->  TeslaBleHttpProxy (Raspberry Pi)  --Bluetooth-->  Véhicule
```

## Prérequis

- Jeedom 4.4 minimum, Debian 10 à 12.
- Un proxy **TeslaBleHttpProxy** installé, fonctionnel et joignable depuis Jeedom.
- La **clé du proxy appairée avec le véhicule**. Cette étape se fait entièrement dans l'interface de TeslaBleHttpProxy (génération de la clé, puis validation avec votre carte-clé dans le véhicule) : reportez-vous à sa documentation.
- Le **VIN** de chaque véhicule à piloter (visible en bas de l'écran principal de l'application Tesla).

> **Astuce**
>
> Avant de configurer le plugin, vérifiez que le proxy répond en ouvrant dans un navigateur `http://<ip_du_proxy>:<port>/api/1/vehicles/<VIN>/body_controller_state`. Vous devez obtenir une réponse JSON.

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

## Fonctionnement

### Rafraîchissement des informations

Toutes les **5 minutes**, et après chaque commande action, le plugin rafraîchit chaque véhicule actif en deux temps :

1. Il interroge l'état du **contrôleur de carrosserie** (`body_controller_state`). Cette requête ne réveille pas le véhicule. Elle met à jour la présence, le verrouillage et l'état de veille.
2. **Uniquement si le véhicule est réveillé**, il récupère les données complètes (`vehicle_data`) : charge, batterie, autonomie et climatisation.

Le plugin ne réveille donc jamais le véhicule de lui-même, afin de ne pas vider la batterie. Tant que le véhicule dort, les informations de charge et de climatisation conservent leur dernière valeur connue. Pour les actualiser, utilisez la commande **Réveiller**, puis **Rafraichir** quelques secondes plus tard.

Si le véhicule est hors de portée du Bluetooth ou si le proxy ne peut pas le joindre, la commande **Présence véhicule** passe à 0.

### Exécution des commandes

Chaque commande action est transmise au proxy, qui attend la confirmation du véhicule avant de répondre. Un rafraîchissement est ensuite lancé automatiquement. En cas de refus du véhicule, la raison est écrite dans le log du plugin.

## Commandes

### Informations

| Commande | Unité | Description |
|---|---|---|
| Présence véhicule | | 1 si le proxy joint le véhicule en Bluetooth |
| Véhicule réveillé | | 1 si le véhicule est éveillé, 0 s'il dort |
| Verrouillage du véhicule | | 1 si le véhicule est verrouillé |
| Etat Charge | | État de la charge renvoyé par le véhicule (`Charging`, `Stopped`, `Complete`, `Disconnected`...) |
| Charge Batterie | % | Niveau de batterie utilisable |
| Limite Charge | % | Limite de charge configurée |
| Autonomie | km | Autonomie estimée |
| Temps de charge | | Temps restant avant la fin de la charge, au format `HHhMM` |
| Vitesse de Charge | km/h | Autonomie récupérée par heure de charge |
| Tension Chargeur | V | Tension délivrée par la borne |
| Courant de Charge (A) | A | Courant de charge configuré |
| Courant Demande Charge | A | Courant demandé par le véhicule |
| Verrouillage Trappe Charge | | État du verrou du câble de charge |
| Mode Charge Programmée | | Mode de charge programmée |
| Heure Départ Programmée | | Heure de départ programmée |
| Température intérieure | °C | Température dans l'habitacle |
| Température extérieure | °C | Température extérieure |
| Température conducteur | °C | Consigne de climatisation côté conducteur |
| Température passager | °C | Consigne de climatisation côté passager |
| Climatisation activée | | 1 si la climatisation fonctionne |
| Chauffage siège conducteur | | Niveau de chauffage du siège conducteur (0 à 3) |
| Chauffage siège passager | | Niveau de chauffage du siège passager (0 à 3) |
| Chauffage du volant | | 1 si le chauffage du volant est actif |
| Mode dégivrage | | État du dégivrage |

Le niveau de batterie alimente aussi le suivi de batterie de Jeedom (page **Analyse > Equipements**).

### Actions

| Commande | Description |
|---|---|
| Rafraichir | Relance immédiatement la lecture des informations |
| Réveiller | Réveille le véhicule, nécessaire pour lire les données de charge et de climatisation |
| Charge Start | Démarre la charge |
| Charge Stop | Arrête la charge |
| Courant de charge | Règle le courant de charge, de 0 à 32 A |
| Limite de charge | Règle la limite de charge, de 50 à 100 % |
| Démarrer le climatiseur | Lance le préconditionnement |
| Arrêter le climatiseur | Arrête le préconditionnement |
| Ouvrir la trappe de charge | Ouvre la trappe de charge |
| Fermer la trappe de charge | Ferme la trappe de charge |
| Faire clignoter les feux | Fait clignoter les phares |
| Klaxonner | Actionne le klaxon |
| Verrouiller les portes | Verrouille le véhicule |
| Déverrouiller les portes | Déverrouille le véhicule |
| Mode sentinelle | Active ou désactive le mode sentinelle |

Certaines commandes sont masquées par défaut sur le widget (ouverture de la trappe, verrouillage des portes, feux, mode sentinelle...). Vous pouvez les rendre visibles depuis l'onglet **Commandes** de l'équipement.

## Exemples d'utilisation

- **Charge solaire** : dans un scénario, ajustez **Courant de charge** en fonction de la production photovoltaïque.
- **Heures creuses** : déclenchez **Charge Start** au début des heures creuses et **Charge Stop** à leur fin.
- **Préchauffage** : lancez **Réveiller** puis **Démarrer le climatiseur** quelques minutes avant votre départ.
- **Alerte** : recevez une notification si **Verrouillage du véhicule** reste à 0 le soir.

## Dépannage

Passez le log du plugin en niveau **Debug** (**Configuration du plugin > Logs**) pour voir chaque URL appelée et chaque réponse du proxy.

- **« L'URL de base n'est pas définie dans la configuration »** : renseignez l'URL du proxy dans la configuration du plugin.
- **« Le VIN n'est pas configuré pour cet équipement »** : renseignez le VIN dans l'équipement puis sauvegardez.
- **Présence véhicule reste à 0** : le proxy ne joint pas le véhicule. Rapprochez le Raspberry Pi du véhicule et vérifiez dans l'interface du proxy que la clé est bien appairée.
- **Les informations de charge ne bougent plus** : le véhicule dort. C'est le comportement normal, voir [Rafraîchissement des informations](#rafraîchissement-des-informations).
- **Aucune requête n'aboutit** : vérifiez l'URL du proxy, notamment le `/` final, et testez-la depuis un navigateur.
- **« Échec de l'exécution de la commande »** : le véhicule a refusé la commande. La raison renvoyée figure à la suite du message dans le log.
