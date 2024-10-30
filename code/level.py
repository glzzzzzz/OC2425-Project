from config import *
from sprite import Sprite
class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        #groups
        self.all_sprites = pygame.sprite.Group()



        self.setup (tmx_map)
    
    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('terrain').tiles():
            Sprite((x*32,y*32-100), surf, self.all_sprites)

    def run(self):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)