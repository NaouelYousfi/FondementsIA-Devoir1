
# main.py
import argparse
import time

from maze import generate_maze, print_maze, overlay_visited, overlay_path
from bfs import bfs
from dfs import dfs
from astar import astar

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

def measure_algorithm(name, solve_fn, grid, start, goal):
    t0 = time.perf_counter()
    path, visited = solve_fn(grid, start, goal)
    t1 = time.perf_counter()
    return {
        "algo": name,
        "path": path,
        "visited": visited or [],
        "nodes": len(visited) if visited else 0,
        "length": (len(path) - 1) if path else None,
        "time_ms": (t1 - t0) * 1000.0,
    }

def print_comparison_table(results):
    header = ("Algorithme", "Noeuds", "Longueur", "Temps (ms)")
    rows = []
    for r in results:
        rows.append((
            r["algo"],
            str(r["nodes"]),
            str(r["length"]) if r["length"] is not None else "—",
            f"{r['time_ms']:.3f}",
        ))
    cols = list(zip(*([header] + rows)))
    widths = [max(len(x) for x in col) for col in cols]
    def fmt_row(row): return "  ".join(s.ljust(w) for s, w in zip(row, widths))
    print(fmt_row(header))
    print("-" * (sum(widths) + 2 * (len(widths) - 1)))
    for row in rows:
        print(fmt_row(row))

def main():
    parser = argparse.ArgumentParser(description="Labyrinthe + BFS / DFS / A* (Manhattan)")
    parser.add_argument("--size", type=int, default=16, help="Taille de la grille (défaut: 16)")
    parser.add_argument("--seed", type=int, default=42, help="Graine aléatoire (défaut: 42)")
    parser.add_argument("--wall-prob", type=float, default=0.35, help="Probabilité de mur interne [0..1]")
    parser.add_argument("--algo", type=str, default="all", choices=["bfs", "dfs", "astar", "all"],
                        help="Algorithme à exécuter")
    args, _ = parser.parse_known_args()

    # 1) Génération
    grid, start, goal = generate_maze(size=args.size, seed=args.seed, wall_probability=args.wall_prob)
    print(f"=== Labyrinthe {args.size}x{args.size} (seed={args.seed}, p_wall={args.wall_prob}) ===")
    print_maze(grid)
    print("\n" + "-" * 64 + "\n")

    # 2) Sélection des algorithmes
    algos = []
    if args.algo in ("bfs", "all"):   algos.append(("BFS", bfs))
    if args.algo in ("dfs", "all"):   algos.append(("DFS", dfs))
    if args.algo in ("astar", "all"): algos.append(("A* (Manhattan)", astar))

    results = []
    for name, fn in algos:
        print(f"=== {name} ===")
        stats = measure_algorithm(name, fn, grid, start, goal)
        results.append(stats)

        # Exploration
        print("Exploration — cases parcourues marquées 'p' :")
        explored_grid = overlay_visited(grid, stats["visited"], visited_char="p")
        print_maze(explored_grid)
        print()

        # Solution
        if stats["path"] is None:
            print("Solution : Aucun chemin trouvé.")
        else:
            print("Solution — chemin trouvé marqué '*' :")
            solved_grid = overlay_path(grid, stats["path"], path_char="*")
            print_maze(solved_grid)
            print("\n" + format_path_with_labels(stats["path"], start, goal))
        print("\n" + "-" * 64 + "\n")

    if len(results) > 1:
        print("--- Tableau comparatif ---")
        print_comparison_table(results)

if __name__ == "__main__":
    main()
