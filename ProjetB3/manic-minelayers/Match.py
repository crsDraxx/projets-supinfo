import random
from MinMax import MinMax
from StupidBot import StupidBot
from MCTS import MCTS
from Glouton import Glouton

class Match:

    def __init__(self, game, player1, player2):
        self.__game = game
        self.__players = {1: player1, 2: player2}
        self.__placed = 0

    def __choosePlacement(self, player):
        who = self.__players[player]

        if isinstance(who, MinMax):
            return who.choosePlacement()

        if isinstance(who, MCTS):
            return who.choosePlacement()

        if isinstance(who, StupidBot):
            return random.randint(0, self.__game.getRows() - 1)

        if isinstance(who, Glouton):
            return who.choosePlacement()

        return None

    
    def playTurn(self):
        if self.__game.getWinner() is not None:
            return False

        current = self.__game.getCurrentPlayer()

        if self.__placed < 2:
            row = self.__choosePlacement(current)
            if row is None:
                return False
            self.__game.placePlayer(current, row)
            self.__placed += 1
            return True

        move = self.__players[current].chooseMove()
        self.__game.movePlayer(current, move[0], move[1])
        return True
    

    def play(self):
        while self.playTurn():
            pass
        return self.__game.getWinner()