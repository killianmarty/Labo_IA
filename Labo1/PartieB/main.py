from functools import cmp_to_key

##CLASSES FOR DATA REPRESENTATION
class Task:
    def __init__(self, id, startDate, endDate) -> None:
        self.id = id
        self.startDate = startDate
        self.endDate = endDate

    def __str__(self) -> str:
        return "[" + str(self.id) + ", " + str(self.startDate) + ", " + str(self.endDate) + "]"

    def __repr__(self):
        return self.__str__()

class State:
    def __init__(self, executed, pending, currentDate) -> None:
        self.executed = executed
        self.pending = pending
        self.currentDate = currentDate

    def sort(self, heuristic):
        self.pending = sorted(self.pending, key=cmp_to_key(lambda item1, item2: heuristic(item1) - heuristic(item2)))

    def executeTask(self, task):
        self.currentDate = task.endDate
        self.executed.append(task)
        self.pending.remove(task)

    def __str__(self) -> str:
        return "(" + str(self.executed) + ", " + str(self.pending) + ", " + str(self.currentDate) + ")"


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

    return State([], pendingTasks, 0)

def explore(initalState, heuristic):
    state = initalState
    while(len(state.pending)!=0):
        state.sort(heuristic)
        state.executeTask(state.pending[0])

        print(state)

    return state


#HEURISTICS
def startDateHeuristic(task):
    return task.startDate

def endDateHeuristic(task):
    return task.endDate

def durationHeuristic(task):
    return task.endDate - task.startDate


#CALLS
inputState = loadData("input/Ex2-3.txt")
result = explore(inputState, endDateHeuristic)