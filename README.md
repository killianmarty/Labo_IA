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

L'état initial est un état où l'ensemble des tâches éxecutées est vide, l'ensemble des tâches restantes est l'ensemble des tâches de l'input, et le temps actuel est 0.

L'état final est l'ensemble des états dont toutes les tâches sont éxecutées avant expiration.

La fonction de successeur est l'ajout d'une nouvelle tâche à l'ensemble des tâches exécutées.

Le coût de chemin est la date de fin d'éxecution de la tâche.

#### Heuristiques possibles

1. Durée de la tâche (Di - Si)
2. Temps d'arrivée (Si)
3. Délai (Di)