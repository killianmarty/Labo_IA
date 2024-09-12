#format index = position, value = value

def loadGrid(file):
    f = open(file)
    res = []
    for line in f:
        l = line.replace(" ", "0")
        row_values = l.strip().split()
        for i in range(len(row_values)):
            row_values[i] =  int(row_values[i])
        res.extend(row_values)
    return res

def getChilds(node):
    childs = []
    zeroIndex = node.index(0)

    #if we can move the void square to the X, we add the new grid to childs list
    
    # X = left
    if(zeroIndex % 3 != 0):
        tmp = node.copy()
        tmp[zeroIndex] = tmp[zeroIndex-1]
        tmp[zeroIndex-1] = 0
        childs.append(tmp)
    
    # X = top
    if(zeroIndex > 2):
        tmp = node.copy()
        tmp[zeroIndex] = tmp[zeroIndex-3]
        tmp[zeroIndex-3] = 0
        childs.append(tmp)

    # X = right
    if((zeroIndex+1) % 3 != 0):
        tmp = node.copy()
        tmp[zeroIndex] = tmp[zeroIndex+1]
        tmp[zeroIndex+1] = 0
        childs.append(tmp)

    # X = bottom
    if(zeroIndex < 5):
        tmp = node.copy()
        tmp[zeroIndex] = tmp[zeroIndex+3]
        tmp[zeroIndex+3] = 0
        childs.append(tmp)

    return childs

def frontierSortWidth(frontier, news):
    new = frontier.copy()
    new.extend(news)
    return new

def parcours(grid, frontierSortMethod):
    objective = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    frontier = [grid]
    path = []
    done = False
    
    while(len(frontier)!=0 and not done):
        currentNode = frontier.pop(0)
        path.append(currentNode)
        #print(f'{currentNode}, {objective}')
        if(currentNode == objective):
            done = True
        else:
            frontier = frontierSortMethod(frontier, getChilds(currentNode))

    return {
        "done": True,
        "path": path
    }

grid = loadGrid("input/Ex1-1.txt")

#print(getChilds(grid))


print(parcours(grid, frontierSortWidth))
