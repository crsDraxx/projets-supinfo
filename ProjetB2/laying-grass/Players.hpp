#pragma once
#include <iostream>
#include <memory>
#include <windows.h>
#include <vector>

using namespace std;
class Players {
private:
    std::string name;
    char starterPiece;
    int colorCode;
    bool exchangeCoupon;
    char actualPiece;
public:
    Players(std::string playerName, char starterPieceSymbol, int color);
    // getters
    std::string getName() const { return name; }
    char getStarterPiece() const { return starterPiece; }
    int getColorCode() const { return colorCode; }
    void displayPlayerInfo(int playerNumber) const;
    void resetColor();
    void useExchangeCoupon();
    void setActualPiece(char piece);
};
