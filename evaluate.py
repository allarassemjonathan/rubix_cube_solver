from rubix_cube import RubixCube


def evaluate_solve_rate(cube, n, num_trials=50, depth=10, node_limit=10**6, **kwargs):
    solved = 0
    total_nodes = [0]
    def update():
        total_nodes[0] += 1
        if n==3 and depth==8:
            if total_nodes[0] % 100 == 0:
                print(total_nodes[0])
        if total_nodes[0] > node_limit:
            raise Exception
        
    for _ in range(num_trials):
        total_nodes = [0]
        c = cube(n, **kwargs)
        c.scramble(depth)
        moves = []
        try:
            moves = c.solve(callback=update)
        except Exception:
            pass
        if c.evaluate(moves):
            print("solved!")
            solved += 1
    return solved / num_trials

def evaluate_node_count(cube: RubixCube.__class__, n, num_trials=50, depth=10, **kwargs):
    total_nodes = [0]
    def update():
        total_nodes[0] += 1
    for x in range(num_trials):
        print(x)
        c = cube(n, **kwargs)
        c.scramble(depth)
        c.solve(update)
    return total_nodes[0] / num_trials

def evaluate_n_moves(cube: RubixCube.__class__, n, num_trials=50, depth=10):
    total_moves = 0
    for _ in range(num_trials):
        c = cube(n)
        c.scramble(depth)
        moves = c.solve()
        total_moves += len(moves)
    return total_moves / num_trials

def print_eval(cube:RubixCube.__class__, n):
    print(f"For {str(cube.__name__)}'s Solver At {n}x{n}x{n}...")
    print(f"\tSolve Rate: {evaluate_solve_rate(cube, n)}")
    print(f"\tAverage Node Count: {evaluate_node_count(cube, n)}")
    print(f"\tAverage Num Moves: {evaluate_n_moves(cube, n)}")

if __name__ == "__main__":
    from rubix_cube import BeginnerCube
    print_eval(BeginnerCube, 3)