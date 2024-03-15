import magiccube as magic
from magiccube.cube_move import CubeMove, CubeMoveType
from magiccube.solver.basic.basic_solver import BasicSolver
from abc import ABC, abstractmethod 
from copy import deepcopy

BASIC_MOVES = ['L','U','F']

def distance(coordA, coordB):
    return sum(abs(x-y) for x,y in zip(coordA, coordB))

class rubix_cube(ABC):
    def __init__(self, n, cube = None) -> None:
        self.moves = []
        self.N = n
        if cube is None:
            self.cube = magic.Cube(n)
        else:
            self.cube = cube
        self._children = None
        self.original_positions = {p: c for c,p in self.cube.get_all_pieces().items()}
        for i in range(1,n+1):
            for m in BASIC_MOVES:
                self.moves.append(str(i) + m)
                self.moves.append(str(i) + m + '\'')

    def child_after(self, move):
        c = deepcopy(self.cube)
        c.rotate(move)
        return rubix_cube(self.N, c)
    
    def cost(self):
        return sum(distance(c, self.original_positions[p]) for c, p in self.cube.get_all_pieces().items())
    
    def children(self):
        if self.children == None:
            self.children = [self.child_after(m) for m in self.moves]
        return self.children
    
    def scramble(self, depth):
        self.cube.scramble(depth)
    
    def view(self):
        print(self.cube)

    def evaluate(self, moves):
        c = deepcopy(self.cube)
        c.rotate([CubeMove.create(m) for m in moves])
        return c.is_done()
    
    @abstractmethod
    def solve(self, callback=lambda: 0) -> list[str]:
        pass

class BeginnerCube(rubix_cube):
    def solve(self, callback=lambda: 0):
        callback()
        solver = BasicSolver(deepcopy(self.cube))
        actions = solver.solve()
        #only works with 3x3x3 so can hardcode
        m = {
            'R': "3L'",
            "R'": '3L',
            'D': "3U'",
            "D'": '3U',
            "B": "3F'",
            "B'": '3F'
        }
        # print("Solver solved ", self.cube.is_done())
        return [m.get(str(action),str(action)) for action in actions]