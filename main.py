import pygame
import random

# setting up
pygame.init()
clock = pygame.time.Clock()
main = pygame.display.set_mode((800,800))
font = pygame.font.SysFont(None, 120)
subfont = pygame.font.SysFont(None, 45)
pygame.display.set_caption("Gomoku")

#margin
BOARD_X = 100
BOARD_Y = 100



class Board:

    def __init__(self):
        self.SIZE = 15
        self.CELL_SIZE = 40
        self.grid = [[""] * self.SIZE for _ in range(self.SIZE)]
    
    def reset(self):
        self.grid = [[""] * self.SIZE for _ in range(self.SIZE)]
    
    def get_cell(self, mouse_pos):
        x,y = mouse_pos
        x -= 100
        y -= 100
        
        col = x // self.CELL_SIZE
        row = y // self.CELL_SIZE

        return row,col




class Game:
    PLAYER_1 = "X"
    PLAYER_2 = "O"
    
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.winner = None
        self.game_over = False
    
    def switchPlayer(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    def restart(self):
        self.board.reset()
        self.winner = None
        self.game_over = False
        self.current_player = 1
    
    def playMove(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            r, c = self.board.get_cell(event.pos)

            if self.board.grid[r][c] == "":

                if self.current_player == 1:
                    self.board.grid[r][c] = self.PLAYER_1
                else:
                    self.board.grid[r][c] = self.PLAYER_2

                self.switchPlayer()


class DrawPiece:

    def __init__(self, game):
        self.game = game
        self.pieceX = pygame.image.load("X.png")
        self.pieceO = pygame.image.load("O.png")
        self.pieceX = pygame.transform.scale(self.pieceX, (40,40))
        self.pieceO = pygame.transform.scale(self.pieceO, (40,40))
    
    def place_piece(self):
        
        for row in range(len(self.game.board.grid)):
            for col in range(len(self.game.board.grid)):
                value = self.game.board.grid[row][col]
                piece_x = BOARD_X + (col * self.game.board.CELL_SIZE)
                piece_y = BOARD_Y + (row * self.game.board.CELL_SIZE)
                if value == "X":
                    main.blit(pieceX, (self.piece_x, piece_y))
                elif value == "O":
                    main.blit(pieceO, (self.piece_x, piece_y))

game = Game()
draw = DrawPiece(game)
                
            
playing = True

while playing:

    main.fill((50,30,72))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        
        game.playMove(event)
        draw.place_piece()

    pygame.display.update()
    
    
