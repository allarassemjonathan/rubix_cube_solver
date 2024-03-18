from rubix_cube import RubixCube
from bisect import insort
from collections import deque
from copy import deepcopy
BIG_NUMBER = 2**32

def gen_f(d):
    return lambda node: d + node.cost()

class RBFSCube(RubixCube):

    def child_after(self, move):
        c = deepcopy(self.cube)
        c.rotate(move)
        return self.__class__(self.N, c)
    
    def RBFS(self, callback=lambda: 0, v=None, b=BIG_NUMBER, d=0, visited=deque()):
        callback()
        f = gen_f(d)
        if self in visited:
            return False, BIG_NUMBER
        if v is None:
            v = self.cost()
        # print(len(visited))
        my_f = f(self)
        if my_f > b:
            return False, my_f
        if self.cube.is_done():
            print("Found solution at depth", d)
            return [""], 0
        moves, children = zip(*self.children(incl_action=True))
        # if len(children) == 0:
        #     return BIG_NUMBER
        costs = [BIG_NUMBER] * len(children)

        for i in range(len(children)):
            x = f(children[i])
            if my_f < v and x < v:
                costs[i] = v
            else:
                costs[i] = x
        
        sorted_indices = sorted(range(len(children)), key=lambda x: costs[x])

        # if len(costs) == 1:
        #     costs.push(BIG_NUMBER)
        #     sorted_indices.append(1)

        while costs[sorted_indices[0]] <=  b:
            l_i = sorted_indices.pop(0)
            visited.append(self)
            m, costs[l_i] = children[l_i].RBFS(callback, costs[l_i], min(b, costs[sorted_indices[0]]), d+1, visited)
            visited.pop()
            # print("Cost", costs[l_i])
            if m:
                return [moves[l_i], *m], 0
            insort(sorted_indices, l_i, key=lambda i: costs[i])
        
        return False, costs[sorted_indices[0]]
    
    def solve(self, callback=lambda: 0):
        return self.RBFS(callback)[0][:-1]

        
