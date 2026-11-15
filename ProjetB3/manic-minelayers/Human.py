class Human:

    def __init__(self, game, player):
        self.__game = game
        self.__player = player

    def chooseMove(self):
        moves = self.__game.getValidMoves(self.__player)

        if len(moves) == 0:
            return None

        print("Déplacements possibles:")
        moveNb = 0
        for move in moves:
            moveNb += 1
            row = move[0]
            col = move[1]
            letter = chr(65 + col)

            print(f"{moveNb}. {letter}{row} -> coordonnées {move}")
            #print (moveNb ,move)

        while True:
            try:
                choice = int(input("Choisissez parmis cette liste: "))

                if 1 <= choice <= len(moves):
                    return moves[choice - 1]
                else:
                    print("Choix invalide, veuillez saisir un autre deplacement")

            except ValueError:
                print("Veuillez saisir un nombre entier")
