from config import *
from timer import Timer
import pygame
from pygame.math import Vector2 as vector

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, role):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill('red')
        self.role = role
        # position
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        # movement
        self.direction = vector(0, 0)
        self.speed = 200
        self.gravity = 1000
        self.jump = False
        self.jump_height = 300
        # collision
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        # timers
        self.timers = {
            'wall jump': Timer(400)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        # Horizontal movement based on role
        if not self.timers['wall jump'].active:
            if self.role == 'chat':  # joueur 1 avec WASD
                if keys[pygame.K_d]:
                    input_vector.x += 1
                if keys[pygame.K_a]:
                    input_vector.x -= 1
            else:  # joueur 2 avec flèches
                if keys[pygame.K_RIGHT]:
                    input_vector.x += 1
                if keys[pygame.K_LEFT]:
                    input_vector.x -= 1
            # Norme de 1 si vecteur non nul
            self.direction.x = input_vector.normalize().x if input_vector.length_squared() > 0 else 0

        # Jump based on role
        if self.role == 'chat':
            if keys[pygame.K_w]:
                self.jump = True
        else:
            if keys[pygame.K_UP]:
                self.jump = True

    def move(self, dt):
        # Horizontal movement
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical movement and gravity
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])):
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

        # Jump
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
            elif any((self.on_surface['left'], self.on_surface['right'])):
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        self.collision('vertical')

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4),
                                 (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4),
                                (2, self.rect.height / 2))

        colide_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_surface['floor'] = floor_rect.collidelist(colide_rects) >= 0
        self.on_surface['right'] = right_rect.collidelist(colide_rects) >= 0
        self.on_surface['left'] = left_rect.collidelist(colide_rects) >= 0

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite == self :
                continue
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else:  # vertical
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()


class Objet(pygame.sprite.Sprite):
    def __init__(self, owner, color, groups, players):
        super().__init__(groups)
        self.owner = owner
        self.color = color
        self.players = players

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (10, 10), 10)
        self.rect = self.image.get_rect(topleft=(0, 0))

    def update(self, dt):
        for player in self.players:
            if player.role == self.owner:
                self.rect.center = player.rect.center
                break
            if player.role != self.owner and self.rect.colliderect(player.rect):
                self.owner = player.role
                break
