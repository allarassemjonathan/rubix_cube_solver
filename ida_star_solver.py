import time
from tqdm import tqdm
from rubix_cube import RubixCube, cube_str
from copy import deepcopy
import math
import sys
import random
import json

mapping = {
    2: 'heuristic_n_2_d_6.json',
    3: 'heuristic_n_3_d_6.json',
    4: 'heuristic_n_4_d_5.json'
}

class IDAstarSolver(RubixCube):
    def __init__(self, n, max_depth, heuristic=None, cube=None) -> None:
        super().__init__(n, cube)
        
        self.max_depth = max_depth
        self.threshold = max_depth
        self.min_threshold = None
        if heuristic is None:
            self.heuristic = json.load(open(mapping[n], "r"))
        else:
            self.heuristic = heuristic
        self.solve_moves = []
        self.num_orderings = 30
        self.random_ordering = [random.sample([j for j in range(len(self.moves))], len(self.moves)) for i in range(self.num_orderings)]


    # Generate next child given a cube and a move
    def child_after(self, move, cube=None):
        c = deepcopy(self.cube) if cube is None else deepcopy(cube)
        c.rotate(move)
        return c
    
    def solve(self, callback=lambda: 0, verbosity:int=0) -> list[str]:

        #Taken from line 27 of solver.py https://github.com/bellerb/RubiksCube_Solver
        while True:

            self.print_if(1, f"Starting search with threshold of {self.threshold}")
            # Calls the serach function with the starting cube, an initial
            #   g-score of 1, and a callback to keep track of node count
            stat = self.search(self.cube, 1, callback=callback, verbosity=0)

            # if search returns true, return the moves that got to the soln
            if stat:
                return self.solve_moves
            
            # otherwise, try again and update the threshold value for pruning sake.
            self.solve_moves = []
            self.threshold = self.min_threshold


    def search(self, cube_state, g_score, depth=0, callback=lambda: 0, verbosity=0):
        callback()
        """
        Code in this section is from https://github.com/bellerb/RubiksCube_Solver
        Typed out, and adapted to use our rubiks cube library.
        Part of it is very similar to the code from that repo, but much of it had to be 
        changed to work with our code.
        """
        # make a deep copy 
        # curr_cube = deepcopy(cube_state)

        # check if the current cube is solved
        if cube_state.is_done():
            return True
        
        # prune any paths that have a length longer than the min threshold
        #   previously found. This is a lot of the iterative deepening part of IDA*
        elif len(self.solve_moves) >= self.threshold:
            self.print_if(2, f"Pruning with len(self.solve_moves) = {len(self.solve_moves)} and self.threshold = {self.threshold}")
            return False

        # Initial min val
        minimum_val = math.inf

        # Var to store the best action so far found
        curr_best_action = None
        children = self.children(incl_action=True, cube=cube_state)

        if verbosity >= 2:
            print(f"Children of current best action: {children}")
        # pick a random ordering of the children
        order_idx = random.randint(0, self.num_orderings-1)

        # Iterate through the children
        for child_num in self.random_ordering[order_idx]:
            
            # unpack the cube, and the move that took it there
            ida_solver, move = children[child_num]
            
            # Check solved again, and if solved, append current move and return True
            if ida_solver.is_done():
                self.solve_moves.append(move)
                return True
            
            # stringify the cube for pattern bg matching
            str_cube = cube_str(ida_solver)
            
            # This is the heuristic score, starting at the max depth
            h_score = self.max_depth  

            # if the current cube config is in the pattern db, retrieve the value 
            #   from the db. This pattern db tells of how many moves until solved.
            if str_cube in self.heuristic:
                h_score = self.heuristic[str_cube]
                
            else:
                # could possibly implement another heuristic here for cubes
                #  not in the pattern db
                pass

            # bound h_score to max depth
            #   (particularly valuable if using another heuristic besides 
            #       pattern db)
            if h_score > self.max_depth:
                h_score = self.max_depth

            # Calculate the f-score using the g-score (passed down recursively)
            #   and the h-score
            f_score = g_score + h_score

            # Update the min val seen and the best move possible if f_score is 
            #   less than the curr min value. 
            if f_score < minimum_val:
                minimum_val = f_score
                curr_best_action = [(ida_solver, move)]
            elif f_score == minimum_val:
                if curr_best_action is None:
                    curr_best_action = [(ida_solver, move)]
                else:
                    curr_best_action.append((ida_solver, move))

            self.print_if(2, f"F-SCORE: {f_score}\n MIN-VAL: {minimum_val}\n G-SCORE: {g_score}\n H-SCORE: {h_score}\n CURR-BEST-ACTIONS: {[i[1] for i in curr_best_action]}\n DEPTH: {depth}")

        if curr_best_action is not None:

            # update the min_threshold for later pruning on further iterations
            if self.min_threshold is None or minimum_val < self.min_threshold:
                self.min_threshold = minimum_val

            self.print_if(1, f"Current Best Action List: {curr_best_action}")
            # pick one of the best next moves and add it to curr path
            next_move = random.choice(curr_best_action)
            self.solve_moves.append(next_move[1])

            # recurse and check its children
            status = self.search(next_move[0], g_score + minimum_val, depth=depth+1, callback=callback)
            if status:
                return status
                
        return False
        
    def build_heuristic_db(self, cube, actions, max_moves = 20, heuristic = None):
        """
        Input: state - string representing the current state of the cube
            actions -list containing tuples representing the possible actions that can be taken
            max_moves - integer representing the max amount of moves alowed (default = 20) [OPTIONAL]
            heuristic - dictionary containing current heuristic map (default = None) [OPTIONAL]
        Description: create a heuristic map for determining the best path for solving a rubiks cube
        Output: dictionary containing the heuristic map
        """
        if heuristic is None:
            heuristic = {cube_str(cube): 0}
        que = [(cube, 0)]
        node_count = sum([len(actions) ** (x + 1) for x in range(max_moves + 1)])
        with tqdm(total=node_count, desc='Heuristic DB') as pbar:
            while True:
                if not que:
                    break
                s, d = que.pop()
                if d > max_moves:
                    continue
                for child in self.children(cube=s):
                    a_str = cube_str(child)
                    if a_str not in heuristic or heuristic[a_str] > d + 1:
                        heuristic[a_str] = d + 1
                    que.append((child, d+1))
                    pbar.update(1)
        return heuristic