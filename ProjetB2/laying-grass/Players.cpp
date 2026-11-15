#include "Players.hpp"
#include <iostream>
#include <vector>
using namespace std;

Players::Players(string playerName, char starterPieceSymbol, int color) {
    name = playerName;
    starterPiece = starterPieceSymbol;
    colorCode = color;
    exchangeCoupon = true;
    actualPiece = '.';

    //vector<int>availableColors = {1, 2, 3, 4, 5, 6, 8, 9, 12, 13, 14};
//1:blue 2:green 3:aqua 4:red 5:purple 6:yellow 8:gray 9:light blue
//11:light aqua 12 :light red 13:light purple 14:light yellow
}

void Players::setActualPiece(char piece) {
    actualPiece = piece;
}

void Players::useExchangeCoupon() {
    if (exchangeCoupon) {
        exchangeCoupon = false;
        cout << name << " Vous utilisez votre coupon d’échange !" << endl;
    } else {
        cout << name << " Vous n’avez plus de coupon d’échange !" << endl;
    }
}

void Players::displayPlayerInfo(int playerNumber) const {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, colorCode);

    cout << "Joueur "<<playerNumber<<" :"<< name
        // << " | Couleur : " << colorCode
         << " | Coupon : " << (exchangeCoupon ? "1" : "0")
         << " | Piece de depart : " << starterPiece
         //<< " | Piece imposee : " << (actualPiece == '.' ? "aucune" : string(1, actualPiece))
         << endl;

    SetConsoleTextAttribute(hConsole, 7);
}

void Players::resetColor() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, 7);
}
