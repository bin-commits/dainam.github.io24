import pygame

from settings import *


class Tube:

    def __init__(self):

        self.balls = []

    # ======================
    # THÔNG TIN
    # ======================

    def empty(self):

        return len(self.balls) == 0

    def full(self):

        return len(self.balls) >= CAPACITY

    def top_color(self):

        if self.empty():
            return None

        return self.balls[-1].color_id

    def free_space(self):

        return CAPACITY - len(self.balls)

    def top_ball(self):

        if self.empty():
            return None

        return self.balls[-1]

    # ======================
    # KIỂM TRA HOÀN THÀNH
    # ======================

    def completed(self):

        if len(self.balls) != CAPACITY:
            return False

        color = self.balls[0].color_id

        for ball in self.balls:

            if ball.color_id != color:
                return False

        return True

    # ======================
    # THÊM / XÓA
    # ======================

    def push(self, ball):

        if self.full():
            return False

        self.balls.append(ball)

        return True

    def pop(self):

        if self.empty():
            return None

        return self.balls.pop()

    # ======================
    # NHÓM MÀU ĐỈNH
    # ======================

    def top_group_size(self):

        if self.empty():
            return 0

        color = self.top_color()

        count = 0

        for ball in reversed(self.balls):

            if ball.color_id == color:
                count += 1
            else:
                break

        return count

    # ======================
    # KIỂM TRA NHẬN
    # ======================

    def can_receive(
        self,
        color_id,
        amount
    ):

        return self.free_space() >= amount

    # ======================
    # DI CHUYỂN NHÓM
    # ======================

    def move_ball_to(
        self,
        target
    ):

        if self.empty():
            return False

        ball = self.top_ball()

        if not target.can_receive(
            ball.color_id,
            1
        ):
            return False

        target.push(
            self.pop()
        )

        return True

    def move_group_to(
        self,
        target
    ):

        if self.empty():
            return False

        color = self.top_color()

        amount = min(
            self.top_group_size(),
            target.free_space()
        )

        if not target.can_receive(
            color,
            amount
        ):
            return False

        moved = []

        for _ in range(amount):

            moved.append(
                self.pop()
            )

        moved.reverse()

        for ball in moved:

            target.push(ball)

        return True

    # ======================
    # VẼ ỐNG NGHIỆM
    # ======================

    def draw(
        self,
        screen,
        x,
        hidden_ball=None
    ):

        outer_rect = pygame.Rect(
            x,
            TUBE_Y,
            TUBE_WIDTH,
            TUBE_HEIGHT
        )

        # =====================
        # SHADOW EFFECT
        # =====================
        
        for i in range(8, 0, -1):
            shadow_alpha = int(25 * (1 - i / 8))
            shadow_rect = pygame.Rect(
                x + i,
                TUBE_Y + i + 2,
                TUBE_WIDTH,
                TUBE_HEIGHT
            )
            shadow_surface = pygame.Surface(
                (TUBE_WIDTH, TUBE_HEIGHT),
                pygame.SRCALPHA
            )
            pygame.draw.rect(
                shadow_surface,
                (0, 0, 0, shadow_alpha),
                (0, 0, TUBE_WIDTH, TUBE_HEIGHT),
                border_radius=24
            )
            screen.blit(
                shadow_surface,
                shadow_rect
            )

        # =====================
        # TUBE BACKGROUND (FILLED)
        # =====================

        pygame.draw.rect(
            screen,
            (250, 250, 250),
            outer_rect,
            border_radius=24
        )

        # =====================
        # TUBE GRADIENT OVERLAY
        # =====================

        gradient_surface = pygame.Surface(
            (TUBE_WIDTH, TUBE_HEIGHT),
            pygame.SRCALPHA
        )

        for dy in range(TUBE_HEIGHT):
            ratio = dy / TUBE_HEIGHT
            alpha = int(80 * ratio)
            pygame.draw.line(
                gradient_surface,
                (100, 120, 150, alpha),
                (0, dy),
                (TUBE_WIDTH, dy)
            )

        screen.blit(gradient_surface, (x, TUBE_Y))

        # =====================
        # TUBE BORDER
        # =====================

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            outer_rect,
            4,
            border_radius=24
        )

        # =====================
        # INNER BRIGHT EDGE
        # =====================

        inner_rect = pygame.Rect(
            x + 4,
            TUBE_Y + 4,
            TUBE_WIDTH - 8,
            TUBE_HEIGHT - 8
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            inner_rect,
            1,
            border_radius=20
        )

        # =====================
        # GLASS HIGHLIGHT
        # =====================

        glass_highlight = pygame.Rect(
            x + 6,
            TUBE_Y + 8,
            7,
            TUBE_HEIGHT - 16
        )

        highlight_surface = pygame.Surface(
            (7, TUBE_HEIGHT - 16),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            highlight_surface,
            (255, 255, 255, 80),
            (0, 0, 7, TUBE_HEIGHT - 16),
            border_radius=6
        )

        screen.blit(highlight_surface, (x + 6, TUBE_Y + 8))

        # =====================
        # VẼ CÁC BÓNG
        # =====================

        center_x = x + TUBE_WIDTH // 2

        visible_index = 0

        for ball in self.balls:

            if ball is hidden_ball:
                continue

            y = (
                TUBE_Y
                + TUBE_HEIGHT
                - 50
                - visible_index * BALL_SPACING
            )

            ball.draw(
                screen,
                center_x,
                y
            )

            visible_index += 1