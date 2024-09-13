#grid format : array with index = position, value = value

def loadGrid(file):
    f = open(file)
    res = []
    for line in f:
        row_values = [int(x) if x else 0 for x in line.split('\t')]
        res.extend(row_values)
    return res

def createNode(grid, parent, cost):
    return {
        "parent": parent,
        "cost": cost,
        "grid": grid
    }

def getChilds(node):
    grid = node["grid"]
    childs = []
    zeroIndex = grid.index(0)

    #if we can move the void square to the X, we add the new grid to childs list
    
    # X = left
    if(zeroIndex % 3 != 0):
        tmp = grid.copy()
        tmp[zeroIndex] = tmp[zeroIndex-1]
        tmp[zeroIndex-1] = 0
        childs.append(createNode(tmp, node, node["cost"] + 1))
    
    # X = top
    if(zeroIndex > 2):
        tmp = grid.copy()
        tmp[zeroIndex] = tmp[zeroIndex-3]
        tmp[zeroIndex-3] = 0
        childs.append(createNode(tmp, node, node["cost"] + 1))

    # X = right
    if((zeroIndex+1) % 3 != 0):
        tmp = grid.copy()
        tmp[zeroIndex] = tmp[zeroIndex+1]
        tmp[zeroIndex+1] = 0
        childs.append(createNode(tmp, node, node["cost"] + 1))

    # X = bottom
    if(zeroIndex < 6):
        tmp = grid.copy()
        tmp[zeroIndex] = tmp[zeroIndex+3]
        tmp[zeroIndex+3] = 0
        childs.append(createNode(tmp, node, node["cost"] + 1))

    return childs


def calculateManhattan(grid):
    return sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3) for i, val in enumerate(grid) if val)

def calculateAStarDistance(node):
    return node["cost"] + calculateManhattan(node["grid"])



def frontierAddWidth(frontier, news):
    frontier.extend(news)

def frontierAddDepth(frontier, news):
    frontier[:0] = news

def frontierAddAStar(frontier, news):
    frontier.extend(news)
    frontier.sort(key=calculateAStarDistance)



def explore(grid, frontierAddMethod):
    initialNode = createNode(grid, None, 0)
    finalNode = None
    objective = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    frontier = [initialNode]
    visited = set()
    path = []
    done = False
    
    #iterate the algorithm
    while(len(frontier)!=0 and not done):
        currentNode = frontier.pop(0)
        currentGrid = currentNode["grid"]

        if(currentGrid == objective):
            done = True
            finalNode = currentNode
        else:
            visited.add(tuple(currentGrid)) #add the grid to the visited grids list

            childs = getChilds(currentNode)
            filteredChilds = [child for child in childs if tuple(child["grid"]) not in visited] #filter the childs to only keep unvisited nodes
            
            frontierAddMethod(frontier, filteredChilds)


    #rebuild the path
    if(done):
        tmp = finalNode
        while(tmp != None):
            path.insert(0, tmp["grid"])
            tmp = tmp["parent"]

    return {
        "solution": done,
        "path": path
    }


grid = loadGrid("input/Ex1-1.txt")

widthResult = explore(grid, frontierAddWidth)
depthResult = explore(grid, frontierAddDepth)
aStarResult = explore(grid, frontierAddAStar)

print(widthResult)
print(depthResult)
print(aStarResult)