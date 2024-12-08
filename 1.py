import pygame
import random
import sys
import json

coin = 1000
bombs = 0

SAVE_FILE = "game_data.json"

game_data = {"coin": 1000, "bombs": 0}

def save_data(data):
    with open("game_data.json", "w") as file:
        json.dump(data, file)

def load_data():
    try:
        with open("game_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return game_data

pygame.init()
WIDTH, HEIGHT = 500, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 10, 20

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

def clear_lines_with_bomb():
    global board
    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

class Block:
    def __init__(self, shape=None):
        self.shape = shape if shape else random.choice(SHAPES)
        self.x, self.y = GRID_WIDTH // 2 - len(self.shape[0]) // 2, 0
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

def initialize_board():
    return [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

board = initialize_board()

def draw_block(block, offset_x=0, offset_y=0):
    for i, row in enumerate(block.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    SCREEN, block.color,
                    (BLOCK_SIZE * (block.x + j + offset_x), BLOCK_SIZE * (block.y + i + offset_y), BLOCK_SIZE,
                     BLOCK_SIZE)
                )

def draw_board():
    SCREEN.fill(BLACK)
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    SCREEN, cell,
                    (BLOCK_SIZE * x, BLOCK_SIZE * y, BLOCK_SIZE, BLOCK_SIZE)
                )
    pygame.draw.rect(
        SCREEN, GREY,
        (0, 0, BLOCK_SIZE * GRID_WIDTH, BLOCK_SIZE * GRID_HEIGHT), 3
    )

def valid_position(block, dx=0, dy=0):
    for i, row in enumerate(block.shape):
        for j, cell in enumerate(row):
            if cell:
                new_x, new_y = block.x + j + dx, block.y + i + dy
                if (
                        new_x < 0
                        or new_x >= GRID_WIDTH
                        or new_y >= GRID_HEIGHT
                        or (new_y >= 0 and board[new_y][new_x])
                ):
                    return False
    return True

def lock_block(block):
    for i, row in enumerate(block.shape):
        for j, cell in enumerate(row):
            if cell:
                board[block.y + i][block.x + j] = block.color

def clear_lines():
    global board, score
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared_lines = GRID_HEIGHT - len(new_board)
    board = [[0] * GRID_WIDTH for _ in range(cleared_lines)] + new_board
    score += cleared_lines * 100

def draw_next_block(block):
    offset_x, offset_y = GRID_WIDTH + 2, 2
    for i, row in enumerate(block.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    SCREEN, block.color,
                    (BLOCK_SIZE * (j + offset_x), BLOCK_SIZE * (i + offset_y), BLOCK_SIZE, BLOCK_SIZE)
                )

def draw_button(text, color, x, y, width, height):
    pygame.draw.rect(SCREEN, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    SCREEN.blit(text_surface, text_rect)

def main_menu():
    global coin, bombs
    data = load_data()
    coin = data.get("coin", 1000)
    bombs = data.get("bombs", 0)

    while True:
        SCREEN.fill(BLACK)

        font = pygame.font.Font(None, 74)
        title_text = font.render("TETRIS", True, WHITE)
        SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        draw_button("START", GREEN, WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
        draw_button("SHOP", GREY, WIDTH // 2 - 75, HEIGHT // 2 + 80, 150, 50)
        draw_button("QUIT", RED, WIDTH // 2 - 75, HEIGHT // 2 + 160, 150, 50)

        font = pygame.font.Font(None, 36)
        coin_text = font.render(f"Coins: {coin}", True, WHITE)
        SCREEN.blit(coin_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if WIDTH // 2 - 75 < mouse_x < WIDTH // 2 + 75 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50:
                    game_loop()
                    return

                if WIDTH // 2 - 75 < mouse_x < WIDTH // 2 + 75 and HEIGHT // 2 + 80 < mouse_y < HEIGHT // 2 + 130:
                    shop_menu()
                    return

                if WIDTH // 2 - 75 < mouse_x < WIDTH // 2 + 75 and HEIGHT // 2 + 160 < mouse_y < HEIGHT // 2 + 210:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def shop_menu():
    global coin, bombs

    while True:
        SCREEN.fill(BLACK)

        font = pygame.font.Font(None, 74)
        shop_title = font.render("SHOP", True, WHITE)
        SCREEN.blit(shop_title, (WIDTH // 2 - shop_title.get_width() // 2, HEIGHT // 4))

        font = pygame.font.Font(None, 36)
        description_text = font.render("Here you can buy themes or blocks!", True, WHITE)
        SCREEN.blit(description_text, (WIDTH // 2 - description_text.get_width() // 2, HEIGHT // 4 + 50))

        draw_button("Bombs", RED, WIDTH // 2 - 75, HEIGHT - 350, 150, 50)
        draw_button("BACK", RED, WIDTH // 2 - 75, HEIGHT - 100, 150, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if WIDTH // 2 - 75 < mouse_x < WIDTH // 2 + 75 and HEIGHT - 100 < mouse_y < HEIGHT - 50:
                    main_menu()
                    return

                elif WIDTH // 2 - 75 < mouse_x < WIDTH // 2 + 75 and HEIGHT - 350 < mouse_y < HEIGHT - 300:
                    global bombs, coin
                    if coin >= 1000:
                        bombs += 1
                        coin -= 1000
                        save_data({"coin": coin, "bombs": bombs})
                        print(f"Bombs increased! Total bombs: {bombs}, Remaining coins: {coin}")
                    else:
                        print("Not enough coins to buy a bomb!")

        pygame.display.update()

def use_bomb():
    global bombs, coin
    if bombs > 0:
        clear_lines_with_bomb()
        bombs -= 1
        save_data({"coin": coin, "bombs": bombs})
        print("Bomb used!")
    else:
        print("No bombs available to use.")

def game_loop():
    global score, coin, bombs
    score = 0
    clock = pygame.time.Clock()
    current_block = Block()
    next_block = Block()
    fall_time = 0
    fall_speed = 1.0
    paused = False
    global board
    board = initialize_board()

    running = True
    while running:
        fall_time += clock.get_rawtime()
        clock.tick()

        level = score // 1000 + 1
        if level == 1:
            fall_speed = 1.0
        elif level == 2:
            fall_speed = 0.6
        elif level == 3:
            fall_speed = 0.4
        else:
            fall_speed = 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_LEFT and valid_position(current_block, dx=-1):
                        current_block.move(-1, 0)
                    elif event.key == pygame.K_RIGHT and valid_position(current_block, dx=1):
                        current_block.move(1, 0)
                    elif event.key == pygame.K_UP:
                        current_block.rotate()
                        if not valid_position(current_block):
                            current_block.rotate()
                    elif event.key == pygame.K_DOWN:
                        if valid_position(current_block, dy=1):
                            current_block.move(0, 1)
                        else:
                            lock_block(current_block)
                            clear_lines()
                            current_block = next_block
                            next_block = Block()
                            if not valid_position(current_block):
                                running = False
                    elif event.key == pygame.K_b:
                        use_bomb()

                elif event.key == pygame.K_m and paused:
                    main_menu()
                    return
                elif event.key == pygame.K_r and paused:
                    score = 0
                    board = initialize_board()
                    current_block = Block()
                    next_block = Block()
                    fall_time = 0
                    paused = False

        if not paused:
            if fall_time / 1000 >= fall_speed:
                if valid_position(current_block, dy=1):
                    current_block.move(0, 1)
                else:
                    lock_block(current_block)
                    clear_lines()
                    current_block = next_block
                    next_block = Block()
                    if not valid_position(current_block):
                        running = False
                fall_time = 0

        draw_board()
        draw_block(current_block)
        draw_next_block(next_block)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (WIDTH - 150, HEIGHT // 4 + 50))
        level_text = font.render(f"Level: {level}", True, WHITE)
        SCREEN.blit(level_text, (WIDTH - 150, HEIGHT // 4 + 100))

        bomb_text = font.render(f"Bombs: {bombs}", True, WHITE)
        SCREEN.blit(bomb_text, (WIDTH - 150, HEIGHT // 4 + 150))

        if paused:
            font = pygame.font.Font(None, 48)
            pause_text = font.render("PAUSED", True, WHITE)
            SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press R to restart", True, WHITE)
            SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press M to Main", True, WHITE)
            SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.update()

    coin += score // 1
    save_data({"coin": coin, "bombs": bombs})
    main_menu()

if __name__ == "__main__":
    main_menu()
    game_loop()