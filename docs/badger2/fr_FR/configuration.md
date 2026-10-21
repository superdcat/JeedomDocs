# Configuration du plugin

Après téléchargement du plugin il vous faut l'activer, aucune configuration n'est nécessaire. Vous pouvez vous rendre immédiatement sur la page du plug-in après activation pour gérer les équipements.

La page de configuration du plugin donne aussi accès aux sketches Arduino, aux librairies, et à la
section **Migration depuis Badger** si vous arrivez de l'ancien plugin : voir la
[procédure de migration](migration.md).

## Configuration du matériel

Ce plug-in s'interface avec des Arduino / ESP connectés en réseau exécutants un sketch spécifique. Sur ces Arduino on connecte le lecteur de badge wiegand. Le protocole wiegand permet une longue distance de câble entre l’Arduino et le lecteur.
Les lecteurs de badge doivent supporter au moins un des protocoles wiegand 8,26 ou 34.  Les lecteurs peuvent être RFID (125 KHz) ou NFC (13.56 Mhz) et pourvu ou non d'un clavier a code.
Exemple : <https://www.zkteco.eu/index.php/categories-11/access-control-systems/rfid-external-readers>
Ces lecteurs sont disponibles dans différents designs à bas prix sur les sites chinois ou eBay (Rechercher "wiegand").

![](images/Screen3.png)

Des exemples de sketch Arduino sont fourni (voir la page de configuration du plug-in)

> Les deux sections ci-dessous décrivent les sketchs d'origine (**v0**), qui restent maintenus et fonctionnent avec une Arduino Uno. Pour une nouvelle installation sur Mega 2560 ou ESP (sketch **v1**), voir le [tutoriel pas à pas](debuter.md) et la page [Cartes et sketch v1](cartes-et-sketch-v1.md).

### Arduino + Interface réseau ENC28J

(Testé sur Duemilanove 168/328 et Uno)
Dans ce sketch 2 paramètres sont à définir :  L'adresse IP du serveur Jeedom et le numéro de lecteur sur le réseau (à incrémenter)

Vous pouvez paramétrer le nombre de secondes au bout duquel le lecteur oublie les premiers chiffres tapés. Cela évite de valider un faux code si des chiffres avaient été saisis quelques heures avant...

Enfin, vous pouvez également utiliser 5 entrées analogiques (A1 à A5) pour y connecter des boutons de type poussoir (5 actions différentes). Dans ce cas vous pouvez régler la valeur du threshold (seuil de déclenchement). Le maximum est 1022, mais si vous avez une petite perte de signal liée à la longeur du cable et que le bouton ne déclenche pas toujours l'évènement dans jeedom, vous pouvez réduire un peu cette valeur.

![](images/inosettings_enc28j60.png)

Câblage :

![](images/arduinowiring_enc28j60.png)

Si vous souhaitez utiliser les entrées analogiques il faudra les cabler avec le 5v. Vous pouvez par exemple utiliser le bouton sonnette d'un digicode. Vous devez également connecter le A0 au ground pour que le système n'ai pas de parasites.
Si vous ne souhaitez pas utiliser les entrées analogiques vous pouvez les laisser toutes (A0 à A5) débranchées.

Attention un lecteur RFID nécessite au moins du 9V voir du 12V s’il est muni d'un clavier. Une tension inférieure lui fera perdre en porté de lecture RFID.  Il est fortement déconseillé d'utiliser la broche VIN de l’Arduino pour alimenter le lecteur en cas de branchement en USB vous allez griller votre Arduino.
Le 12V peu être pris en amont de l’Arduino et utiliser une alimentation commune.

### Arduino + Interface réseau W5100 (W5100/W5200/W5500-based devices)

(Testé sur Uno et Mega 2560)
Dans ce sketch 2 paramètres sont à définir :  L'adresse IP du serveur Jeedom et le numéro de lecteur sur le réseau (à incrémenter)

Vous pouvez paramétrer le nombre de secondes au bout duquel le lecteur oublie les premiers chiffres tapés. Cela évite de valider un faux code si des chiffres avaient été saisis quelques heures avant...

Enfin, vous pouvez également utiliser 5 entrées analogiques (A1 à A5) pour y connecter des boutons de type poussoir (5 actions différentes). Dans ce cas vous pouvez régler la valeur du threshold (seuil de déclenchement). Le maximum est 1022, mais si vous avez une petite perte de signal liée à la longeur du cable et que le bouton ne déclenche pas toujours l'évènement dans jeedom, vous pouvez réduire un peu cette valeur.

![](images/inosettings_w5100.png)

Câblage :

![](images/arduinowiring_w5100.png)

Si vous souhaitez utiliser les entrées analogiques il faudra les cabler avec le 5v. Vous pouvez par exemple utiliser le bouton sonnette d'un digicode. Vous devez également connecter le A0 au ground pour que le système n'ai pas de parasites.
Si vous ne souhaitez pas utiliser les entrées analogiques vous pouvez les laisser toutes (A0 à A5) débranchées.

Attention un lecteur RFID nécessite au moins du 9V voir du 12V s’il est muni d'un clavier. Une tension inférieure lui fera perdre en porté de lecture RFID.  Il est fortement déconseillé d'utiliser la broche VIN de l’Arduino pour alimenter le lecteur en cas de branchement en USB vous allez griller votre Arduino.
Le 12V peu être pris en amont de l’Arduino et utiliser une alimentation commune.

### Jeedouino

Pour les utilisateurs de Jeedouino, le sketch de celui-ci peut être facilement modifié pour inclure cette fonctionnalité. Dans ce cas les PIN 2 et 3 ne devront pas être utilisées par Jeedouino.

Un sketch d'exemple est disponible dans la page de configuration du plugin, mais il ne contient pas toutes les fonctionnalités. Il est là pour vous aider à modifier votre sketch Jeedouino.

## Configuration des équipements

La configuration des équipements Badger est divisée en 4 sections : Configuration générale, Lecteurs, Badges et Codes.

![](images/Screen1.png)

### Configuration générale

La configuration générale dispose d'un raccourci vers la page de configuration/installation du plug-in, un lien vers la documentation, et un bouton pour activer ou désactiver le mode inclusion.
Le mode inclusion permet d'ajouter automatiquement un nouveau lecteur de badge ou d'enregistrer un nouveau badge.

Pour ajouter un nouveau lecteur de badge, il faudra donc suivre la procédure suivante :

- Configurer l’Arduino (cf. chapitre configuration du matériel)
- Activer le mode inclusion sur Jeedom
- Utiliser le nouveau lecteur de badge avec un badge.
Le nouveau lecteur apparaitra alors dans la liste des lecteurs (un rechargement de la page peut être nécessaire)
Sélectionnez ce nouveau lecteur pour le configurer (cf. chapitre suivant)

<a id="inclusion"></a>
#### Section « Inclusion »

Le mode inclusion est une **fenêtre limitée dans le temps** : il s'arrête tout seul à l'échéance, même si vous fermez la page ou si Jeedom redémarre. Tant qu'il est actif, un bandeau de la page du plugin affiche « Inclusion active, fin dans … » (compte à rebours) et le nombre de créations par rapport à la limite, avec deux boutons :

- **Prolonger** : relance l'inclusion pour la même durée. Le compteur de créations **n'est pas remis à zéro**.
- **Arrêter l'inclusion** : ferme la fenêtre immédiatement.

Chaque création est écrite dans le log et signalée dans le centre de messages (une notification regroupée par inclusion). Les réglages se trouvent dans la configuration du **plugin**, bloc **Inclusion**, avec l'état de l'inclusion et un bouton d'arrêt. La case « Autoriser l'inclusion de devices inconnus » n'existe plus : l'inclusion se démarre uniquement par le bouton **Mode inclusion** de la page du plugin.

| Champ | Défaut | Rôle |
|---|---|---|
| Durée de l'inclusion (minutes) | 5 | Durée de la fenêtre, de 1 à 60. |
| Nombre maximal de créations par inclusion | 20 | De 0 à 1000. Au-delà, les lecteurs et badges inconnus ne sont plus créés jusqu'à la fin de l'inclusion (avertissement dans le log et notification) ; l'inclusion reste ouverte. **0 supprime la limite : à éviter.** |
| Approbation obligatoire des créations | Désactivée | Voir ci-dessous. |

**Approbation obligatoire** : si vous cochez cette option, chaque lecteur ou badge créé par l'inclusion est marqué « En attente d'approbation » et listé sur la page du plugin. **Approuver** l'active ; **Refuser** le supprime. Un lecteur en attente **ne crée pas de badge**, même à son premier appel : approuvez d'abord le lecteur, puis présentez le badge (enrôlement en deux temps). Sans l'option, un élément créé reste, comme avant, **inactif** jusqu'à ce que vous cochiez **Activer** sur sa fiche.

L'acceptation de la nouvelle adresse IP d'un lecteur « le temps d'un appel en inclusion » ne vaut que pendant la fenêtre.

Une inclusion qui était active avant la mise à jour du plugin est arrêtée par la mise à jour (un message du centre de messages le signale) : relancez-la au besoin.

<a id="blocage-des-lecteurs"></a>
#### Section « Blocage des lecteurs »

Ces réglages se trouvent aussi sur la page de configuration du **plugin** et valent pour tous les lecteurs. Les limites d'essais et le temps de blocage de départ se règlent lecteur par lecteur (voir [Configuration des lecteurs](#configuration-des-lecteurs)). Une valeur hors bornes est remplacée silencieusement par la valeur par défaut.

| Champ | Défaut | Rôle |
|---|---|---|
| Durée maximale de blocage (minutes) | 60 | Plafond du blocage, de 1 à 1440. Après une période calme de cette durée, le blocage repart de sa valeur de départ. |
| Échecs cumulés avant blocage | 10 | Nombre de badges inconnus et de codes faux cumulés dans la fenêtre, de 1 à 1000, qui bloque le lecteur même si des badges ou codes valides sont passés entre-temps. |
| Fenêtre des échecs cumulés (minutes) | 10 | Durée pendant laquelle un échec compte dans cette limite, de 1 à 1440. |

**Attention : la valeur 0 désactive la limite globale.** C'est alors la seule protection contre quelqu'un qui détient un badge ou un code valide et qui intercale ses essais entre deux présentations valides : à éviter.

<a id="controle-ip-origine"></a>
#### Option « Contrôler l'IP d'origine des lecteurs »

Cette option se trouve sur la page de configuration du **plugin** (Plugins > Gestion des plugins > Badger Fork), pas sur la page des équipements. Elle est **activée par défaut** et nous vous recommandons de la laisser ainsi.

Quand elle est activée, le plugin refuse les appels qu'un lecteur relié directement à votre réseau ne peut pas émettre :

- un appel qui vient d'une adresse non locale (Internet, par exemple) ;
- un appel relayé par un tunnel ou un reverse proxy (le plugin repère les en-têtes que ces relais ajoutent) ;
- un appel d'un lecteur dont la case « Refuser les appels venant d'une autre IP » est cochée et qui vient d'une autre adresse que son IP autorisée, ou de l'adresse de Jeedom lui-même (voir [Configuration des lecteurs](#configuration-des-lecteurs)).

Cette case par lecteur n'a d'effet que si l'option est activée.

**Quand la décocher** : seulement si vos lecteurs eux-mêmes joignent Jeedom à travers un reverse proxy ou un NAT. Leur adresse d'origine n'est alors pas la leur, et leurs appels seraient refusés.

**Quand ne PAS la décocher** : si Jeedom est publié par un tunnel ou un accès distant (cloudflared, accès distant Jeedom…). Les lecteurs n'empruntent pas ce tunnel : ne désactivez rien, c'est justement ce que l'option bloque.

Tant que l'option est décochée, un bandeau rouge s'affiche : « Le contrôle d'IP d'origine est désactivé : n'importe quel appareil du réseau, ou d'Internet si Jeedom est publié par un tunnel, peut se faire passer pour un lecteur. » Le bandeau apparaît ou disparaît dès que vous cochez ou décochez la case ; sauvegardez ensuite la configuration.

> L'option ne concerne que les lecteurs **v0** (sketch d'origine). Les lecteurs **v1** sont toujours limités à leur IP, option cochée ou non.

### Configuration des lecteurs

La configuration des lecteurs permet d'ajuster certains paramètres du lecteur. Elle doit être effectuée et sauvegardé après chaque ajout de nouveau lecteur.

![](images/Screen2.png)

- Le nom de l'équipement dans jeedom.
- L'objet parent jeedom (optionnel).
- Activer / Désactiver (un lecteur désactivé sera ignoré par le plug-in).
- Visible / Invisible (dans jeedom)
- ID (ce paramètre ne peut pas être changé) Cette ID est composé du mot BADGER et du numéro de lecteur défini dans le sketch Arduino.
- **IP autorisée** : l'adresse d'où viennent les appels de ce lecteur, telle que Jeedom la voit. Elle se renseigne à la création du lecteur et peut être modifiée ici (par exemple après une réservation DHCP). Laissez le champ vide ou saisissez une adresse IPv4 ou IPv6. Ces adresses sont refusées à la sauvegarde, car ce ne sont jamais celles d'un lecteur : `127.0.0.1` (et tout `127.x.x.x`), `::1`, `0.0.0.0`, `::` et l'adresse de Jeedom lui-même. Un lecteur v0 non verrouillé met cette adresse à jour à chaque appel.
- **Refuser les appels venant d'une autre IP** (décochée par défaut) : hors mode inclusion, un appel de ce lecteur qui vient d'une autre adresse que l'IP autorisée est refusé et écrit dans le log. À réserver à un lecteur à **IP fixe** (réservation DHCP dans votre box) : sinon ses appels seront refusés dès que son adresse changera. Pour accepter une nouvelle adresse, activez le mode inclusion le temps d'un appel du lecteur (redémarrage ou badge), ou corrigez l'IP autorisée à la main. **Ne cochez pas cette case pour un lecteur dont les appels passent par un relais installé sur Jeedom** : ils seraient refusés. Cette case concerne les lecteurs v0 et n'a aucun effet si l'option « Contrôler l'IP d'origine des lecteurs » est décochée dans la configuration du plugin.
- Le model détermine la liste des fonctionnalités du lecteur et les paramètres disponibles pour celui-ci. Un lecteur JeedouinoLAN, ou qui annonce `model=wiegand2`, reçoit son modèle dès sa création en inclusion (pour `wiegand2`, la commande `PinTryLimit` est créée d'emblée).
- **Temps de blocage** : durée du **premier** blocage, en minutes (de 1 à 1440). Pendant ce temps, Jeedom ignore tout appel du lecteur. Elle **double à chaque blocage consécutif** (1, 2, 4, 8 minutes…) sans dépasser la durée maximale réglée dans la configuration du plugin (voir [Blocage des lecteurs](#blocage-des-lecteurs)). Un nouveau lecteur démarre à 1 minute.
- **Limite de badge inconnu** : nombre de badges inconnus consécutifs qui bloque le lecteur (1 ou plus). Un badge connu remet ce nombre à zéro.
- **Limite de code faux** : nombre de codes faux consécutifs qui bloque le lecteur (1 ou plus). Un code valide remet ce nombre à zéro.

Les deux limites valent **3** pour un lecteur créé après la mise à jour. Un lecteur **déjà existant qui n'avait aucune limite enregistrée reçoit 1**, qui était sa valeur effective jusque-là : son comportement ne change pas. Si vous voulez plus de tolérance (3, par exemple), saisissez-la vous-même sur sa fiche. Une limite que vous aviez réglée (5, par exemple) est conservée.

Une valeur **vide, 0 ou négative** est refusée à la sauvegarde, avec un message d'erreur : « Limite d'essais invalide : saisissez un nombre entier supérieur ou égal à 1. » ou « Temps de blocage invalide : saisissez un nombre entier de minutes, de 1 à 1440. » Rien n'est enregistré tant que la valeur n'est pas corrigée.

Sous ces champs, un bloc **Verrouillage** affiche l'état du lecteur :

| Ligne | Signification |
|---|---|
| Verrouillage | « Libre », ou « Verrouillé jusqu'à » suivi de la date et de l'heure de fin du blocage |
| Niveau | Nombre de blocages consécutifs (0 = aucun) ; il fixe la durée du prochain blocage |
| Essais de badge / Essais de code | Échecs consécutifs comptés, rapportés à la limite (par exemple 2 / 3) |
| Échecs récents | Échecs cumulés dans la fenêtre de la limite globale, rapportés à son seuil |

Le bouton **Débloquer** apparaît dès que le lecteur est bloqué ou qu'un compteur n'est pas à zéro. Il remet à zéro les compteurs, le niveau et le blocage, après confirmation. Il est réservé aux administrateurs, et l'action est écrite dans le log (niveau Erreur) avec le nom de l'utilisateur. Désactiver puis réactiver un lecteur remet aussi ses compteurs à zéro.

### Configuration des badges et entrées analogiques

La configuration des badges permet d'ajuster certains paramètres. Elle doit être effectuée et sauvegardé après chaque ajout de nouveau badge.
Les entrées analogiques apparaissent comme des badges.

![](images/Screen4.png)

- Le nom de l'équipement dans jeedom.
- L'objet parent jeedom (optionnel).
- Activer / Désactiver (un badge désactivé sera ignoré par le plug-in).
- Visible / Invisible (dans jeedom)
- Le model est purement informatif. Il sert à mieux les reconnaitre dans l'administration du plugin. Un badge créé en mode inclusion reçoit le modèle « Tag RFID » ; une entrée analogique (Analog1 à Analog5) reçoit « Analog Input ». Les badges déjà créés ne changent pas.
- La valeur (ce paramètre ne peut pas être changé) affiche l'identifiant lu sur le badge en décimal. Pour les entrées analogique, il indique le numéro de l'entrée utilisée

### Configuration des codes

La configuration des codes permet d'ajuster certains paramètres. Elle doit être effectuée et sauvegardé après chaque ajout de nouveau code.

![](images/Screen5.png)

- Le nom de l'équipement dans jeedom.
- L'objet parent jeedom (optionnel).
- Activer / Désactiver (un badge désactivé sera ignoré par le plug-in).
- Visible / Invisible (dans jeedom)
- **Code (masqué)** : le code secret. Il est stocké chiffré et le champ est toujours vide au chargement de la page. Laissez-le vide pour conserver le code actuel. Pour le remplacer, saisissez un nouveau code de 1 à 24 chiffres (4 au moins sont conseillés). Ce code doit être différent de celui de tous les autres équipements code.
- **Voir le code** : affiche le code actuel. Ce bouton est réservé aux administrateurs, et chaque consultation est écrite dans le log.
- **Ajouter une commande info GetPin** : case décochée par défaut. Voir « Génération d'un code temporaire » dans le fonctionnement.

Les codes ne sont pas créés par inclusion automatique. Il faut utiliser le bouton "Ajouter" pour créer un nouveau code. Un nouvel équipement code reçoit un code de 4 chiffres généré automatiquement : cliquez sur **Voir le code** pour le connaître, ou saisissez le vôtre.

Les lecteurs déjà installés n'ont rien à changer : ils envoient le même code qu'avant.

#### Mise à jour du plugin et codes existants

- La mise à jour chiffre les codes déjà enregistrés, sans les modifier.
- Les codes en double, ou vides, hérités d'avant la mise à jour sont signalés dans le centre de notifications de Jeedom. Un code vide continue d'ouvrir quand on valide sur le clavier sans rien saisir, comme avant la mise à jour : corrigez-les en saisissant un nouveau code.
- Un équipement qui avait la commande GetPin la garde, case cochée, et une notification vous invite à la décocher si elle ne vous sert pas.
- La clé de chiffrement est celle de Jeedom. Elle est incluse dans la sauvegarde complète de Jeedom : conservez cette sauvegarde.
- **Retour à une version antérieure du plugin** : restaurez d'abord la sauvegarde Jeedom faite avant la mise à jour. Sinon, les codes n'ouvrent plus rien.
