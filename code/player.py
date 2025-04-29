from config import *
from timer import Timer
import pygame
from pygame.math import Vector2 as vector

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, role, players, bombe):
        super().__init__(groups)
        self.role = role
        self.bombe = bombe
        self.has_bomb = False

        self.frames = []
        frame_count = 3  
        for i in range(frame_count):
            if self.role == "chat":
                path = f'OC2425-Project/data/angel/big_zombie_idle_anim_f{i}.png'
            else:
                path = f'OC2425-Project/data/monster/big_demon_idle_anim_f{i}.png'
            image = pygame.image.load(path).convert_alpha()
            self.frames.append(image)

        self.frame_index = 0
        self.animation_speed = 8  # Images par seconde
        self.base_image = self.frames[0]
        self.image = self.base_image 

        self.base_image = self.image
        self.facing_right = True  # Direction initiale

        self.players = players
        self.colliding_with = None
        self.can_swap = True

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.direction = vector(0, 0)
        self.speed = 200
        self.gravity = 1000
        self.jump = False
        self.jump_height = 300
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.timers = {
            'wall jump': Timer(400),
            'bomb cooldown': Timer(3000)  
        }

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.base_image = self.frames[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        iv = vector(0, 0)
        if not self.timers['wall jump'].active:
            if self.role == 'chat':
                if keys[pygame.K_d]: iv.x += 1
                if keys[pygame.K_a]: iv.x -= 1
            else:
                if keys[pygame.K_RIGHT]: iv.x += 1
                if keys[pygame.K_LEFT]: iv.x -= 1
            self.direction.x = iv.normalize().x if iv.length_squared() else 0
        if self.role == 'chat':
            if keys[pygame.K_w]: self.jump = True
        else:
            if keys[pygame.K_UP]: self.jump = True

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])):
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')
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
        floor = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2))
        left = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), (2, self.rect.height / 2))
        rects = [s.rect for s in self.collision_sprites]
        self.on_surface['floor'] = floor.collidelist(rects) >= 0
        self.on_surface['right'] = right.collidelist(rects) >= 0
        self.on_surface['left'] = left.collidelist(rects) >= 0

    def collision(self, axis):
        for spr in self.collision_sprites:
            if spr is self:
                continue
            if isinstance(spr, Player) and spr.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    if self.old_rect.right <= spr.old_rect.left:
                        self.rect.right = spr.rect.left
                    elif self.old_rect.left >= spr.old_rect.right:
                        self.rect.left = spr.rect.right
                    self.direction.x = 0
                else:
                    if self.old_rect.bottom <= spr.old_rect.top:
                        self.rect.bottom = spr.rect.top
                    elif self.old_rect.top >= spr.old_rect.bottom:
                        self.rect.top = spr.rect.bottom
                    self.direction.y = 0
                continue
            if spr.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    if self.rect.left <= spr.rect.right and self.old_rect.left >= spr.old_rect.right:
                        self.rect.left = spr.rect.right
                    if self.rect.right >= spr.rect.left and self.old_rect.right <= spr.old_rect.left:
                        self.rect.right = spr.rect.left
                else:
                    if self.rect.bottom >= spr.rect.top and self.old_rect.bottom <= spr.old_rect.top:
                        self.rect.bottom = spr.rect.top
                    if self.rect.top <= spr.rect.bottom and self.old_rect.top >= spr.old_rect.bottom:
                        self.rect.top = spr.rect.bottom
                    self.direction.y = 0
        touching = any(isinstance(s, Player) and s is not self and self.rect.colliderect(s.rect) for s in self.collision_sprites)
        if not touching:
            self.can_swap = True

    def update_timers(self):
        for t in self.timers.values():
            t.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
        # Flip horizontal selon la direction
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        self.image = pygame.transform.flip(self.base_image, not self.facing_right, False)

class Objet(pygame.sprite.Sprite):
    def __init__(self, owner, color, groups, players):
        super().__init__(groups)
        self.owner = owner
        self.color = color
        self.players = players

        self.frames = []
        frame_count = 3
        for i in range(frame_count):
            path = f'OC2425-Project/data/bombe/bombe{i}.png'
            image = pygame.image.load(path).convert_alpha()
            self.frames.append(image)

        self.frame_index = 0
        self.animation_speed = 8  # images par seconde

        self.base_image = self.frames[0]
        self.image = self.base_image
        self.rect = self.image.get_rect()

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.base_image = self.frames[int(self.frame_index)]
        self.image = self.base_image

    def update(self, dt):
        for p in self.players:
            if p.role == self.owner and p.has_bomb:
                offset = pygame.math.Vector2(10, 0) if p.facing_right else pygame.math.Vector2(-10, 0)
                self.rect.center = p.rect.center + offset
                break
        self.animate(dt)