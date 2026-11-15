#ifndef PIECESSHAPE_HPP
#define PIECESSHAPE_HPP

#include <vector>

struct ShapeMatrix {
    std::string name;             // Nom de la pièce
    int matrix[4][4];             // Forme de la pièce (0 = vide, 1+ = bloc)
};

class PiecesShape {
public:
    static std::vector<ShapeMatrix> getShapes(char playerSymbol);
};

#endif
