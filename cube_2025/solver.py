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

    def __init__(self, cube=None):
        """
        Initialize the solver with a cube
        """
        if cube is None:
            cube = Cube(size=3)
        if not isinstance(cube, Cube):
            raise TypeError("cube must be a Cube")
        self.cube = cube

    def orient_cube(self):
        """
        Orient the cube to a standard position
        """
        move_map ={
            'W': {
                "U": (),
                "L": ({"axis": "z", "clockwise": True},),
                "R": ({"axis": "z", "clockwise": False},),
                "F": ({"axis": "x", "clockwise": True},),
                "B": ({"axis": "x", "clockwise": False},),
                "D": (
                    {"axis": "x", "clockwise": True}, 
                    {"axis": "x", "clockwise": True},
                ),
            },
            'R': {
                "U": (),
                "L": ({"axis": "y", "clockwise": False},),
                "R": ({"axis": "y", "clockwise": True},),
                "F": (),
                "B": ({"axis": "y", "clockwise": True},{"axis": "y", "clockwise": True},),
                "D": (),
            }
        }

        # Find the white center and orient it to the top
        for color in ['W', 'R']:
            center = self.cube.centers(color_filter=[color])[0]
            start_position = center.position
            for move in move_map[color][start_position]:
                self.cube.rotate_cube(**move)
        
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

    def _correct_white_edge_count(self, edges):
        """
        Check if the white edges are in the correct position
        """
        correct = 0
        for edge in edges:
            if edge.position[0] == "U":
                face = edge.position[1]
                if self.cube.get_sticker(face, 1) == self.cube.get_sticker(face, 4):
                    correct += 1
        return correct

    def _align_white_edges(self, edges=None):
        """
        Align the white edges to the top layer
        """
        if edges is None:
            edges = self.cube.edges(color_filter=["W"])
        max_correct = 0
        for _ in range(4):
            correct = self._correct_white_edge_count(edges)
            logging.debug("correct: %d, max_correct: %d", correct, max_correct)
            if correct > max_correct:
                max_correct = correct
            self.cube.rotate_face("U", clockwise=True)
        correct = self._correct_white_edge_count(edges)
        logging.debug("equal? correct: %d, max_correct: %d", correct, max_correct)
        sentinel = 0
        while correct != max_correct:
            sentinel += 1
            if sentinel > 4:
                logging.warning(
                    "Too many iterations, breaking out of the loop at line %d",
                    __import__("inspect").currentframe().f_lineno,
                )
                print_color_cube(self.cube)
                print(self.cube)
                sys.exit(1)
                break
            logging.debug("rotate? correct: %d, max_correct: %d", correct, max_correct)
            self.cube.rotate_face("U", clockwise=True)
            correct = self._correct_white_edge_count(edges)

        logging.debug("edges: %s", edges)

    def _cross_up_clear(self, face):
        """
        check to see if rotating a face will impact a correctly positioned
        white edge
        """
        # get up edge of face
        edge = self.cube.get_cubie(f"U{face}")
        # if edge doesn't have white, we can move it
        if not "W" in edge.color:
            return True
        # if edge is not oriented, we can move it
        if edge.orientation != 0:
            return True
        # if not the correct edge, we can move it
        if self.cube.face_color(face) in edge.color:
            return True
        # lets not move it
        return False

    def cross(self):
        """
        2nd attempt to solve the cross on the first layer
        """
        self.orient_cube()
        white_edges = self.cube.edges(color_filter=["W"])
        self._align_white_edges(white_edges)
        counter = 0
        while not self._check_white_cross():
            counter += 1
            logging.debug("Iteration: %d", counter)
            if counter > 100:
                logging.warning(
                    "Too many iterations, breaking out of the loop at line %d",
                    __import__("inspect").currentframe().f_lineno,
                )
                logging.warning(self.cube)
                break

            for edge in white_edges:
                logging.debug("Considering edge %s", edge)
                # 1: up:
                logging.debug(
                    "edge.position[0] (%s) == 'U', %s",
                    edge.position[0],
                    edge.position[0] == "U",
                )
                if edge.position[0] == "U":
                    logging.debug("Edge %s is in the up layer", edge)
                    # a: white up
                    if edge.orientation == 0:
                        # is it in the right position?
                        # does other color match center?
                        if edge.color[1] == self.cube.get_sticker(edge.position[1], 4):
                            logging.debug("Edge %s is in the right position", edge)
                            # already in the right position
                            continue
                    # b: not white up or not in the right possition, send down
                    logging.debug(
                        "Edge %s is not in the right position, send down", edge
                    )
                    for _ in range(2):
                        self.cube.rotate_face(edge.position[1], clockwise=True)
                logging.debug(
                    "edge.position (%s) != 'U' || 'D', %s",
                    edge.position,
                    "U" not in edge.position and "D" not in edge.position,
                )
                # if 'U' not in edge.position and 'D' not in edge.position:
                #     # 2: middle
                #     logging.debug("Edge %s is in the middle layer", edge)
                #     # is it in the right position?
                #     # does other color match center?
                #     if edge.color[1] == self.cube.get_sticker(edge.position[1], 4):
                #         logging.debug("Edge %s is in the right position", edge)
                #         # already in the right position
                #         continue
                #     else:
                #         logging.debug("Edge %s is not in the right position, send down", edge)
                #         # a: other aligned
                #         if edge.orientation == 0:
                #             for _ in range(2):
                #                 self.cube.rotate_face(edge.position[1], clockwise=True)
                #         # b: not other aligned
                #         else:
                #             for _ in range(2):
                #                 self.cube.rotate_face(edge.position[1], clockwise=False)

                # 2: middle
                if "U" not in edge.position and "D" not in edge.position:
                    logging.debug("Edge %s is on the equator", edge)
                    # a: other aligned
                    logging.debug(
                        "position_index for %d is %d",
                        edge.orientation,
                        (edge.orientation + 1) % 2,
                    )
                    other_color = edge.get_colors(color_filter="W")[0]
                    other_face = edge.position[(edge.orientation + 1) % 2]
                    logging.debug(
                        "%s == %s? %s",
                        edge.get_colors("W"),
                        self.cube.face_color(other_face),
                        edge.get_colors("W") == self.cube.face_color(other_face),
                    )
                    if other_color == self.cube.face_color(other_face):
                        logging.debug("Edge %s is aligned", edge)
                        self.cube.rotate_face(other_face, clockwise=True)
                        if edge.position != f"U{other_face}":
                            # undo
                            self.cube.rotate_face(other_face, clockwise=False)
                            # other direction
                            self.cube.rotate_face(other_face, clockwise=False)
                    # b: not other aligned
                    else:
                        logging.debug("Edge %s is not aligned", edge)
                        other_color = edge.get_colors(color_filter="W")[0]
                        other_face = edge.position[(edge.orientation + 1) % 2]
                        while not self._cross_up_clear(other_face):
                            logging.debug("Clearing face %s", other_face)
                            self.cube.rotate_face("U")
                        self.cube.rotate_face(other_face)
                        if edge.position != f"D{other_face}":
                            # undo
                            self.cube.rotate_face(other_face, clockwise=False)
                            # other direction
                            self.cube.rotate_face(other_face, clockwise=False)
                        # put up layer back
                        self._align_white_edges()

                # 3: down
                if edge.position[0] == "D":
                    logging.debug("Edge %s is in the down layer", edge)
                    # is it in the right position?
                    # does other color match center?
                    while not edge.get_colors(color_filter="W")[
                        0
                    ] == self.cube.face_color(edge.position[1]):
                        logging.debug(
                            "Edge %s, non-white color is %s",
                            edge,
                            edge.get_colors(color_filter="W")[0],
                        )
                        logging.debug(
                            "Edge %s is not in the right position, aligning", edge
                        )
                        self.cube.rotate_face("D", clockwise=True)
                        logging.debug(
                            "Edge %s: %s == %s? %s",
                            edge,
                            edge.get_colors(color_filter="W")[0],
                            self.cube.face_color(edge.position[1]),
                            edge.get_colors(color_filter="W")[0]
                            == self.cube.face_color(edge.position[1]),
                        )
                    # a: white down
                    if edge.orientation == 0:
                        logging.debug("Edge %s white is down, send up", edge)
                        # send up
                        for _ in range(2):
                            self.cube.rotate_face(edge.position[1], clockwise=True)
                    # b: not white down
                    else:
                        other_color = edge.get_colors("W")[0]
                        logging.debug(
                            "Edge %s is not white down, twist and send up", edge
                        )
                        # rotate down counter clockwise
                        logging.debug("rotate down counter clockwise")
                        self.cube.rotate_face("D", clockwise=False)
                        # rotate up clockwise
                        logging.debug("rotate up clockwise")
                        self.cube.rotate_face("U", clockwise=True)
                        # rotate other face counter clockwise
                        logging.debug(
                            "rotate other face %s counter clockwise",
                            self.cube.face_by_color(other_color),
                        )
                        self.cube.rotate_face(
                            "".join(edge.position).replace("D", ""), clockwise=False
                        )
                        # rotate up counter clockwise
                        logging.debug("rotate up counter clockwise")
                        self.cube.rotate_face("U", clockwise=False)
                        # rotate other face clockwise
                        logging.debug("rotate other face %s clockwise", other_color)
                        self.cube.rotate_face(
                            self.cube.face_by_color(other_color), clockwise=True
                        )
        return self._check_white_cross()

    def f2l(self):
        """
        Solve the first two layers
        """
        # Implement the first two layerols solving algorithm here
        white_corners = self.cube.corners(color_filter=["W"])
        target_edges = []
        for edge in self.cube.edges():
            if "W" not in edge.color and "Y" not in edge.color:
                target_edges.append(edge)
        print(f"white_corners: {white_corners}")
        print(f"target_edges: {target_edges}")
        

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
    print("Run test_solver.py to test the solver")
    solver = Solver()
    solver.cube.scramble()
    solver.cross()
    solver.f2l()
    