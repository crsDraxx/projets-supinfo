from copy import deepcopy
from ManicMinelayers import ManicMinelayers

WIN = 1000000
INFINITY = 10000000

class MinMax:
    def __init__(self, game, player, depth=4, heuristic=1):
        self.__game = game
        self.__player = player
        if player == 1:
            self.__opponent = 2
        else:
            self.__opponent = 1
        self.__depth = depth
        self.__heuristic = heuristic


    def choosePlacement(self):
        grid = self.__game.getGrid()
        rows = self.__game.getRows()
        cols = self.__game.getCols()

        if self.__player == 1:
            col= 0
        else:
            col = cols -1
        bestRow = None
        bestCount = -1

        for row in range(rows):
            if grid[row][col] != 0:
                continue

            count = 0
            for move in ManicMinelayers.MOVES:
                newRow = row + move[0]
                newCol = col + move[1]
                if self.__game.isInside(newRow, newCol):
                    if grid[newRow][newCol] == 0:
                        count += 1

            if count > bestCount:
                bestCount = count
                bestRow = row

        return bestRow
    

    def __heuristic_1(self,game):
        myMoves = game.getValidMoves(self.__player)
        opponentMoves = game.getValidMoves(self.__opponent)
        return len(myMoves) - len(opponentMoves)


    def __heuristic_2(self,grid , player):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == player:
                    return(row, col)
        return None


    def __distances(self, game, grid, start):
        rows = len(grid)
        cols= len(grid[0])
        distance = [[-1 for _ in range(cols)] for _ in range(rows)]
        distance[start[0]][start[1]] = 0
        queue = [start]
        index = 0
        while index < len(queue):
            current = queue[index]
            index += 1
            row = current[0]
            col = current[1]

            for move in ManicMinelayers.MOVES:
                newRow = row + move[0]
                newCol = col + move[1]
                if game.isInside(newRow, newCol):
                    if grid[newRow][newCol] == 0 and distance[newRow][newCol] == -1:
                        distance[newRow][newCol] = distance[row][col] + 1
                        queue.append((newRow, newCol))
        return distance


    def __territory(self, game):
        grid = game.getGrid()
        myStart = self.__heuristic_2(grid, self.__player)
        opponentStart = self.__heuristic_2(grid, self.__opponent)
        myDistance = self.__distances(game, grid, myStart)
        opponentDistance = self.__distances(game, grid, opponentStart)

        score = 0
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                d1 = myDistance[row][col]
                d2 = opponentDistance[row][col]
                if d1 > 0 and (d2 == -1 or d1 < d2):
                    score += 1
                elif d2 > 0 and (d1 == -1 or d2 < d1):
                    score -= 1
        return score


    def __evaluate(self, game):
        if self.__heuristic == 1:
            return self.__heuristic_1(game)
        return self.__territory(game)


    def __minmax(self, game, depth , alpha, beta):
        winner = game.getWinner()
        if winner == "draw":
            return 0
        if winner == self.__player:
            return WIN + depth
        if winner ==  self.__opponent:
            return -(WIN + depth)
        if depth == 0:
            return self.__evaluate(game)

        current = game.getCurrentPlayer()
        moves = game.getValidMoves(current)

        if current == self.__player:
            best = -INFINITY
            for move in moves:
                child = deepcopy(game)
                child.movePlayer(current, move[0], move[1])
                score = self.__minmax(child, depth - 1, alpha, beta)
                if score > best:
                    best = score
                if best > alpha:
                    alpha = best
                if alpha >= beta:
                    break
            return best

        best = INFINITY
        for move in moves:
            child = deepcopy(game)
            child.movePlayer(current, move[0], move[1])
            score = self.__minmax(child, depth - 1, alpha, beta)
            if score < best:
                best = score
            if best < beta:
                beta = best
            if alpha >= beta:
                break
        return best


    def chooseMove(self):
        moves = self.__game.getValidMoves(self.__player)

        if len(moves) == 0:
            return None

        bestMove = None
        bestScore = -INFINITY
        alpha = -INFINITY

        for move in moves:
            child = deepcopy(self.__game)
            child.movePlayer(self.__player, move[0], move[1])
            score = self.__minmax(child, self.__depth - 1, alpha, INFINITY)
            if score > bestScore:
                bestScore = score
                bestMove = move
            if bestScore > alpha:
                alpha = bestScore
        return bestMove
