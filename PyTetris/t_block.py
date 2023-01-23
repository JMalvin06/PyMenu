import pygame
from PyTetris.t_settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self,board_pos,color,is_shape=False):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill(color)
        self.pos = (board_pos[1] + 1) * (TILE_SIZE + 1) + 125, (board_pos[0] + 1) * (TILE_SIZE + 1) + 25
        self.rect = self.image.get_rect(topleft = self.pos)
        self.board_pos =  board_pos
        self.is_shape = is_shape
    
    def update(self):
        #self.rect.
        self.rect.topleft = (self.board_pos[1] + 1) * (TILE_SIZE + 1) + 125, (self.board_pos[0] + 1) * (TILE_SIZE + 1) + 25
        #self.rect.y = (self.board_pos[0] + 1) * (TILE_SIZE + 1) + 25