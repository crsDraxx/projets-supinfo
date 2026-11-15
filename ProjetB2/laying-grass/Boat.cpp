#include "Board.hpp"
#include <algorithm>
#include <cctype>
#include <limits>
#include <random>

namespace bs {

Board::Board(int size, bool interactive) : m_size(size) {
    if (interactive) askAndPlaceFleet();
    else             randomPlaceFleet();
}

void Board::randomPlaceFleet() {
    // même flotte que askAndPlaceFleet, mais placements aléatoires
    std::vector<std::unique_ptr<Boat>> templates;
    templates.emplace_back(std::make_unique<AircraftCarrier>(5));
    templates.emplace_back(std::make_unique<BattleShip>(4));
    templates.emplace_back(std::make_unique<Cruiser>(3));
    templates.emplace_back(std::make_unique<Submarine>(3));
    templates.emplace_back(std::make_unique<Destroyer>(2));

    std::mt19937 rng{std::random_device{}()};
    std::uniform_int_distribution<int> coin(0,1);
    std::uniform_int_distribution<int> pos(0, m_size-1);

    for (auto& t : templates) {
        while (true) {
            Orientation o = coin(rng) ? Orientation::Horizontal : Orientation::Vertical;
            Coordinate origin{pos(rng), pos(rng)};

            std::unique_ptr<Boat> b;
            switch (t->code()) {
                case 'A': b = std::make_unique<AircraftCarrier>(t->length()); break;
                case 'B': b = std::make_unique<BattleShip>(t->length());     break;
                case 'C': b = std::make_unique<Cruiser>(t->length());        break;
                case 'S': b = std::make_unique<Submarine>(t->length());      break;
                case 'D': b = std::make_unique<Destroyer>(t->length());      break;
            }
            b->placeAt(origin, o);
            if (!canPlace(*b)) continue;

            m_fleet.push_back(std::move(b));
            break;
        }
    }
}


void Board::startOfOwnerTurnTick() {
    // Chaque début de tour du propriétaire : tick sur tous les bateaux
    for (auto& b : m_fleet) b->ownerTurnTick();
}

bool Board::allSunk() const {
    return std::all_of(m_fleet.begin(), m_fleet.end(),
        [](const std::unique_ptr<Boat>& b){ return b->isSunk(); });
}

ShotOutcome Board::receiveShot(const Coordinate& c) {
    ShotOutcome out{};
    // Parcours des bateaux pour voir si l’un est à cette position
    for (auto& b : m_fleet) {
        // Sous-marin plongé : intouchable → compter comme Miss
        if (b->code()=='S' && b->isSubmerged()) continue;

        if (b->occupies(c)) {
            b->registerHit(c);
            if (b->isSunk()) {
                out.result = ShotResult::Sunk;
                out.shipCode = b->code();
                out.sunkPositions = b->positions();
            } else {
                out.result = ShotResult::Hit;
                out.shipCode = b->code();
            }
            return out;
        }
    }
    // à l’eau
    out.result = ShotResult::Miss;
    m_waterHits.insert(c);
    return out;
}

void Board::recordMiss(const Coordinate& c) { m_trackingMiss.insert(c); }
void Board::recordHit(const Coordinate& c)  { m_trackingHit.insert(c);  }
void Board::recordSunk(const std::vector<Coordinate>& coords) {
    for (auto& c : coords) m_trackingSunk.insert(c);
}

// ----------------------------
// Déplacements & plongée
// ----------------------------
Boat* Board::findBoatByCode(char code) {
    for (auto& b : m_fleet) if (b->code()==code) return b.get();
    return nullptr;
}
const Boat* Board::findBoatByCode(char code) const {
    for (auto& b : m_fleet) if (b->code()==code) return b.get();
    return nullptr;
}

bool Board::canTranslate(const Boat& b, int dx, int dy) const {
    // Simule la translation et vérifie bornes + chevauchement
    for (auto p : b.positions()) {
        p.x += dx; p.y += dy;
        if (p.x < 0 || p.y < 0 || p.x >= m_size || p.y >= m_size) return false;
        // collision avec autres bateaux (ignorer soi-même)
        for (const auto& other : m_fleet) {
            if (other.get() == &b) continue;
            if (other->occupies(p)) return false;
        }
    }
    return true;
}

bool Board::moveForward(char shipCode) {
    Boat* b = findBoatByCode(shipCode);
    if (!b) return false;
    if (!b->neverHit()) return false; // ne peut bouger que s'il n'a jamais été touché

    int step = b->stepSize();
    int dx=0, dy=0;
    if (b->orientation()==Orientation::Horizontal) dx = step;
    else dy = step;

    if (!canTranslate(*b, dx, dy)) return false;
    b->moveBy(dx, dy);
    return true;
}

bool Board::moveBackward(char shipCode) {
    Boat* b = findBoatByCode(shipCode);
    if (!b) return false;
    if (!b->neverHit()) return false;

    int step = b->stepSize();
    int dx=0, dy=0;
    if (b->orientation()==Orientation::Horizontal) dx = -step;
    else dy = -step;

    if (!canTranslate(*b, dx, dy)) return false;
    b->moveBy(dx, dy);
    return true;
}

bool Board::diveSubmarine(char shipCode) {
    Boat* b = findBoatByCode(shipCode);
    if (!b) return false;
    if (b->code()!='S') return false;
    return b->dive();          // true si action acceptée
}

bool Board::surfaceSubmarine(char shipCode) {
    Boat* b = findBoatByCode(shipCode);
    if (!b) return false;
    if (b->code()!='S') return false;
    b->surface();
    return true;
}

// ----------------------------
// Placement interactif
// ----------------------------
void Board::askAndPlaceFleet() {
    // Flotte par défaut
    std::vector<std::unique_ptr<Boat>> templates;
    templates.emplace_back(std::make_unique<AircraftCarrier>(5));
    templates.emplace_back(std::make_unique<BattleShip>(4));
    templates.emplace_back(std::make_unique<Cruiser>(3));
    templates.emplace_back(std::make_unique<Submarine>(3));
    templates.emplace_back(std::make_unique<Destroyer>(2));

    std::cout << "\n=== Place your fleet on a " << m_size << "x" << m_size << " board ===\n";
    for (auto& t : templates) {
        while (true) {
            std::cout << "\nPlacing " << t->name() << " [" << t->code()
                      << "] (length=" << t->length() << ")\n";
            Orientation o = askOrientation();
            Coordinate origin = askCoordinate(m_size, "Origin (x y)");

            std::unique_ptr<Boat> b;
            switch (t->code()) {
                case 'A': b = std::make_unique<AircraftCarrier>(t->length()); break;
                case 'B': b = std::make_unique<BattleShip>(t->length());     break;
                case 'C': b = std::make_unique<Cruiser>(t->length());        break;
                case 'S': b = std::make_unique<Submarine>(t->length());      break;
                case 'D': b = std::make_unique<Destroyer>(t->length());      break;
            }
            b->placeAt(origin, o);

            if (!canPlace(*b)) {
                std::cout << "Invalid placement (out of bounds or overlaps). Try again.\n";
                continue;
            }
            m_fleet.push_back(std::move(b));
            printOwn();
            break;
        }
    }
    std::cout << "All boats placed!\n";
}

bool Board::canPlace(const Boat& b) const {
    for (auto& p : b.positions()) {
        if (p.x < 0 || p.y < 0 || p.x >= m_size || p.y >= m_size) return false;
    }
    if (overlapWithAny(b)) return false;
    return true;
}

bool Board::overlapWithAny(const Boat& b, const Boat* ignore) const {
    for (const auto& existing : m_fleet) {
        if (ignore && existing.get()==ignore) continue;
        for (const auto& p : b.positions()) {
            if (existing->occupies(p)) return true;
        }
    }
    return false;
}

// ----------------------------
// I/O helpers
// ----------------------------
Orientation Board::askOrientation() {
    while (true) {
        std::cout << "Orientation (H=horizontal / V=vertical): ";
        std::string s; std::cin >> s;
        if (!s.empty()) {
            char c = static_cast<char>(std::toupper(s[0]));
            if (c=='H') return Orientation::Horizontal;
            if (c=='V') return Orientation::Vertical;
        }
        std::cout << "Invalid input. ";
    }
}

Coordinate Board::askCoordinate(int boardSize, const std::string& prompt) {
    while (true) {
        std::cout << prompt << " (0.." << boardSize-1 << "): ";
        int x,y;
        if (std::cin >> x >> y) {
            if (x>=0 && y>=0 && x<boardSize && y<boardSize) return {x,y};
        }
        std::cout << "Invalid coordinate.\n";
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
}

// ----------------------------
// Affichage
// ----------------------------
char Board::cellForOwn(int x, int y) const {
    Coordinate c{x,y};
    // tir à l'eau subi ?
    if (m_waterHits.count(c)) return 'o';

    // bateau ?
    for (const auto& b : m_fleet) {
        if (b->occupies(c)) {
            bool hit = b->hits().count(c) > 0;
            char code = b->code();
            if (hit) code = static_cast<char>(std::tolower(code));
            return code;
        }
    }
    return '.';
}

char Board::cellForTracking(int x, int y) const {
    Coordinate c{x,y};
    if (m_trackingSunk.count(c)) return 'X';
    if (m_trackingHit.count(c))  return 'x';
    if (m_trackingMiss.count(c)) return 'o';
    return '.';
}

void Board::printOwn() const {
    std::cout << "\nYour board (own view):\n   ";
    for (int x=0;x<m_size;++x) std::cout << x%10;
    std::cout << "\n";
    for (int y=0;y<m_size;++y) {
        std::cout << (y%10) << ": ";
        for (int x=0;x<m_size;++x) std::cout << cellForOwn(x,y);
        std::cout << "\n";
    }
}

void Board::printTracking() const {
    std::cout << "\nOpponent board (tracking):\n   ";
    for (int x=0;x<m_size;++x) std::cout << x%10;
    std::cout << "\n";
    for (int y=0;y<m_size;++y) {
        std::cout << (y%10) << ": ";
        for (int x=0;x<m_size;++x) std::cout << cellForTracking(x,y);
        std::cout << "\n";
    }
}

} // namespace bs
