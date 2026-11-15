from copy import deepcopy
import math

class Sommet: 
    def __init__(self, game, parent=None, move=None):
        self.__game = deepcopy(game)
        self.__parent = parent 
        self.__move = move

        self.__children = []
        self.__visits = 0
        self.__wins = 0

        player = self.__game.getCurrentPlayer()
        self.__untriedMoves = self.__game.getValidMoves(player)

        if move is None:
            self.__playerJustMoved = None
        else:
            self.__playerJustMoved = 3 - player

    def addChild(self, move):
        if move not in self.__untriedMoves:
            return None
        
        newGame = deepcopy(self.__game)
        player = newGame.getCurrentPlayer()

        if not newGame.movePlayer(player, move[0], move[1]):
            return None

        child = Sommet(newGame, self, move)
        self.__children.append(child)
        self.__untriedMoves.remove(move)

        return child

    def isFullyExpanded(self):
        return len(self.__untriedMoves) == 0

    def getGame(self):
        return deepcopy(self.__game)

    def getParent(self):
        return self.__parent

    def getChildren(self):
        return self.__children

    def getMove(self):
        return self.__move

    def getVisits(self):
        return self.__visits

    def getWins(self): 
        return self.__wins

    def getUntriedMoves(self):
        return self.__untriedMoves.copy()

    def getPlayerJustMoved(self):
        return self.__playerJustMoved

    def update(self, winner):
        self.__visits += 1

        if winner == "draw":
            self.__wins += 0.5
        elif winner == self.__playerJustMoved:
            self.__wins += 1 

    def isTerminal(self):
        return self.__game.getWinner() is not None

    def bestChild(self, c=1.414):
        if len(self.__children) == 0:
            return None

        best = None
        bestScore = float("-inf")

        for child in self.__children:
            if child.getVisits() == 0:
                score = float("inf")
            else:
                exploitation = child.getWins() / child.getVisits()
                exploration = c * math.sqrt(

                    math.log(max(1, self.__visits)) / child.getVisits()
                )

                score = exploitation + exploration

            if score > bestScore : 
                bestScore = score
                best = child

        return best