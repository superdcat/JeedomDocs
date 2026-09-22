# Changelog plugin Badger Fork

>**IMPORTANT**
>
>S'il n'y a pas d'information sur la mise à jour, c'est que celle-ci concerne uniquement de la mise à jour de documentation, de traduction ou de texte.

# 22/09/2026

- Correctif : les liens de documentation, de changelog et de téléchargement des librairies Arduino pointent de nouveau vers un emplacement valide
- Correctif : les liens de documentation et de changelog pointent vers le site publie jeedomdocs.decastro.fr
- Nouveauté : publication du plugin sur le Market, avec import des équipements et rétro-compatibilité de l'ancien plugin Badger
- Correctif : page de configuration : tant que l'ancien plugin Badger est installé, le bouton d'URL de compatibilité reste en mode « Ajouter » et grisé, au lieu de proposer à tort de la retirer
- Correctif : les librairies Arduino (EtherCard et Wiegand) sont désormais téléchargeables depuis le site de documentation : les liens de la page de configuration fonctionnent de nouveau
- Correctif : import de la configuration Badger : le bouton renvoyait une erreur 500 sans aucun message. La cause du blocage est maintenant affichée et journalisée, et un équipement en échec n'interrompt plus l'import des autres.
- Correctif : import de la configuration Badger : l'import échouait sur tous les équipements tant que le plugin Badger était installé (Jeedom interdit deux équipements de même nom dans le même objet). Les équipements sont maintenant importés sans objet parent, et y sont replacés automatiquement dès la désinstallation de Badger.

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
