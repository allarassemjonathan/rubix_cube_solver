import magiccube as magic
from magiccube.solver.basic.basic_solver import BasicSolver
from abc import ABC, abstractmethod 
from copy import deepcopy

BASIC_MOVES = ['L','U','F']

class rubix_cube(ABC):
    def __init__(self, n, cube = None) -> None:
        self.moves = []
        self.N = n
        if cube is None:
            self.cube = magic.Cube(n)
        else:
            self.cube = cube
        self._children = None
        for i in range(1,n+1):
            for m in BASIC_MOVES:
                self.moves.append(str(i) + m)
                self.moves.append(str(i) + m + '\'')

    def child_after(self, move):
        c = deepcopy(self.cube)
        c.rotate(move)
        return rubix_cube(self.N, c)
    
    def children(self):
        if self.children == None:
            self.children = [self.child_after(m) for m in self.moves]
        return self.children
    
    def scramble(self, depth):
        self.cube.scramble(depth)
    
    def view(self):
        print(self.cube)
    
    @abstractmethod
    def solve(self):
        pass

class BeginnerCube(rubix_cube):
    def solve(self):
        solver = BasicSolver(self.cube)
        actions = solver.solve()
        return actions