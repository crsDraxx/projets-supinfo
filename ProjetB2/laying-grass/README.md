# Laying Grass

Jeu de plateau multijoueur en console, en C++. Projet de 2ème année (B2) à SUPINFO. Chaque joueur place des tuiles de formes variées sur un plateau partagé.

> **Statut : en cours de développement.** Le plateau, les pièces et le placement de départ sont en place. La boucle de jeu complète n'est pas terminée.

## Fonctionnalités
- 2 à 9 joueurs : plateau 20x20 (2 à 4 joueurs) ou 30x30 (5 à 9 joueurs)
- Placement aléatoire de cases bonus : Exchange (`E`), Stone (`S`), Robbery (`R`)
- Une vingtaine de formes de tuiles (du monomino au pentomino), avec rotation et retournement
- Affichage en console avec une couleur par joueur
- Placement de la pièce de départ de chaque joueur

## Organisation des fichiers
| Fichier | Rôle |
|---|---|
| `main.cpp` | Point d'entrée |
| `Board.cpp` / `Board.hpp` | Plateau, affichage, bonus, boucle de jeu |
| `Players.cpp` / `Players.hpp` | Joueurs (nom, pièce de départ, couleur) |
| `PiecesShape.cpp` / `PiecesShape.hpp` | Formes des tuiles, rotation, retournement |
| `Pieces.cpp` / `Pieces.hpp` | Gestion des pièces |
| `Laying_Grass.cbp` | Projet Code::Blocks |

## Prérequis
- Compilateur C++ (g++ / MinGW)
- **Windows uniquement** : le projet utilise `<windows.h>` pour les couleurs de la console

## Compilation
Avec Code::Blocks : ouvrir `Laying_Grass.cbp`, puis compiler et lancer.

Avec g++ :
```bash
g++ *.cpp -o laying_grass
```

## Remarque
Le projet est conservé tel qu'il a été rendu. Le dossier contient aussi quelques fichiers hérités d'un autre exercice (`Board.h`, `Boat.cpp`, `Boat.hpp`).

## Technologies
C++, programmation orientée objet, Code::Blocks