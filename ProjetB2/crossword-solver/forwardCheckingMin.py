from logic import is_compatible
from forwardChecking import update_domains, restore_domains


def forward_checking_min(variables, domains, neighbors, assignment=None):
    if assignment is None:
        assignment = {}

    # cas de base : toutes les variables ont un mot
    if len(assignment) == len(variables):
        return assignment

    # prendre la variable non assignée avec le plus petit domaine
    unassigned = [var for var in variables if var not in assignment]
    next_var = min(unassigned, key=lambda var: len(domains[var]))

    # essayer avec chaque mot du domaine de la variable
    for word in domains[next_var]:
        if is_compatible(next_var, word, assignment, neighbors):
            assignment[next_var] = word

            removed_words = update_domains(variables, domains, assignment, neighbors)

            empty_domain = False
            for var in variables:
                if var not in assignment and len(domains[var]) == 0:
                    empty_domain = True
                    break

            if not empty_domain:
                result = forward_checking_min(variables, domains, neighbors, assignment)
                if result is not None:
                    return result

            restore_domains(domains, removed_words)
            del assignment[next_var]

    return None