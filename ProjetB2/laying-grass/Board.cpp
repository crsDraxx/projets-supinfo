#include <iostream>
#include <iomanip>
#include <random>
#include <cmath>
#include "Board.hpp"
#include "Players.hpp"
#include "PiecesShape.hpp"
#include "Pieces.hpp"
#include <vector>
#include <algorithm>

using namespace std;

// create board
Board::Board(int nbPlayers, char emptySymbol){
    if (nbPlayers >= 2 && nbPlayers <= 4){
        boardSize = 20;

    }else if (nbPlayers >= 5 && nbPlayers <= 9){
        boardSize = 30;

    }else{
        cout << "Nombre de joueurs invalide!" <<endl;
        boardSize = 0;
    }
    emptySymbol = '.';
    board = vector<vector<char>>(boardSize,vector<char>(boardSize, emptySymbol));
};

// Vérifie si une case est libre pour poser une tuile (pas une case spéciale et pas occupée)
    bool Board::isEmpty(int x, int y) const {
        if (x < 0 || y < 0 || x >= boardSize || y >= boardSize) return false;
        char c = board[x][y];
        if (c == '.' ) return true;       // case vide
        return false;                      // occupée ou case spéciale
    }
    // Place une tuile sur le plateau
    void Board::placeTile(int x, int y, char piece) {
        if (isEmpty(x, y)) {
            board[x][y] = piece;
        } else {
            cout << "Impossible de placer la tuile ici !" << endl;
        }
    }

//display board
void Board::displayBoard(){
    int lines = boardSize;
    int columns = boardSize;

    // Display column index
    cout << "   ";
    for (int c = 0; c < columns; ++c) {
        char letter = 'A' + c;
        cout << setw(2) << letter << " ";
    }
    cout << "\n";

    // Display line index and lines
    for (int l = 0; l < lines; ++l) {
        char letter = 'A' + l;
        cout << setw(2) << letter << " ";
        for (int c = 0; c < columns; ++c) {
            cout << " " << board[l][c] << " ";
        }
        cout << "\n";
    }
};

// Bonus squares
void Board::placeSpecialTiles(int nbPlayers) {

    // ---- Determination of bonus pieces ----
    int numE = ceil(1.5 * nbPlayers); // Exchange
    int numS = ceil(0.5 * nbPlayers); // Stone
    int numR = nbPlayers;             // Robbery

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(1, boardSize - 2);

    auto isValidPosition = [&](int r, int c) -> bool {
        return (r > 0 && c > 0 && r < boardSize - 1 && c < boardSize - 1);
    };

    auto isNearBonus = [&](int r, int c) -> bool {
        for (int dr = -1; dr <= 1; ++dr) {
            for (int dc = -1; dc <= 1; ++dc) {
                int nr = r + dr, nc = c + dc;
                if (nr >= 0 && nc >= 0 && nr < boardSize && nc < boardSize) {
                    if (board[nr][nc] == 'E' || board[nr][nc] == 'S' || board[nr][nc] == 'R')
                        return true;
                }
            }
        }
        return false;
    };

    auto placeBonus = [&](char symbol, int count) {
        int placed = 0;
        while (placed < count) {
            int r = dist(gen);
            int c = dist(gen);

            if (isValidPosition(r, c) && !isNearBonus(r, c) && board[r][c] == '.') {
                board[r][c] = symbol;
                placed++;
            }
        }
    };

    //Placement des bonus
    placeBonus('E', numE); // Exchange
    placeBonus('S', numS); // Stone
    placeBonus('R', numR); // Robbery

};



// --- Boucle complète du jeu ---
// Étape 1 : placement des starter pieces
// Étape 2 : chaque joueur joue à tour de rôle en plaçant ses pièces
void Board::startGame(std::vector<Players>& players, int totalRounds) {
    int nbPlayers = players.size();




    // --- Étape 1 : placement des pièces de départ ---
    for (int i = 0; i < nbPlayers; ++i) {
        Players &p = players[i];
        bool valid = false;
        char lineChar, colChar;
        int x, y;

        while (!valid) {
            cout << "\n=== Placement des pieces de depart ===\n";
            cout << "\n" << p.getName() << ", place ta piece de depart.\n";
            displayBoard();
            cout << "\n " <<endl;
            cout << "Line (most top-left square of the tile): ";
            cin >> lineChar;
            cout << "Column (most top-left square of the tile): ";
            cin >> colChar;

            x = toupper(lineChar) - 'A';
            y = toupper(colChar) - 'A';

            if (x < 0 || x >= getSize() || y < 0 || y >= getSize()) {
                cout << "❌ Coordonnees hors plateau ! Reessaie.\n";
                continue;
            }
            if (!isEmpty(x, y)) {
                cout << "❌ Case déjà occupee ! Reessaie.\n";
                continue;
            }

            // Place la pièce de départ (symbole unique du joueur)
            placeTile(x, y, p.getStarterPiece());
            valid = true;
        }
        displayBoard();
    }
    cout << "\n " <<endl;
    cout << "\n " <<endl;
    cout << "\n " <<endl;

    // --- Étape 2 : tours de jeu avec les pièces ---
    Pieces pieceManager; // gestionnaire de toutes les pièces
    int currentTurn = 0;
    int nbTotalTurns = totalRounds * nbPlayers;

    while (currentTurn < nbTotalTurns) {
        int playerIndex = currentTurn % nbPlayers;
        Players &p = players[playerIndex];


        cout << "\nJoueur: " << p.getName() << " (" << playerIndex + 1 << ")"
             << " - Tour" << (currentTurn + 1) << endl;
        displayBoard();

        // Récupération des pièces du joueur




        string chosenPieceName;
        cout << "\n " <<endl;
        cout << "Choisis une piece à placer : ";
        cin >> chosenPieceName;
        cout << "\n " <<endl;



        // Placement de la pièce sur le plateau
        bool placed = false;
        while (!placed) {
            char lineChar, colChar;
            int x, y;
            cout << "Line (most top-left square of the tile): ";
            cin >> lineChar;
            cout << "Column (most top-left square of the tile): ";
            cin >> colChar;

            x = toupper(lineChar) - 'A';
            y = toupper(colChar) - 'A';





        }

        currentTurn++;
    }

    cout << "\n=== Fin de la partie ===\n";
}
