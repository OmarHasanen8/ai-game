def dfs_path(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = set()
    parent = {}

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1], len(visited)

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current

    return [], len(visited)

def dfs(maze, start, key, treasure):
    path1, v1 = dfs_path(maze, start, key)
    path2, v2 = dfs_path(maze, key, treasure)
    if path1 and path2:
        return path1 + path2[1:], v1 + v2
    return [], v1 + v2
