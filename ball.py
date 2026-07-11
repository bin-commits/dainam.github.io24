import pygame

from settings import *


class Ball:

    def __init__(self, color_id):

        self.color_id = color_id

    @property
    def color(self):

        return COLORS[self.color_id]

    def draw(
        self,
        screen,
        x,
        y
    ):

        x = int(x)
        y = int(y)

        # =====================
        # GLOW EFFECT
        # =====================

        for i in range(3, 0, -1):
            alpha = int(30 * (1 - i / 3))
            glow_surface = pygame.Surface(
                ((BALL_RADIUS + i * 4) * 2, (BALL_RADIUS + i * 4) * 2),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                glow_surface,
                (*self.color, alpha),
                (BALL_RADIUS + i * 4, BALL_RADIUS + i * 4),
                BALL_RADIUS + i * 4
            )
            screen.blit(
                glow_surface,
                (x - BALL_RADIUS - i * 4, y - BALL_RADIUS - i * 4)
            )

        # =====================
        # BÓNG ĐỔ
        # =====================

        pygame.draw.circle(
            screen,
            (100, 100, 100),
            (
                x + 5,
                y + 6
            ),
            BALL_RADIUS + 2
        )

        # =====================
        # THÂN BÓNG
        # =====================

        pygame.draw.circle(
            screen,
            self.color,
            (
                x,
                y
            ),
            BALL_RADIUS
        )

        # =====================
        # VÙNG SÁNG CHÍNH
        # =====================

        pygame.draw.circle(
            screen,
            (
                255,
                255,
                255
            ),
            (
                x - 10,
                y - 10
            ),
            10
        )

        # =====================
        # VÙNG SÁNG PHỤ
        # =====================

        pygame.draw.circle(
            screen,
            (
                240,
                240,
                240
            ),
            (
                x - 3,
                y - 3
            ),
            5
        )

        # =====================
        # VIỀN NGOÀI
        # =====================

        pygame.draw.circle(
            screen,
            (
                40,
                40,
                40
            ),
            (
                x,
                y
            ),
            BALL_RADIUS,
            2
        )
