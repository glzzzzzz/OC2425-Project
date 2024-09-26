import pygame
import sys
import random
 
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FRAMES_PER_SECOND = 40
 
catch = False
 
class Player :
    names_players = []
 
    def __init__(self, x, y, width, height, x_velocity, role, color) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_velocity = x_velocity
        self.y_gravity = 2
        self.jump_height = self.y_velocity = 20
        self.jumping = False
        self.role = role
        self.color = color
        self.affect_gravity = True
        Player.names_players.append(self)
   
    def left(self) :
        self.x -= self.x_velocity
   
    def right(self) :
        self.x += self.x_velocity
 
    def gravity(self) :
        if self.affect_gravity :
            if self.y < WINDOW_HEIGHT - self.height :
 
                self.y += 5
 
 
 
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
   
    def collision_plateforme(self, plateforme):
        player_rect = self.get_rect()
        plateforme_rect = plateforme.get_rect()
        if player_rect.colliderect(plateforme_rect):
            # Collision par le dessus : Le joueur tombe sur la plateforme
            if player_rect.bottom <= plateforme_rect.top + self.y_velocity or self.y > plateforme.y:
                self.y = plateforme.y - self.height  # Place le joueur sur le dessus de la plateforme
                self.jumping = False  # Arrête le s8aut
                self.affect_gravity = False
                self.y_velocity = self.jump_height  # Réinitialise la vélocité du saut
           
            # Empêcher les joueurs de passer à travers la plateforme par le bas ou les côtés
            elif player_rect.top < plateforme_rect.bottom and player_rect.bottom > plateforme_rect.bottom:
                # On évite de forcer une position en cas de collision sur les côtés ou en dessous
                pass
       
class Objet :
    def __init__(self, owner, size, color) :
        self.owner = owner
        self.size = size
        self.x = 0
        self.y = 0
        self.color = color
 
    def follow(self) :
        for player in Player.names_players :
            if player.role == self.owner :
                self.x = player.x + player.width/2 - self.size/2
                self.y = player.y + player.height/2 - self.size/2
 
class Plateforme :
    name_plateforme = []
 
    def __init__(self, x, y, height, width, color) :
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        Plateforme.name_plateforme.append(self)
 
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
 
 
plateforme1 = Plateforme(900,WINDOW_HEIGHT-120,10, 500,(0,0,100))
plateforme2 = Plateforme(200,WINDOW_HEIGHT-240,10, 400,(0,0,100))
sol = Plateforme(0,WINDOW_HEIGHT-20,20, WINDOW_WIDTH,(0,0,100))
bombe = Objet("chat", 15, (10,10,10))
player1 = Player(200, 200, 30, 40, 25, "chat", (100,0,0))
player2 = Player(1000, 200, 30, 40, 25, "souris",(0,100,0))
 
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
 
while True:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
    # store keys pressed
    keys = pygame.key.get_pressed()
 
   
    #player 1
    if keys[pygame.K_LEFT] and player1.x>0:
        player1.left()
    if keys[pygame.K_RIGHT] and player1.x < WINDOW_WIDTH - player1.width :
        player1.right()
    if keys[pygame.K_UP] and not player1.jumping :
        player1.jumping = True
 
    #player 2
    if keys[pygame.K_a] and player2.x>0:
        player2.left()
    if keys[pygame.K_d] and player2.x < WINDOW_WIDTH - player2.width :
        player2.right()
    if keys[pygame.K_w] and not player2.jumping :
        player2.jumping = True
   
    if keys[pygame.K_ESCAPE] :
        pygame.quit()
 
    screen.fill((0,0,0))
 
    if catch :
        pygame.time.delay(500)
        catch = False
 
    if player1.get_rect().colliderect(player2.get_rect()):
        if player1.role == "chat" :
            player1.role = "souris"
            player2.role = "chat"
        elif player1.role == "souris" :
            player1.role = "chat"
            player2.role = "souris"
 
        player1.x = random.randint(0, WINDOW_WIDTH/2 - player1.width)
        player2.x = random.randint(WINDOW_WIDTH/2 - player1.width, WINDOW_WIDTH - player2.width)
        player1.y = random.randint(0, WINDOW_HEIGHT - player1.height)
        player2.y = random.randint(0, WINDOW_HEIGHT - player2.height)
 
        catch = True
 
    for player in Player.names_players :
        player.affect_gravity = True
        if player.jumping :
            player.y -= player.y_velocity
            player.y_velocity -= player.y_gravity
            if player.y_velocity < - player.jump_height :
                player.jumping = False
                player.y_velocity = player.jump_height
        elif player.y < WINDOW_HEIGHT - player.width :
            player.gravity()
        pygame.draw.rect(screen, player.color,(player.x,player.y,player.width,player.height))
        for plateforme in Plateforme.name_plateforme :
            player.collision_plateforme(plateforme)
   
    bombe.follow()
    pygame.draw.rect(screen, bombe.color,(bombe.x,bombe.y,bombe.size,bombe.size))
       
    for plateforme in Plateforme.name_plateforme :
        pygame.draw.rect(screen, plateforme.color,(plateforme.x,plateforme.y,plateforme.width,plateforme.height))
   
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
    
