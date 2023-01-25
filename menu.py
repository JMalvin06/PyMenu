from snake_main import *
from num_main import *
from PyTetris.t_main import *

import pygame


class Menu():
    def __init__(self):
        self.held = False
        self.backdrop = pygame.Surface((500,500))
        self.backdrop.fill((190,190,190))
        font = pygame.font.SysFont(None, 80)
        self.title = font.render('3 Games in One',True,'black')
        font = pygame.font.SysFont(None, 50)
        self.caption = font.render('Select a Game:',True,'black')
        #self.backdrop.blit(self.title, (70,10))
        #self.backdrop.blit(self.caption, (120,80))
        self.snake_button = pygame.Surface((200,100))
        self.snake_button.fill((160,160,160))
        self.snake_outline = pygame.Surface((206,106))
        self.snake_outline.fill((0,0,0))
        font = pygame.font.SysFont(None, 70)
        self.snake_text = font.render('Snake',True,(0,0,0))
        
        self.num_button = pygame.Surface((200,100))
        self.num_button.fill((160,160,160))
        self.num_outline = pygame.Surface((206,106))
        self.num_outline.fill((0,0,0))
        self.first_text = font.render('2',True,(0,0,0))
        self.second_text = font.render('0',True,(0,0,0))
        self.third_text = font.render('4',True,(0,0,0))
        self.fourth_text = font.render('8',True,(0,0,0))

        self.tetris_button = pygame.Surface((200,100))
        self.tetris_button.fill((160,160,160))
        self.tetris_outline = pygame.Surface((206,106))
        self.tetris_outline.fill((0,0,0))
        self.st_text = font.render('Tetris',True,(0,0,0))
        self.blocks = []
        for i in range(4):
            cube = pygame.Surface((20,20))
            cube.fill('purple')
            self.blocks.append(cube)
        self.t_positions = [(270,465),(291,465),(312,465),(291,486)]

        self.snake = []
        for i in range(4):
            cube = pygame.Surface((20,20))
            cube.fill((50,145,255))
            self.snake.append(cube)
        self.s_positions = [(130,325),(130,345),(150,345),(170,345)]
        self.apple = pygame.Surface((20,20))
        self.apple.fill('red')

        self.tile = pygame.Surface((40,40))
        self.tile.fill((238,228,218))
        font = pygame.font.SysFont(None, 40)
        self.num = font.render('2',True,'black')

        
        #self.nd_text = font.render('0',True,(0,0,0))
        #self.rd_text = font.render('4',True,(0,0,0))
        #self.th_text = font.render('8',True,(0,0,0))
        #self.backdrop.blit(self.num_outline,(267,147))
        #self.backdrop.blit(self.num_button,(270,150))'''



    def update(self):
        for index, cube in enumerate(self.blocks):
            screen.blit(cube,self.t_positions[index])
        screen.blit(self.backdrop,(50,100))
        screen.blit(self.title, (85,120))
        screen.blit(self.caption, (170,180))
        self.backdrop.blit(self.snake_outline,(27,167))
        self.backdrop.blit(self.snake_button,(30,170))
        self.backdrop.blit(self.num_outline,(267,167))
        self.backdrop.blit(self.num_button,(270,170))
        self.backdrop.blit(self.tetris_outline,(147,307))
        self.backdrop.blit(self.tetris_button,(150,310))
        screen.blit(self.snake_text,(102,280))
        screen.blit(self.first_text,(365,279))
        screen.blit(self.second_text,(393,280))
        screen.blit(self.third_text,(419,280))
        screen.blit(self.fourth_text,(445,280))
        screen.blit(self.st_text,(230,420))
        #print(pygame.mouse.get_pos())
        for index, cube in enumerate(self.blocks):
            screen.blit(cube,self.t_positions[index])
        for index, cube in enumerate(self.snake):
            screen.blit(cube,self.s_positions[index])
        screen.blit(self.apple,(210,345))
        screen.blit(self.tile,(400,325))
        screen.blit(self.num, (413,333))
        self.check_events()
        
    
    def check_events(self):
        global screen
        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pos)
        if self.snake_button.get_rect().collidepoint((mouse_pos[0] - 81, mouse_pos[1] - 270)):
            #print(pygame.mouse.get_pressed())
            if pygame.mouse.get_pressed()[0]:
                self.snake_button.fill((120,120,120))
                self.held = True
            else:
                self.snake_button.fill((140,140,140))
            if not pygame.mouse.get_pressed()[0] and self.held:
                start_snake()
                self.held = False
                screen = pygame.display.set_mode((600,700))
        elif self.num_button.get_rect().collidepoint((mouse_pos[0] - 321, mouse_pos[1] - 270)):
            #print(pygame.mouse.get_pressed())
            if pygame.mouse.get_pressed()[0]:
                self.num_button.fill((120,120,120))
                self.held = True
            else:
                self.num_button.fill((140,140,140))
            if not pygame.mouse.get_pressed()[0] and self.held:
                start_num() 
                self.held = False
                screen = pygame.display.set_mode((600,700))
        elif self.tetris_button.get_rect().collidepoint((mouse_pos[0] - 201, mouse_pos[1] - 412)):
            #print(pygame.mouse.get_pressed())
            if pygame.mouse.get_pressed()[0]:
                self.tetris_button.fill((120,120,120))
                self.held = True
            else:
                self.tetris_button.fill((140,140,140))
            if not pygame.mouse.get_pressed()[0] and self.held:
                start_tetris() 
                self.held = False
                screen = pygame.display.set_mode((600,700))
        else:
            self.held = False
            self.num_button.fill((160,160,160))
            self.snake_button.fill((160,160,160))
            self.tetris_button.fill((160,160,160))
        #else:
            #print('nan')
        #if self.num_button.get_rect().collidepoint(pygame.mouse.get_pos()):
        #    print('2048')
        


pygame.init()
menu = Menu()
screen = pygame.display.set_mode((600,700))
clock = pygame.time.Clock()
while True:
    #screen = pygame.display.set_mode((600,700))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.set_caption(f'{clock.get_fps() :.1f}')
    screen.fill((30,30,30))
    menu.update()
    pygame.display.flip()
    clock.tick(60)
    