# Fonctionnement et Utilisation des équipements

Le plug-in n'exécute que très peu de tache en automatique, il met simplement à disponibilité des équipements et des commandes à utiliser dans vos propres scenarios. Des exemples de scenarios sont disponible dans cette documentation.
Les entrées analogiques fonctionnent comme des badges. Pour les paramétrer référez vous à la documentation concernant les badges.

## Fonctions automatiques

En automatique le plug-in va gérer la présentation de codes faux et de badges inconnu en bloquant le lecteur pendant une période donnée. Les paramètres de chaque lecteur ajustent cette fonctionnalité, elle est très importante en termes de sécurité. Elle permet de bloquer une attaque brute du lecteur.
Lorsqu’un lecteur atteint sa limite de code faux, la commande "PinTryLimit" (type info-string) est déclenchée et une erreur est inscrite dans les logs.
Lorsqu’un lecteur atteint sa limite de badges inconnu, la commande "TagTryLimit" (type info-string) est déclenchée et une erreur est inscrite dans les logs.
On peut alors déclencher un scenario sur ces commandes pour prévenir quelqu’un, déclencher une "pré" alarme .. etc.

### Comment fonctionne le blocage

- **Deux compteurs par lecteur** : les badges inconnus et les codes faux se comptent séparément, chacun avec sa limite (voir [Configuration des lecteurs](configuration.md#configuration-des-lecteurs)).
- **Un succès ne remet à zéro que son propre type** : un badge valide remet à zéro le compteur de badges, pas celui de codes (et inversement). Un badge valide suivi d'un code faux, répétés, finit donc par bloquer le lecteur.
- **Les compteurs ne baissent pas avec le temps.** Ils ne retombent qu'à un succès du même type. Après un blocage, ils restent au niveau de la limite : une seule nouvelle erreur, même longtemps après, déclenche un nouveau blocage et un nouvel événement, jusqu'à un succès du même type. C'est le comportement historique du plugin, conservé.
- **Le blocage s'allonge, puis se calme** : chaque blocage consécutif dure le double du précédent, jusqu'au maximum du plugin. Après une période calme de cette durée maximale sans nouvel échec, le blocage repart de sa durée de départ. Seul cet allongement retombe avec le temps.
- **Limite globale** : en plus des deux compteurs, le plugin cumule tous les échecs (badges inconnus et codes faux) sur une fenêtre glissante (10 échecs en 10 minutes par défaut). Elle bloque le lecteur même si des badges ou codes valides sont intercalés. Réglages : [Blocage des lecteurs](configuration.md#blocage-des-lecteurs).
- **Pendant le blocage, tout appel du lecteur est ignoré** : aucun badge ni code n'est examiné, valide ou non, et aucun événement n'est produit. Le log (niveau Erreur) écrit « Lecteur bloqué : appel ignoré » avec le nom du lecteur et l'heure de fin ; le badge ou le code présenté n'y figure jamais.
- **Le lecteur n'est jamais désactivé** par le blocage : il reprend tout seul à l'heure indiquée, ou dès qu'un administrateur clique sur **Débloquer** sur sa fiche.
- **Les commandes** "TagTryLimit" et "PinTryLimit" reçoivent la date et l'heure **à l'entrée dans le blocage**, une seule fois par blocage, pas à chaque appel ignoré. La commande "PinTryLimit" est créée automatiquement au premier blocage sur code si elle n'existe pas encore sur le lecteur.

Le lecteur lui-même n'est pas informé du blocage : le plugin lui répond comme d'habitude.

## Fonctions configurable dans jeedom

### Test de présentation de badge ou code

Lors de la présentation d'un code ou d'un badge connu et actif, la commande "Presentation" (type info-string) est déclenchée, cette commande contient un texte avec le format suivant :  (Date) (Heure) - (Nom du lecteur utilisé)
La commande "BadgerID" (type info-string) est aussi mise à jour avec le nom du lecteur utilisé.

Ces commandes peuvent être utilisées dans un scenario pour déclencher une action (ouverture de porte, désactivation d'alarme ...)
Voici un premier exemple simple :

![](images/Screen6.png)

Ce scenario simple est déclenché par la présentation d'un code ou d'un badge. On peut ajouter d'autres codes ou badge comme déclencheurs.

![](images/Screen7.png)

Ici le scenario test sur quel lecteur le code ou badge a été présenté. Et dans ce cas il pourrait déclencher l'ouverture d'une porte associée à ce lecteur.  Ici je mets juste à jours une variable debug pour la démo.

Un deuxième exemple plus complexe, nous voulons une double authentification badge + code :

![](images/Screen8.png)

Ce scenario simple est déclenché uniquement par la présentation d'un badge précis.

![](images/Screen9.png)

Ici le scenario test sur quel lecteur le code ou badge a été présenté puis attend 20 secondes que le code défini soit entré. Si le bon code n'est pas entré dans les 20 secondes, le scenario est annulé et le badge doit être a nouveau présenté.

### Activation / Désactivation d'un code ou badge

En associant le plug-in agenda, on peut définir une plage horaire pendant laquelle un badge ou code sera actif. En utilisant la fonction activer / désactiver du scenario.

![](images/Screen10.png)

### Génération d'un code temporaire

Les Codes disposent de la commande "ChangePin" pour définir ou générer un nouveau code, et, si vous le demandez, de la commande "GetPin" pour le relire.
La commande "ChangePin" (type message string) a la syntaxe suivante :

| Titre | Message | Description |
| --- | --- | --- |
| "set" | Valeur du nouveau code | Définit un nouveau code (1 à 24 chiffres, unique entre équipements code ; sinon il est refusé) |
| "rnd4" | (vide) | Génère un code aléatoire sûr sur 4 chiffres |
| "rnd6" | (vide) | Génère un code aléatoire sûr sur 6 chiffres |
| "rnd8" | (vide) | Génère un code aléatoire sûr sur 8 chiffres |

Les codes aléatoires conservent leurs zéros initiaux (par exemple « 0042 ») et le code généré est retourné à l'appelant.

La commande "GetPin" (type info string) est **optionnelle**. Elle n'existe que si la case « Ajouter une commande info GetPin » est cochée sur l'équipement code (décochée par défaut). Cochée, la commande est créée non visible et non historisée, et publie le code en clair. Décochée, la commande est supprimée : les scénarios qui la lisent ne la trouvent plus.

**Avertissement de sécurité** : cocher GetPin ou appeler ChangePin avec "set" fait apparaître le code en clair dans les logs et les événements du cœur de Jeedom, que le plugin ne contrôle pas. Préférez "rnd4", "rnd6" ou "rnd8", et le bouton « Voir le code » de la page de l'équipement.

Un scenario possible : pour donner accès temporairement a votre habitation a quelqu'un alors que vous n'avez pas accès a Jeedom :  déclenché par un sms, un scenario génère un code temporaire, l'active et renvoi sa valeur par sms. Le scenario désactive ce code au bout de 1 heure.
Comme il n'est pas possible de créer des nouveaux codes. Au préalable on aura créé un code nommé "temporaire" que l'on aura désactivé.
