#-----------------------------------------BFS----------------------------


from collections import deque

# Directions 4-connexes : droite, bas, gauche, haut
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

#---------------BFS-------------------------
def bfs(grid, start, goal):
    """
    BFS : trouve le plus court chemin (en nombre d'étapes) de start à goal.
    Retourne (path, visited_order) où :
      - path : liste [(r,c), ...] ou None si pas de chemin
      - visited_order : liste des cases explorées (dans l'ordre de dépilement)
    """
    if start == goal:
        return [start], [start]

    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    visited_order = []

    while queue:
        r, c = queue.popleft()
        visited_order.append((r, c))

        if (r, c) == goal:
            return reconstruct_path(parent, start, goal), visited_order

        for nr, nc in get_neighbors(grid, r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))

    return None, visited_order

