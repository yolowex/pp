from core.common.names import *
import core.common.resources as cr


class Button:
    def __init__(
        self,
        content_surface: Surface,
        normal_color,
        hover_color,
        stick_top_left=False,
        stick_top_right=False,
        stick_bottom_left=False,
        stick_bottom_right=False,
        callback=None,
    ):
        self.rect = content_surface.get_frect()
        self.content_surface = content_surface
        self.hover_surface = pg.transform.scale(
            self.content_surface, Vector2(self.content_surface.get_size()) * 1.1
        )
        self.callback = callback
        self.is_hovered = False

        self.stick_top_left = stick_top_left
        self.stick_top_right = stick_top_right
        self.stick_bottom_left = stick_bottom_left
        self.stick_bottom_right = stick_bottom_right

        self.update_position()

    def update_position(self):
        padding = 5
        if self.stick_top_left:
            self.rect.topleft = (padding, padding)

        elif self.stick_top_right:
            self.rect.topright = (
                pg.display.get_surface().get_width() - padding,
                padding,
            )
        elif self.stick_bottom_left:
            self.rect.bottomleft = (
                padding,
                pg.display.get_surface().get_height() - padding,
            )
        elif self.stick_bottom_right:
            self.rect.bottomright = (
                pg.display.get_surface().get_width() - padding,
                pg.display.get_surface().get_height() - padding,
            )

    def render(self, screen):
        if cr.event_holder.mouse_held_keys[0] and self.is_hovered:
            return

        surface = self.content_surface
        if self.is_hovered:
            surface = self.hover_surface

        content_rect = surface.get_rect(center=self.rect.center)
        screen.blit(surface, content_rect)

    def check_events(self):
        for event in cr.event_holder.events:
            if event.type == pg.MOUSEMOTION:
                self.is_hovered = self.rect.collidepoint(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered and self.callback:
                    self.callback()
