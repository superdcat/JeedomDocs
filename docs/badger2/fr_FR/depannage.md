# Dépannage détaillé

Cette page recense les symptômes et les messages que vous pouvez rencontrer, leur cause et l'action à mener. Chaque entrée est atteignable depuis le [tutoriel](debuter.md) et la [référence technique](reference.md).

**Les messages du plugin cités ici se lisent dans Analyse > Logs, log `badger2`.** Les avertissements n'y sont écrits que si le niveau de log du plugin est au moins **Avertissement** : voir [Niveau de log](reference.md#niveau-de-log). Les messages de la console du lecteur se lisent dans le moniteur série de l'IDE Arduino (115 200 bauds, voir la [console série](cartes-et-sketch-v1.md#console-serie)).

> **À confirmer : les entrées propres au sketch v1 sont tirées du code, pas d'une observation sur matériel réel.**

## Tableau des symptômes

| Symptôme | Cause probable | Entrée détaillée |
|---|---|---|
| Rien ne s'affiche à la console série | Mauvaise vitesse ou mauvais port, console désactivée | [Rien à la console](#rien-console) |
| Le sketch refuse de compiler | Carte ou profil incompatible, carte Uno, réglage hors limites | [Compilation refusée : profil](#compilation-refusee-profil) |
| Le lecteur n'apparaît pas dans Jeedom | Inclusion non activée, réseau, adresse de Jeedom | [Lecteur absent de Jeedom](#lecteur-absent) |
| Lecteur présent mais « En attente de l'annonce du lecteur » | Lecteur créé inactif | [Lecteur en attente d'annonce](#lecteur-attente-hello) |
| Le badge est lu mais la porte reste fermée | Badge inconnu ou désactivé, lecteur bloqué, aucun scénario | [Badge lu, porte fermée](#badge-porte-fermee) |
| Le lecteur ne se fait plus entendre après un changement d'adresse | Adresse enregistrée différente, réservation DHCP absente | [Lecteur muet après changement d'adresse](#lecteur-muet-adresse) |
| « version de protocole non supportée » | Le lecteur annonce une version que le plugin ne connaît pas | [Version non supportée](#version-non-supportee) |
| « signature invalide » | Secret du lecteur différent de celui de Jeedom | [Signature refusée](#signature-refusee) |
| « rejeu » | Compteur du lecteur remis à zéro, appel rejoué | [Rejeu refusé](#rejeu-refuse) |
| « rétrogradation » | Lecteur appairé reflashé avec un ancien sketch | [Rétrogradation refusée](#retrogradation-refusee) |
| « Secret absent ou illisible » | Secret perdu côté Jeedom | [Secret perdu](#secret-perdu) |
| « Exiger le protocole v1 signé est refusé / impossible / État du lecteur illisible » (tableau de posture) | Lecteur v0, dernier appel en v0, lecteur désactivé ou en attente, état illisible | [Exiger le protocole v1 signé refusé](#exiger-v1-refuse) |
| « Aucun appel enregistré (depuis la mise à jour du plugin ou le dernier vidage du cache) » | Marqueur d'activité vide après une mise à jour ou un vidage du cache | [Aucun appel enregistré](#aucun-appel-enregistre) |
| Fonction grisée sur la fiche, capacité inconnue | Capacité non annoncée par le lecteur | [Capacité non annoncée](#capacite-non-annoncee) |
| Appel refusé : adresse d'origine non locale, en-tête de proxy, origine interdite, lecteur appelé depuis une autre IP | Lecteur hors réseau local, tunnel ou proxy, lecteur verrouillé sur une autre adresse | [Origine refusée](#origine-refusee) |
| « Appel v0 refusé : … » (commande inconnue, nom de lecteur invalide, IP déclarée invalide, valeur de badge ou code hors du contrat v0) | Appel d'un lecteur d'origine hors du format émis par les sketchs | [Appel v0 hors format](#appel-v0-hors-format) |
| Autres refus d'un appel v1 | Identifiant, équipement en double, corps invalide, retard | [Autres refus d'un appel v1](#autres-refus-v1) |
| Mise à jour à distance sans effet | Mot de passe, port, `ota -` | [Mise à jour à distance](#depannage-ota) |
| « Une migration de données a échoué : consultez le journal » (centre de messages) | Une évolution de données n'a pas pu s'appliquer (un équipement n'a pas pu être enregistré) | [Migration de données en échec](#migration-donnees-echec) |
| « Lecteur bloqué : appel ignoré » ; « Verrouillé jusqu'à » sur la fiche ; blocage qui revient | Trop de badges inconnus ou de codes faux, ou limite globale atteinte | [Lecteur bloqué](#lecteur-bloque) |
| « Limite d'essais invalide » ; « Temps de blocage invalide » ; « Lecteur occupé, réessayez » ; « Lecteur introuvable » | Valeur vide, nulle ou hors bornes à la sauvegarde ; deux actions simultanées | [Messages de l'interface](#messages-interface-securite) |
| « Code refusé » ; « Ce code est déjà utilisé » ; « Code illisible » ; « Impossible de générer un code unique » ; messages « Code non converti », « Plusieurs équipements code portent le même code » | Code hors format, en double, illisible ou hérité d'avant la mise à jour | [Messages sur les codes](#messages-codes) |
| « Inclusion : limite de … créations atteinte » ; « L'inclusion n'est pas active » ; « Élément introuvable ou déjà traité » | Limite d'inclusion, fenêtre échue, élément déjà traité | [Messages d'inclusion](#messages-inclusion) |
| « Exiger le chiffrement est impossible… » ; « identifiant en clair » ; « identifiant chiffré indéchiffrable » | Exigence de chiffrement sans lecteur qui le permette ; lecteur qui envoie en clair ou chiffre mal | [Exiger le chiffrement : refus et échecs](#exiger-chiffrement-refuse) |
| Bandeau jaune « Au moins un lecteur utilise l'ancien protocole » ; bandeau rouge « Le contrôle d'IP d'origine est désactivé » ; « Posture de sécurité indisponible » | Lecteur v0 actif ; option décochée ; tableau de posture illisible | [Bandeaux et posture](#bandeaux-securite) |
| Autres lignes de la tranche sécurité dans le journal (« verrou … indisponible », « version des données … », « paramètre de version répété », « IP … remplacée »…) | Voir le tableau | [Autres messages du journal](#journal-securite-divers) |

<a id="rien-console"></a>
## Rien ne s'affiche à la console série

- **Cause** : vitesse du moniteur différente de 115 200 bauds ; mauvais port série ; fin de ligne qui n'est pas « NL et CR » (les commandes ne passent pas) ; console désactivée dans le fichier de configuration du sketch (`BADGER2_CONSOLE` ou `BADGER2_TRACES` à `0`) ; carte sans puce USB (WT32-ETH01) qui demande un adaptateur série externe.
- **Action** : réglez 115 200 bauds, choisissez le bon port, appuyez sur le bouton reset de la carte (le démarrage se lit sur la console) et tapez `aide`. Si rien n'apparaît toujours, vérifiez la console dans le fichier de configuration. Le lecteur fonctionne sans console : son absence n'empêche pas de lire les badges.

<a id="compilation-refusee-profil"></a>
## Compilation refusée : profil, carte ou réglage

- **Cause** : la carte choisie dans l'IDE ne correspond pas au profil du fichier de configuration (le message nomme la carte attendue) ; une Uno, une Nano ou une Pro Mini est refusée en v1 ; deux fonctions sont sur la même broche ; une valeur est hors limites. Chaque refus nomme le réglage à corriger.
- **Action** : corrigez le réglage nommé, ou choisissez la bonne entrée dans Outils > Type de carte (voir le [tableau des cartes](cartes-et-sketch-v1.md#tableau-capacites)). Pour une Uno, gardez le sketch d'origine (v0).

<a id="lecteur-absent"></a>
## Le lecteur n'apparaît pas dans Jeedom

Contrôlez dans l'ordre :

1. **Réseau du lecteur** : la console affiche « Réseau : adresse … » quand le lecteur a une adresse. « Réseau : lien absent » = câble ou Wi-Fi ; « Réseau : pas d'adresse, nouvel essai dans … » = le DHCP ne répond pas ; « Réseau : aucun module Ethernet détecté » = shield ou module mal enfiché, bibliothèque Ethernet non conforme.
2. **Adresse de Jeedom** : `config` à la console montre la cible. « Envoi : Jeedom injoignable, nouvel essai dans … » = adresse ou port faux, pare-feu, Jeedom arrêté. Le lecteur parle en **HTTP** : saisissez le port HTTP de Jeedom, pas celui du HTTPS.
3. **Inclusion** : un lecteur n'est créé que si le **mode inclusion** est actif. Sans lui, le log écrit « Appel v1 refusé : lecteur … inconnu (inclusion désactivée …) » (lecteur v1) ou « Lecteur inconnu detecté : … » (lecteur d'origine). Activez le mode inclusion, redémarrez le lecteur (ou présentez un badge pour un lecteur d'origine) et rechargez la page. L'inclusion **s'arrête seule** (5 minutes par défaut) : si le bandeau « Inclusion active » a disparu, relancez-la. Si la **limite de créations** de l'inclusion (20 par défaut) est atteinte, le log écrit un avertissement et plus rien n'est créé : arrêtez l'inclusion, relancez-la, ou relevez la limite dans la configuration du plugin. Avec l'**approbation obligatoire**, le lecteur est bien créé mais « En attente d'approbation » : approuvez-le sur la page du plugin.
4. **Origine** : voir [Origine refusée](#origine-refusee).
5. **Test** : la commande `test` à la console répond « Jeedom a accepté le battement (ok) » quand tout est bon.

<a id="lecteur-attente-hello"></a>
## Lecteur présent mais « En attente de l'annonce du lecteur »

- **Cause** : un lecteur v1 créé par l'inclusion est **inactif** ; l'appel qui l'a créé n'a aucun autre effet. Même affichage pour un lecteur désactivé au moment de son démarrage.
- **Action** : ouvrez sa fiche, cochez **Activer**, sauvegardez, puis redémarrez le lecteur (bouton reset). Sa fiche affiche alors protocole, firmware, carte et capacités.

<a id="badge-porte-fermee"></a>
## Le badge est lu mais la porte reste fermée

Le plugin ne commande pas la porte tout seul : un badge **connu et actif** met à jour la commande `Presentation` de son équipement, et c'est **un scénario Jeedom** qui ouvre ensuite la porte. Vérifiez :

- **Badge inconnu** : le log écrit « Badge inconnu présenté sur le lecteur … » (niveau Erreur). Enregistrez-le par le mode inclusion, puis activez-le (ou approuvez-le si l'approbation obligatoire est cochée). Un lecteur « En attente d'approbation » ne crée pas de badge.
- **Badge ou lecteur désactivé** : cochez **Activer** sur l'équipement et sauvegardez.
- **Lecteur bloqué** : après trop de badges inconnus ou de codes faux, le lecteur ignore **tout** appel, même d'un badge valide, jusqu'à la fin du blocage. Le log écrit « Lecteur bloqué : appel ignoré » (niveau Erreur) avec l'heure de fin. Ouvrez la fiche du lecteur : le bloc **Verrouillage** indique « Verrouillé jusqu'à … » ainsi que le niveau et les essais. Attendez l'heure indiquée, ou cliquez sur **Débloquer** (administrateur). Un blocage qui revient vite ou s'allonge est normal : voir [Comment fonctionne le blocage](fonctionement.md#comment-fonctionne-le-blocage). Procédure complète : [Lecteur bloqué](#lecteur-bloque).
- **Aucun scénario** : sans scénario déclenché par `Presentation`, rien ne s'ouvre. Voir [Fonctionnement et utilisation des équipements](fonctionement.md).
- **Format de badge non reconnu en v1** : seules les trames de 26 et 34 bits sont reconnues. Un badge enrôlé en décimal (sketch `JeedouinoLAN`) ou lu en 24 ou 32 bits est traité comme inconnu.
- **Premier badge d'un lecteur neuf** : l'appel qui crée un lecteur v1 n'est pas traité ; présentez le badge une seconde fois.
- **Événement en retard** : un événement reçu plus de 30 secondes après sa survenue par un lecteur appairé est accepté sans effet (log « événement … en retard de … s : accepté, sans effet »).
- **Mode debug en observation seule** : la porte n'est pas traitée pendant ce mode. Cliquez sur **Arrêter**.

Pour voir ce que le plugin reçoit, utilisez le [mode debug](reference.md#mode-debug).

<a id="lecteur-muet-adresse"></a>
## Le lecteur ne se fait plus entendre après un changement d'adresse

- **Cause** : le plugin mémorise l'adresse du lecteur. Si elle change (nouveau bail DHCP, redémarrage de la box) hors mode inclusion, les appels sont refusés (réponse 403). Le log écrit « Appel v1 refusé : lecteur … appelé depuis …, adresse enregistrée … : activer l'inclusion le temps d'un appel pour enregistrer la nouvelle adresse (une réservation DHCP évite ce refus) » ; la console du lecteur écrit « Envoi : refusé par le plugin (auth) ».
- **Action** : activez le mode inclusion, faites parler le lecteur (redémarrage ou badge), puis arrêtez l'inclusion : la nouvelle adresse est enregistrée. Cette acceptation ne vaut que **pendant la fenêtre d'inclusion** : une fois échue, relancez-la. **Évitez le problème en réservant une adresse fixe au lecteur dans votre box** (réservation DHCP). Un lecteur d'origine met à jour son adresse tout seul, sauf si vous avez coché « Refuser les appels venant d'une autre IP » sur sa fiche (voir [Origine refusée](#origine-refusee)).

<a id="version-non-supportee"></a>
## « version de protocole non supportée : mettre à jour le plugin »

- **Message** : « Appel refusé : version de protocole non supportée : mettre à jour le plugin (version reçue …, adresse …, versions servies : v0, v1) », réponse 400.
- **Cause** : le lecteur annonce une version de protocole que ce plugin ne connaît pas (sketch plus récent que le plugin).
- **Action** : mettez à jour le plugin, ou reflashez le lecteur avec un sketch de la version du plugin. Les versions servies s'affichent dans Analyse > Santé.

<a id="signature-refusee"></a>
## « signature invalide »

- **Message** : « Appel v1 refusé : signature invalide (lecteur …, adresse …) », réponse 403 ; console : « Envoi : refusé par le plugin (auth) ». Un lecteur appairé dont l'appel n'est **pas signé du tout** reçoit « Appel v1 refusé : rétrogradation, appel non signé au nom du lecteur appairé … ».
- **Cause** : le secret du lecteur n'est pas celui de Jeedom : secret régénéré après le flash, fichier de configuration ancien, valeur saisie à la console qui prime sur le fichier, sauvegarde Jeedom restaurée.
- **Action** : tapez `config` à la console (le secret est indiqué « défini (console) » ou « défini (config.h) »), puis régénérez le secret depuis la fiche et reconfigurez le lecteur (téléchargement du fichier et flash, ou commande `secret`). Voir [Régénérer le secret](reference.md#regenerer-secret).

<a id="rejeu-refuse"></a>
## « rejeu »

- **Message** : « Appel v1 refusé : rejeu (lecteur …, démarrage …, séquence …) », réponse 403 ; console : « Envoi : le plugin a déjà reçu ce démarrage (mémoire effacée ?) : nouvel appairage nécessaire ».
- **Cause** : le compteur de démarrages du lecteur est repassé en arrière (mémoire du lecteur effacée, effacement complet à l'ISP) ou un appel déjà reçu a été renvoyé. Un lecteur dont la mémoire est usée annonce « Mémoire non volatile : compteur de démarrages non enregistré » : ses badges sont refusés à chaque redémarrage jusqu'au remplacement de la carte.
- **Action** : régénérez le secret depuis la fiche (nouvel appairage) et reconfigurez le lecteur. Si le message revient à chaque redémarrage, changez la carte.

<a id="retrogradation-refusee"></a>
## « rétrogradation » : un lecteur appairé n'est plus entendu

- **Message** : « Appel refusé : rétrogradation : appel v0 (ancienne route|route courante) au nom du lecteur appairé … : seul « Rabaisser à v0 » le permet » ; ou « Appel v1 refusé : version inférieure au plancher du lecteur … ».
- **Cause** : un lecteur appairé a une **version minimale v1** : il n'accepte plus d'appel v0. Typique d'un lecteur reflashé avec un sketch d'origine.
- **Action** : si vous voulez garder le sketch d'origine sur ce lecteur, cliquez sur **Rabaisser à v0** dans sa fiche (le lecteur redevient non authentifié : voir [Rabaisser à v0](reference.md#rabaisser-v0)). Sinon, reflashez-le avec le sketch v1.

<a id="secret-perdu"></a>
## « Secret absent ou illisible »

- **Message** : la fiche affiche « Secret absent ou illisible : tous les appels de ce lecteur sont refusés. Régénérez le secret. » ; log : « lecteur … appairé mais secret absent ou illisible : régénérer le secret » ; ou « Secret de test public : régénérez le secret du lecteur ».
- **Cause** : le secret n'est plus lisible côté Jeedom (restauration d'une sauvegarde, migration).
- **Action** : cliquez sur **Régénérer le secret**, téléchargez la configuration et reconfigurez le lecteur.

Si c'est le **fichier téléchargé** qui est perdu, retéléchargez-le : le secret ne change pas. Le secret n'est jamais affiché à l'écran.

<a id="exiger-v1-refuse"></a>
## « Exiger le protocole v1 signé » refusé

Ces messages s'affichent quand vous cliquez sur **Appairer ce lecteur** dans le tableau [Posture de sécurité des lecteurs](reference.md#posture-securite). Aucun appel du lecteur n'est affecté.

| Message | Cause | Action |
|---|---|---|
| « … refusé pour ce lecteur : il n'a jamais utilisé le protocole v1 (sketch d'origine) et l'exiger le couperait. Reflashez-le d'abord avec le sketch v1. » | Lecteur d'origine (v0), jamais annoncé en v1. | Reflashez-le avec le sketch v1 (Mega 2560 ou ESP), redémarrez-le pour qu'il s'annonce, puis appairez-le. |
| « … refusé pour ce lecteur : son dernier appel est en protocole v0 et l'exiger le couperait. Reflashez-le d'abord avec le sketch v1. » | Lecteur déjà annoncé en v1, mais dont le dernier appel est en v0 (reflashé avec un ancien sketch). | Reflashez-le avec le sketch v1 et attendez un appel en v1. |
| « Exiger le protocole v1 signé est impossible pour un lecteur désactivé ou en attente d'approbation : activez-le ou approuvez-le d'abord. » | Lecteur inactif. | Activez-le, ou approuvez-le (voir [Inclusion](reference.md#inclusion-reference)), puis recommencez. |
| « État du lecteur illisible : ouvrez sa fiche. » | Le plugin n'a pas pu lire l'état du lecteur. | Ouvrez sa fiche ; consultez le log `badger2` (voir [Niveau de log](reference.md#niveau-de-log)). |

<a id="aucun-appel-enregistre"></a>
## « Aucun appel enregistré »

- **Message** : dans le tableau de posture, colonne **Dernière activité** : « Aucun appel enregistré (depuis la mise à jour du plugin ou le dernier vidage du cache) ».
- **Cause** : la date du dernier appel est tenue par Jeedom depuis la mise à jour du plugin ou le dernier vidage du cache. Tant que le lecteur n'a pas rappelé, elle est vide. Un lecteur éteint, débranché ou sans réseau donne le même affichage.
- **Action** : présentez un badge ou attendez le prochain appel du lecteur. Si rien ne s'affiche après un appel, voir [Le lecteur n'apparaît pas dans Jeedom](#lecteur-absent).

<a id="capacite-non-annoncee"></a>
## Capacité non annoncée ou inconnue

- **Fonction grisée dans la fiche** : elle exige une capacité que le lecteur n'annonce pas ; la raison est affichée. Aucune fonction n'est concernée pour l'instant.
- **Capacité affichée sous son seul nom brut** : le plugin est plus ancien que le sketch. Ce n'est pas une erreur.
- **Côté lecteur** : une réponse n'agit que pour une capacité annoncée. Sans secret, un lecteur n'ouvre pas sur une réponse du plugin (console : « Gâche : sans secret, la réponse du plugin n'ouvre pas »).
- **Deux lecteurs n'ont pas la même liste** : elle dépend de la carte et des fonctions compilées.

<a id="origine-refusee"></a>
## Appel refusé : origine

Ces refus sont écrits au niveau **Avertissement** dans le log `badger2` : ils sont **invisibles au niveau de log par défaut (Erreur)**. Passez le log à Avertissement (ou plus) avant de chercher (voir [Niveau de log](reference.md#niveau-de-log)). Un appel refusé reçoit une réponse 403 et ne déclenche aucun événement.

- « Appel refuse : adresse d'origine non locale … » : le plugin n'accepte que les adresses du réseau local. Un lecteur derrière un VPN ou un routage public est refusé. Si vos lecteurs sont en adressage public sur votre réseau, ou passent par un NAT, voir l'option « Contrôler l'IP d'origine des lecteurs » dans la [configuration](configuration.md#controle-ip-origine).
- « Appel refusé : en-tête de proxy … présent (tunnel ou reverse proxy), adresse de connexion … » : le lecteur doit parler **directement** à Jeedom, sans proxy ni tunnel. Si ce message apparaît alors que c'est un tunnel d'accès distant (cloudflared…) qui amène l'appel, c'est le comportement voulu : ne décochez pas l'option. Ne la décochez que si ce sont vos **lecteurs** qui passent par un reverse proxy.
- « Appel refusé : adresse d'origine … interdite pour un lecteur (bouclage ou adresse du serveur : tunnel ou proxy installé sur Jeedom ?), lecteur … » : l'appel d'un lecteur **verrouillé** (case « Refuser les appels venant d'une autre IP » cochée) arrive depuis Jeedom lui-même, typiquement via un relais installé sur la machine de Jeedom. Action : décochez la case pour ce lecteur. Un lecteur non verrouillé n'est pas refusé dans ce cas : le log écrit seulement, au niveau Info, « adresse d'origine … interdite (relais sur Jeedom ?), IP déclarée utilisée ».
- « Appel refusé : lecteur … appelé depuis …, IP autorisée … : activer l'inclusion le temps d'un appel ou corriger l'IP autorisée sur la page du lecteur (une réservation DHCP évite ce refus) » : le lecteur est **verrouillé** et appelle depuis une autre adresse que son IP autorisée (nouveau bail DHCP, lecteur remplacé, ou appareil imposteur). « IP autorisée aucune » signifie que le champ est vide. Action : si l'adresse est légitime, activez le mode inclusion le temps d'un appel du lecteur, ou corrigez le champ « IP autorisée » sur sa fiche ; puis réservez une adresse fixe au lecteur dans votre box. Sinon, ne faites rien : le refus est le comportement voulu.
- **Docker, NAT** : derrière un NAT ou avec Jeedom sous Docker, l'adresse vue par le plugin peut être celle du NAT et non celle du lecteur : un lecteur verrouillé sur son adresse peut alors être refusé, ou plusieurs lecteurs partager la même adresse. **À confirmer** sur une installation Docker réelle. Voir [Corriger l'IP d'un lecteur](securite.md#proc-ip).
- « Appel v1 refusé : adresse d'origine … interdite pour un lecteur (bouclage, adresse du serveur ou adresse invalide) » : une adresse de Jeedom lui-même ou invalide ne peut pas être celle d'un lecteur.
- À la sauvegarde d'un lecteur, « IP autorisée invalide » ou « IP autorisée refusée » : l'adresse saisie n'est pas une IP, ou c'est une adresse de bouclage, non spécifiée ou de Jeedom. Saisissez l'adresse réelle du lecteur ou laissez le champ vide.

<a id="appel-v0-hors-format"></a>
## Appel v0 hors format

Ces refus sont écrits au niveau **Avertissement** dans le log `badger2` : ils sont **invisibles au niveau de log par défaut (Erreur)**. Passez le log à Avertissement (ou plus) avant de chercher (voir [Niveau de log](reference.md#niveau-de-log)).

Un appel de lecteur d'origine (v0) qui sort du format émis par les sketchs est refusé : réponse 403, **aucun effet** (rien n'est créé, aucun compteur ne bouge, aucun scénario ne se déclenche). Tout ce que les sketchs d'origine émettent reste accepté, y compris l'appui sur Entrée seule au clavier.

| Message du log | Cause | Action |
|---|---|---|
| « Appel v0 refusé : commande inconnue « … » (lecteur …, adresse …) » | La commande de l'appel n'est pas une de celles des sketchs | Ce n'est pas un lecteur d'origine : vérifiez qui appelle l'adresse. |
| « Appel v0 refusé : nom de lecteur invalide « … » (adresse …) » | Nom de lecteur avec des caractères interdits et inconnu de Jeedom | Corrigez le nom dans le sketch ; sinon, ne faites rien. |
| « Appel v0 refusé : IP déclarée invalide « … » (lecteur …, adresse …) » | L'adresse annoncée par l'appel n'est pas une adresse IP | Vérifiez le sketch et son adresse. |
| « Appel v0 refusé : valeur de badge hors du contrat v0, valeur masquée, visible en mode debug … » | Valeur de badge hors format | Activez le mode debug pour voir la valeur reçue. |
| « Appel v0 refusé : code hors du contrat v0, valeur masquée, visible en mode debug … » | Code hors format | Idem. Le code n'est jamais écrit dans le log. |

En mode debug, le résultat de l'appel est « Refusé : paramètre hors du contrat v0 (HTTP 403) » (ou « commande inconnue »). Si un lecteur légitime est refusé, ouvrez une demande avec ce résultat.

<a id="autres-refus-v1"></a>
## Autres refus d'un appel v1

| Message du log | Cause | Action |
|---|---|---|
| « Appel v1 refusé (adresse …, lecteur …) : » suivi d'un motif (valeur hors bornes, champ absent…) | Corps d'appel invalide, réponse 400 ; console : « Envoi : refusé par le plugin (invalid) » | Vérifiez que le sketch et le plugin sont à jour ; utilisez le mode debug. |
| « identifiant … de casse différente de celui d'un équipement enregistré » | Le lecteur annonce `Porte` alors que l'équipement s'appelle `PORTE` | Alignez la casse de l'identifiant du lecteur. |
| « identifiant … désigne un équipement qui n'est pas un lecteur » | L'identifiant du lecteur est celui d'un badge ou d'un code | Changez l'identifiant du lecteur. |
| « plusieurs équipements portent l'identifiant … » | Deux équipements Badger Fork ont le même identifiant, à la casse près | Supprimez ou renommez le doublon. |
| « verrou d'appairage indisponible » ou « appairage … modifié pendant l'appel » | Appairage en cours de modification | Réessayez ; l'appel est réémis par le lecteur. |
| « réponse non signée (appairage modifié ou secret illisible) » | Appairage modifié ou secret illisible pendant l'appel | Régénérez le secret. |
| Console : « Envoi : réponse non authentifiée (signature absente ou fausse) » | Le lecteur a un secret mais la réponse du plugin n'est pas signée : lecteur non appairé côté plugin ou secrets différents | Appairez le lecteur depuis sa fiche et reconfigurez-le avec son secret. |
| Console : « Envoi : réponse non conforme (HTTP …) » | Réponse inattendue (erreur du serveur web, 503) | Contrôlez Jeedom et le plugin ; le lecteur réémet l'événement. |

<a id="depannage-ota"></a>
## Mise à jour à distance sans effet

- **Aucun port à l'écoute** : le mot de passe n'est pas enregistré ou le lecteur n'a pas redémarré après `ota mdp` (voir [Mise à jour à distance](cartes-et-sketch-v1.md#mise-a-jour-distance)). La console indique « inactive (aucun mot de passe) ».
- **Mega** : la fonction est refusée à la compilation ; elle n'existe que sur ESP8266 et ESP32.
- **Mot de passe refusé** : le port est refermé 10 secondes après un refus.
- **Après `ota -`** : la mise à jour à distance est désactivée immédiatement ; pour la réactiver, `ota mdp` puis un redémarrage. Si `ota -` répond par un refus d'écriture, rien n'est effacé et la mise à jour à distance **reste active** : vérifiez avec `ota`.
- **Lecteur injoignable après la mise à jour** : une configuration réseau fausse dans le binaire en est la cause ; reflashez par câble USB.

<a id="migration-donnees-echec"></a>
## Migration de données en échec

- **Cause** : une évolution de données du plugin n'a pas pu s'appliquer, par exemple parce qu'un équipement n'a pas pu être enregistré. Le centre de messages affiche « Une migration de données a échoué : consultez le journal ».
- **Action** : ouvrez le journal badger2 et cherchez la ligne « Migration des données n° … en échec ». Corrigez si possible l'équipement cité, puis désactivez et réactivez le plugin, ou attendez la prochaine mise à jour. Vos équipements restent utilisables en attendant. Le message disparaît quand toutes les migrations sont passées.

<a id="lecteur-bloque"></a>
## Lecteur bloqué

- **Message** : « Lecteur bloqué : appel ignoré (lecteur …, jusqu'à …) » (niveau Erreur, donc visible par défaut). Sur la fiche du lecteur, le bloc **Verrouillage** affiche « Verrouillé jusqu'à » suivi de la date et de l'heure.
- **Cause** : le lecteur a atteint sa limite de badges inconnus ou de codes faux consécutifs, ou la limite globale d'échecs cumulés. Pendant le blocage, **tout** appel est ignoré, même celui d'un badge valide. Un appareil du réseau qui envoie de faux appels peut aussi provoquer ce blocage.
- **Action** : attendez l'heure indiquée, ou cliquez sur **Débloquer** sur la fiche du lecteur (administrateurs seulement). **Désactiver puis réactiver le plugin ne débloque pas** : seul le bouton le fait. Procédure pas à pas : [Débloquer un lecteur](securite.md#proc-debloquer). Si le blocage revient aussitôt, c'est normal tant qu'aucun succès du même type n'a remis le compteur à zéro : voir [Comment fonctionne le blocage](fonctionement.md#comment-fonctionne-le-blocage).
- Si le journal écrit « enregistrement du blocage illisible, lecteur bloqué pour la durée initiale (« Débloquer » sur la fiche) » : l'état du blocage n'a pas pu être lu, le lecteur est bloqué par précaution pour la durée de départ. Cliquez sur **Débloquer**.

<a id="messages-interface-securite"></a>
## Messages de l'interface : blocage, adresse, verrous

Ces messages s'affichent en haut de la page en rouge.

| Message | Cause | Action |
|---|---|---|
| « Limite d'essais invalide : saisissez un nombre entier supérieur ou égal à 1. » | Limite de badge inconnu ou de code faux vide, nulle, négative ou non numérique, à la sauvegarde de la fiche du lecteur | Saisissez 1 ou plus. Rien n'est enregistré tant que la valeur n'est pas corrigée. |
| « Temps de blocage invalide : saisissez un nombre entier de minutes, de 1 à 1440. » | Temps de blocage hors bornes | Saisissez un nombre entier de minutes de 1 à 1440. |
| « Lecteur occupé, réessayez » ; « Inclusion occupée, réessayez » ; « Appairage occupé, réessayez » | Deux actions sur le même élément se sont croisées (deux onglets, deux administrateurs) | Recliquez après quelques secondes. |
| « Lecteur introuvable » | Le lecteur a été supprimé depuis l'ouverture de la page | Rechargez la page. |
| « IP autorisée invalide : saisissez l'adresse IPv4 ou IPv6 du lecteur, ou laissez le champ vide. » ; « IP autorisée refusée : une adresse de bouclage (127.0.0.1, ::1), non spécifiée (0.0.0.0, ::) ou du serveur Jeedom n'est jamais celle d'un lecteur. » | Adresse saisie qui n'est pas une IP, ou qui ne peut pas être celle d'un lecteur | Saisissez l'adresse réelle du lecteur, ou laissez le champ vide. |

<a id="messages-inclusion"></a>
## Messages d'inclusion

| Message | Où | Cause | Action |
|---|---|---|---|
| « L'inclusion n'est pas active » | Interface (clic sur Prolonger) | L'inclusion s'est arrêtée à l'échéance ou a été arrêtée | Cliquez sur **Mode inclusion** pour la relancer. |
| « Élément introuvable ou déjà traité » | Interface (Approuver, Refuser) | L'élément a déjà été approuvé ou refusé (autre onglet, autre administrateur) | Rechargez la page. |
| « Inclusion : limite de créations atteinte. Les lecteurs et badges inconnus présentés ne sont plus créés jusqu'à la fin de l'inclusion. » | Centre de messages | La limite de créations de la fenêtre est atteinte | Arrêtez l'inclusion et relancez-la, ou relevez la limite (configuration du plugin, bloc Inclusion). |
| « Inclusion : limite de … créations atteinte, … non créé (appel ignoré) » | Journal, Avertissement | Idem, pour chaque appel qui aurait créé un élément | Idem. |
| « Inclusion : verrou indisponible, création ignorée (…) » | Journal, Avertissement | Le plugin n'a pas pu poser son verrou de comptage : l'élément n'est pas créé | Recommencez la présentation ; si cela se répète, vérifiez que le dossier temporaire de Jeedom est inscriptible. |
| « L'inclusion était active : la mise à jour du plugin l'a arrêtée. Elle est désormais limitée dans le temps : relancez-la depuis la page du plugin si besoin. » | Centre de messages | Une inclusion ouverte avant la mise à jour est arrêtée | Relancez-la depuis la page du plugin si besoin. |
| « Inclusion : création d'équipements par les lecteurs… » | Centre de messages | Notification regroupée : des éléments ont été créés pendant l'inclusion | Vérifiez qu'ils sont tous attendus ; refusez ou supprimez les autres. |
| Un badge ou un lecteur créé n'ouvre rien | Page du plugin | L'élément est inactif ou « En attente d'approbation » | Activez-le ou approuvez-le : voir [Inclure, approuver ou refuser](securite.md#proc-inclusion). |

<a id="messages-codes"></a>
## Messages sur les codes

| Message | Cause | Action |
|---|---|---|
| « Code refusé : de 1 à 24 chiffres » | Code saisi (formulaire ou `ChangePin` avec `set`) vide, non numérique ou de plus de 24 chiffres | Saisissez de 1 à 24 chiffres. |
| « Ce code est déjà utilisé » | Un autre équipement code porte déjà ce code | Choisissez un autre code, ou générez-en un avec `rnd6` ou `rnd8`. |
| « Impossible de générer un code unique : supprimez des codes inutilisés » | `rnd4`, `rnd6` ou `rnd8` n'a pas trouvé de code libre après plusieurs essais (peu de combinaisons à 4 chiffres) | Utilisez un code plus long, ou supprimez les codes inutilisés. |
| « Code illisible : redéfinissez-le » | Le code enregistré ne peut plus être déchiffré (clé de chiffrement de Jeedom changée ou sauvegarde restaurée sans elle) | Redéfinissez le code. |
| « Code introuvable » | L'équipement code a été supprimé ou n'est plus un code | Rechargez la page. |
| « Enregistrement du code impossible » | Le code n'a pas pu être chiffré ou enregistré | Réessayez ; si cela persiste, consultez le journal `badger2`. |
| Journal : « Code … : code de moins de 4 chiffres, facile à deviner » (Avertissement) | Code très court | Choisissez 4 chiffres ou plus. |
| Journal : « Recherche du code : … code(s) illisible(s) écarté(s) (clé de chiffrement de Jeedom changée ?) » (Erreur) | Des codes enregistrés ne peuvent pas être déchiffrés : ils ne reconnaissent plus rien | Redéfinissez ces codes. |
| Centre de messages : « Plusieurs équipements code portent le même code (il reste valable tant qu'il n'est pas changé) : … » | Codes en double hérités d'avant la mise à jour | Donnez un code différent à chacun. |
| Centre de messages : « Code non converti : redéfinissez-le : … » ; « Code illisible : redéfinissez-le (la clé de chiffrement de Jeedom a-t-elle changé ?) : … » | La mise à jour n'a pas pu convertir ou lire ces codes | Redéfinissez-les. |
| Centre de messages : « Code vide ou hors du clavier du lecteur à vérifier (un code vide s'ouvre en validant sans rien saisir) : … » | Codes vides hérités | Saisissez un vrai code. |
| Centre de messages : « La commande GetPin a été conservée : décochez la case « Ajouter une commande info GetPin » si elle ne sert pas. » | Équipement qui avait déjà GetPin avant la mise à jour | Décochez la case si aucun scénario ne lit la commande. |

<a id="exiger-chiffrement-refuse"></a>
## Exiger le chiffrement : refus et échecs

⚠️ Aucun sketch publié n'envoie encore d'identifiants chiffrés : ces messages ne devraient pas apparaître aujourd'hui en usage normal. Ils concernent le bouton **Exiger le chiffrement pour ce lecteur** du tableau [Posture de sécurité des lecteurs](reference.md#posture-securite).

| Message | Cause | Action |
|---|---|---|
| « Exiger le chiffrement est réservé à un lecteur v1 appairé : appairez-le d'abord. » | Lecteur non appairé | [Appairez-le](reference.md#appairage-appairer). |
| « Exiger le chiffrement est impossible : ce lecteur n'annonce pas le chiffrement de ses identifiants. » | Le lecteur n'annonce pas cette capacité | Rien à faire tant qu'aucun sketch ne l'annonce. |
| « Exiger le chiffrement est impossible pour l'instant : le dernier badge ou code de ce lecteur est arrivé en clair, l'exiger le couperait. » | Dernier identifiant reçu en clair | Attendez un identifiant chiffré. |
| « Exiger le chiffrement est impossible pour l'instant : aucun badge ni code chiffré n'a encore été reçu de ce lecteur. » | Aucun identifiant chiffré reçu | Présentez un badge ou saisissez un code sur ce lecteur. |
| « État du lecteur illisible : ouvrez sa fiche. » | État illisible | Ouvrez la fiche et consultez le journal. |
| Journal : « Appel v1 refusé : identifiant en clair (événement …) alors que les identifiants chiffrés sont exigés pour le lecteur … » (403) | L'exigence est posée et le lecteur envoie un identifiant en clair | Reflashez le lecteur avec un sketch qui chiffre, ou cliquez sur **Ne plus exiger le chiffrement**. |
| Journal : « Appel v1 refusé (adresse …, lecteur …) : identifiant chiffré indéchiffrable (…) : sans effet, non compté comme essai de code » (400) | Le contenu chiffré est illisible (signature juste) | Vérifiez l'appairage et la configuration du sketch. |
| Journal : « Lecteur … : 3 appels chiffrés indéchiffrables de suite : vérifier l'appairage (secret du lecteur et configuration du sketch) » (Erreur) | Échecs répétés | Idem. La page affiche aussi « Échecs de déchiffrement répétés : vérifier l'appairage ». |
| Journal : « Appel v1 du lecteur … : lecture de l'identifiant chiffré impossible (secret ou calcul inutilisable) » (Erreur) | Le secret ne peut pas servir au déchiffrement | [Régénérez le secret](reference.md#regenerer-secret). |

<a id="bandeaux-securite"></a>
## Bandeaux et posture de sécurité

- **Bandeau jaune « Au moins un lecteur utilise l'ancien protocole : il peut être usurpé par un appareil du réseau local »** : au moins un lecteur **actif** est en v0. Il liste les lecteurs concernés. Ce n'est pas une panne : voir [Que faire d'un lecteur qui reste en v0 ?](securite.md#lecteur-v0-durable). Il disparaît quand plus aucun lecteur actif n'est en v0.
- **Bandeau rouge « Le contrôle d'IP d'origine est désactivé : n'importe quel appareil du réseau, ou d'Internet si Jeedom est publié par un tunnel, peut se faire passer pour un lecteur. »** : l'option est décochée dans la configuration du plugin. Recochez-la sauf si vos lecteurs passent par un reverse proxy ou un NAT : voir [Corriger l'IP d'un lecteur et régler le filtrage](securite.md#proc-ip).
- **« Posture de sécurité indisponible : consultez le journal du plugin »** : le tableau n'a pas pu être calculé. Le journal `badger2` écrit « Posture de sécurité indisponible : … » (Erreur). Rechargez la page ; si cela persiste, signalez le message du journal. Les appels des lecteurs ne sont pas affectés.
- **Journal « Posture du lecteur … »** (Erreur) : l'état d'un lecteur n'a pas pu être lu ; le tableau affiche « État illisible ». Ouvrez sa fiche.

<a id="journal-securite-divers"></a>
## Autres messages du journal de la tranche sécurité

Les messages au niveau Avertissement ou Info ne sont écrits que si le niveau de log est monté : voir [Niveau de log](reference.md#niveau-de-log).

| Message | Niveau | Cause | Action |
|---|---|---|---|
| « Appel refusé : paramètre de version répété dans le corps de la requête (adresse …) » | Avertissement | L'appel (réponse 400) contient deux fois le paramètre de version : aucun lecteur ne l'émet | Vérifiez qui appelle cette adresse. |
| « Lecteur … : limite d'essais ou temps de blocage invalide, ramené à 1 » | Avertissement | Une valeur enregistrée est illisible ; le plugin applique 1 | Ouvrez la fiche du lecteur, saisissez des valeurs valides et sauvegardez. |
| « Lecteur … : verrou anti-bruteforce indisponible, compteur mis à jour sans verrou » | Avertissement | Le verrou de comptage n'a pas pu être posé ; le comptage continue sans lui | Passager en général ; si fréquent, vérifiez que le dossier temporaire de Jeedom est inscriptible. |
| « Lecteur … : IP autorisée … remplacée par … (inclusion active) » ; « Appel v1 : lecteur … appelé depuis …, adresse enregistrée … remplacée (inclusion active) » | Avertissement | L'inclusion a enregistré une nouvelle adresse pour le lecteur | Normal si vous l'avez voulu (corriger une IP). Sinon, arrêtez l'inclusion et vérifiez l'adresse. |
| « Lecteur … : IP … remplacée par … (lecteur non verrouillé) » | Info | Un lecteur v0 non verrouillé met son adresse à jour à chaque appel | Normal. |
| « Lecteur … : IP déclarée … non enregistrée (adresse de bouclage ou du serveur, jamais celle d'un lecteur) » | Avertissement | L'appel annonce une adresse qui ne peut pas être celle d'un lecteur | Vérifiez le sketch et son adresse. |
| « Lecteur … : IP autorisée … effacée (adresse invalide ou interdite pour un lecteur) » | Avertissement | Une adresse invalide a été retirée de la fiche | Saisissez l'adresse réelle. |
| « Version des données (n° …) plus récente que ce plugin (n° …) : aucune migration exécutée, version conservée » | Avertissement | Vous êtes revenu à une version antérieure du plugin | Restaurez la sauvegarde Jeedom d'avant la mise à jour : voir [Mettre à jour sans surprise](securite.md#mise-a-jour-sans-surprise). |
| « Version des données illisible : toutes les migrations sont rejouées (idempotentes) » | Avertissement | Le numéro de version des données est illisible | Rien à faire : les migrations sont rejouées sans effet sur des données à jour. |
| « Migration des codes : équipement #… non converti (…) » ; « Migration des codes : équipements illisibles (…) » | Erreur | La conversion d'un code n'a pas abouti | Voir [Migration de données en échec](#migration-donnees-echec). |
| « Import : code de … illisible (ancienne valeur de type inattendu), un code neuf sera généré » | Avertissement | Import depuis Badger : l'ancien code n'a pas pu être repris | Redéfinissez le code de cet équipement. |

## Une question qui reste sans réponse ?

Consultez le [mode debug](reference.md#mode-debug) pour voir les appels reçus, puis ouvrez une discussion sur le forum communautaire de Jeedom en joignant le log `badger2` **sans** secret ni valeur de badge.
