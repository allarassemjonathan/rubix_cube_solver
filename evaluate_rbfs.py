from rbfs_cube import RBFSCube
from evaluate import evaluate_solve_rate, evaluate_node_count

# for cube_size in range(2,5):
#     print(f"n={cube_size}")
#     for depth in range(2,9):
#         print(f"\td={depth}")
#         print(f"\t\tSolve rate:", evaluate_solve_rate(RBFSCube, cube_size, num_trials=15, depth=depth, node_limit=5000))
#         print(f"\t\tAvg Node:", evaluate_node_count(RBFSCube, cube_size, num_trials=15, depth=depth, node_limit=5000))

print(f"\td={7}")
print(f"\t\tSolve rate:", evaluate_solve_rate(RBFSCube, 3, num_trials=15, depth=7, node_limit=5000))
print(f"\t\tAvg Node:", evaluate_node_count(RBFSCube, 3, num_trials=15, depth=7, node_limit=5000))
for cube_size in range(4,5):
    print(f"n={cube_size}")
    for depth in range(2,8):
        print(f"\td={depth}")
        print(f"\t\tSolve rate:", evaluate_solve_rate(RBFSCube, cube_size, num_trials=15, depth=depth, node_limit=5000))
        print(f"\t\tAvg Node:", evaluate_node_count(RBFSCube, cube_size, num_trials=15, depth=depth, node_limit=5000))