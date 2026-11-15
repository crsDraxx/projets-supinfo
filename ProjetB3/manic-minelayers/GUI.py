import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ManicMinelayers import ManicMinelayers
import random
from StupidBot import StupidBot
from MinMax import MinMax
from MCTS import MCTS
from Glouton import Glouton
from Concours import Concours
import threading
import traceback

class GUI:
    BG = "#0B0D14"
    PANEL = "#171B27"
    CELL = "#252B3A"
    LILAC = "#B7A2DF"
    LILAC_START = "#61437B"
    TURQUOISE = "#67C9CC"
    TEXT = "#F2F2F7"
    MUTED = "#9DA5B8"
    RED = "#E25563"

    def __init__(self, game):
        self.__game = game

        self.__window = tk.Tk()
        self.__window.title("Manic Minelayers")
        self.__window.geometry("1100x700")
        self.__window.minsize(900, 600)
        self.__window.configure(bg = self.BG)
        self.__rows = tk.StringVar(value="5")
        self.__cols = tk.StringVar(value="10")
        self.showHome()

    def showHome(self):
        self.__homeFrame = tk.LabelFrame(self.__window, bg= self.BG)
        self.__homeFrame.pack(fill="both", expand= True)

        title =tk.Label(
            self.__homeFrame,
            text = "Manic Minelayers",
            font = ("Segoe UI", 32, "bold"),
            fg = self.TEXT,
            bg = self.BG
        )
        title.pack(pady=(110, 10))

        subtitle = tk.Label(
            self.__homeFrame,
            text = "CHOISIR UN PLATEAU",
            font = ("Segoe UI", 16),
            fg = self.MUTED,
            bg = self.BG
        )
        subtitle.pack(pady=(0, 45))

        self.__buttonsFrame = tk.Frame(
            self.__homeFrame,
            bg = self.BG
        )
        self.__buttonsFrame.pack()

        self.__classicButton = tk.Canvas(
            self.__buttonsFrame,
            width=320,
            height=56,
            bg=self.BG,
            highlightthickness=0,
            cursor="hand2"
        )
        self.__classicButton.pack(pady=10)

        self.__classicButton.create_oval(
            2, 2, 58, 54,
            fill=self.LILAC,
            outline=self.LILAC
        )
        self.__classicButton.create_oval(
            262, 2, 318, 54,
            fill=self.LILAC,
            outline=self.LILAC
        )
        self.__classicButton.create_rectangle(
            30, 2, 290, 54,
            fill=self.LILAC,
            outline=self.LILAC
        )

        self.__classicButton.create_text(
            160, 28,
            text="Classique 5 x 10",
            font=("Segoe UI", 13, "bold"),
            fill=self.BG
        )

        self.__customButton = tk.Canvas(
            self.__buttonsFrame,
            width=320,
            height=56,
            bg=self.BG,
            highlightthickness=0,
            cursor="hand2"
        )
        self.__customButton.pack(pady=10)

        self.__customButton.create_oval(
            2, 2, 58, 54,
            fill=self.CELL,
            outline=self.CELL
        )
        self.__customButton.create_oval(
            262, 2, 318, 54,
            fill=self.CELL,
            outline=self.CELL
        )
        self.__customButton.create_rectangle(
            30, 2, 290, 54,
            fill=self.CELL,
            outline=self.CELL
        )

        self.__customButton.create_text(
            160, 28,
            text="Personnalisé",
            font=("Segoe UI", 13, "bold"),
            fill=self.TEXT
        )

        self.__classicButton.bind(
            "<Button-1>",
            lambda event: self.selectBoardMode("default")
        )

        self.__customButton.bind(
            "<Button-1>",
            lambda event: self.selectBoardMode("custom")
        )

        self.__customFrame = tk.Frame(self.__homeFrame, bg=self.BG)

        tk.Label(
            self.__customFrame, text="Lignes :", bg=self.BG, fg=self.TEXT
        ).pack(side="left", padx=5)

        self.__rowsEntry = tk.Entry(self.__customFrame, width=5)
        self.__rowsEntry.pack(side="left", padx=5)
        self.__rowsEntry.insert(0, "5")

        tk.Label(
            self.__customFrame, text="Colonnes :", bg=self.BG, fg=self.TEXT
        ).pack(side="left", padx=5)

        self.__colsEntry = tk.Entry(self.__customFrame, width=5)
        self.__colsEntry.pack(side="left", padx=5)
        self.__colsEntry.insert(0, "10")

        self.selectBoardMode("default")

        tk.Label(
            self.__homeFrame,
            text="CHOISIR SON ADVERSAIRE",
            font=("Segoe UI", 12),
            bg=self.BG,
            fg=self.MUTED
        ).pack(pady=(20, 10))

        self.__aiChoice = ttk.Combobox(
            self.__homeFrame,
            values=["StupidBot", "Glouton", "MinMax H1", "MinMax H2", "MCTS"],
            state="readonly",
            width=25
        )
        self.__aiChoice.set("StupidBot")
        self.__aiChoice.pack()

        self.__startButton = tk.Button(
            self.__homeFrame,
            text="COMMENCER LA PARTIE",
            font=("Segoe UI", 12, "bold"),
            bg=self.TURQUOISE,
            fg=self.BG,
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=15,
            command=self.startGame
        )
        self.__startButton.pack(pady=25)
            
    
    def selectBoardMode(self, mode):
        self.__boardMode = mode

        if mode == "default":
            classicColor = self.LILAC
            classicText = self.BG

            customColor = self.CELL
            customText = self.TEXT
        else:
            classicColor = self.CELL
            classicText = self.TEXT

            customColor = self.LILAC
            customText = self.BG

        for item in self.__classicButton.find_all():
            if self.__classicButton.type(item) == "text":
                self.__classicButton.itemconfigure(
                    item,
                    fill=classicText
                )
            else:
                self.__classicButton.itemconfigure(
                    item,
                    fill=classicColor,
                    outline=classicColor
                )

        for item in self.__customButton.find_all():
            if self.__customButton.type(item) == "text":
                self.__customButton.itemconfigure(
                    item,
                    fill=customText
                )
            else:
                self.__customButton.itemconfigure(
                    item,
                    fill=customColor,
                    outline=customColor
                )

        if mode == "custom":
            self.__customFrame.pack(pady=20)
        else:
            self.__customFrame.pack_forget()

    
    def startGame(self):
        if self.__boardMode == "default":
            rows = 5
            cols = 10
        else:
            try:
                rows = int(self.__rowsEntry.get())
                cols = int(self.__colsEntry.get())
            except ValueError:
                messagebox.showerror(
                    "Erreur",
                    "Entre des nombres entiers pour les dimensions."
                )
                return

        if rows < 3 or cols < 3:
            messagebox.showerror(
                "Erreur",
                "Le plateau doit avoir au moins 3 lignes et 3 colonnes."
            )
            return

        self.__selectedAI = self.__aiChoice.get()
        self.__game = ManicMinelayers(rows, cols)
        self.showGame()
  
    def showGame(self):
        rows = self.__game.getRows()
        cols = self.__game.getCols()
        self.__homeFrame.destroy()

        self.__gameFrame = tk.Frame(self.__window, bg=self.BG)
        self.__gameFrame.pack(fill="both", expand=True)

        title = tk.Label(
            self.__gameFrame,
            text="MANIC MINELAYERS",
            font=("Segoe UI", 24, "bold"),
            bg=self.BG,
            fg=self.TEXT
        )
        title.pack(pady=25)

        self.__contentFrame = tk.Frame(self.__gameFrame, bg=self.BG)
        self.__contentFrame.pack(fill="both", expand=True, padx=30, pady=20)

        self.__boardFrame = tk.Frame(self.__contentFrame, bg=self.PANEL)
        self.__boardFrame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        self.__sideFrame = tk.Frame(
            self.__contentFrame,
            bg=self.BG,
            width=260
        )
        self.__sideFrame.pack(side="right", fill="y")
        self.__sideFrame.pack_propagate(False)

        self.__infoFrame = tk.Frame(
            self.__sideFrame,
            bg=self.PANEL,
            padx=20,
            pady=20
        )
        self.__infoFrame.pack(fill="x", pady=(0, 15))

        
        tk.Label(
            self.__infoFrame,
            text="INFORMATIONS",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 15))

        tk.Label(
            self.__infoFrame,
            text="■ Joueur A",
            bg=self.PANEL,
            fg=self.LILAC
        ).pack(anchor="w", pady=5)

        tk.Label(
            self.__infoFrame,
            text="■ IA " + self.__selectedAI,
            bg=self.PANEL,
            fg=self.TURQUOISE
        ).pack(anchor="w", pady=5)

        self.__turnLabel = tk.Label(
            self.__infoFrame,
            text="Placement initial",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 11, "bold")
        )
        self.__turnLabel.pack(anchor="w", pady=(20, 0))

        self.__commandFrame = tk.Frame(
            self.__sideFrame,
            bg=self.PANEL,
            padx=20,
            pady=20
        )
        self.__commandFrame.pack(fill="x")
        tk.Label(
            self.__commandFrame,
            text="COMMANDES",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 15))

        tk.Button(
            self.__commandFrame,
            text="Nouvelle partie",
            bg=self.LILAC,
            fg=self.BG,
            relief="flat",
            cursor="hand2",
            command=self.newGame
        ).pack(fill="x", pady=5, ipady=8)

        tk.Button(
            self.__commandFrame,
            text="Règles du jeu",
            bg=self.CELL,
            fg=self.TEXT,
            relief="flat",
            cursor="hand2",
            command=self.showRules
        ).pack(fill="x", pady=5, ipady=8)

        self.__statsButton = tk.Button(
            self.__commandFrame,
            text="Lancer les statistiques",
            command=self.launchStats,
            bg=self.LILAC,
            fg=self.BG,
            relief="flat",
            cursor="hand2",
          
        )
        self.__statsButton.pack(pady=5, ipady=8, fill="x")

        self.__placed = False
        self.__winnerShown = False
        self.__botTask = None
        
        if self.__selectedAI == "Glouton":
            self.__bot = Glouton(self.__game, 2)

        elif self.__selectedAI == "MinMax H1":
            self.__bot = MinMax(self.__game, 2, depth=4, heuristic=1)

        elif self.__selectedAI == "MinMax H2":
            self.__bot = MinMax(self.__game, 2, depth=4, heuristic=2)

        elif self.__selectedAI == "MCTS":
            self.__bot = MCTS(self.__game, 2)

        else:
            self.__bot = StupidBot(self.__game, 2)


        cellSize = min(65, 700 // cols, 480 // rows)
        self.__cellSize = cellSize

        self.__board = tk.Canvas(
            self.__boardFrame,
            width=cols * cellSize +30,
            height=rows * cellSize + 30,
            bg=self.PANEL,
            highlightthickness=0
        )
        self.__board.pack(expand=True, pady=20)
        for row in range(rows):
            for col in range(cols):
                x1 = 30 + col * cellSize
                y1 = 30 + row * cellSize
                x2 = x1 + cellSize
                y2 = y1 + cellSize

                color = self.CELL

                if col == 0:
                    color = self.LILAC_START

                self.__board.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=self.BG,
                    width=3
                )

                if row == 0:

                    self.__board.create_text(
                        x1 + cellSize / 2, 15,
                        text=str(col + 1),
                        fill=self.MUTED
                    )

                if col == 0:
                    self.__board.create_text(
                        15, y1 + cellSize / 2,
                        text=str(row + 1),
                        fill=self.MUTED
                    )

        self.__board.bind("<Button-1>", self.onBoardClick)

    def newGame(self):
        if self.__botTask is not None:
            self.__window.after_cancel(self.__botTask)
            self.__botTask = None

        self.__gameFrame.destroy()
        self.showHome()

    def showRules(self):
        messagebox.showinfo(
            "Règles de Manic Minelayers",
            "Chaque joueur commence à une extrémité du plateau.\n\n"
            "Les déplacements se font en L, comme un cavalier aux échecs.\n\n"
            "Chaque case quittée devient une mine et ne peut plus être utilisée.\n\n"
            "Le but est de bloquer son adversaire."
        )

    def launchStats(self):
        print("Lancement des statistiques...")
        threading.Thread(
            target=self.runStats,
            daemon=True
        ).start()

    def runStats(self):
        try:
            concours = Concours(100)
            concours.run()
            print("Statistiques terminées.")
        except Exception:
            traceback.print_exc()


    def checkWinner(self):
        winner = self.__game.getWinner()

        if winner is None or self.__winnerShown:
            return

        self.__winnerShown = True

        if winner == 1:
            messagebox.showinfo(
                "Fin de partie",
                "Le joueur A a gagné !"
            )
        elif winner == 2:
            messagebox.showinfo(
                "Fin de partie",
                "L'IA a gagné !"
            )
        else:
            messagebox.showinfo(
                "Fin de partie",
                "Match nul !"
            )

    
    def onBoardClick(self, event):
        row = (event.y - 30) // self.__cellSize
        col = (event.x - 30) // self.__cellSize

        if not self.__game.isInside(row, col):
            return

        if not self.__placed:
            if col != 0:
                return

            if self.__game.placePlayer(1, row):
                if self.__selectedAI == "StupidBot":
                    botRow = random.randrange(self.__game.getRows())
                else:
                    botRow = self.__bot.choosePlacement()

                self.__game.placePlayer(2, botRow)
                self.__placed = True
                self.showPlayers()
                self.checkWinner()

            return

        if self.__game.getWinner() is not None:
            return

        if self.__game.getCurrentPlayer() != 1:
            return

        if self.__game.movePlayer(1, row, col):
            self.showPlayers()
            self.checkWinner()

            if self.__game.getWinner() is None:
                self.__botTask = self.__window.after(
                    500,
                    self.playBot
                )

    def showPlayers(self):
        self.__board.delete("players")
        self.__board.delete("start")

        if self.__placed:
            for row in range(self.__game.getRows()):
                x = 30
                y = 30 + row * self.__cellSize

                self.__board.create_rectangle(
                    x, y,
                    x + self.__cellSize,
                    y + self.__cellSize,
                    fill=self.CELL,
                    outline=self.BG,
                    width=3,
                    tags="start"
                )

        grid = self.__game.getGrid()
        size = self.__cellSize

        moves = []

        if self.__placed and self.__game.getCurrentPlayer() == 1:
            moves = self.__game.getValidMoves(1)

        for row in range(self.__game.getRows()):
            for col in range(self.__game.getCols()):
                value = grid[row][col]

                x = 30 + col * size
                y = 30 + row * size

                if (row, col) in moves:
                    self.__board.create_rectangle(
                        x + 3, y + 3,
                        x + size - 3, y + size - 3,
                        fill="#39334D",
                        outline="",
                        tags="players"
                    )
                    
                if value == 3:
                    self.__board.create_rectangle(
                        x + 3, y + 3,
                        x + size - 3, y + size - 3,
                        fill="#40232E",
                        outline="",
                        tags="players"
                    )

                    self.__board.create_line(
                        x + 8, y + 8,
                        x + size - 8, y + size - 8,
                        fill=self.RED,
                        width=6,
                        tags="players"
                    )

                    self.__board.create_line(
                        x + size - 8, y + 8,
                        x + 8, y + size - 8,
                        fill=self.RED,
                        width=6,
                        tags="players"
                    )

                if value == 1 or value == 2:
                    if value == 1:
                        color = self.LILAC
                        letter = "A"
                    else:
                        color = self.TURQUOISE
                        letter = "B"

                    self.__board.create_rectangle(
                        x + 4, y + 4,
                        x + size - 4, y + size - 4,
                        fill=color,
                        outline="",
                        tags="players"
                    )

                    self.__board.create_text(
                        x + size / 2,
                        y + size / 2,
                        text=letter,
                        fill=self.BG,
                        font=("Segoe UI", 12, "bold"),
                        tags="players"
                    )

        self.updateTurn()

    def playBot(self):
        self.__botTask = None

        if self.__game.getWinner() is not None:
            self.checkWinner()
            return

        move = self.__bot.chooseMove()

        if move is not None:
            self.__game.movePlayer(2, move[0], move[1])
            
        self.showPlayers()
        self.checkWinner()

    def updateTurn(self):
        winner = self.__game.getWinner()

        if winner is not None:
            text = "Partie terminée"
            color = self.TEXT
        elif self.__game.getCurrentPlayer() == 1:
            text = "Tour du joueur A"
            color = self.LILAC
        else:
            text = "Tour de l'IA"
            color = self.TURQUOISE

        self.__turnLabel.config(text=text, fg=color)

    def run(self):
        self.__window.mainloop()
