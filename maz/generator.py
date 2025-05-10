import random

MAZ_SIZE = 10
OBSTACLE_RATIO = 0.2
START = 2
OBSTACLE = 1
EMPTY = 0
KEY = 3
TREASURE = 4

def generate_empty_maze(size):
    return [[EMPTY for _ in range(size)] for _ in range(size)]

def get_random_free_position(occupied, size):
    while True:
        pos = (random.randint(0, size - 1), random.randint(0, size - 1))
        if pos not in occupied:
            return pos

def place_item(maze, value, occupied, size):
    pos = get_random_free_position(occupied, size)
    maze[pos[0]][pos[1]] = value
    occupied.add(pos)

def generate_maze():
    maze = generate_empty_maze(MAZ_SIZE)
    occupied = set()

    maze[0][0] = START
    occupied.add((0, 0))

    place_item(maze, KEY, occupied, MAZ_SIZE)
    place_item(maze, TREASURE, occupied, MAZ_SIZE)

    obstacle_count = int(MAZ_SIZE * MAZ_SIZE * OBSTACLE_RATIO)
    for _ in range(obstacle_count):
        place_item(maze, OBSTACLE, occupied, MAZ_SIZE)

    return maze

def print_maze(maze):
    print("\nGenerated Maze:")
    for row in maze:
        print(" ".join(map(str, row)))

