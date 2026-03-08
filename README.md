
# Devoir I – INF-5183 – Algorithmes de Recherche dans un Labyrinthe

**Université du Québec en Outaouais – DESS en Science de données et IA**  
**Cours : Fondements de l’Intelligence Artificielle (INF-5183)**  
**Étudiante : Naouel Yousfi — Session : Hiver 2026**

## Structure
- `maze.py` : génération d’un labyrinthe non parfait (chemin S→G garanti)
- `bfs.py` : BFS (chemin minimal en nombre de pas)
- `dfs.py` : DFS (pile LIFO, non optimal)
- `astar.py` : A* (heuristique Manhattan, optimal)
- `main.py` : point d’entrée (CLI)
- `requirements.txt` : dépendances (aucune si vide)

## Exécution
```bash
python main.py --size 16 --seed 42 --wall-prob 0.35 --algo all
