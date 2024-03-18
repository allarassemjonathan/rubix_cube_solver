import magiccube as magic
from magiccube.cube_move import CubeMove, CubeMoveType
from magiccube.solver.basic.basic_solver import BasicSolver
from abc import ABC, abstractmethod
from copy import deepcopy
from magiccube.cube import Face, Color

BASIC_MOVES = ['L', 'U', 'F']

# Compute the manhattan distance between two tuples

def cube_str(cube):
    face_order = [Face.D, Face.R, Face.F, Face.L, Face.B, Face.U]
    return "".join(color.name.lower() for face in face_order for color in cube.get_face_flat(face))
def distance(coordA, coordB):
    return sum(abs(x-y) for x,y in zip(coordA, coordB))

class RubixCube(ABC):
    __slots__ = ('moves', 'N', 'cube', '_children', 'original_positions', 'verbosity')
    def __init__(self, n, cube = None, verbosity = 0, beta=18, **kwargs) -> None:
        self.verbosity = verbosity
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

    def print_if(self, v=0, *args, **kwargs):
        if self.verbosity >= v:
            print(*args, **kwargs)
    
    def cost(self):
        return sum(distance(c, self.original_positions[p.get_piece_colors(True)]) for c, p in self.cube.get_all_pieces().items())/(self.N**2)

    @abstractmethod
    def child_after(self, move, cube=None):
        pass

    def get_cube(self):
        return self.cube

    def get_size(self):
        return self.N

    def children(self, incl_action=False, cube=None) -> list:
        if cube:
            if incl_action:
                return [(self.child_after(m, cube=cube), m) for m in self.moves]
            else:
                return [self.child_after(m, cube=cube) for m in self.moves]
        else:
            if self._children is None:
                if incl_action:
                    self._children = [(m, self.child_after(m)) for m in self.moves]
                else:
                    self._children = [self.child_after(m) for m in self.moves]
            return self._children

    def get_moves(self) -> list:
        return self.moves

    def scramble(self, depth: int) -> any:
        return self.cube.scramble(depth)

    def view(self) -> None:
        print(self.cube)

    def evaluate(self, moves) -> bool:
        c = deepcopy(self.cube)
        c.rotate([CubeMove.create(m) for m in moves])
        return c.is_done()

    @abstractmethod
    def solve(self, callback=lambda: 0) -> list[str]:
        pass

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, RubixCube):
            s_p = self.cube.get_all_pieces()
            v_p = __value.cube.get_all_pieces()
            return all(s_p[k].get_piece_colors() == v_p[k].get_piece_colors() for k in s_p.keys())
        return False


class BeginnerCube(RubixCube):
    def solve(self, callback=lambda: 0):
        callback()
        solver = BasicSolver(deepcopy(self.cube))
        actions = solver.solve()
        # only works with 3x3x3 so can hardcode
        m = {
            'R': "3L'",
            "R'": '3L',
            'D': "3U'",
            "D'": '3U',
            "B": "3F'",
            "B'": '3F'
        }
        # print("Solver solved ", self.cube.is_done())
        return [m.get(str(action), str(action)) for action in actions]
