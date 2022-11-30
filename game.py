import math
import time
from datetime import datetime
import random

import pygame

from pipe import Pipe

# Global variables
running = False

playing = False
dead = False

pipes = []  # Has all the pipes on screen

width, height, pixel = 690, 420, 64  # Create sizes
screen = pygame.display.set_mode((width, height))  # Create screen

y = height / 2  # Sets the current height of the player
gravity = -0.01  # Gravity
speed = 0  # Current speed

random_pipe = 3
last_pipe = 0
score = 0


def setup():
    pygame.init()

    # Set caption
    pygame.display.set_caption("Flappy Bird")

    # Set icon
    icon_image = pygame.image.load("Sprites/icon.png")
    pygame.display.set_icon(icon_image)

    # Set background
    background_image = pygame.image.load("Sprites/background.png")
    background_image = pygame.transform.scale(background_image, (width, height))
    screen.blit(background_image, (0, 0))


def run():
    global playing, pipes

    menu_screen()  # Starts with the menu screen

    while running:
        if playing:
            reset_screen()

            global last_pipe

            if (not pipes) or ((datetime.now() - last_pipe).total_seconds() >= random_pipe):
                last_pipe = datetime.now()

                pipe = Pipe(width, height)
                pipes.append(pipe)

            for pipe in pipes:
                if not pipe.update():
                    pipes.remove(pipe)
                    continue

                draw_pipe(pipe)

                global score, dead

                if pipe.collide(y, width, height):
                    # Removing current game
                    pipes.clear()
                    playing = False
                    dead = True

                    # Moving to menu screen
                    death_screen()

                elif pipe.same_x(width):
                    score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user wants to leave the game
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                if not playing and not dead:  # If on the menu screen
                    pos = pygame.mouse.get_pos()

                    if 396 > pos[0] > 294 and 304.5 > pos[1] > 255.5:  # If clicked on start
                        playing = True

                        reset_screen()
                else:  # While in game
                    global speed

                    if speed < 0:
                        speed = 0

                    speed += (1.5 / (1 + math.pow(math.e, speed)))

            if event.type == pygame.MOUSEBUTTONUP:
                if dead:
                    dead = False
                    score = 0

                    menu_screen()

        if playing:  # If game is running
            current_location()
            draw_player()

        pygame.display.update()


def draw_pipe(pipe):
    pipe_image = pygame.image.load("Sprites/pipe.png")

    pipe_down_image = pygame.transform.scale(pipe_image, (50, pipe.hole[0]))

    pipe_up_image = pygame.transform.scale(pipe_image, (50, pipe.hole[1]))
    pipe_up_image = pygame.transform.rotate(pipe_up_image, 180)

    screen.blit(pipe_down_image, (pipe.x, height - pipe.hole[0]))
    screen.blit(pipe_up_image, (pipe.x, 0))


def draw_player():
    player_image = pygame.image.load("Sprites/player.png")
    player_image = pygame.transform.scale(player_image, (30, 30))
    player_image = pygame.transform.rotate(player_image, math.degrees(math.atan(speed / 2)))

    screen.blit(player_image, (width / 3, y))


def current_location():
    global speed, y

    if y - speed >= height - 30:  # If player is at the bottom
        y = height - 30
        speed = 0
    elif y - speed <= 0:  # If player is at the top
        y = 0
        speed = gravity
    else:
        speed += gravity
        y -= speed


def reset_screen():  # Reset the screen to the background image
    background_image = pygame.image.load("Sprites/background.png")
    background_image = pygame.transform.scale(background_image, (width, height))
    screen.blit(background_image, (0, 0))


def menu_screen():  # Creates the menu screen
    def outline_text(font, font_name, font_size, text, color, surface):
        outline_font = pygame.font.SysFont(font_name, font_size)
        if font.get_bold():
            outline_font.set_bold(font.get_bold)
        if font.get_italic():
            outline_font.set_italic(font.get_italic)

        text_outline = outline_font.render(text, True, color)

        for x_bonus in range(2):
            for y_bonus in range(2):
                surface.blit(text_outline, (x_bonus * 4, y_bonus * 4))

    reset_screen()

    # Adds the title
    text_font = pygame.font.SysFont("inkfree", 64)
    text_font.set_bold(True)
    text_font.set_italic(True)

    text = text_font.render("Flappy Bird", True, (150, 150, 0))

    text_surface = pygame.Surface((text.get_width() + 4, text.get_height() + 4), pygame.SRCALPHA)

    outline_text(text_font, "inkfree", 64, "Flappy Bird", pygame.Color(0, 0, 0), text_surface)
    text_surface.blit(text, (2, 2))
    text_surface = pygame.transform.rotate(text_surface, 5)

    screen.blit(text_surface, ((width / 2) - (text_surface.get_width() / 2), (height / 4) - (text_surface.get_height() / 2)))

    # Adds the buttons
    start_text_font = pygame.font.SysFont("comicsans", 32)
    start_text_font.set_bold(True)

    start_text = start_text_font.render("Start", True, (150, 150, 0))

    start_text_surface = pygame.Surface((start_text.get_width() + 4, start_text.get_height() + 4), pygame.SRCALPHA)

    outline_text(start_text_font, "comicsans", 32, "Start", pygame.Color(0, 0, 0), start_text_surface)
    start_text_surface.blit(start_text, (2, 2))

    screen.blit(start_text_surface, ((width / 2) - (start_text_surface.get_width() / 2), (height / 1.5) - (start_text_surface.get_height() / 2)))


def death_screen():
    def outline_text(font, font_name, font_size, text, color, surface):
        outline_font = pygame.font.SysFont(font_name, font_size)
        if font.get_bold():
            outline_font.set_bold(font.get_bold)
        if font.get_italic():
            outline_font.set_italic(font.get_italic)

        text_outline = outline_font.render(text, True, color)

        for x_bonus in range(2):
            for y_bonus in range(2):
                surface.blit(text_outline, (x_bonus * 4, y_bonus * 4))

    reset_screen()

    # Adds the title
    text_font = pygame.font.SysFont("inkfree", 64)
    text_font.set_bold(True)
    text_font.set_italic(True)

    text = text_font.render("You Lost!", True, (150, 150, 0))

    text_surface = pygame.Surface((text.get_width() + 4, text.get_height() + 4), pygame.SRCALPHA)

    outline_text(text_font, "inkfree", 64, "You Lost!", pygame.Color(0, 0, 0), text_surface)
    text_surface.blit(text, (2, 2))

    screen.blit(text_surface, ((width / 2) - (text_surface.get_width() / 2), (height / 4) - (text_surface.get_height() / 2)))

    # Adds the score
    score_font = pygame.font.SysFont("inkfree", 48)
    score_font.set_bold(True)
    score_font.set_italic(True)

    score_text = score_font.render(f"Total Score: {score}", True, (255, 255, 255))

    score_surface = pygame.Surface((score_text.get_width() + 4, score_text.get_height() + 4), pygame.SRCALPHA)

    outline_text(score_font, "inkfree", 48, f"Total Score: {score}", pygame.Color(0, 0, 0), score_surface)
    score_surface.blit(score_text, (2, 2))

    screen.blit(score_surface, ((width / 2) - (score_surface.get_width() / 2), (height / 4 * 3) - (score_surface.get_height() / 2)))
