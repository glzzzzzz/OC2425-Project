from config import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from network import Network
class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        pygame.display.set_caption('potato')

        self.clock = pygame.time.Clock()

        self.tmx_maps = {0: load_pygame(r'../data/background/test_map.tmx')}
        
        self.level = Level(self.tmx_maps[0])

    #@staticmethod
    #def read(str):
     #   str = str.split(",")
      #  return int(str[0]),int(str[1])
    
    #@staticmethod
    #def make_pos(tup):
     #   return str(tup[0]) + "," + str(tup[1])
    
    def run(self):

        #n = Network()
        #startPos = Game.read(n.getPos())

        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()

            self.level.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()

