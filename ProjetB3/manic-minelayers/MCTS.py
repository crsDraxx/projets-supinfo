import math
import random
import time

from Sommet import Sommet
from MinMax import MinMax


class MCTS:
    def __init__(self, game, player, temperature=math.sqrt(2), maxIterations=1000, maxTime=None):
        self.__game = game
        self.__player = player
        self.__temperature = temperature
        self.__maxIterations = maxIterations
        self.__maxTime = maxTime
        self.__placer = MinMax(game, player, 1,1)


    def choosePlacement(self):
        return self.__placer.choosePlacement()
    

    def chooseMove(self):
        moves = self.__game.getValidMoves(self.__player)

        if len(moves) == 0:
            return None
        if len(moves) == 1:
            return moves[0]

        root = Sommet(self.__game)
        startTime = time.time()
        iterations = 0

        while self.__mustContinue(startTime, iterations):
            selected = self.__selection(root)

            if selected.isTerminal():
                newNode = selected
            else:
                newNode = self.__expansion(selected)

            winner = self.__simulation(newNode)
            self.__backpropagation(newNode, winner)
            iterations += 1

        return self.__bestMove(root)
    

    def __mustContinue(self, startTime, iterations):
        if self.__maxIterations is not None and iterations >= self.__maxIterations:
            return False
        if self.__maxTime is not None and time.time() - startTime >= self.__maxTime:
            return False
        return True


    def __selection(self, root):
        current = root

        while not current.isTerminal():
            if not current.isFullyExpanded():
                return current
            current = current.bestChild(self.__temperature)

        return current

    def __expansion(self, node):
        move = random.choice(node.getUntriedMoves())
        return node.addChild(move)

    def __simulation(self, node):
        game = node.getGame()

        while game.getWinner() is None:
            current = game.getCurrentPlayer()
            move = random.choice(game.getValidMoves(current))
            game.movePlayer(current, move[0], move[1])

        return game.getWinner()

    def __backpropagation(self, node, winner):
        while node is not None:
            node.update(winner)
            node = node.getParent()

    def __bestMove(self, root):
        bestChild = None

        for child in root.getChildren():
            if bestChild is None or child.getVisits() > bestChild.getVisits():
                bestChild = child
        return bestChild.getMove()

