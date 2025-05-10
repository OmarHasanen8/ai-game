import math

def evaluate(player_pos, enemy_pos, treasure_pos):
    # دالة التقييم: الفرق بين المسافات إلى الكنز
    player_dist = abs(player_pos[0] - treasure_pos[0]) + abs(player_pos[1] - treasure_pos[1])
    enemy_dist = abs(enemy_pos[0] - treasure_pos[0]) + abs(enemy_pos[1] - treasure_pos[1])
    return player_dist - enemy_dist  # كلما كان العدو أقرب للكنز، كانت القيمة أفضل له

def get_neighbors(pos, maze):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    rows, cols = len(maze), len(maze[0])
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1:
            neighbors.append((nx, ny))
    return neighbors

def minimax(maze, depth, is_enemy_turn, player_pos, enemy_pos, treasure_pos):
    if depth == 0 or player_pos == treasure_pos or enemy_pos == player_pos:
        return evaluate(player_pos, enemy_pos, treasure_pos), enemy_pos

    if is_enemy_turn:
        max_eval = -math.inf
        best_move = enemy_pos
        for move in get_neighbors(enemy_pos, maze):
            eval_score, _ = minimax(maze, depth - 1, False, player_pos, move, treasure_pos)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = player_pos
        for move in get_neighbors(player_pos, maze):
            eval_score, _ = minimax(maze, depth - 1, True, move, enemy_pos, treasure_pos)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

def alpha_beta(maze, depth, is_enemy_turn, player_pos, enemy_pos, treasure_pos, alpha, beta):
    if depth == 0 or player_pos == treasure_pos or enemy_pos == player_pos:
        return evaluate(player_pos, enemy_pos, treasure_pos), enemy_pos

    if is_enemy_turn:
        max_eval = -math.inf
        best_move = enemy_pos
        for move in get_neighbors(enemy_pos, maze):
            eval_score, _ = alpha_beta(maze, depth - 1, False, player_pos, move, treasure_pos, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = player_pos
        for move in get_neighbors(player_pos, maze):
            eval_score, _ = alpha_beta(maze, depth - 1, True, move, enemy_pos, treasure_pos, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_enemy_move(maze, player_pos, enemy_pos, treasure_pos, use_alpha_beta=True, depth=4):
    if use_alpha_beta:
        _, move = alpha_beta(maze, depth, True, player_pos, enemy_pos, treasure_pos, -math.inf, math.inf)
    else:
        _, move = minimax(maze, depth, True, player_pos, enemy_pos, treasure_pos)
    return move
