from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, func=None, repeat=False):
        self.duration = duration      # en millisecondes
        self.func = func
        self.start_time = 0
        self.active = False
        self.repeat = repeat
            
    def activate(self):
        if not self.active: 
            self.active = True
            self.start_time = get_ticks()
            
               
    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        current_time = get_ticks()
        if not self.active:
            return
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()

    def get_time_left(self):
        """Retourne le temps restant en millisecondes (>= 0)."""
        if not self.active:
            return 0
        remaining = self.duration - (get_ticks() - self.start_time)
        return max(0, remaining)
