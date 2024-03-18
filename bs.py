# Jonathan Allarassem 
# Beam Search Implementation
from rubix_cube import RubixCube
import magiccube as magic
from copy import deepcopy
from magiccube.cube_move import CubeMove
import evaluate as e

MAX_DEPTH = 7
# Rank the cube using the Manhattan distance
def heuristic(c1:magic.Cube, n):
    original_positions = {p.get_piece_colors(True): c for c,p in magic.Cube(n).get_all_pieces().items()}
    return sum(distance(c, original_positions[p.get_piece_colors(True)]) for c, p in c1.get_all_pieces().items())/16

# Defining the Manhattan distance
def distance(coordA, coordB):
    return sum(abs(x-y) for x,y in zip(coordA, coordB))

# Comparing two cubes
def Same(s_p:magic.Cube, v_p:magic.Cube) -> bool:
            s_p = s_p.get_all_pieces()
            v_p = v_p.get_all_pieces()
            return all(s_p[k].get_piece_colors() == v_p[k].get_piece_colors() for k in s_p.keys())

class BeamSearch(RubixCube):
    
    def child_after(self, move):
        c = deepcopy(self.cube)
        c.rotate(move)
        return BeamSearch(self.N, c)
        
        # Verbose can be the following:
        # 0. Default value: Does not print anything
        # 1. Print out the actions taken by the Beam Search Algo 
        # And whether it resulted with a success or failure
        # 2. Print out the actions taken by the Beam Search,  
        # The max depth reached and some other parameters
    def solve(self, beta:int, verbose=0, callback=lambda: 0):
        # Get the initial moves
        # No move has been made yet so it is empty
        num = self.N
        cube = self.cube
        openCubes = {'': cube} 
        ClosedCubes = []
        path = []
        MaxDepth = 0
        Neighbors = []
        while len(openCubes)!=0:
            # Remove a cube from the fringe. It does not matter if it is the best
            # since all cubes will be removed at some point
            callback()
            if MaxDepth == 0:
                action, node = list(openCubes.items()).pop()
            

            # Close this cube
            ClosedCubes.append(node)
            if MaxDepth==MAX_DEPTH:
                if verbose>=1:
                    print('failure')
                return path
            
            # If it is the goal, 
            # Return can take advantage of for a max openlist, the number of children is k
            # Thus at depth = 1, we know that one of the children of the current node will 
            # A solution
            if len(Neighbors)>0:
                for neighbor in Neighbors:
                    if neighbor[1].is_done():
                                path.extend(action.split(' '))
                                if verbose>=1:
                                    print('success')
                                print('Answer is', path)
                                return path  
            else:
                 if node.is_done():
                        path.extend(action.split(' '))
                        if verbose>=1:
                            print('success')
                            print('Answer is', path)
                            return path  
                                        
            
            # Generate all the neighbors
            Neighbors = []
            for a in self.get_moves():
                    cube.rotate(a)
                    # add the pair (action, resulting cube)
                    Neighbors.append((a + ' ' + action,deepcopy(cube)))
                    if a[-1]=='\'':
                        # undo the action done earlier
                        cube.rotate(a[-2])
                    else:
                        # undo the action done earlier
                        cube.rotate(a+'\'')


            if verbose>=1:
                for a, _ in Neighbors:
                    print('Actions Leading To Neighbors: ', a, 'on\n', _)

            # For each neighbor
            for NewPath, NewChild in Neighbors:
                IsInOpen = False
                IsInClosed = False

                # check the this neighbor is neither closed nor open
                for p, vertex in openCubes.items():
                    if Same(vertex, NewChild):
                        IsInOpen = True
                        OldNode = vertex
                for element in ClosedCubes:
                    if Same(element, NewChild):
                        IsInClosed = True
                
                # if that is the case add him in the open list
                if not IsInClosed and not IsInOpen:
                    openCubes[NewPath] = NewChild
                    
                # if it is open check if the current path is better
                elif IsInOpen:
                    NewScore = heuristic(NewChild, num)                        
                    OldScore = heuristic(OldNode, num)
                    if NewScore <= OldScore:
                        openCubes[NewPath] = vertex
                        openCubes.pop(p)
                # if it is not closed add him in the opencube
                elif not IsInClosed:
                    openCubes[NewPath] = NewChild

            # Reading the cubes into a dictionary
            rankings = {}
            for key, value in openCubes.items():
                rankings[key] = heuristic(value, num)
            
           
            # Finding the best beta children (beta with least score)
            ListRankings = sorted(rankings.items(), key=lambda item: item[1])[:beta]
            
            
            # Getting the best action/ popping something off the stack
            action,CubeAction = ListRankings[0] 
            if verbose>=1:
                print('Next Immediate Action in Queue: ', action)
            
            # Getting the best incoming cube
            node = openCubes[action]
            ListRankings.remove((action, CubeAction))
            openCubes.pop(action)
            UpdatedCubes = {k[0]:openCubes[k[0]] for k in ListRankings}

            # Passing that value back to the openCube dictionnary
            openCubes.update(UpdatedCubes)
            MaxDepth+=1
            
        
            

# TESTING FOR NODE COUNT FOR 2
for v in range(8):
    print(v, 'result (nc)', e.evaluate_node_count(BeamSearch, 3, depth=v,beta=18, num_trials=15, verbose=0))
    print(v, 'result (sr)', e.evaluate_solve_rate(BeamSearch, 3, depth=v,beta=18, num_trials=15, verbose=0))
