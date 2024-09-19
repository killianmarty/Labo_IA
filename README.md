# Laboratoire 6GEI608 (Intelligence artificielle et reconnaissance des formes)

## Auteur

Killian Marty

## Laboratoire 1 : partie A

### Problème avec un état objectif (8-puzzle)

#### Structure de données

Pour ce problème j'ai choisi d'implémenter les algorithmes de recherches en Python.

La structure de données que j'ai utilisé pour représenter un état est un array dans lequel l'index de chaque valeur représente sa position dans la grille.

Par exemple la grille suivante :

|   |   |   |
| - | - | - |
| 7 | 2 | 4 |
| 5 |   | 6 |
| 8 | 3 | 1 |

Est représentée comme ceci en Python :

```python
[7, 2, 4, 5, 0, 6, 8, 3, 1]
```

Ensuite j'ai également utilisé une structure de "noeud" qui contient le parent direct, le coût, la grille, et l'action réalisée pour l'atteindre.

#### Implémentation

Comme les trois algorithmes de recherches sont basés sur le même algorithme mais avec uniquement la façon de trier la frontière qui varie, j'ai décidé de n'implémenter qu'une fonction de recherche générique "explore" à laquelle je passe en paramètre la fonction responsable d'ajouter/trier des éléments à la frontière.

Cette fonction reprend l'algorithme vu en cours, en ajoutant une vérification afin d'éviter de visiter plusieurs fois un état. En effet, cette vérification est nécéssaire avec d'éviter de tourner en boucle.

Une fois l'état objectif atteint, la fonction "explore" reconstruit le chemin de la solution en remontant les parents depuis l'état final, et retourne la solution.

Enfin, j'ai crée des fonctions principales pour chaque algorithme de recherche (Largeur, Profondeur, A*) qui se chargent de charger la grille depuis le fichier, appeller la fonction "explore" avec les bons paramètres, afficher le chemin final, et écrire le résultat d'exécution dans un fichier.

#### Observations

Ma première observation, est que l'algorithme A* est le plus rapide, suivi par le parcours en largeur.

En revanche, l'exécution du parcours en profondeur est significativement plus longue et retourne un chemin bien plus long.


### Algorithmes gloutons

#### Definition du problème

Un état est l'ensemble des tâches exécutées, des tâches retantes, et du temps actuel.

L'état initial est un état où l'ensemble des tâches exécutées est vide, l'ensemble des tâches restantes est l'ensemble des tâches de l'input, et le temps actuel est 0.

L'état objectif est l'ensemble des états dont toutes les tâches sont exécutées avant expiration.

La fonction de successeur est l'ajout d'une nouvelle tâche à l'ensemble des tâches exécutées, le retrait de celle-ci de l'ensemble des tâches restantes et la mise à jour du temps actuel.

Le coût de chemin est la date de fin d'éxecution de la tâche.

#### Heuristiques possibles

1. Durée de la tâche (Di - Si)
2. Temps d'arrivée (Si)
3. Délai (Di)

#### Heuristique possible pour A*

Le nombre de tâches restantes à exécuter est une heuristique possible pour A*, car cette heuristique ne surestime pas le coût étant donné que le la durée d'une tâche est supérieure ou égale à 1.

#### Analyse de l'applicabilité dans la vie réelle

Les résultats avec A* ne permettent pas d'exécuter toutes les tâches avec les inputs fournis, tout comme les algorithmes gloutons. Ainsi, il n'est pas nécéssaire d'utiliser des ressources pour exécuter un algorithme de type A* alors qu'un algorithme glouton peut donner un résultat similaire en utilisant moins de ressources.

Cette hypothèse est d'autant plus vraie que dans la vie réelle, le nombre de tâches à exécuter est bien plus grand que dans les inputs et les "conflits" sont donc plus fréquents.