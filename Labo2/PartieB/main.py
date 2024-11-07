from createur import Createur
from player import Player


def testAlgorithm(nbIter):
    #this function returns True if the solution is always good
    c = 0
    for i in range(nbIter):
        creator = Createur()
        player = Player(creator)
        player.verbose = False
        if(player.play() == creator.combination):
            c+=1

    return c == nbIter



if __name__ == "__main__":
    
    creator = Createur()
    player = Player(creator)

    print("Combinaison secrète :", creator.combination)
    print("Combinaison trouvée par l'algorithme :", player.play())