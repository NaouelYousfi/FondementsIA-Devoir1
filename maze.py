# maze.py
import random

# Ordre d'exploration commun (droite, bas, gauche, haut)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# ------------------------------------------------------------
# Génération d'un labyrinthe non parfait (chemin S->G garanti)
# ------------------------------------------------------------
def create_empty_grid(size):
    return [["#" for _ in range(size)] for _ in range(size)]

def generate_random_path(start, goal):
    """
    Chemin S->G en choisissant aléatoirement droite/bas.
    Hypothèse : start=(1,1), goal=(size-2,size-2)
    """
    (r, c) = start
    (gr, gc) = goal
    path = [(r, c)]
    while (r, c) != (gr, gc):
        moves = []
        if c < gc: moves.append("right")
        if r < gr: moves.append("down")
        move = random.choice(moves)
        if move == "right":
            c += 1
        else:
            r += 1
        path.append((r, c))
    return path

def carve_path(grid, path):
    for (r, c) in path:
        grid[r][c] = "."

def add_random_walls(grid, path, wall_probability=0.35):
    """
    Place des murs au hasard à l’intérieur, sans toucher aux cases du chemin.
    Les bords restent des murs par construction.
    """
    n = len(grid)
    path_set = set(path)
    for r in range(1, n - 1):
        for c in range(1, n - 1):
            if (r, c) in path_set:
                continue
            grid[r][c] = "#" if random.random() < wall_probability else "."

def generate_maze(size=16, seed=42, wall_probability=0.35):
    random.seed(seed)
    grid = create_empty_grid(size)
    start = (1, 1)
    goal = (size - 2, size - 2)
    path = generate_random_path(start, goal)
    carve_path(grid, path)
    add_random_walls(grid, path, wall_probability=wall_probability)
    grid[start[0]][start[1]] = "S"
    grid[goal[0]][goal[1]] = "G"
    return grid, start, goal

# ------------------------------------------------------------
# Affichage / Overlays / Voisins
# ------------------------------------------------------------
def print_maze(grid):
    for row in grid:
        print(" ".join(row))

def overlay_visited(grid, visited, visited_char="p"):
    """
    Retourne une COPIE de la grille avec les cellules visitées marquées 'visited_char'.
    N'écrase pas S, G ni les murs '#'.
    """
    result = [row[:] for row in grid]
    for (r, c) in visited:
        if result[r][c] not in ("S", "G", "#"):
            result[r][c] = visited_char
    return result

def overlay_path(grid, path, path_char="*"):
    """
    Retourne une COPIE de la grille avec le chemin 'path' marqué par 'path_char' (sans écraser S/G).
    """
    result = [row[:] for row in grid]
    if path:
        for (r, c) in path:
            if result[r][c] not in ("S", "G"):
                result[r][c] = path_char
    return result

def get_neighbors(grid, r, c):
    """
    Voisins 4-connexes accessibles (dans les bornes et != mur '#').
    """
    n = len(grid)
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != "#":
            yield (nr, nc)
