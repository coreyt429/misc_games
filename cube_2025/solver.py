"""
Module to solve a rubiks cube puzzle
"""
import sys
import json
import logging
from random import choice, randint
from cube import Cube, FACE_COLORS
from visualize import print_color_cube


class Solver:
    """
    Class to solve a rubiks cube puzzle
    """

    def __init__(self, cube):
        """
        Initialize the solver with a cube
        """
        if not isinstance(cube, Cube):
            raise TypeError("cube must be a Cube")
        self.cube = cube

    def orient_cube(self):
        """
        Orient the cube to a standard position
        """
        centers = self.cube.centers()
        # Find the white center and orient it to the top
        for center in centers:
            if "W" in center.color:
                if center.position in ['L']:
                    self.cube.rotate_cube(axis="z", clockwise=True)
                elif center.position in ['R']:
                    self.cube.rotate_cube(axis="z", clockwise=False)
                elif center.position in ['F']:
                    self.cube.rotate_cube(axis="x", clockwise=True)
                elif center.position in ['B']:
                    self.cube.rotate_cube(axis="x", clockwise=False)
                elif center.position in ['D']:
                    self.cube.rotate_cube(axis="y", clockwise=True)
                    self.cube.rotate_cube(axis="y", clockwise=True)
                break
        for center in centers:
            if "R" in center.color:
                if center.position in ['L']:
                    self.cube.rotate_cube(axis="y", clockwise=False)
                elif center.position in ['R']:
                    self.cube.rotate_cube(axis="y", clockwise=True)
                elif center.position in ['B']:
                    self.cube.rotate_cube(axis="y", clockwise=True)
                    self.cube.rotate_cube(axis="y", clockwise=True)
                elif center.position in ['D']:
                    self.cube.rotate_cube(axis="y", clockwise=True)
                    self.cube.rotate_cube(axis="y", clockwise=True)
                break
        
        
    def count_edge_faces(self, edges, color):
        """
        Count the number of edges with a specific color
        """
        counts = {
            "U": 0,
            "D": 0,
            "L": 0,
            "R": 0,
            "F": 0,
            "B": 0,
        }
        for edge in edges:
            counts[edge.position[edge.orientation]] += 1
        return counts

    def _check_white_cross(self):
        """
        Check if the white cross is solved
        """
        white_edges = self.cube.edges(color_filter=["W"])
        self._align_white_edges(white_edges)
        edge_counts = self.count_edge_faces(white_edges, "W")
        if edge_counts["U"] != 4:
            logging.debug("Only %d white edges are in the up layer", edge_counts["U"])
            return False
        for edge in white_edges:
            if edge.orientation != 0:
                logging.debug("Edge %s is not oriented correctly", edge)
                return False
            if edge.color[1] != self.cube.face_color(edge.position[1]):
                logging.debug("Edge %s is not in the correct position", edge)
                return False
        return True

    def _down_edges_up(self, edges):
        """
        Move the edges from the down layer to the top layer
        """
        self._align_white_edges(edges)
        for edge in edges:
            if edge.position[0] != 'D':
                continue
            if edge.orientation == 1:
                continue
            if edge.color[1] != self.cube.face_color(edge.position[1]):
                for _ in range(3):
                    self.cube.rotate_face('D', clockwise=True)
                    if edge.color[1] == self.cube.face_color(edge.position[1]):
                        break
            face = edge.position[1]
            for _ in range(2):
                self.cube.rotate_face(face, clockwise=True)
        self.orient_cube()
    
    def _correct_white_edge_count(self, edges):
        """
        Check if the white edges are in the correct position
        """
        correct = 0
        for edge in edges:
            if edge.position[0] == 'U':
                face = edge.position[1]
                if self.cube.get_sticker(face,1) == self.cube.get_sticker(face,4):
                    correct += 1
        return correct

    def _align_white_edges(self, edges):
        """
        Align the white edges to the top layer
        """
        max_correct = 0
        for _ in range(4):
            correct = self._correct_white_edge_count(edges)
            logging.debug("correct: %d, max_correct: %d", correct, max_correct)
            if correct > max_correct:
                max_correct = correct
            self.cube.rotate_face('U', clockwise=True)
        correct = self._correct_white_edge_count(edges)
        logging.debug("equal? correct: %d, max_correct: %d", correct, max_correct)
        sentinel = 0
        while correct != max_correct:
            sentinel += 1
            if sentinel > 4:
                logging.warning("Too many iterations, breaking out of the loop at line %d", __import__('inspect').currentframe().f_lineno)
                print_color_cube(self.cube)
                print(self.cube)
                sys.exit(1)
                break
            logging.debug("rotate? correct: %d, max_correct: %d", correct, max_correct)
            self.cube.rotate_face('U', clockwise=True)
            correct = self._correct_white_edge_count(edges)

        logging.debug("edges: %s", edges)

    def _wrong_up_edges_down(self, edges):
        """
        Move the edges from the up layer to the down layer
        If they are incorrectly positioned
        """
        self._align_white_edges(edges)
        changed = False
        for edge in edges:
            if edge.position[0] != 'U':
                continue
            if edge.orientation == 1:
                continue
            if edge.color[1] != self.cube.face_color(edge.position[1]):
                face = edge.position[1]
                for _ in range(2):
                    changed = True
                    self.cube.rotate_face(face, clockwise=True)
        self.orient_cube()
        return changed

    def _up_edges_flipped(self, edges):
        """
        Move the edges from the up layer to the down layer
        If they are flipped
        F'UL'U'
        """
        self._align_white_edges(edges)
        changed = False
        for edge in edges:
            if edge.position[0] != 'U':
                continue
            if edge.orientation == 0:
                continue
            counter = 0
            while 'F' not in edge.position:
                counter += 1
                if counter > 10:
                    logging.warning("Too many iterations, breaking out of the loop at line %d", __import__('inspect').currentframe().f_lineno)
                    break
                self.cube.rotate_cube(axis='y', clockwise=True)
            changed = True
            # F'
            self.cube.rotate_face('F', clockwise=False)
            # U
            self.cube.rotate_face('U', clockwise=True)
            # L'
            self.cube.rotate_face('L', clockwise=False)
            # U'
            self.cube.rotate_face('U', clockwise=False)
            self.orient_cube()
            return changed
    
    def _down_edges_flipped(self, edges):
        """
        Move the edges from the down layer to the up layer
        If they are flipped
        F'U'RU
        """
        self._align_white_edges(edges)
        changed = False
        for edge in edges:
            if edge.position[0] != 'D':
                continue
            if edge.orientation == 0:
                continue
            counter = 0
            while self.cube.face_color(edge.position[1]) != edge.color[1]:
                counter += 1
                if counter > 10:
                    logging.warning("Too many iterations, breaking out of the loop at line %d", __import__('inspect').currentframe().f_lineno)
                    break
                self.cube.rotate_face('D', clockwise=True)
            while 'F' not in edge.position:
                counter += 1
                if counter > 10:
                    logging.warning("Too many iterations, breaking out of the loop at line %d", __import__('inspect').currentframe().f_lineno)
                    break
                self.cube.rotate_cube(axis='y', clockwise=True)
            if self._up_empty_face('F'):
                changed = True
                # F'
                self.cube.rotate_face('F', clockwise=False)
                # U'
                self.cube.rotate_face('U', clockwise=False)
                # R
                self.cube.rotate_face('R', clockwise=True)
                # U
                self.cube.rotate_face('U', clockwise=True)
            self.orient_cube()
            return changed
   
                   
    def _white_edges_up(self, edges):
        """
        Move the edges from the white layer to the up layer
        If they are flipped
        """
        self._align_white_edges(edges)
        changed = False
        for edge in edges:
            # skip the edges in the up layer
            if 'U' in edge.position:
                logging.debug("Edge %s is in the up layer", edge)
                continue
            # detect the face that is not the white face
            face = edge.position[1]
            if edge.orientation == 0 and edge.position[0] != 'D':
                face = edge.position[0]
            logging.debug("face: %s, edge: %s", face, edge)
            sentinel = 0
            logging.debug("U%s in %s", face, [other_edge.position for other_edge in edges])
            if self._up_empty_face(face):
                sentinel = 0
                while edge.position != f"U{face}":
                    self.cube.rotate_face(face, clockwise=True)
                    changed = True
                    sentinel += 1
                    logging.debug("%d: edge.position: %s, face: %s", sentinel, edge.position, face)
                    if sentinel > 10:
                        logging.warning("Too many iterations, breaking out of the loop at line %d", __import__('inspect').currentframe().f_lineno)
                        break
        self.orient_cube()
        return changed
    
    def _up_empty_face(self, face):
        """
        Make the up face empty
        """
        sentinel = 0
        while 'W' in self.cube.get_cubie(f"U{face}").color:
            self.cube.rotate_face('U', clockwise=True)
            sentinel += 1
            if sentinel > 4:
                logging.warning("Too many iterations, breaking out of the loop at line %d", __import__('inspect').currentframe().f_lineno)
                return False
        return True

    def cross(self):
        """
        Solve the cross on the first layer
        """
        self.orient_cube()
        counter = 0
        while not self._check_white_cross():
            counter += 1
            logging.debug("Iteration: %d", counter)
            if counter > 100:
                logging.warning("Too many iterations, breaking out of the loop at line %d", __import__('inspect').currentframe().f_lineno)
                self._white_edges_up(self.cube.edges(color_filter=["W"]))
                self._align_white_edges(self.cube.edges(color_filter=["W"]))
                break
            white_edges = self.cube.edges(color_filter=["W"])
            edge_counts = self.count_edge_faces(white_edges, "W")
            logging.debug("Edge counts: %s", edge_counts)
            if self._white_edges_up(self.cube.edges(color_filter=["W"])):
                logging.debug("White edges up")
            if self._wrong_up_edges_down(white_edges):
                logging.debug("Moved wrong up edges down")
            if self._up_edges_flipped(white_edges):
                logging.debug("Flipped up edges")
            if self._down_edges_up(white_edges):
                logging.debug("Moved down edges up")
            if self._down_edges_flipped(white_edges):
                logging.debug("Flipped down edges")
            # self._middle_edges_up(white_edges)
        # FIXME: get load from state working 
        # test with:
        #   GYYWWYRWWBWWOYRGOGROYGGWOGRROORBRBBOBRGBRYWGOBBYGOYWBY
        #   GWGBWBGGRWWBBYGOOYOYOYGGWRBYORBBYYORYYGRRWRROWGWOORBWB
        #   BBGWWYBYWWYOWYGBGOYGOBGRWORGBYBBOBRGWROWROGOYRRRGOWYYR
        # this cube is not finishing the cross
        return self._check_white_cross()
        
            
  


    def f2l(self):
        """
        Solve the first two layers
        """
        # Implement the first two layers solving algorithm here
        pass

    def oll(self):
        """
        Solve the orientation of the last layer
        """
        # Implement the orientation of the last layer solving algorithm here
        pass

    def pll(self):
        """
        Solve the permutation of the last layer
        """
        # Implement the permutation of the last layer solving algorithm here
        pass

    def solve(self):
        """
        Solve the cube
        """
        # Implement the solving algorithm here
        self.cross()
        self.f2l()
        self.oll()
        self.pll()


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    solver = Solver(Cube(size=3))
    stats = {
        "cross": 0,
        "fail": 0
    }
    # `solver.cube.load("GYYWWYRWWBWWOYRGOGROYGGWOGRROORBRBBOBRGBRYWGOBBYGOYWBY")
    # solver.cross()`
    # solver.cube.load("WWRWWWRWGWRBOYRGOGOGGGGYOGBWOYYBRYBOYBRBRORYOBRBGOYWBY")
    # # solver.cube.rotate_face('U', clockwise=False)
    # solver._align_white_edges(solver.cube.edges(color_filter=["W"]))
    # solver.cross()
    # print_color_cube(solver.cube)
    failures = set()
    for idx in range(100000):
        print(f"\rIteration: {idx}: {stats['cross']}/{stats['fail']}", end="", flush=True)
        solver.cube.reset()
        solver.cube.scramble()
        start_state = str(solver.cube)
        if solver.cross():
            stats["cross"] += 1
            # print(f"Cross solved for {start_state}")
        else:
            stats["fail"] += 1
            # print(f"Cross failed for {start_state}")
            failures.add(start_state)
    print(f"{stats['cross']} crosses solved")
    print(f"{stats['fail']} crosses failed")


"""
Notes:
  I think the white cross logic can be a lot simpler, if we focus on one edge at a time
    if up an oriented, but not correctly positioned, move it to the down layer
    if up an oriented incorrectly, rotate other face
    Scenarios:
      1: up:
        a: white up
        b: not white up
      2: middle
        a: other aligned
        b: not other aligned
      3: down
        a: white down
        b: not white down

    if middle:
      rotate other face so that white is down
      rotate down until other color matches center
      rotate other face so that white is up
    if down and white down:
      rotate down until other color matches center
      rotate other face so that white is up
    if down and not white down:
      rotate align to free up side
    
"""