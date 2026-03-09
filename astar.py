# -----------------------------------A*------------------------------

# astar.py
from heapq import heappush, heappop
from maze import get_neighbors

def manhattan(a, b):
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)

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

def astar(grid, start, goal):
    """
    A* avec heuristique Manhattan (admissible dans une grille 4-connexe sans diagonales).
    Retourne (path, expanded_order).
    """
    if start == goal:
        return [start], [start]

    g_score = {start: 0}
    parent = {start: None}
    open_heap = []
    tie = 0  # pour stabiliser l'ordre en cas d'égalité de f(n)

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
            tentative_g = g_score[current] + 1  # coût uniforme
            if tentative_g < g_score.get(nb, float("inf")):
                g_score[nb] = tentative_g
                parent[nb] = current
                tie += 1
                heappush(open_heap, (tentative_g + manhattan(nb, goal), tentative_g, tie, nb))

    return None, expanded_order
