from collections import deque

def bfs_path(maze, start, goal):
    """
    تبحث عن أقصر مسار من start إلى goal داخل المتاهة باستخدام BFS.
    تعيد المسار كقائمة [(x1, y1), (x2, y2), ...] أو [] إذا لم يُوجد مسار.
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque()
    visited = set()
    parent = {}

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # أعلى، أسفل، يمين، يسار

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)

            if (0 <= nx < rows and 0 <= ny < cols and
                    maze[nx][ny] != 1 and
                    neighbor not in visited):

                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return []  # لم يتم العثور على مسار

def bfs(maze, start, key, treasure):
    """
    يعيد المسار الكامل من start → key → treasure داخل المتاهة باستخدام BFS.
    """
    path_to_key = bfs_path(maze, start, key)
    path_to_treasure = bfs_path(maze, key, treasure)

    if not path_to_key or not path_to_treasure:
        return []

    # حذف المفتاح المكرر عند دمج المسارين
    full_path = path_to_key + path_to_treasure[1:]
    return full_path







    
