import pygame
from maz.generator import generate_maze
from search.animi_ai import get_enemy_move

# === إعدادات ===
CELL_SIZE = 50
MAZE = generate_maze()
ROWS, COLS = len(MAZE), len(MAZE[0])
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# === ألوان ===
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 150)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# === رموز المتاهة ===
START = 2
OBSTACLE = 1
EMPTY = 0
KEY = 3
TREASURE = 4

# === تحميل الصور ===
def load_images():
    key_img = pygame.image.load("assets/key.png")
    treasure_img = pygame.image.load("assets/treasure.png")
    win_img = pygame.image.load("assets/win.jpg")
    lose_img = pygame.image.load("assets/lose.png")
    return {
        "key": pygame.transform.scale(key_img, (CELL_SIZE, CELL_SIZE)),
        "treasure": pygame.transform.scale(treasure_img, (CELL_SIZE, CELL_SIZE)),
        "win": pygame.transform.scale(win_img, (200, 200)),
        "lose": pygame.transform.scale(lose_img, (200, 200)),
    }

# === رسم خلية ===
def draw_cell(win, x, y, color):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(win, color, rect)
    pygame.draw.rect(win, BLACK, rect, 1)

# === رسم المتاهة ===
def draw_maze(win, maze, images, show_key):
    for y in range(ROWS):
        for x in range(COLS):
            value = maze[y][x]
            color = WHITE
            if value == OBSTACLE:
                color = GRAY
            elif value == START:
                color = BLUE
            draw_cell(win, x, y, color)
            if value == KEY and show_key:
                win.blit(images["key"], (x * CELL_SIZE, y * CELL_SIZE))
            elif value == TREASURE:
                win.blit(images["treasure"], (x * CELL_SIZE, y * CELL_SIZE))

# === إيجاد موقع العنصر في المتاهة ===
def find(maze, value):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == value:
                return (x, y)
    return None

# === إعادة تهيئة اللعبة ===
def reset_game():
    global MAZE, player_pos, enemy_pos, key_pos, treasure_pos
    global player_has_key, enemy_has_key, winner_text

    MAZE = generate_maze()
    player_pos = [0, 0]
    enemy_pos = [COLS - 1, ROWS - 1]
    key_pos = find(MAZE, KEY)
    treasure_pos = find(MAZE, TREASURE)
    player_has_key = False
    enemy_has_key = False
    winner_text = ""

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Maze Game - المستوى الثالث")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    images = load_images()

    reset_game()

    global player_pos, enemy_pos, key_pos, treasure_pos
    global player_has_key, enemy_has_key, winner_text

    running = True
    show_key = True
    frame_counter = 0
    max_end_frames = 180  # 3 ثوانٍ قبل إعادة التشغيل

    while running:
        win.fill(WHITE)
        draw_maze(win, MAZE, images, show_key)

        # رسم اللاعب والعدو
        draw_cell(win, player_pos[0], player_pos[1], DARK_BLUE)
        draw_cell(win, enemy_pos[0], enemy_pos[1], RED)

        # عرض صورة الفوز/الخسارة إن وُجدت
        if winner_text:
            image_key = "win" if "فاز" in winner_text else "lose"
            win.blit(images[image_key], (WIDTH // 2 - 100, HEIGHT // 2 - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    show_key = True
                    continue

                if not winner_text:
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT: dx = -1
                    elif event.key == pygame.K_RIGHT: dx = 1
                    elif event.key == pygame.K_UP: dy = -1
                    elif event.key == pygame.K_DOWN: dy = 1

                    new_x = player_pos[0] + dx
                    new_y = player_pos[1] + dy

                    if 0 <= new_x < COLS and 0 <= new_y < ROWS and MAZE[new_y][new_x] != OBSTACLE:
                        player_pos = [new_x, new_y]

                        if not player_has_key and tuple(player_pos) == key_pos:
                            player_has_key = True
                            show_key = False

                        prev_enemy = tuple(enemy_pos)
                        enemy_pos = list(get_enemy_move(MAZE, tuple(player_pos), tuple(enemy_pos), treasure_pos, last_enemy_pos=prev_enemy))

                        if not enemy_has_key and tuple(enemy_pos) == key_pos:
                            enemy_has_key = True
                            show_key = False

                        if player_has_key and tuple(player_pos) == treasure_pos:
                            winner_text = "اللاعب فاز!"
                        elif enemy_has_key and tuple(enemy_pos) == treasure_pos:
                            winner_text = "العدو فاز!"
                        elif tuple(enemy_pos) == tuple(player_pos):
                            winner_text = "العدو أمسك اللاعب!"

        # إعادة تشغيل تلقائية بعد نهاية اللعبة
        if winner_text:
            frame_counter += 1
            if frame_counter >= max_end_frames:
                reset_game()
                show_key = True
                frame_counter = 0

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
