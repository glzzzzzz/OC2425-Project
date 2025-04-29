from config import *
from level import Level
from pytmx.util_pygame import load_pygame
from network import Network
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
        # Give bomb to correct player
        for p in self.level.players:
            p.has_bomb = (p.role == self.level.bombe.owner)

        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Send position and bomb owner: "x,y|owner"
            msg = f"{player1.rect.x},{player1.rect.y}|{self.level.bombe.owner}"
            reply = n.send(msg)

            if reply:
                pos_part, owner_part = reply.split("|")
                x2, y2 = map(int, pos_part.split(","))
                player2.rect.topleft = (x2, y2)
                # Update bomb owner locally
                if owner_part != self.level.bombe.owner:
                    self.level.bombe.owner = owner_part
                    # update has_bomb flags
                    for p in self.level.players:
                        p.has_bomb = (p.role == owner_part)

            # Update & draw
            self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    Game().run()