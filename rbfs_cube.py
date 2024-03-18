# RBFS Implementation - Kenneth Browder

from rubix_cube import rubix_cube
from bisect import insort
from collections import deque

BIG_NUMBER = 2**32

def gen_f(d):
    return lambda node: d + node.cost()

class RBFSCube(rubix_cube):
    #Based on pseudocode from: https://cdn.aaai.org/AAAI/1992/AAAI92-082.pdf

    def RBFS(self, callback=lambda: 0, v=None, b=BIG_NUMBER, d=0, visited=deque()):

        callback()  #for evaluation functions
        f = gen_f(d) #generate the cost function for this node depth

        # Added to avoid cycles
        if self in visited:
            return False, BIG_NUMBER
        
        # Generate v for starting node
        if v is None:
            v = self.cost()
        my_f = f(self)

        # PSEUDOCODE: IF f(N)>B, return f(N)
        if my_f > b:
            return False, my_f
        
        # PSEUDOCODE: IF N is a goal, EXIT algorithm
        if self.cube.is_done():
            self.print_if(1, "Found solution at depth", d)
            return [""], 0
        
        moves, children = zip(*self.children())

        # PSEUDOCODE: IF N has no children, return INFINITY
        #   irrelevant for Rubiks Cube Problem
        # if len(children) == 0:
        #     return BIG_NUMBER

        costs = [BIG_NUMBER] * len(children)

        # PSEUDOCODE: FOR each child Ni of N
        # PSEUDOCODE:   IF f(N) < V and f(Ni) < V THEN F[i] := V
        # PSEUDOCODE:   ELSE F[i] = Ni
        for i in range(len(children)):
            x = f(children[i])
            self.print_if(2, "Calculated f-value of", x, "for child")
            if my_f < v and x < v:
                costs[i] = v
            else:
                costs[i] = x
        
        # PSEUDOCODE: sort Ni and F[il in increasing order of F[i] 
        sorted_indices = sorted(range(len(children)), key=lambda x: costs[x])

        # PSEUDOCODE: IF only one child, FE21 := infinity
        #   irrelevant because b = constant > 1
        # if len(costs) == 1:
        #     costs.push(BIG_NUMBER)
        #     sorted_indices.append(1)

        

        if self.verbosity >= 2:
            print("Sorted costs are:", [costs[i] for i in sorted_indices])
        
        visited.append(self)
        self.print_if(1, "Visitng path", visited)

        # PSEUDOCODE: WHILE (FL-11 <= B)
        # PSEUDOCODE:   F[1] := RBFS(N1, F[1], MIN(B, F[2]))
        # PSEUDOCODE:   insert N1 and F[1] in sorted order 
        while costs[sorted_indices[0]] <=  b:
            l_i = sorted_indices.pop(0)
            self.print_if(2, "Evaluating path of cost", costs[l_i], "with upper bound", min(b, costs[sorted_indices[0]]))
            m, costs[l_i] = children[l_i].RBFS(callback, costs[l_i], min(b, costs[sorted_indices[0]]), d+1, visited)
            if m:
                return [moves[l_i], *m], 0
            insort(sorted_indices, l_i, key=lambda i: costs[i])
        visited.pop()

        # PSEUDOCODE: RETURN F[1]
        return False, costs[sorted_indices[0]]
    
    def solve(self, callback=lambda: 0):
        moves = self.RBFS(callback)[0][:-1]
        self.print_if(1, "Moves to solution are", moves)
        return moves

        
