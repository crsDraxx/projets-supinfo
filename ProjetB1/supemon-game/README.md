# Supemon Game

Jeu de combat au tour par tour en C, inspiré de Pokémon. Projet de 1ère année (B1) à SUPINFO.

## Fonctionnalités
- Combats contre des Supémons
- Boutique pour acheter des objets
- Centre Supemon pour soigner son équipe
- Menu principal en console

## Compilation et lancement

Avec GCC :
```bash
gcc main.c supemon.c -o supemon
./supemon
```

Avec Code::Blocks : ouvrir `Supemon_game.cbp`, puis compiler et lancer.

## Organisation des fichiers
| Fichier | Rôle |
|---|---|
| `main.c` | Menu principal et boucle du jeu |
| `supemon.c` | Logique du jeu (combats, boutique, centre Supemon) |
| `Supemon_game.cbp` | Projet Code::Blocks |

## Technologies
C, Code::Blocks