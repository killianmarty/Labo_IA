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

Cette fonction reprend l'algorithme vu en cours, en ajoutant une vérification afin d'éviter de visiter plusieurs fois un état. En effet, cette vérification est nécéssaire afin d'éviter de tourner en boucle.

Une fois l'état objectif atteint, la fonction "explore" reconstruit le chemin de la solution en remontant les parents depuis l'état final, et retourne la solution.

Enfin, j'ai crée des fonctions principales pour chaque algorithme de recherche (Largeur, Profondeur, A*) qui s'occupent de charger la grille depuis le fichier, appeller la fonction "explore" avec les bons paramètres, afficher le chemin final, et écrire le résultat d'exécution dans un fichier.

#### Observations

Ma première observation, est que l'algorithme A* est le plus rapide, suivi par le parcours en largeur.

En revanche, l'exécution du parcours en profondeur est significativement plus longue et retourne un chemin bien plus long.


### Algorithmes gloutons

#### Definition du problème

Un état est l'ensemble des tâches exécutées, des tâches retantes, et du temps actuel.

L'état initial est un état où l'ensemble des tâches exécutées est vide, l'ensemble des tâches restantes est l'ensemble des tâches de l'input, et le temps actuel est 0.

L'état objectif est un état dans lequel on exécute le maximum de tâches.

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

## Laboratoire 1 : Partie B

Dans cette partie l'objectif est de résoudre une grille de sudoku par deux méthodes : le Hill Climbing et le Backtracking.

### Méthode 1 : Hill Climbing

L'objectif de cette méthode est de partir d'un état initial et de choisir un voisin qui améliore l'heuristique de l'état initial, si c'est le cas, il devient l'état courant et on répète l'opération jusqu'a avoir une solution admissible.

Dans le cas du sudoku, un état est une grille de sudoku (matrice 9x9 avec des 0 pour réprésenter une case vide), l'heuristique est le nombre de conflits sur la grille, et une solution admissible est une grille sans conflits.

**NOTE : Le format d'entrée est un fichier texte extrait du site https://qqwing.com/generate.html en mode "compact".**

Pour implémenter cette méthode, j'ai créé 2 versions de l'algorithme .

#### Version principale : swap de cases

##### Principe

Dans cette version, la grille initiale est une grille dont on remplit chaque ligne par tous les chiffres de 1 à 9 (en évitant les cases fixées par la grille de départ), et un voisin de la grille est la même grille, mais dont on a échangé deux cases (non fixées) d'une même ligne.

Pour choisir l'état voisin, on choisit une ligne aléatoirement, puis on choisit deux cases de cette ligne aléatoirement que l'on va échanger.

##### Utilisation

###### Version python

Modifier la variable "inputFile" dans Labo1/PartieB/hill_climbing_main.py pour séléctionner le fichier d'entrée. Puis :

```bash
cd Labo1/PartieB/
python3 hill_climbing_main.py
```

###### Version C avec multithreading

Comme un algorithme de Hill Climbing peut être très long à l'éxécution, j'ai décidé d'implémenter une version en C avec une composante de multithreading pour améliorer les performances. Voici les instructions pour l'éxécuter (fonctionne sur Linux, je n'ai pas testé sur Windows):

**Optionnel : modifier le nombre de threads dans le define NUM_THREADS du fichier main_version.c (par défaut à 8 threads).**

```bash
cd Labo1/PartieB/
make
./hill_climbing_main chemin_relatif_du_fichier_input
```

#### Version alternative : remplissage de case

Dans cette version, la grille initiale est la grille de départ dans le fichier d'input, un voisin est la même grille mais avec une case aléatoire non fixée remplie par un nombre aléatoire entre 1 et 9.

##### Utilisation

Modifier la variable "inputFile" dans Labo1/PartieB/hill_climbing_alt.py pour séléctionner le fichier d'entrée. Puis :

```bash
cd Labo1/PartieB/
python3 hill_climbing_alt.py
```

#### Performances

Après de nombreux tests, la version principale à en moyenne un temps d'éxécution plus court, cependant, il reste très long pour des grilles dont la solution n'est pas évidente (grille de niveau simple/easy/intermadiate/expert).

Pour un sudoku de niveau "Simple", l'éxecution de la version C avec 8 threads prends environ 40 minutes sur ma machine.

Ainsi, l'algorithme de Hill Climbing n'est pas adapté pour résoudre efficacement un sudoku.

### Méthode 2 : Backtracking

#### Principe

La méthode de backtracking consiste à ajouter des valeurs dans des cases vides jusqu'à ne plus avoir de possibilités. Lorsqu'il n'y a plus de possibilités, si c'est parce qu'il n'y a plus de cases vides alors le sudoku est résolu, sinon, on teste une autre valeur dans la case, si il n'y a plus de valeurs possibles, on remonte dans la case vide précédente et on recommence.

C'est donc un cas particulier du parcours en profondeur. Pour l'implémenter, on peut utiliser un algorithme qui utilise une liste frontière comme dans les parties précédentes et trier cette liste en choisissant la case avec le plus de possibilités, puis les valeurs qui réduisent le plus le nombre total de possibilité de la grille.

Or, une implémentation plus simple est une implémentation récursive qui choisit la première case vide, la remplit avec toutes les valeurs possibles, et itère de façon récursive.

#### Utilisation

Modifier la variable "inputFile" dans Labo1/PartieB/backtracking.py pour séléctionner le fichier d'entrée. Puis :

```bash
    cd Labo1/PartieB/
    python3 backtracking.py
```

#### Observations

Cette méthode est beaucoup plus rapide que le Hill Climbing, elle est quasiment instantanée. Elle est donc plus adaptée pour résoudre un sudoku.

## Ce que j'ai appris dans ce laboratoire

Ce laboratoire m'a permis d'apprendre à implémenter les algorithmes de parcours d'arbres, ce que je n'avais jamais fait auparavant. J'ai aussi découvert des applications des arbres en IA que je ne soupçonnais pas. J'ai également appris à implémenter un algorithme de Hill Climbing quand on ne peut pas calculer le gradient (j'ai déjà implémenté une descente du gradient auparavant). De plus j'ai découvert le Backtracking.

Cependant, j'ai déjà implémenté des algorithmes gloutons auparavant.

En conclusion, j'ai découvert des applications de l'IA différentes de ce à dont on peut penser quand on pense à l'IA (réseaux de neuronnes etc...).







## Laboratoire 2 : Partie A

### Familiarisation avec le langage

Pour me familiariser avec le langage, j'ai testé les deux premiers exemples et l'exemple de coloriage fournis au lien suivant : https://www.dbai.tuwien.ac.at/proj/dlv/tutorial/

Tout compile bien et fontionne bien.

J'ai ensuite modifié l'exemple de coloriage pour qu'il corresponde à celui du cours. Cela fonctionne bien et le fichier est disponible dans "Labo2/PartieA/coloring2.dl".

Enfin, j'ai corrigé les "checks" de l'exemple des 8-reines. En effet, la verification des diagonales ne couvrait pas tous les cas en fonction de si X1 > X2 et Y1 > Y2 ou pas. Ce qui retournait une erreur "constraint not safe".

J'ai donc modifié les contraintes fortes pour utiliser des comparaisons de valeurs absolues afin d'éviter ce problème. L'avantage de cette implémentation est que l'on peut vérifier qu'il n'y a pas de reine dans la même colonne et dans les mêmes diagonales, uniquement avec cette ligne de contrainte :

```dlv
:- q(X1,Y1), q(X2,Y2), #absdiff(X1, X2, N), #absdiff(Y1, Y2, N), N <> 0.
```