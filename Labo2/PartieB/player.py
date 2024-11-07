class Player: 
    def __init__(self, createur):
        self.lastFeedback = []
        self.possibilities = self.createAllCombinations()
        self.createur = createur
        self.verbose = True

    def createAllCombinations(self):
        tmp = []
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    for l in range(6):
                        tmp.append([i, j, k, l])
        return tmp

    def filterKnowledgeBase(self):
        for i in reversed(range(len(self.possibilities))):
            if(not self.couldMatch(self.lastFeedback, self.possibilities[i])):
                self.possibilities.pop(i)

    def couldMatch(self, sentence, guess):

        knowledgeCombination = sentence[0]
        knowledgeFeedback = sentence[1]


        colors = [0, 0, 0, 0, 0, 0]
        for i in range(4):
            colors[knowledgeCombination[i]] += 1

        correct = 0
        for i in range(4):
            if(colors[guess[i]]!=0):
                correct += 1
                colors[guess[i]] -= 1


        a = 0
        for i in range(4):
            if(correct != 0 and knowledgeCombination[i] == guess[i]):
                a += 1

        b = correct - a            

        return (a == knowledgeFeedback[0] and b == knowledgeFeedback[1])

    def play(self):

        comb = None
        i=1

        while(len(self.possibilities) > 0):

            comb = self.possibilities.pop()
            result = self.createur.checkCombination(comb)

            self.lastFeedback = [comb, result]
            self.filterKnowledgeBase()

            if(self.verbose):
                print("Tour de jeu", str(i), "il reste", str(len(self.possibilities) + 1), "possibilités.")
            i+=1

        return comb