import json
import logging
import random
import time


class cube:
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
        self.debug = False
        self.type = 1
        self.original_logging_level = logging.getLogger().getEffectiveLevel()
        self.new_cube()  # initialize cube even if we are loading a file
        if filename is not None:
            self.load(filename)

    def print(self):
        logging.debug(f"cube{self.type}.print()")
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
                if self.debug:
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
        logging.debug(f"cube.set_debug({debug})")
        """
        Sets the debug mode.
        """
        self.debug = debug
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(self.original_logging_level)

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
                    save_data[f"{face}{position}"] = self.get_square_label(
                        face, position
                    )

            # Convert the cube to a JSON string
            save_json = json.dumps(save_data, indent=4)

            # Write the JSON string to a file
            with open(filename, "w") as file:
                file.write(save_json)

            logging.info(f"Cube successfully saved to {filename}")
        except Exception as e:
            logging.warning(f"An error occurred: {e}")

    def load(self, filename):
        """
        Load the cube representation from a JSON file.

        Parameters:
        filename (str): The name of the file to load the JSON data.
        """
        try:
            """
            {
  "F1": "R1",
  "F2": "R2",
  "F3": "R3",
  "F4": "R4",
  "F5": "R5",
  "F6": "R6",
          """
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
            with open(filename, "r") as file:
                data_json = file.read()
            data = json.loads(data_json)
            for position, value in data.items():
                row, col = positions[int(position[1])]
                self.cube[position[0]][row][col] = value
            logging.info(f"Cube successfully loaded from {filename}")
        except Exception as e:
            logging.warning(f"An error occurred: {e}")

    def scramble(self, moves=40):
        logging.debug(f"cube.scramble({moves})")
        for _ in range(moves):
            face = random.choice(self.faces + "CM")
            clockwise = random.choice([True, False])
            self.rotate(face, clockwise)

    def orient_cube(self):
        logging.debug(f"cube.orient_cube()")
        self.orient_face("W", "D")
        while self.cube["F"][1][1][0] != "R":
            self.rotate_cube()

    def orient_face(self, color, face):
        logging.debug(f"cube.orient_face({color},{face})")
        if face in "UDFB":
            while self.find_center(color) not in "UDFB":
                logging.debug(f"Rotating from {self.find_center(color)}")
                self.rotate_cube()
            while self.find_center(color) not in face:
                logging.debug(f"Tilting from {self.find_center(color)}")
                self.tilt_cube(cube)
        else:
            logging.debug(f"Face {face} is either L OR R")
            while self.find_center(color) not in "LRFB":
                logging.debug(f"Tilting from {self.find_center(color)}")
                self.tilt_cube()
            while self.find_center(color) not in face:
                logging.debug(f"Rotating from {self.find_center(color)}")
                self.rotate_cube()

    def find_center(self, color):
        logging.debug(f"cube.find_center({color})")
        for face in self.faces:
            logging.debug(f"find_center({color}) {face} {self.cube[face][1][1]}")
            if self.cube[face][1][1][0] == color:
                return face

    def rotate_cube(self, clockwise=True):
        logging.debug(f"cube.rotate_cube({clockwise})")
        self.rotate("U", not clockwise)
        # decision point, should middle rotate like up or down?
        self.rotate("M", not clockwise)
        self.rotate("D", clockwise)

    def tilt_cube(self, clockwise=True):
        logging.debug(f"cube.tilt_cube({clockwise})")
        self.rotate("L", not clockwise)
        self.rotate("C", clockwise)
        self.rotate("R", clockwise)

    def make_move(self, move):
        logging.debug(f"make_move({move})")
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

    def rotate(self, face, clockwise=True):
        # FIXME,  this could be simplified by directly assigning squares:
        # Example:
        """
        c = self.cube
        if face == 'F' and clockwise:
            c['U'][2][0],c['U'][2][1],c['U'][2][2],c['R'][0][0],c['R'][1][0],c['R'][2][0],c.['D'][0][2],c.['D'][0][1],c.['D'][0][0],c.['L'][2][2],c.['L'][1][2],c.['L'][0][2] = [c.['L'][2][2],c.['L'][1][2],c.['L'][0][2],c['U'][2],c['R'][0][0],c['R'][1][0],c['R'][2][0],c.['D'][0]]

        """
        logging.debug(f"cube.rotate({face}, {clockwise})")
        # Rotate the face itself
        if face not in "CM":
            if clockwise:
                self.cube[face] = [list(row) for row in zip(*self.cube[face][::-1])]
            else:
                self.cube[face] = [list(row) for row in zip(*self.cube[face])][::-1]

        # C rotation currently has counterclockwise logic, so reverse to make it work as expected.
        # if face == 'C':
        #    clockwise = not clockwise

        # Extract the rows/columns to be rotated
        rows_cols = []

        if face == "F":
            if clockwise:
                rows_cols.extend(self.cube["U"][2])
                rows_cols.append(self.cube["R"][2][0])
                rows_cols.append(self.cube["R"][1][0])
                rows_cols.append(self.cube["R"][0][0])
                rows_cols.extend(reversed(self.cube["D"][0]))
                rows_cols.append(self.cube["L"][2][2])
                rows_cols.append(self.cube["L"][1][2])
                rows_cols.append(self.cube["L"][0][2])
            else:
                rows_cols.extend(self.cube["U"][2])
                rows_cols.append(self.cube["R"][0][0])
                rows_cols.append(self.cube["R"][1][0])
                rows_cols.append(self.cube["R"][2][0])
                rows_cols.extend(reversed(self.cube["D"][0]))
                rows_cols.append(self.cube["L"][0][2])
                rows_cols.append(self.cube["L"][1][2])
                rows_cols.append(self.cube["L"][2][2])
        elif face == "B":
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
        elif face == "U":
            rows_cols.extend(self.cube["B"][0])
            rows_cols.extend(self.cube["R"][0])
            rows_cols.extend(self.cube["F"][0])
            rows_cols.extend(self.cube["L"][0])
        elif face == "D":
            rows_cols.extend(self.cube["F"][2])
            rows_cols.extend(self.cube["R"][2])
            rows_cols.extend(self.cube["B"][2])
            rows_cols.extend(self.cube["L"][2])
        elif face == "L":
            # UFDB
            for neighbor in "UFD":
                rows_cols.append(self.cube[neighbor][0][0])
                rows_cols.append(self.cube[neighbor][1][0])
                rows_cols.append(self.cube[neighbor][2][0])
            rows_cols.append(self.cube["B"][2][2])
            rows_cols.append(self.cube["B"][1][2])
            rows_cols.append(self.cube["B"][0][2])
        elif face == "R":
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
        elif face == "C":
            rows_cols.append(self.cube["B"][0][1])
            rows_cols.append(self.cube["B"][1][1])
            rows_cols.append(self.cube["B"][2][1])
            for neighbor in "DFU":
                rows_cols.append(self.cube[neighbor][2][1])
                rows_cols.append(self.cube[neighbor][1][1])
                rows_cols.append(self.cube[neighbor][0][1])

        elif face == "M":
            # for neighbor in 'LFRB':
            # shift self.sides by one side
            for neighbor in self.sides[1:] + self.sides[:1]:
                rows_cols.extend(self.cube[neighbor][1])

        # print(rows_cols)
        # Rotate the extracted rows/columns
        if clockwise:
            rows_cols = rows_cols[-3:] + rows_cols[:-3]
        else:
            rows_cols = rows_cols[3:] + rows_cols[:3]
        # print(rows_cols)

        if face == "F":
            self.cube["U"][2] = rows_cols[0:3]
            self.cube["R"][0][0] = rows_cols[3]
            self.cube["R"][1][0] = rows_cols[4]
            self.cube["R"][2][0] = rows_cols[5]
            self.cube["D"][0] = rows_cols[6:9]
            self.cube["L"][2][2] = rows_cols[9]
            self.cube["L"][1][2] = rows_cols[10]
            self.cube["L"][0][2] = rows_cols[11]
        elif face == "B":
            self.cube["U"][0] = rows_cols[0:3]
            self.cube["L"][0][0] = rows_cols[3]
            self.cube["L"][1][0] = rows_cols[4]
            self.cube["L"][2][0] = rows_cols[5]
            self.cube["D"][2] = rows_cols[6:9]
            self.cube["R"][2][2] = rows_cols[9]
            self.cube["R"][1][2] = rows_cols[10]
            self.cube["R"][0][2] = rows_cols[11]
        elif face == "U":
            self.cube["B"][0] = rows_cols[0:3]
            self.cube["R"][0] = rows_cols[3:6]
            self.cube["F"][0] = rows_cols[6:9]
            self.cube["L"][0] = rows_cols[9:12]
        elif face == "D":
            self.cube["F"][2] = rows_cols[0:3]
            self.cube["R"][2] = rows_cols[3:6]
            self.cube["B"][2] = rows_cols[6:9]
            self.cube["L"][2] = rows_cols[9:12]
        elif face == "L":
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
        elif face == "R":
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
        elif face == "C":
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
        elif face == "M":
            self.cube["L"][1] = rows_cols[0:3]
            self.cube["F"][1] = rows_cols[3:6]
            self.cube["R"][1] = rows_cols[6:9]
            self.cube["B"][1] = rows_cols[9:12]

    """
    Command String functions
    """

    def transpose_command(self, command_string, target, source="F"):
        logging.debug(f'cube.transpose_command("{command_string}",{target},{source})')
        new_command = ""
        if target in self.sides:
            offset = self.sides.find(target) - self.sides.find(source)
            codex = self.sides[offset:] + self.sides[:offset]
            logging.debug(f"offset: {offset}")
            for char in command_string:
                if char in self.sides:
                    idx = self.sides.find(char)
                    new_command += codex[idx]
                else:
                    new_command += char
        else:
            new_command = "X,X'"
        logging.debug(f"cube.transpose_command returning {new_command}")
        return new_command

    def run_command_string(self, command):
        logging.debug(f"cube.run_command_string(cube,{command})")
        for move in command.rstrip(",").lstrip(",").split(","):
            self.make_move(move)

    def superflip(self):
        """
        Run superflip algorithm
        """
        self.run_command_string(
            "R,L,U,U,F,U',D,F,F,R,R,B,B,L,U,U,F',B',U,R,R,D,F,F,U,R,R,U"
        )

    """
    Search and Identify functions
    """

    def find_edge_pieces(self, colors):
        logging.debug(f"find_edge_pieces({colors})")
        edge_pieces = set()
        for face in self.faces:
            logging.debug(f"{face},{self.cube[face]}")
            for row, col in [(0, 1), (1, 0), (1, 2), (2, 1)]:
                logging.debug(f"row: {row}, col: {col}")
                if self.cube[face][row][col][0] in colors:
                    edge_pieces.add((face, (row, col)))
        return edge_pieces

    def id_position(self, face, position):
        logging.debug(f"id_position(cube,{face},{position})")
        retval = {
            "face": face,
            "color": self.color_of_position(face, position),
            "face_color": self.color_of_position(face, (1, 1)),
        }
        if position == (1, 1):
            retval["type"] = "center"
        elif position in ((0, 1), (1, 0), (1, 2), (2, 1)):
            retval["type"] = "edge"
            retval["opposite"] = self.find_edge_opposite(face, position)
            retval["opposite_color"] = self.color_of_position(*retval["opposite"])
            retval["opposite_face_color"] = self.color_of_position(
                retval["opposite"][0], (1, 1)
            )
        elif position in ((0, 0), (0, 2), (2, 0), (2, 2)):
            retval["type"] = "corner"
            retval["mates"] = self.find_corner_mates(face, position)
            # (('F', (2, 2)), ('R', (2, 0)), ('D', (0, 2)))
            retval["mate_color"] = []
            retval["mate_face_color"] = []
            for mate in retval["mates"]:
                retval["mate_color"].append(self.color_of_position(*mate))
                retval["mate_face_color"].append(
                    self.color_of_position(mate[0], (1, 1))
                )
        else:
            retval["type"] = "unkown"

        return retval

    def color_of_position(self, face, position):
        logging.debug(f"color_of_position({face}, {position})")
        row, col = position
        return self.cube[face][row][col][0]

    def find_edge_opposite(self, face, position):
        logging.debug(f"find_edge_opposite({face}, {position})")
        row, col = position
        opposite_edges = {
            ("U", (0, 1)): ("B", (0, 1)),
            ("B", (0, 1)): ("U", (0, 1)),
            ("U", (2, 1)): ("F", (0, 1)),
            ("F", (0, 1)): ("U", (2, 1)),
            ("U", (1, 0)): ("L", (0, 1)),
            ("L", (0, 1)): ("U", (1, 0)),
            ("U", (1, 2)): ("R", (0, 1)),
            ("R", (0, 1)): ("U", (1, 2)),
            ("D", (0, 1)): ("F", (2, 1)),
            ("F", (2, 1)): ("D", (0, 1)),
            ("D", (2, 1)): ("B", (2, 1)),
            ("B", (2, 1)): ("D", (2, 1)),
            ("D", (1, 0)): ("L", (2, 1)),
            ("L", (2, 1)): ("D", (1, 0)),
            ("D", (1, 2)): ("R", (2, 1)),
            ("R", (2, 1)): ("D", (1, 2)),
            ("F", (1, 0)): ("L", (1, 2)),
            ("L", (1, 2)): ("F", (1, 0)),
            ("F", (1, 2)): ("R", (1, 0)),
            ("R", (1, 0)): ("F", (1, 2)),
            ("B", (1, 0)): ("R", (1, 2)),
            ("R", (1, 2)): ("B", (1, 0)),
            ("B", (1, 2)): ("L", (1, 0)),
            ("L", (1, 0)): ("B", (1, 2)),
        }
        return opposite_edges.get((face, (row, col)), None)

    def get_square_label(self, face, position):
        logging.warning(f"get_square_label({face},{position})")
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

    def get_white_edge_by_color(self, color):
        edges = self.find_edge_pieces("W")
        for face, position in edges:
            edge_data = self.id_position(face, position)
            if edge_data["opposite_color"] == color:
                return face, position
        return "F", (1, 1)

    def get_white_corner_by_color(self, colors):
        logging.debug(f"cube.get_white_corner_by_color({colors})")
        corners = self.sort_white_corners(self.find_corner_pieces("W"))
        for face, position in corners:
            corner_data = self.id_position(face, position)
            if sorted(colors) == sorted(corner_data["mate_color"]):
                return face, position
        return "F", (1, 1)

    def find_corner_pieces(self, color):
        logging.debug(f"find_corner_pieces({color})")
        corner_pieces = set()
        for face in self.faces:
            for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                if self.cube[face][row][col][0] == color:
                    corner_pieces.add((face, (row, col)))
        return corner_pieces

    def find_corner_mates(self, face, position):
        logging.debug(f"cube.find_corner_mates({face},{position})")
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

    """
    Solver Functions
    """

    def solve_white_cross(self):
        logging.debug(f"cube.solve_white_cross()")
        """
        Solve the bottom edges (white cross)
        """
        self.orient_cube()
        counter = 0
        while not self.check_white_cross():
            counter += 1
            if counter > 100:
                log.warning("cube.solve_white_cross() too many loops")
                break
            edge_pieces = self.find_edge_pieces("W")
            sorted_edge_pieces = sorted(
                edge_pieces, key=lambda x: self.order.index(x[0])
            )
            for face, position in sorted_edge_pieces:
                if not self.place_white_edge(face, position):
                    break
        return self.check_white_cross()

    def check_white_cross(self):
        logging.debug(f"cube.check_white_cross()")
        self.orient_cube()
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

    def place_white_edge(self, face, position, recursion_level=-1):
        logging.debug(f"place_white_edge({face},{position},{recursion_level})")
        recursion_level += 1
        if recursion_level > 10:
            return False
        data = self.id_position(face, position)
        if face in "UD":
            sides = "FLBR"
            side_map = "RBOG"
            pos_target = side_map.find(data["opposite_color"])
            pos_current = side_map.find(data["opposite_face_color"])
            moves = abs(pos_current - pos_target)
            if face == "D":
                # {'face': 'D', 'color': 'W', 'face_color': 'W', 'type': 'edge', 'opposite': ('B', (2, 1)), 'opposite_color': 'G', 'opposite_face_color': 'O'}
                if (
                    data["color"] == data["face_color"]
                    and data["opposite_color"] == data["opposite_face_color"]
                ):
                    return True
                if moves > 0:
                    command_string = (
                        f"{data['opposite'][0]}," * 2
                        + "U'," * moves
                        + f"{self.find_center(data['opposite_color'])}," * 2
                    )
                    self.run_command_string(command_string)
                    face, position = self.get_white_edge_by_color(
                        data["opposite_color"]
                    )
                    return self.place_white_edge(face, position, recursion_level)
            elif face == "U":
                if moves > 0:
                    command_string = (
                        "U'," * moves
                        + f"{self.find_center(data['opposite_color'])}," * 2
                    )
                    self.run_command_string(command_string)
                    face, position = self.get_white_edge_by_color(
                        data["opposite_color"]
                    )
                    return self.place_white_edge(face, position, recursion_level)
                else:
                    command_string = f"{self.find_center(data['opposite_color'])}," * 2
                    self.run_command_string(command_string)
                    face, position = self.get_white_edge_by_color(
                        data["opposite_color"]
                    )
                    return self.place_white_edge(face, position, recursion_level)
        else:  # use transpose for sides
            logging.debug(f"Transposing command for {face} {position}")
            command_string = None
            if position == (1, 0):
                command_string = self.transpose_command("L',U,L", face)
            elif position == (1, 2):
                command_string = self.transpose_command("R,U,R'", face)
            elif position == (0, 1):
                command_string = self.transpose_command("F',L',U,L,F", face)
            elif position == (2, 1):
                command_string = self.transpose_command("F',R,U,R',F", face)
            if not command_string is None:
                logging.debug(f"command_string: {command_string}")
                self.run_command_string(command_string)
                face, position = self.get_white_edge_by_color(data["opposite_color"])
                return self.place_white_edge(face, position, recursion_level)
        return False

    def solve_white_corners(self):
        logging.debug(f"solve_white_corners()")
        self.orient_cube()
        counter = 0
        # print('solve_white_corners')
        while not self.check_white_corners():
            counter += 1
            if counter > 10:
                logging.warning("solve_white_corners loop detected")
                break
            corners = self.sort_white_corners(self.find_corner_pieces("W"))
            for face, position in corners:
                if not self.check_white_corner(face, position):
                    self.place_white_corner(face, position)
                    # break if we make changes, because corners is no longer valid
                    break
        return self.check_white_corners()

    def check_white_corners(self):
        logging.debug(f"check_white_corners()")
        self.orient_cube()
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
        corners = self.find_corner_pieces("W")
        # Sort corners based on the order string
        sorted_corners = sorted(corners, key=lambda x: self.order.index(x[0]))
        for face, position in sorted_corners:
            corner_data = self.id_position(face, position)
            if sorted(corner_data["mate_color"]) != sorted(
                corner_data["mate_face_color"]
            ):
                return False
        return True

    def sort_white_corners(self, unsorted_corners):
        logging.debug(f"cube.sort_white_corners({unsorted_corners})")
        sorted_corners = []
        color_order = [("R", "G"), ("G", "O"), ("O", "B"), ("B", "R")]
        target = color_order.pop()
        while len(sorted_corners) < 4:
            for face, position in unsorted_corners:
                corner_data = self.id_position(face, position)
                found = True
                for color in target:
                    if color not in corner_data["mate_color"]:
                        found = False
                if found:
                    sorted_corners.append((face, position))
                    if len(color_order) > 0:
                        target = color_order.pop()
            pass
        logging.debug(f"sort_white_corners({sorted_corners})")
        return sorted_corners

    def check_white_corner(self, face, position):
        logging.debug(f"check_white_corner({face},{position})")
        corner_data = self.id_position(face, position)
        colors = corner_data["mate_color"]
        if face == "D":
            logging.debug(f"{colors} at bottom already")
            if sorted(corner_data["mate_color"]) == sorted(
                corner_data["mate_face_color"]
            ):
                logging.debug(f"{colors} oriented correctly")
                return True
            else:
                return False
        else:
            return False

    def place_white_corner(self, face, position, recursion_level=-1):
        logging.debug(f"place_white_corner({face},{position},{recursion_level})")
        recursion_level += 1
        if recursion_level > 10:
            return False
        corner_data = self.id_position(face, position)
        # save colors so we can find this corner again when we move it.
        colors = corner_data["mate_color"]
        if face == "D":
            logging.debug(f"{colors} at bottom already")
            # if mate_color and mate_face_color have the same colors
            if sorted(corner_data["mate_color"]) == sorted(
                corner_data["mate_face_color"]
            ):
                logging.debug(f"{colors} oriented correctly")
                return True
            else:
                logging.debug("Wrong slot")
                command_strings = {
                    (0, 0): "L',U,L",
                    (0, 2): "R,U,R'",
                    (2, 0): "L,U,L'",
                    (2, 2): "R',U',R",
                }
                self.run_command_string(command_strings[position])
                face, position = self.get_white_corner_by_color(colors)
                return self.place_white_corner(face, position, recursion_level)
        elif face in self.sides:
            logging.debug(f"{colors} at side {face} {position}")
            if position in ((2, 0), (2, 2)):
                logging.debug(f"{colors} on bottom row")
                if sorted(corner_data["mate_color"]) == sorted(
                    corner_data["mate_face_color"]
                ):
                    logging.debug(f"{colors} is in the correct position, rotating")
                    # rotate in place
                    command_string = "L',U',L"  # command for (2,0)
                    if position == (2, 2):
                        command_string = "R,U,R',U',R,U,R',U',R,U,R',U',R,U,R',U'"
                    self.run_command_string(
                        self.transpose_command(command_string, face)
                    )
                    face, position = self.get_white_corner_by_color(colors)
                    return self.place_white_corner(face, position, recursion_level)
                else:  # pup up to top for next pass
                    command_string = "L',U',L"  # string for (2,0)
                    if position == (2, 2):
                        command_string = "R,U,R'"
                    self.run_command_string(
                        self.transpose_command(command_string, face)
                    )
                    face, position = self.get_white_corner_by_color(colors)
                    return self.place_white_corner(face, position, recursion_level)
            else:
                logging.debug(f"{colors} on top row")
                face, position = self.hover_white_corner(face, position)
                face, position = self.get_white_corner_by_color(colors)
                corner_data = self.id_position(face, position)
                command_string = "U,R,U',R'"  # string for (0,2)
                if position == (0, 0):
                    command_string = "U',L',U,L"
                self.run_command_string(self.transpose_command(command_string, face))
                face, position = self.get_white_corner_by_color(colors)
                return self.place_white_corner(face, position, recursion_level)
        elif face == "U":
            logging.debug(f"{colors} facing Up")
            face, position = self.hover_white_corner(face, position)
            face, position = self.get_white_corner_by_color(colors)
            corner_data = self.id_position(face, position)
            if face in self.sides:
                logging.debug(f"{colors} on side {face} after hovering")
                command_string = ""
                if position == (2, 2):
                    command_string = "R,U,R'"
                elif position == (2, 0):
                    command_string = "L',U',L"
                elif position == (0, 2):
                    command_string = "F,U,F'"
                elif position == (0, 0):
                    command_string = "R',F,R,F'"
                self.run_command_string(command_string, face)
                face, position = self.get_white_corner_by_color(colors)
                return self.place_white_corner(face, position, recursion_level)
            else:
                logging.debug(f"{colors} on side {face} after hovering")
                for mate_face, mate_position in corner_data["mates"]:
                    if mate_face != "U":
                        corner_data = self.id_position(mate_face, mate_position)
                        break
                face = mate_face
                position = mate_position
                logging.debug(
                    f"Found a mate: {mate_face} {mate_position} {corner_data}"
                )
                if position == (0, 0):
                    self.run_command_string(
                        self.transpose_command("L,L,U',L,L,U,L,L", face)
                    )
                if position == (0, 2):
                    sides = "FLBR"
                    face_idx = sides.find(face)
                    face_idx -= 1
                    if face_idx > 0:
                        face_idx = 3
                    tmp_face = sides[face_idx]
                    self.run_command_string(
                        self.transpose_command("L,L,U',L,L,U,L,L", tmp_face)
                    )
                else:
                    pass
                face, position = self.get_white_corner_by_color(colors)
                return self.place_white_corner(face, position, recursion_level)
        else:
            pass
        return None

    def hover_white_corner(self, face, position):
        logging.debug(f"cube.hover_white_corner(cube,{face},{position})")
        # put the white corner on the top above its final position
        """
        hover_white_corner(cube,B,(0, 0))
        corner_data {'face': 'B', 'color': 'W', 'face_color': 'O', 'type': 'corner', 'mates': (('B', (0, 0)), ('R', (0, 2)), ('U', (0, 2))), 'mate_color': ['W', 'B', 'R'], 'mate_face_color': ['O', 'G', 'Y']}
        """
        corner_data = self.id_position(face, position)
        match_colors = []
        for color in corner_data["mate_color"]:
            if color != "W":
                match_colors.append(color)
        found = False
        while not found:
            found = True
            for color in match_colors:
                # print(f"Is {color} from {match_colors} in mate_face_color {corner_data['mate_face_color']}")
                if color not in corner_data["mate_face_color"]:
                    # print("No")
                    found = False
            if not found:
                # print("Not aligned, rotate once")
                sides = "FLBR"
                self.make_move("U")
                face_idx = sides.find(face)
                face_idx += 1
                if face_idx == 4:
                    face_idx = 0
                logging.debug(
                    f" Setting face from {face} to {sides[face_idx]}:{face_idx}"
                )
                face = sides[face_idx]
                corner_data = self.id_position(face, position)
        logging.debug(f"corner_data {corner_data}")
        logging.debug(f"returning {face},{position}")
        return face, position

    def solve_second_layer(self):
        logging.debug("cube.solve_second_layer()")
        counter = 0
        while not self.check_second_layer():
            counter += 1
            if counter > 200:
                logging.warning("solve_second_layer breaking loop")
                break
            edges = self.find_edge_pieces("RGOB")
            for face, position in edges:
                edge_data = self.id_position(face, position)
                # {'face': 'R', 'color': 'G', 'face_color': 'G', 'type': 'edge', 'opposite': ('B', (1, 0)), 'opposite_color': 'O', 'opposite_face_color': 'O'}
                if (
                    edge_data["color"] not in "WY"
                    and edge_data["opposite_color"] not in "WY"
                ):
                    # skip edges that are already in the right place
                    if (
                        edge_data["color"] != edge_data["face_color"]
                        or edge_data["opposite_color"]
                        != edge_data["opposite_face_color"]
                    ):
                        if position == (0, 1) and face != "U":
                            sides = "FLBR"
                            sentinel = 0
                            while edge_data["color"] != edge_data["face_color"]:
                                sentinel += 1
                                if sentinel > 4:
                                    return
                                self.run_command_string("U")
                                face_idx = sides.find(face)
                                face_idx += 1
                                if face_idx == 4:
                                    face_idx = 0
                                face = sides[face_idx]
                                edge_data = self.id_position(face, position)
                            if (edge_data["color"], edge_data["opposite_color"]) in (
                                ("O", "G"),
                                ("G", "R"),
                                ("R", "B"),
                                ("B", "O"),
                            ):
                                # break left
                                self.run_command_string(
                                    self.transpose_command("U',L',U,L,U,F,U',F'", face)
                                )
                            else:
                                # break right
                                self.run_command_string(
                                    self.transpose_command("U,R,U',R',U',F',U,F", face)
                                )
                            break
                        elif face == "U":
                            pass
                        else:
                            # print("Not top: ",edge_data,position,counter)
                            if position == (1, 2):  # right side
                                # run_command_string(cube,transpose_command("U,R,U',R',U',F',U,F,U,U,U,R,U',R',U',F',U,F",face))
                                self.run_command_string(
                                    self.transpose_command("U,R,U',R',U',F',U,F", face)
                                )
                                break
                            else:
                                self.run_command_string(
                                    self.transpose_command("U',L',U,L,U,F,U',F'", face)
                                )
                                break
        return self.check_second_layer()

    def check_second_layer(self):
        logging.debug(f"cube.check_second_layer()")
        self.orient_cube()
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
        logging.debug(f"solve_yellow_cross()")
        self.orient_cube()
        counter = 0
        up_count = 0
        while up_count < 4:
            counter += 1
            if counter > 1000:
                logging.warning("solve_yellow_cross too many loops")
                break
            edge_pieces = self.find_edge_pieces("Y")
            up_count = 0
            for face, position in edge_pieces:
                # print(face,position)
                if face == "U":
                    up_count += 1
            if up_count < 4:
                while 1 <= up_count <= 2 and self.cube["U"][1][0][0] != "Y":
                    self.run_command_string("U")
                if up_count == 2:
                    if self.cube["U"][2][1][0] == "Y":
                        self.run_command_string("U")
                self.run_command_string("F,R,U,R',U',F'")
        return self.check_yellow_cross()

    def check_yellow_cross(self):
        logging.debug(f"check_yellow_cross()")
        self.orient_cube()
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
        logging.debug(f"cube.solve_yellow_edges()")
        self.orient_cube()
        changed = True
        counter = 0
        sides = self.sides
        target = "RGOB"
        logging.debug(f"solve_yellow_edges sides: {sides}")
        # print("solve_yellow_edges",self.count_yellow_edges())
        while (yellow_edges := self.count_yellow_edges()) < 4:
            # print("yellow_edges",yellow_edges)
            counter += 1
            if counter > 100:
                logging.warning("solve_yellow_edges too many loops")
                break
            edge_colors = self.get_yellow_edges()
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
                self.orient_cube()
                for a, b in (("R", "G"), ("O", "B")):
                    while self.cube["F"][1][1][0] != a:
                        self.run_command_string("X")
                    while self.cube["F"][0][1][0] != a:
                        self.run_command_string("U")

                    if self.cube["R"][0][1][0] == b:
                        logging.debug(f"{b} is in the right spot")
                        # a and b are in position
                        pass
                    elif self.cube["L"][0][1][0] == b:
                        logging.debug(f"{a} and {b} are swapped")
                        # a and b are swapped
                        self.run_command_string("R,U,R',U,R,U,U,R',U")
                        # line up red edge
                        while self.cube["F"][0][1][0] != a:
                            self.run_command_string("U")
                    else:
                        logging.debug(f"{b} is on the far side of the world")
                        # b is on the opposite side:
                        # rotate
                        self.run_command_string("U'")
                        # swap
                        self.run_command_string("R,U,R',U,R,U,U,R',U")
                self.orient_cube()
        return self.check_yellow_edges()

    def check_yellow_edges(self):
        logging.debug(f"cube.check_yellow_edges")
        self.orient_cube()
        for side in self.sides:
            if self.cube[side][0][1][0] != self.cube[side][1][1][0]:
                return False
        return True

    def count_yellow_edges(self):
        logging.debug("cube.count_yellow_edges()")
        count = 0
        edge_pieces = self.find_edge_pieces("Y")
        logging.debug(f"edge_pieces: {edge_pieces}")
        self.orient_cube()
        for i in range(4):
            # self.print()
            logging.debug(f"{self.cube['F'][0][1]},{self.cube['F'][1][1]}")
            if self.cube["F"][0][1][0] == self.cube["F"][1][1][0]:
                count += 1
            self.run_command_string("X")
        return count

    def get_yellow_edges(self):
        logging.debug("cube.get_yellow_edges")
        edge_colors = ""
        for side in self.sides:
            edge_colors += self.cube[side][0][1][0]
        return edge_colors

    def solve_yellow_corners(self):
        logging.debug("cube.solve_yellow_corners()")
        counter = 0
        while True:
            counter += 1
            if counter > 100:
                logging.warning("solve_yellow_corners too many loops")
                break
            corners = self.find_corner_pieces("Y")
            logging.debug(corners)
            matched_corners = []
            for face, position in corners:
                corner_data = self.id_position(face, position)
                face_colors = []
                for mate in corner_data["mates"]:
                    face_colors.append(self.cube[mate[0]][1][1][0])
                if sorted(corner_data["mate_color"]) == sorted(face_colors):
                    matched_corners.append((face, position))
                logging.debug(matched_corners)
            if len(matched_corners) == 0:
                self.run_command_string("U,R,U',L',U,R',U',L")
            if len(matched_corners) == 1:
                corner_data = self.id_position(
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
                # FIXME bug1.cube gets here, it seems to have 2 matching corners, which shouldn't be possible
                # print("How did we get here?")
                logging.debug("cube.solve_yellow_corners: We shouldn't get here!")
                pass
        return False

    def orient_yellow_corners(self):
        logging.debug(f"orient_yellow_corners()")
        self.orient_cube()
        top_corners = [("U", (0, 0)), ("U", (0, 2)), ("U", (2, 0)), ("U", (2, 2))]
        counter = 0
        while self.up_yellow_corner_count() < 4:
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
        return self.check_yellow_corners()

    def check_yellow_corners(self):
        logging.debug("cube.check_yellow_corners()")
        self.orient_cube()
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
        corners = self.find_corner_pieces("Y")
        # Sort corners based on the order string
        sorted_corners = sorted(corners, key=lambda x: self.order.index(x[0]))
        logging.debug(sorted_corners)
        for face, position in sorted_corners:
            corner_data = self.id_position(face, position)
            if sorted(corner_data["mate_color"]) != sorted(
                corner_data["mate_face_color"]
            ):
                return False
        return True

    def up_yellow_corner_count(self):
        logging.debug("cube.up_yellow_corner_count()")
        top_corners = [("U", (0, 0)), ("U", (0, 2)), ("U", (2, 0)), ("U", (2, 2))]
        count = 0
        for corner in top_corners:
            if self.cube[corner[0]][corner[1][0]][corner[1][1]][0] == "Y":
                count += 1
        logging.debug(f"up_yellow_corner_count = {count}")
        return count

    def solve(self):
        logging.debug("cube.solve")
        solved = False
        failed_step = None
        if self.solve_white_cross():
            if self.solve_white_corners():
                if self.solve_second_layer():
                    if self.solve_yellow_cross():
                        if self.solve_yellow_edges():
                            if self.solve_yellow_corners():
                                if self.orient_yellow_corners():
                                    solved = True
                                else:
                                    failed_step = "orient_yellow_corners"
                            else:
                                failed_step = "solve_yellow_corners"
                        else:
                            failed_step = "solve_yellow_edges"
                    else:
                        failed_step = "solve_yellow_cross"
                else:
                    failed_step = "solve_second_layer"
            else:
                failed_step = "solve_white_corners"
        else:
            failed_step = "solve_white_cross"
        return solved, failed_step

    def clock(self):
        logging.debug("cube.clock")
        solved = False
        failed_step = None
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
                failed_step = step_name
                break
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000  # convert to milliseconds
            print(f"{step_name} took {time_taken:.2f} ms")
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000
        end_time = time.time()
        time_taken = (end_time - all_start_time) * 1000
        print(f"Total took {time_taken:.2f} ms")

        if failed_step is None:
            solved = True

        return time_taken
