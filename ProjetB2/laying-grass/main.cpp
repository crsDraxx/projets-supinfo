#include <iostream>
#include "Board.hpp"
#include "Players.hpp"
#include <vector>
#include <algorithm>
#include <windows.h>

using namespace std;

int main()
{
    string answer;
    int nbPlayers;

    cout << "Bienvenue dans LAYING GRASS!\n" << endl;

    cout << "Voulez-vous jouer? (oui/non)\n";
    cin >> answer;

    if (answer == "oui") {
        cout <<"\nCombien de joueurs etes-vous? (2 à 9)\n";
        cin >> nbPlayers;
        cin.ignore();

        //collect players informations
        vector<Players>players;
        vector<int>availableColors = {1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14};

        for (int i = 0; i < nbPlayers; ++i){
            string name;
            int color;

            cout<<"\nQuel est le nom du joueur "<< i+1<<" ?\n";
            getline(cin,name);

            cout<<"\nChoisissez votre couleur: \n";

            for (auto color: availableColors){
                //show the color of every index color
                HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
                SetConsoleTextAttribute(hConsole, color);
                cout << color << " ";
                SetConsoleTextAttribute(hConsole, 7);
            }
            cout<<"\n";
            cin>>color;
            cin.ignore();

            //check if the color is available if not redo the player
            auto isColorAvailable = find(availableColors.begin(), availableColors.end(), color);
            if (isColorAvailable == availableColors.end()) {
                cout << "Couleur invalide !\n";
                --i;
                continue;
            }
        availableColors.erase(isColorAvailable);

        // Starter symbol
        char starterPiece = '1' + i;
        players.emplace_back(name, starterPiece, color);
        }
        cout <<"\n RECAPITULATIF DES JOUEURS\n";
       // for (const auto& p: players ){
         //       p.displayPlayerInfo(i);
         for (int i = 0; i < nbPlayers; ++i){
            players[i].displayPlayerInfo(i+1);
         }


        //display board


        //display tiles
        Board board(nbPlayers);
        board.placeSpecialTiles(nbPlayers);
        board.startGame(players, 10);
        board.displayBoard();





    }

    else if (answer == "non") {
        cout << "OK Bonne continuation!"<< endl;
    }
    else{
        cout << "Je n'ai pas compris votre réponse!"<<endl;
    }


    return 0;
}
