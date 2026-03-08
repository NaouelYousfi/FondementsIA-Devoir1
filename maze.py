import random


# ============================================================
# 1. Fonction pour créer une grille vide de taille N x N
# ============================================================
def create_empty_grid(size):
    """
    Crée une grille remplie de murs (#).
    size: dimension de la grille (ex. 16)
    Retourne une liste de listes représentant le labyrinthe.
    """
    return [["#" for _ in range(size)] for _ in range(size)]


# ============================================================
# 2. Générer un chemin S -> G (droite ou bas, de façon aléatoire)
# ============================================================
def generate_random_path(start, goal):
    """
    Crée un chemin garanti entre start et goal
    en avançant aléatoirement soit à droite, soit en bas.

    start = (1,1)
    goal = (14,14) pour un 16x16

    Retourne la liste des positions du chemin.
    """
    r, c = start
    gr, gc = goal
    path = [(r, c)]

    while (r, c) != (gr, gc):
        moves = []

        # Peut-on aller à droite ?
        if c < gc:
            moves.append("right")

        # Peut-on aller en bas ?
        if r < gr:
            moves.append("down")

        # Choix aléatoire dans les moves possibles
        move = random.choice(moves)

        # Appliquer le mouvement choisi
        if move == "right":
            c += 1
        else:  # move == "down"
            r += 1

        path.append((r, c))

    return path


# ============================================================
# 3. Placer le chemin S -> G dans la grille
# ============================================================
def carve_path(grid, path):
    """
    Convertit un chemin sous forme de listes de positions
    en passages '.' dans la grille.
    """
    for (r, c) in path:
        grid[r][c] = "."


# ============================================================
# 4. Remplir l'intérieur avec des murs aléatoires
# ============================================================
def add_random_walls(grid, path, wall_probability=0.35):
    """
    Ajoute des murs (#) aléatoirement dans les cellules internes.
    - wall_probability : chance qu'une case devienne un mur.
    - Les cases du path ne sont jamais modifiées.
    - Les bords sont déjà des murs et ne doivent pas être modifiés.
    """
    size = len(grid)
    path_set = set(path)  # Pour vérification rapide

    for r in range(1, size - 1):
        for c in range(1, size - 1):

            # Ne pas modifier les cases du chemin
            if (r, c) in path_set:
                continue

            # Placer un mur avec une probabilité donnée
            if random.random() < wall_probability:
                grid[r][c] = "#"
            else:
                grid[r][c] = "."


# ============================================================
# 5. Fonction principale de génération du labyrinthe
# ============================================================
def generate_maze(size=16, seed=10):
    """
    Fonction principale :
    - initialise la seed
    - crée la grille
    - génère un chemin garanti
    - ajoute des murs aléatoires
    - place S et G
    - retourne la grille finale
    """
    random.seed(seed)  # Pour la reproductibilité

    # 1. Créer la grille
    grid = create_empty_grid(size)

    # 2. Définir start et goal
    start = (1, 1)
    goal = (size - 2, size - 2)

    # 3. Générer un chemin aléatoire garanti
    path = generate_random_path(start, goal)

    # 4. Carver ce chemin dans la grille
    carve_path(grid, path)

    # 5. Remplir l’intérieur aléatoirement
    add_random_walls(grid, path)

    # 6. Placer S et G
    grid[start[0]][start[1]] = "S"
    grid[goal[0]][goal[1]] = "G"

    return grid


# ============================================================
# 6. Fonction d'affichage du labyrinthe
# ============================================================
def print_maze(grid):
    """
    Affiche la grille de manière lisible.
    """
    for row in grid:
        print(" ".join(row))


# ============================================================
# 7. Exemple d'utilisation
# ============================================================
if __name__ == "__main__":
    print("Création du labyrinte final")
    maze = generate_maze(size=16, seed=10)
    print_maze(maze)
