from core.common.names import *
from core.event_holder import EventHolder
import core.common.resources as cr
from core.common.utils import *

class PythagorasProof:
    def __init__(self):
        self.p1 = self.p2 = self.p3 = self.p_center = Vector2()
        self.init_points()


    def init_points(self):
        length = cr.screen.get_width() * 0.28
        self.p1 = cr.sc_center()
        self.p2 = get_rotated_point(self.p1, length, -45)
        self.p3 = get_rotated_point(self.p1, length, -135)
        # self.p_center = find_triangle_center(self.p1,self.p2,self.p3)

        center_triangle(self.p1,self.p2,self.p3,cr.sc_center())

    def render_rectangle(self):

        pg.draw.lines(
            cr.screen,
            "white",
            True,
            points = [
                self.p1,
                self.p2,
                self.p3,
            ]
            ,
            width= 2
        )

    def render(self):
        self.render_rectangle()

    def check_events(self):
        if cr.event_holder.window_resized:
            self.on_screen_resize()

    def on_screen_resize(self):
        self.init_points()