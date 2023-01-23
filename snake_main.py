import pygame
import sys
from snake import *
from random import *
class Game():
    def __init__(self):
        player_pos = (12.5,12.5)
        INITIAL_SCORE = 2
        player_sprite = Player(player_pos)
        player_sprite.rect.x = 0
        player_sprite.rect.y = 0
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.tails = pygame.sprite.Group()
        self.prev_pos = (-25,-25)
        self.last_tail_pos = self.prev_pos
        self.game_start = self.player.sprite.vel.x != 0 or self.player.sprite.vel.x != 0
        
        self.apple_sprite  = Apple()
        self.apple = pygame.sprite.GroupSingle(self.apple_sprite)

        self.tail_positions = []
        #tail = Tail(self.prev_pos)
        #self.tails.add(tail)
        for i in range(INITIAL_SCORE):
            self.grow_snake()
        #    tail = Tail((self.prev_pos[0] - 25, self.prev_pos[1]))
        #    self.tails.add(tail)


    def grow_snake(self):
        tail = Tail((self.last_tail_pos[0] + 12.5, self.last_tail_pos[1] + 12.5))
        self.tails.add(tail)

    def run(self):
        self.apple.draw(screen)
        self.player.draw(screen)
        self.tails.draw(screen)
        self.player.update()
        if self.isCollide():
            self.apple.update()
            self.grow_snake()
        
               
    def isCollide(self):
        collide = self.apple_sprite.rect.colliderect(self.player.sprite.rect)
        return collide

    def fixed_update(self):
        #print('player: ',str(self.player.sprite.get_pos()))
        #for tail in self.tails:
        #    print(tail.pos)
        self.prev_pos = self.player.sprite.get_pos()
        self.tail_positions = [(tail.rect.x,tail.rect.y) for tail in self.tails]
        self.last_tail_pos = self.tail_positions[-1]
        del self.tail_positions[-1]
        self.tail_positions.insert(0,self.prev_pos)
        self.prev_pos = (self.player.sprite.rect.x, self.player.sprite.rect.y)
        for pos in enumerate(self.tail_positions):
            for tail in enumerate(self.tails):
                if(tail[0] == pos[0]):
                    tail[1].rect.center = pos[1][0] + 12.5 ,pos[1][1] + 12.5
        collision = pygame.sprite.spritecollide(self.player.sprite,self.tails,False)
        if (len(collision) >= 2 or self.player.sprite.rect.x >= 600 or self.player.sprite.rect.x < 0 or self.player.sprite.rect.y >= 600 or self.player.sprite.rect.y < 0) and self.game_start:
            start_snake()
        self.player.sprite.fixed_update()
        if not self.game_start:
            self.game_start = self.player.sprite.vel.x != 0 or self.player.sprite.vel.x != 0

class Apple(pygame.sprite.Sprite):
    def rand_pos(self):
        ran = [i for i in range(0,600,25)]
        return choice(ran), choice(ran)

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.image.fill('red')
        pos = (self.rand_pos()[0] + 12.5, self.rand_pos()[1] + 12.5)
        self.rect  = self.image.get_rect(center = pos)

    def update(self):
        self.rect.x = self.rand_pos()[0]
        self.rect.y = self.rand_pos()[1]

def reset():
    global game
    game = Game()

def start_snake():
    pygame.init()
    screen_width, screen_height = 600, 600
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    game = Game()
    clock = pygame.time.Clock()
    SCREEN_UPDATE = pygame.USEREVENT + 1
    pygame.time.set_timer(SCREEN_UPDATE, 200)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == SCREEN_UPDATE:
                game.fixed_update()
        
        screen.fill((175,215,70))
        game.run()  
        
        pygame.display.set_caption("Score: " + str(len(game.tails)))
        pygame.display.flip()
        clock.tick(60)