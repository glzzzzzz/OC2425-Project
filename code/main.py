from config import *
from level import Level
from pytmx.util_pygame import load_pygame
from network import Network
from timer import Timer
from random import randint
import pygame
import pytmx
from pathlib import Path
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('potato')
        self.clock = pygame.time.Clock()
        
        
        #Music
        pygame.mixer.music.load('../data/Sons/music.mp3') 
        pygame.mixer.music.play(-1)

        # Load maps
        self.tmx_maps = {0: load_pygame('../data/background/test_map.tmx')}
        self.level = Level(self.tmx_maps[0])

        # Explosion-related
        self.bomb_explosion_timer = Timer(BOMB_TIMER)
        self.winner_message = ""

        self.game_over = False
        self.game_over_timer = 0

        # Font for winner message
        self.font = pygame.font.SysFont(None, 72)
        self.timer_font = pygame.font.SysFont(None, 36)

    def run(self):
        n = Network()

        # Setup local player
        player1 = self.level.players[0]
        player1.role = n.getRole()
        start_x, start_y = n.getPos()
        player1.rect.topleft = (start_x, start_y)

        # Assign remote role
        player2 = self.level.players[1]
        player2.role = 'souris' if player1.role == 'chat' else 'chat'

        # Initialize bomb owner from server
        self.level.bombe.owner = n.getBombOwner()
        for p in self.level.players:
            p.has_bomb = (p.role == self.level.bombe.owner)

        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Réseau
            msg = f"{player1.rect.x},{player1.rect.y}|{self.level.bombe.owner}"
            reply = n.sendRecieve(msg)
            ready, pos_part, owner_part = reply.split("|")
            if ready == 'True' :
                ready = True
            else :
                ready = False
            x2, y2 = map(int, pos_part.split(","))
            player2.rect.topleft = (x2, y2)
            if owner_part != self.level.bombe.owner:
                self.level.bombe.owner = owner_part
                for p in self.level.players:
                    p.has_bomb = (p.role == owner_part)

            # Update & draw
            self.display_surface.fill((0, 0, 0))


            if ready and not self.game_over:
                self.level.run(dt)
                self.bomb_explosion_timer.activate()

                # Gérer le timer d'explosion
                self.bomb_explosion_timer.update()
                if not self.bomb_explosion_timer.active:
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()
                    bomb_holder = next((p for p in self.level.players if p.has_bomb), None)
                    if bomb_holder:
                        self.winner_message = f"{'Joueur 1' if bomb_holder.role == 'souris' else 'Joueur 2'} a gagné !"
                    else:
                        self.winner_message = "Personne n'avait la bombe !"

            # Afficher le timer s'il y a encore du temps
            if not self.game_over:
                ms_left = self.bomb_explosion_timer.get_time_left()
                seconds = ms_left / 1000
                timer_text = f"Temps avant explosion : {seconds:.1f}s"
                text_surf = self.timer_font.render(timer_text, True, (255, 255, 255))
                self.display_surface.blit(text_surf, (10, 10))

            # Afficher le message de fin s’il y a lieu
            if self.game_over:
                text_surface = self.font.render(self.winner_message, True, (255, 255, 0))
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(text_surface, text_rect)

                if pygame.time.get_ticks() - self.game_over_timer > 3000:
                    pygame.quit()
                    return
            else:
                self.level.all_sprites.draw(self.display_surface)

            pygame.display.update()

if __name__ == '__main__':
    Game().run()