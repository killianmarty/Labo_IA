import random
import copy
import time
import sys
import getopt
import math

MAX_ITER = 200
nb_iter = 0

inputFile = "input/input10.txt"

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
    #This function fills the free boxes in each row with numbers

    grid = copy.deepcopy(grid)
    for row in range(9):

        availableNumbers = list(range(1, 10))
        
        #Randomize the order of the numbers
        random.shuffle(availableNumbers)

        for val in grid[row]:
            if(val!=0):
                availableNumbers.remove(val)

        for col in range(9):
            if(not isFixed(col, row)):
                grid[row][col] = availableNumbers[0]
                availableNumbers.pop(0)
    
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
    #we choose a random row, and we chose two random unfixed boxes to swap
    tmp = copy.deepcopy(grid)

    row = random.randint(0, 8)
    x1 = random.randint(0, 8)
    x2 = random.randint(0, 8)

    while(isFixed(x1, row) or isFixed(x2, row) or x1 == x2):
        row = random.randint(0, 8)
        x1 = random.randint(0, 8)
        x2 = random.randint(0, 8)

    swap(tmp, x1, row, x2, row)

    return tmp


def HillClimb(grid):
    
    global nb_iter
    max_iter = MAX_ITER
    
    while(True):
        i=0
        currentGrid = fillInitialGrid(grid)
        currentHeuristic = heuristic(grid)
        

        #round of guessing, we consider its stuck if the heuristic does not improve in max_iter iterations
        while(i < max_iter):

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

            else:
                i+=1

            nb_iter += 1



# MAIN CALLS
print("Loading grid from file '" + inputFile + "' ...")
initialGrid = loadGrid(inputFile)

print("Running Hill Climbing algorithm...")
startDate = time.time()
result = HillClimb(initialGrid)
executionTime = time.time() - startDate

print("Found a solution :")
printgrid(result)
print(f'Execution time : {math.floor(executionTime)} seconds.')
print(f'Number of iterations : {nb_iter}.')