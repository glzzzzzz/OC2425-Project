from config import *
from sprite import Sprite
from player import Player

class Monster(Player):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, groups, collision_sprites)
        self.image.fill('green')

class Zombie(Player):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, groups, collision_sprites)
        self.image.fill('blue')

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        #groupes de sprites
        self.all_sprites = pygame.sprite.Group()

        self.collision_sprites = pygame.sprite.Group()


        self.setup (tmx_map)
    
    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('terrain').tiles():
            Sprite((x*32,y*32-100), surf, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Object'): 
            if obj.name =='monster':
                Monster((obj.x, obj.y-100), self.all_sprites, self.collision_sprites)
            if obj.name == 'zombie':
                Zombie((obj.x, obj.y-100), self.all_sprites, self.collision_sprites)

            tmx_map.get_layer_by_name('Object')
    def run(self, dt):
        
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)