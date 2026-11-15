# Résolveur de mots croisés

Projet d'algorithmique de 2ème année (B2) à SUPINFO. Il résout des mots croisés en les modélisant comme un problème de satisfaction de contraintes (CSP) et compare trois algorithmes.

## Points clés
- Modélisation CSP : variables, domaines, contraintes de croisement
- Trois algorithmes comparés : backtracking, forward checking, forward checking avec heuristique MRV
- Version terminal et interface graphique Tkinter
- Aucune dépendance externe

## Structure
```
crossword-solver/
├── data/
│   ├── dictMP1.txt
│   ├── dictMP2.txt
│   ├── gridMP1.txt
│   └── gridMP2.txt
├── logic.py               # Lecture des fichiers, variables, domaines, contraintes
├── backtracking.py        # Algorithme 1 : Backtracking
├── forwardChecking.py     # Algorithme 2 : Forward Checking
├── forwardCheckingMin.py  # Algorithme 3 : Forward Checking + MRV
├── main.py                # Version terminal
└── gui.py                 # Interface graphique Tkinter
```

## Prérequis
- Python 3.10+
- Tkinter (inclus avec Python)

## Lancement
```bash
python main.py   # version terminal
python gui.py    # interface graphique
```

## Format des fichiers
**Grille** : `_` = case blanche, `#` = case noire.
```
___#
_#__
____
_#_#
##__
##_#
```
**Dictionnaire** : un mot par ligne.
```
ant
bus
car
year
search
```

## Modélisation
- **Variable** : un quadruplet `(i, j, h, l)` = ligne de départ, colonne de départ, horizontal (`True`) ou vertical (`False`), longueur.
- **Domaine** : tous les mots du dictionnaire dont la longueur est égale à `l`.
- **Contrainte** : deux mots qui se croisent partagent la même lettre à la case commune.

## Algorithmes
1. **Backtracking** : essais et retours en arrière. Dans le pire cas, il explore tout l'espace de recherche (complexité exponentielle).
2. **Forward Checking** : après chaque assignation, retire des domaines des variables restantes les mots devenus incompatibles. Dès qu'un domaine est vide, il revient en arrière sans continuer.
3. **Forward Checking + MRV** : choisit en priorité la variable dont le domaine est le plus petit (Minimum Remaining Values), donc la plus contrainte.

## Résultats
| Algorithme | gridMP1 | gridMP2 |
|---|---|---|
| Backtracking | ~0 s | très long |
| Forward Checking | ~0 s | long |
| Forward Checking MRV | ~0 s | ~206 s |

MRV > Forward Checking > Backtracking. L'écart devient très net sur les grandes grilles avec un grand dictionnaire.

## Technologies
Python, Tkinter, algorithmique (CSP, backtracking, heuristiques)