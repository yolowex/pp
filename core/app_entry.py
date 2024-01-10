from core.common.names import *
from core.event_holder import EventHolder
from core.pythagoras_proof import PythagorasProof
import core.common.resources as cr

class AppEntry:
    def __init__(self):
        cr.screen = pg.display.set_mode([800,600],pg.RESIZABLE)
        cr.event_holder = EventHolder()
        self.pp = PythagorasProof()

    def render(self):
        cr.screen.fill("white")
        self.pp.render()
        pg.display.update()

    def check_events(self):
        cr.event_holder.get_events()
        self.pp.check_events()

    def run(self):
        while not cr.event_holder.should_quit:
            self.check_events()
            self.render()