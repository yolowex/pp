import os

from core.common.names import *
from core.event_holder import EventHolder
import core.common.resources as cr
from core.common.utils import *
from core.button import Button


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
        self.drag_point_size = 7
        self.p1 = self.p2 = self.p3 = self.p_center = Vector2()
        self.init_points()
        self.locked_point_id: Optional[int] = None
        self.locked_center = False
        self.render_exec_stack: list[str] = []
        self.font = pg.font.SysFont("sans", 18)
        self.distance_scale = 0.02841
        self.reset_button_image = pg.image.load(
            os.getcwd() + "/assets/ui_buttons/reset.png"
        )
        self.reset_button_image = pg.transform.scale(self.reset_button_image, [50, 50])
        self.reset_button = Button(
            self.reset_button_image,
            "black",
            "gray",
            stick_top_left=True,
            callback=self.reset,
        )
        self.reset()

    def reset(self):
        self.triangle_center = cr.sc_center()
        self.drag_point_size = 7
        self.p1 = self.p2 = self.p3 = self.p_center = Vector2()
        self.init_points()
        self.locked_point_id: Optional[int] = None
        self.locked_center = False
        self.render_exec_stack: list[str] = []
        self.font = self.font
        self.distance_scale = 0.033332

    def init_points(self):
        length = cr.screen.get_height() * 0.25
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

    def get_line_name(self, p1, p2):
        if p1 == self.p1 and p2 == self.p2:
            return "B"
        if p1 == self.p2 and p2 == self.p3:
            return "C"
        if p1 == self.p3 and p2 == self.p1:
            return "A"

    def render_formula(self):
        dest_a = round(self.p3.distance_to(self.p1) * self.distance_scale, 2)
        dest_b = round(self.p1.distance_to(self.p2) * self.distance_scale, 2)
        dest_c = round(self.p3.distance_to(self.p2) * self.distance_scale, 2)

        dest2_a = round((self.p3.distance_to(self.p1) * self.distance_scale) ** 2, 2)
        dest2_b = round((self.p1.distance_to(self.p2) * self.distance_scale) ** 2, 2)
        dest2_c = round((self.p3.distance_to(self.p2) * self.distance_scale) ** 2, 2)

        space = lambda x: " " * x

        formula_text = (
            f"A\u00B2 + B\u00B2 = C\u00B2"
            + space(5)
            + "=>"
            + space(5)
            + f"{dest_a}\u00B2 + {dest_b}\u00B2 = {dest_c}\u00B2"
            + space(5)
            + "=>"
            + space(5)
            + f"\u221A{dest2_a} + \u221A{dest2_b} = \u221A{dest2_c}"
        )
        surface_text = self.font.render(formula_text, True, "black")

        cr.screen.blit(
            surface_text,
            [
                cr.screen.get_width() / 2 - surface_text.get_width() / 2,
                cr.screen.get_height() - surface_text.get_height() - 5,
            ],
        )

    def render_square_polygon(self, p1: Vector2, p2: Vector2, direction=1):
        poly = create_square_from_line(p1, p2, direction=direction)
        poly_center = get_polygon_center(poly)
        line_center = get_line_center(p1, p2)
        line_name = self.get_line_name(p1, p2)

        poly_text = self.font.render(
            f"{round((p1.distance_to(p2)*self.distance_scale)**2,2)}"[::-1].zfill(6)[
                ::-1
            ],
            True,
            "black",
            "white",
        )

        line_text = self.font.render(
            f"{line_name}: {round((p1.distance_to(p2)*self.distance_scale),2)}"[
                ::-1
            ].zfill(4)[::-1],
            True,
            "black",
            "white",
        )

        pg.draw.polygon(cr.screen, "black", points=poly, width=2)

        cr.screen.blit(
            poly_text,
            (
                poly_center.x - poly_text.get_width() / 2,
                poly_center.y - poly_text.get_height() / 2,
            ),
        )

        draw_border(
            cr.screen,
            poly_text,
            "gray",
            1,
            Vector2(
                poly_center.x - poly_text.get_width() / 2,
                poly_center.y - poly_text.get_height() / 2,
            ),
        )

        cr.screen.blit(
            line_text,
            (
                line_center.x - line_text.get_width() / 2,
                line_center.y - line_text.get_height() / 2,
            ),
        )

        draw_border(
            cr.screen,
            line_text,
            "gray",
            1,
            Vector2(
                line_center.x - line_text.get_width() / 2,
                line_center.y - line_text.get_height() / 2,
            ),
        )

    def render_polygons(self):
        self.render_square_polygon(self.p1, self.p2, 1)
        self.render_square_polygon(self.p2, self.p3)
        self.render_square_polygon(self.p3, self.p1)

    def render(self):
        self.render_polygons()
        # self.render_rectangle()
        self.render_circles()
        self.render_formula()
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

            self.triangle_center.xy = find_triangle_center(self.p1, self.p2, self.p3)

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
            set_drag_cursor(cc, mh)
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
        self.process_reset_button()

    def on_screen_resize(self):
        # self.init_points()
        self.triangle_center = cr.sc_center()
        self.recenter_points()
        self.reset_button.update_position()

    def process_reset_button(self):
        # a process even is both a check and a render method.
        # they use render_exec_stack to render things in the appropriate time and
        # are called in check_events
        self.reset_button.check_events()
        self.render_exec_stack.append("self.reset_button.render(cr.screen)")
