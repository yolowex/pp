from core.common.names import *
from core.event_holder import EventHolder
import core.common.resources as cr
from core.common.utils import *


def drag_point_rect(point: Vector2, size: float):
    return FRect(point.x - size / 2, point.y - size / 2, size, size)


def set_drag_cursor(current_cursor, mouse_held):
    if mouse_held:
        if pg.mouse.get_visible():
            pg.mouse.set_visible(False)

    else:
        if not pg.mouse.get_visible():
            pg.mouse.set_visible(True)

        if current_cursor != pg.SYSTEM_CURSOR_HAND:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)


class PythagorasProof:
    def __init__(self):
        self.triangle_center = cr.sc_center()
        self.drag_point_size = 10
        self.p1 = self.p2 = self.p3 = self.p_center = Vector2()
        self.init_points()
        self.locked_point_id: Optional[int] = None
        self.locked_center = False
        self.render_exec_stack: list[str] = []

    def init_points(self):
        length = cr.screen.get_width() * 0.22
        self.p1 = cr.sc_center()
        self.p2 = get_rotated_point(self.p1, length, -45)
        self.p3 = get_rotated_point(self.p1, length, -135)
        # self.p_center = find_triangle_center(self.p1,self.p2,self.p3)

        center_triangle(self.p1, self.p2, self.p3, self.triangle_center)

    def recenter_points(self):
        center_triangle(self.p1, self.p2, self.p3, self.triangle_center)

    def get_locked_point(self):
        if self.locked_point_id == 2:
            return self.p2

        if self.locked_point_id == 3:
            return self.p3

    def get_locked_point_line(self):
        if self.locked_point_id == 2:
            return resize_line(self.p2, self.p1, 100)

        if self.locked_point_id == 3:
            return resize_line(self.p3, self.p1, 100)

    def set_locked_point(self, point: Vector2 = None):
        if point == self.p2:
            self.locked_point_id = 2

        elif point == self.p3:
            self.locked_point_id = 3
        else:
            self.locked_point_id = point  # because it would be None

    def render_circles(self):
        pg.draw.circle(
            cr.screen,
            Color(220, 80, 45),
            self.p2,
            self.drag_point_size,
        )
        pg.draw.circle(
            cr.screen,
            Color(220, 80, 45),
            self.p3,
            self.drag_point_size,
        )
        pg.draw.circle(
            cr.screen,
            Color(45, 80, 220),
            self.triangle_center,
            self.drag_point_size,
        )

    def render_rectangle(self):
        pg.draw.lines(
            cr.screen,
            "black",
            True,
            points=[
                self.p1,
                self.p2,
                self.p3,
            ],
            width=2,
        )

    def render(self):
        self.render_rectangle()
        self.render_circles()
        while len(self.render_exec_stack) != 0:
            # coolest shit I've written ever
            exec(self.render_exec_stack[0])
            self.render_exec_stack.pop(0)

    def check_drag_circles(self):
        mr = cr.event_holder.mouse_rect
        # current mouse cursor
        cc = pg.mouse.get_cursor()
        mh = cr.event_holder.mouse_held_keys[0]
        mc = cr.event_holder.mouse_pressed_keys[0]
        m_released = cr.event_holder.mouse_released_keys[0]

        if m_released and self.locked_point_id is not None:
            self.set_locked_point()
            self.recenter_points()

        if m_released and self.locked_center:
            self.locked_center = False

        new_point = None
        if self.locked_point_id is not None:
            locked_line = self.get_locked_point_line()
            locked_point = self.get_locked_point()

            new_point = closest_point_on_line(
                locked_line[0], locked_line[1], cr.event_holder.mouse_pos
            )

            locked_point.xy = new_point

            self.triangle_center.xy = find_triangle_center(
                self.p1,
                self.p2,
                self.p3
            )

        if self.locked_center:
            self.triangle_center.xy = cr.event_holder.mouse_pos
            self.recenter_points()

        if mr.colliderect(drag_point_rect(self.p2, self.drag_point_size)):
            set_drag_cursor(cc, mh)
            if mc:
                self.set_locked_point(self.p2)

        elif mr.colliderect(drag_point_rect(self.p3, self.drag_point_size)):
            set_drag_cursor(cc, mh)
            if mc:
                self.set_locked_point(self.p3)

        else:
            if not pg.mouse.get_visible():
                pg.mouse.set_visible(True)

            if cc != pg.SYSTEM_CURSOR_ARROW:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if mr.colliderect(drag_point_rect(self.triangle_center, self.drag_point_size)):
            set_drag_cursor(cc,mh)
            if mc:
                self.locked_center = True


        if cr.event_holder.should_render_debug and new_point is not None:
            self.render_exec_stack.append(
                f"""
pg.draw.line(
    cr.screen,
    "green",
    {str(new_point)},
    {str(cr.event_holder.mouse_pos)},
)
"""
            )
            self.render_exec_stack.append(
                """
pg.draw.line(
    cr.screen,
    "green",
    self.get_locked_point_line()[0],
    self.get_locked_point_line()[1],
)
"""
            )

    def check_events(self):
        if cr.event_holder.window_resized:
            self.on_screen_resize()

        self.check_drag_circles()

    def on_screen_resize(self):
        # self.init_points()
        self.triangle_center = cr.sc_center()
        self.recenter_points()
