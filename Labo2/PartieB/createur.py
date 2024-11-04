import random


class Createur:
    def __init__(self):
        self.combinaison = self.createCombinaison()

    def createCombinaison(self):
        tmp = []
        for i in range(4):
            tmp.append(random.randint(0, 5))
            #0 = rouge, 1 = vert, 2 = bleu, 3 = jaune, 4 = orange, 5 = marron

        return tmp

    def checkCombinaison(self, combinaison):
        #count colors existing but in the wrong place
        colors = [0, 0, 0, 0, 0, 0]
        for i in range(4):
            colors[self.combinaison[i]] += 1

        correct = 0
        for i in range(4):
            if(colors[combinaison[i]]!=0):
                correct += 1
                colors[combinaison[i]] -= 1


        a = 0
        for i in range(4):
            if(correct != 0 and self.combinaison[i] == combinaison[i]):
                a += 1
                correct -= 1

        b = correct

        return (a, b)

    

class Player: 
    def __init__(self, createur):
        self.kb = []
        self.possibilities = self.createAllCombinaisons()
        self.createur = createur

    def createAllCombinaisons(self):
        tmp = []
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    for l in range(6):
                        tmp.append([i, j, k, l])
        return tmp

    def filterKnowledgeBase(self):
        for i in reversed(range(len(self.possibilities))):
            for sentence in self.kb:
                if(not self.couldMatch(sentence, self.possibilities[i])):
                    self.possibilities.pop(i)
                    break

    def couldMatch(self, sentence, guess):

        colors = [0, 0, 0, 0, 0, 0]
        for i in range(4):
            colors[sentence[0][i]] += 1

        correct = 0
        for i in range(4):
            if(colors[guess[i]]!=0):
                correct += 1
                colors[guess[i]] -= 1


        a = 0
        for i in range(4):
            if(correct != 0 and sentence[0][i] == guess[i]):
                a += 1
                correct -= 1

        b = correct
                    

        return (a == sentence[1][0] and b >= sentence[1][1])

    def play(self):
        comb = None
        while(len(self.possibilities) > 1):
            comb = self.possibilities[0]
            result = self.createur.checkCombinaison(comb)

            if(result == (4, 0)):
                return comb 

            #add to kb
            self.kb.append([comb, result])
            

            self.filterKnowledgeBase()
            self.possibilities.pop(0)
            print("un tour de jeu " + str(len(self.kb)))
            print(len(self.possibilities))
        return comb


if __name__ == "__main__":
    creator = Createur()

    # a = creator.createCombinaison()
    # print(creator.combinaison)
    # print(a)
    # print(creator.checkCombinaison(a))

    player = Player(creator)
    print(player.play())

    print(creator.combinaison)