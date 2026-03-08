# -----------------------------------A*------------------------------

from heapq import heappush, heappop

# Directions 4-connexes : droite, bas, gauche, haut
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def manhattan(a, b):
    """
    Heuristique h(n) : distance de Manhattan entre a=(r1,c1) et b=(r2,c2)
      h(n) = |r1 - r2| + |c1 - c2|
   """
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)


def astar(grid, start, goal):
    """
    A* (A-Star) — Recherche informée avec file de priorité (tas binaire).
    Fonction d’évaluation : f(n) = g(n) + h(n)
      - g(n) : coût réel depuis start (ici coût uniforme 1 par déplacement)
      - h(n) : heuristique de Manhattan vers goal

    Retourne (path, expanded_order) :
      - path : liste [(r,c), ...] du chemin optimal (ou None)
      - expanded_order : ordre des cellules réellement EXPANSÉES (dépilées du tas)
                         utile pour visualiser l'exploration (marquées 'p')
    """
    if start == goal:
        return [start], [start]

    # g_score : meilleur coût connu pour atteindre un noeud
    g_score = {start: 0}
    # parent : pour reconstruire le chemin
    parent = {start: None}

    # Tas de l'open set : tuples (f, g, tie, (r,c))
    # - 'tie' sert de briseur d'égalité pour stabilité (compteur simple)
    open_heap = []
    tie = 0
    heappush(open_heap, (manhattan(start, goal), 0, tie, start))

    # Closed set : noeuds déjà EXPANSÉS (on n’y revient plus)
    closed = set()

    # Pour la visualisation de l'exploration (ordre d’expansion)
    expanded_order = []

    while open_heap:
        f, gcur, _, current = heappop(open_heap)

        # Si déjà traité (présent dans closed), on saute (entrée obsolète)
        if current in closed:
            continue

        # On EXPANSE 'current' maintenant
        closed.add(current)
        expanded_order.append(current)

        # Test de but
        if current == goal:
            return reconstruct_path(parent, start, goal), expanded_order

        cr, cc = current
        for nr, nc in get_neighbors(grid, cr, cc):
            neighbor = (nr, nc)
            if neighbor in closed:
                continue

            tentative_g = g_score[current] + 1  # coût uniforme

            # Si meilleur chemin vers 'neighbor' trouvé, on met à jour
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                tie += 1
                fscore = tentative_g + manhattan(neighbor, goal)
                heappush(open_heap, (fscore, tentative_g, tie, neighbor))

    # Aucune solution atteinte
    return None, expanded_order
