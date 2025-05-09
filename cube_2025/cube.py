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
CORNER_FACE_ORDER = {
    "UFR": ('U', 'F', 'R'),
    "UFL": ('U', 'L', 'F'),
    "UBL": ('U', 'B', 'L'),
    "UBR": ('U', 'R', 'B'),
    "DFR": ('D', 'F', 'R'),
    "DFL": ('D', 'L', 'F'),
    "DBL": ('D', 'B', 'L'),
    "DBR": ('D', 'R', 'B'),
}
FACE_POSITIONS = {
    "U": {
        0: "UBL",
        1: "UB",
        2: "UBR",
        3: "UL",
        4: "U",
        5: "UR",
        6: "UFL",
        7: "UF",
        8: "UFR",
    },
    "D": {
        0: "DFL",
        1: "DF",
        2: "DFR",
        3: "DL",
        4: "D",
        5: "DR",
        6: "DBL",
        7: "DB",
        8: "DBR",
    },
    "L": {
        0: "UBL",
        1: "UL",
        2: "UFL",
        3: "BL",
        4: "L",
        5: "FL",
        6: "DBL",
        7: "DL",
        8: "DFL",
    },
    "R": {
        0: "UFR",
        1: "UR",
        2: "UBR",
        3: "FR",
        4: "R",
        5: "BR",
        6: "DFR",
        7: "DR",
        8: "DBR",
    },
    "F": {
        0: "UFL",
        1: "UF",
        2: "UFR",
        3: "FL",
        4: "F",
        5: "FR",
        6: "DFL",
        7: "DF",
        8: "DFR",
    },
    "B": {
        0: "UBR",
        1: "UB",
        2: "UBL",
        3: "BR",
        4: "B",
        5: "BR",
        6: "DBR",
        7: "DB",
        8: "DBL",
    },
}

FACE_ROTATIONS = {
    # (axis, clockwise)
    'U': ("y", True),
    'D': ("y", False),
    'L': ("x", False),
    'R': ("x", True),
    'F': ("z", True),
    'B': ("z", False)
}

ROTATION_MAP = {
    "x": {
        "UFR": "UBR",
        "UF": "UB",
        "UFL": "UBL",
        "UL": "BL",
        "U": "B",
        "UR": "BR",
        "UBL": "DBL",
        "UB": "DB",
        "UBR": "DBR",
        "DFR": "UFR",
        "DF": "UF",
        "DFL": "UFL",
        "DL": "FL",
        "D": "F",
        "DR": "FR",
        "DBL": "DFL",
        "DB": "DF",
        "DBR": "DFR",
        "FL": "UL",
        "F": "U",
        "FR": "UR",
        "L": "L",
        "R": "R",
        "BL": "DL",
        "B": "D",
        "BR": "DR",
    },
    "y": {
        "UFR": "UFL",
        "UF": "UL",
        "UFL": "UBL",
        "UL": "UB",
        "U": "U",
        "UR": "UF",
        "UBL": "UBR",
        "UB": "UR",
        "UBR": "UFR",
        "DFR": "DFL",
        "DF": "DL",
        "DFL": "DBL",
        "DL": "DB",
        "D": "D",
        "DR": "DF",
        "DBL": "DBR",
        "DB": "DR",
        "DBR": "DFR",
        "FL": "BL",
        "F": "L",
        "FR": "FL",
        "L": "B",
        "R": "F",
        "BL": "BR",
        "B": "R",
        "BR": "FR",
    },
    "z": {
        "UFR": "DFR",
        "UF": "FR",
        "UFL": "UFR",
        "UL": "UR",
        "U": "R",
        "UR": "DR",
        "UBL": "UBR",
        "UB": "BR",
        "UBR": "DBR",
        "DFR": "DFL",
        "DF": "FL",
        "DFL": "UFL",
        "DL": "UL",
        "D": "L",
        "DR": "DL",
        "DBL": "UBL",
        "DB": "BL",
        "DBR": "DBL",
        "FL": "UF",
        "F": "F",
        "FR": "DF",
        "L": "U",
        "R": "D",
        "BL": "UB",
        "B": "B",
        "BR": "DB",
    },
}

ROTATION_MAP_INVERSE = {
    "x": {value:key for key, value in ROTATION_MAP["x"].items()},
    "y": {value:key for key, value in ROTATION_MAP["y"].items()},
    "z": {value:key for key, value in ROTATION_MAP["z"].items()},
}

def get_axis_map(axis, clockwise=True):
    """
    Get the axis map for the cubie.
    The axis can be 'x', 'y', or 'z'.
    """
    if clockwise:
        return ROTATION_MAP[axis]
    else:
        return ROTATION_MAP_INVERSE[axis]

class Cubie:
    """
    Class representing a single cubie in the cube.
    Each cubie has a color and an index.
    """


    def rotate(self, axis, clockwise, axis_map=None):
        """
        Rotate the cubie around a specified face.
        The face can be 'U', 'D', 'L', 'R', 'F', or 'B'.
        face=W specifies whole cube
        """
        if axis_map is None:
            axis_map = get_axis_map(axis, clockwise)
        # rotate the cubie
        new_position = axis_map[self.position]
        self.position = new_position
        # rotate the cubie orientation
        # self.orientation = (self.orientation + 1) % len(self.color)
        

    def __init__(self, position, color, orientation):
        self.position = position
        self.color = color
        self.orientation = orientation

    def __repr__(self):
        return (
            f"Cubie(color={self.color}, "
            + f"position={self.position}, "
            + f"orientation={self.orientation})"
        )

    def __str__(self):
        return f"{self.color} {self.position} {self.orientation}"

    def to_dict(self):
        """
        dict representation of the cubie
        """
        return {
            "position": self.position,
            "color": self.color,
            "orientation": self.orientation,
        }


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
        self.cubies = []
        for corner in CORNERS:
            self.cubies.append(
                Cubie(
                    position=corner,
                    color=tuple(COLORS[FACES.index(face)] for face in CORNER_FACE_ORDER[corner]),
                    orientation=0,
                )
            )
        if self.size == 3:
            for edge in EDGES:
                self.cubies.append(
                    Cubie(
                        position=edge,
                        color=tuple(COLORS[FACES.index(face)] for face in edge),
                        orientation=0,
                    )
                )
            for center in FACES:
                self.cubies.append(
                    Cubie(
                        position=center,
                        color=tuple(COLORS[FACES.index(face)] for face in center),
                        orientation=0,
                    )
                )

    def load(self, state):
        """
        Load a cube state from a string representation.
        The string should be 6 * n^2 characters long,
        representing the colors of the stickers on each face.
        Note, while this will load a debug string or normal string,
        a debug string is preffered for loading.
        # FIXME: rework to use cubies.  need to fully understand cubie orientation for loading
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

    def get_sticker(self, face, index):
        """
        Get the sticker at a specific face and index.
        This is useful for accessing specific stickers on the cube.
        """
        position = FACE_POSITIONS[face][index]
        cubie = self.get_cubie(position)
        if cubie is None:
            raise ValueError(f"Invalid cubie position {position}")
        # print(f"cubie.color: {cubie.color}")
        # print(f"cubie.position: {cubie.position}")
        # print(f"cubie.orientation: {cubie.orientation}")
        # print(f"position.index(face): {position.index(face)}")
        if len(cubie.color) == 3:
            return cubie.color[(CORNER_FACE_ORDER[position].index(face) + cubie.orientation) % len(cubie.color)]
        return cubie.color[(position.index(face) + cubie.orientation) % len(cubie.color)]

    def get_cubie(self, position):
        """
        Get the cubie at a specific position.
        This is useful for accessing specific cubies on the cube.
        """
        for cubie in self.cubies:
            if cubie.position == position:
                return cubie
        return None
    
    def get_cubies(self, face_filter=None, color_filter=None):
        """
        Get a list of cubies that match the specified filters.
        The filters can be face_filter (a list of faces) or color_filter (a list of colors).
        """
        cubies = []
        for cubie in self.cubies:
            if face_filter and not any(face in cubie.position for face in face_filter):
                continue
            if color_filter and not any(color in cubie.color for color in color_filter):
                continue
            cubies.append(cubie)
        return cubies

    def state(self):
        """
        Return a string representation of the cube's current state.
        This is useful for comparing cube states or storing them in sets/dictionaries.
        """
        # FIXME: rework to use cubies.
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
        state_string = ""
        for face in FACES:
            for idx in range(self.size**2):
                state_string += self.get_sticker(face, idx)
        return state_string

    def __repr__(self):
        """
        String representation of the cube.
        """
        debug = self.debug
        self.debug = True
        cube_str = str(self)
        self.debug = debug
        return (
            f"Cube(size={self.size}, state='{cube_str}', "
            f"debug={self.debug} cubies={[repr(cubie) for cubie in self.cubies]})"
        )

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
        """
        self.logger.debug("rotate_face: %s clockwise: %s", face, clockwise)
        (axis, mod_clockwise) = FACE_ROTATIONS[face]
        if not mod_clockwise:
            clockwise = not clockwise
        axis_map = get_axis_map(axis, clockwise)
        
        for cubie in self.get_cubies(face_filter=[face]):
            cubie.rotate(axis, clockwise, axis_map)
        for cubie in self.get_cubies():
            print(cubie)




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("Run test_cube.py to test the Cube class.")
    cube = Cube(size=3, debug=True)
    for curr_cubie in cube.get_cubies(face_filter=["G", 'B']):
        print(curr_cubie)
    print(f"str(cube): {str(cube)}")
    print(f"repr(cube): {repr(cube)}")
    print(f"hash(cube): {hash(cube)}")
    cube.rotate_face("U", clockwise=True)
    for curr_cubie in cube.get_cubies():
        print(curr_cubie)
