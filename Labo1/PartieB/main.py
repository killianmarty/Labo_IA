from functools import cmp_to_key
import copy

##CLASSES FOR DATA REPRESENTATION
class Task:
    def __init__(self, id, startDate, endDate) -> None:
        self.id = id
        self.startDate = startDate
        self.endDate = endDate

    def __str__(self) -> str:
        return "(" + str(self.id) + ", " + str(self.startDate) + ", " + str(self.endDate) + ")"

    def __repr__(self):
        return self.__str__()

#MAIN FUNCTIONS
def loadData(inputFile):
    f = open(inputFile, 'r')
    lines = f.readlines()
    f.close()

    pendingTasks = []

    for line in lines[1:]:
        split = line.split('\t')
        newTask = Task(int(split[0]), int(split[1]), int(split[2]))
        pendingTasks.append(newTask)

    return pendingTasks

def explore(initalState, heuristic):
    executedTasks = []
    pendingTasks = initalState.copy()
    currentTime = 0

    #Sort with heuristic
    pendingTasks.sort(key=cmp_to_key(lambda item1, item2: heuristic(item1) - heuristic(item2)))
    
    #Execute the tasks if possible
    for task in pendingTasks:
        if(task.startDate >= currentTime):
            executedTasks.append(task)
            pendingTasks.remove(task)
            currentTime += task.endDate - task.startDate

    return (executedTasks, pendingTasks, currentTime)

#HEURISTICS
def startDateHeuristic(task):
    return task.startDate

def endDateHeuristic(task):
    return task.endDate

def durationHeuristic(task):
    return task.endDate - task.startDate

def maxHeuristic(task):
    return max(startDateHeuristic(task), endDateHeuristic(task), durationHeuristic(task))


#CALLS
inputState = loadData("input/Ex2-1.txt")

resultStartDate = explore(inputState, startDateHeuristic)
resultEndDate = explore(inputState, endDateHeuristic)
resultDuration = explore(inputState, durationHeuristic)
resultMax = explore(inputState, maxHeuristic)

print(resultStartDate)
print(resultEndDate)
print(resultDuration)
print(resultMax)

print("----------")

### A STAR IMPLEMENTATION

#Node structure : [executed, pending, currentTime] with executed, pending = arrays of "Task"

#function to calculate cost + heuristic for A*
def AStarHeuristic(currentNode):
    return currentNode[2] + len(currentNode[1])

def AStar(inputState):
    currentNode = [[], inputState, 0]
    taskNumber = len(inputState)

    frontier = [currentNode]
    visited = []

    while(len(currentNode[1]) != 0 and len(frontier) != 0):
        currentNode = frontier.pop(0)
        visited.append(currentNode)
        
        childs = getChilds(currentNode)
        for child in childs:
            if(not child in visited):
                frontier.append(child)

        frontier.sort(key=cmp_to_key(lambda item1, item2: AStarHeuristic(item1) - AStarHeuristic(item2)))

    solved = (len(currentNode[1]) == 0)
    return {"finalNode" :currentNode, "solved" : solved}


def getChilds(currentNode):
    
    childs = []

    for i in range(len(currentNode[1])):
        task = currentNode[1][i]
        if(currentNode[2] <= task.startDate):

            #we create a child
            nodeCopy = copy.deepcopy(currentNode)
            nodeCopy[0].append(task)
            nodeCopy[1].pop(i)
            nodeCopy[2] += (task.endDate - task.startDate)

            childs.append(nodeCopy)

    return childs


print(AStar(inputState))