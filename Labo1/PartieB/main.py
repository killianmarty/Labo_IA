# grid = 9x9 matrix
# value = number of values placed without conflict
# node = grid and value

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

def checkUnique(array):
    c=0
    for e in array:
        if(e==0):
            c += 1
    return len(array) > len(set(array)) + c -1

def evaluate(grid):
    c=0

    #check for same number on same line
    for i in range(9):
        if(checkUnique(grid[i])):
            c+=1

    #check for same number on same column
    for i in range(9):
        if(checkUnique(grid[:][i])):
            c+=1  

    #check for same number on same square
    for i in range(9):
        tmp = []
        for j in range(9):
            tmp.append(grid[(i//3)*3 + j//3][(i%3)*3 + j%3])
        if(checkUnique(tmp)):
            c+=1

    return c

def createNode(grid, conflicts):
    return {
        "grid": grid,
        "conflicts": conflicts
    }

#def getNeighbor(grid):
    # randomIndex = random.randint(0, 8)
    # while(grid[randomIndex//3][randomIndex%3]!=0):
    #     randomIndex = random.randint(0, 8)
    
    # newGrid = copy.deepcopy(grid)
    # newGrid[randomIndex//3][randomIndex%3] = random.randint(1, 9)

    # return newGrid

# def countZeros(grid):
#     count = 0
#     for l in grid:
#         for c in l:
#             if(c==0):
#                 count+=1
#     return count


# def hillClimb(node):
#     currentNode = node.copy()
#     i=0

#     while(countZeros(currentNode["grid"])!=0):
#         newGrid = getNeighbor(node["grid"])
#         newNode = createNode(newGrid, evaluate(newGrid))

#         if(newNode["conflicts"]==0):
#             currentNode = newNode

#     return currentNode

def fillInitialGrid(grd):
    grid = copy.deepcopy(grd)
    for i in range(9):
        row = grid[i]
        rowSet = set(row)
        for j in range(9):
            c=0
            if(not j in rowSet):
                while(grid[i][c]!=0):
                    c+=1
                grid[i][c]=j
    
    return grid



grid = loadGrid("input/input1.txt")
node = createNode(grid, 0)
result = hillClimb(node)

print(result)