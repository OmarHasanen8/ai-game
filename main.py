from maz.generator import generate_maze, print_maze
from search.BFS import bfs as bfs_search
from search.DFS import dfs as dfs_search
from search.astar import astar_search
from search.animi_ai import get_enemy_move
import time

# إيجاد موقع عنصر في المتاهة
def find_in_maze(maze, target):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == target:
                return (i, j)
    return None

# تمييز المسار داخل نسخة من المتاهة
def mark_path_on_maze(maze, path, symbol=8):
    marked = [row[:] for row in maze]
    for x, y in path:
        if marked[x][y] == 0:
            marked[x][y] = symbol
    return marked

# تنفيذ خوارزمية وعرض النتائج
def run_and_report(name, search_fn, maze, start, key, treasure):
    start_time = time.perf_counter()
    path, visited = search_fn(maze, start, key, treasure)
    duration = time.perf_counter() - start_time

    print(f"\n=== {name} ===")
    if path:
        print(f"Path length: {len(path)}")
        print(f"Visited nodes: {visited}")
        print(f"Execution time: {duration:.6f} seconds")
        print_maze(mark_path_on_maze(maze, path))
    else:
        print(f"No path found using {name}.")

def simulate_enemy(maze, player_path, enemy_start, treasure, depth=4):
    print("\n=== Enemy Simulation (Alpha-Beta) ===")
    enemy_pos = enemy_start
    for step_num, player_pos in enumerate(player_path):
        enemy_pos = get_enemy_move(maze, player_pos, enemy_pos, treasure, use_alpha_beta=True, depth=depth)
        print(f"Step {step_num+1}: Enemy moved to {enemy_pos}")
        if enemy_pos == treasure:
            print("Enemy reached the treasure first!")
            return enemy_pos
        if enemy_pos == player_pos:
            print("Enemy caught the player!")
            return enemy_pos
    print("Player reached the treasure safely.")
    return enemy_pos

def main():
    maze = generate_maze()
    print("=== Original Maze ===")
    print_maze(maze)

    start = (0, 0)
    enemy_start = (len(maze) - 1, len(maze[0]) - 1)
    key = find_in_maze(maze, 3)
    treasure = find_in_maze(maze, 4)

    if not key or not treasure:
        print("Key or treasure not found!")
        return

    run_and_report("BFS", bfs_search, maze, start, key, treasure)
    run_and_report("DFS", dfs_search, maze, start, key, treasure)
    run_and_report("A*", astar_search, maze, start, key, treasure)

    # تجربة المسار الأفضل (A*) ومواجهة العدو
    path_to_key, _ = astar_search(maze, start, key, treasure)
    if not path_to_key:
        print("Player could not reach the key.")
        return

    path_to_treasure, _ = astar_search(maze, key, treasure, treasure)
    if not path_to_treasure:
        print("Player could not reach the treasure.")
        return

    full_player_path = path_to_key + path_to_treasure[1:]
    simulate_enemy(maze, full_player_path, enemy_start, treasure)

if __name__ == "__main__":
    main()
