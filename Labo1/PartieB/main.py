import random
import copy

def loadGrid(src):
    matrix=[]
    f = open(src, 'r')
    for line in f.readlines():
        if(line=='\n'):
            break
        matrix.append([int(x) for x in list(line.replace(".", "0"))[:-1]])
        

    f.close()
    return matrix

def heuristic(grid):
    #Here heuristic is the number of conflicts and we want to minimize it

    conflicts = 0
    # Row: No need to count conficts on rows because the elements are unique on rows

    # Column
    for j in range(9):
        col = [grid[i][j] for i in range(9)]
        conflicts += len(set(col)) - 9
    # Square 3x3
    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            sub_grid = []
            for i in range(3):
                for j in range(3):
                    sub_grid.append(grid[x+i][y+j])
            conflicts += len(set(sub_grid)) - 9

    return -conflicts


def fillInitialGrid(grid):
    #this function fills the free boxes in each row with numbers in disorder
    grid = copy.deepcopy(grid)
    for row in range(9):
        unset = [i for i in range(1, 10)]
        for val in grid[row]:
            if(val!=0):
                unset.remove(val)
        for col in range(9):
            if(not isFixed(col, row)):
                rand = random.randint(0, len(unset)-1)
                grid[row][col] = unset[0]
                unset.pop(0)
    
    return grid

def printgrid(grid):
    for line in grid:
        string = ""
        for number in line:
            string += str(number) + " "
        print(string)
    print()

def isFixed(x, y):
    return initialGrid[y][x] != 0

def swap(grid, x1, y1, x2, y2):
    tmp = grid[y2][x2]
    grid[y2][x2] = grid[y1][x1]
    grid[y1][x1] = tmp


def getNeighbor(grid):
    #we choose a random row, and we find the best pair of x1 and x2 to swap
    tmp = copy.deepcopy(grid)

    row = random.randint(0,8)
    bestx1=0
    bestx2=0
    bestHeuristic = 999
    for x1 in range(9):
        for x2 in range(x1, 9):
            if(isFixed(x1, row) or isFixed(x2, row)):
                continue

            swap(tmp, x1, row, x2, row)
            newHeuristic = heuristic(tmp)
            swap(tmp, x1, row, x2, row)

            #TODO <= or < ?
            if(newHeuristic <= bestHeuristic):
                bestHeuristic = newHeuristic
                bestx1 = x1
                bestx2 = x2
                bestrow = row

    swap(tmp, bestx1, row, bestx2, row)

    return tmp


def HillClimb(grid):
    
    max_iter = 100
    
    while(True):
        i=0
        currentGrid = fillInitialGrid(grid)
        currentHeuristic = heuristic(grid)

        #round of guessing, we consider its stuck if the heuristic does not improve in max_iter iterations
        while(i < max_iter * 10/currentHeuristic):

            newGrid = getNeighbor(currentGrid)
            newHeuristic = heuristic(newGrid)

            #if solution, we return it
            if(newHeuristic == 0):
                return newGrid
            
            #if the neighbor is better, it becomes the new grid
            if(newHeuristic < currentHeuristic):
                i=0
                currentGrid = newGrid
                currentHeuristic = newHeuristic
                print(newHeuristic)

            i+=1


initialGrid = loadGrid("input/input5.txt")
result = HillClimb(initialGrid)
printgrid(result)