# Vincent MOUCADEAU 1A TP3

import os
import time
from random import randint

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

pieces = ["r","n","b","q","k","b","n","r"]

clearConsole()

def create_and_initialise_matrix(lon, lar, val):
    """
    require: lon, lar, val are not null integers
    ensure: return a rows * column list which represent a matrix
    """

    return [[val for i in range(lon)] for i in range(lar)]


def create_game_board():
    """
    Permet de créer un plateau de jeu (matrice 8x8)
    require: nothing
    ensure: return a correct game board
    """
    return create_and_initialise_matrix(8,8, ' ')

"""
def initialise_game_board():
    board = create_game_board()
    for i in range(8):
        board[1][i] = "P" + str(i) + "_N"
        board[6][i] = "P" + str(i) + "_B"
        board[0][i] = pieces[i] + "_N"
        board[7][i] = pieces[i] + "_B"
    
    return board
"""

def initialise_game_board():
    board = create_game_board()
    for i in range(8):
        board[1][i] = "p"
        board[6][i] = "P"
        board[0][i] = pieces[i]
        board[7][i] = pieces[i].upper()
    
    return board


# Exemple of fen string : "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
def initialise_game_board_from_fen(fen_string):
    board = create_game_board()
    fenboard = fen_string.split(' ')[0] # on récupère les positions des pièces de la chaine FEN
    pos_x, pos_y = (0, 0)
    for i in fenboard:
        if i == "/":
            pos_x = 0
            pos_y += 1
        else:
            if i.isdigit():
                pos_x += int(i)
            else:
                board[pos_y][pos_x] = i
                pos_x += 1
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
    
    """
    row = 8
    for i in board:
        print("+---+---+---+---+---+---+---+---+")
        line = "| "
        for k in i:
            line += k + " | "
        print(line + str(row))
        row -= 1
    print("+---+---+---+---+---+---+---+---+")
    print("  a   b   c   d   e   f   g   h  ")
    

game_board = initialise_game_board_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

def is_in_matrix(matrix, x, y):
    """
    Vérifie si des coordonnées sont dans une matrice
    require: matrix (list), x, y (integers)
    ensure: return True if the coordinates are in the matrice, False otherwise
    return: boolean
    """
    return len(matrix[0]) > x and len(matrix) > y

def get_piece_coordinates(piece_name):
    x, y = (-1,-1) # the piece is not on the board at this point
    for i in range(len(game_board)):
        for k in range(len(game_board[i])):
            if game_board[i][k] == piece_name:
                x, y = (k, i)
    return (x,y)

def is_a_piece(piece_name):
    is_a_piece = get_piece_coordinates(piece_name) != (-1,-1)
    return is_a_piece



def force_integer_input(text):
    """
    Demande à l'utilisateur d'entrer un nombre entier pour éviter les erreurs
    require: input text
    ensure: force the user to enter a correct integer
    return: an integer !!!
    """
    var = input(text)
    while isinstance(var, str): # Tant que var est un string
        try:
            var = int(var)
        except:
            print("Vous devez entrer un nombre entier.")
            var = input(text)

    return var

def enter_position(board):
    """
    Demande à l'utilisateur d'entrer des coordonnées appartenant au plateau
    require: board (list)
    ensure: force the user to enter correct coordinates (integers)
    return: tuple (x, y) => coordinates
    """
    piece = input("Entrez le nom de la pièce à bouger : ")
    pos_x = force_integer_input("Entrez une coordonnée en x : ")
    pos_y = force_integer_input("Entrez une coordonnée en y : ")
    while not is_in_matrix(board, pos_x, pos_y):
        print("Ces coordonnées n'existent pas sur le plateau.")
        pos_x = force_integer_input("Entrez une coordonnée en x : ")
        pos_y = force_integer_input("Entrez une coordonnée en y : ")
    while not is_a_piece(piece):
        print("Cette pièce n'existe pas sur le plateau.")
        piece = input("Entrez le nom de la pièce à bouger : ")
    return (piece, pos_x, pos_y)

def is_someone_on_the_path(start_pos, end_pos):
    result = False
    start_x, start_y = start_pos[0], start_pos[1]
    end_x, end_y = end_pos[0], end_pos[1]
    if abs(end_y - start_y) == abs(end_x - start_x): # on se déplace en diagonale (les problèmes)
        for i in range((end_y - start_y)):
            if start_x < end_x:
                if start_y < end_y:
                    if game_board[start_y+i][start_x+i] != ' ':
                        result = True
                else:
                    if game_board[start_y-i][start_x+i] != ' ':
                        result = True
            else:
                if start_y < end_y:
                    if game_board[start_y+i][start_x-i] != ' ':
                        result = True
                else:
                    if game_board[start_y-i][start_x-i] != ' ':
                        result = True
    elif start_x == end_x: # on se déplace verticalement
        for i in range(abs(end_y-start_y)):
            if start_y < end_y:
                if game_board[start_y+i][start_x] != ' ':
                    result = True
            else:
                if game_board[start_y-i][start_x] != ' ':
                    result = True
    elif start_y == end_y: # on se déplace horizontalement
        for i in range(abs(end_x-start_x)):
            if start_x < end_x:
                if game_board[start_y][start_x+i] != ' ':
                    result = True
            else:
                if game_board[start_y][start_x-i] != ' ':
                    result = True  
    else:
        result = False
    return result

#print(is_someone_on_the_path((4,5), (0,1)))

def is_position_valid(piece_name, start_pos, end_pos):
    position_valid = True
    start_x, start_y = start_pos[0], start_pos[1]
    end_x, end_y = end_pos[0], end_pos[1]
    piece_target = game_board[end_y][end_x]
    # PION
    if piece_name == "p" or piece_name == "P": 
        if start_x == end_x:
            if piece_target != ' ':    
                distance = end_y - start_y if piece_name == "p" else start_y - end_y
                if distance == 2 and start_y != 1:
                    position_valid = False
                elif distance == 1:
                    position_valid = True
                else:
                    position_valid = False
            else:
                position_valid = False
    
    
    return position_valid


def move_piece(piece_name, end_x, end_y):
    piece_coord = get_piece_coordinates(piece_name)
    piece_target = (end_x,end_y)
    piece_moved = False
    if is_position_valid(piece_name, piece_coord, piece_target):
        game_board[piece_coord[1]][piece_coord[0]] = ' '
        game_board[end_y][end_x] = piece_name
        piece_moved = True
    return piece_moved


#to_move = enter_position(game_board)


#to_move = ('P0_B', 0, 1)

#print(move_piece(to_move[0], to_move[1], to_move[2]))
#print_game_board(game_board)
