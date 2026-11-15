# Manic Minelayers

Jeu de stratégie en Python avec interface Tkinter, réalisé en 3ème année (B3) à SUPINFO.

Le joueur affronte une intelligence artificielle sur un plateau rectangulaire. Les déplacements se font en L, comme ceux du cavalier aux échecs. Chaque case quittée devient bloquée. Le premier joueur qui ne peut plus bouger perd.

## Points clés
- Plusieurs IA comparées : aléatoire, glouton, MinMax avec élagage alpha-bêta (2 heuristiques) et Monte-Carlo Tree Search
- Mode statistiques : tournoi automatique entre toutes les IA
- Interface graphique Tkinter, sans dépendance externe

## Prérequis
- Python 3
- Tkinter (inclus avec Python sur Windows et macOS)

Aucune bibliothèque externe : pas de `pip install`.

## Lancement
```bash
python main.py
```
Sous Windows, si `python` ne fonctionne pas : `py main.py`.

## Jouer une partie
1. Choisir la taille du plateau : **Classique** (5 lignes x 10 colonnes) ou **Personnalisé**.
2. Choisir l'IA adverse.
3. Cliquer sur **Commencer la partie**, puis sur une case de la première colonne pour placer ton pion A.

L'IA place son pion B sur la dernière colonne.

### Règles
- Déplacements en L (cavalier).
- Les cases accessibles sont indiquées en lilas atténué.
- Une case quittée devient bloquée (croix rouge).
- Les joueurs jouent à tour de rôle.
- Si un joueur ne peut plus bouger, l'autre gagne. Si aucun ne peut bouger, c'est un match nul.

## Les intelligences artificielles
| IA | Principe |
|---|---|
| **StupidBot** | Choisit un déplacement au hasard |
| **Glouton** | Choisit le coup qui maximise le nombre de ses propres déplacements possibles ensuite |
| **MinMax H1** | MinMax avec élagage alpha-bêta (profondeur 4). Heuristique : nombre de mes coups moins nombre de coups adverses |
| **MinMax H2** | Même algorithme, heuristique de territoire : nombre de cases atteignables avant l'adversaire (parcours en largeur) |
| **MCTS** | Monte-Carlo Tree Search (sélection UCB, expansion, simulation aléatoire, rétropropagation) |

Certaines IA peuvent mettre plus de temps à jouer.

## Mode statistiques
Le bouton **Lancer les statistiques** organise un concours entre toutes les IA : chaque paire joue 100 parties dans chaque ordre. Les résultats s'affichent dans le terminal qui a lancé le programme. Les simulations peuvent être longues.

## Organisation des fichiers
| Fichier | Rôle |
|---|---|
| `main.py` | Point d'entrée |
| `GUI.py` | Interface graphique Tkinter |
| `ManicMinelayers.py` | Plateau, déplacements et règles |
| `Human.py` | Joueur humain |
| `StupidBot.py` | IA aléatoire |
| `Glouton.py` | IA gloutonne |
| `MinMax.py` | MinMax et heuristiques |
| `MCTS.py` | Monte-Carlo Tree Search |
| `Sommet.py` | Nœuds de l'arbre MCTS |
| `Match.py` | Gestion d'une partie entre deux joueurs |
| `Concours.py` | Tournoi et statistiques |

## En cas de problème
1. Vérifier Python : `python --version` ou `py --version`.
2. Ouvrir le terminal dans le dossier contenant `main.py`.
3. Vérifier que tous les fichiers `.py` sont présents.
4. Tester Tkinter : `python -m tkinter` doit ouvrir une petite fenêtre.

## Technologies
Python, Tkinter, algorithmique de jeux (MinMax, alpha-bêta, MCTS)