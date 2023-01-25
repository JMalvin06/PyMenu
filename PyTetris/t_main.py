
import random
from PyTetris.t_settings import *
from PyTetris.t_block import *
from PyTetris.t_shape import *
import pygame
import copy

game_end =  False

class Game():
    def __init__(self):
        global game_end
        game_end = False
        self.lines_scored = 0
        self.score = 0
        self.line_count = 0
        self.r_ready = True
        self.r_time = 0
        self.r_cooldown = 200
        self.board = BOARD
        self.background = []
        self.blocks = pygame.sprite.Group()
        for row in range(22):
            for col in range(12):
                if (row < 1 or row >= 21) or col == 0 or col == 11:
                    image = pygame.Surface((TILE_SIZE,TILE_SIZE))
                    image.fill('grey')
                    self.background.append((image, (col, row)))
                    #screen.blit(image, (col * (TILE_SIZE + 1) + 125,row * (TILE_SIZE + 1) + 25))
        for row_index,row in enumerate(self.board):
            for col_index, space in enumerate(row):
                if space == 'x':
                    block = Block([row_index,col_index],'red')
                    self.blocks.add(block)
        #self.blocks.add(Block((5,4)))
        self.shape = Shape(self.create_shape())
        for block in self.shape.group:
            self.blocks.add(block)
            #print(block.board_pos)
        
    def update_board(self):
        for block in self.blocks:
            self.blocks.remove(block)
        for row in self.board():
            for val in row:
                pass

                
    def delay_rotation(self):
        if not self.r_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.r_time >= self.r_cooldown:
                self.r_ready = True

    def remove_shape(self):
        global game_end
        for tile in self.shape.group:
            tile.is_shape = False
            self.shape.group.remove(tile)
        for block in self.blocks:
            if block.board_pos[0] == 1 and (block.board_pos[1] <= 3 and block.board_pos[1] <= 6):
                #self.reset()
                game_end = True
                return None
        self.shape.group = self.create_shape()
        
    def is_under(self):
        for block in self.blocks:
            for s_block in self.shape.group:
                if block.board_pos[1] == s_block.board_pos[1] and block.board_pos[0] - 1 == s_block.board_pos[0] and not block.is_shape:
                    return True
        return False

    def is_right(self):
        for block in self.blocks:
            for s_block in self.shape.group:
                if (block.board_pos[0] == s_block.board_pos[0] and block.board_pos[1] - 1 == s_block.board_pos[1] and not block.is_shape) or s_block.board_pos[1] == 9:
                    return True
        return False
    
    def is_left(self):
        for block in self.blocks:
            for s_block in self.shape.group:
                if (block.board_pos[0] == s_block.board_pos[0] and block.board_pos[1] + 1 == s_block.board_pos[1] and not block.is_shape) or s_block.board_pos[1] == 0:
                    return True
        return False

    def is_bottom(self):
        for block in self.shape.group:
            if block.board_pos[0] == 19:
                return True
        return False

    def get_input(self):
        #right_end = False
        #left_end = False
        keys = pygame.key.get_pressed()
        '''for block in self.shape.group:
                if block.board_pos[1] >= 9:
                    right_end = True
                    break
                if block.board_pos[1] <= 0:
                    left_end = True
                    break'''
                
        if keys[pygame.K_RIGHT]  and not self.is_right():
            self.shape.move_right()
        if keys[pygame.K_LEFT] and not self.is_left():
            self.shape.move_left()
        if keys[pygame.K_UP] and self.r_ready:
            self.r_ready = False
            self.r_time = pygame.time.get_ticks()
            self.rotate_shape()
            #print('done')
        if keys[pygame.K_SPACE]:
            self.shape.screen_cooldown = 25
        else:
            self.shape.screen_cooldown = 1000
            

    
    def update(self):
        self.delay_rotation()
        self.get_input()
        self.shape.update()
        #for row in self.board:
        #    print(row)
        #print()
        
        if (self.is_bottom() or self.is_under()) and self.shape.screen_ready:
            self.remove_shape()
            self.shape = Shape(self.create_shape())
            for block in self.shape.group:
                self.blocks.add(block)
            self.delete_lines()
            
            #print('done')
        
        
        self.shape.move_down()
        for image in self.background:
            screen.blit(image[0], (image[1][0] * (TILE_SIZE + 1) + 125,image[1][1] * (TILE_SIZE + 1) + 25))
        '''for row_index in range(len(self.board)):
            for col_index in range(len(self.board[0])):
                next = False
                for block in self.blocks:
                    #print('row_index: ' + str(row_index))
                    #print(block.board_pos[0])
                    if (block.board_pos[0] == row_index and block.board_pos[1] == col_index):
                        self.board[block.board_pos[0]][block.board_pos[1]] = 'x'
                        next = True
                        break
                if not next and self.board[row_index][col_index] == 'x':
                    self.board[row_index][col_index] = '-'''
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[0])):
                self.board[row_index][col_index] = '-'
                for block in self.blocks:
                    if (block.board_pos[0] == row_index and block.board_pos[1] == col_index):
                        self.board[block.board_pos[0]][block.board_pos[1]] = 'x'
                        break

        self.blocks.draw(screen)
        
        #for block in self.shape.group:
        #    print(block.board_pos)
        #for block in self.blocks:
        #    print(block.board_pos)
    
    def delete_lines(self):
        line_count = 0
        for row_index, row in enumerate(self.board):
            line = True
            for val in row:
                if val == '-':
                    line = False
                    break
            if line:
                line_count += 1
                for i in range(row_index,0,-1):
                    for j in range(len(row)):
                        if i == row_index:
                            self.board[i][j] = '-'
                            for block in self.blocks:
                                if block.board_pos[0] == i and block.board_pos[1] == j:
                                    self.blocks.remove(block)
                        else:
                            #self.board[i+1][j] = self.board[i][j]
                            for block in self.blocks:
                                if block.board_pos[0] == i and block.board_pos[1] == j and not block.is_shape:
                                    block.board_pos[0] += 1
                            #self.board[i][j] = '-'
                            
                for block in self.blocks:
                    block.update()
        self.line_count += line_count
        self.add_score(line_count)

    def rotate_shape(self):
        min_row, min_col = 200,200
        for block in self.shape.group:
            if block.board_pos[1] < min_col:
                min_row = block.board_pos[0]
                min_col = block.board_pos[1]
            #if block.board_pos[1] < min_col:
            #    min_col = block.board_pos[0]
        count = 0
        if self.rotation >= len(SHAPES[self.shape_num]) - 1:
            self.rotation = 0
        else:
            self.rotation += 1
        row_positions = []
        col_positions = []
        left_dif = 0
        vert_dif = 0
        hor_block_dif = 0
        for row_index,row in enumerate(SHAPES[self.shape_num][self.rotation]):
            for col_index,col in enumerate(row):
                if col == 'x':
                    b_count = 0
                    for block in self.shape.group:
                        if b_count == count:
                            #print(col_index + min_col)
                            #print(len(self.board[0]))
                            
                            if col_index + min_col >= len(self.board[0]):
                                left_dif = ((col_index + min_col) - len(self.board[0])) + 1
                            if row_index + min_row >= len(self.board):
                                vert_dif = ((row_index + min_row) - len(self.board)) + 1
                            for c_block in self.blocks:
                                if (col_index + min_col == c_block.board_pos[1] and row_index + min_row == c_block.board_pos[0]) and not c_block.is_shape:
                                    max_col = 0
                                    for r in range(len(SHAPES[self.shape_num][self.rotation])):
                                        for c in range(len(SHAPES[self.shape_num][self.rotation][r])):
                                            if c > max_col:
                                                max_col = c
                                    hor_block_dif = ((max_col + min_col) - c_block.board_pos[1]) + 2
                                    print(hor_block_dif)
                            row_positions.append(row_index + min_row)
                            col_positions.append(col_index + min_col)
                        b_count += 1
                    count += 1
        prev_rot = [(block.board_pos[0],block.board_pos[1]) for block in self.shape.group]
        #print(prev_rot)
        for index, block in enumerate(self.shape.group):
            block.board_pos[0] = row_positions[index] - vert_dif
            #print(hor_block_dif)
            block.board_pos[1] = (col_positions[index] - left_dif) - hor_block_dif
        for s_block in self.shape.group:
            for t_block in self.blocks:
                if((s_block.board_pos[0] == t_block.board_pos[0] and s_block.board_pos[1] == t_block.board_pos[1]) and not t_block.is_shape) or s_block.board_pos[1] < 0:
                    #print('revert')
                    self.rotation - 1
                    for i, n_block in enumerate(self.shape.group):
                        n_block.board_pos[0] = prev_rot[i][0] 
                        n_block.board_pos[1] = prev_rot[i][1]
                    
        #if self.is_left():

                    
    def add_score(self,score):
        if score == 1:
            self.score += 40 * (int(self.lines_scored/10 + 1))
        elif score == 2:
            self.score += 100 * (int(self.lines_scored/10 + 1))
        elif score == 3:
            self.score += 300 * (int(self.lines_scored/10 + 1))
        elif score == 4:
            self.score += 1200 * (int(self.lines_scored/10 + 1))
        
        



    def get_color(self,val):
        if val == 0:
            return 'orange'
        elif val == 1:
            return 'blue'
        elif val == 2:
            return 'yellow'
        elif val == 3:
            return 'purple'
        elif val == 4:
            return 'red'
        elif val == 5:
            return 'green'
        elif val == 6:
            return 'teal'


    def create_shape(self):
        group = pygame.sprite.Group()
        self.shape_num = random.randint(0,len(SHAPES) - 1)
        color = self.get_color(self.shape_num)
        self.rotation = 0
        for row_index,row in enumerate(SHAPES[self.shape_num][self.rotation]):
            for col_index,col in enumerate(row):
                if col == 'x':
                    group.add(Block([row_index,col_index+3],color,True))
        return group

    def reset(self):
        for block in self.blocks:
            self.blocks.remove(block)
            if block.is_shape:
                self.shape.group.remove(block)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j] = '-'
                
       
        
        
        
        

def start_tetris():
    global screen
    global game_end
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    game = Game()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_end:
                game.reset()
                return None
                pygame.quit()
                exit()
        
        screen.fill((30,30,30))
        
        game.update()
        pygame.display.set_caption(str(game.score))
        pygame.display.flip()
        clock.tick(FPS)