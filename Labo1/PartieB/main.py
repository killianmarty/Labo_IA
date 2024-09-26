import random
import copy
import time
import sys
import getopt

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
        if(('--shuffle', '') in opts):
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
    #we choose a random row, and we find the best pair of x1 and x2 to swap
    tmp = copy.deepcopy(grid)

    row = random.randint(0,8)
    bestx1=None
    bestx2=None
    bestHeuristic = float('inf')

    for x1 in range(9):
        for x2 in range(x1, 9):
            if((isFixed(x1, row) or isFixed(x2, row))):
                continue

            swap(tmp, x1, row, x2, row)
            newHeuristic = heuristic(tmp)
            swap(tmp, x1, row, x2, row)

            #TODO <= or < ?
            if(newHeuristic < bestHeuristic):
                bestHeuristic = newHeuristic
                bestx1 = x1
                bestx2 = x2

    swap(tmp, bestx1, row, bestx2, row)

    return tmp


def HillClimb(grid):
    
    max_iter = 250
    if(len(args)!=0):
        max_iter = int(args[0])
        print(max_iter)
    
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

                currentGrid = newGrid
                currentHeuristic = newHeuristic
                

            i+=1

# options
opts = []
args = []

try:

   opts, args = getopt.getopt(sys.argv[1:], "s:", ["shuffle"])

except getopt.GetoptError as err:

   print(err)

print(opts, args)



# MAIN CALLS

initialGrid = loadGrid("./input/input11.txt")
startDate = time.time()
result = HillClimb(initialGrid)
executionTime = time.time() - startDate

printgrid(result)
print(executionTime)