from rubix_cube import rubix_cube


def evaluate_solve_rate(cube: rubix_cube.__class__, n, num_trials=50, depth=10):
    solved = 0
    for _ in range(num_trials):
        c = cube(n)
        c.scramble(depth)
        moves = c.solve()
        if c.evaluate(moves):
            solved += 1
    return solved / num_trials

def evaluate_node_count(cube: rubix_cube.__class__, n, num_trials=50, depth=10):
    total_nodes = [0]
    def update():
        total_nodes[0] += 1
    for _ in range(num_trials):
        c = cube(n)
        c.scramble(depth)
        c.solve(update)
    return total_nodes[0] / num_trials

def evaluate_n_moves(cube: rubix_cube.__class__, n, num_trials=50, depth=10):
    total_moves = 0
    for _ in range(num_trials):
        c = cube(n)
        c.scramble(depth)
        moves = c.solve()
        total_moves += len(moves)
    return total_moves / num_trials

def print_eval(cube:rubix_cube.__class__,  n):
    print(f"For {str(cube.__name__)}'s Solver At {n}x{n}x{n}...")
    print(f"\tSolve Rate: {evaluate_solve_rate(cube, n)}")
    print(f"\tAverage Node Count: {evaluate_node_count(cube, n)}")
    print(f"\tAverage Num Moves: {evaluate_n_moves(cube, n)}")

if __name__ == "__main__":
    from rubix_cube import BeginnerCube
    print_eval(BeginnerCube, 3)