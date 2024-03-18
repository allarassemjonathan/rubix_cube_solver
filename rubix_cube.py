import magiccube as magic
from magiccube.cube_move import CubeMove, CubeMoveType
from magiccube.solver.basic.basic_solver import BasicSolver
from abc import ABC, abstractmethod
from copy import deepcopy
from magiccube.cube import Face, Color

BASIC_MOVES = ['L', 'U', 'F']

# Compute the manhattan distance between two tuples
def ManhattanDistance(t1, t2):
    return abs(t1[0]-t2[0]) + abs(t1[1]-t2[1]) + abs(t1[2]-t2[2])



def distance(coordA, coordB) -> float:
    return sum(abs(x - y) for x, y in zip(coordA, coordB))

# Rank the cube c1
def man_heuristic(c1:magic.Cube, n):
    original_positions = {p.get_piece_colors(True): c for c,p in magic.Cube(n).get_all_pieces().items()}
    return sum(distance(c, original_positions[p.get_piece_colors(True)]) for c, p in c1.get_all_pieces().items())/16


def invertFace(face, rev=True):
    return face[::-1] if rev else face

def cube_str(cube):
    face_order = [Face.D, Face.R, Face.F, Face.L, Face.B, Face.U]
    return "".join(color.name.lower() for face in face_order for color in cube.get_face_flat(face))

# def generate_heuristic():


class RubixCube(ABC):

    def __init__(self, n, cube=None) -> None:
        self.moves = []
        self.N = n
        if cube is None:
            self.cube = magic.Cube(n)
        else:
            self.cube = cube
        self._children = None
        self.original_positions = {p: c for c, p in self.cube.get_all_pieces().items()}
        for i in range(1, n + 1):
            for m in BASIC_MOVES:
                self.moves.append(str(i) + m)
                self.moves.append(str(i) + m + '\'')

    @abstractmethod
    def child_after(self, move, cube=None):
        pass

    def get_cube(self):
        return self.cube

    def get_size(self):
        return self.N

    def cost(self) -> float:
        return sum(distance(c, self.original_positions[p]) for c, p in self.cube.get_all_pieces().items())

    def children(self, incl_action=False, cube=None) -> list:
        if cube:
            if incl_action:
                return [(self.child_after(m, cube=cube), m) for m in self.moves]
            else:
                return [self.child_after(m, cube=cube) for m in self.moves]
        else:
            if self._children is None:
                if incl_action:
                    self._children = [(self.child_after(m), m) for m in self.moves]
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

    def repr(self):
        return self.cube.str()


class BeginnerCube(RubixCube):
    def child_after(self, move):
        pass

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
