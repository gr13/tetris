import pygame
from copy import deepcopy
from typing import List

class Figure:
    figure = None
    figure_rect = None
    color = None
    TILE = None

    anim_count, anim_limit = 0, 2000

    def __init__(self, TILE, figure, figure_rect, color):
        self.figure = figure
        self.figure_rect = figure_rect
        self.color = color
        self.TILE = TILE

    def draw(self, window: pygame.Surface, is_next: bool = False):
        for i in range(4):
            self.figure_rect.x = self.figure[i].x * self.TILE
            self.figure_rect.y = self.figure[i].y * self.TILE
            if is_next:
                self.figure_rect.x += 380
                self.figure_rect.y += 185
            pygame.draw.rect(window, self.color, self.figure_rect)

    def move_x(self, dx: int):
        for i in range(4):
            self.figure[i].x += dx

    def move_y(self, anim_speed: int, anim_limit: int = None):
        if not anim_limit:
            anim_limit = self.anim_limit
        self.anim_count += anim_speed
        if self.anim_count > anim_limit:
            self.anim_count = 0
            for i in range(4):
                self.figure[i].y += 1

    def rotate(self):
        center = self.figure[0]
        for i in range(4):
            x = self.figure[i].y - center.y
            y = self.figure[i].x - center.x
            self.figure[i].x = center.x - x
            self.figure[i].y = center.y + y

    def off_screen(self, width:int, height:int, field: List):
        for i in range(4):
            if self.figure[i].x < 0 or self.figure[i].x > width:
                return False
            elif self.figure[i].y > height-1 or self.figure[i].x >= width or field[self.figure[i].y][self.figure[i].x]:
                return False
        return True
