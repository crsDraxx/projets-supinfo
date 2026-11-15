#pragma once
#include <memory>
#include <vector>
#include <iostream>
#include <windows.h>



using namespace std;

// Type pour représenter une forme de tuile
using Shape = vector<vector<char>>;

struct TileInfo {
    string name;
    Shape shape;
};

class PiecesShape {
private:
    // Toutes les formes de tuiles possibles (Blokus standard)
    vector<TileInfo> allShapes;

    // Initialiser toutes les formes
    void initializeShapes();

public:
    // Constructeur
    PiecesShape();

    // Obtenir toutes les formes
    vector<TileInfo> getAllShapes() const;

    // Rotation de 90° dans le sens horaire
    Shape rotate(const Shape& shape) const;

    // Retournement horizontal
    Shape flip(const Shape& shape) const;

    // Afficher une tuile avec couleur
    void displayTile(const Shape& shape, const string& colorCode) const;
};
