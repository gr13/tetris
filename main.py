import pygame
from classes.game import Game

pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 750, 940

MAIN_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

main_game = Game(MAIN_WINDOW, SCREEN_WIDTH, SCREEN_HEIGHT)

def main_menu(window):
    title_font = pygame.font.SysFont("comcsans", 70)

    run = True
    while run:
        window.blit(main_game.BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        window.blit(
            title_label,
            (
                SCREEN_WIDTH/2 - title_label.get_width()/2,
                SCREEN_HEIGHT/2 - title_label.get_height()/2,
            )
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_game.main()
                quit()

main_menu(MAIN_WINDOW)
