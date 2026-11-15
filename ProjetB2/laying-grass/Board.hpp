#pragma once
#include <memory>
#include <vector>
#include <iostream>
#include <string>

typedef std::vector<std::vector<char>> Shape;
using namespace std;

class Players;
class Pieces;
struct Piece;

class Board {

private:

    int boardSize;

    vector<vector<char>>board;

    char emptySymbol;

    bool isValidPosition(int r, int c) const;

    bool isNearBonus(int r, int c) const;

    void placeBonus(char symbol, int count);

public:

    Board(int nbPlayers, char emptySymbol = '.');

    void displayBoard();

    void placeSpecialTiles(int nbPlayers);

    bool isEmpty(int x, int y) const;

    void placeTile(int x, int y, char piece);

    bool placeTileOnBoard(int x, int y, const vector<vector<char>>& shape, char playerLetter);

    int getSize() const { return boardSize; }

    void startGame(vector<Players>& players, int totalRounds);

    bool placerTuile(int x, int y, const Shape& tuile, char lettreJoueur);

    void afficherTuileColor(const Shape& tuile, char lettreJoueur, int colorCode) const;


};
