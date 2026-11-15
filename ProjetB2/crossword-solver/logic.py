# lire les fichiers grid et dict

def read_grid_file(file_name):
    grid = []

    with open(file_name, "r") as f:
        for line in f:
            row = []
            for c in line.rstrip('\n'):
                if c == "_":
                    row.append(0)
                elif c == "#":
                    row.append(1)
            if row:
                grid.append(row)
    return grid


def read_dict_file(file_name):
    words = []

    with open(file_name, "r") as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words


# trouver les variables

def determine_variables(grid):
    variables = []
    nb_rows = len(grid)
    nb_cols = len(grid[0])

    # mots horizontaux
    for i in range(nb_rows):
        j = 0
        while j < nb_cols:
            if grid[i][j] == 0:
                start = j
                length = 0
                while j < nb_cols and grid[i][j] == 0:
                    j += 1
                    length += 1
                if length >= 2:
                    variables.append((i, start, True, length))
            else:
                j += 1

    # mots verticaux
    for j in range(nb_cols):
        i = 0
        while i < nb_rows:
            if grid[i][j] == 0:
                start = i
                length = 0
                while i < nb_rows and grid[i][j] == 0:
                    i += 1
                    length += 1
                if length >= 2:
                    variables.append((start, j, False, length))
            else:
                i += 1

    return variables


# trouver les domaines

def determine_domains(variables, words):
    domains = {}
    for var in variables:
        length = var[3]
        possible_words = []
        for word in words:
            if len(word) == length:
                possible_words.append(word)
        domains[var] = possible_words
    return domains


# trouver les cases occupées par une variable

def get_word_cells(var):
    i, j, h, l = var
    cells = []
    for k in range(l):
        if h:
            cells.append((i, j + k))
        else:
            cells.append((i + k, j))
    return cells


# précalculer les croisements entre variables une seule fois

def get_neighbors(variables):
    neighbors = {var: [] for var in variables}

    for i, var in enumerate(variables):
        cells_var = get_word_cells(var)
        for j, other_var in enumerate(variables):
            if i >= j:
                continue
            cells_other = get_word_cells(other_var)
            for k, cell in enumerate(cells_var):
                if cell in cells_other:
                    idx_other = cells_other.index(cell)
                    neighbors[var].append((other_var, k, idx_other))
                    neighbors[other_var].append((var, idx_other, k))

    return neighbors


# vérifier si le mot est compatible avec les mots déjà placés

def is_compatible(var, word, assignment, neighbors):
    for (other_var, idx_var, idx_other) in neighbors[var]:
        if other_var in assignment:
            if word[idx_var] != assignment[other_var][idx_other]:
                return False
    return True


# afficher la grille complétée

def display_solution(grid, assignment):
    nb_rows = len(grid)
    nb_cols = len(grid[0])

    result = []
    for i in range(nb_rows):
        row = []
        for j in range(nb_cols):
            if grid[i][j] == 1:
                row.append('  ')
            else:
                row.append('  ')
        result.append(row)

    for var, word in assignment.items():
        cells = get_word_cells(var)
        for k, (r, c) in enumerate(cells):
            result[r][c] = ' ' + word[k]

    separator = '+' + ('--+' * nb_cols)
    print(separator)
    for row in result:
        print('|' + '|'.join(row) + '|')
        print(separator)