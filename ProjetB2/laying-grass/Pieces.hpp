#pragma once
#include <iostream>
#include <memory>
#include <string>
#include <map>
#include <windows.h>
#include <vector>
#include "PiecesShape.hpp"

class Pieces {
private:
    PiecesShape shapeManager;
    // Pour chaque joueur (identifié par sa lettre minuscule), stocke les tuiles disponibles
    map<char, vector<TileInfo>> playerPieces;

public:
    // Constructeur
    Pieces();

    // Initialiser les pièces pour un joueur
    void initPlayerPieces(char playerLetter);

    // Obtenir les tuiles disponibles pour un joueur
    vector<TileInfo> getPlayerTiles(char playerLetter) const;

    // Retirer une tuile après utilisation
    bool removeTile(char playerLetter, const string& tileName);

    // Vérifier si un joueur a encore des tuiles
    bool hasRemainingTiles(char playerLetter) const;

    // Obtenir le nombre de tuiles restantes
    int getRemainingTilesCount(char playerLetter) const;

    // Obtenir le gestionnaire de formes (pour rotate/flip/display)
    PiecesShape& getShapeManager();

    // Trouver une tuile par son nom
    bool findTile(char playerLetter, const string& tileName, TileInfo& outTile) const;
};
