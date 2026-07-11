from settings import *

class MoveAnimation:

    def __init__(
        self,
        ball,
        start_x,
        start_y,
        end_x,
        end_y
    ):

        self.ball = ball

        self.start_x = start_x
        self.start_y = start_y

        self.end_x = end_x
        self.end_y = end_y

        self.x = start_x
        self.y = start_y

        self.top_y = 120

        self.phase = 0

        self.finished = False

        self.speed_up = 15
        self.speed_down = 12
        self.speed_side = 18

        self.scale = 1.0

    def update(self):

        if self.finished:
            return

        # Bay lên
        if self.phase == 0:

            self.y -= self.speed_up

            self.scale = min(
                1.15,
                self.scale + 0.01
            )

            if self.y <= self.top_y:

                self.y = self.top_y
                self.phase = 1

        # Bay ngang
        elif self.phase == 1:

            dx = self.end_x - self.x

            if abs(dx) < self.speed_side:

                self.x = self.end_x
                self.phase = 2

            else:

                if dx > 0:
                    self.x += self.speed_side
                else:
                    self.x -= self.speed_side

        # Hạ xuống
        elif self.phase == 2:

            self.y += self.speed_down

            self.scale = max(
                1.0,
                self.scale - 0.01
            )

            if self.y >= self.end_y:

                self.y = self.end_y
                self.finished = True

    def draw(
        self,
        screen
    ):

        self.ball.draw(
            screen,
            self.x,
            self.y
        )