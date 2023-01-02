import json
import pygame
from copy import deepcopy
from random import choice, randrange

from classes.figure import Figure

FIGURES_POS = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]


class Game:
    run = True
    FPS = 60
    lost = False
    record = 0

    W = 10
    H = 20
    TILE = 45
    GAME_RES = W*TILE, H*TILE

    clock = pygame.time.Clock()
    window = None
    BG = None
    grid = None
    figures = None
    field = None

    figure = None
    next_figure = None

    anim_limit = None
    anim_speed = 60

    score = 0
    scores = {0:0, 1:100, 2:300, 3:700, 4:1500}
    record = 0

    def __init__(self, window, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.window = window
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_sc = pygame.Surface(self.GAME_RES)

        self.grid = [
            pygame.Rect(
                x * self.TILE, y * self.TILE, self.TILE, self.TILE
            ) for x in range (self.W) for y in range(self.H)
        ]

        self.figures = [
            [pygame.Rect(x + self.W // 2, y + 1, 1, 1) for x,y in fig_pos] for fig_pos in FIGURES_POS
        ]

        self.set_game()

        self.figure = Figure(self.TILE, deepcopy(choice(self.figures)), self.figure_rect, (randrange(30, 256), randrange(30,256), randrange(30, 256)))
        self.next_figure = Figure(self.TILE, deepcopy(choice(self.figures)), self.figure_rect, (randrange(30, 256), randrange(30,256), randrange(30, 256)))

        self.main_font = pygame.font.SysFont("comicsans", 65)
        self.font = pygame.font.SysFont("comicsans", 45)
        self.load_images()

        self.title_tetris = self.main_font.render("TETRIS", True, pygame.Color("darkorange"))
        self.title_score = self.font.render("score:", True, pygame.Color("green"))
        self.title_record = self.font.render("record:", True, pygame.Color("purple"))

    def set_game(self):
        self.figure_rect = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)
        self.field = [[0 for i in range(self.W)] for j in range(self.H)]
        self.anim_limit = None
        self.anim_speed = 60
        self.get_record()
        self.score = 0

    def load_images(self):
        # background
        self.BG = pygame.image.load("img/bg.jpg").convert()
        self.GAME_BG = pygame.image.load("img/bg2.jpg").convert()

    def move_objects(self, dx: int, rotate: bool, anim_limit: int):
        # move x
        figure_old = deepcopy(self.figure)
        self.figure.move_x(dx)
        if not self.figure.off_screen(self.W, self.H, self.field):
            self.figure = deepcopy(figure_old)

        # move y
        figure_old = deepcopy(self.figure)
        self.figure.move_y(self.anim_speed, anim_limit)

        if not self.figure.off_screen(self.W, self.H, self.field):
            for i in range(4):
                self.field[figure_old.figure[i].y][figure_old.figure[i].x] = figure_old.color
            self.figure = self.next_figure
            self.next_figure = Figure(
                self.TILE,
                deepcopy(choice(self.figures)),
                self.figure_rect,
                (randrange(30, 256), randrange(30,256), randrange(30, 256))
            )
            self.anim_limit = 2000
        
        # rotate
        if rotate:
            figure_old = deepcopy(self.figure)
            self.figure.rotate()

            if not self.figure.off_screen(self.W, self.H, self.field):
                self.figure = deepcopy(figure_old)

    def draw_titles(self):
        self.window.blit(self.title_tetris, (485, -10))
        self.window.blit(self.title_score, (535, 780))
        self.window.blit(self.font.render(str(self.score), True, pygame.Color("white")), (550, 840))
        self.window.blit(self.title_record, (525, 650))
        self.window.blit(self.font.render(str(self.record), True, pygame.Color("gold")), (550, 710))

    def draw_grid(self):
        [pygame.draw.rect(self.game_sc, (40, 40, 40), i_rect, 1) for i_rect in self.grid]

    def draw_field(self):
        figure_rect = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * self.TILE, y * self.TILE
                    pygame.draw.rect(self.game_sc, col, figure_rect)

    def check_lines(self):
        line, lines = self.H - 1, 0
        for row in range(self.H-1, -1, -1):
            count = 0
            for i in range(self.W):
                if self.field[row][i]:
                    count += 1
                self.field[line][i] = self.field[row][i]
            if count < self.W:
                line -= 1
            else:
                self.anim_speed += 3
                lines +=1

        self.score += self.scores[lines]

    def set_record(self):
        if self.score > self.record:
            data = {"record": self.score}
            json.dump(data,open("record.json","w"))

    def get_record(self):
        data = json.load(open("record.json"))
        if not data:
            self.record = 0
            return
        self.record = data.get("record")


    def game_over(self):
        for i in range(self.W):
            if self.field[0][i]:
                self.set_record()
                self.set_game()


    def draw_window(self):
        self.window.blit(self.BG, (0,0))
        self.window.blit(self.game_sc, (20,20))
        self.game_sc.blit(self.GAME_BG, (0,0))
        self.draw_grid()
        self.draw_field()
        self.draw_titles()
        self.figure.draw(self.game_sc)

        self.next_figure.draw(self.window, True)

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def main(self):
        while self.run:
            dx, rotate = 0, False
            #self.clock.tick(self.FPS)
            self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        self.anim_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True

            self.move_objects(dx, rotate, self.anim_limit)
            self.check_lines()
            self.game_over()
            self.draw_window()