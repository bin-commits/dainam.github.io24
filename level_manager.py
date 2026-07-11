import random

from tube import Tube
from ball import Ball


class LevelManager:

    def __init__(self):

        self.current_level = 1

    # ==========================
    # THÔNG TIN LEVEL
    # ==========================

    def level_info(self):

        level_data = {

            1: 3,
            2: 3,

            3: 4,
            4: 4,

            5: 5,
            6: 5,

            7: 6,
            8: 6,

            9: 7,
            10: 7,

            11: 8,
            12: 8,

            13: 9,
            14: 9,

            15: 10,
            16: 10,

            17: 11,
            18: 11,

            19: 12,
            20: 12
        }

        color_count = level_data.get(
            self.current_level,
            12
        )

        tube_count = color_count + 2

        return (
            color_count,
            tube_count
        )

    # ==========================
    # TẠO LEVEL
    # ==========================

    def create_level(self):

        color_count, tube_count = (
            self.level_info()
        )

        tubes = [
            Tube()
            for _ in range(tube_count)
        ]

        balls = []

        for color_id in range(color_count):

            for _ in range(4):

                balls.append(
                    Ball(color_id)
                )

        random.shuffle(balls)

        index = 0

        for tube_id in range(
            tube_count - 2
        ):

            for _ in range(4):

                tubes[tube_id].push(
                    balls[index]
                )

                index += 1

        return tubes

    # ==========================
    # KIỂM TRA THẮNG
    # ==========================

    def level_completed(
        self,
        tubes
    ):

        for tube in tubes:

            if tube.empty():
                continue

            if not tube.completed():
                return False

        return True

    # ==========================
    # CHUYỂN MÀN
    # ==========================

    def next_level(self):

        if self.current_level < 20:

            self.current_level += 1

    def campaign_completed(self):

        return (
            self.current_level >= 20
        )
