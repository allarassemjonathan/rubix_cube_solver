import magiccube as magic
from magiccube.cube_move import CubeMove, CubeMoveType
from magiccube.solver.basic.basic_solver import BasicSolver
from abc import ABC, abstractmethod 
from copy import deepcopy

BASIC_MOVES = ['L','U','F']

def distance(coordA, coordB):
    # print(coordA, coordB)
    return sum(abs(x-y) for x,y in zip(coordA, coordB))

class rubix_cube(ABC):
    __slots__ = ('moves', 'N', 'cube', '_children', 'original_positions')
    def __init__(self, n, cube = None) -> None:
        self.moves = []
        self.N = n
        if cube is None:
            self.cube = magic.Cube(n)
        else:
            self.cube = cube
        self._children = None
        self.original_positions = {p.get_piece_colors(True): c for c,p in magic.Cube(n).get_all_pieces().items()}
        for i in range(1,n+1):
            for m in BASIC_MOVES:
                self.moves.append(str(i) + m)
                self.moves.append(str(i) + m + '\'')

    def child_after(self, move):
        c = deepcopy(self.cube)
        c.rotate(move)
        return self.__class__(self.N, c)
    
    def cost(self):
        return sum(distance(c, self.original_positions[p.get_piece_colors(True)]) for c, p in self.cube.get_all_pieces().items())/(self.N**2)
    
    def children(self):
        if self._children == None:
            self._children = [(m, self.child_after(m)) for m in self.moves]
        return self._children
    
    def scramble(self, depth):
        return self.cube.scramble(depth)
    
    def view(self):
        print(self.cube)

    def evaluate(self, moves):
        c = deepcopy(self.cube)
        c.rotate([CubeMove.create(m) for m in moves])
        return c.is_done()
    
    @abstractmethod
    def solve(self, callback=lambda: 0) -> list[str]:
        pass

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, rubix_cube):
            s_p = self.cube.get_all_pieces()
            v_p = __value.cube.get_all_pieces()
            return all(s_p[k].get_piece_colors() == v_p[k].get_piece_colors() for k in s_p.keys())
        return False

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