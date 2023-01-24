import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.image.fill((50,145,255))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 25
        self.vel = Vector2(0,0)
        self.pos = Vector2(pos)
        self.direction = 'right'
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.vel.y == 0:
            self.vel = Vector2(0,-self.speed)
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.vel.y == 0:
            self.vel = Vector2(0,self.speed)
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.vel.x == 0:
            self.vel = Vector2(-self.speed,0)
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.vel.x == 0:
            self.vel = Vector2(self.speed,0)
    
    def get_input(self):
        if self.direction == 'right':
            self.vel = Vector2(self.speed,0)
        elif self.direction == 'left':
            self.vel = Vector2(-self.speed,0)
        elif self.direction == 'up':
            self.vel = Vector2(0,-self.speed)
        elif self.direction == 'down':
            self.vel = Vector2(0,self.speed)
        elif self.direction == 'none':
            self.vel = Vector2(0,0)

    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def update(self):
        pass
        #self.player_input()


    def fixed_update(self,next_move):
        self.direction = next_move
        self.get_input()
        self.pos += self.vel
        self.rect.center = self.pos


    
class Tail(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.image.fill((50,145,255))
        self.rect = self.image.get_rect(center = pos)
        self.pos = self.rect.x,self.rect.y
    

    def set_last_pos(self,pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    

