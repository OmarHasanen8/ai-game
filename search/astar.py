import heapq
import math

def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def astar_path(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = [(heuristic(start, goal), 0, start)]
    parent = {}
    g_score = {start: 0}
    visited = set()
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1], len(visited)

        if current in visited:
            continue
        visited.add(current)

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and neighbor not in visited:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                    parent[neighbor] = current

    return [], len(visited)

def astar_search(maze, start, key, treasure):
    path1, v1 = astar_path(maze, start, key)
    path2, v2 = astar_path(maze, key, treasure)
    if path1 and path2:
        return path1 + path2[1:], v1 + v2
    return [], v1 + v2

