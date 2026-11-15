import random

class StupidBot:

    def __init__(self, game, player):
        self.__game = game
        self.__player = player

    def chooseMove(self):
        moves = self.__game.getValidMoves(self.__player)

        if len(moves) > 0:
            return random.choice(moves)
        return None