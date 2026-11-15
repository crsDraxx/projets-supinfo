from logic import is_compatible


def update_domains(variables, domains, assignment, neighbors):
    removed_words = {}

    for var in variables:
        if var not in assignment:
            removed_words[var] = []

            for word in domains[var][:]:
                if not is_compatible(var, word, assignment, neighbors):
                    domains[var].remove(word)
                    removed_words[var].append(word)

    return removed_words


def restore_domains(domains, removed_words):
    for var, words in removed_words.items():
        for word in words:
            domains[var].append(word)


def forward_checking(variables, domains, neighbors, assignment=None):
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

            removed_words = update_domains(variables, domains, assignment, neighbors)

            empty_domain = False
            for var in variables:
                if var not in assignment and len(domains[var]) == 0:
                    empty_domain = True
                    break

            if not empty_domain:
                result = forward_checking(variables, domains, neighbors, assignment)
                if result is not None:
                    return result

            restore_domains(domains, removed_words)
            del assignment[next_var]

    return None