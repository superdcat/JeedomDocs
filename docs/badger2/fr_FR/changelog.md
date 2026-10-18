# Changelog plugin Badger Fork

>**IMPORTANT**
>
>S'il n'y a pas d'information sur la mise à jour, c'est que celle-ci concerne uniquement de la mise à jour de documentation, de traduction ou de texte.

# 19/10/2026

- Documentation : la référence du protocole v1 des futurs lecteurs Badger2 précise le traitement des réponses non signées ou mal signées et l'usage réservé du secret du lecteur (en préparation : les lecteurs déjà installés ne sont pas concernés). <!-- UC009 -->
- Évolution : les futurs lecteurs Badger2 en protocole v1 exigeront une Arduino Mega 2560 ou un ESP ; une Uno ou une Nano garde son sketch actuel (BadgerW5100 ou BadgerENC28J60), qui reste pris en charge et fonctionne comme avant (aucun lecteur déjà installé n'est concerné). <!-- UC003 -->

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
