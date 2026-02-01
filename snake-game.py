import pygame
import random
import sys
import math

pygame.init()
pygame.mixer.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 800, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Snake Game 🐍")

clock = pygame.time.Clock()

# ================= COLORS =================
BG = (18, 18, 18)
GRID = (30, 30, 30)
SNAKE_HEAD = (0, 255, 140)
SNAKE_BODY = (0, 180, 100)
FOOD = (255, 80, 80)
TEXT = (255, 255, 255)

font = pygame.font.SysFont("consolas", 28)

# ================= SOUNDS =================
eat_sound = None
try:
    eat_sound = pygame.mixer.Sound(pygame.mixer.get_init())
except:
    pass

# ================= GRID =================
def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

# ================= FOOD =================
def draw_food(x, y):
    pygame.draw.circle(
        screen,
        FOOD,
        (x + CELL // 2, y + CELL // 2),
        CELL // 2 - 2
    )

# ================= SNAKE =================
def draw_snake(snake):
    for i, block in enumerate(snake):
        color = SNAKE_HEAD if i == len(snake) - 1 else SNAKE_BODY
        pygame.draw.rect(
            screen,
            color,
            (block[0], block[1], CELL, CELL),
            border_radius=8
        )

        # eyes
        if i == len(snake) - 1:
            pygame.draw.circle(screen, (0, 0, 0),
                               (block[0] + 6, block[1] + 6), 3)
            pygame.draw.circle(screen, (0, 0, 0),
                               (block[0] + 14, block[1] + 6), 3)

# ================= MAIN GAME =================
def game():

    while True:

        x = WIDTH // 2
        y = HEIGHT // 2
        dx = dy = 0

        snake = [[x, y]]
        length = 1

        foodx = random.randrange(0, WIDTH, CELL)
        foody = random.randrange(0, HEIGHT, CELL)

        game_over = False

        while not game_over:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -CELL
                        dy = 0

                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = CELL
                        dy = 0

                    elif event.key == pygame.K_UP and dy == 0:
                        dy = -CELL
                        dx = 0

                    elif event.key == pygame.K_DOWN and dy == 0:
                        dy = CELL
                        dx = 0

            x += dx
            y += dy

            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                game_over = True

            screen.fill(BG)
            draw_grid()

            snake.append([x, y])
            if len(snake) > length:
                snake.pop(0)

            if [x, y] in snake[:-1]:
                game_over = True

            draw_snake(snake)
            draw_food(foodx, foody)

            score_text = font.render(f"Score: {length-1}", True, TEXT)
            screen.blit(score_text, (10, 10))

            pygame.display.update()

            if x == foodx and y == foody:
                foodx = random.randrange(0, WIDTH, CELL)
                foody = random.randrange(0, HEIGHT, CELL)
                length += 1

            clock.tick(12)

        # ===== GAME OVER SCREEN =====
        screen.fill((0, 0, 0))
        over = font.render("GAME OVER", True, (255, 80, 80))
        again = font.render("Press ENTER to play again", True, TEXT)
        screen.blit(over, (WIDTH//2 - 90, HEIGHT//2 - 40))
        screen.blit(again, (WIDTH//2 - 170, HEIGHT//2 + 10))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False


game()
