# Migration depuis le plugin Badger

**Badger Fork** (`badger2`) est un fork du plugin **Badger** (`badger`) : même matériel, mêmes sketches,
mais un identifiant de plugin différent. Les deux peuvent cohabiter le temps de la bascule, et une
procédure guidée reprend votre configuration existante.

Tout se passe dans **Plugins > Gestion des plugins > Badger Fork**, section **Migration depuis Badger**.

> **Faites une sauvegarde Jeedom avant de commencer.** La migration recrée des équipements et peut
> modifier vos scénarios, vues et droits. Une sauvegarde est le seul retour en arrière possible.

## L'ordre des opérations n'est pas négociable

Les trois étapes ont des prérequis **opposés** : elles ne peuvent pas être faites dans un autre ordre.

1. **Importer la configuration de Badger** — *avant* de désinstaller Badger, car sa désinstallation
   supprime ses équipements de la base Jeedom.
2. **Désinstaller Badger.**
3. **Ajouter l'URL de compatibilité** — *après* la désinstallation, car celle-ci efface le dossier du
   plugin d'origine, et donc le fichier de compatibilité s'il avait été posé avant.

La page de configuration applique ces règles toute seule : chaque bouton reste grisé tant que son
prérequis n'est pas rempli, et un encart rappelle l'ordre tant que Badger est encore installé.

## Étape 1 — Importer la configuration de Badger

Le bouton **Importer la configuration de Badger** reprend tous vos lecteurs, badges et codes, avec
leurs commandes, leurs noms personnalisés, leur catégorie, leur affichage et le réglage
« Autoriser l'inclusion de devices inconnus ». Un compteur à côté du bouton indique combien
d'équipements Badger sont encore présents en base.

L'import est **relançable** : les équipements déjà repris ne sont pas dupliqués.

### La case « Remplacer partout dans Jeedom les anciennes commandes par les nouvelles »

Cochée par défaut, elle reporte sur les commandes de Badger Fork toutes les références aux commandes de
Badger, dans :

- les **scénarios** et leurs expressions,
- les **variables** et les **listeners**,
- les **vues**, le **design 2D** et le **design 3D**,
- les **interactions**,
- les **droits et options** des utilisateurs.

**Sans elle, ces éléments continueront de pointer vers des commandes que la désinstallation de Badger
supprimera** : scénarios muets, tuiles vides, interactions sans effet. Si vous avez déjà importé sans
la cocher, relancez simplement l'import en la cochant — le report se fait aussi pour les équipements
déjà repris.

### Pourquoi les équipements arrivent sans objet parent

Jeedom interdit deux équipements portant le **même nom dans le même objet**. Tant que Badger est
installé, son équipement occupe déjà la place. Les équipements importés sont donc créés **sans objet
parent**, en mémorisant l'objet visé.

Un bandeau orange vous indique combien d'équipements sont dans cet état. **Ils y retournent
automatiquement** dès que Badger est désinstallé : il suffit de rouvrir la page de configuration du
plugin, ou d'attendre la prochaine mise à jour de Badger Fork.

### Si un équipement échoue

L'import ne s'arrête pas au premier problème : chaque équipement est traité indépendamment. Le compte
rendu affiché en fin d'import indique combien ont été importés, combien étaient déjà présents, combien
sont en échec et combien attendent leur objet parent. Le détail de chaque échec est dans le log
**badger2** (*Analyse > Logs*).

## Étape 2 — Désinstaller Badger

Une fois l'import vérifié, désinstallez le plugin **Badger** d'origine.

> ⚠️ La désinstallation **supprime définitivement les équipements de Badger** de la base Jeedom. Ne la
> faites qu'après avoir vérifié que tout est bien repris côté Badger Fork.

Au retour sur la page de configuration de Badger Fork, les équipements importés retrouvent leur objet
parent et le bandeau orange disparaît.

## Étape 3 — Ajouter l'URL de compatibilité

Les lecteurs déjà en service appellent l'ancienne adresse du plugin Badger, qui est **figée dans le
firmware de l'Arduino** : ils n'iront pas chercher la nouvelle tout seuls. Deux solutions.

### Solution A — Reflasher les Arduino (recommandée à terme)

Les sketches à jour sont téléchargeables depuis la page de configuration du plugin. C'est la solution
propre : une seule adresse, plus de fichier de compatibilité à maintenir.

### Solution B — Activer l'URL de compatibilité

Le bouton **Ajouter l'URL de compatibilité avec Badger1** pose un petit fichier de redirection à
l'ancienne adresse. Vos lecteurs continuent de fonctionner **sans être reflashés**.

- Le bouton n'est disponible **qu'une fois Badger désinstallé** : avant, il écraserait le plugin encore
  en place, et la désinstallation effacerait ensuite le fichier.
- L'état est affiché en permanence (*Ancienne URL active* / *inactive*).
- Le bouton **Retirer l'URL de compatibilité** la désactive, une fois tous vos lecteurs reflashés.
- Ce choix est mémorisé : une désactivation puis réactivation du plugin ne le perd pas.

## Vérifications après migration

- Vos lecteurs, badges et codes apparaissent bien dans **Badger Fork**, dans les bons objets.
- Vos scénarios se déclenchent toujours à la présentation d'un badge ou d'un code.
- Le log **badger2** (*Analyse > Logs*) enregistre bien les présentations.
- Si vous n'avez pas reflashé vos Arduino, l'URL de compatibilité est **active**.

En cas de doute, le log **badger2** est le premier endroit à regarder : import, réaffectation des objets
parents, pose et retrait de l'URL de compatibilité y sont tous tracés.
