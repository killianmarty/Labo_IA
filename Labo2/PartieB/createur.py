import random

class Createur:
    def __init__(self):
        self.combination = self.createCombination()
        self.nbFeedbacks = 0

    def createCombination(self):
        tmp = []
        for i in range(4):
            tmp.append(random.randint(0, 5))    #0 = rouge, 1 = vert, 2 = bleu, 3 = jaune, 4 = orange, 5 = marron

        return tmp

    def checkCombination(self, combination):
        colors = [0, 0, 0, 0, 0, 0]
        for i in range(4):
            colors[self.combination[i]] += 1

        correct = 0
        for i in range(4):
            if(colors[combination[i]]!=0):
                correct += 1
                colors[combination[i]] -= 1


        a = 0
        for i in range(4):
            if(self.combination[i] == combination[i]):
                a += 1

        b = correct - a

        self.nbFeedbacks += 1

        return (a, b)