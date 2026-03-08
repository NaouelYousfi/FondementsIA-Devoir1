
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py — Projet Labyrinthe : Génération + BFS / DFS / A* (Manhattan)
Affichages demandés :
  - Exploration : cases parcourues marquées 'p'
  - Solution    : chemin trouvé marqué '*'
  - Chemin      : "Chemin : S(r, c) -> ... -> G(r, c)"
Statistiques :
  - Nombre de nœuds explorés
  - Longueur du chemin
  - Temps d'exécution (ms)
Tableau comparatif optionnel pour BFS, DFS, A*.
"""

import argparse
import time
import random
from collections import deque
from heapq import heappush, heappop

# ============================================================
# Génération du labyrinthe (chemin S->G garanti, puis murs aléatoires)
# ============================================================

def create_empty_grid(size):
    return [["#" for _ in range(size)] for _ in range(size)]



def generate_random_path(start, goal):
    """
    Chemin S->G en choisissant aléatoirement droite/bas, sans sortir de la grille.
    start=(1,1), goal=(n-2, n-2).
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
    random.seed(seed)
    path = generate_random_path(start, goal)
    carve_path(grid, path)
    random.seed(seed)
    add_random_walls(grid, path, wall_probability=wall_probability)
    grid[start[0]][start[1]] = "S"
    grid[goal[0]][goal[1]] = "G"
    return grid, start, goal

# ============================================================
# Outils d’affichage / superposition
# ============================================================

def print_maze(grid):
    for row in grid:
        print(" ".join(row))

def overlay_visited(grid, visited, visited_char="p"):
    result = [row[:] for row in grid]
    for (r, c) in visited:
        if result[r][c] not in ("S", "G", "#"):
            result[r][c] = visited_char
    return result

def overlay_path(grid, path, path_char="*"):
    result = [row[:] for row in grid]
    if path:
        for (r, c) in path:
            if result[r][c] not in ("S", "G"):
                result[r][c] = path_char
    return result

def format_path_with_labels(path, start, goal):
    if not path:
        return "Chemin : (aucun)"
    parts = []
    for i, (r, c) in enumerate(path):
        if i == 0 and (r, c) == start:
            parts.append(f"S({r}, {c})")
        elif i == len(path) - 1 and (r, c) == goal:
            parts.append(f"G({r}, {c})")
        else:
            parts.append(f"({r}, {c})")
    return "Chemin : " + " -> ".join(parts)

# ============================================================
# Algorithmes de recherche : BFS, DFS, A*
# ============================================================

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # droite, bas, gauche, haut

def get_neighbors(grid, r, c):
    n = len(grid)
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != "#":
            yield (nr, nc)

def reconstruct_path(parent, start, goal):
    if goal not in parent:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path if path and path[0] == start else None

# ----- BFS -----
def bfs(grid, start, goal):
    if start == goal:
        return [start], [start]
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    visited_order = []
    while queue:
        node = queue.popleft()
        visited_order.append(node)
        if node == goal:
            return reconstruct_path(parent, start, goal), visited_order
        for nb in get_neighbors(grid, *node):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                queue.append(nb)
    return None, visited_order

# ----- DFS -----
def dfs(grid, start, goal):
    if start == goal:
        return [start], [start]
    stack = [start]
    visited = set([start])
    parent = {start: None}
    visited_order = []
    while stack:
        node = stack.pop()
        visited_order.append(node)
        if node == goal:
            return reconstruct_path(parent, start, goal), visited_order
        neighbors = list(get_neighbors(grid, *node))
        for nb in reversed(neighbors):  # pour respecter l’ordre DIRECTIONS
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                stack.append(nb)
    return None, visited_order

# ----- A* (Manhattan) -----
def manhattan(a, b):
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)

def astar(grid, start, goal):
    if start == goal:
        return [start], [start]
    g_score = {start: 0}
    parent = {start: None}
    open_heap = []
    tie = 0
    heappush(open_heap, (manhattan(start, goal), 0, tie, start))
    closed = set()
    expanded_order = []
    while open_heap:
        f, gcur, _, current = heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        expanded_order.append(current)
        if current == goal:
            return reconstruct_path(parent, start, goal), expanded_order
        for nb in get_neighbors(grid, *current):
            if nb in closed:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nb, float("inf")):
                g_score[nb] = tentative_g
                parent[nb] = current
                tie += 1
                heappush(open_heap, (tentative_g + manhattan(nb, goal), tentative_g, tie, nb))
    return None, expanded_order

# ============================================================
# Mesures et tableau comparatif
# ============================================================

def measure_algorithm(name, solve_fn, grid, start, goal):
    t0 = time.perf_counter()
    path, visited = solve_fn(grid, start, goal)
    t1 = time.perf_counter()
    nodes = len(visited) if visited else 0
    length = (len(path) - 1) if path else None
    time_ms = (t1 - t0) * 1000.0
    return {
        "algo": name,
        "nodes": nodes,
        "length": length,
        "time_ms": time_ms,
        "path": path,
        "visited": visited,
    }

def print_comparison_table(results):
    header = ("Algorithme", "Noeuds", "Longueur", "Temps (ms)")
    rows = []
    for r in results:
        length_str = str(r["length"]) if r["length"] is not None else "—"
        rows.append((
            r["algo"],
            str(r["nodes"]),
            length_str,
            f"{r['time_ms']:.3f}",
        ))
    cols = list(zip(*([header] + rows)))
    widths = [max(len(x) for x in col) for col in cols]
    def fmt_row(row): return "  ".join(s.ljust(w) for s, w in zip(row, widths))
    print(fmt_row(header))
    print("-" * (sum(widths) + 2 * (len(widths) - 1)))
    for row in rows:
        print(fmt_row(row))

# ============================================================
# Programme principal (CLI)
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Génération de labyrinthe + BFS / DFS / A* avec affichages et stats."
    )
    parser.add_argument("--size", type=int, default=16, help="Taille de la grille NxN (défaut: 16)")
    parser.add_argument("--seed", type=int, default=42, help="Graine aléatoire (défaut: 42)")
    parser.add_argument("--wall-prob", type=float, default=0.35,
                        help="Probabilité de mur interne [0..1] (défaut: 0.35)")
    parser.add_argument("--algo", type=str, default="all",
                        choices=["bfs", "dfs", "astar", "all"],
                        help="Algorithme à exécuter (défaut: all)")
    parser.add_argument("--no-compare", action="store_true",
                        help="Ne pas afficher le tableau comparatif (utile si --algo != all)")
    parser.add_argument("--export", action="store_true",
                        help="Export des affichages dans des fichiers .txt")
    #args = parser.parse_args()
    args, _ = parser.parse_known_args()
    # Génération
    maze, start, goal = generate_maze(size=args.size, seed=args.seed, wall_probability=args.wall_prob)

    print(f"=== Labyrinthe {args.size}x{args.size} (seed={args.seed}, p_wall={args.wall_prob}) ===")
    print_maze(maze)
    print("\n" + "-" * 64 + "\n")

    # Sélection de l’algo
    algos = []
    if args.algo in ("bfs", "all"):
        algos.append(("BFS", bfs))
    if args.algo in ("dfs", "all"):
        algos.append(("DFS", dfs))
    if args.algo in ("astar", "all"):
        algos.append(("A* (Manhattan)", astar))

    results = []
    for name, fn in algos:
        print(f"=== {name} ===")
        stats = measure_algorithm(name, fn, maze, start, goal)
        results.append(stats)

        # Exploration : p
        print("Exploration — cases parcourues marquées 'p' :")
        explored = stats["visited"] or []
        maze_vis = overlay_visited(maze, explored, visited_char="p")
        print_maze(maze_vis)
        if args.export:
            with open(f"exploration_{name.replace(' ', '_')}.txt", "w", encoding="utf-8") as f:
                for row in maze_vis: f.write(" ".join(row) + "\n")
        print("\n")

        # Solution : *
        if stats["path"] is None:
            print("Solution : Aucun chemin trouvé.")
        else:
            print("Solution — chemin trouvé marqué '*' :")
            maze_sol = overlay_path(maze, stats["path"], path_char="*")
            print_maze(maze_sol)
            if args.export:
                with open(f"solution_{name.replace(' ', '_')}.txt", "w", encoding="utf-8") as f:
                    for row in maze_sol: f.write(" ".join(row) + "\n")
            print("\n" + format_path_with_labels(stats["path"], start, goal))
        print("\n" + "-" * 64 + "\n")

    # Tableau comparatif
    if not args.no_compare and len(results) > 1:
        print("--- Tableau comparatif ---")
        print_comparison_table(results)

if __name__ == "__main__":
    main()
