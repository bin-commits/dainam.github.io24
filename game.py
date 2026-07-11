import math
import pygame

from settings import *
from level_manager import LevelManager
from astar import solve
from ui import Button
from animation import MoveAnimation


class Game:
    def __init__(self):
        self.state = "menu"

        self.level_complete = False

        self.animation = None

        self.pending_move = None

        self.solve_button = Button(
            WIDTH - 270,
            40,
            220,
            55,
            "Giải bằng A*"
        )

        self.restart_button = Button(
            WIDTH - 270,
            110,
            220,
            55,
            "Chơi lại"
        )

        self.font = pygame.font.SysFont(
            "Segoe UI",
            26
        )

        self.title_font = pygame.font.SysFont(
            "Segoe UI",
            48,
            bold=True
        )
        self.play_button = Button(
            WIDTH // 2 - 150,
            300,
            300,
            70,
            "Chơi Game"
        )

        self.level_button = Button(
            WIDTH // 2 - 150,
            390,
            300,
            70,
            "Chọn Màn"
        )

        self.exit_button = Button(
            WIDTH // 2 - 150,
            480,
            300,
            70,
            "Thoát"
        )

        self.level_select_button = Button(
            WIDTH // 2 - 120,
            HEIGHT // 2 + 20,
            240,
            60,
            "Chọn Màn"
        )

        self.back_button = Button(
            20,
            20,
            120,
            50,
            "← Back"
        )

        self.next_level_button = Button(
            WIDTH // 2 - 120,
            HEIGHT // 2 + 40,
            240,
            60,
            "Next Level"
        )

        self.manager = LevelManager()

        self.selected_tube = None

        self.hidden_ball = None

        self.moves = 0

        self.stars = 3

        self.solution = []

        self.auto_solving = False

        self.solve_timer = 0

        self.load_level()

    def load_level(self):

        self.tubes = self.manager.create_level()

        self.selected_tube = None

        self.moves = 0

        self.animation = None

        self.solution = []

        self.auto_solving = False

        self.solve_timer = 0

    def calculate_stars(self):

        if self.moves <= 10:
            return 3

        if self.moves <= 20:
            return 2

        return 1

    def draw_star_icon(
        self,
        screen,
        center_x,
        center_y,
        size
    ):

        outer = size // 2
        inner = outer * 0.45
        points = []

        for i in range(10):
            angle = i * 36
            radius = outer if i % 2 == 0 else inner
            rad = math.radians(angle)
            points.append(
                (
                    center_x + radius * math.cos(rad),
                    center_y - radius * math.sin(rad)
                )
            )

        pygame.draw.polygon(
            screen,
            (255, 215, 0),
            points
        )
        pygame.draw.polygon(
            screen,
            (200, 170, 0),
            points,
            2
        )

    # =====================
    # VỊ TRÍ CỘT
    # =====================

    def tube_x(self, index):

        total_width = (
            len(self.tubes) * TUBE_WIDTH
            +
            (len(self.tubes) - 1)
            * TUBE_SPACING
        )

        start_x = (
            WIDTH - total_width
        ) // 2

        return (
            start_x
            +
            index
            *
            (
                TUBE_WIDTH
                +
                TUBE_SPACING
            )
        )

    # =====================
    # LẤY CỘT ĐƯỢC CLICK
    # =====================

    def tube_clicked(self, pos):

        mx, my = pos

        for i in range(len(self.tubes)):

            x = self.tube_x(i)

            rect = pygame.Rect(
                x,
                TUBE_Y,
                TUBE_WIDTH,
                TUBE_HEIGHT
            )

            if rect.collidepoint(mx, my):
                return i

        return None

    # =====================
    # MOVE
    # =====================

    def move(self, source, target):

        if source == target:
            return False

        success = (
            self.tubes[source]
            .move_ball_to(
                self.tubes[target]
            )
        )

        if success:

            self.moves += 1

            self.check_win()

        return success

    def start_animation(self, source, target):
        print("START:", source, target)

        source_tube = self.tubes[source]

        target_tube = self.tubes[target]

        ball = source_tube.top_ball()

        self.hidden_ball = ball

        if ball is None:    
            return  

        source_x = self.tube_x(source)

        target_x = self.tube_x(target)

        start_x = (
            source_x
            +  
            TUBE_WIDTH // 2
        )

        start_y = (
            TUBE_Y
            +
            TUBE_HEIGHT
            -
            50
            -
            (
                len(source_tube.balls)-1
            )
            * BALL_SPACING
        )

        end_x = (
            target_x
            +
            TUBE_WIDTH // 2
        )

        end_y = (
            TUBE_Y
            +
            TUBE_HEIGHT
            -
            50
            -
            (
                len(target_tube.balls)
            )
            * BALL_SPACING
        )

        self.animation = MoveAnimation(
            ball,
            start_x,
            start_y,
            end_x,
            end_y
        )

        self.pending_move = (
            source,
            target
        )

    def draw_menu(
        self,
        screen
    ):

        self.draw_background(
            screen
        )

        title = self.title_font.render(
            "BALL ARRANGEMENT",
            True,
            BLACK
        )

        screen.blit(
            title,
            (
                WIDTH // 2
                - title.get_width() // 2,
                120
            )
        )

        self.play_button.draw(
            screen,
            self.font
        )

        self.level_button.draw(
            screen,
            self.font
        )

        self.exit_button.draw(
            screen,
            self.font
        )

    def draw_level_select(
        self,
        screen
    ):

        title = self.title_font.render(
            "CHỌN MÀN",
            True,
            BLACK
        )

        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                60
            )
        )

        button_w = 80
        button_h = 50
        gap = 20

        start_x = WIDTH // 2 - (5 * button_w + 4 * gap) // 2
        start_y = 180

        level = 1

        for row in range(4):
            for col in range(5):

                x = start_x + col * (button_w + gap)
                y = start_y + row * (button_h + gap)

                rect = pygame.Rect(
                    x, y,
                    button_w,
                    button_h
                )

                pygame.draw.rect(
                    screen,
                    (255,255,255),
                    rect,
                    border_radius=12
                )

                pygame.draw.rect(
                    screen,
                    BLACK,
                    rect,
                    2,
                    border_radius=12
                )

                text = self.font.render(
                    str(level),
                    True,
                    BLACK
                )

                screen.blit(
                    text,
                    (
                        rect.centerx - text.get_width() // 2,
                        rect.centery - text.get_height() // 2
                    )
                )

                level += 1

        self.back_button.draw(
            screen,
            self.font
        )

    def handle_level_select(
        self,
        event
    ):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        button_w = 80
        button_h = 50
        gap = 20

        start_x = WIDTH // 2 - (5 * button_w + 4 * gap) // 2
        start_y = 180

        level = 1

        for row in range(4):
            for col in range(5):

                x = start_x + col * (button_w + gap)
                y = start_y + row * (button_h + gap)

                rect = pygame.Rect(
                    x, y,
                    button_w,
                    button_h
                )

                if rect.collidepoint(event.pos):

                    self.manager.current_level = level
                    self.load_level()
                    self.state = "playing"
                    return

                level += 1

    # =====================
    # KIỂM TRA THẮNG
    # =====================

    def check_win(self):

        if self.manager.level_completed(
            self.tubes
        ):

            self.stars = (
                self.calculate_stars()
            )

            self.level_complete = True

    # =====================
    # CHUYỂN ĐỔI STATE
    # =====================

    def current_state(self):

        result = []

        for tube in self.tubes:

            result.append(
                tuple(
                    ball.color_id
                    for ball in tube.balls
                )
            )

        return tuple(result)

    # =====================
    # A*
    # =====================

    def start_astar(self):

        state = self.current_state()

        self.solution = solve(state)

        self.auto_solving = True

        self.solve_timer = 0

    # =====================
    # EVENT
    # =====================

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.back_button.clicked(event):

                if self.state == "level_select":
                    self.state = "menu"
                    return

                if self.state == "playing":
                    self.state = "menu"
                    return

        if self.state == "level_select":
            self.handle_level_select(event)
            return

        if self.state == "menu":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.play_button.clicked(
                    event
                ):

                    self.state = "playing"

                elif self.level_select_button.clicked(
                    event
                ):

                    self.state = "level_select"

                elif self.exit_button.clicked(
                    event
                ):

                    pygame.quit()
                    quit()

            return

        if self.level_complete:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.next_level_button.clicked(
                    event
                ):

                    self.manager.next_level()

                    self.load_level()

                    self.level_complete = False

            return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return  
        
        print("CLICK:", event.pos)

        if self.restart_button.clicked(event):
            self.load_level()
            return

        if self.solve_button.clicked(event):
            self.start_astar()
            return

        tube = self.tube_clicked(
            event.pos
        )

        print("TUBE:", tube)

        if tube is None:
            return

        if self.selected_tube is None:

            if not self.tubes[
                tube
            ].empty():

                self.selected_tube = tube

        else:

            self.start_animation(
                self.selected_tube,
                tube
            )
            self.selected_tube = None

    # =====================
    # UPDATE
    # =====================

    def update(self):

        if self.animation:

            self.animation.update()

            if self.animation.finished:

                source, target = (
                    self.pending_move
                )

                self.move(
                    source,
                    target
                )

                self.animation = None

                self.pending_move = None

                self.hidden_ball = None

        if self.auto_solving:

            self.solve_timer += 1

            if self.solve_timer > 25:

                self.solve_timer = 0

                if len(self.solution) > 0:

                    source, target = (
                        self.solution.pop(0)
                    )

                    self.move(
                        source,
                        target
                    )

                else:

                    self.auto_solving = False

    # =====================
    # DRAW
    # =====================

    def draw_background(
        self,
        screen
    ):

        top_color = (
            70,
            110,
            200
        )

        bottom_color = (
            220,
            235,
            255
        )

        for y in range(HEIGHT):

            ratio = y / HEIGHT

            r = int(
                top_color[0]
                +
                (
                    bottom_color[0]
                    - top_color[0]
                )
                * ratio
            )

            g = int(
                top_color[1]
                +
                (
                    bottom_color[1]
                    - top_color[1]
                )
                * ratio
            )

            b = int(
                top_color[2]
                +
                (
                    bottom_color[2]
                    - top_color[2]
                )
                * ratio
            )

            pygame.draw.line(
                screen,
                (r, g, b),
                (0, y),
                (WIDTH, y)
            )

    def draw_title(
        self,
        screen
    ):

        title = (
            self.title_font.render(
                "BALL ARRANGEMENT",
                True,
                BLACK
            )
        )

        screen.blit(
            title,
            (
                WIDTH // 2
                -
                title.get_width() // 2,
                40
            )
        )

    def draw_info(
        self,
        screen
    ):

        # =====================
        # LEVEL BOX
        # =====================

        level_box = pygame.Rect(
            150,
            20,
            200,
            80
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            level_box,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            (52, 152, 219),
            level_box,
            3,
            border_radius=15
        )

        level_text = (
            self.font.render(
                f"Level: {self.manager.current_level}",
                True,
                (52, 152, 219)
            )
        )

        moves_text = (
            self.font.render(
                f"Moves: {self.moves}",
                True,
                BLACK
            )
        )

        screen.blit(
            level_text,
            (170, 30)
        )

        screen.blit(
            moves_text,
            (170, 65)
        )

    def draw_tubes(
        self,
        screen
    ):

        for i, tube in enumerate(
            self.tubes
        ):

            x = self.tube_x(i)

            tube.draw(
                screen,
                x,
                self.hidden_ball
            )

            if (
                self.selected_tube
                ==
                i
            ):

                pygame.draw.rect(
                    screen,
                    (0, 255, 255),
                    (
                        x - 5,
                        TUBE_Y - 5,
                        TUBE_WIDTH + 10,
                        TUBE_HEIGHT + 10
                    ),
                    4,
                    border_radius=20
                )

    def draw(
        self,
        screen
    ):

        self.draw_background(screen)

        if self.state == "menu":
            self.draw_menu(screen)
            return

        if self.state == "level_select":
            self.draw_level_select(screen)
            return

        self.draw_title(
            screen
        )

        self.draw_info(
            screen
        )

        self.back_button.draw(
            screen,
            self.font
        )

        self.draw_tubes(
            screen
        )

        self.solve_button.draw(
            screen,
            self.font
        )

        self.restart_button.draw(
            screen,
            self.font
        )

        if self.animation:

            self.animation.draw(
                screen
            )

        if getattr(
            self,
            "level_complete",
            False
        ):

            popup_rect = pygame.Rect(
                WIDTH // 2 - 250,
                HEIGHT // 2 - 120,
                500,
                240
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                popup_rect,
                border_radius=25
            )

            pygame.draw.rect(
                screen,
                (0, 180, 0),
                popup_rect,
                4,
                border_radius=25
            )

            text = self.title_font.render(
                "LEVEL COMPLETE!",
                True,
                (0, 180, 0)
            )

            screen.blit(
                text,
                (
                    popup_rect.centerx
                    - text.get_width() // 2,
                    popup_rect.y + 40
                )
            )

            info = self.font.render(
                "Nhan chuot de qua man",
                True,
                BLACK
            )

            screen.blit(
                info,
                (
                    popup_rect.centerx
                    - info.get_width() // 2,
                    popup_rect.y + 130
                )
            )

            star_size = 40
            spacing = 10
            total_width = self.stars * star_size + (self.stars - 1) * spacing
            start_x = popup_rect.centerx - total_width // 2
            star_y = popup_rect.y + 90

            for i in range(self.stars):
                self.draw_star_icon(
                    screen,
                    start_x + i * (star_size + spacing) + star_size // 2,
                    star_y + star_size // 2,
                    star_size
                )

            moves_surface = self.font.render(
                f"Moves: {self.moves}",
                True,
                BLACK
            )

            screen.blit(
                moves_surface,
                (
                    popup_rect.centerx
                    - moves_surface.get_width() // 2,
                    popup_rect.y + 150
                )
            )

            self.next_level_button.draw(
                screen,
                self.font
            )