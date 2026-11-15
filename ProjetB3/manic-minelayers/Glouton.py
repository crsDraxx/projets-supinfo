from copy import deepcopy

class Glouton:
    def __init__(self, game, player):
        self.__game = game
        self.__player = player

    def choosePlacement(self):
        bestRow = None
        bestScore = -1

        for row in range(self.__game.getRows()):
            testGame = deepcopy(self.__game)

            if testGame.placePlayer(self.__player, row):
                score = len(testGame.getValidMoves(self.__player))

                if score > bestScore:
                    bestScore = score
                    bestRow = row

        return bestRow

    def chooseMove(self):
        moves = self.__game.getValidMoves(self.__player)

        if len(moves) == 0:
            return None

        bestMove = None
        bestScore = -1

        for move in moves:
            testGame =deepcopy(self.__game)

            if testGame.movePlayer(self.__player, move[0], move[1]):
                score = len(testGame.getValidMoves(self.__player))

                if score > bestScore:
                    bestScore = score
                    bestMove = move

        return bestMove
    