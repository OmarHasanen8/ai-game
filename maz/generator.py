import random

MAZ_SIZE = 10
OBSTACLE_RATIO = 0.2
START = 2
OBSTACLE = 1
EMPTY = 0
KEY = 3
TREASURE = 4

def generate_empty_maze(MAZ_SIZE):
    return [[EMPTY for _ in range(MAZ_SIZE)] for _ in range(MAZ_SIZE)]

def get_random_free_position(occupied):
    while True:
        pos = (random.randint(0, MAZ_SIZE - 1), random.randint(0, MAZ_SIZE - 1))
        if pos not in occupied:
            return pos

def place_item(maze, value, occupied):
    pos = get_random_free_position(occupied)
    maze[pos[0]][pos[1]] = value
    occupied.add(pos)

def generate_maze():
    maze = generate_empty_maze(MAZ_SIZE)
    occupied = set()  # إنشاء مجموعة فارغة بشكل صحيح

    # وضع نقطة البداية
    maze[0][0] = START
    occupied.add((0, 0))  # إضافة نقطة البداية إلى المواقع المشغولة كـ tuple

    # وضع المفتاح والكنز
    place_item(maze, KEY, occupied)
    place_item(maze, TREASURE, occupied)

    # وضع العوائق
    obstacle_count = int(MAZ_SIZE * MAZ_SIZE * OBSTACLE_RATIO)
    for _ in range(obstacle_count):
        place_item(maze, OBSTACLE, occupied)

    return maze

def print_maze(maze):
    print("\nGenerated Maze:")
    for row in maze:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    final_maze = generate_maze()
    print_maze(final_maze)
