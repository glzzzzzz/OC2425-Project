from config import *
from level import Level
from pytmx.util_pygame import load_pygame
from network import Network
from timer import Timer
from random import randint
import pygame
import pytmx

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('potato')
        self.clock = pygame.time.Clock()

        # Load maps
        self.tmx_maps = {0: load_pygame(r'OC2425-Project/data/background/test_map.tmx')}
        self.level = Level(self.tmx_maps[0])

        # Explosion-related
        self.bomb_explosion_timer = Timer(randint(BOMB_MIN_TIMER, BOMB_MAX_TIMER))
        self.bomb_explosion_timer.activate()
        self.game_frozen = False
        self.winner_message = ""

        # Font for winner message
        self.font = pygame.font.SysFont(None, 72)

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

            # Gérer le timer d'explosion
            if not self.game_frozen:
                self.bomb_explosion_timer.update()
                if not self.bomb_explosion_timer.active:
                    # Bombe a explosé
                    bomb_holder = next((p for p in self.level.players if p.has_bomb), None)
                    if bomb_holder:
                        self.winner_message = f"{'Joueur 1' if bomb_holder.role == 'souris' else 'Joueur 2'} a gagné !"
                    else:
                        self.winner_message = "Personne n'avait la bombe !"
                    self.game_frozen = True

            # Réseau
            if not self.game_frozen:
                msg = f"{player1.rect.x},{player1.rect.y}|{self.level.bombe.owner}"
                reply = n.sendRecieve(msg)
                if reply:
                    pos_part, owner_part = reply.split("|")
                    x2, y2 = map(int, pos_part.split(","))
                    player2.rect.topleft = (x2, y2)
                    if owner_part != self.level.bombe.owner:
                        self.level.bombe.owner = owner_part
                        for p in self.level.players:
                            p.has_bomb = (p.role == owner_part)

            # Update & draw
            self.display_surface.fill((0, 0, 0))


            if not self.game_frozen:
                self.level.run(dt)
            else:
                self.level.all_sprites.draw(self.display_surface)

                text_surface = self.font.render(self.winner_message, True, (255, 255, 0))
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(text_surface, text_rect)

            pygame.display.update()

if __name__ == '__main__':
    Game().run()