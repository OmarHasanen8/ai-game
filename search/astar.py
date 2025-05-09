from maz.generator import generate_maze, print_maze
from search.BFS import BFS as bfs_search
from search.DFS import DFS as dfs_search
from search.astar import astar_path
import time

# دالة إيجاد موقع عنصر معين في المتاهة
def find_in_maze(maze, target):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == target:
                return (i, j)
    return None

# تمييز المسار داخل المتاهة بالقيمة 8
def mark_path_on_maze(maze, path):
    marked = [row[:] for row in maze]
    for x, y in path:
        if marked[x][y] == 0:
            marked[x][y] = 8
    return marked

def run_and_report(name, search_fn, maze, start, key, treasure):
    start_time = time.perf_counter()
    if name == "A*":
        path1, visited1 = astar_path(maze, start, key)
        path2, visited2 = astar_path(maze, key, treasure)
    else:
        path1, visited1 = search_fn(maze, start, key)
        path2, visited2 = search_fn(maze, key, treasure)

    exec_time = time.perf_counter() - start_time

    full_path = path1 + path2[1:] if path1 and path2 else []
    visited_total = visited1 + visited2

    print(f"\n=== {name} Result ===")
    if full_path:
        print(f"Path length: {len(full_path)}")
        print(f"Visited nodes: {visited_total}")
        print(f"Execution time: {exec_time:.6f} seconds")
        print_maze(mark_path_on_maze(maze, full_path))
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
        print("Key or treasure not found.")
        return

    run_and_report("BFS", bfs_search, maze, start, key, treasure)
    run_and_report("DFS", dfs_search, maze, start, key, treasure)
    run_and_report("A*", None, maze, start, key, treasure)

if __name__ == "__main__":
    main()