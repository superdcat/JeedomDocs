# Changelog plugin Badger Fork

>**IMPORTANT**
>
>S'il n'y a pas d'information sur la mise à jour, c'est que celle-ci concerne uniquement de la mise à jour de documentation, de traduction ou de texte.

# 20/10/2026

- Ajout : un lecteur Badger2 en protocole v1 peut désormais être appairé depuis sa fiche : le plugin génère son secret (affiché une seule fois), vérifie la signature de chacun de ses appels, refuse les appels rejoués ou repassés en v0 à son nom, et l'administrateur peut régénérer le secret ou rabaisser le lecteur à v0 ; les lecteurs jamais appairés, dont tous les lecteurs déjà installés, fonctionnent exactement comme avant. <!-- UC017 -->
- Documentation : la documentation explique l'appairage d'un lecteur Badger2 en protocole v1 : où le trouver dans la fiche, l'affichage unique du secret, ce qui est refusé ensuite, la régénération du secret et le retour à v0. <!-- UC017 -->
- Ajout : un administrateur peut télécharger depuis la fiche d'un lecteur un fichier de configuration du sketch Badger2 déjà rempli (carte, adresse de Jeedom, identifiant et secret du lecteur) ; le secret d'appairage n'est plus affiché à l'écran, il n'est fourni que dans ce fichier, et un lecteur d'origine n'est en rien modifié par ce téléchargement. <!-- UC018 -->
- Documentation : la documentation explique le téléchargement de la configuration du sketch d'un lecteur v1 (choix de la carte, adresse de Jeedom, Wi-Fi, emplacement du fichier, cas d'un lecteur d'origine) et la nouvelle façon de récupérer le secret après l'appairage. <!-- UC018 -->
- Documentation : la documentation est réorganisée en deux entrées : un tutoriel pas à pas pour débutants, de l'achat du matériel à la première porte ouverte, et une référence technique complète (cartes et capacités, câblage, appairage, compatibilité des anciens lecteurs, console, dépannage détaillé) ; vos anciens lecteurs continuent de fonctionner sans rien changer, et le nouveau sketch exige une Mega 2560 ou un ESP. <!-- UC099 -->
- Correctif : import depuis Badger : si Badger d'origine n'avait jamais réglé l'inclusion, l'import n'efface plus l'option d'inclusion de Badger Fork. Si vous aviez activé l'inclusion dans Badger Fork avant un import, vérifiez son état dans la page du plugin. <!-- UC017 -->
- Évolution : le sketch Badger2 (protocole v1) compile désormais tel quel : la ligne de sécurité BADGER2_DEVELOPPEMENT_ACCEPTE n'existe plus, ni dans le sketch ni dans le fichier de configuration téléchargé depuis la fiche d'un lecteur, appairé ou non ; une telle ligne restée dans un ancien fichier est simplement ignorée. Le sketch v1 n'a toujours pas été essayé sur une carte réelle : gardez de quoi revenir au sketch d'origine. Les lecteurs d'origine ne sont pas concernés. <!-- UC099 -->
- Évolution : sur un lecteur ESP doté de la mise à jour à distance (sketch Badger2), la commande console « ota - » désactive désormais la mise à jour à distance immédiatement : l'ancien mot de passe ne sert plus, sans attendre de redémarrage. Les lecteurs Mega et les lecteurs d'origine ne sont pas concernés. <!-- UC014 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 ne promet plus d'empreinte de configuration (cfg) ; ce champ reste accepté mais sans effet (les lecteurs déjà installés ne sont pas concernés). <!-- UC018 -->
- Évolution : le protocole v1 des futurs lecteurs Badger2 ne comporte plus du tout d'empreinte de configuration : ni champ, ni capacité, ni libellé dans la fiche du lecteur ; un lecteur qui enverrait encore ces données les verrait ignorées comme toute donnée inconnue. Les lecteurs déjà installés ne sont pas concernés. <!-- UC018 -->

# 19/10/2026

- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 précise le traitement des réponses non signées ou mal signées et l'usage réservé du secret du lecteur (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC009 -->
- Évolution : les futurs lecteurs Badger2 en protocole v1 exigeront une Arduino Mega 2560 ou un ESP ; une Uno ou une Nano garde son sketch actuel (BadgerW5100 ou BadgerENC28J60), qui reste pris en charge et fonctionne comme avant (aucun lecteur déjà installé n'est concerné). <!-- UC003 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 précise les retours que le lecteur sait appliquer (ouverture de la gâche, voyant, buzzer, heure) et les conditions de leur prise en compte selon qu'un secret est configuré ou non (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC010 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 décrit le mode hors ligne : refus par défaut quand Jeedom est injoignable, liste blanche locale d'empreintes signée par le plugin ou, à vos risques, ouverture libre, et remise des passages à Jeedom à son retour (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC011 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 décrit les ordres signés que Jeedom pourra envoyer au lecteur (ouverture de la gâche, voyant, buzzer, battement, resynchronisation de la liste blanche, redémarrage) et leur accusé de réception ; le port d'ordres ne doit jamais être joignable depuis Internet (en préparation : les lecteurs déjà installés ne sont pas concernés) <!-- UC012 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 mentionne deux capacités informatives, la console de provisionnement (configuration et diagnostic par le port série du lecteur) et la LED d'état (en préparation : les lecteurs déjà installés ne sont pas concernés) <!-- UC013 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 mentionne la capacité informative de mise à jour à distance du firmware, protégée par mot de passe et réservée aux cartes ESP (en préparation : les lecteurs déjà installés ne sont pas concernés) <!-- UC014 -->
- Ajout : le plugin reçoit désormais les appels des futurs lecteurs Badger2 en protocole v1 : un lecteur v1 est reconnu par son identifiant et par son adresse enregistrée, ses badges et codes déclenchent les mêmes commandes qu'un lecteur actuel, et Analyse > Santé affiche « v1 : supportée » (les lecteurs déjà installés fonctionnent exactement comme avant). <!-- UC015 -->
- Ajout : la fiche de chaque lecteur affiche désormais son protocole, son firmware, sa carte et son transport, les capacités qu'il annonce et la date de sa dernière annonce (« v0 (sketch d'origine) » pour un lecteur d'origine, « En attente de l'annonce du lecteur » pour un lecteur v1 qui ne s'est pas encore annoncé). <!-- UC016 -->
- Documentation : nouvelle section « Version, firmware et capacités de chaque lecteur ». <!-- UC016 -->

# 18/10/2026

- Correctif : les traductions anglaise, allemande et espagnole de la configuration du plugin et des équipements, et des messages de migration depuis Badger, sont complétées. <!-- UC020 -->
- Documentation : publication de la référence technique du protocole v1 des futurs lecteurs Badger2 (en préparation : ni le plugin ni les sketches actuels ne l'utilisent encore ; les lecteurs déjà installés ne sont pas concernés). <!-- UC001 -->
- Ajout : le plugin reconnaît la version de protocole de chaque appel de lecteur : les lecteurs actuels (sketch d'origine, ancienne ou nouvelle adresse) fonctionnent exactement comme avant, un appel annonçant une version inconnue est refusé avec un avertissement explicite, et les versions prises en charge sont visibles dans Analyse > Santé. <!-- UC002 -->
- Documentation : la page de présentation et la référence du protocole des lecteurs décrivent la reconnaissance des versions et leur affichage dans Analyse > Santé. <!-- UC002 -->
- Ajout : nouveau mode debug réservé à l'administrateur, activable 15, 30 ou 60 minutes depuis la page du plugin : il montre en clair ce que les lecteurs envoient et ce que le plugin en fait, avec une option « observation seule » pour mettre au point un lecteur sans rien déclencher. <!-- UC021 -->
- Évolution : les badges et codes reçus des lecteurs ne sont plus écrits en clair dans le log du plugin, y compris dans le nom d'un badge ou d'un code qui les contiendrait. <!-- UC021 -->
- Documentation : la documentation décrit le mode debug : activation, ce qui est montré ou jamais montré, arrêt automatique, et précautions avec l'observation seule. <!-- UC021 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 décrit le champ facultatif port, qui indique lequel des deux lecteurs Wiegand d'un même boîtier a lu le badge (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC005 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 décrit la saisie de code au clavier : badge suivi d'un code envoyés ensemble et envoi touche par touche, deux options désactivées par défaut (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC006 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 précise le sens de l'état des entrées (bouton de sortie, sonnette, autoprotection, entrées analogiques) et les valeurs de l'événement de porte (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC007 -->
- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 décrit l'annonce de démarrage (capacités, cause du redémarrage), le battement de cœur et son compteur d'événements perdus, ainsi que la période de battement que le plugin peut ajuster (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC008 -->

# 17/10/2026

- Correctif : sécurité : les lecteurs ne sont plus acceptés que depuis une adresse IP locale (réseau privé). Un appel venant d'Internet est refusé et signalé dans le log. <!-- UC101 -->
- Correctif : sécurité : les appels des lecteurs arrivant par un tunnel ou un reverse proxy (cloudflared, accès distant…) sont désormais refusés, et l'adresse de bouclage ou du serveur n'est plus jamais enregistrée comme IP d'un lecteur. <!-- UC101 -->

# 22/09/2026

- Correctif : les liens de documentation, de changelog et de téléchargement des librairies Arduino pointent de nouveau vers un emplacement valide
- Correctif : les liens de documentation et de changelog pointent vers le site publie jeedomdocs.decastro.fr
- Nouveauté : publication du plugin sur le Market, avec import des équipements et rétro-compatibilité de l'ancien plugin Badger
- Correctif : page de configuration : tant que l'ancien plugin Badger est installé, le bouton d'URL de compatibilité reste en mode « Ajouter » et grisé, au lieu de proposer à tort de la retirer
- Correctif : les librairies Arduino (EtherCard et Wiegand) sont désormais téléchargeables depuis le site de documentation : les liens de la page de configuration fonctionnent de nouveau
- Correctif : import de la configuration Badger : le bouton renvoyait une erreur 500 sans aucun message. La cause du blocage est maintenant affichée et journalisée, et un équipement en échec n'interrompt plus l'import des autres.
- Correctif : import de la configuration Badger : l'import échouait sur tous les équipements tant que le plugin Badger était installé (Jeedom interdit deux équipements de même nom dans le même objet). Les équipements sont maintenant importés sans objet parent, et y sont replacés automatiquement dès la désinstallation de Badger.
- Ajout : migration depuis Badger : une case à cocher (activée par défaut) reporte automatiquement, partout dans Jeedom, les références aux commandes de Badger sur celles de Badger Fork — scénarios, vues, design, interactions et droits utilisateur. Sans elle, ces éléments pointeraient vers des commandes supprimées à la désinstallation de Badger.
- Documentation : ajout d'une page décrivant toute la procédure de migration depuis l'ancien plugin Badger (import, case de remplacement des commandes, objets parents, désinstallation, URL de compatibilité). L'installation est désormais documentée uniquement depuis le Market.

# 01/06/2022

- Divers petits correctifs (liens, images, etc)
- Ajout d'un système pour oublier automatiquement les chiffres saisis au bout de 30 s (pour éviter que la prochaine saisie d'un code complet soit en erreur)
- Ajout de la gestion des entrées analogiques pour utiliser des boutons poussoir ou le bouton sonnette d'un digicode
- Mise à jour de la documentation

# 01/05/2022

- Reprise du plugin
- Correctif : problème de class object
- Correctif : liens des sketchs
- Correctif : liens de documentation
- Suppression des bords blancs sur l'icône
