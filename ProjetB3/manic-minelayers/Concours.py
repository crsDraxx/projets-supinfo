from ManicMinelayers import ManicMinelayers
from StupidBot import StupidBot
from MinMax import MinMax
from MCTS import MCTS
from Match import Match
from Glouton import Glouton

def makeStupidBot(game, player):
    return StupidBot(game, player)
def makeMinMax1(game, player):
    return MinMax(game, player, 4, 1)
def makeMinMax2(game, player):
    return MinMax(game, player, 4, 2)
def makeMCTS(game, player):
    return MCTS(game, player, maxIterations=100)
def makeGlouton(game, player):
    return Glouton(game, player)


class Concours:

    def __init__(self, games=100):
        self.__games = games
        self.__players = [
            ["StupidBot", makeStupidBot],
            ["MinMax H1", makeMinMax1],
            ["MinMax H2", makeMinMax2],
            ["MCTS", makeMCTS],
            ["Glouton", makeGlouton]
        ]


    def __playSeries(self, builderFirst , builderSecond):
        winsFirst = 0
        winsSecond = 0
        draws = 0

        for i in range(self.__games):
            game = ManicMinelayers()
            player1 = builderFirst(game, 1)
            player2 = builderSecond(game, 2)
            match = Match(game, player1, player2)
            winner = match.play()

            if winner == 1:
                winsFirst += 1
            elif winner == 2:
                winsSecond += 1
            elif winner == "draw":
                draws += 1

        return [winsFirst, winsSecond, draws]

    def __runPair(self, name1, builder1, name2, builder2):
        print(name1 + " vs " + name2 + " (" + str(self.__games) + " parties par ordre)")
        result = self.__playSeries(builder1, builder2)
        print(name1 + " commence : " + name1 + " " + str(result[0]) + ", " + name2 + " " + str(result[1]) + ", nuls " + str(result[2]))
        total1 = result[0]
        total2 = result[1]
        totalDraws = result[2]

        result = self.__playSeries(builder2, builder1)
        print(name2 + " commence : " + name2 + " " + str(result[0]) + ", " + name1 + " " + str(result[1]) + ", nuls " + str(result[2]))
        total1 += result[1]
        total2 += result[0]
        totalDraws += result[2]

        print("Total : " + name1 + " " + str(total1) + ", " + name2 + " " + str(total2) + ", nuls " + str(totalDraws))


    def run(self):
        for i in range(len(self.__players)):
            for j in range(i + 1,len(self.__players)):
                self.__runPair(self.__players[i][0], self.__players[i][1], self.__players[j][0], self.__players[j][1])
                print() 