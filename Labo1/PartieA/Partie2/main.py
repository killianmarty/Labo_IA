from functools import cmp_to_key
import copy

#State (also Node here) structure : State(executed, pending, currentTime) with executed, pending = arrays of "Task"

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

class State:
    def __init__(self, executed, pending, currentTime) -> None:
        self.executed = executed
        self.pending = pending
        self.currentTime = currentTime

    def __str__(self) -> str:
        return "{executed: " + str(self.executed) + ", pending: " + str(self.pending) + ", currentTime: " + str(self.currentTime) + "}"

    def __repr__(self):
        return self.__str__()

#Loading function
def loadData(inputFile):
    f = open(inputFile, 'r')
    lines = f.readlines()
    f.close()

    pendingTasks = []

    for line in lines[1:]:
        split = line.split('\t')
        newTask = Task(int(split[0]), int(split[1]), int(split[2]))
        pendingTasks.append(newTask)

    return State([], pendingTasks, 0)



##############################
## GREEDY ALGORITHM SECTION ##
##############################


#Greedy heuristics
def startDateHeuristic(task):
    return task.startDate

def endDateHeuristic(task):
    return task.endDate

def durationHeuristic(task):
    return task.endDate - task.startDate



def greedy(initalState, heuristic):
    state = copy.deepcopy(initalState)

    #Sort with heuristic
    state.pending.sort(key=cmp_to_key(lambda item1, item2: heuristic(item1) - heuristic(item2)))
    
    #Execute the tasks if possible
    for task in state.pending:
        if(task.startDate >= state.currentTime):
            state.executed.append(task)
            state.pending.remove(task)
            state.currentTime = task.endDate

    return state



####################
## A STAR SECTION ##
####################

#Function to calculate cost + heuristic for A*
def AStarHeuristic(currentState):
    return currentState.currentTime + len(currentState.pending)

#Function to get childs of a node in the tree
def getChilds(currentState):
    childs = []

    for i in range(len(currentState.pending)):
        task = currentState.pending[i]
        if(currentState.currentTime <= task.startDate):

            #Create a child
            stateCopy = copy.deepcopy(currentState)
            stateCopy.executed.append(task)
            stateCopy.pending.pop(i)
            stateCopy.currentTime = task.endDate

            childs.append(stateCopy)

    return childs



def AStar(inputState):
    currentState = copy.deepcopy(inputState)

    frontier = [currentState]
    visited = []

    while(len(currentState.pending) != 0 and len(frontier) != 0):
        currentState = frontier.pop(0)
        visited.append(currentState)
        
        childs = getChilds(currentState)
        for child in childs:
            if(not child in visited):
                frontier.append(child)

        frontier.sort(key=cmp_to_key(lambda item1, item2: AStarHeuristic(item1) - AStarHeuristic(item2)))



    solved = (len(currentState.pending) == 0)

    return {
        "finalNode": currentState,
        "solved": solved
    }



###########
## CALLS ##
###########

src = "input/Ex2-1.txt"

print("Loading data from " + src)
inputState = loadData("input/Ex2-1.txt")

#Greedy algorithm calls
print("\nResolut of greedy algoritm with start date heuristic :")
resultStartDate = greedy(inputState, startDateHeuristic)
print(resultStartDate)

print("\nResolut of greedy algoritm with end date heuristic :")
resultEndDate = greedy(inputState, endDateHeuristic)
print(resultEndDate)

print("\nResolut of greedy algoritm with duration heuristic :")
resultDuration = greedy(inputState, durationHeuristic)
print(resultDuration)

#A* call
print("\nResolut of A* algorithm :")
print(AStar(inputState))