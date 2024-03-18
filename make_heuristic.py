import rubix_cube as r
import ida_star_solver as i
import json
import sys

heuristic = json.load(open('better_heuristic.json'))
# heuristic = None

# c = r.BeginnerCube(3)
MAX_DEPTH = 3
N = 4
s = i.IDAstarSolver(n=N, heuristic=heuristic, max_depth=MAX_DEPTH)

print(s.get_moves())
print(s.get_cube())
MAX_MOVES = 4
GENERATE_DB = True
if GENERATE_DB:
    hb = s.build_heuristic_db(
        cube=s.get_cube(), 
        actions=s.get_moves(),
        max_moves=MAX_MOVES)
    with open(f"heuristic_n_{N}_d_{MAX_MOVES+1}.json", "w+", encoding='utf-8') as f:
        json.dump(
            hb,
            f,
            ensure_ascii=False,
            indent=4
        )