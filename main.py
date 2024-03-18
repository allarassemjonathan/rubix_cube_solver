from rbfs_cube import RBFSCube
import evaluate as e
print(e.evaluate_solve_rate(RBFSCube, 3, 10, 6, node_limit=3000))