import rubix_cube as r
import ida_star_solver as i
import json
import sys
import evaluate

heuristic = json.load(open('heuristic_n_2_d_6.json'))
# heuristic = None

mapping = {
    2: 'heuristic_n_2_d_6.json',
    3: 'heuristic_n_3_d_6.json',
    4: 'heuristic_n_4_d_5.json'
}
# c = r.BeginnerCube(3)
MAX_DEPTH = 4
s = i.IDAstarSolver(n=3, heuristic=heuristic, max_depth=MAX_DEPTH)
moves = s.scramble(MAX_DEPTH)

solve_moves = s.solve()
s.evaluate(solve_moves)

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

# m = {
#             'R': "3L'",
#             "R'": '3L',
#             'D': "3U'",
#             "D'": '3U',
#             "B": "3F'",
#             "B'": '3F'
#         }
        # print("Solver solved ", self.cube.is_done())
# print([m.get(str(action), str(action)) for action in moves])
# print(moves)
# print(node_count)

MAX_MOVES = 4
GENERATE_DB = False
if GENERATE_DB:
    hb = s.build_heuristic_db(
        cube=s.get_cube(), 
        actions=s.get_moves(),
        max_moves=MAX_MOVES)
    with open("better_heuristic.json", "w+", encoding='utf-8') as f:
        json.dump(
            hb,
            f,
            ensure_ascii=False,
            indent=4
        )
# sys.exit()
# s.solve()
s.view()

#
# c.view()

# print("Cost", c.cost())

# c.scramble(100)

# print("Cost", c.cost())

# c.view()

# print(c.solve())