import rubix_cube as r
from ida_star_solver import IDAstarSolver
import json

from rbfs_cube import RBFSCube
import evaluate as e

# heuristic = json.load(open('heuristic_n_2_d_6.json'))
# heuristic = None
MAX_DEPTH = 5 # can be in range 0-8, not guaranteed to work for anything above pattern db max
CUBE_SIZE = 3 # 2, 3 or 4
s = IDAstarSolver(n=CUBE_SIZE, max_depth=MAX_DEPTH)

moves = s.scramble(MAX_DEPTH)
solve_moves = s.solve()
print(solve_moves)
s.evaluate(solve_moves)
s.view()

print(e.evaluate_solve_rate(RBFSCube, 3, 10, 6, node_limit=3000))
# print(moves)
# print(i.cube_str(s.cube))

# s.view()
# NUM_TRIALS = 15
# with open("out3.txt", "w+") as f:
#     for n in range(4, 5):
#         heuristic = json.load(open(mapping[n], "r"))
#         for depth in range(2, 9):
            
#             print(f"Size Cube: {n}, Max Depth: {depth} Trials: {NUM_TRIALS}")
#             out = evaluate.evaluate_node_count(i.IDAstarSolver, n=n, num_trials=NUM_TRIALS, depth=depth, heuristic=heuristic, max_depth=depth)
#             print(out)
#             f.write(f"{out}\n")

# NUM_TRIALS = 15
# with open("out2.txt", "w+") as f:
#     for n in range(4, 5):
#         heuristic = json.load(open(mapping[n], "r"))
#         for depth in range(2, 9):
            
#             print(f"Size Cube: {n}, Max Depth: {depth} Trials: {NUM_TRIALS}")
#             out = evaluate.evaluate_solve_rate(i.IDAstarSolver, n=n, num_trials=NUM_TRIALS, depth=depth, node_limit=1000, heuristic=heuristic, max_depth=depth)
#             print(out)
#             f.write(f"{out}\n")
# moves = s.solve(callback=update)


