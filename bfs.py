#-----------------------------------------BFS----------------------------

# bfs.py
from collections import deque
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

def bfs(grid, start, goal):
    """
    BFS : trouve le plus court chemin (en nombre d'étapes) de start à goal.
    Retourne (path, visited_order).
    """
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
