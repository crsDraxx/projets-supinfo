from logic import is_compatible


def backtracking(variables, domains, neighbors, assignment=None):
    if assignment is None:
        assignment = {}

    # cas de base : toutes les variables ont un mot
    if len(assignment) == len(variables):
        return assignment

    # variable sans mot
    for var in variables:
        if var not in assignment:
            next_var = var
            break

    # essayer avec chaque mot du domaine de la variable
    for word in domains[next_var]:
        if is_compatible(next_var, word, assignment, neighbors):
            assignment[next_var] = word

            result = backtracking(variables, domains, neighbors, assignment)
            if result is not None:
                return result

            del assignment[next_var]

    return None