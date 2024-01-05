from core.common.names import *
from core.event_holder import EventHolder

class AppEntry:
    def __init__(self):
        self.event_holder = EventHolder()
        self.screen = pg.display.set_mode([800,600],pg.RESIZABLE)

    def render(self):
        self.screen.fill("black")


        pg.display.update()

    def check_events(self):
        self.event_holder.get_events()

    def run(self):
        while not self.event_holder.should_quit:
            self.check_events()
            self.render()