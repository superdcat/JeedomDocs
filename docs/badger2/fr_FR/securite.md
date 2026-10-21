# Sécurité de vos lecteurs

Cette page résume ce que le plugin protège, ce qu'il ne protège pas, et ce que vous devez faire (ou ne pas faire) pour garder un contrôle d'accès fiable. Elle renvoie vers le détail : [Configuration](configuration.md), [Référence technique](reference.md), [Fonctionnement](fonctionement.md) et [Dépannage](depannage.md).

> ⚠️ **Un lecteur v0 reste usurpable depuis le réseau local.** Un lecteur v0 est un lecteur flashé avec un sketch d'origine (Arduino Uno W5100 ou ENC28J60, JeedouinoLAN, anciens sketchs de Badger). Il n'authentifie pas ses appels : tout appareil de votre réseau local qui connaît le fonctionnement du plugin peut envoyer de faux appels en son nom. Les protections ci-dessous (filtrage par adresse, blocage après échecs…) rendent l'attaque plus difficile, **elles ne la rendent pas impossible**. Seul un **reflash avec le sketch v1, appairé et signé** y remédie (carte Mega 2560 ou ESP : voir [Cartes et sketch v1](cartes-et-sketch-v1.md)).
>
> ⚠️ **Le code d'un lecteur v0 circule en clair sur le réseau**, du lecteur vers Jeedom. Le chiffrement du code dans Jeedom (voir plus bas) protège ce qui est **enregistré**, pas ce qui est **transmis**. En v1, la signature protège l'authenticité des appels, pas leur confidentialité : le trafic reste en HTTP.
>
> **Vos lecteurs déjà flashés continuent de fonctionner sans reflash**, après la mise à jour comme avant. Rien de ce qui suit ne vous oblige à reflasher.

## Sur cette page

- [Ce que protège chaque mesure](#mesures)
- [Les réglages livrés et leurs valeurs par défaut](#reglages-securite)
- [Mettre à jour sans surprise](#mise-a-jour-sans-surprise)
- [Débloquer un lecteur](#proc-debloquer)
- [Inclure, approuver ou refuser un lecteur ou un badge](#proc-inclusion)
- [Gérer les codes](#proc-codes)
- [Exiger le protocole v1 signé (et le chiffrement)](#proc-exiger-v1)
- [Corriger l'IP d'un lecteur et régler le filtrage](#proc-ip)
- [Sécuriser les dossiers du plugin (Apache, nginx)](#proc-arborescence)
- [Lire le journal pour diagnostiquer un refus](#proc-journal)
- [Que faire d'un lecteur qui reste en v0 ?](#lecteur-v0-durable)

<a id="mesures"></a>
## Ce que protège chaque mesure

Pour chaque mesure : ce qu'elle protège, ce qu'elle **ne** protège **pas**, et ce qui change entre un lecteur v0 et un lecteur v1.

<a id="mesure-filtrage-ip"></a>
### Filtrage par l'adresse d'origine des appels

- **Ce qu'elle protège** : le plugin refuse un appel qui vient d'une adresse non locale (Internet), qui est relayé par un tunnel ou un reverse proxy, ou qui vient de l'adresse de Jeedom lui-même. Pour un lecteur dont vous cochez « Refuser les appels venant d'une autre IP », tout appel venant d'une autre adresse que son **IP autorisée** est refusé.
- **Ce qu'elle ne protège pas** : un appareil de votre réseau local peut toujours émettre un appel qui paraît valide. Pour un lecteur v0 non verrouillé sur son IP, rien ne l'en empêche. Pour un lecteur verrouillé, il doit en plus se faire passer pour l'adresse du lecteur.
- **v0** : l'option « Contrôler l'IP d'origine des lecteurs » s'applique, activée par défaut. La case par lecteur n'a d'effet que si l'option est activée.
- **v1** : le lecteur est toujours limité à son IP, option cochée ou non.
- **Docker, NAT** : derrière un NAT, ou sous Docker avec un proxy intégré, l'adresse que Jeedom voit n'est plus celle du lecteur mais celle du NAT : plusieurs lecteurs peuvent partager la même adresse et le verrou par lecteur ne les distingue plus. **À confirmer** : ce cas n'a pas été essayé sur une installation Docker réelle.
- Détail : [Option « Contrôler l'IP d'origine des lecteurs »](configuration.md#controle-ip-origine). Procédure : [Corriger l'IP d'un lecteur](#proc-ip).

<a id="mesure-validation"></a>
### Validation des entrées et journal

- **Ce qu'elle protège** : un appel v0 qui sort du format émis par les sketchs d'origine (commande inconnue, nom de lecteur ou valeur de badge invalide, IP déclarée invalide, code non conforme) est refusé sans aucun effet : rien n'est créé, aucun compteur ne bouge. Le journal neutralise tout ce qui vient du réseau (retours à la ligne, caractères spéciaux, longueurs excessives) : personne ne peut fabriquer de fausses lignes. Aucun code n'est jamais écrit dans le journal du plugin, et un badge inconnu ou un code faux y apparaît sans sa valeur.
- **Ce qu'elle ne protège pas** : elle vérifie la **forme** d'un appel, pas son **auteur**. Un appel conforme, forgé par un appareil du réseau, est accepté.
- **v0** : tout ce que les sketchs d'origine émettent reste accepté, y compris l'appui sur Entrée seule au clavier.
- **v1** : son contrat a sa propre validation, plus stricte (champs signés).
- Détail : [Appel v0 hors format](depannage.md#appel-v0-hors-format).

<a id="mesure-blocage"></a>
### Blocage après échecs (anti-bruteforce)

- **Ce qu'elle protège** : après trop de badges inconnus ou de codes faux, le lecteur ignore **tout** appel pendant un temps de blocage qui double à chaque blocage consécutif, jusqu'à un maximum. Une limite globale bloque aussi un lecteur dont les échecs s'accumulent dans une fenêtre de temps, même si des badges ou codes valides sont intercalés.
- **Ce qu'elle ne protège pas** : le blocage est par lecteur. Un appareil du réseau qui envoie de faux appels peut **provoquer volontairement** le blocage d'un lecteur légitime (déni de service) : c'est une raison de plus de laisser le filtrage par IP actif. Avec la limite globale à 0, quelqu'un qui détient un code valide peut intercaler ses essais sans jamais être bloqué.
- **v0 et v1** : même mécanisme, mêmes limites.
- Détail : [Comment fonctionne le blocage](fonctionement.md#blocage-fonctionnement). Procédure : [Débloquer un lecteur](#proc-debloquer).

<a id="mesure-pin"></a>
### Codes chiffrés dans Jeedom

- **Ce qu'elle protège** : les codes enregistrés sont **chiffrés**, le champ Code est toujours vide au chargement de la page, et seul un administrateur peut afficher un code par « Voir le code » (chaque consultation est écrite dans le journal). Deux équipements code ne peuvent plus porter le même code. Le générateur (`rnd4`, `rnd6`, `rnd8`) produit des codes aléatoires sûrs.
- **Ce qu'elle ne protège pas** : le code qu'un lecteur v0 envoie reste en clair sur le réseau. Une commande `GetPin` cochée, ou un `ChangePin` avec `set`, écrit le code **en clair dans les journaux et l'historique de Jeedom**, hors de tout contrôle du plugin. Un code vide ou de moins de 4 chiffres reste faible. La clé de chiffrement est celle de Jeedom : sans elle, les codes sont illisibles.
- **v0 et v1** : le chiffrement dans Jeedom est identique. Pour un lecteur v1 appairé, le code est de plus protégé contre le rejeu par la signature.
- **Comparaison des codes** : par défaut, un lecteur v0 compare le code tapé comme un nombre quand les deux valeurs en ont l'allure : `42` ouvre un code `0042`, et `1e3` ouvre un code `1000`. L'option par lecteur « Comparer les codes exactement » supprime ces variantes (voir [Comparer les codes exactement](#proc-comparaison-exacte)). Elle est **décochée par défaut** et ne change rien en v1, qui compare déjà exactement.
- Détail : [Configuration des codes](configuration.md#codes-configuration) et [Génération d'un code temporaire](fonctionement.md#codes-temporaires). Procédure : [Gérer les codes](#proc-codes).

<a id="mesure-inclusion"></a>
### Inclusion bornée et approbation

- **Ce qu'elle protège** : l'inclusion (création automatique de lecteurs et de badges inconnus) dure 5 minutes par défaut puis s'arrête seule, crée 20 équipements au plus, et chaque création est tracée (journal et centre de messages). Avec l'**approbation obligatoire**, chaque élément créé attend votre feu vert. Un élément créé par inclusion est **inactif** tant qu'il n'est pas activé ou approuvé : un badge inclus n'ouvre rien d'office.
- **Ce qu'elle ne protège pas** : pendant la fenêtre, n'importe quel appareil du réseau qui envoie un appel peut créer un équipement (dans la limite des créations). L'approbation obligatoire est **désactivée par défaut**. Pendant l'inclusion, un lecteur peut aussi voir son adresse mise à jour.
- **v0 et v1** : identique.
- Détail : [Section Inclusion](configuration.md#inclusion). Procédure : [Inclure, approuver ou refuser](#proc-inclusion).

<a id="mesure-posture"></a>
### Posture de sécurité par lecteur

- **Ce qu'elle protège** : le tableau « Posture de sécurité des lecteurs » dit, lecteur par lecteur, s'il est en v0 filtré, v0 non filtré, v1 non appairé ou v1 signé, ce qu'il risque et quoi faire. Un lecteur appairé et « exigé v1 signé » refuse tout appel v0 ou non signé. Un lecteur v1 appairé dont l'exigence de chiffrement est posée refuse les badges et codes envoyés en clair.
- **Ce qu'elle ne protège pas** : le tableau lui-même **n'empêche rien**, il informe. Le niveau « v1 non appairé » repose sur ce que le lecteur annonce, non authentifié. Aucune exigence n'est posée par défaut ni en masse.
- **Colonne « Comparaison des codes »** : pour un lecteur v0, elle affiche « Comparaison exacte » ou « Comparaison souple » selon l'option du lecteur (voir [Comparer les codes exactement](#proc-comparaison-exacte)). Elle reste vide pour un lecteur v1. Quand un lecteur v0 est en comparaison souple et qu'au moins un de vos codes commence par un zéro ou contient une lettre de `a` à `f`, la colonne « Recommandation » ajoute « Activer la comparaison exacte des codes ». Ce n'est qu'un **affichage** : rien n'est activé à votre place.
- **v0** : jamais exigible, il faut d'abord reflasher. **v1** : appairage, puis exigence.
- Détail : [Posture de sécurité des lecteurs](reference.md#posture-securite). Procédure : [Exiger le protocole v1 signé](#proc-exiger-v1).

<a id="mesure-relais-migrations"></a>
### Relais de compatibilité et migrations de données

- **Ce qu'elle protège** : à chaque mise à jour, les évolutions de données (chiffrement des codes, limites par défaut, éléments existants non touchés) s'appliquent **une seule fois, dans l'ordre**. Un échec est signalé, nommé dans le journal et retenté. Le relais de l'ancienne adresse que vous avez choisi est rétabli après une mise à jour ou une réactivation du plugin. Une inclusion active avant la mise à jour est arrêtée.
- **Ce qu'elle ne protège pas** : le relais de compatibilité sert les anciens sketchs, qui sont des lecteurs v0 : il ne les rend pas plus sûrs. Désactiver puis réactiver le plugin ne débloque pas les lecteurs.
- **v0 et v1** : sans effet sur les appels des lecteurs.
- Détail : [Évolutions de données à chaque mise à jour](configuration.md#migrations-donnees) et [Migration depuis Badger](migration.md).

<a id="mesure-refacto"></a>
### Remise en ordre interne du code

Une partie de la tranche de sécurité a réorganisé le code du plugin **sans changer son comportement**. Vous n'avez rien à faire et rien à constater.

<a id="mesure-arborescence"></a>
### Fermeture des dossiers internes

- **Ce qu'elle protège** : l'accès direct par une adresse web aux dossiers internes du plugin (documentation de travail, outillage, tests, sketchs, code interne) est fermé **sous Apache**.
- **Ce qu'elle ne protège pas** : **sous nginx, rien n'est protégé tant que vous n'avez pas ajouté une règle** (voir [Sécuriser les dossiers du plugin](#proc-arborescence)). D'autres dossiers (pages du plugin, traductions, documentation) restent joignables ; ils ne contiennent aucun secret.
- **v0 et v1** : l'API des lecteurs reste joignable sur ses deux adresses (`plugins/badger2/…` et l'ancienne `plugins/badger/…`), sans changement pour les lecteurs.
- Détail : [Accès direct aux dossiers internes](configuration.md#acces-direct-dossiers).

<a id="mesure-chiffrement-v1"></a>
### Chiffrement des identifiants sur le canal v1

- **Ce qu'elle protège** : le plugin sait déchiffrer les badges et codes qu'un lecteur v1 appairé enverrait chiffrés, et vous pouvez **exiger** ce chiffrement lecteur par lecteur : les badges et codes envoyés en clair sont alors refusés.
- ⚠️ **Aucun sketch publié n'envoie encore d'identifiants chiffrés.** Aujourd'hui, la colonne « Chiffrement des identifiants » affiche « Non annoncé » pour tous vos lecteurs, et cette protection n'est **pas disponible côté lecteur**. Ne comptez pas dessus.
- **v0** : jamais concerné. **v1** : à venir, **À confirmer** avec un sketch qui émet le chiffrement.
- Détail : [Exiger le chiffrement des identifiants](reference.md#exiger-chiffrement).

<a id="reglages-securite"></a>
## Les réglages livrés et leurs valeurs par défaut

Les réglages communs se trouvent dans **Plugins > Gestion des plugins > Badger Fork** ; les réglages par lecteur sur la fiche de chaque lecteur. Une valeur hors bornes saisie dans la configuration du plugin est remplacée par la valeur par défaut sans message.

| Réglage | Où | Défaut | Valeurs | Pourquoi ce défaut |
|---|---|---|---|---|
| Contrôler l'IP d'origine des lecteurs | Configuration du plugin, Général | **Activé** | coché / décoché | Refuse les appels qu'un lecteur relié directement au réseau ne peut pas émettre. À décocher seulement derrière un reverse proxy ou un NAT. |
| Durée de l'inclusion (minutes) | Configuration du plugin, Inclusion | **5** | 1 à 60 | Une fenêtre courte limite le temps pendant lequel un appareil inconnu peut créer des équipements. |
| Nombre maximal de créations par inclusion | Configuration du plugin, Inclusion | **20** | 0 à 1000 (0 = sans limite, à éviter) | Suffit pour un parc normal et borne les créations en cas d'abus. |
| Approbation obligatoire des créations | Configuration du plugin, Inclusion | **Désactivée** | coché / décoché | Le comportement des lecteurs déjà installés ne change pas. À cocher si vous voulez valider chaque création. |
| Durée maximale de blocage (minutes) | Configuration du plugin, Blocage des lecteurs | **60** | 1 à 1440 | Plafond du blocage progressif. |
| Échecs cumulés avant blocage | Configuration du plugin, Blocage des lecteurs | **10** | 1 à 1000 (0 = désactivée, à éviter) | Bloque un lecteur dont les échecs s'accumulent malgré des succès intercalés. |
| Fenêtre des échecs cumulés (minutes) | Configuration du plugin, Blocage des lecteurs | **10** | 1 à 1440 | Durée pendant laquelle un échec compte dans la limite globale. |
| Temps de blocage (minutes) | Fiche du lecteur | **1** pour un nouveau lecteur | 1 à 1440 | Durée du premier blocage ; elle double à chaque blocage consécutif. |
| Limite de badge inconnu | Fiche du lecteur | **3** pour un nouveau lecteur ; **1** pour un lecteur existant sans limite enregistrée | 1 ou plus | Tolère une erreur de manipulation sans bloquer ; un lecteur existant garde son comportement d'avant. |
| Limite de code faux | Fiche du lecteur | **3** pour un nouveau lecteur ; **1** pour un lecteur existant sans limite enregistrée | 1 ou plus | Idem. |
| IP autorisée | Fiche du lecteur | Renseignée à la création du lecteur | adresse IPv4 ou IPv6, ou vide | Sert de référence au verrou par IP. |
| Refuser les appels venant d'une autre IP | Fiche du lecteur | **Décochée** | coché / décoché | Un lecteur à adresse non réservée serait refusé à chaque changement d'adresse. À cocher pour un lecteur à IP fixe. |
| Ajouter une commande info GetPin | Fiche d'un code | **Décochée** | coché / décoché | La commande publie le code en clair : elle n'existe que si vous la demandez. |
| Comparer les codes exactement | Fiche du lecteur | **Décochée** (y compris pour un lecteur existant) | coché / décoché | Un lecteur v0 déjà en service continue d'ouvrir comme avant (42 ouvre 0042). À cocher lecteur par lecteur, une fois vérifié que chacun tape son code en entier. Sans effet en v1. |
| Exiger le protocole v1 signé | Tableau de posture | **Non exigé** | bouton par lecteur | Un lecteur encore en v0 ne fonctionnerait plus : jamais par défaut, jamais en masse. |
| Exiger le chiffrement des identifiants | Tableau de posture | **Non exigé** | bouton par lecteur | Aucun sketch ne chiffre encore ; même principe que ci-dessus. |

<a id="mise-a-jour-sans-surprise"></a>
## Mettre à jour sans surprise

Ce qui se passe quand vous mettez à jour le plugin vers la version qui contient ces protections :

- **Vos lecteurs déjà flashés fonctionnent sans reflash.** Ils continuent d'appeler la même adresse (l'ancienne `/plugins/badger/…` via le relais si vous l'utilisez, ou `/plugins/badger2/…`), avec les mêmes paramètres.
- **Les noms ne changent pas** : les commandes `BadgerID`, `Presentation`, `TagTryLimit`, `PinTryLimit` et les badges nommés `BADGE <valeur>` restent identiques. Vos scénarios, vues et historiques continuent de s'appliquer.
- **Vos codes sont convertis** : ils sont **chiffrés sans être modifiés**. Les codes en double ou vides sont signalés dans le centre de messages. Un code vide continue d'ouvrir comme avant : corrigez-le à votre rythme.
- **GetPin est conservée là où elle existait** : l'équipement garde la commande, case cochée, et un message vous invite à la décocher si elle ne sert pas. **Les nouveaux codes n'ont pas de GetPin**, sauf si vous cochez la case.
- **Limites par défaut** : un lecteur existant sans limite enregistrée reçoit **1** pour les badges inconnus et les codes faux (sa valeur effective d'avant) ; seuls les lecteurs créés ensuite démarrent à **3**. Saisissez vous-même une valeur plus tolérante si vous le souhaitez.
- **Une inclusion active est arrêtée** : un message du centre de messages le signale ; relancez-la au besoin. Elle dure désormais 5 minutes par défaut.
- **Éléments existants non touchés** : les lecteurs et badges déjà créés restent actifs, sans « attente d'approbation ». Les modèles déjà affichés ne changent pas.
- **Blocage d'un lecteur** : désactiver puis réactiver le plugin, ou le mettre à jour, **ne débloque plus** les lecteurs : utilisez le bouton **Débloquer**.
- **Les 3 boutons de téléchargement des sketchs d'origine** de la configuration du plugin ouvrent désormais leur page sur GitHub (accès à Internet nécessaire).
- **Comparaison des codes** : aucune mise à jour ne coche « Comparer les codes exactement ». Tous vos lecteurs gardent la comparaison d'origine, et `42` ouvre toujours `0042` tant que vous n'avez rien coché.
- **Retour à une version antérieure** : restaurez d'abord la **sauvegarde Jeedom faite avant la mise à jour**, sinon les codes (chiffrés) n'ouvrent plus rien. Si vous remontez ensuite de version, un code que vous avez redéfini en clair entre-temps est chiffré à la prochaine sauvegarde de cet équipement.
- Si une évolution de données échoue, le centre de messages affiche « Une migration de données a échoué : consultez le journal » : voir [Migration de données en échec](depannage.md#migration-donnees-echec).

**Avant de mettre à jour** : faites une sauvegarde complète de Jeedom. Elle contient la clé qui déchiffre vos codes.

<a id="proc-debloquer"></a>
## Débloquer un lecteur

Un lecteur « bloqué » ignore **tous** ses appels (même un badge valide) jusqu'à la fin du blocage. Le journal écrit « Lecteur bloqué : appel ignoré ».

1. Ouvrez **Plugins > Sécurité > Badger Fork** et cliquez sur le lecteur dans la liste **Lecteurs**.
2. Lisez le bloc **Verrouillage** : « Verrouillé jusqu'à » suivi de la date et de l'heure, le **Niveau** (nombre de blocages consécutifs, qui fixe la durée du prochain), les **Essais de badge** et **Essais de code** (rapportés à leur limite) et les **Échecs récents** (rapportés à la limite globale).
3. Deux possibilités : **attendez** l'heure indiquée, ou cliquez sur **Débloquer** (administrateurs seulement) et confirmez. Le message « Lecteur débloqué » s'affiche. Les compteurs, le niveau et le blocage sont remis à zéro, et l'action est écrite dans le journal avec le nom de l'utilisateur.
4. Si le blocage revient vite, c'est normal : un compteur ne baisse pas avec le temps, il ne retombe qu'à un succès du même type. Présentez un badge ou un code valide pour le remettre à zéro. Voir [Comment fonctionne le blocage](fonctionement.md#blocage-fonctionnement).

Le bouton n'apparaît que si le lecteur est bloqué ou si un compteur n'est pas à zéro. **Désactiver puis réactiver le plugin ne débloque pas** les lecteurs. Désactiver puis réactiver **le lecteur** depuis sa fiche remet ses compteurs à zéro. Réglages : [Blocage des lecteurs](configuration.md#blocage-des-lecteurs).

Si « Débloquer » répond « Lecteur occupé, réessayez », deux actions se sont croisées : recliquez.

<a id="proc-inclusion"></a>
## Inclure, approuver ou refuser un lecteur ou un badge

1. Sur la page du plugin, cliquez sur **Mode inclusion**. Un bandeau « Inclusion active, fin dans … » affiche le compte à rebours et le nombre de créations par rapport à la limite.
2. **Lecteur** : redémarrez-le (lecteur v1) ou présentez un badge (lecteur v0). **Badge** : présentez-le à un lecteur **déjà actif et, si l'approbation est obligatoire, déjà approuvé**. Rechargez la page : l'élément est dans sa liste.
3. Sans approbation obligatoire, l'élément créé est **inactif** : ouvrez sa fiche, cochez **Activer** et sauvegardez. Avec l'approbation obligatoire, il apparaît dans la liste **En attente d'approbation** (type, équipement, date de création, lecteur d'origine, valeur) : cliquez sur **Approuver** pour l'activer, ou sur **Refuser** (après confirmation) pour le supprimer avec ses commandes.
4. Cliquez sur **Arrêter l'inclusion** quand vous avez terminé ; sinon elle s'arrête seule à l'échéance (**Prolonger** repart pour la même durée sans remettre le compteur de créations à zéro).

**Pourquoi un badge inclus n'ouvre pas tant qu'il n'est pas approuvé** : un élément créé par l'inclusion est volontairement inactif, car n'importe quel appareil du réseau peut en provoquer la création. Tant qu'il n'est pas activé (ou approuvé), il ne met pas à jour `Presentation` et aucun scénario ne se déclenche. Un lecteur en attente ne crée pas de badge : approuvez d'abord le lecteur, puis présentez le badge. La présentation qui crée un badge ne déclenche rien non plus : présentez-le une seconde fois.

Si l'inclusion s'arrête avant que vous ayez fini, ou si rien n'est créé, voir [Le lecteur n'apparaît pas dans Jeedom](depannage.md#lecteur-absent). Réglages : [Section Inclusion](configuration.md#inclusion).

<a id="proc-codes"></a>
## Gérer les codes

- **Définir ou changer un code par le formulaire (recommandé)** : ouvrez l'équipement code, saisissez le nouveau code dans le champ **Code (masqué)** (de 1 à 24 chiffres, 4 au moins sont conseillés) et sauvegardez. Laissez le champ vide pour garder le code actuel.
- **Voir le code** : cliquez sur **Voir le code** (administrateurs seulement). Chaque consultation est écrite dans le journal, avec le nom de l'utilisateur. Cliquez sur **Masquer le code** pour le cacher.
- **Unicité** : un code doit être différent de celui de tous les autres équipements code, sinon il est refusé (« Ce code est déjà utilisé »).
- **Par scénario**, avec la commande `ChangePin` : titre `rnd4`, `rnd6` ou `rnd8` pour **générer** un code aléatoire de 4, 6 ou 8 chiffres (message vide ; les zéros initiaux sont conservés, et le code généré est retourné à l'appelant), ou titre `set` avec le nouveau code en message pour **définir** un code.
- ⚠️ **Préférez le formulaire ou `rnd4`, `rnd6`, `rnd8` à `set`.** Avec `set`, le code est écrit en clair dans les journaux de Jeedom, que le plugin ne contrôle pas.

### La case « Ajouter une commande info GetPin »

- **Par défaut, elle est décochée** et la commande `GetPin` n'existe pas.
- Cochée, elle crée une commande info `GetPin` (non visible, non historisée) qui **publie le code en clair** : il apparaît dans les journaux d'événements de Jeedom et dans son flux temps réel, hors de tout contrôle du plugin. Ne la cochez que si un scénario en a vraiment besoin.
- Décochée (puis sauvegardée), la commande est **supprimée** : un scénario qui la lisait ne la trouve plus et doit être corrigé. Le formulaire vous prévient avant la suppression.
- **À la mise à jour**, un équipement qui avait déjà `GetPin` la **garde**, case cochée : un scénario qui la lisait continue de fonctionner. Un message vous invite à la décocher si elle ne sert pas. Un code créé après la mise à jour n'en a pas.
- Pour retrouver un code sans `GetPin`, utilisez **Voir le code**.

<a id="proc-comparaison-exacte"></a>
### Comparer les codes exactement (lecteur v0)

Par défaut, un lecteur v0 ouvre aussi avec une **variante** du code : un code `0042` s'ouvre en tapant `42` ou `042`, et un code `1000` en tapant `1e3`. Cette option, **par lecteur**, supprime ces variantes.

- **Décochée (par défaut)** : rien ne change, y compris pour les lecteurs déjà installés. `42` ouvre `0042`, `1e3` ouvre `1000`.
- **Cochée** : un code n'ouvre que s'il est tapé **à l'identique**, caractère pour caractère. `0042` ouvre `0042` ; `42`, `042` ne l'ouvrent plus ; `1e3` n'ouvre plus `1000`.
- **Une variante est un code faux** : elle compte dans les essais de code du lecteur et peut donc mener au blocage, exactement comme n'importe quel code faux (voir [Débloquer un lecteur](#proc-debloquer)).
- **Par lecteur, pas par code** : un même code peut être comparé exactement sur un lecteur et souplement sur un autre.
- **Sans effet en v1** : un lecteur v1 compare toujours exactement, case cochée ou non.

Pour l'activer :

1. Ouvrez la fiche du lecteur et cochez **Comparer les codes exactement**.
2. Lisez l'avertissement qui s'affiche : « Les codes tapés sans leurs zéros initiaux (ex. 42 pour 0042) n'ouvriront plus avec ce lecteur ». Si au moins un de vos codes commence par un zéro ou contient une lettre, il ajoute : « Au moins un code commence par un zéro ou contient une lettre : vérifiez qu'il est tapé en entier ». L'avertissement ne montre **jamais** de code, ni une partie de code. Il n'apparaît que lorsque vous cochez la case, pas à l'ouverture d'une fiche déjà cochée.
3. Sauvegardez. Le changement ne prend effet qu'à la sauvegarde.

Le journal garde la trace du changement, sans aucun code, et au niveau Erreur (donc visible avec le réglage par défaut) : « Lecteur <nom> (#<numéro>) : comparaison exacte des codes activée », ou « … désactivée (comparaison souple) » quand vous décochez.

⚠️ **Sur la porte de production, laissez la case décochée** tant que vous n'avez pas vérifié que **chaque utilisateur tape son code en entier**, zéros initiaux compris. Un utilisateur habitué à taper `42` pour `0042` serait refusé, puis bloqué après quelques essais. **Essayez d'abord l'option sur un autre lecteur**, avec un code de test, avant de l'étendre. Pour revenir en arrière, décochez et sauvegardez.

Pour savoir quels lecteurs sont concernés, voir la colonne « Comparaison des codes » du tableau de [Posture de sécurité par lecteur](#mesure-posture).

Détail : [Configuration des codes](configuration.md#codes-configuration) et [Génération d'un code temporaire](fonctionement.md#codes-temporaires). Messages d'erreur : [Messages sur les codes](depannage.md#messages-codes).

<a id="proc-exiger-v1"></a>
## Exiger le protocole v1 signé (et le chiffrement)

**Exiger le protocole v1 signé**, c'est appairer le lecteur : il n'accepte plus que les appels signés avec son secret. Un lecteur v0 ne le peut pas.

**Conditions** : lecteur v1 (déjà annoncé en v1, dernier appel en v1), actif (ni désactivé, ni en attente d'approbation) et non encore appairé. Sinon le plugin refuse avec un message : voir [Exiger le protocole v1 signé refusé](depannage.md#exiger-v1-refuse).

1. Dans le tableau **Posture de sécurité des lecteurs** (page du plugin), cliquez sur **Appairer ce lecteur** dans la colonne « Exiger le protocole v1 signé ».
2. **Lisez l'avertissement et confirmez** : « Exiger le protocole v1 signé pour ce lecteur ? Un lecteur encore flashé en v0 ne fonctionnera plus. Un secret va être généré : tant qu'il n'est pas reporté sur le lecteur (configuration du sketch, sur la fiche du lecteur qui va s'ouvrir), tous ses appels seront refusés. »
3. La fiche du lecteur s'ouvre. **Téléchargez la configuration du sketch**, reportez-la sur le lecteur et reflashez-le (voir [Configuration du sketch d'un lecteur v1](reference.md#configuration-sketch)). Le fichier contient le secret : ne le partagez pas et supprimez-le après le flash.
4. Vérifiez : la colonne affiche « Exigé » et la fiche « v1 (lecteur appairé : appels v0 et non signés refusés) ».

**Retour en arrière** : cliquez sur **Rabaisser à v0** (colonne du tableau ou fiche du lecteur) et confirmez. Le secret est supprimé et les appels v0 ou non signés sont de nouveau acceptés : tout appareil du réseau peut alors se faire passer pour ce lecteur. À réserver à un lecteur reflashé avec un ancien sketch. Voir [Rabaisser à v0](reference.md#rabaisser-v0).

**Exiger le chiffrement des identifiants** : ⚠️ **aucun sketch ne l'émet encore**. Tant que la colonne affiche « Non annoncé », il n'y a rien à exiger, et exiger le chiffrement couperait le lecteur (le plugin refuse alors de le proposer). Quand un sketch le permettra, la procédure est : [Exiger le chiffrement des identifiants](reference.md#exiger-chiffrement). Pour le lever, cliquez sur **Ne plus exiger le chiffrement**.

<a id="proc-ip"></a>
## Corriger l'IP d'un lecteur et régler le filtrage

**Corriger l'IP d'un lecteur** (nouveau bail DHCP, lecteur remplacé) :

- **Par l'inclusion** : activez le mode inclusion, faites parler le lecteur (redémarrage ou badge), puis arrêtez l'inclusion. La nouvelle adresse est acceptée le temps d'un appel, **seulement pendant la fenêtre d'inclusion**.
- **À la main** : ouvrez la fiche du lecteur, corrigez le champ **IP autorisée** (adresse IPv4 ou IPv6, ou vide) et sauvegardez. Ces adresses sont refusées : `127.0.0.1` (et tout `127.x.x.x`), `::1`, `0.0.0.0`, `::` et l'adresse de Jeedom lui-même.
- **Pour que ça ne se reproduise pas**, réservez une adresse fixe au lecteur dans votre box (réservation DHCP), puis cochez « Refuser les appels venant d'une autre IP » sur sa fiche.

**Le filtrage par IP d'origine** (option « Contrôler l'IP d'origine des lecteurs », activée par défaut) :

| Votre situation | Que faire |
|---|---|
| Lecteurs reliés directement à votre réseau local | **Laissez l'option cochée.** |
| Les lecteurs eux-mêmes joignent Jeedom à travers un **reverse proxy** ou un **NAT** | Vous pouvez la **décocher** : leur adresse d'origine n'est alors pas la leur, leurs appels seraient refusés. Un bandeau rouge rappelle que n'importe quel appareil peut alors se faire passer pour un lecteur v0. |
| Jeedom est publié par un **tunnel ou un accès distant** (cloudflared, accès distant Jeedom…) | **Ne décochez rien.** Les lecteurs n'empruntent pas ce tunnel : l'option bloque justement les appels qui y passent. |
| Jeedom tourne sous **Docker** | L'adresse vue d'un lecteur peut être celle du NAT du conteneur : ne cochez pas « Refuser les appels venant d'une autre IP » avant d'avoir vérifié l'adresse inscrite dans « IP autorisée ». **À confirmer** sur une installation Docker réelle. |

Détail : [Option « Contrôler l'IP d'origine des lecteurs »](configuration.md#controle-ip-origine) et [Configuration des lecteurs](configuration.md#configuration-des-lecteurs). Messages de refus : [Appel refusé : origine](depannage.md#origine-refusee).

<a id="proc-arborescence"></a>
## Sécuriser les dossiers du plugin (Apache, nginx)

La protection des dossiers internes **dépend de votre serveur web**.

- **Apache** (installation standard de Jeedom) : la protection est **active d'office** par des fichiers `.htaccess`. Elle suppose qu'Apache les prenne en compte (`AllowOverride All`, réglage standard). Rien à faire.
- **nginx** : nginx **ignore** les `.htaccess`. Tant que vous n'avez pas ajouté la règle ci-dessous, les dossiers internes (`.memory`, `.claude`, `.githooks`, `.github`, `arduino`, `tests`, `core/class`, `core/php`) restent lisibles par quiconque joint votre Jeedom.

```nginx
# Badger Fork : dossiers internes du plugin, jamais appelés par un navigateur
location ~ /plugins/badger2/(\.memory|\.claude|\.githooks|\.github|arduino|tests|core/class|core/php)(/|$) {
    deny all;
}
```

1. Placez cette règle dans le bloc `server` de Jeedom, **avant** la `location` qui traite le PHP.
2. Testez avec `nginx -t`, puis rechargez nginx.
3. Vérifiez : `curl -sI http://<box>/plugins/badger2/core/php/badger2.inc.php` doit répondre **403**. Une réponse **200** signifie que la règle est placée après la `location` du PHP, ou masquée par une `location ^~` qui couvre `/plugins/`.

La règle n'ôte rien aux lecteurs : l'API reste joignable sur ses deux adresses.

> **À confirmer sur une installation nginx réelle** : cette règle n'a pas été essayée sous nginx. Sous nginx, d'autres dossiers (pages du plugin, traductions, documentation) restent aussi joignables : ils ne contiennent aucun secret. Si vous avez installé le plugin par `git clone`, le dossier `.git` peut être joignable sous nginx : protégez-le par une règle semblable.

Détail et rappel affiché dans la configuration du plugin : [Accès direct aux dossiers internes](configuration.md#acces-direct-dossiers).

<a id="proc-journal"></a>
## Lire le journal pour diagnostiquer un refus

Le journal se lit dans **Analyse > Logs**, log `badger2`. Son niveau par défaut est **Erreur** : les refus d'appel sont écrits au niveau **Avertissement** et restent **invisibles** tant que vous ne montez pas le niveau.

1. Ouvrez **Plugins > Gestion des plugins > Badger Fork**.
2. Réglez le niveau de log sur **Avertissement** (ou **Info** pour voir aussi les badges présentés).
3. Reproduisez le problème, lisez le log `badger2`, puis **remettez le niveau par défaut**.

Au niveau Erreur, vous voyez déjà : les badges inconnus et codes faux (sans leur valeur), les lecteurs bloqués, les déblocages, les consultations d'un code, l'activation, la prolongation et l'arrêt de l'inclusion, les approbations et refus. Voir [Niveau de log](reference.md#niveau-de-log) et le [dépannage](depannage.md), qui cite chaque message tel qu'il apparaît.

<a id="lecteur-v0-durable"></a>
## Que faire d'un lecteur qui reste en v0 ?

Un Arduino Uno reste en v0 : il n'existe pas de sketch v1 pour lui. Vous pouvez le garder, sans l'exposer davantage :

- laissez actif le **contrôle de l'IP d'origine** ;
- réservez-lui une **adresse fixe** et cochez « Refuser les appels venant d'une autre IP » ;
- gardez des **limites d'essais** serrées et la limite globale active ;
- isolez les lecteurs sur un **réseau dédié** si votre matériel le permet ;
- remplacez-le par une carte Mega 2560 ou ESP quand vous le pouvez : [Débuter pas à pas](debuter.md).

---

[Retour à l'accueil](index.md) · [Référence technique](reference.md) · [Dépannage](depannage.md)
