import pygame

from settings import *


class Button:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text

    def draw(
        self,
        screen,
        font
    ):

        mouse = pygame.mouse.get_pos()

        hover = self.rect.collidepoint(
            mouse
        )

        # =====================
        # BUTTON SHADOW
        # =====================

        if hover:
            shadow_offset = 2
        else:
            shadow_offset = 4

        shadow_rect = pygame.Rect(
            self.rect.x + shadow_offset,
            self.rect.y + shadow_offset + 2,
            self.rect.width,
            self.rect.height
        )

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            shadow_rect,
            border_radius=15
        )

        # =====================
        # BUTTON BACKGROUND
        # =====================

        color = (
            (80, 150, 255)
            if hover
            else
            (52, 152, 219)
        )

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=15
        )

        # =====================
        # BUTTON BORDER
        # =====================

        border_color = (
            (100, 180, 255)
            if hover
            else (255, 255, 255)
        )

        pygame.draw.rect(
            screen,
            border_color,
            self.rect,
            3,
            border_radius=15
        )

        # =====================
        # BUTTON HIGHLIGHT
        # =====================

        if hover:
            highlight_surface = pygame.Surface(
                (self.rect.width, self.rect.height // 3),
                pygame.SRCALPHA
            )
            pygame.draw.rect(
                highlight_surface,
                (255, 255, 255, 40),
                (0, 0, self.rect.width, self.rect.height // 3),
                border_radius=15
            )
            screen.blit(
                highlight_surface,
                self.rect.topleft
            )

        # =====================
        # TEXT
        # =====================

        text_surface = font.render(
            self.text,
            True,
            WHITE
        )

        screen.blit(
            text_surface,
            (
                self.rect.centerx
                -
                text_surface.get_width() // 2,
                self.rect.centery
                -
                text_surface.get_height() // 2
            )
        )

    def clicked(
        self,
        event
    ):

        return (
            event.type
            ==
            pygame.MOUSEBUTTONDOWN
            and
            self.rect.collidepoint(
                event.pos
            )
        )