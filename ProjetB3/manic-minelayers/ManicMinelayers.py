class ManicMinelayers:
    MOVES = [
        (1, 2), (1, -2),
        (-1, 2), (-1, -2),
        (2, 1), (2, -1),
        (-2, 1), (-2, -1)
    ]
    def __init__(self, m=5, n=10):
        if not ((m >= 2 and n>= 3) or (m >= 3 and n>= 2)):
            raise ValueError("Dimensions trop petite pour permettre un déplacment en L")
        
        self.__row = m
        self.__col = n
        self.resetGame()
        

    def getGrid(self):
        return [row.copy() for row in self.__grid]

    def getRows(self):
        return self.__row

    def getCols(self):
        return self.__col

    def getPosition(self, player):
        self.__checkPlayer(player)
        return self.__positions[player]

    def getCurrentPlayer(self):
        return self.__currentPlayer

    def __checkPlayer(self, player):
        if player not in (1,2):
            raise ValueError("Le numero du joueur n'est pas valide!")

    def resetGame(self):
        self.__grid = [[0 for _ in range(self.__col)] for _ in range(self.__row)]

        self.__positions = {1: None, 2: None}
        self.__currentPlayer = 1

    def isInside(self, row, col):
        return( 0 <= row < self.__row and 0 <= col < self.__col)

    def placePlayer(self, player, row):
        self.__checkPlayer(player)

        if player != self.__currentPlayer:
            return False

        if self.__positions[player] is not None:
            return False

        if not self.isInside(row, 0):
            return False

        if player == 1:
            col = 0
        else :
            col = self.__col -1

        self.__grid[row][col] = player
        self.__positions[player] = (row, col)

        if player == 1:
            self.__currentPlayer = 2
        else:
            self.__currentPlayer = 1

        return True

    def getValidMoves(self, player):
        self.__checkPlayer(player)

        position = self.__positions[player]

        if position is None:
            return []

        row, col = position
        validMoves = []

        for move in self.MOVES:
            deltaRow = move[0]
            deltaCol = move[1]

            newRow = row + deltaRow
            newCol = col + deltaCol

            if self.isInside(newRow, newCol):
                if self.__grid[newRow][newCol] == 0:
                    validMoves.append((newRow, newCol))

        return validMoves

    def canMove(self, player, row, col):
        return (row, col) in self.getValidMoves(player)

    def movePlayer(self, player, row, col):
        self.__checkPlayer(player)

        if None in self.__positions.values():
            return False

        if self.getWinner() is not None:
            return False

        if player != self.__currentPlayer:
            return False

        if not self.canMove(player, row, col):
            return False

        oldPosition = self.__positions[player]

        oldRow = oldPosition[0]
        oldCol = oldPosition[1]

        self.__grid[oldRow][oldCol] = 3

        self.__grid[row][col] = player
        self.__positions[player] = (row, col)

        if player == 1:
            self.__currentPlayer = 2
        else:
            self.__currentPlayer = 1 
       
        return True

    def getWinner(self):
        if None in self.__positions.values():
            return None

        moves1 = self.getValidMoves(1)
        moves2= self.getValidMoves(2)

        if len(moves1) == 0 and len(moves2) == 0:
            return "draw"
        elif len(moves2) == 0:
            return 1
        elif len(moves1) == 0:
            return 2
        
        return None

    def displayBoard(self):
        symbols = {
            0: ".",
            1: "A",
            2: "B",
            3: "#"
        }

        letters = [chr(65 + col) for col in range(self.__col)]

        print("  " + " ".join(letters))

        for row, line in enumerate(self.__grid):
            print(row, " ".join(symbols[case] for case in line))