#include "Pieces.hpp"
#include "PiecesShape.hpp"
#include <vector>
#include <string>

#include <cctype>

// Constructeur
Pieces::Pieces() {
    // Le shapeManager est automatiquement initialisé
}

// Initialiser les pièces pour un joueur
void Pieces::initPlayerPieces(char playerLetter) {
    // Chaque joueur commence avec toutes les formes disponibles
    playerPieces[playerLetter] = shapeManager.getAllShapes();
}

// Obtenir les tuiles disponibles pour un joueur
vector<TileInfo> Pieces::getPlayerTiles(char playerLetter) const {
    auto it = playerPieces.find(playerLetter);
    if (it != playerPieces.end()) {
        return it->second;
    }
    return vector<TileInfo>(); // Retourne un vecteur vide si le joueur n'existe pas
}

// Retirer une tuile après utilisation
bool Pieces::removeTile(char playerLetter, const string& tileName) {
    auto it = playerPieces.find(playerLetter);
    if (it == playerPieces.end()) {
        return false;
    }

    auto& tiles = it->second;
    for (auto tileIt = tiles.begin(); tileIt != tiles.end(); ++tileIt) {
        if (tileIt->name == tileName) {
            tiles.erase(tileIt);
            return true;
        }
    }
    return false;
}

// Vérifier si un joueur a encore des tuiles
bool Pieces::hasRemainingTiles(char playerLetter) const {
    auto it = playerPieces.find(playerLetter);
    if (it != playerPieces.end()) {
        return !it->second.empty();
    }
    return false;
}

// Obtenir le nombre de tuiles restantes
int Pieces::getRemainingTilesCount(char playerLetter) const {
    auto it = playerPieces.find(playerLetter);
    if (it != playerPieces.end()) {
        return it->second.size();
    }
    return 0;
}

// Obtenir le gestionnaire de formes
PiecesShape& Pieces::getShapeManager() {
    return shapeManager;
}

// Trouver une tuile par son nom
bool Pieces::findTile(char playerLetter, const string& tileName, TileInfo& outTile) const {
    auto it = playerPieces.find(playerLetter);
    if (it == playerPieces.end()) {
        return false;
    }

    const auto& tiles = it->second;
    for (const auto& tile : tiles) {
        if (tile.name == tileName) {
            outTile = tile;
            return true;
        }
    }
    return false;
}
