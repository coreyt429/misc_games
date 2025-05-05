"""
Module to simulate a cube puzzle of nxn size.
This module provides a class `Cube` that represents a cube puzzle of size n x n.
It includes methods to rotate the cube, check if it is solved, and print its current state.
The cube is initialized with a solved state, and the user can perform rotations on the cube.
This module only handles cube movements, and does not include any solving algorithms.
"""

import logging

FACES = ["U", "D", "L", "R", "F", "B"]
COLORS = ["W", "Y", "G", "B", "R", "O"]


class Cube:
    """
    Class representing a cube puzzle of size n x n.
    The cube is initialized with a solved state, and the user can perform rotations on the cube.
    """

    def __init__(self, **kwargs):
        """
        Initialize the cube with size n x n.
        """
        self.logger = logging.getLogger(__name__)
        self.size = kwargs.get("size", 3)
        self.moves = kwargs.get("moves", 0)
        self.history = kwargs.get("history", [])
        self.debug = kwargs.get("debug", False)
        if "cube" in kwargs:
            self.cube = kwargs["cube"]
        else:
            self.cube = {}
            for face_idx, face in enumerate(FACES):
                self.cube[face] = []
                for idx in range(self.size**2):
                    self.cube[face].append({"color": COLORS[face_idx], "index": idx})
        self.solved_state = self.state()

    def is_solved(self):
        """
        Check if the cube is in the solved state.
        The cube is considered solved if all stickers on each face are the same color.
        """

        return self.solved_state == hash(self)

    def state(self):
        """
        Return a string representation of the cube's current state.
        This is useful for comparing cube states or storing them in sets/dictionaries.
        """
        return "".join(
            [
                "".join([sticker["color"] for sticker in self.cube[face]])
                for face in FACES
            ]
        )

    def __str__(self):
        """
        Return a string representation of the cube for printing.
        """
        if self.debug:
            return "".join(
                [
                    "".join(
                        [
                            sticker["color"] + str(sticker["index"])
                            for sticker in self.cube[face]
                        ]
                    )
                    for face in FACES
                ]
            )
        return "".join(
            [
                "".join([sticker["color"] for sticker in self.cube[face]])
                for face in FACES
            ]
        )

    def _rotate_face(self, face, clockwise=True):
        """
        Rotate a face of the cube clockwise or counterclockwise.
        The face is represented by its index in the FACES list.
        """
        self.logger.debug("_rotate_face: %s clockwise: %s", face, clockwise)
        self.logger.debug("_rotate_face: %s", self.cube[face])
        size = self.size
        grid = [self.cube[face][i * size : (i + 1) * size] for i in range(size)]
        if clockwise:
            rotated = [list(row) for row in zip(*grid[::-1])]
        else:
            rotated = [list(row) for row in zip(*grid)][::-1]
        self.cube[face] = [sticker for row in rotated for sticker in row]
        self.logger.debug("_rotate_face: %s", self.cube[face])

    def rotate_cube(self, clockwise=True, axis="Y"):
        """
        Rotate the cube around a specified axis.
        The axis can be 'X', 'Y', or 'Z'.
        """
        axis = axis.lower()
        if not clockwise:
            axis = (axis + "'").replace("''", "'")

        movements = {
            "y": (
                ("R", "F"),
                ("F", "L"),
                ("L", "B"),
                ("B", "R"),
                ("U", True),
                ("D", False),
            ),
            "y'": (
                ("R", "B"),
                ("B", "L"),
                ("L", "F"),
                ("F", "R"),
                ("U", False),
                ("D", True),
            ),
            "x'": (
                ("U", "F"),
                ("F", "D"),
                ("D", "B"),
                ("B", "U"),
                ("L", True),
                ("R", False),
            ),
            "x": (
                ("U", "B"),
                ("B", "D"),
                ("D", "F"),
                ("F", "U"),
                ("L", False),
                ("R", True),
            ),
            "z'": (
                ("U", "L"),
                ("L", "D"),
                ("D", "R"),
                ("R", "U"),
                ("F", True),
                ("B", False),
            ),
            "z": (
                ("U", "R"),
                ("R", "D"),
                ("D", "L"),
                ("L", "U"),
                ("F", False),
                ("B", True),
            ),
        }
        new_cube = {}
        for source, destination in movements[axis]:
            self.logger.debug("rotate_cube: %s -> %s", source, destination)
            if isinstance(destination, bool):
                self._rotate_face(source, destination)
                continue
            new_cube[destination] = self.cube[source]
        self.logger.debug("new_cube: %s", new_cube)
        for face, squares in new_cube.items():
            self.logger.debug("rotate_cube: %s -> %s", face, squares)
            self.cube[face] = squares
            self.logger.debug("rotate_cube: %s -> %s", face, self.cube[face])
        self.logger.debug("self.cube: %s", self.cube)

    def _rotate_slice(self, axis, index, clockwise=True):
        """
        Rotate a slice of the cube along a specified axis and index.
        """
        self.logger.debug("_rotate_slice: %s %s %s", axis, index, clockwise)
        size = self.size
        face_map = {
            "x": {
                "U": [i * size + index for i in range(size)],
                "B": [i * size + (size - 1 - index) for i in range(size)],
                "D": [i * size + index for i in range(size)],
                "F": [i * size + index for i in range(size)],
            },
            "y": {
                "L": [index * size + i for i in range(size)],
                "B": [index * size + i for i in range(size)],
                "R": [index * size + i for i in range(size)],
                "F": [index * size + i for i in range(size)],
            },
            "z": {
                "U": [i * size + index for i in range(size)],
                "R": [index * size + i for i in range(size)],
                "D": [i * size + index for i in range(size)],
                "L": [index * size + i for i in range(size)],
            },
        }
        self.logger.debug("_rotate_slice face_map: %s", face_map)

    def rotate_face(self, face, clockwise=True):
        """
        Rotate a face of the cube.
        This method is not implemented yet.
        """
        self.logger.debug("rotate_face: %s clockwise: %s", face, clockwise)
        # rotate the stickers on the face itself
        self._rotate_face(face, clockwise)
        # rotate the stickers on the adjacent faces
        slices = {
            "U": ("z", 0),
            "D": ("z", self.size - 1),
            "L": ("y", 0),
            "R": ("y", self.size - 1),
            "F": ("x", 0),
            "B": ("x", self.size - 1),
        }
        self._rotate_slice(*slices[face], clockwise)
        self.moves += 1
        # FIXME: decision point, should history store moves, or state?
        # if moves, then we likely need to add cube rotations as well
        # maybe the same if state.
        self.history.append((face, clockwise))


if __name__ == "__main__":
    print("Run test.py to test the Cube class.")
