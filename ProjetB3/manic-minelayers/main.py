
from ManicMinelayers import ManicMinelayers
from GUI import GUI

if __name__ == "__main__":
    game = ManicMinelayers()
    interface = GUI(game)
    interface.run()
