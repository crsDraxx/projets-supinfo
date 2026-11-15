#include <iostream>
#include <iomanip>
#include <random>
#include <cmath>
#include <windows.h>  // Ajoutez cette ligne si manquante (pour HANDLE et SetConsoleTextAttribute)
#include "Board.hpp"
#include "Players.hpp"
#include "PiecesShape.hpp"
#include "Pieces.hpp"
#include <vector>

#include <algorithm>

// Constructeur
PiecesShape::PiecesShape() {
    initializeShapes();
}

// Initialiser toutes les formes de tuiles
void PiecesShape::initializeShapes() {
    // Monomino (1 carré)
    allShapes.push_back({"I1", {
        {'X'}
    }});

    // Domino (2 carrés)
    allShapes.push_back({"I2", {
        {'X', 'X'}
    }});

    // Trominos (3 carrés)
    allShapes.push_back({"I3", {
        {'X', 'X', 'X'}
    }});

    allShapes.push_back({"L3", {
        {'X', '.'},
        {'X', 'X'}
    }});

    // Tetrominos (4 carrés)
    allShapes.push_back({"I4", {
        {'X', 'X', 'X', 'X'}
    }});

    allShapes.push_back({"O4", {
        {'X', 'X'},
        {'X', 'X'}
    }});

    allShapes.push_back({"T4", {
        {'X', 'X', 'X'},
        {'.', 'X', '.'}
    }});

    allShapes.push_back({"L4", {
        {'X', '.'},
        {'X', '.'},
        {'X', 'X'}
    }});

    allShapes.push_back({"Z4", {
        {'X', 'X', '.'},
        {'.', 'X', 'X'}
    }});

    // Pentominos (5 carrés)
    allShapes.push_back({"I5", {
        {'X', 'X', 'X', 'X', 'X'}
    }});

    allShapes.push_back({"L5", {
        {'X', '.'},
        {'X', '.'},
        {'X', '.'},
        {'X', 'X'}
    }});

    allShapes.push_back({"T5", {
        {'X', 'X', 'X'},
        {'.', 'X', '.'},
        {'.', 'X', '.'}
    }});

    allShapes.push_back({"P5", {
        {'X', 'X'},
        {'X', 'X'},
        {'X', '.'}
    }});

    allShapes.push_back({"W5", {
        {'X', '.', '.'},
        {'X', 'X', '.'},
        {'.', 'X', 'X'}
    }});

    allShapes.push_back({"U5", {
        {'X', '.', 'X'},
        {'X', 'X', 'X'}
    }});

    allShapes.push_back({"F5", {
        {'.', 'X', 'X'},
        {'X', 'X', '.'},
        {'.', 'X', '.'}
    }});

    allShapes.push_back({"X5", {
        {'.', 'X', '.'},
        {'X', 'X', 'X'},
        {'.', 'X', '.'}
    }});

    allShapes.push_back({"Z5", {
        {'X', 'X', '.'},
        {'.', 'X', '.'},
        {'.', 'X', 'X'}
    }});

    allShapes.push_back({"V5", {
        {'X', '.', '.'},
        {'X', '.', '.'},
        {'X', 'X', 'X'}
    }});

    allShapes.push_back({"N5", {
        {'.', 'X'},
        {'X', 'X'},
        {'X', '.'},
        {'X', '.'}
    }});

    allShapes.push_back({"Y5", {
        {'.', 'X'},
        {'X', 'X'},
        {'.', 'X'},
        {'.', 'X'}
    }});
}

// Obtenir toutes les formes
vector<TileInfo> PiecesShape::getAllShapes() const {
    return allShapes;
}

// Rotation de 90° dans le sens horaire
Shape PiecesShape::rotate(const Shape& shape) const {
    if (shape.empty() || shape[0].empty()) {
        return shape;
    }

    int n = shape.size();
    int m = shape[0].size();
    Shape rotated(m, vector<char>(n, '.'));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            rotated[j][n-1-i] = shape[i][j];
        }
    }
    return rotated;
}

// Retournement horizontal
Shape PiecesShape::flip(const Shape& shape) const {
    Shape flipped = shape;
    for (auto& row : flipped) {
        reverse(row.begin(), row.end());
    }
    return flipped;
}

// Afficher une tuile avec couleur
void PiecesShape::displayTile(const Shape& shape, const string& colorCode) const {
    for (const auto& row : shape) {
        for (char c : row) {
            if (c == 'X') {
                cout << colorCode << "■ " << "\033[0m";
            } else {
                cout << "  ";
            }
        }
        cout << endl;
    }
}
