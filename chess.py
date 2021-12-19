# Vincent MOUCADEAU 1A TP3

import os
import time
from random import randint
import pygame  


clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

"""
PIECES :
p : pawn
r : rook (tour)
n : knight (cavalier)
b : bishop (fou)
q : queen (dame)
k : king (roi)

En minuscule : pièce noire
En majuscule : pièce blanche

Ce système de notation permet d'utiliser le FEN pour charger n'importe quelle position dans le programme (voir initialise_game_board_from_fen)
Plus d'informations : https://www.chess.com/terms/fen-chess
"""



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
    pieces = ["r","n","b","q","k","b","n","r"]
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
    

def is_in_matrix(matrix, x, y):
    """
    Vérifie si des coordonnées sont dans une matrice
    require: matrix (list), x, y (integers)
    ensure: return True if the coordinates are in the matrice, False otherwise
    return: boolean
    """
    return len(matrix[0]) > x and len(matrix) > y

def get_piece_coordinates(board, piece_name):
    x, y = (-1,-1) # the piece is not on the board at this point
    for i in range(len(board)):
        for k in range(len(board[i])):
            if board[i][k] == piece_name:
                x, y = (k, i)
    return (x,y)

def is_a_piece(board, piece_name):
    is_a_piece = get_piece_coordinates(board, piece_name) != (-1,-1)
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




def is_someone_on_the_path(board, start_pos, end_pos):
    result = False
    start_x, start_y = start_pos[0], start_pos[1]
    end_x, end_y = end_pos[0], end_pos[1]
    if abs(end_y - start_y) == abs(end_x - start_x): # on se déplace en diagonale (les problèmes)
        for i in range(1,abs(end_y - start_y)):
            if start_x < end_x:
                if start_y < end_y:
                    if board[start_y+i][start_x+i] != ' ':
                        result = True
                else:
                    if board[start_y-i][start_x+i] != ' ':
                        result = True
            else:
                if start_y < end_y:
                    if board[start_y+i][start_x-i] != ' ':
                        result = True
                else:
                    if board[start_y-i][start_x-i] != ' ':
                        result = True
    elif start_x == end_x: # on se déplace verticalement
        for i in range(1,abs(end_y-start_y)):
            if start_y < end_y:
                if board[start_y+i][start_x] != ' ':
                    result = True
            else:
                if board[start_y-i][start_x] != ' ':
                    result = True
    elif start_y == end_y: # on se déplace horizontalement
        for i in range(1,abs(end_x-start_x)):
            if start_x < end_x:
                if board[start_y][start_x+i] != ' ':
                    result = True
            else:
                if board[start_y][start_x-i] != ' ':
                    result = True  
    else:
        result = False
    return result


def is_position_valid(board, piece_name, start_pos, end_pos):

    position_valid = False
    start_x, start_y = start_pos[0], start_pos[1]
    end_x, end_y = end_pos[0], end_pos[1]
    piece_target = board[end_y][end_x]

    diag_move = abs(end_y - start_y) == abs(end_x - start_x)
    vert_move = start_y == end_y
    hor_move = start_x == end_x

    # Vérification préliminaire
    if piece_target == ' ' or piece_target.isupper() != piece_name.isupper():
        # CAVALIER
        if piece_name in ('N', 'n'):
            dir_offset = [(-1,-2), (1,-2), (2,-1), (2,1), (1,2), (-1,2), (-2,1), (-2,-1)]
            for x, y in dir_offset:
                if start_x + x == end_x and start_y + y == end_y:
                    position_valid = True


        # Vérification de la présence d'une pièce sur la trajectoire
        if not is_someone_on_the_path(board, start_pos, end_pos):
            # PION
            if piece_name in ('P', 'p'):
                if hor_move:
                    if piece_target == ' ':    
                        distance = end_y - start_y if piece_name == "p" else start_y - end_y
                        if distance == 2 and (start_y == 1 or start_y == 6):
                            position_valid = True
                        elif distance == 1:
                            position_valid = True
                        else:
                            position_valid = False
                elif end_x == start_x + 1 or end_x == start_x - 1:
                    if piece_name == "p":
                        if end_y == start_y + 1:
                            if piece_target != ' ' and piece_target.isupper():
                                position_valid = True
                    else:
                        if end_y == start_y - 1:
                            if piece_target != ' ' and piece_target.islower():
                                position_valid = True
            # FOU
            if piece_name in ("B", "b"):
                if diag_move:
                    position_valid = True

            # TOUR
            if piece_name in ("R", "r"):
                if hor_move or vert_move:
                    position_valid = True
            
            # DAME
            if piece_name in ("Q", "q"):
                if diag_move or hor_move or vert_move:
                    position_valid = True 

            # ROI
            if piece_name in ("K", "k"):
                if abs(end_y - start_y) <= 1 and abs(end_x - start_x) <= 1: # si on se déplace d'une case dans toutes les directions
                    position_valid = True

    return position_valid

""" USELESS WITH USER INTERFACE
def move_piece(board, piece_name, end_x, end_y):
    piece_coord = get_piece_coordinates(piece_name)
    piece_target = (end_x,end_y)
    piece_moved = False
    if is_position_valid(piece_name, piece_coord, piece_target):
        board[piece_coord[1]][piece_coord[0]] = ' '
        board[end_y][end_x] = piece_name
        piece_moved = True
    return piece_moved
"""

# User Interface
scr = pygame.display.set_mode((640,640))  
UI_board = create_and_initialise_matrix(8,8,' ') # Create a matrix for the UI game board

def UI_makeboard(screen):
    white_color = (240,217,181)
    brown_color = (181,136,99)  
    for k in range(8):
        for i in range(8):
            pygame.draw.rect(screen, white_color if (i+k) % 2 == 0 else brown_color, pygame.Rect(80*i, 80*k, 80, 80)) 
 
def UI_drawpiece(board, piece_name, pos_x, pos_y):
    img_path = "pieces/b" + piece_name + ".png" if piece_name.islower() else "pieces/w" + piece_name.lower() + ".png"
    piece = pygame.image.load(img_path).convert_alpha()
    piece = pygame.transform.scale(piece,(80,80))
    board[pos_y][pos_x] = piece

def UI_drawboard_from_matrice(UI_board, game_board):
    for y in range(8):
        for x in range(8):
            if game_board[y][x] != ' ':
                piece_name = game_board[y][x]
                UI_drawpiece(UI_board, piece_name, x, y)

def UI_get_legal_moves(board, piece_x, piece_y):
    legal_moves_coord = []
    for y in range(8):
        for x in range(8):
            if is_position_valid(board, board[piece_y][piece_x], (piece_x, piece_y), (x, y)):
                legal_moves_coord += [(x, y)]
    return legal_moves_coord


clock = pygame.time.Clock()

def UI_Init(screen, UI_board, game_board):
    pygame.init()  
    done = False  
    piece_draging = False
    last_move = False # [start_pos, end_pos]
    legal_moves = None
    tour = True # True = blanc, False = noir
    
    while not done:  
        UI_makeboard(screen)
        if last_move:
            start_x, start_y = last_move[0]
            end_x, end_y = last_move[1]
            yellow_color = (247,236,91)
            hint = pygame.Surface((80,80))
            hint.set_alpha(100)
            hint.fill(yellow_color)
            scr.blit(hint, [80*start_x, 80*start_y])
            scr.blit(hint, [80*end_x, 80*end_y])
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                done = True 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                sq_x, sq_y = (int(8*(mouse_x/640)), int(8*(mouse_y/640)))
                
                if game_board[sq_y][sq_x] != ' ': # Si il y a une pièce sur la case
                    if tour and game_board[sq_y][sq_x].isupper() or not tour and game_board[sq_y][sq_x].islower():
                        piece_draging = [sq_x, sq_y, UI_board[sq_y][sq_x], game_board[sq_y][sq_x]] # On stocke les coordonnées de la pièce, son nom et sa "surface" pour la déplacer
                        UI_board[sq_y][sq_x] = ' ' # On enlève la pièce de l'UI
                        
                    

            if event.type == pygame.MOUSEBUTTONUP:
                if piece_draging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    sq_x, sq_y = (int(8*(mouse_x/640)), int(8*(mouse_y/640)))
                    if legal_moves == None:
                        legal_moves = UI_get_legal_moves(game_board, piece_draging[0], piece_draging[1])
                    if (sq_x, sq_y) in legal_moves: # Si la case sélectionnée est une case valide
                        # Play sound
                        if UI_board[sq_y][sq_x] != ' ': # If there is a piece here
                            pygame.mixer.music.load('audio/take.mp3')
                        else:
                            pygame.mixer.music.load('audio/move.mp3')
                        pygame.mixer.music.play()
                        
                        # On place la pièce sur la case sélectionnée
                        UI_board[sq_y][sq_x] = piece_draging[2] 
                        # On met à jour le plateau de jeu (matrice)
                        game_board[sq_y][sq_x] = piece_draging[3]
                        game_board[piece_draging[1]][piece_draging[0]] = ' '
                        last_move = [(piece_draging[0], piece_draging[1]), (sq_x, sq_y)]
                        tour = not tour # On change de joueur
                    else:
                        # On replace la pièce dans sa case d'origine
                        UI_board[piece_draging[1]][piece_draging[0]] = piece_draging[2] 
                    
                    piece_draging = False # On arrête de déplacer la pièce
                    legal_moves = None # On vide les legal moves
        
        if piece_draging:
            # On affiche les cases valides
            if legal_moves == None:
                legal_moves = UI_get_legal_moves(game_board, sq_x, sq_y)
            for square in legal_moves:
                green_color = (0,255,0)
                hint = pygame.Surface((80,80))
                hint.set_alpha(50)
                hint.fill(green_color)
                scr.blit(hint, [80*square[0], 80*square[1]])

        # On affiche les pièces sur le plateau
        for y in range(8):
            for x in range(8):
                if UI_board[y][x] != ' ':
                    screen.blit(UI_board[y][x],[80*x,80*y])

        # Si on déplace une pièce
        if piece_draging:
            mouse_x, mouse_y = pygame.mouse.get_pos()  
            # On positionne le centre de la pièce sur la souris
            piece = piece_draging[2]
            scr.blit(piece,[mouse_x-40,mouse_y-40])
            
        
        pygame.display.flip() # Uptdate the screen
        clock.tick(75) # 75 FPS limit

game_board = initialise_game_board_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
UI_drawboard_from_matrice(UI_board, game_board)
UI_Init(scr, UI_board, game_board)
