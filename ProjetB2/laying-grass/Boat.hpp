#pragma once
#include <vector>
#include <string>
#include <set>
#include <optional>

namespace bs {

struct Coordinate {
    int x{0}; // colonne
    int y{0}; // ligne

    bool operator==(const Coordinate& o) const noexcept { return x==o.x && y==o.y; }
    bool operator<(const Coordinate& o)  const noexcept { return (y<o.y) || (y==o.y && x<o.x); }
};

enum class Orientation { Horizontal, Vertical };
enum class ShotResult  { Miss, Hit, Sunk };

struct ShotOutcome {
    ShotResult result{ShotResult::Miss};
    char shipCode{' '};                      // code du bateau touché (si Hit/Sunk)
    std::vector<Coordinate> sunkPositions{}; // rempli quand Sunk
};

/**
 * Classe de base pour tous les bateaux.
 * - Compare la taille via operator<
 * - Déplacement forward/backward (logique déléguée au Board pour la validation espace)
 * - "Jamais touché" = m_hits.empty()
 */
class Boat {
public:
    Boat(std::string name, char code, int length);

    // --- Accès lecture (encapsulation) ---
    const std::string& name()   const noexcept { return m_name; }
    char               code()   const noexcept { return m_code; }
    int                length() const noexcept { return m_length; }
    const Coordinate&  origin() const noexcept { return m_origin; }
    Orientation        orientation() const noexcept { return m_orientation; }
    const std::vector<Coordinate>& positions() const noexcept { return m_positions; }
    const std::set<Coordinate>&    hits()      const noexcept { return m_hits; }

    // --- État de combat ---
    bool occupies(const Coordinate& c) const noexcept;
    void registerHit(const Coordinate& c);      // enregistre un impact si c ∈ positions
    bool isSunk() const noexcept;
    bool neverHit() const noexcept { return m_hits.empty(); }

    // --- Placement / déplacement (modifient la géométrie) ---
    void placeAt(Coordinate origin, Orientation orient);
    // moveBy est protected mais Board y a accès via friend ; il bouge la géométrie
    // en laissant les validations au Board.
    friend class Board;

    // Déplacement : taille du pas (Destroyer = 2, sinon = 1)
    virtual int stepSize() const noexcept { return 1; }

    // Comparaison par taille (longueur)
    friend bool operator<(const Boat& a, const Boat& b) noexcept {
        return a.m_length < b.m_length;
    }

    // Sous-marins : API par défaut (non-submersible). Submarine override.
    virtual bool canDive()           const noexcept { return false; }
    virtual bool isSubmerged()       const noexcept { return false; }
    virtual bool dive()                    { return false; } // retourne true si action acceptée
    virtual void surface()                 {}
    // Tick appelé au début du tour du propriétaire pour gérer la durée de plongée
    virtual void ownerTurnTick()           {}

protected:
    // Déplace la géométrie brute (sans validation)
    void moveBy(int dx, int dy);

protected:
    std::string m_name;
    char        m_code;
    int         m_length;

    Coordinate  m_origin{0,0};
    Orientation m_orientation{Orientation::Horizontal};
    std::vector<Coordinate> m_positions; // cases occupées
    std::set<Coordinate>    m_hits;      // sous-ensemble de positions
};

// --- Sous-classes concrètes ---

class AircraftCarrier : public Boat {
public:
    explicit AircraftCarrier(int length = 5) : Boat("Aircraft Carrier", 'A', length) {}
};

class BattleShip : public Boat {
public:
    explicit BattleShip(int length = 4) : Boat("Battleship", 'B', length) {}
};

class Cruiser : public Boat {
public:
    explicit Cruiser(int length = 3) : Boat("Cruiser", 'C', length) {}
};

class Submarine : public Boat {
public:
    explicit Submarine(int length = 3) : Boat("Submarine", 'S', length) {}

    // Submersible
    bool canDive()     const noexcept override { return true; }
    bool isSubmerged() const noexcept override { return m_submerged; }
    bool dive()              override;   // plonge 1 tour max ; retourne true si accepté
    void surface()           override;   // ressort
    void ownerTurnTick()     override;   // gestion durée max 1 tour

private:
    bool m_submerged{false};
    int  m_submergeTurnsLeft{0}; // max 1 ; décrémenté au début du tour du propriétaire
};

class Destroyer : public Boat {
public:
    explicit Destroyer(int length = 2) : Boat("Destroyer", 'D', length) {}
    int stepSize() const noexcept override { return 2; } // se déplace de 2 cases
};

} // namespace bs
