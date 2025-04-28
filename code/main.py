from config import *
from level import Level
from pytmx.util_pygame import load_pygame
from network import Network
from player import Player, Objet
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('potato')
        self.clock = pygame.time.Clock()

        # Load maps
        self.tmx_maps = {0: load_pygame(r'OC2425-Project/data/background/test_map.tmx')}
        self.level = Level(self.tmx_maps[0])

    @staticmethod
    def read_pos(string):
        """Convert 'x,y' into (int(x), int(y))"""
        x, y = string.split(",")
        return int(x), int(y)

    @staticmethod
    def make_pos(tup):
        """Convert (x, y) into 'x,y'"""
        return f"{int(tup[0])},{int(tup[1])}"

    def run(self):
        n = Network()

        player1 = self.level.players[0]
        player1.role = n.getRole()

        startPos = n.getPos()
        player1.rect.x = int(startPos[0])
        player1.rect.y = int(startPos[1])

        player2 = self.level.players[1]
        player2.role = 'souris' if player1.role == 'chat' else 'chat'

        while True:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # --- Communication Réseau ---
            my_pos = Game.make_pos((player1.rect.x, player1.rect.y))
            reply_pos = n.send(my_pos)

            if reply_pos:
                p2pos = Game.read_pos(reply_pos)
                player2.rect.x = int(p2pos[0])
                player2.rect.y = int(p2pos[1])

            # --- Update et Draw ---
            self.level.run(dt)  # <<< Garde run(dt) ici, pas update !
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
