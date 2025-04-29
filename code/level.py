from config import *
from sprite import Sprite
from player import Player, Objet
import pygame

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.players = []

        self.setup(tmx_map)

        # Créer la bombe APRES avoir instancié les joueurs
        self.bombe = Objet("chat", (255, 255, 0), self.all_sprites, self.players)

        # Mettre à jour les joueurs avec la bombe
        for p in self.players:
            p.bombe = self.bombe
            p.has_bomb = (p.role == self.bombe.owner)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE - 100), surf, (self.all_sprites, self.collision_sprites))
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'monster':
                p = Player((obj.x, obj.y - 100), self.all_sprites, self.collision_sprites, "chat", self.players, None)
                self.players.append(p)
                self.collision_sprites.add(p)
            if obj.name == 'zombie':
                p = Player((obj.x, obj.y - 100), self.all_sprites, self.collision_sprites, "souris", self.players, None)
                self.players.append(p)
                self.collision_sprites.add(p)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)
