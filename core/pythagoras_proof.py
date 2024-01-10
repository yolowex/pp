from core.common.names import *
from core.event_holder import EventHolder
import core.common.resources as cr
from core.common.utils import *

def drag_point_rect(point: Vector2,size:float):
    return FRect(point.x - size / 2,point.y - size / 2,size,size)

def set_drag_cursor(current_cursor,mouse_held):
    if mouse_held :
        if pg.mouse.get_visible():
            pg.mouse.set_visible(False)
    else :
        if not pg.mouse.get_visible() :
            pg.mouse.set_visible(True)

        if current_cursor != pg.SYSTEM_CURSOR_HAND :
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

class PythagorasProof:
    def __init__(self):
        self.drag_point_size = 10
        self.p1 = self.p2 = self.p3 = self.p_center = Vector2()
        self.init_points()


    def init_points(self):
        length = cr.screen.get_width() * 0.28
        self.p1 = cr.sc_center()
        self.p2 = get_rotated_point(self.p1, length, -45)
        self.p3 = get_rotated_point(self.p1, length, -135)
        # self.p_center = find_triangle_center(self.p1,self.p2,self.p3)

        center_triangle(self.p1,self.p2,self.p3,cr.sc_center())


    def render_drag_circles(self):
        pg.draw.circle(
            cr.screen,
            Color(220,80,45),
            self.p2,
            self.drag_point_size,
        )
        pg.draw.circle(
            cr.screen,
            Color(220,80,45),
            self.p3,
            self.drag_point_size,
        )

    def render_rectangle(self):

        pg.draw.lines(
            cr.screen,
            "black",
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
        self.render_drag_circles()

    def check_drag_circles(self):
        mr = cr.event_holder.mouse_rect
        # current mouse cursor
        cc = pg.mouse.get_cursor()
        mc = cr.event_holder.mouse_held_keys[0]


        if mr.colliderect(drag_point_rect(self.p2,self.drag_point_size)):
            set_drag_cursor(cc,mc)

        elif mr.colliderect(drag_point_rect(self.p3,self.drag_point_size)):
            set_drag_cursor(cc,mc)

        else:
            if not pg.mouse.get_visible() :
                pg.mouse.set_visible(True)

            if cc != pg.SYSTEM_CURSOR_ARROW:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)



    def check_events(self):
        if cr.event_holder.window_resized:
            self.on_screen_resize()

        self.check_drag_circles()

    def on_screen_resize(self):
        self.init_points()