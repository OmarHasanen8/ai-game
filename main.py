from maz.generator import generate_maze, print_maze
from search.BFS import bfs

# دالة للعثور على موقع عنصر معين داخل المتاهة (مثل المفتاح أو الكنز)
def find_in_maze(maze, target):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == target:
                return (i, j)
    return None

# تمييز المسار داخل نسخة من المتاهة باستخدام القيمة 8
def mark_path_on_maze(maze, path):
    marked = [row[:] for row in maze]  # نسخ المتاهة دون تعديل الأصل
    for x, y in path:
        if marked[x][y] == 0:
            marked[x][y] = 8  # تحديد المسار
    return marked

def main():
    # توليد متاهة عشوائية
    maze = generate_maze()
    print("The original maze:")
    print_maze(maze)

    # تحديد المواضع
    start = (0, 0)
    key = find_in_maze(maze, 3)
    treasure = find_in_maze(maze, 4)

    # التأكد من وجود المفتاح والكنز
    if not key or not treasure:
        print("No key or treasure found!")
        return

    # البحث عن المسار من البداية إلى المفتاح ثم إلى الكنز
    path = bfs(maze, start, key, treasure)

    if not path:
        print("\nNo path to the treasure found!")
    else:
        print("\nPath from start to key to treasure:")
        print(path)

        # عرض المتاهة مع تمييز المسار
        marked_maze = mark_path_on_maze(maze, path)
        print("\nMaze with path marking (8 represents the path):")
        print_maze(marked_maze)

if __name__ == "__main__":
    main()