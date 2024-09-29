import random
import copy
import time
import math

inputFile = "./input/input11.txt"

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
    for i in range(9):
        conflicts += len(set(grid[i])) - 9
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
    

    randX = random.randint(0, 8)
    randY = random.randint(0, 8)
    while(isFixed(randX, randY)):
        randX = random.randint(0, 8)
        randY = random.randint(0, 8)

    bestValue = None
    bestHeuristic = float('inf')
    for i in range(1, 10):
        tmp = copy.deepcopy(grid)
        tmp[randY][randX] = i
        tmpHeuristic = heuristic(tmp)
        if(tmpHeuristic < bestHeuristic):
            bestValue = i
            bestHeuristic = tmpHeuristic

    tmp = copy.deepcopy(grid)
    tmp[randY][randX] = bestValue
    return tmp

def countZeros(grid):
    c=0
    for i in range(9):
        for j in range(9):
            if(grid[i][j]==0):
                c+=1
    return c

def HillClimb(grid):
    
    max_iter = 1000
    
    while(True):
        i=0
        currentGrid = copy.deepcopy(grid)
        currentHeuristic = heuristic(currentGrid)
        

        #round of guessing, we consider its stuck if the heuristic does not improve in max_iter iterations
        while(i < max_iter):

            newGrid = getNeighbor(currentGrid)
            newHeuristic = heuristic(newGrid)

            #if solution, we return it
            if(newHeuristic == 0):
                if(countZeros(newGrid)==0):
                    return newGrid
            
            #if the neighbor is better, it becomes the new grid
            if(newHeuristic <= currentHeuristic):   
                i=0 
                currentGrid = newGrid
                currentHeuristic = newHeuristic  
            else:
                i+=1

print("Loading grid from file '" + inputFile + "' ...")
initialGrid = loadGrid(inputFile)
print("Running HillClimb algorithm (alternative version) ...")
startDate = time.time()
result = HillClimb(initialGrid)
executionTime = time.time() - startDate

print("Found a solution :")
printgrid(result)
print(f'Execution time: {math.floor(executionTime)} seconds')