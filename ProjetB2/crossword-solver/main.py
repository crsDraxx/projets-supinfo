import time
from logic import read_grid_file, read_dict_file, determine_variables, determine_domains, display_solution, get_neighbors
from backtracking import backtracking
from forwardChecking import forward_checking
from forwardCheckingMin import forward_checking_min


def choose_data():
    print("\n Quel mots croisés voulez-vous?")
    print("1. gridMP1 + dictMP1")
    print("2. gridMP2 + dictMP2")
    choice = input("Votre choix (1 ou 2) : ")

    if choice == "1":
        return "data/gridMP1.txt", "data/dictMP1.txt"
    elif choice == "2":
        return "data/gridMP2.txt", "data/dictMP2.txt"
    else:
        print("Choix invalide, gridMP1 choisi par defaut.")
        return "data/gridMP1.txt", "data/dictMP1.txt"


def choose_algorithm():
    print("\n Choisissez l'algorithme")
    print("1. Backtracking")
    print("2. Forward Checking")
    print("3. Forward Checking MRV")
    print("4. Les trois")
    choice = input("Votre choix (1, 2, 3 ou 4) : ")
    return choice


def run(algo_name, algo_func, variables, domains, neighbors, grid):
    print(f"         {algo_name}")
    print("En cours...")

    start = time.time()
    solution = algo_func(variables, domains.copy(), neighbors)
    time_passed = time.time() - start

    if solution:
        display_solution(grid, solution)
        print(f"Temps : {time_passed:.4f}s")
    else:
        print("Aucune solution trouvée.")


#lancement de résolution => appel des autres fonctions

grid_path, dict_path = choose_data()

grid      = read_grid_file(grid_path)
words     = read_dict_file(dict_path)
variables = determine_variables(grid)
domains   = determine_domains(variables, words)
neighbors = get_neighbors(variables)        

print(f"\nGrille chargée : {len(variables)} variables")

choice = choose_algorithm()

if choice == "1":
    run("BACKTRACKING", backtracking, variables, domains, neighbors, grid)
elif choice == "2":
    run("FORWARD CHECKING", forward_checking, variables, domains, neighbors, grid)
elif choice == "3":
    run("FORWARD CHECKING MRV", forward_checking_min, variables, domains, neighbors, grid)
elif choice == "4":
    run("BACKTRACKING", backtracking, variables, domains, neighbors, grid)
    run("FORWARD CHECKING", forward_checking, variables, domains, neighbors, grid)
    run("FORWARD CHECKING MRV", forward_checking_min, variables, domains, neighbors, grid)
else:
    print("Choix invalide.")