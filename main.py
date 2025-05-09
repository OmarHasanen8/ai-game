from maz.generator import generate_maze, print_maze
from search.BFS import bfs as bfs_search
from search.DFS import dfs as dfs_search
import time

def find_in_maze(maze, target):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == target:
                return (i, j)
    return None

def mark_path_on_maze(maze, path):
    marked = [row[:] for row in maze]
    for x, y in path:
        if marked[x][y] == 0:
            marked[x][y] = 8
    return marked

def main():
    maze = generate_maze()
    print("The original maze:")
    print_maze(maze)

    start = (0, 0)
    key = find_in_maze(maze, 3)
    treasure = find_in_maze(maze, 4)

    if not key or not treasure:
        print("No key or treasure found!")
        return

    # --- BFS ---
    start_time = time.perf_counter()
    bfs_path, bfs_visited = bfs_search(maze, start, key, treasure)
    bfs_time = time.perf_counter() - start_time

    # --- DFS ---
    start_time = time.perf_counter()
    dfs_path, dfs_visited = dfs_search(maze, start, key, treasure)
    dfs_time = time.perf_counter() - start_time

    print("\n=== BFS Result ===")
    if bfs_path:
        print(f"Path length: {len(bfs_path)}")
        print(f"Visited nodes: {bfs_visited}")
        print(f"Execution time: {bfs_time:.6f} seconds")
        print_maze(mark_path_on_maze(maze, bfs_path))
    else:
        print("No path found with BFS.")

    print("\n=== DFS Result ===")
    if dfs_path:
        print(f"Path length: {len(dfs_path)}")
        print(f"Visited nodes: {dfs_visited}")
        print(f"Execution time: {dfs_time:.6f} seconds")
        print_maze(mark_path_on_maze(maze, dfs_path))
    else:
        print("No path found with DFS.")

if __name__ == "__main__":
    main()
