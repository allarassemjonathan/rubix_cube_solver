import magiccube as magic
class rubix_cube:
    def __init__(self, n) -> None:
        self.moves = ["B", "B'", "F", "F'", "S", "S'", "F", "F'", "U", "U'", "E", "E'", "D", "D'", "L", "L'", "R", "R'"]
        self.cube = magic.Cube(n)
    
    def children(self):
        return [self.cube.rotate(move) for move in self.moves]
    
    def view(self):
        print(self.cube)

