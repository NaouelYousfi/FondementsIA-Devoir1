# ----------------------------DFS------------------------------------------------

# dfs.py
from maze import get_neighbors

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

def dfs(grid, start, goal):
    """
    DFS : recherche en profondeur (pile LIFO).
    Retourne (path, visited_order). Chemin non garanti minimal.
    """
    if start == goal:
        return [start], [start]

    stack = [start]
    visited = {start}
    parent = {start: None}
    visited_order = []

    while stack:
        node = stack.pop()
        visited_order.append(node)
        if node == goal:
            return reconstruct_path(parent, start, goal), visited_order

        neighbors = list(get_neighbors(grid, *node))
        # Respecte l'ordre de DIRECTIONS (droite, bas, gauche, haut)
        for nb in reversed(neighbors):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                stack.append(nb)

    return None, visited_order
