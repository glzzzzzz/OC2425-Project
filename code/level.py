from config import *
from sprite import Sprite
from player import Player, Objet

class Monster(Player):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, groups, collision_sprites)
        self.image.fill('green')

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        
        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1

            if keys[pygame.K_LEFT]:
                input_vector.x -= 1
            #norme de 1
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_UP]:
            self.jump = True

class Zombie(Player):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, groups, collision_sprites)
        self.image.fill('blue')

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        
        if not self.timers['wall jump'].active:
            if keys[pygame.K_d]:
                input_vector.x += 1

            if keys[pygame.K_a]:
                input_vector.x -= 1
            #norme de 1
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_w]:
            self.jump = True

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        #groupes de sprites
        self.all_sprites = pygame.sprite.Group()

        self.collision_sprites = pygame.sprite.Group()

        self.players = []


        self.setup (tmx_map)
    
    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('terrain').tiles():
            Sprite((x*32,y*32-100), surf, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Object'): 
            if obj.name =='monster':
                player1 = Player((obj.x, obj.y-100), self.all_sprites, self.collision_sprites, "chat")
                self.players.append(player1)
            if obj.name == 'zombie':
                player2 = Player((obj.x, obj.y-100), self.all_sprites, self.collision_sprites, "souris")
                self.players.append(player2)
            tmx_map.get_layer_by_name('Object')
            
        self.bombe = Objet("chat", (255,255,0), self.all_sprites, self.players)
    def run(self, dt):
        self.display_surface.fill('black')
        
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)