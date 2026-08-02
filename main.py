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
        self.layout = pygame.image.load("gomoku_grid.png")
    
    def reset(self):
        self.grid = [[""] * self.SIZE for _ in range(self.SIZE)]

    def drawBoard(self):
        main.blit(self.layout, (BOARD_X, BOARD_Y))

    def get_cell(self, mouse_pos):
        x,y = mouse_pos
        x -= 100
        y -= 100

        if x < 0 or x >= 600 or y < 0 or y >= 600:
            return None
        else:
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
        self.playerScore = 0
        self.aiScore = 0
        self.restart = pygame.image.load("playagain.png")
        self.restartBut = self.restart.get_rect(center=(400, 450))
        self.addedScore = False
        self.back = pygame.image.load("back_button.png")
        self.backBut = self.back.get_rect(center = (50,75))
        self.starting = True
    
    def switchPlayer(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    def restarting(self):
        self.board.reset()
        self.winner = None
        self.game_over = False
        self.current_player = 1
        self.addedScore = False
        self.game_over = False

    
    def playMove(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            cell = self.board.get_cell(event.pos)
            if cell is None:
                return
            else:
                r, c = cell
                if self.board.grid[r][c] == "":

                    if self.current_player == 1:
                        self.board.grid[r][c] = self.PLAYER_1
                    else:
                        self.board.grid[r][c] = self.PLAYER_2

                    self.switchPlayer()

    def checkWin(self):
        size = self.board.SIZE
        grid = self.board.grid

        for row in range(size):
            for col in range(size):
                value = grid[row][col]

                if value == "":
                    continue

                # Horizontal
                if col <= size - 5:
                    if all(grid[row][col + i] == value for i in range(5)):
                        return "Horizontal", row, col, value

                # Vertical
                if row <= size - 5:
                    if all(grid[row + i][col] == value for i in range(5)):
                        return "Vertical", row, col, value

                # Diagonal: top-left to bottom-right
                if row <= size - 5 and col <= size - 5:
                    if all(grid[row + i][col + i] == value for i in range(5)):
                        return "DiagonalL2R", row, col, value

                # Diagonal: top-right to bottom-left
                if row <= size - 5 and col >= 4:
                    if all(grid[row + i][col - i] == value for i in range(5)):
                        return "DiagonalR2L", row, col, value

        return None, None, None, None

    
    def displayWin(self, winType, row, col):
        cell = self.board.CELL_SIZE

        directions = {
            "Horizontal": (0, 1),
            "Vertical": (1, 0),
            "DiagonalL2R": (1, 1),
            "DiagonalR2L": (1, -1)
        }

        row_change, col_change = directions[winType]

        end_row = row + row_change * 4
        end_col = col + col_change * 4

        start_x = BOARD_X + col * cell + cell // 2
        start_y = BOARD_Y + row * cell + cell // 2

        end_x = BOARD_X + end_col * cell + cell // 2
        end_y = BOARD_Y + end_row * cell + cell // 2

        pygame.draw.line(
            main,
            (100, 255, 255),
            (start_x, start_y),
            (end_x, end_y),
            5
        )
           

class DrawPiece:

    def __init__(self, game):
        self.game = game
        self.pieceX = pygame.image.load("X.png")
        self.pieceO = pygame.image.load("O.png")
        self.pieceX = pygame.transform.scale(self.pieceX, (30,30))
        self.pieceO = pygame.transform.scale(self.pieceO, (30,30))
    
    def place_piece(self):
        
        for row in range(len(self.game.board.grid)):
            for col in range(len(self.game.board.grid)):
                value = self.game.board.grid[row][col]
                piece_x = BOARD_X + (col * self.game.board.CELL_SIZE) + 6
                piece_y = BOARD_Y + (row * self.game.board.CELL_SIZE) + 6
                if value == "X":
                    main.blit(self.pieceX, (piece_x, piece_y))
                elif value == "O":
                    main.blit(self.pieceO, (piece_x, piece_y))


class AIplay:
    def __init__(self, game):
        self.waitingTime = 500
        self.potential = False
        self.level = 0
        self.game = game
        self.waiting = False
        self.startTime = 0

    def randomMove(self): #level 1
        empty_cells = []

        for row in range(self.game.board.SIZE):
            for col in range(self.game.board.SIZE):
                if self.game.board.grid[row][col] == "":
                    empty_cells.append((row, col))

        if empty_cells:
            row, col = random.choice(empty_cells)
            self.game.board.grid[row][col] = self.game.PLAYER_2
            self.game.switchPlayer()

    def blocking(self):
        grid = self.game.board.grid
        size = self.game.board.SIZE

        for row in range(size):
            for col in range(size):
                directions = [
                    (0, 1),   # horizontal
                    (1, 0),   # vertical
                    (1, 1),   # diagonal left-right
                    (1, -1)   # diagonal right-left
                ]

                for row_change, col_change in directions:
                    cells = []

                    # Look at groups of 4 cells
                    for i in range(4):
                        r = row + row_change * i
                        c = col + col_change * i

                        if not (0 <= r < size and 0 <= c < size):
                            break

                        cells.append((r, c))

                    if len(cells) != 4:
                        continue

                    player_count = 0
                    empty_cells = []

                    for r, c in cells:
                        if grid[r][c] == self.game.PLAYER_1:
                            player_count += 1
                        elif grid[r][c] == "":
                            empty_cells.append((r, c))

                    # Three X pieces and one empty space
                    if player_count == 3 and len(empty_cells) == 1:
                        r, c = empty_cells[0]
                        grid[r][c] = self.game.PLAYER_2
                        self.game.switchPlayer()
                        return True

        return False

    def findWin(self):
        grid = self.game.board.grid
        size = self.game.board.SIZE
        cell = []
        # after placcement find an empty place around it and check if the 
        # opposite has O as well if does then add one to form a row of 3 and just build

        for row in range(size): #check if theres any O placement yet
            for col in range(size):
                value = grid[row][col]
                
                if value == "O":
                    cell.append((row, col))
        
        if len(cell) == 0:
            return False
        else:
            for row, col in cell:
            #find cells surrounding
                preferChoice = []
                possibleChoice = []
                #hor
                if col + 1 < size:
                    if grid[row][col+1] == "":
                        possibleChoice.append((row,col+1))
                        if col - 1 >= 0 and grid[row][col-1] == "O":
                            preferChoice.append((row,col+1))
                if col - 1 >= 0:
                    if grid[row][col-1] == "":
                        possibleChoice.append((row,col-1))
                        if col + 1 < size and grid[row][col+1] == "O":
                            preferChoice.append((row,col-1))
                #ver
                if row + 1 < size:
                    if grid[row+1][col] == "":
                        possibleChoice.append((row+1,col))
                        if row - 1 >= 0 and grid[row-1][col] == "O":
                            preferChoice.append((row+1,col))
                if row - 1 >= 0:
                    if grid[row-1][col] == "":
                        possibleChoice.append((row-1,col))
                        if row + 1 < size and grid[row+1][col] == "O":
                            preferChoice.append((row-1,col))
        
                #diag 1
                if row + 1 < size and col + 1 < size:
                    if grid[row+1][col+1] == "":
                        possibleChoice.append((row+1,col+1))
                        if row - 1 >= 0 and col - 1 >= 0 and grid[row-1][col-1] == "O":
                            preferChoice.append((row+1,col+1))
                if row - 1 >= 0 and col - 1 >= 0:
                    if grid[row-1][col-1] == "":
                        possibleChoice.append((row-1,col-1))
                        if row + 1 < size and col + 1 < size and grid[row+1][col+1] == "O":
                            preferChoice.append((row-1,col-1))
                
                #diag 2
                if row + 1 < size and col - 1 >= 0:
                    if grid[row+1][col-1] == "":
                        possibleChoice.append((row+1,col-1))
                        if row - 1 >= 0 and col + 1 < size and grid[row-1][col+1] == "O":
                            preferChoice.append((row+1,col-1))
                if row - 1 >= 0 and col + 1 < size:
                    if grid[row-1][col+1] == "":
                        possibleChoice.append((row-1,col+1))
                        if row + 1 < size and col - 1 >= 0 and grid[row+1][col-1] == "O":
                            preferChoice.append((row-1,col+1))
            
            #see if there are any preferable move or just go with possible choices
            if len(preferChoice) != 0:
                r, c = random.choice(preferChoice)
                grid[r][c] = self.game.PLAYER_2
                self.game.switchPlayer()
                return True
            elif len(possibleChoice) != 0:
                r, c = random.choice(possibleChoice)
                grid[r][c] = self.game.PLAYER_2
                self.game.switchPlayer()
                return True
            else:
                return False

    def move(self):
        if self.level >= 3:
            if not self.blocking():
                if not self.findWin():
                    self.randomMove()
        elif self.level >= 2:
            if not self.blocking():
                self.randomMove()
        else:
            self.randomMove()
            

game = Game()
draw = DrawPiece(game)
game.board.reset()
ai = AIplay(game)
    
            
playing = True

easy_r = 50
medium_r = 50
hard_r = 50

easy = pygame.draw.circle(main, (100,255,100), (200,450), easy_r)
medium = pygame.draw.circle(main, (255,180,80),(400,450), medium_r)
hard = pygame.draw.circle(main, (255,100,100), (600,450), hard_r)

while playing:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if not game.game_over and not game.starting and game.current_player == 1:
            game.playMove(event)
        
        mouse_pos = pygame.mouse.get_pos() #animations

        if easy.collidepoint(mouse_pos):
            easy_r = 60
        else:
            easy_r = 50     
        if medium.collidepoint(mouse_pos):
            medium_r = 60
        else:
            medium_r = 50
        if hard.collidepoint(mouse_pos):
            hard_r = 60
        else:
            hard_r = 50

        if event.type == pygame.MOUSEBUTTONDOWN: #pressing buttons

            if game.game_over:
                if game.restartBut.collidepoint(event.pos):
                    game.restarting()

                elif game.backBut.collidepoint(event.pos):
                    game.restarting()
                    game.starting = True
                    game.playerScore = 0
                    game.aiScore = 0

            elif game.starting:
                if easy.collidepoint(event.pos):
                    ai.level = 1
                    game.starting = False

                elif medium.collidepoint(event.pos):
                    ai.level = 2
                    game.starting = False

                elif hard.collidepoint(event.pos):
                    ai.level = 3
                    game.starting = False

            else:
                if game.backBut.collidepoint(event.pos):
                    game.restarting()
                    game.starting = True
                    game.playerScore = 0
                    game.aiScore = 0



    result, row, col, winner = game.checkWin()
    
    if not game.starting: #delay between ai times and times before showing winning screen

        if result is not None and not game.game_over:
            game.game_over = True
            seeRel = pygame.time.get_ticks()
            

        if not game.game_over and game.current_player == 2:

            if not ai.waiting:
                ai.waiting = True
                ai.startTime = pygame.time.get_ticks()

            elif pygame.time.get_ticks() - ai.startTime >= ai.waitingTime:
                ai.move()
                ai.waiting = False

    main.fill((50, 30, 72))
    if not game.game_over and not game.starting: #main screen
        game.board.drawBoard()
        main.blit(game.back, game.backBut)
        draw.place_piece()
    elif game.game_over:
        time_since_win = pygame.time.get_ticks() - seeRel

        if time_since_win < 500: 
            game.board.drawBoard()
            draw.place_piece()
            game.displayWin(result, row, col)

        else: #ending bit

            if winner == "X":
                playerWin = "You"
                if not game.addedScore:
                    game.playerScore += 1
                    game.addedScore = True
            elif winner == "O":
                playerWin = "Robot"
                if not game.addedScore:
                    game.aiScore += 1
                    game.addedScore = True
            else:
                playerWin = "Draw"

            if playerWin != "Draw":
                winText = font.render(f"{playerWin} win!", True, (217,255,244))
            else:
                winText = font.render("It's a draw!", True, (217,255,244))

            main.blit(game.restart, game.restartBut)
            main.blit(game.back, game.backBut)
            scoring = subfont.render(f"Player's score: {game.playerScore}   AI's score: {game.aiScore}", True, (217,255,244))
            scoring_rect = scoring.get_rect(center=(400,300))
            winText_rect = winText.get_rect(center=(400,200))
            main.blit(winText, winText_rect)
            main.blit(scoring, scoring_rect)
        
    elif game.starting:
        welcome = font.render("Gomoku", True, (217,255,244))
        welcome_rect = welcome.get_rect(center=(400,200))
        main.blit(welcome, welcome_rect)

        easy = pygame.draw.circle(main, (100,255,100), (200,450), easy_r)
        medium = pygame.draw.circle(main, (255,180,80),(400,450), medium_r)
        hard = pygame.draw.circle(main, (255,100,100), (600,450), hard_r)

                        

    pygame.display.update()

pygame.quit()
    
