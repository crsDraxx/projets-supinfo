#pragma once
#include "Boat.hpp"
#include <memory>
#include <iostream>

namespace bs {

/**
 * Board : g�re la flotte d�un joueur, les tir re�us, le suivi, et MAINTENANT :
 * - d�placement forward/backward (validation bord/chevauchements)
 * - sous-marins submerg�s intouchables
 * - tick d�but de tour (ownerTurnTick) pour g�rer la remont�e auto des sous-marins
 */
class Board {
public:
    explicit Board(int size = 10, bool interactive = true); // demande les placements au joueur

    int size() const noexcept { return m_size; }

    // Tick de d�but de tour (propri�taire)
    void startOfOwnerTurnTick();

    // Tir re�u -> calcule ShotOutcome (ignore les sous-marins plong�s)
    ShotOutcome receiveShot(const Coordinate& c);

    // Affichages console
    void printOwn() const;        // grille propri�taire (A/B/C/S/D ; minuscule si touch� ; 'o' si tir � l�eau subi)
    void printTracking() const;   // grille de suivi (o = manqu�, x = touch�, X = coul�)

    // Suivi (cot� attaquant)
    void recordMiss(const Coordinate& c);
    void recordHit(const Coordinate& c);
    void recordSunk(const std::vector<Coordinate>& coords);

    // D�placements (s�lection par code du bateau, F = forward, B = backward)
    // Retourne true si le mouvement a �t� effectu�.
    bool moveForward(char shipCode);
    bool moveBackward(char shipCode);

    // Choix de plong�e/surface (true si action effectu�e)
    bool diveSubmarine(char shipCode);
    bool surfaceSubmarine(char shipCode);

    // State
    bool allSunk() const;

private:
    int m_size{10};
    std::vector<std::unique_ptr<Boat>> m_fleet;

    // Tirs adverses re�us � l�eau (pour affichage 'o' dans printOwn)
    std::set<Coordinate> m_waterHits;

    // Plateau de suivi (pour affichage tracking)
    std::set<Coordinate> m_trackingMiss;
    std::set<Coordinate> m_trackingHit;
    std::set<Coordinate> m_trackingSunk;

private:
    // Placement initial
    void askAndPlaceFleet();
    void randomPlaceFleet();

    // Recherche utilitaire
    Boat*       findBoatByCode(char code);
    const Boat* findBoatByCode(char code) const;

    // Validation placement/mouvement
    bool canPlace(const Boat& b) const;
    bool overlapWithAny(const Boat& b, const Boat* ignore = nullptr) const;
    bool canTranslate(const Boat& b, int dx, int dy) const;

    // I/O helpers
    static Orientation askOrientation();
    static Coordinate  askCoordinate(int boardSize, const std::string& prompt);

    // Affichage helpers
    char cellForOwn(int x, int y) const;
    char cellForTracking(int x, int y) const;
};

} // namespace bs
