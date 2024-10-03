import time
import math

inputFile = "input/input13.txt"

nb_iter = 0

def loadGrid(src):
    matrix=[]
    f = open(src, 'r')
    for line in f.readlines():
        if(line=='\n'):
            break
        matrix.append([int(x) for x in list(line.replace(".", "0"))[:-1]])
        

    f.close()
    return matrix

def printGrid(grid):
    for line in grid:
        string = ""
        for number in line:
            string += str(number) + " "
        print(string)
    print()

def isPossible(grid, x, y, value):
    for i in range(9):
        if grid[y][i] == value:
            return False
        if grid[i][x] == value:
            return False
        if grid[y//3*3+i//3][x//3*3+i%3] == value:
            return False
    return True

def findNextEmptyBox(grid):
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                return [x, y]
    return None

def backtracking(grid):
    global nb_iter
    nb_iter+=1
    emptyBox = findNextEmptyBox(grid)

    if emptyBox == None:
        return True
    x, y = emptyBox

    for i in range(1, 10):
        if isPossible(grid, x, y, i):
            grid[y][x] = i
            if backtracking(grid):
                return True
            grid[y][x] = 0
    return False



print("Loading input grid...")
matrix = loadGrid(inputFile)

print("Running backtracking method...")

startDate = time.time()

backtracking(matrix)

executionTime = time.time() - startDate

print("Found solution :")
printGrid(matrix)
print(f'Execution time : {math.floor(executionTime)} seconds.')
print("Number of iterations: ", nb_iter)