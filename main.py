from maz.generator import generate_maze, print_maze
from search.BFS import bfs
from search.DFS import dfs
from search.astar import astar_path
import time

# إيجاد مواقع العناصر
def find(maze, target):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == target:
                return (i, j)
    return None

# تمييز المسار بالقيمة 8
def mark_path(maze, path):
    marked = [row[:] for row in maze]
    for x, y in path:
        if marked[x][y] == 0:
            marked[x][y] = 8
    return marked

# تنفيذ خوارزمية وقياس الزمن والنتائج
def run_algo(name, fn, maze, start, key, treasure):
    start_time = time.perf_counter()
    if name == "A*":
        path1, visited1 = astar_path(maze, start, key)
        path2, visited2 = astar_path(maze, key, treasure)
    else:
        path1, visited1 = fn(maze, start, key)
        path2, visited2 = fn(maze, key, treasure)
    elapsed = time.perf_counter() - start_time

    path = path1 + path2[1:] if path1 and path2 else []
    return {
        "name": name,
        "path": path,
        "visited": visited1 + visited2,
        "time": elapsed
    }

def report(result):
    print(f"\n=== {result['name']} ===")
    if result['path']:
        print(f"Path length: {len(result['path'])}")
        print(f"Visited nodes: {result['visited']}")
        print(f"Execution time: {result['time']:.6f}s")
    else:
        print("Path not found.")

def main():
    maze = generate_maze()
    print("=== Generated Maze ===")
    print_maze(maze)

    start = (0, 0)
    key = find(maze, 3)
    treasure = find(maze, 4)

    if not key or not treasure:
        print("Missing key or treasure.")
        return

    results = [
        run_algo("BFS", bfs, maze, start, key, treasure),
        run_algo("DFS", dfs, maze, start, key, treasure),
        run_algo("A*", None, maze, start, key, treasure),
    ]

    for res in results:
        report(res)

    print("\n=== Marked Path for A* (if found) ===")
    a_star_result = next((r for r in results if r['name'] == "A*"), None)
    if a_star_result and a_star_result["path"]:
        print_maze(mark_path(maze, a_star_result["path"]))

if __name__ == "__main__":
    main()
