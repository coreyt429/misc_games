"""
Module to simulate a cube puzzle of nxn size.
This module provides a class `Cube` that represents a cube puzzle of size n x n.
It includes methods to rotate the cube, check if it is solved, and print its current state.
The cube is initialized with a solved state, and the user can perform rotations on the cube.
This module only handles cube movements, and does not include any solving algorithms.
"""

import logging
from random import choice
from collections import deque

FACES = ["U", "D", "L", "R", "F", "B"]
COLORS = ["W", "Y", "G", "B", "R", "O"]
FACE_COLORS = dict(zip(FACES, COLORS))
CORNERS = ["UFL", "UFR", "UBR", "UBL", "DFL", "DFR", "DBR", "DBL"]
EDGES = ["UF", "UR", "UB", "UL", "DF", "DR", "DB", "DL", "FL", "FR", "BL", "BR"]

class Cube:
    """
    Class representing a cube puzzle of size n x n.
    The cube is initialized with a solved state, and the user can perform rotations on the cube.
    """

    def __init__(self, **kwargs):
        """
        Initialize the cube with size n x n.
        Parameters:
        - size: The size of the cube (default is 3 for a 3x3 cube).
        - state: A state string representing the cube's current state (optional).
        - debug: A boolean flag to enable debug logging (default is False).
        """
        self.logger = logging.getLogger(__name__)
        self.size = kwargs.get("size", 3)
        if self.size < 2 or self.size > 3:
            raise ValueError(f"Invalid cube size {self.size}: int({self.size})")
        self.debug = kwargs.get("debug", False)
        # init cube in solved state
        self.cube = {}
        self.cubies = []
        if "state" in kwargs:
            self.load(kwargs["state"])
        else:
            self.reset()
        self.solved_state = self._solved_state()

    def reset(self):
        """
        Reset the cube to its solved state.
        This method is useful for resetting the cube after scrambling or solving.
        """
        self.cube = {}
        for face_idx, face in enumerate(FACES):
            self.cube[face] = []
            for idx in range(self.size**2):
                self.cube[face].append({"color": COLORS[face_idx], "index": idx})
        
    def load(self, state):
        """
        Load a cube state from a string representation.
        The string should be 6 * n^2 characters long,
        representing the colors of the stickers on each face.
        Note, while this will load a debug string or normal string,
        a debug string is preffered for loading.
        """
        self.logger.debug("load: %s", state)
        # load non_debug string
        states = [char for char in state if char in COLORS]
        if "0" in state:
            # load debug string
            states = [state[i : i + 2] for i in range(0, len(state), 2)]
        self.size = int((len(states) / 6) ** 0.5)
        if self.size < 2:
            raise ValueError(f"Invalid cube size {self.size}: int({len(states)} / 6)")
        if len(states) != 6 * self.size**2:
            raise ValueError(
                f"Invalid cube state length {len(states)} for size {self.size}"
            )
        self.cube = {}
        for face in FACES:
            self.cube[face] = []
            for idx in range(self.size**2):
                square = states.pop(0)
                color = square[0]
                square_idx = idx
                if len(square) > 1:
                    square_idx = int(square[1:])
                self.cube[face].append({"color": color, "index": square_idx})
        
        return self.cube

    def _solved_state(self):
        """
        Calculate the solved state of the cube.
        The solved state is a hash of the cube's current state.
        """
        solve_state = ""
        for color in COLORS:
            for idx in range(self.size**2):
                solve_state += color + str(idx)
        return hash(solve_state)

    def scramble(self, moves=20):
        """
        Scramble the cube by performing a series of random rotations.
        The number of moves can be specified (default is 20).
        """
        for _ in range(moves):
            face = choice(FACES)
            self.rotate_face(face, clockwise=choice([True, False]))

    def is_solved(self):
        """
        Check if the cube is in the solved state.
        The cube is considered solved if all stickers on each face are the same color.
        """
        self.logger.debug("is_solved: %s == %s", self.solved_state, hash(self))
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

    def __hash__(self):
        """
        Return a hash of the cube's current state.
        This is useful for comparing cube states or storing them in sets/dictionaries.
        """
        debug = self.debug
        self.debug = True
        cube_str = str(self)
        self.debug = debug
        return hash(str(cube_str))

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

    def __repr__(self):
        """
        String representation of the cube.
        """
        debug = self.debug
        self.debug = True
        cube_str = str(self)
        self.debug = debug
        return f"Cube(size={self.size}, state='{cube_str}', debug={self.debug})"

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
            "y": {
                # 0, 1, 2 for index 0, size 3
                "F": [i + (size * index) for i in range(size)],
                "L": [i + (size * index) for i in range(size)],
                "B": [i + (size * index) for i in range(size)],
                "R": [i + (size * index) for i in range(size)],
            },
            "z": {
                # 6, 7, 8 for index 0, size 3
                "U": [i + ((size**2 - (index * size)) - size) for i in range(size)],
                # 0, 3, 6 for index 0, size 3
                "R": [i * size + index for i in range(size)],
                # 0, 1, 2 for index 0, size 3
                "D": [i + (size * index) for i in range(size)],
                # 6, 3, 0 for index 0, size 3
                "L": list(reversed([i * size + index for i in range(size)])),
            },
            "x": {
                # 6, 3, 0 for index 0, size 3,
                "U": list(reversed([i * size + index for i in range(size)])),
                # 2, 5, 8 for index 0, size 3
                "B": [i * size + (size - 1 - index) for i in range(size)],
                # 6, 3, 0 for index 0, size 3,
                "D": list(reversed([i * size + index for i in range(size)])),
                # 6, 3, 0 for index 0, size 3,
                "F": list(reversed([i * size + index for i in range(size)])),
            },
        }
        faces = face_map[axis]
        row = deque()
        for face, squares in faces.items():
            for idx in squares:
                row.append(self.cube[face][idx])
        scalar = 1 if clockwise else -1
        # the last index we will reference from the opposite side
        if index == size - 1:
            scalar = -scalar
        # x axis moves seem reversed, so let's reverse the scalar
        if axis == "x":
            scalar = -scalar
        row.rotate(scalar * size)
        for face, squares in faces.items():
            for idx in squares:
                self.cube[face][idx] = row.popleft()
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
            "U": ("y", 0),
            "D": ("y", self.size - 1),
            "L": ("x", 0),
            "R": ("x", self.size - 1),
            "F": ("z", 0),
            "B": ("z", self.size - 1),
        }
        self._rotate_slice(*slices[face], clockwise)


if __name__ == "__main__":
    print("Run test_cube.py to test the Cube class.")
    import json
    cube = Cube(size=3, debug=True)
    for cubie in cube.cubies:
        print(cubie)
