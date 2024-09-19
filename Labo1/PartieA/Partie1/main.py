import time

#grid format : array with index = position, value = value

def loadGrid(file):
    f = open(file)
    res = []
    for line in f:
        row_values = [int(x) if x else 0 for x in line.split('\t')]
        res.extend(row_values)
    f.close()
    return res

def saveOutput(output, file):
    f = open(file, "w")
    for i in range(len(output["frontierLengths"])):
        frontierLength = output["frontierLengths"][i]
        f.write(str(i+1) + '\t' + str(frontierLength)+'\n')
    f.write(str(output["visitedStates"]) + '\n')
    f.write(str(output["executionTime"]) + "s\n")
    f.close()

    print("Output data saved to " + file)

def createNode(grid, parent, cost, action):
    return {
        "parent": parent,
        "cost": cost,
        "grid": grid,
        "action": action
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
        childs.append(createNode(tmp, node, node["cost"] + 1, "left"))
    
    # X = top
    if(zeroIndex > 2):
        tmp = grid.copy()
        tmp[zeroIndex] = tmp[zeroIndex-3]
        tmp[zeroIndex-3] = 0
        childs.append(createNode(tmp, node, node["cost"] + 1, "top"))

    # X = right
    if((zeroIndex+1) % 3 != 0):
        tmp = grid.copy()
        tmp[zeroIndex] = tmp[zeroIndex+1]
        tmp[zeroIndex+1] = 0
        childs.append(createNode(tmp, node, node["cost"] + 1, "right"))

    # X = bottom
    if(zeroIndex < 6):
        tmp = grid.copy()
        tmp[zeroIndex] = tmp[zeroIndex+3]
        tmp[zeroIndex+3] = 0
        childs.append(createNode(tmp, node, node["cost"] + 1, "bottom"))

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
    initialNode = createNode(grid, None, 0, None)
    finalNode = None
    target = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    frontier = [initialNode]
    visited = set()
    path = []
    done = False

    #start time measure
    startDate = time.time()

    #track the frontier length
    frontierLengthByIteration = []
    
    #iterate the algorithm
    while(len(frontier)!=0 and not done):
        currentNode = frontier.pop(0)
        currentGrid = currentNode["grid"]

        frontierLengthByIteration.append(len(frontier))

        if(currentGrid == target):
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
            if(tmp["action"]!=None):
                path.insert(0, tmp["action"])
            tmp = tmp["parent"]

    #end time measure
    executionTime = time.time() - startDate

    return {
        "solution": done,
        "executionTime": executionTime,
        "frontierLengths" : frontierLengthByIteration,
        "visitedStates": len(visited),
        "path": path
    }




### "Main" functions to test the 3 algorithms implementations

def runWidthExploration(input, output):
    print("Running Width exploration...")
    grid = loadGrid(input)
    result = explore(grid, frontierAddWidth)
    print(result["path"])
    saveOutput(result, output)

def runDepthExploration(input, output):
    print("Running Depth exploration...")
    grid = loadGrid(input)
    result = explore(grid, frontierAddDepth)
    print(result["path"])
    saveOutput(result, output)

def runAStarExploration(input, output):
    print("Running A* exploration...")
    grid = loadGrid(input)
    result = explore(grid, frontierAddAStar)
    print(result["path"])
    saveOutput(result, output)



### CALLS
filename = "input/Ex1-1.txt"
runWidthExploration(filename, "output/width.txt")
runDepthExploration(filename, "output/depth.txt")
runAStarExploration(filename, "output/astar.txt")