from maz.generator import generate_maze, print_maze
from search.BFS import bfs as bfs_search
from search.DFS import dfs as dfs_search
from search.astar import astar_search
import time

# إيجاد موقع عنصر في المتاهة
def find_in_maze(maze, target):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == target:
                return (i, j)
    return None

# تمييز المسار داخل نسخة من المتاهة
def mark_path_on_maze(maze, path):
    marked = [row[:] for row in maze]
    for x, y in path:
        if marked[x][y] == 0:
            marked[x][y] = 8
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

def main():
    maze = generate_maze()
    print("=== Original Maze ===")
    print_maze(maze)

    start = (0, 0)
    key = find_in_maze(maze, 3)
    treasure = find_in_maze(maze, 4)

    if not key or not treasure:
        print("Key or treasure not found!")
        return

    run_and_report("BFS", bfs_search, maze, start, key, treasure)
    run_and_report("DFS", dfs_search, maze, start, key, treasure)
    run_and_report("A*", astar_search, maze, start, key, treasure)

if __name__ == "__main__":
    main()
