"""
cube.py
A class representing a Rubik's Cube with various functionalities.
It includes methods for initializing, printing, rotating, scrambling,
solving, and saving/loading the cube state.
"""

import json
import logging
import random
import time


EDGE_PAIRS = [
    (("U", (0, 1)), ("B", (0, 1))),
    (("U", (2, 1)), ("F", (0, 1))),
    (("U", (1, 0)), ("L", (0, 1))),
    (("U", (1, 2)), ("R", (0, 1))),
    (("D", (0, 1)), ("F", (2, 1))),
    (("D", (2, 1)), ("B", (2, 1))),
    (("D", (1, 0)), ("L", (2, 1))),
    (("D", (1, 2)), ("R", (2, 1))),
    (("F", (0, 1)), ("U", (2, 1))),
    (("F", (2, 1)), ("D", (0, 1))),
    (("F", (1, 0)), ("L", (1, 2))),
    (("F", (1, 2)), ("R", (1, 0))),
    (("B", (0, 1)), ("U", (0, 1))),
    (("B", (2, 1)), ("D", (2, 1))),
    (("B", (1, 0)), ("R", (1, 2))),
    (("B", (1, 2)), ("L", (1, 0))),
    (("L", (0, 1)), ("U", (1, 0))),
    (("L", (2, 1)), ("D", (1, 0))),
    (("L", (1, 0)), ("B", (1, 2))),
    (("L", (1, 2)), ("F", (1, 0))),
    (("R", (0, 1)), ("U", (1, 2))),
    (("R", (2, 1)), ("D", (1, 2))),
    (("R", (1, 0)), ("F", (1, 2))),
    (("R", (1, 2)), ("B", (1, 0))),
]

OPPOSITE_EDGES = dict(EDGE_PAIRS)
OPPOSITE_EDGES.update({v: k for k, v in EDGE_PAIRS})


class Cube:
    """
    A class representing a Rubik's Cube.
    """

    COLORS = {
        "K": "\033[0;30;40m",  # Black text on Black background (reset)
        "R": "\033[30;41m",  # Black text on Red background
        "Y": "\033[30;43m",  # Black text on Yellow background
        "G": "\033[30;42m",  # Black text on Green background
        "B": "\033[30;44m",  # Black text on Blue background
        "O": "\033[30;48;5;208m",  # Black text on Orange background
        "W": "\033[30;47m",  # Black text on White background
    }
    RESET = "\033[0m"
    BLOCK = "  "

    def __init__(self, filename=None):
        self.faces = "FRBLUD"
        self.colors = "RGOBYW"
        self.sides = "FRBL"
        self.order = "DFRBLU"
        self.cfg = {
            "debug": False,
            "scramble": 40,
            "type": 1,
            "original_logging_level": logging.getLogger().getEffectiveLevel(),
        }
        self.new_cube()  # initialize cube even if we are loading a file
        if filename is not None:
            self.load(filename)

    def print(self):
        """
        Prints the cube in a formatted manner with colors.
        """
        blank = [["K0" for _ in range(3)] for _ in range(3)]
        print()
        rows = [
            blank[0] + self.cube["U"][0] + blank[0] + blank[0],
            blank[1] + self.cube["U"][1] + blank[1] + blank[1],
            blank[2] + self.cube["U"][2] + blank[2] + blank[2],
            self.cube["L"][0]
            + self.cube["F"][0]
            + self.cube["R"][0]
            + self.cube["B"][0],
            self.cube["L"][1]
            + self.cube["F"][1]
            + self.cube["R"][1]
            + self.cube["B"][1],
            self.cube["L"][2]
            + self.cube["F"][2]
            + self.cube["R"][2]
            + self.cube["B"][2],
            blank[0] + self.cube["D"][0] + blank[0] + blank[0],
            blank[1] + self.cube["D"][1] + blank[1] + blank[1],
            blank[2] + self.cube["D"][2] + blank[2] + blank[2],
        ]
        for row in rows:
            row_string = ""
            count = 0
            for square in row:
                count += 1
                color = self.COLORS[square[0]]
                if self.cfg["debug"]:
                    row_string += f"{color}{square}{self.RESET} "
                else:
                    row_string += f"{color}{self.BLOCK}{self.RESET} "
                if count > 2:
                    row_string += " "
                    count = 0
            print(row_string)
            print()

    def new_cube(self):
        """
        Initializes a new cube with default colors and numbers.
        """
        self.cube = {
            face: [
                [
                    self.colors[self.faces.find(face)] + str(i + 1 + 3 * j)
                    for i in range(3)
                ]
                for j in range(3)
            ]
            for face in self.faces
        }

    def set_debug(self, debug):
        """
        Sets the debug mode.
        """
        self.cfg["debug"] = debug
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(self.cfg["original_logging_level"])

    def save(self, filename):
        """
        Save the cube representation to a JSON file.

        Parameters:
        filename (str): The name of the file to save the JSON data.
        """
        try:
            save_data = {}
            for face in self.faces:
                for position in range(1, 10):
                    save_data[f"{face}{position}"] = self._get_square_label(
                        face, position
                    )

            # Convert the cube to a JSON string
            save_json = json.dumps(save_data, indent=4)

            # Write the JSON string to a file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(save_json)

            logging.info("Cube successfully saved to %s", filename)
        except (IOError, json.JSONDecodeError) as e:
            logging.warning("An error occurred while saving/loading the cube: %s", e)

    def load(self, filename):
        """
        Load the cube representation from a JSON file.

        Parameters:
        filename (str): The name of the file to load the JSON data.
        """
        try:
            positions = {
                1: (0, 0),  # 1
                2: (0, 1),  # 2
                3: (0, 2),  # 3
                4: (1, 0),  # 4
                5: (1, 1),  # 5
                6: (1, 2),  # 6
                7: (2, 0),  # 7
                8: (2, 1),  # 8
                9: (2, 2),  # 9
            }
            # Read the JSON string from a file
            with open(filename, "r", encoding="utf-8") as file:
                data_json = file.read()
            data = json.loads(data_json)
            for position, value in data.items():
                row, col = positions[int(position[1])]
                self.cube[position[0]][row][col] = value
            logging.info("Cube successfully loaded from %s", filename)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning("An error occurred while loading the cube: %s", e)

    def scramble(self, moves=40):
        """
        Scramble the cube by performing a series of random rotations.
        Parameters:
          moves (int): The number of random moves to perform.
        """
        logging.debug("cube.scramble(%d)", moves)
        for _ in range(moves):
            face = random.choice(self.faces + "CM")
            clockwise = random.choice([True, False])
            self.rotate(face, clockwise)

    def _orient_cube(self):
        """
        Orient the cube so that the white face is on top and the red face is in front.
        """
        logging.debug("cube._orient_cube()")
        self._orient_face("W", "D")
        while self.cube["F"][1][1][0] != "R":
            self.rotate_cube()

    def _orient_face(self, color, face):
        """
        Orient the cube so that the specified color is on the specified face.
        Parameters:
          color (str): The color to orient.
          face (str): The face to orient the color on.
        """
        logging.debug("cube._orient_face(%s, %s)", color, face)
        if face in "UDFB":
            while self._find_center(color) not in "UDFB":
                logging.debug("Rotating from %s", self._find_center(color))
                self.rotate_cube()
            while self._find_center(color) not in face:
                logging.debug("Tilting from %s", self._find_center(color))
                self.tilt_cube()
        else:
            logging.debug("Face %s is either L OR R", face)
            while self._find_center(color) not in "LRFB":
                logging.debug("Tilting from %s", self._find_center(color))
                self.tilt_cube()
            while self._find_center(color) not in face:
                logging.debug("Rotating from %s", self._find_center(color))
                self.rotate_cube()

    def _find_center(self, color):
        """
        Find the center piece of the specified color.
        """
        logging.debug("cube._find_center(%s)", color)
        for face in self.faces:
            logging.debug("_find_center(%s) %s %s", color, face, self.cube[face][1][1])
            if self.cube[face][1][1][0] == color:
                return face
        return None

    def rotate_cube(self, clockwise=True):
        """
        Rotate the cube around the vertical axis (U and D faces).
        Parameters:
          clockwise (bool): Whether to rotate clockwise or counter-clockwise.
        """
        logging.debug("cube.rotate_cube(%s)", clockwise)
        self.rotate("U", not clockwise)
        # decision point, should middle rotate like up or down?
        self.rotate("M", not clockwise)
        self.rotate("D", clockwise)

    def tilt_cube(self, clockwise=True):
        """
        Tilt the cube around the horizontal axis (F and B faces).
        Parameters:
          clockwise (bool): Whether to tilt clockwise or counter-clockwise.
        """
        logging.debug("cube.tilt_cube(%s)", clockwise)
        self.rotate("L", not clockwise)
        self.rotate("C", clockwise)
        self.rotate("R", clockwise)

    def _make_move(self, move):
        """
        Perform a move on the cube.
        Parameters:
          move (str): The move to perform.
        """
        logging.debug("_make_move(%s)", move)
        if move in "U'F'D'L'R'B'C'M'":
            if move[-1] == "'":
                self.rotate(move[0], clockwise=False)
            else:
                self.rotate(move[0], clockwise=True)
        elif move.upper() in "T'":
            if move[-1] == "'":
                self.tilt_cube(clockwise=False)
            else:
                self.tilt_cube(clockwise=True)
        elif move.upper() in "X'":
            if move[-1] == "'":
                self.rotate_cube(clockwise=False)
            else:
                self.rotate_cube(clockwise=True)

    def _rotate_face_squares(self, face, clockwise=True):
        """
        Rotate the specified face of the cube.
        Parameters:
          face (str): The face to rotate.
        """
        if face not in "CM":
            if clockwise:
                self.cube[face] = [list(row) for row in zip(*self.cube[face][::-1])]
            else:
                self.cube[face] = [list(row) for row in zip(*self.cube[face])][::-1]

    def _rotate_face_front(self, clockwise=True):
        """
        Rotate the front face of the cube.
        """
        rows_cols = []
        rows_cols.extend(self.cube["U"][2])
        rows_cols.append(self.cube["R"][2][0])
        rows_cols.append(self.cube["R"][1][0])
        rows_cols.append(self.cube["R"][0][0])
        rows_cols.extend(reversed(self.cube["D"][0]))
        rows_cols.append(self.cube["L"][2][2])
        rows_cols.append(self.cube["L"][1][2])
        rows_cols.append(self.cube["L"][0][2])
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            # reverse right and left
            rows_cols[3:6] = reversed(rows_cols[3:6])
            rows_cols[9:12] = reversed(rows_cols[9:12])
            rows_cols = rows_cols[3:] + rows_cols[:3]
        self.cube["U"][2] = rows_cols[0:3]
        self.cube["R"][0][0] = rows_cols[3]
        self.cube["R"][1][0] = rows_cols[4]
        self.cube["R"][2][0] = rows_cols[5]
        self.cube["D"][0] = rows_cols[6:9]
        self.cube["L"][2][2] = rows_cols[9]
        self.cube["L"][1][2] = rows_cols[10]
        self.cube["L"][0][2] = rows_cols[11]

    def _rotate_face_back(self, clockwise=True):
        """
        Rotate the back face of the cube.
        """
        rows_cols = []
        if clockwise:
            rows_cols.extend(reversed(self.cube["U"][0]))
            rows_cols.append(self.cube["L"][0][0])
            rows_cols.append(self.cube["L"][1][0])
            rows_cols.append(self.cube["L"][2][0])
            rows_cols.extend(self.cube["D"][2])
            rows_cols.append(self.cube["R"][0][2])
            rows_cols.append(self.cube["R"][1][2])
            rows_cols.append(self.cube["R"][2][2])
        else:
            rows_cols.extend(reversed(self.cube["U"][0]))
            rows_cols.append(self.cube["L"][2][0])
            rows_cols.append(self.cube["L"][1][0])
            rows_cols.append(self.cube["L"][0][0])
            rows_cols.extend(self.cube["D"][2])
            rows_cols.append(self.cube["R"][2][2])
            rows_cols.append(self.cube["R"][1][2])
            rows_cols.append(self.cube["R"][0][2])
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        self.cube["U"][0] = rows_cols[0:3]
        self.cube["L"][0][0] = rows_cols[3]
        self.cube["L"][1][0] = rows_cols[4]
        self.cube["L"][2][0] = rows_cols[5]
        self.cube["D"][2] = rows_cols[6:9]
        self.cube["R"][2][2] = rows_cols[9]
        self.cube["R"][1][2] = rows_cols[10]
        self.cube["R"][0][2] = rows_cols[11]

    def _rotate_face_up(self, clockwise=True):
        """
        Rotate the up face of the cube.
        """
        rows_cols = []
        rows_cols.extend(self.cube["B"][0])
        rows_cols.extend(self.cube["R"][0])
        rows_cols.extend(self.cube["F"][0])
        rows_cols.extend(self.cube["L"][0])
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        self.cube["B"][0] = rows_cols[0:3]
        self.cube["R"][0] = rows_cols[3:6]
        self.cube["F"][0] = rows_cols[6:9]
        self.cube["L"][0] = rows_cols[9:12]

    def _rotate_face_down(self, clockwise=True):
        """
        Rotate the down face of the cube.
        """
        rows_cols = []
        rows_cols.extend(self.cube["F"][2])
        rows_cols.extend(self.cube["R"][2])
        rows_cols.extend(self.cube["B"][2])
        rows_cols.extend(self.cube["L"][2])
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        self.cube["F"][2] = rows_cols[0:3]
        self.cube["R"][2] = rows_cols[3:6]
        self.cube["B"][2] = rows_cols[6:9]
        self.cube["L"][2] = rows_cols[9:12]

    def _rotate_face_left(self, clockwise=True):
        """
        Rotate the left face of the cube.
        """
        rows_cols = []
        # UFDB
        for neighbor in "UFD":
            rows_cols.append(self.cube[neighbor][0][0])
            rows_cols.append(self.cube[neighbor][1][0])
            rows_cols.append(self.cube[neighbor][2][0])
        rows_cols.append(self.cube["B"][2][2])
        rows_cols.append(self.cube["B"][1][2])
        rows_cols.append(self.cube["B"][0][2])
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        # UFDB
        self.cube["U"][0][0] = rows_cols[0]
        self.cube["U"][1][0] = rows_cols[1]
        self.cube["U"][2][0] = rows_cols[2]
        self.cube["F"][0][0] = rows_cols[3]
        self.cube["F"][1][0] = rows_cols[4]
        self.cube["F"][2][0] = rows_cols[5]
        self.cube["D"][0][0] = rows_cols[6]
        self.cube["D"][1][0] = rows_cols[7]
        self.cube["D"][2][0] = rows_cols[8]
        self.cube["B"][2][2] = rows_cols[9]
        self.cube["B"][1][2] = rows_cols[10]
        self.cube["B"][0][2] = rows_cols[11]

    def _rotate_face_right(self, clockwise=True):
        """
        Rotate the right face of the cube.
        """
        rows_cols = []
        if clockwise:
            # UBDF
            for neighbor in "UBDF":
                # print(neighbor,cube[neighbor])
                if neighbor == "B":
                    rows_cols.append(self.cube[neighbor][2][0])
                    rows_cols.append(self.cube[neighbor][1][0])
                    rows_cols.append(self.cube[neighbor][0][0])
                elif neighbor in "U":
                    rows_cols.append(self.cube[neighbor][0][2])
                    rows_cols.append(self.cube[neighbor][1][2])
                    rows_cols.append(self.cube[neighbor][2][2])
                else:
                    rows_cols.append(self.cube[neighbor][2][2])
                    rows_cols.append(self.cube[neighbor][1][2])
                    rows_cols.append(self.cube[neighbor][0][2])
                # print(rows_cols)
        else:
            for neighbor in "UBDF":
                # print(neighbor,cube[neighbor])
                if neighbor in "B":
                    rows_cols.append(self.cube[neighbor][0][0])
                    rows_cols.append(self.cube[neighbor][1][0])
                    rows_cols.append(self.cube[neighbor][2][0])
                elif neighbor in "DF":
                    rows_cols.append(self.cube[neighbor][0][2])
                    rows_cols.append(self.cube[neighbor][1][2])
                    rows_cols.append(self.cube[neighbor][2][2])
                else:
                    rows_cols.append(self.cube[neighbor][2][2])
                    rows_cols.append(self.cube[neighbor][1][2])
                    rows_cols.append(self.cube[neighbor][0][2])
                # print(rows_cols)
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        # UBDF
        self.cube["U"][2][2] = rows_cols[0]
        self.cube["U"][1][2] = rows_cols[1]
        self.cube["U"][0][2] = rows_cols[2]
        self.cube["B"][2][0] = rows_cols[3]
        self.cube["B"][1][0] = rows_cols[4]
        self.cube["B"][0][0] = rows_cols[5]
        self.cube["D"][0][2] = rows_cols[6]
        self.cube["D"][1][2] = rows_cols[7]
        self.cube["D"][2][2] = rows_cols[8]
        self.cube["F"][2][2] = rows_cols[9]
        self.cube["F"][1][2] = rows_cols[10]
        self.cube["F"][0][2] = rows_cols[11]

    def _rotate_face_center(self, clockwise=True):
        """
        Rotate the center face of the cube.
        """
        rows_cols = []
        rows_cols.append(self.cube["B"][0][1])
        rows_cols.append(self.cube["B"][1][1])
        rows_cols.append(self.cube["B"][2][1])
        for neighbor in "DFU":
            rows_cols.append(self.cube[neighbor][2][1])
            rows_cols.append(self.cube[neighbor][1][1])
            rows_cols.append(self.cube[neighbor][0][1])
        for neighbor in "UBDF":
            # print(neighbor,cube[neighbor])
            if neighbor in "B":
                rows_cols.append(self.cube[neighbor][0][0])
                rows_cols.append(self.cube[neighbor][1][0])
                rows_cols.append(self.cube[neighbor][2][0])
            elif neighbor in "DF":
                rows_cols.append(self.cube[neighbor][0][2])
                rows_cols.append(self.cube[neighbor][1][2])
                rows_cols.append(self.cube[neighbor][2][2])
            else:
                rows_cols.append(self.cube[neighbor][2][2])
                rows_cols.append(self.cube[neighbor][1][2])
                rows_cols.append(self.cube[neighbor][0][2])
            # print(rows_cols)
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        # UFDB
        self.cube["U"][0][1] = rows_cols[11]
        self.cube["U"][1][1] = rows_cols[10]
        self.cube["U"][2][1] = rows_cols[9]
        self.cube["F"][0][1] = rows_cols[8]
        self.cube["F"][1][1] = rows_cols[7]
        self.cube["F"][2][1] = rows_cols[6]
        self.cube["D"][0][1] = rows_cols[5]
        self.cube["D"][1][1] = rows_cols[4]
        self.cube["D"][2][1] = rows_cols[3]
        self.cube["B"][2][1] = rows_cols[2]
        self.cube["B"][1][1] = rows_cols[1]
        self.cube["B"][0][1] = rows_cols[0]

    def _rotate_face_middle(self, clockwise=True):
        """
        Rotate the middle face of the cube.
        """
        rows_cols = []
        # for neighbor in 'LFRB':
        # shift self.sides by one side
        for neighbor in self.sides[1:] + self.sides[:1]:
            rows_cols.extend(self.cube[neighbor][1])

        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        self.cube["L"][1] = rows_cols[0:3]
        self.cube["F"][1] = rows_cols[3:6]
        self.cube["R"][1] = rows_cols[6:9]
        self.cube["B"][1] = rows_cols[9:12]

    def rotate(self, face, clockwise=True):
        """
        Rotate the specified face of the cube.
        Parameters:
          face (str): The face to rotate.
          clockwise (bool): Whether to rotate clockwise or counter-clockwise.
        """
        logging.debug("cube.rotate(%s, %s)", face, clockwise)
        # Rotate the face itself
        self._rotate_face_squares(face, clockwise)

        face_rotate_funcs = {
            "F": self._rotate_face_front,
            "B": self._rotate_face_back,
            "U": self._rotate_face_up,
            "D": self._rotate_face_down,
            "L": self._rotate_face_left,
            "R": self._rotate_face_right,
            "C": self._rotate_face_center,
            "M": self._rotate_face_middle,
        }
        face_rotate_funcs[face](clockwise)

    ##########################
    # Command String functions
    ##########################

    def _transpose_command(self, command_string, target, source="F"):
        """
        Method to transpose a command string based on the target and source faces.
        """
        logging.debug(
            'cube._transpose_command("%s", %s, %s)', command_string, target, source
        )
        new_command = ""
        if target in self.sides:
            offset = self.sides.find(target) - self.sides.find(source)
            codex = self.sides[offset:] + self.sides[:offset]
            logging.debug("offset: %s", offset)
            for char in command_string:
                if char in self.sides:
                    idx = self.sides.find(char)
                    new_command += codex[idx]
                else:
                    new_command += char
        else:
            new_command = "X,X'"
        logging.debug("cube._transpose_command returning %s", new_command)
        return new_command

    def run_command_string(self, command):
        """
        Run a command string on the cube.
        """
        logging.debug("cube.run_command_string(cube, %s)", command)
        for move in command.rstrip(",").lstrip(",").split(","):
            self._make_move(move)

    def superflip(self):
        """
        Run superflip algorithm
        """
        self.run_command_string(
            "R,L,U,U,F,U',D,F,F,R,R,B,B,L,U,U,F',B',U,R,R,D,F,F,U,R,R,U"
        )

    ###############################
    # Search and Identify functions
    ###############################

    def _find_edge_pieces(self, colors):
        """
        Find edge pieces of the specified colors.
        """
        logging.debug("_find_edge_pieces(%s)", colors)
        edge_pieces = set()
        for face in self.faces:
            logging.debug("%s,%s", face, self.cube[face])
            for row, col in [(0, 1), (1, 0), (1, 2), (2, 1)]:
                logging.debug("row: %s, col: %s", row, col)
                if self.cube[face][row][col][0] in colors:
                    edge_pieces.add((face, (row, col)))
        return edge_pieces

    def _id_position(self, face, position):
        """
        Identify the type of position on the cube (center, edge, corner).
        """
        logging.debug("_id_position(cube,%s,%s)", face, position)
        retval = {
            "face": face,
            "color": self._color_of_position(face, position),
            "face_color": self._color_of_position(face, (1, 1)),
        }
        if position == (1, 1):
            retval["type"] = "center"
        elif position in ((0, 1), (1, 0), (1, 2), (2, 1)):
            retval["type"] = "edge"
            retval["opposite"] = self._find_edge_opposite(face, position)
            retval["opposite_color"] = self._color_of_position(*retval["opposite"])
            retval["opposite_face_color"] = self._color_of_position(
                retval["opposite"][0], (1, 1)
            )
        elif position in ((0, 0), (0, 2), (2, 0), (2, 2)):
            retval["type"] = "corner"
            retval["mates"] = self._find_corner_mates(face, position)
            # (('F', (2, 2)), ('R', (2, 0)), ('D', (0, 2)))
            retval["mate_color"] = []
            retval["mate_face_color"] = []
            for mate in retval["mates"]:
                retval["mate_color"].append(self._color_of_position(*mate))
                retval["mate_face_color"].append(
                    self._color_of_position(mate[0], (1, 1))
                )
        else:
            retval["type"] = "unkown"

        return retval

    def _color_of_position(self, face, position):
        """
        Get the color of a specific position on the cube.
        """
        logging.debug("_color_of_position(%s, %s)", face, position)
        row, col = position
        return self.cube[face][row][col][0]

    def _find_edge_opposite(self, face, position):
        return OPPOSITE_EDGES.get((face, position))

    def _get_square_label(self, face, position):
        """
        Get the label of a specific square on the cube.
        """
        logging.warning("_get_square_label(%s,%s)", face, position)
        positions = {
            1: (0, 0),  # 1
            2: (0, 1),  # 2
            3: (0, 2),  # 3
            4: (1, 0),  # 4
            5: (1, 1),  # 5
            6: (1, 2),  # 6
            7: (2, 0),  # 7
            8: (2, 1),  # 8
            9: (2, 2),  # 9
        }
        row, col = positions[position]
        return self.cube[face][row][col]

    def _get_white_edge_by_color(self, color):
        """
        Get the white edge piece by its color.
        """
        edges = self._find_edge_pieces("W")
        for face, position in edges:
            edge_data = self._id_position(face, position)
            if edge_data["opposite_color"] == color:
                return face, position
        return "F", (1, 1)

    def _get_white_corner_by_color(self, colors):
        """
        Get the white corner piece by its colors.
        """
        logging.debug("cube._get_white_corner_by_color(%s)", colors)
        corners = self._sort_white_corners(self._find_corner_pieces("W"))
        for face, position in corners:
            corner_data = self._id_position(face, position)
            if sorted(colors) == sorted(corner_data["mate_color"]):
                return face, position
        return "F", (1, 1)

    def _find_corner_pieces(self, color):
        """
        Find corner pieces of the specified color.
        """
        logging.debug("_find_corner_pieces(%s)", color)
        corner_pieces = set()
        for face in self.faces:
            for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                if self.cube[face][row][col][0] == color:
                    corner_pieces.add((face, (row, col)))
        return corner_pieces

    def _find_corner_mates(self, face, position):
        """
        Find the corner mates for a given face and position.
        """
        logging.debug("cube._find_corner_mates(%s, %s)", face, position)
        row, col = position
        corner_mates = [
            (("F", (0, 0)), ("L", (0, 2)), ("U", (2, 0))),
            (("F", (0, 2)), ("U", (2, 2)), ("R", (0, 0))),
            (("F", (2, 0)), ("D", (0, 0)), ("L", (2, 2))),
            (("F", (2, 2)), ("R", (2, 0)), ("D", (0, 2))),
            (("B", (0, 0)), ("R", (0, 2)), ("U", (0, 2))),
            (("B", (0, 2)), ("U", (0, 0)), ("L", (0, 0))),
            (("B", (2, 0)), ("D", (2, 2)), ("R", (2, 2))),
            (("B", (2, 2)), ("L", (2, 0)), ("D", (2, 0))),
        ]
        target = (face, (row, col))
        for mates in corner_mates:
            if target in mates:
                return mates
        return None

    ##################
    # Solver Functions
    ##################

    def solve_white_cross(self):
        """
        Solve the bottom edges (white cross)
        """
        self._orient_cube()
        while not self._check_white_cross():
            edge_pieces = self._find_edge_pieces("W")
            sorted_edge_pieces = sorted(
                edge_pieces, key=lambda x: self.order.index(x[0])
            )
            for face, position in sorted_edge_pieces:
                if not self._place_white_edge(face, position):
                    break
        return self._check_white_cross()

    def _check_white_cross(self):
        """
        Check if the white cross is solved
        """
        logging.debug("cube._check_white_cross()")
        self._orient_cube()
        for square in [
            self.cube["D"][0][1],
            self.cube["D"][1][0],
            self.cube["D"][1][2],
            self.cube["D"][2][1],
        ]:
            if square[0] != "W":
                return False
        for side in self.sides:
            if self.cube[side][2][1][0] != self.cube[side][1][1][0]:
                return False
        return True

    def _place_white_edge(self, face, position):
        """
        Place the white edge in the correct position
        """
        logging.debug("_place_white_edge(%s,%s)", face, position)
        data = self._id_position(face, position)
        if face in "UD":
            # sides = "FLBR"
            side_map = "RBOG"
            pos_target = side_map.find(data["opposite_color"])
            pos_current = side_map.find(data["opposite_face_color"])
            moves = abs(pos_current - pos_target)
            if face == "D":
                if (
                    data["color"] == data["face_color"]
                    and data["opposite_color"] == data["opposite_face_color"]
                ):
                    return True
                if moves > 0:
                    command_string = (
                        f"{data['opposite'][0]}," * 2
                        + "U'," * moves
                        + f"{self._find_center(data['opposite_color'])}," * 2
                    )
                    self.run_command_string(command_string)
                    face, position = self._get_white_edge_by_color(
                        data["opposite_color"]
                    )
                    return self._place_white_edge(face, position)
            elif face == "U":
                if moves > 0:
                    command_string = (
                        "U'," * moves
                        + f"{self._find_center(data['opposite_color'])}," * 2
                    )
                    self.run_command_string(command_string)
                    face, position = self._get_white_edge_by_color(
                        data["opposite_color"]
                    )
                    return self._place_white_edge(face, position)
                command_string = f"{self._find_center(data['opposite_color'])}," * 2
                self.run_command_string(command_string)
                face, position = self._get_white_edge_by_color(data["opposite_color"])
                return self._place_white_edge(face, position)
        else:  # use transpose for sides
            logging.debug("Transposing command for %s %s", face, position)
            command_string = None
            if position == (1, 0):
                command_string = self._transpose_command("L',U,L", face)
            elif position == (1, 2):
                command_string = self._transpose_command("R,U,R'", face)
            elif position == (0, 1):
                command_string = self._transpose_command("F',L',U,L,F", face)
            elif position == (2, 1):
                command_string = self._transpose_command("F',R,U,R',F", face)
            if not command_string is None:
                logging.debug("command_string: %s", command_string)
                self.run_command_string(command_string)
                face, position = self._get_white_edge_by_color(data["opposite_color"])
                return self._place_white_edge(face, position)
        return False

    def solve_white_corners(self):
        """
        Solve the white corners
        """
        logging.debug("solve_white_corners()")
        self._orient_cube()
        counter = 0
        # print('solve_white_corners')
        while not self._check_white_corners():
            counter += 1
            if counter > 10:
                logging.warning("solve_white_corners loop detected")
                break
            corners = self._sort_white_corners(self._find_corner_pieces("W"))
            for face, position in corners:
                if not self._check_white_corner(face, position):
                    self._place_white_corner(face, position)
                    # break if we make changes, because corners is no longer valid
                    break
        return self._check_white_corners()

    def _check_white_corners(self):
        """
        Check if the white corners are in the correct position and oriented correctly
        """
        logging.debug("_check_white_corners()")
        self._orient_cube()
        # are all the white corners facing down
        for square in [
            self.cube["D"][0][0],
            self.cube["D"][0][2],
            self.cube["D"][2][0],
            self.cube["D"][2][2],
        ]:
            if square[0] != "W":
                return False
        # are all the white corners in the right slots
        corners = self._find_corner_pieces("W")
        # Sort corners based on the order string
        sorted_corners = sorted(corners, key=lambda x: self.order.index(x[0]))
        for face, position in sorted_corners:
            corner_data = self._id_position(face, position)
            if sorted(corner_data["mate_color"]) != sorted(
                corner_data["mate_face_color"]
            ):
                return False
        return True

    def _sort_white_corners(self, unsorted_corners):
        """
        Sort the white corners based on their colors
        """
        logging.debug("cube._sort_white_corners(%s)", unsorted_corners)
        sorted_corners = []
        color_order = [("R", "G"), ("G", "O"), ("O", "B"), ("B", "R")]
        target = color_order.pop()
        while len(sorted_corners) < 4:
            for face, position in unsorted_corners:
                corner_data = self._id_position(face, position)
                found = True
                for color in target:
                    if color not in corner_data["mate_color"]:
                        found = False
                if found:
                    sorted_corners.append((face, position))
                    if len(color_order) > 0:
                        target = color_order.pop()
        logging.debug("_sort_white_corners(%s)", sorted_corners)
        return sorted_corners

    def _check_white_corner(self, face, position):
        """
        Check if the white corner is in the correct position and oriented correctly
        """
        logging.debug("_check_white_corner(%s,%s)", face, position)
        corner_data = self._id_position(face, position)
        colors = corner_data["mate_color"]
        if face == "D":
            logging.debug("%s at bottom already", colors)
            if sorted(corner_data["mate_color"]) == sorted(
                corner_data["mate_face_color"]
            ):
                logging.debug("%s oriented correctly", colors)
                return True
        return False

    def _place_white_corner_down(self, face, position, corner_data, colors):
        """
        Place the white corner in the correct position from the bottom face
        """
        # if mate_color and mate_face_color have the same colors
        if sorted(corner_data["mate_color"]) == sorted(corner_data["mate_face_color"]):
            logging.debug("%s oriented correctly", colors)
            return True
        logging.debug("Wrong slot")
        command_strings = {
            (0, 0): "L',U,L",
            (0, 2): "R,U,R'",
            (2, 0): "L,U,L'",
            (2, 2): "R',U',R",
        }
        self.run_command_string(command_strings[position])
        face, position = self._get_white_corner_by_color(colors)
        return self._place_white_corner(face, position)

    def _place_white_corner_up(self, face, position, corner_data, colors):
        """
        Place the white corner in the correct position from the top face
        """
        mate_face = None
        mate_position = None
        logging.debug("%s facing Up", colors)
        face, position = self._hover_white_corner(face, position)
        face, position = self._get_white_corner_by_color(colors)
        corner_data = self._id_position(face, position)
        if face in self.sides:
            logging.debug("%s on side %s after hovering", colors, face)
            command_string = ""
            if position == (2, 2):
                command_string = "R,U,R'"
            elif position == (2, 0):
                command_string = "L',U',L"
            elif position == (0, 2):
                command_string = "F,U,F'"
            elif position == (0, 0):
                command_string = "R',F,R,F'"
            self.run_command_string(command_string)
            face, position = self._get_white_corner_by_color(colors)
            return self._place_white_corner(face, position)
        logging.debug("%s on side %s after hovering", colors, face)
        for mate_face, mate_position in corner_data["mates"]:
            if mate_face != "U":
                corner_data = self._id_position(mate_face, mate_position)
                break
        face = mate_face
        position = mate_position
        logging.debug("Found a mate: %s %s %s", mate_face, mate_position, corner_data)
        if position == (0, 0):
            self.run_command_string(self._transpose_command("L,L,U',L,L,U,L,L", face))
        if position == (0, 2):
            sides = "FLBR"
            face_idx = sides.find(face)
            face_idx -= 1
            if face_idx > 0:
                face_idx = 3
            tmp_face = sides[face_idx]
            self.run_command_string(
                self._transpose_command("L,L,U',L,L,U,L,L", tmp_face)
            )
        face, position = self._get_white_corner_by_color(colors)
        return self._place_white_corner(face, position)

    def _place_white_corner(self, face, position):
        """
        Place the white corner in the correct position
        """
        logging.debug("_place_white_corner(%s,%s)", face, position)
        corner_data = self._id_position(face, position)
        # save colors so we can find this corner again when we move it.
        colors = corner_data["mate_color"]
        if face == "D":
            logging.debug("%s at bottom already", colors)
            return self._place_white_corner_down(face, position, corner_data, colors)

        if face in self.sides:
            logging.debug("%s at side %s %s", colors, face, position)
            if position in ((2, 0), (2, 2)):
                logging.debug("%s on bottom row", colors)
                if sorted(corner_data["mate_color"]) == sorted(
                    corner_data["mate_face_color"]
                ):
                    logging.debug("%s is in the correct position, rotating", colors)
                    # rotate in place
                    command_string = "L',U',L"  # command for (2,0)
                    if position == (2, 2):
                        command_string = "R,U,R',U',R,U,R',U',R,U,R',U',R,U,R',U'"
                    self.run_command_string(
                        self._transpose_command(command_string, face)
                    )
                    face, position = self._get_white_corner_by_color(colors)
                    return self._place_white_corner(face, position)
                # pup up to top for next pass
                command_string = "L',U',L"  # string for (2,0)
                if position == (2, 2):
                    command_string = "R,U,R'"
                self.run_command_string(self._transpose_command(command_string, face))
                face, position = self._get_white_corner_by_color(colors)
                return self._place_white_corner(face, position)
            logging.debug("%s on top row", colors)
            face, position = self._hover_white_corner(face, position)
            face, position = self._get_white_corner_by_color(colors)
            corner_data = self._id_position(face, position)
            command_string = "U,R,U',R'"  # string for (0,2)
            if position == (0, 0):
                command_string = "U',L',U,L"
            self.run_command_string(self._transpose_command(command_string, face))
            face, position = self._get_white_corner_by_color(colors)
            return self._place_white_corner(face, position)
        if face == "U":
            self._place_white_corner_up(face, position, corner_data, colors)
        return None

    def _hover_white_corner(self, face, position):
        """
        Hover the white corner to the top layer
        """
        corner_data = self._id_position(face, position)
        match_colors = []
        for color in corner_data["mate_color"]:
            if color != "W":
                match_colors.append(color)
        found = False
        while not found:
            found = True
            for color in match_colors:
                if color not in corner_data["mate_face_color"]:
                    found = False
            if not found:
                sides = "FLBR"
                self._make_move("U")
                face_idx = sides.find(face)
                face_idx += 1
                if face_idx == 4:
                    face_idx = 0
                logging.debug(
                    " Setting face from %s to %s:%d", face, sides[face_idx], face_idx
                )
                face = sides[face_idx]
                corner_data = self._id_position(face, position)
        logging.debug("corner_data %s", corner_data)
        logging.debug("returning %s,%s", face, position)
        return face, position

    def solve_second_layer(self):
        """
        Solve the second layer
        """
        logging.debug("cube.solve_second_layer()")
        while not self._check_second_layer():
            edges = self._find_edge_pieces("RGOB")
            for face, position in edges:
                edge_data = self._id_position(face, position)
                if not (
                    edge_data["color"] not in "WY"
                    and edge_data["opposite_color"] not in "WY"
                ):
                    continue
                # skip edges that are already in the right place
                if (
                    edge_data["color"] != edge_data["face_color"]
                    or edge_data["opposite_color"] != edge_data["opposite_face_color"]
                ):
                    if position == (0, 1) and face != "U":
                        sides = "FLBR"
                        while edge_data["color"] != edge_data["face_color"]:
                            self.run_command_string("U")
                            face_idx = sides.find(face)
                            face_idx = (face_idx + 1) % 4
                            face = sides[face_idx]
                            edge_data = self._id_position(face, position)
                        if (edge_data["color"], edge_data["opposite_color"]) in (
                            ("O", "G"),
                            ("G", "R"),
                            ("R", "B"),
                            ("B", "O"),
                        ):
                            # break left
                            self.run_command_string(
                                self._transpose_command("U',L',U,L,U,F,U',F'", face)
                            )
                        else:
                            # break right
                            self.run_command_string(
                                self._transpose_command("U,R,U',R',U',F',U,F", face)
                            )
                        break
                    if face != "U":
                        if position == (1, 2):  # right side
                            self.run_command_string(
                                self._transpose_command("U,R,U',R',U',F',U,F", face)
                            )
                            break
                        self.run_command_string(
                            self._transpose_command("U',L',U,L,U,F,U',F'", face)
                        )
                        break
        return self._check_second_layer()

    def _check_second_layer(self):
        """
        Check if the second layer is complete
        """
        logging.debug("cube._check_second_layer()")
        self._orient_cube()
        for side in self.sides:
            # print(side,cube[side][1][0],cube[side][1][1],cube[side][1][2])
            color = self.cube[side][1][0][0]
            for square in [
                self.cube[side][1][0],
                self.cube[side][1][1],
                self.cube[side][1][1][0],
                self.cube[side][1][2],
            ]:
                if square[0] != color:
                    return False
        return True

    def solve_yellow_cross(self):
        """
        Solve the yellow cross
        """
        logging.debug("solve_yellow_cross()")
        self._orient_cube()
        counter = 0
        up_count = 0
        while up_count < 4:
            counter += 1
            if counter > 1000:
                logging.warning("solve_yellow_cross too many loops")
                break
            edge_pieces = self._find_edge_pieces("Y")
            up_count = 0
            for face, _ in edge_pieces:
                if face == "U":
                    up_count += 1
            if up_count < 4:
                while 1 <= up_count <= 2 and self.cube["U"][1][0][0] != "Y":
                    self.run_command_string("U")
                if up_count == 2:
                    if self.cube["U"][2][1][0] == "Y":
                        self.run_command_string("U")
                self.run_command_string("F,R,U,R',U',F'")
        return self._check_yellow_cross()

    def _check_yellow_cross(self):
        """
        Check if the yellow cross is complete
        """
        logging.debug("_check_yellow_cross()")
        self._orient_cube()
        for square in [
            self.cube["U"][0][1],
            self.cube["U"][1][0],
            self.cube["U"][1][2],
            self.cube["U"][2][1],
        ]:
            if square[0] != "Y":
                return False
        return True

    def solve_yellow_edges(self):
        """
        Solve the yellow edges
        """
        logging.debug("cube.solve_yellow_edges()")
        self._orient_cube()
        # changed = True
        counter = 0
        sides = self.sides
        target = "RGOB"
        logging.debug("solve_yellow_edges sides: %s", sides)
        while self._count_yellow_edges() < 4:
            counter += 1
            if counter > 100:
                logging.warning("solve_yellow_edges too many loops")
                break
            edge_colors = self._get_yellow_edges()
            # print("edge_colors",edge_colors)
            # right order, just rotated
            if target in edge_colors + edge_colors:
                # print("right order, just rotated")
                while self.cube["F"][0][1][0] != self.cube["F"][1][1][0]:
                    logging.debug(
                        "solve_yellow_edges: {self.cube['F'][0][1][0]} != {self.cube['F'][1][1][0]}"
                    )
                    self.run_command_string("U")
            else:
                # print("not the right order")
                self._orient_cube()
                for a, b in (("R", "G"), ("O", "B")):
                    while self.cube["F"][1][1][0] != a:
                        self.run_command_string("X")
                    while self.cube["F"][0][1][0] != a:
                        self.run_command_string("U")

                    if self.cube["R"][0][1][0] == b:
                        logging.debug("%s is in the right spot", b)
                    elif self.cube["L"][0][1][0] == b:
                        logging.debug("%s and %s are swapped", a, b)
                        # a and b are swapped
                        self.run_command_string("R,U,R',U,R,U,U,R',U")
                        # line up red edge
                        while self.cube["F"][0][1][0] != a:
                            self.run_command_string("U")
                    else:
                        logging.debug("%s is on the far side of the world", b)
                        # b is on the opposite side:
                        # rotate
                        self.run_command_string("U'")
                        # swap
                        self.run_command_string("R,U,R',U,R,U,U,R',U")
                self._orient_cube()
        return self._check_yellow_edges()

    def _check_yellow_edges(self):
        """
        Check if the yellow edges are in the right place
        """
        logging.debug("cube._check_yellow_edges")
        self._orient_cube()
        for side in self.sides:
            if self.cube[side][0][1][0] != self.cube[side][1][1][0]:
                return False
        return True

    def _count_yellow_edges(self):
        """
        Count the number of yellow edges
        """
        logging.debug("cube._count_yellow_edges()")
        count = 0
        edge_pieces = self._find_edge_pieces("Y")
        logging.debug("edge_pieces: %s", edge_pieces)
        self._orient_cube()
        for _ in range(4):
            logging.debug("%s,%s", self.cube["F"][0][1], self.cube["F"][1][1])
            if self.cube["F"][0][1][0] == self.cube["F"][1][1][0]:
                count += 1
            self.run_command_string("X")
        return count

    def _get_yellow_edges(self):
        """
        Get the colors of the yellow edges
        """
        logging.debug("cube._get_yellow_edges")
        edge_colors = ""
        for side in self.sides:
            edge_colors += self.cube[side][0][1][0]
        return edge_colors

    def solve_yellow_corners(self):
        """
        Solve the yellow corners
        """
        logging.debug("cube.solve_yellow_corners()")
        counter = 0
        while True:
            counter += 1
            if counter > 100:
                logging.warning("solve_yellow_corners too many loops")
                break
            corners = self._find_corner_pieces("Y")
            logging.debug(corners)
            matched_corners = []
            for face, position in corners:
                corner_data = self._id_position(face, position)
                face_colors = []
                for mate in corner_data["mates"]:
                    face_colors.append(self.cube[mate[0]][1][1][0])
                if sorted(corner_data["mate_color"]) == sorted(face_colors):
                    matched_corners.append((face, position))
                logging.debug(matched_corners)
            if len(matched_corners) == 0:
                self.run_command_string("U,R,U',L',U,R',U',L")
            if len(matched_corners) == 1:
                corner_data = self._id_position(
                    matched_corners[0][0], matched_corners[0][1]
                )
                target = ("F", (0, 2))
                if target in corner_data["mates"]:
                    self.run_command_string("U,R,U',L',U,R',U',L")
                else:
                    self.run_command_string("X")
            if len(matched_corners) in [2, 3]:
                logging.warning("How did this happen?")
            elif len(matched_corners) == 4:
                return True
            else:
                logging.debug("cube.solve_yellow_corners: We shouldn't get here!")
        return False

    def orient_yellow_corners(self):
        """
        Orient the yellow corners
        """
        logging.debug("orient_yellow_corners()")
        self._orient_cube()
        # top_corners = [("U", (0, 0)), ("U", (0, 2)), ("U", (2, 0)), ("U", (2, 2))]
        counter = 0
        while self._up_yellow_corner_count() < 4:
            counter += 1
            if counter > 12:
                logging.warning("breaking orient_yellow_corners loop")
                break
            while self.cube["U"][2][2][0] == "Y":
                self.run_command_string("U")
            self.run_command_string("R',D',R,D")
            self.run_command_string("R',D',R,D")
        while self.cube["F"][0][1][0] != self.cube["F"][1][1][0]:
            self.run_command_string("U")
        return self._check_yellow_corners()

    def _check_yellow_corners(self):
        """
        Check if the yellow corners are in the right place
        """
        logging.debug("cube._check_yellow_corners()")
        self._orient_cube()
        # are all the white corners facing down
        for square in [
            self.cube["U"][0][0],
            self.cube["U"][0][2],
            self.cube["U"][2][0],
            self.cube["U"][2][2],
        ]:
            if square[0] != "Y":
                return False
        # are all the white corners in the right slots
        corners = self._find_corner_pieces("Y")
        # Sort corners based on the order string
        sorted_corners = sorted(corners, key=lambda x: self.order.index(x[0]))
        logging.debug(sorted_corners)
        for face, position in sorted_corners:
            corner_data = self._id_position(face, position)
            if sorted(corner_data["mate_color"]) != sorted(
                corner_data["mate_face_color"]
            ):
                return False
        return True

    def _up_yellow_corner_count(self):
        """
        Count the number of yellow corners
        """
        logging.debug("cube._up_yellow_corner_count()")
        top_corners = [("U", (0, 0)), ("U", (0, 2)), ("U", (2, 0)), ("U", (2, 2))]
        count = 0
        for corner in top_corners:
            if self.cube[corner[0]][corner[1][0]][corner[1][1]][0] == "Y":
                count += 1
        logging.debug("_up_yellow_corner_count = %d", count)
        return count

    def solve(self):
        """
        Solve the cube
        """
        logging.debug("cube.solve")
        steps = [
            ("solve_white_cross", self.solve_white_cross),
            ("solve_white_corners", self.solve_white_corners),
            ("solve_second_layer", self.solve_second_layer),
            ("solve_yellow_cross", self.solve_yellow_cross),
            ("solve_yellow_edges", self.solve_yellow_edges),
            ("solve_yellow_corners", self.solve_yellow_corners),
            ("orient_yellow_corners", self.orient_yellow_corners),
        ]

        for step_name, step_func in steps:
            if not step_func():
                return False, step_name

        return True, None

    def clock(self):
        """
        Solve the cube using the clock method
        """
        logging.debug("cube.clock")
        steps = [
            ("solve_white_cross", self.solve_white_cross),
            ("solve_white_corners", self.solve_white_corners),
            ("solve_second_layer", self.solve_second_layer),
            ("solve_yellow_cross", self.solve_yellow_cross),
            ("solve_yellow_edges", self.solve_yellow_edges),
            ("solve_yellow_corners", self.solve_yellow_corners),
            ("orient_yellow_corners", self.orient_yellow_corners),
        ]

        all_start_time = time.time()
        for step_name, step_func in steps:
            start_time = time.time()
            if not step_func():
                break
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000  # convert to milliseconds
            print(f"{step_name} took {time_taken:.2f} ms")
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000
        end_time = time.time()
        time_taken = (end_time - all_start_time) * 1000
        print(f"Total took {time_taken:.2f} ms")
        return time_taken
