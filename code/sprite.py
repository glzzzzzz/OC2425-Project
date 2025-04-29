import pygame
from config import TILE_SIZE
 
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, type_element):
        super().__init__(groups)
        if type_element == 0 : 
            self.image = pygame.image.load(r'OC2425-Project/data/background/sol.png').convert_alpha()
        if type_element == 1 : 
            self.image = pygame.image.load(r'OC2425-Project/data/background/feuilles.png').convert_alpha()

        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()