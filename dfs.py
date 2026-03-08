# ----------------------------DFS------------------------------------------------


# Directions 4-connexes : droite, bas, gauche, haut
# Garder un ordre coherent  avec BFS pour comparer
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def dfs(grid, start, goal):
    """
    DFS (Depth-First Search) itératif avec pile (LIFO).
    Retourne (path, visited_order) où :
      - path : liste [(r,c), ...] du chemin trouvé (PAS forcément le plus court),
               ou None si aucun chemin.
      - visited_order : liste des cellules réellement explorées (ordre de pop).

    Détails d’implémentation :
      - On empile des voisins non visités.
      - On marque 'visited' au moment de l’empilement (évite doublons).
      - On enregistre 'visited_order' au moment du dépilement (exploration réelle).
      - Pour respecter l’ordre visuel des directions, on empile les voisins
        en ordre inversé (ainsi, le premier dans DIRECTIONS est exploré en profondeur).
    """
    if start == goal:
        return [start], [start]

    stack = [start]  # pile LIFO
    visited = set([start])  # ensemble des positions déjà vues
    parent = {start: None}  # pour reconstruire le chemin
    visited_order = []  # ordre d’exploration (au moment du pop)

    while stack:
        r, c = stack.pop()
        visited_order.append((r, c))

        if (r, c) == goal:
            return reconstruct_path(parent, start, goal), visited_order

        # On matérialise les voisins pour les empiler en ordre inversé
        neighbors = list(get_neighbors(grid, r, c))
        # Inverser pour que le premier de DIRECTIONS soit exploré en profondeur en premier
        for nr, nc in reversed(neighbors):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                stack.append((nr, nc))

    # Aucun chemin trouvé
    return None, visited_order
