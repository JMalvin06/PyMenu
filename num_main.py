import pygame
import sys
import random
import copy
from num_settings import *
'''
This is my rendition of 2048 using pygame, which is actually my second iteration.
I decided to utilize the values stored within the Tile object more than values in arrays (I figured that out the hard way)
This was slightly painful to program, but I hope you enjoy!
'''

reset = False
ready = True
input_time = 0
input_cooldown = COOLDOWN
quit = False

def delay():
    global ready
    if not ready:
        current_time = pygame.time.get_ticks()
        if current_time - input_time >= input_cooldown:
            ready = True

class Game(): 
    def __init__(self):
        self.score_val = 0
        self.background = pygame.Surface((400,400))
        self.background.fill((186,172,159))
        self.tiles_back = [pygame.Surface((TILE_SIZE,TILE_SIZE)) for i in range(16)]
        self.score = pygame.Surface((90,75))
        self.score.fill((186,172,159))
        self.new_game_button = pygame.Surface((145,45))
        self.new_game_button.fill((142,122,101))
        self.undo_button = pygame.Surface((90,45))
        self.undo_button.fill((142,122,101))
        self.change = False
        self.board = copy.deepcopy(BOARD)
        self.tile_size = TILE_SIZE
        self.tiles = pygame.sprite.Group()
        self.update_board()
        self.add_rand()
        self.has_won = False
        self.prev_board = copy.deepcopy(self.board)
        self.prev_score = 0


    def update_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != 0:
                    tile = Tile((col * (self.tile_size + 5) + 113, row * (self.tile_size + 5) + 113),(row,col), self.tile_size,self.board[row][col])
                    self.tiles.add(tile)

    def get_input(self):
        global input_time
        global ready
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and ready:
            self.prev_board = copy.deepcopy(self.board)
            self.prev_score = self.score_val
            self.move_up()
            self.merge_up()
            if self.change and ready:
                self.add_rand()
            self.update_text()
            ready = False
            self.change = False
            input_time = pygame.time.get_ticks()
            self.check_win()
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and ready:
            self.prev_board = copy.deepcopy(self.board)
            self.prev_score = self.score_val
            self.move_down()
            self.merge_down()
            if self.change and ready:
                self.add_rand()
            self.update_text()
            ready = False
            self.change = False
            input_time = pygame.time.get_ticks()
            self.check_win()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ready:
            self.prev_board = copy.deepcopy(self.board)
            self.prev_score = self.score_val
            self.move_left()
            self.merge_left()
            if self.change and ready:
                self.add_rand()
            self.update_text()
            ready = False
            self.change = False
            input_time = pygame.time.get_ticks()
            self.check_win()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and ready:
            self.prev_board = copy.deepcopy(self.board)
            self.prev_score = self.score_val
            self.move_right()
            self.merge_right()
            if self.change and ready:
                self.add_rand()
            self.update_text()
            ready = False
            self.change = False
            input_time = pygame.time.get_ticks()
            self.check_win()
        if keys[pygame.K_ESCAPE]:
            self.pause_game('Paused', 20)
        if keys[pygame.K_r] and ready:
            self.reset()
            input_time = pygame.time.get_ticks()
            ready = False
        if keys[pygame.K_u] and ready:
            self.undo()
            input_time = pygame.time.get_ticks()
            ready = False

    def reset(self):
        self.board = copy.deepcopy(BOARD)
        for tile in self.tiles:
            self.tiles.remove(tile)
        self.add_rand()
        self.prev_board = copy.deepcopy(self.board)
        self.prev_score = 0
        self.ready = False
        self.input_time = pygame.time.get_ticks()
        self.score_val = 0

    def undo(self):
        self.board = copy.deepcopy(self.prev_board)
        self.score_val = self.prev_score
        for tile in self.tiles:
            self.tiles.remove(tile)
        self.update_board()

    def move_up(self):
        for row in range(1,len(self.board)):
            for col in range(4):
                if self.board[row][col] != 0 and self.board[row - 1][col] == 0:
                    for tile in self.tiles:
                        if tile.board_pos == (row,col):
                            self.board[row - 1][col] = self.board[row][col]
                            self.board[row][col] = 0
                            tile.board_pos = (row - 1, col)
                            new_pos = ((col * (self.tile_size + 5)) + 113, ((row-1) * (self.tile_size + 5)) + 113)
                            if tile.rect.topleft != new_pos:
                                tile.new_pos = new_pos
                            self.move_up()
                            self.change = True
                            break

    def move_down(self):
        for row in range(len(self.board) - 2, -1, -1):
            for col in range(len(self.board[row])):
                if self.board[row][col] != 0 and self.board[row + 1][col] == 0:
                    for tile in self.tiles:
                        if tile.board_pos == (row,col):
                            self.board[row + 1][col] = self.board[row][col]
                            self.board[row][col] = 0
                            tile.board_pos = (row + 1, col)
                            new_pos = ((col * (self.tile_size + 5)) + 113, ((row+1) * (self.tile_size + 5)) + 113)
                            if tile.rect.topleft != new_pos:
                                tile.new_pos = new_pos
                            self.move_down()
                            self.change = True
                            break
    
    def move_right(self):
        for col in range(len(self.board) - 2, -1, -1):
            for row in range(len(self.board[col])):
                if self.board[row][col] != 0 and self.board[row][col + 1] == 0:
                    for tile in self.tiles:
                        if tile.board_pos == (row,col):
                            self.board[row][col + 1] = self.board[row][col]
                            self.board[row][col] = 0
                            tile.board_pos = (row, col + 1)
                            new_pos = (((col+1) * (self.tile_size + 5)) + 113, (row * (self.tile_size + 5)) + 113)
                            if tile.rect.topleft != new_pos:
                                tile.new_pos = new_pos
                            self.move_right()
                            self.change = True
                            break

    def move_left(self):
        for col in range(1,len(self.board)):
            for row in range(4):
                if self.board[row][col] != 0 and self.board[row][col - 1] == 0:
                    for tile in self.tiles:
                        if tile.board_pos == (row,col):
                            self.board[row][col - 1] = self.board[row][col]
                            self.board[row][col] = 0
                            tile.board_pos = (row, col - 1)
                            new_pos = (((col-1) * (self.tile_size + 5)) + 113, (row * (self.tile_size + 5)) + 113)
                            if tile.rect.topleft != new_pos:
                                tile.new_pos = new_pos
                            self.move_left()
                            self.change = True
                            break

    def merge_down(self):
        for row in range(len(self.board) - 1, 0, -1):
            for col in range(len(self.board[row])):
                if self.board[row][col] == self.board[row - 1][col] and self.board[row][col] != 0: 
                    for tile in self.tiles:
                        if tile.board_pos == (row - 1,col):
                            self.board[row][col] = self.board[row][col] * 2
                            self.score_val += self.board[row][col]
                            self.board[row - 1][col] = 0
                            tile.new_pos = ((col * (self.tile_size + 5)) + 113, ((row) * (self.tile_size + 5)) + 113)
                            self.tiles.remove(tile)
                            self.change = True
                            self.move_down()
                            break
    
    def merge_up(self):
        for row in range(0,len(self.board) - 1):
            for col in range(4):
                if self.board[row][col] == self.board[row + 1][col] and self.board[row][col] != 0:
                    for tile in self.tiles:
                        if tile.board_pos == (row + 1,col):
                            self.board[row][col] = self.board[row][col] * 2
                            self.score_val += self.board[row][col]
                            self.board[row + 1][col] = 0
                            tile.new_pos = ((col * (self.tile_size + 5)) + 113, ((row) * (self.tile_size + 5)) + 113)
                            self.tiles.remove(tile)
                            self.change = True
                            self.move_up()
                            break

    def merge_left(self):
        for col in range(0,len(self.board) - 1):
            for row in range(4):
                if self.board[row][col] == self.board[row][col + 1] and self.board[row][col] != 0:
                    for tile in self.tiles:
                        if tile.board_pos == (row,col + 1):
                            self.board[row][col] = self.board[row][col] * 2
                            self.score_val += self.board[row][col]
                            self.board[row][col + 1] = 0
                            tile.new_pos = ((col * (self.tile_size + 5)) + 113, ((row) * (self.tile_size + 5)) + 113)
                            self.tiles.remove(tile)
                            self.change = True
                            self.move_left()
                            break
                            
    def merge_right(self):
        for col in range(len(self.board) - 1, 0, -1):
            for row in range(len(self.board[col])):
                if self.board[row][col] == self.board[row][col - 1] and self.board[row][col] != 0:
                    for tile in self.tiles:
                        if tile.board_pos == (row,col - 1):
                            self.board[row][col] = self.board[row][col] * 2
                            self.score_val += self.board[row][col]
                            self.board[row][col - 1] = 0
                            tile.new_pos = ((col * (self.tile_size + 5)) + 113, ((row) * (self.tile_size + 5)) + 113)
                            self.tiles.remove(tile)
                            self.change = True
                            self.move_right()
                            break
    

    def update_text(self):
        for row_index, row in enumerate(self.board):
            for col_index in range(len(row)):
                for tile in self.tiles:
                    if tile.board_pos == (row_index,col_index):
                        tile.value = self.board[row_index][col_index]

    def add_rand(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        four_chance = 1 == random.randint(1,10)
        value = 2
        if four_chance: value = 4
        if self.board[row][col] == 0:
            self.tiles.add(Tile(((col * (self.tile_size + 5)) + 113, (row * (self.tile_size + 5)) + 113), (row,col), self.tile_size, value))
            self.board[row][col] = value
        else:
            self.add_rand()

    def check_win(self):
        for row in self.board:
            for val in row:
                if val == 2048 and not self.has_won:
                    self.pause_game('You Won!', 0)
                    self.has_won = True


    def run(self):
        for tile in self.tiles:
            tile.set_pos()
            self.board[tile.board_pos[0]][tile.board_pos[1]] = tile.value
            if (tile.remove and tile.rect.topleft == tile.new_pos) or tile.value == 0:
                self.tiles.remove(tile)
                self.board[tile.board_pos[0]][tile.board_pos[1]] = 0
        screen.blit(self.background,(100,100))
        screen.blit(self.score, ((110,10)))
        font = pygame.font.SysFont(None, 40)
        score_title = font.render('Score',True,'white')
        font = pygame.font.SysFont(None, 50)
        score_text = font.render(str(self.score_val),True,'white')
        font = pygame.font.SysFont(None, 38)
        new_game_text = font.render('New Game',True,'white')
        undo_text = font.render('Undo',True,'white')
        if self.score_val >= 10000:
            screen.blit(score_text,(105,45))
        elif self.score_val >= 1000:
            screen.blit(score_text,(115,45))
        elif self.score_val >= 100:
            screen.blit(score_text,(125,45))
        elif self.score_val >= 10:
            screen.blit(score_text,(135,45))
        else:
            screen.blit(score_text,(145,45))
        
        screen.blit(score_title,(117,20))
        
        for row in range(4):
            for col in range(4):
                for tile in self.tiles_back:
                    tile.fill((204,192,180))
                    screen.blit(tile,((col * (self.tile_size + 5)) + 113, ((row-1) * (self.tile_size + 5)) + 208))
        
        screen.blit(self.new_game_button,(350,40))
        screen.blit(new_game_text,(355,50))
        screen.blit(self.undo_button,(250,40))
        screen.blit(undo_text,(261,50))
        self.tiles.draw(screen)
        self.get_input()
        delay()
        for tile in self.tiles:
            tile.run()
    
    def pause_game(self,text,offset):
        global quit
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        #pygame.quit()
                        #exit()
                        quit = True
                        paused = False
                screen.fill('grey')
                font = pygame.font.SysFont(None, 100)
                title_text = font.render(text,True,'black')
                font = pygame.font.SysFont(None, 50)
                desc_text = font.render('Press C to continue or Q to quit',True,'black')
                screen.blit(title_text, (150 + offset,200))
                screen.blit(desc_text, (40,300))
                pygame.display.update()


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,board_pos,size,val):
        super().__init__()
        self.pos = pos
        self.new_pos = pos
        self.image = pygame.Surface((size,size))
        self.board_pos = board_pos
        self.rect = self.image.get_rect(topleft = pos)
        self.value = val
        self.direction = pygame.math.Vector2()
        self.speed = 95
        self.remove = False
    
    def set_pos(self):
        if self.rect.topleft != self.new_pos:
            if self.rect.x > self.new_pos[0]:
                self.direction.x = -1
            elif self.rect.x < self.new_pos[0]:
                self.direction.x = 1
            else:
                self.direction.x = 0
            if self.rect.y > self.new_pos[1]:
                self.direction.y = -1
            elif self.rect.y < self.new_pos[1]:
                self.direction.y = 1
            else:
                self.direction.y = 0
            
            self.rect.topleft += self.direction * self.speed

    
    def run(self):
        color = (0,0,0)
        pos = (30,25)
        text_color = 'white'
        if self.value < 16:
            pos = (30,25)
            size = 75
            if self.value == 2:
                color = (238,228,218)
                text_color = 'black'
            elif self.value == 4:
                color = (237,224,200)
                text_color = 'black'
            elif self.value == 8:
                color  = (242,177,121)
        elif self.value == 128:
            pos = (0,25)
            size = 75
            color = (237,207,115)
        elif self.value < 128:
            pos = (15,25)
            size = 75
            if self.value == 16:
                color = (245,149,99)
            elif self.value == 32:
                color = (246,124,96)
            else:
                color = (246,94,59)
        elif self.value < 1024:
            pos = (5,25)
            size = 70
            if self.value == 256:
                color = (237,204,98)
            else:
                color = (237,200,80)
        else:
            pos = (5,30)
            size = 50
            if self.value == 1024:
                color = (237,197,63)
            elif self.value == 2048:
                color = (237,194,45)
            else:
                color = (62,57,51)
        font = pygame.font.SysFont(None, size)
        tile_text = font.render(str(self.value),True,text_color)
        self.image.fill(color)
        self.image.blit(tile_text, pos)


def start_num():
    pygame.init()
    global screen
    global ready
    global input_time
    global quit
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or quit:
                #pygame.quit()
                #sys.exit()
                quit = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0] >= 350 and mouse_pos[0] <= 495 and mouse_pos[1] >= 40 and mouse_pos[1] <= 95) and ready:
                    game.reset()
                    input_time = pygame.time.get_ticks()
                    ready = False
                elif (mouse_pos[0] >= 250 and mouse_pos[0] <= 360 and mouse_pos[1] >= 40 and mouse_pos[1] <= 95) and ready:
                    game.undo()
                    input_time = pygame.time.get_ticks()
                    ready = False

        screen.fill((249,248,238))
        game.run()
        pygame.display.set_caption(('2048 Pygame'))
        pygame.display.flip()
        clock.tick(FPS)
