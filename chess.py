# Vincent MOUCADEAU 1A TP3

import os
import time
from random import randint

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

pieces = ["T1","C1","F1","RE","RO","F2","C2","T2"]

 
def create_and_initialise_matrix(lon, lar, val):
    """
    require: lon, lar, val are not null integers
    ensure: return a rows * column list which represent a matrix
    """

    return [[val for i in range(lon)] for i in range(lar)]


def create_game_board():
    """
    Permet de créer un plateau de jeu (matrice 9x9) (pour mettre les coordonnées)
    require: nothing
    ensure: return a correct game board
    """
    return create_and_initialise_matrix(8,8, ' ')
    
def initialise_game_board():
    board = create_game_board()
    # initialise black pawns
    for i in range(8):
        board[1][i] = "P" + str(i) + "_N"
        board[6][i] = "P" + str(i) + "_B"
        board[0][i] = pieces[i] + "_N"
        board[7][i] = pieces[i] + "_B"
    
    return board


def print_matrix(matrix):
    """
    Permet d'afficher une matrice ligne par ligne dans la console
    require: matrix (list)
    ensure: print a beautiful matrix in the console
    """
    for i in matrix:
        print(i)



def print_game_board(board):
    """
    Permet d'afficher un beau plateau de jeu dans la console
    require: board (list)
    ensure: print a beautiful board in the console
    
    PREVIOUS VERSION (bataille navale):
    for i in board:
        print("-----------------------------------------")
        line = "| "
        for k in i:
            line += k + " | "
        print(line)
    print("-----------------------------------------")
    """
    print_matrix(board)