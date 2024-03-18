import rubix_cube as r
from rbfs_cube import RBFSCube
import evaluate as e
c = r.BeginnerCube(3)

c.view()

print("Cost", c.cost())

c.scramble(100)

print("Cost", c.cost())

c.view()

print(c.solve())
print(e.evaluate_solve_rate(RBFSCube, 3, 10, 6, node_limit=3000))