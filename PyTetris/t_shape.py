import pygame

class Shape():
    def __init__(self,group):
        self.group = group
        self.screen_ready = False
        self.screen_cooldown = 1000
        self.screen_time = pygame.time.get_ticks()
        self.input_ready = False
        self.input_cooldown = 100
        self.input_time = 0
    
    def screen_delay(self):
        if not self.screen_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.screen_time >= self.screen_cooldown:
                self.screen_ready = True
    
    def input_delay(self):
        if not self.input_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.input_time >= self.input_cooldown:
                self.input_ready = True
    
    def update(self):
        self.screen_delay()
        self.input_delay()
        for block in self.group:
            block.update()

    def move_down(self):
        if self.screen_ready:
            self.screen_time = pygame.time.get_ticks()
            for block in self.group:
                block.board_pos[0] += 1
            self.screen_ready = False
    
    def move_left(self):
        if self.input_ready:
            self.input_time = pygame.time.get_ticks()
            for block in self.group:
                if block.board_pos[1] <= 0:
                    block.board_pos[1] = 0
                else:
                    block.board_pos[1] -= 1
            self.input_ready = False

    def move_right(self):
        if self.input_ready:
            self.input_time = pygame.time.get_ticks()
            for block in self.group:
                block.board_pos[1] += 1
            self.input_ready = False
