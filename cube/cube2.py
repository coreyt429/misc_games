"""
Rubik's Cube Solver
-------------------

This module provides functionality to represent, manipulate, and solve a Rubik's cube.
It includes the `cube` class, which offers methods for initializing, solving, scrambling,
displaying, saving, and loading a Rubik's cube.

Imports:
    - json: For saving and loading the cube's state.
    - logging: For logging debug and information messages.
    - random: For scrambling the cube.
    - time: For measuring solve times.

Classes:
    - cube: A class to represent and manipulate a Rubik's cube.

Class `Cube`:
    Attributes:
        COLORS (dict): ANSI color codes for different faces of the cube.
        RESET (str): ANSI reset code to reset colors.
        BLOCK (str): A string representing a block used in cube visualization.
        cube (dict): Data representation of the Rubik's cube.

    Methods:
        __init__(filename=None): Initialize a cube object.
        get_piece(face, position): Retrieve a specific piece of the cube.
        ensure_list(myvar): Ensure a variable is a list.
        get_square(face, position): Retrieve a specific square of the cube.
        get_square_label(face, position): Get a label for a specific square.
        get_labels(face, indices): Get labels for multiple squares.
        print(label=None): Display the cube.
        new_cube(): Initialize a new cube with default colors and numbers.
        set_debug(debug): Set the debug mode.
        save(filename): Save the cube to a JSON file.
        load(filename): Load the cube from a JSON file.
        scramble(moves=40): Scramble the cube.
        orient_cube(front='R', down='W'): Orient the cube to specific front and down faces.
        orient_face(color, face): Orient a specific center color to a specific face.
        find_center(**kwargs): Find the face a center is on, or the color of the center on a face.
        whole_cube(faces, clockwise=True): Rotate the entire cube.
        rotate_cube(clockwise=True): Rotate the cube horizontally.
        tilt_cube(clockwise=True): Rotate the cube vertically.
        make_move(move): Execute a move on the cube.
        rotate_face(face, clockwise=True): Rotate a specific face.
        rotate_axis(face, colors, positions, clockwise): Rotate pieces on an axis.
        rotate_y_axis(plane, clockwise=True): Rotate on the Y axis.
        rotate_x_axis(plane, clockwise=True): Rotate on the X axis.
        rotate_z_axis(plane, clockwise=True): Rotate on the Z axis.
        rotate(face, clockwise=True): Rotate a specific face relative to F.
        run_command_string(command): Run a string of move commands.
        get_pieces(colors, piece_types=['corners', 'edges'], inclusive=True, match='color'):
            Find pieces that match criteria.
        face_of_color(color): Get the face that has this color center.
        solve_white_cross(): Solve the white cross.
        check_white_cross(): Check the white cross.
        place_white_edge(edge): Place and align a white edge.
        solve_white_corners(): Solve the white corners.
        check_white_corner(piece): Check the position of a white corner.
        check_white_corners(): Check all white corners.
        place_white_corner(piece): Place and orient a white corner.
        solve_second_layer(): Solve the middle layer.
        check_second_layer(): Check the second layer.
        solve_yellow_cross(): Place yellow edges.
        check_yellow_cross(): Check the yellow edges.
        solve_yellow_edges(): Orient the yellow edges.
        check_yellow_edges(): Check the yellow edges.
        solve_yellow_corners(): Place the yellow corners.
        orient_yellow_corners(): Orient yellow corners so yellow is up.
        check_yellow_corners(): Check the yellow corners.
        solve(): Solve the cube.
        clock(): Solve the cube and time each step.
"""

import sys
import json
import logging
import random
import time


class Cube:
    """
    A class to represent and manipulate a Rubik's cube.

    This class provides methods for initializing, solving, scrambling,
    and displaying a Rubik's cube.
    It also supports saving to and loading from a file.

    Attributes:
        COLORS (dict): ANSI color codes for different faces of the cube.
        RESET (str): ANSI reset code to reset colors.
        BLOCK (str): A string representing a block used in cube visualization.
        cube (dict): Data representation of the Rubik's cube.

    Methods:
        __init__(filename=None): Initialize a cube object.
        get_piece(face, position): Retrieve a specific piece of the cube.
        ensure_list(myvar): Ensure a variable is a list.
        get_square(face, position): Retrieve a specific square of the cube.
        get_square_label(face, position): Get a label for a specific square.
        get_labels(face, indices): Get labels for multiple squares.
        print(label=None): Display the cube.
        new_cube(): Initialize a new cube with default colors and numbers.
        set_debug(debug): Set the debug mode.
        save(filename): Save the cube to a JSON file.
        load(filename): Load the cube from a JSON file.
        scramble(moves=40): Scramble the cube.
        orient_cube(front='R', down='W'): Orient the cube to specific front and down faces.
        orient_face(color, face): Orient a specific center color to a specific face.
        find_center(**kwargs): Find the face a center is on, or the color of the center on a face.
        whole_cube(faces, clockwise=True): Rotate the entire cube.
        rotate_cube(clockwise=True): Rotate the cube horizontally.
        tilt_cube(clockwise=True): Rotate the cube vertically.
        make_move(move): Execute a move on the cube.
        rotate_face(face, clockwise=True): Rotate a specific face.
        rotate_axis(face, colors, positions, clockwise): Rotate pieces on an axis.
        rotate_y_axis(plane, clockwise=True): Rotate on the Y axis.
        rotate_x_axis(plane, clockwise=True): Rotate on the X axis.
        rotate_z_axis(plane, clockwise=True): Rotate on the Z axis.
        rotate(face, clockwise=True): Rotate a specific face relative to F.
        run_command_string(command): Run a string of move commands.
        get_pieces(colors, piece_types=['corners', 'edges'], inclusive=True, match='color'):
            Find pieces that match criteria.
        face_of_color(color): Get the face that has this color center.
        solve_white_cross(): Solve the white cross.
        check_white_cross(): Check the white cross.
        place_white_edge(edge): Place and align a white edge.
        solve_white_corners(): Solve the white corners.
        check_white_corner(piece): Check the position of a white corner.
        check_white_corners(): Check all white corners.
        place_white_corner(piece): Place and orient a white corner.
        solve_second_layer(): Solve the middle layer.
        check_second_layer(): Check the second layer.
        solve_yellow_cross(): Place yellow edges.
        check_yellow_cross(): Check the yellow edges.
        solve_yellow_edges(): Orient the yellow edges.
        check_yellow_edges(): Check the yellow edges.
        solve_yellow_corners(): Place the yellow corners.
        orient_yellow_corners(): Orient yellow corners so yellow is up.
        check_yellow_corners(): Check the yellow corners.
        solve(): Solve the cube.
        clock(): Solve the cube and time each step.
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
        """
        Initialize a cube2 object

        Args:
            filename (str): filename to load a cube from

        Returns:
            cube2 object
        """
        self.cfg = {
            "debug": False,
            "scramble": 40,
            "type": 2,
            "original_logging_level": logging.getLogger().getEffectiveLevel(),
        }
        self.faces = "FRBLUD"
        self.colors = "RGOBYW"
        self.side_colors = "RGOB"
        self.sides = "FRBL"
        self.order = "DFRBLU"
        self.new_cube()  # initialize cube even if we are loading a file
        if filename is not None:
            self.load(filename)

    def get_piece(self, face, position):
        """
        function to retrieve a specific piece that holds the square specified

        Args:
            face (str): The face of the cube to select U, D, F, R, B, L
            position (int):  numeric position on the face 1, 2, 3, 4, 5, 6, 7, 8, 9

        Returns:
            piece data structure (list of square data structures)
        """
        logging.debug("cube2.get_piece(%s,%s)", face, position)
        # corners
        if position in [1, 3, 7, 9]:
            for corner in self.cube["corners"]:
                for square in corner:
                    if (
                        square["position"] == position
                        and square["center"] == self.cube["faces"][face]
                    ):
                        return corner
        # edges
        elif position in [2, 4, 6, 8]:
            for edge in self.cube["edges"]:
                for square in edge:
                    if (
                        square["position"] == position
                        and square["center"] == self.cube["faces"][face]
                    ):
                        return edge
        # centers
        else:
            for center in self.cube["centers"]:
                for square in center:
                    if (
                        square["position"] == position
                        and square["center"] == self.cube["faces"][face]
                    ):
                        return center
        return [{"color": "W", "position": 0}]

    def ensure_list(self, myvar):
        """
        function make a non-list a list

        Args:
            myvar (any): variable to check

        Returns:
            list containing myvar
        """
        if not isinstance(myvar, list):
            myvar = [myvar]
        return myvar

    def get_square(self, face, position):
        """
        select a square object based on face and position

        Args:
            face (str): The face of the cube to select U, D, F, R, B, L
            position (int):  numeric position on the face 1, 2, 3, 4, 5, 6, 7, 8, 9

        Returns:
            square data structure
        """
        logging.debug("cube2.get_square(%s,%s)", face, position)
        piece = self.ensure_list(self.get_piece(face, position))

        for square in piece:
            if square["center"] == self.cube["faces"][face]:
                return square
        return None

    def get_square_label(self, face, position):
        """
        get a label for a specific square:

        Args:
            face (str): The face of the cube to select U, D, F, R, B, L
            position (int):  numeric position on the face 1, 2, 3, 4, 5, 6, 7, 8, 9

        Returns:
            square data label (str)
        """
        logging.debug("cube2.get_square_label(%s,%s)", face, position)
        square = self.get_square(face, position)
        return square["color"] + str(square["start"])

    def get_labels(self, face, indices):
        """
        Args:
            face (str): The face of the cube to select U, D, F, R, B, L
            indices (list(int)):  list of numeric positions on the face 1, 2, 3, 4, 5, 6, 7, 8, 9

        Returns:
            list of square data structure
        """
        return [self.get_square_label(face, i) for i in indices]

    def print(self, label=None):
        """
        Display the cube

        Args:
            label (str): Label for the cube

        Returns:
            none

        Obsolete at this point, you can now just print(cube_object) instead
        """
        # print(json.dumps(self.cube,indent=2))
        logging.debug("cube%s.print()", self.cfg["type"])
        # Prints the cube in a formatted manner with colors.
        blank = [["K0" for _ in range(3)] for _ in range(3)]
        print()
        if label is not None:
            print(f"{label}:")

        # Define blank row
        blank_row = blank[0]

        # Build rows
        rows = []

        # Add the 'U' face rows
        for i in range(3):
            rows.append(
                blank_row
                + self.get_labels("U", range(1 + i * 3, 4 + i * 3))
                + blank_row
                + blank_row
            )

        # Add the middle faces rows
        for i in range(3):
            rows.append(
                self.get_labels("L", range(1 + i * 3, 4 + i * 3))
                + self.get_labels("F", range(1 + i * 3, 4 + i * 3))
                + self.get_labels("R", range(1 + i * 3, 4 + i * 3))
                + self.get_labels("B", range(1 + i * 3, 4 + i * 3))
            )

        # Add the 'D' face rows
        for i in range(3):
            rows.append(
                blank_row
                + self.get_labels("D", range(1 + i * 3, 4 + i * 3))
                + blank_row
                + blank_row
            )

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
        Args:
            None

        Return:
            None (self.cube is modified)

        """
        self.cube = {
            "faces": {"U": "Y", "F": "R", "R": "G", "B": "O", "D": "W", "L": "B"},
            "centers": [],
            "edges": [],
            "corners": [],
        }
        # build centers
        for color in self.colors:
            self.cube["centers"].append(
                [{"color": color, "center": color, "position": 5, "start": 5}]
            )

        # build edges
        edge_map = [
            (("R", 2, 2), ("Y", 8, 8)),
            (("R", 4, 4), ("B", 6, 6)),
            (("R", 6, 6), ("G", 4, 4)),
            (("R", 8, 8), ("W", 2, 2)),
            (("O", 2, 2), ("Y", 2, 2)),
            (("O", 4, 4), ("G", 6, 6)),
            (("O", 6, 6), ("B", 4, 4)),
            (("O", 8, 8), ("W", 8, 8)),
            (("G", 2, 2), ("Y", 6, 6)),
            (("G", 8, 8), ("W", 6, 6)),
            (("B", 2, 2), ("Y", 4, 4)),
            (("B", 8, 8), ("W", 4, 4)),
        ]

        for edge_a, edge_b in edge_map:
            self.cube["edges"].append(
                [
                    {
                        "color": edge_a[0],
                        "center": edge_a[0],
                        "position": edge_a[1],
                        "start": edge_a[2],
                    },
                    {
                        "color": edge_b[0],
                        "center": edge_b[0],
                        "position": edge_b[1],
                        "start": edge_b[2],
                    },
                ]
            )

        # build corners
        corner_map = [
            (("R", 9, 9), ("G", 7, 7), ("W", 3, 3)),
            (("R", 7, 7), ("W", 1, 1), ("B", 9, 9)),
            (("R", 3, 3), ("G", 1, 1), ("Y", 9, 9)),
            (("R", 1, 1), ("Y", 7, 7), ("B", 3, 3)),
            (("O", 9, 9), ("B", 7, 7), ("W", 7, 7)),
            (("O", 7, 7), ("W", 9, 9), ("G", 9, 9)),
            (("O", 3, 3), ("B", 1, 1), ("Y", 1, 1)),
            (("O", 1, 1), ("G", 3, 3), ("Y", 3, 3)),
        ]

        for edge_a, edge_b, edge_c in corner_map:
            self.cube["corners"].append(
                [
                    {
                        "color": edge_a[0],
                        "center": edge_a[0],
                        "position": edge_a[1],
                        "start": edge_a[2],
                    },
                    {
                        "color": edge_b[0],
                        "center": edge_b[0],
                        "position": edge_b[1],
                        "start": edge_b[2],
                    },
                    {
                        "color": edge_c[0],
                        "center": edge_c[0],
                        "position": edge_c[1],
                        "start": edge_c[2],
                    },
                ]
            )

    def get_debug(self):
        """
        Gets the debug mode.

        Args:
            None

        Returns:
            bool: current debug setting
        """
        return self.cfg["debug"]

    def set_debug(self, debug):
        """
        Sets the debug mode.

        Args:
            debug (bool): new debug setting

        Returns:
            None
        """
        logging.debug("cube.set_debug(%s)", debug)

        self.cfg["debug"] = debug
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(self.cfg["original_logging_level"])

    def save(self, filename):
        """
        Save the cube representation to a JSON file.

        Args:
            filename (str): The name of the file to save the JSON data.

        Returns:
            None
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
            with open(filename, "w", encoding="utf-8") as file:
                file.write(save_json)

            logging.info("Cube successfully saved to %s", filename)
        except (FileNotFoundError, json.JSONDecodeError) as e_str:
            logging.warning("An error occurred: %s", e_str)

    def load(self, filename):
        """
        Load the cube representation from a JSON file.

        Args:
            filename (str): The name of the file to load the JSON data.

        Returns:
            None
        """
        logging.info("load(%s)", filename)

        try:
            # Read the JSON string from a file
            with open(filename, "r", encoding="utf-8") as file:
                data_json = file.read()
            data = json.loads(data_json)
            # set cube orientation
            for face in self.faces:
                self.cube["faces"][face] = data[f"{face}5"][0]

            for position, value in data.items():
                current_color, current_position = list(position)
                original_color, original_position = list(value)
                if int(current_position) != 5:
                    piece = next(
                        (
                            p
                            for p in self.get_pieces(original_color)
                            for square in p
                            if square["color"] == original_color
                            and square["start"] == int(original_position)
                        ),
                        None,
                    )
                    # if piece:
                    for square in piece:
                        if square["color"] == original_color and square["start"] == int(
                            original_position
                        ):
                            square["center"] = self.cube["faces"][current_color]
                            square["position"] = int(current_position)
            logging.info("Cube successfully loaded from %s", filename)
        except (FileNotFoundError, json.JSONDecodeError) as e_str:
            logging.warning("An error occurred: %s", e_str)

    def scramble(self, moves=40):
        """
        Scramble the cube

        Args:
            moves (int): Number of moves to make during scrambling (default: 40)
        """
        logging.debug("cube.scramble(%s)", moves)
        for _ in range(moves):
            face = random.choice(self.faces)
            clockwise = random.choice([True, False])
            self.rotate(face, clockwise)

    def orient_cube(self, front="R", down="W"):
        """
        Orient the cube to s specific front and down face

        Args:
            front (str): new front face (default: 'R')
            down (str): new down face (default: 'W')

        Returns:
            None
        """
        logging.debug("cube2.orient_cube('%s','%s')", front, down)
        self.orient_face(down, "D")
        sentinel = 0
        while self.get_square("F", 5)["color"] != front:
            sentinel += 1
            if sentinel > 4:
                logging.warning(
                    "cube2.orient_cube(%s%s) no match in all four sides", front, down
                )
                break
            self.rotate_cube()

    def orient_face(self, color, face):
        """
        Orient a specific center color to a specific face

        Args:
            color (str): center color R, G, B, O, Y, W
            face (str): face to move center to F, R, B, L, U, D

        Returns:
            None

        """
        logging.debug("cube2.orient_face(%s,%s)", color, face)
        if self.cube["faces"][face] != color:
            for current_face in self.cube["faces"]:
                if self.cube["faces"][current_face] == color:
                    break
            if face in "UDFB":
                if current_face not in "UDFB":
                    self.rotate_cube()
                while self.cube["faces"][face] != color:
                    self.tilt_cube()
            else:
                if current_face not in "LRFB":
                    self.tilt_cube()
                while self.cube["faces"][face] != color:
                    self.rotate_cube()
        else:
            pass  # do nothing, already oriented

    def find_center(self, **kwargs):
        """
        Finds the face a center is on, or the color the center on a face.

        kwargs:
            color (str) = color to find R, G, O, B, Y, W
            face (str) = face to identify F, R, B, L, U, D

        Returns:
            face (str) or color (str)
        """
        logging.debug("cubes2.find_center(%s)", kwargs)
        if "color" in kwargs:  # color passed, return face
            for face in self.cube["faces"]:
                if self.cube["faces"][face] == kwargs["color"]:
                    return face
        elif "face" in kwargs:
            return self.cube["faces"][kwargs["face"]]
        return None

    def whole_cube(self, faces, clockwise=True):
        """
        Rotate entire cube

        Args:
            faces (str): faces to rotate ex: 'FRBL' or 'FUBD'
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)

        Returns:
            None
        """
        logging.debug("cube2.whole_cube(%s.%s)", faces, clockwise)
        current = ""
        for face in faces:  # FRBL
            current += self.cube["faces"][face]
        # RGOB
        if not clockwise:
            new = current[3:] + current[:3]
        else:
            new = current[1:] + current[:1]
        if "U" in faces:
            self.rotate_face("B", clockwise)
            self.rotate_face("B", clockwise)
        for idx, position in enumerate(faces):
            self.cube["faces"][position] = new[idx]
        if "U" not in faces:
            self.rotate_face("U", clockwise)
            self.rotate_face("D", not clockwise)
        else:
            self.rotate_face("L", clockwise)
            self.rotate_face("R", not clockwise)
            self.rotate_face("B", clockwise)
            self.rotate_face("B", clockwise)

    def rotate_cube(self, clockwise=True):
        """
        Rotate the cube horizontally

        Args:
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)

        Returns:
            None
        """
        logging.debug("cube2.rotate_cube(%s)", clockwise)
        self.whole_cube(self.sides, clockwise)

    def tilt_cube(self, clockwise=True):
        """
        Rotate the cube vertically

        Args:
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)

        Returns:
            None
        """
        logging.debug("cube2.tilt_cube(%s)", clockwise)
        self.whole_cube("FUBD", clockwise)

    def make_move(self, move):
        """
        Execute move on the cube.

        Args:
            move (str): single move to execute

        Returns:
            None
        """
        logging.debug("cube2.make_move(%s)", move)
        if move.upper() in "U'F'D'L'R'B'C'M'":
            if move[-1] == "'":
                self.rotate(move[0].upper(), clockwise=False)
            else:
                self.rotate(move[0].upper(), clockwise=True)
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
        else:
            logging.warning("cube2.make_move(%s): unkown move", move)

    def rotate_face(self, face, clockwise=True):
        """
        Rotate a face

        Rotate a particular face

        Args:
            face (str): face to rotate
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)
        """
        logging.debug("rotate_face(self,%s,%s)", face, clockwise)
        position_map = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
        if not clockwise:
            position_map = [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
        for piece in self.cube["edges"] + self.cube["corners"]:
            for square in piece:
                if square["center"] == self.cube["faces"][face]:
                    square["position"] = position_map[square["position"]]

    def rotate_axis(self, face, colors, positions, clockwise):
        """
        Rotate pieces on an axis

        Args:
            face (str) : face we are rotating
            colors (str): starting colors of pieces to rotate
            positions (list(list(int))): list of sides, which are lists of position
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)
        """
        if face in self.faces:
            self.rotate_face(face, clockwise)

        for piece in self.get_pieces(
            self.cube["faces"][face], ["edges", "corners"], True, "center"
        ):
            for square in piece:
                if square["center"] in colors:
                    idx = (colors.find(square["center"]) + 1) % len(colors)
                    next_color = colors[idx]

                    if positions in [[1, 4, 7], [3, 6, 9]] and self.cube["faces"][
                        "B"
                    ] in [square["center"], next_color]:
                        self.update_square_position(square, positions, next_color)
                    elif square["position"] in positions:
                        square["center"] = next_color

    def update_square_position(self, square, positions, next_color):
        """
        Update the position of a square based on the given parameters.
        """
        position_map = None
        if positions == [1, 4, 7]:
            alt_positions = [9, 6, 3]
        else:
            alt_positions = [7, 4, 1]

        if (
            square["center"] == self.cube["faces"]["B"]
            and square["position"] in alt_positions
        ):
            position_map = dict(zip(alt_positions, positions))
        elif next_color == self.cube["faces"]["B"] and square["position"] in positions:
            position_map = dict(zip(positions, alt_positions))

        if position_map is not None:
            square["center"] = next_color
            square["position"] = position_map[square["position"]]

    def rotate_y_axis(self, plane, clockwise=True):
        """
        Rotate on Y axis

        Args:
            plane (int): Y axis plane to rotate (0,1,2)
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)
        """
        logging.debug("cube2.rotate_y_axis(%s, %s)", plane, clockwise)
        colors = ""
        updown = ""
        positions = []
        for face in self.sides:
            colors += self.cube["faces"][face]
        if clockwise:
            colors = colors[::-1]
        colors = colors + colors
        if plane == 2:
            updown = "D"
            colors = colors[::-1]
            positions = [7, 8, 9]
        elif plane == 0:
            positions = [1, 2, 3]
            updown = "U"
        else:
            logging.debug(
                "cube2.rotate_y_axis(%s, %s):  Invalid plane %s",
                plane,
                clockwise,
                plane,
            )
        self.rotate_axis(updown, colors, positions, clockwise)

    def rotate_x_axis(self, plane, clockwise=True):
        """
        Rotate on X axis

        Args:
            plane (int): X axis plane to rotate (0,1,2)
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)
        """
        logging.debug("cube2.rotate_x_axis(%s, %s)", plane, clockwise)
        colors = ""
        sides = "FUBD"
        leftright = ""
        positions = []
        for side in sides:
            colors += self.cube["faces"][side]
        if clockwise:
            colors = colors[::-1]
        colors = colors + colors
        if plane == 2:
            leftright = "R"
            colors = colors[::-1]
            positions = [3, 6, 9]
        elif plane == 0:
            positions = [1, 4, 7]
            leftright = "L"
        else:
            logging.debug(
                "cube2.rotate_x_axis(%s, %s):  Invalid plane %s",
                plane,
                clockwise,
                plane,
            )
        self.rotate_axis(leftright, colors, positions, clockwise)

    def rotate_z_axis(self, plane, clockwise=True):
        """
        Rotate on Z axis

        Args:
            plane (int): Z axis plane to rotate (0,1,2)
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)
        """
        logging.debug("cube2.rotate_z_axis(%s, %s)", plane, clockwise)
        colors = ""
        sides = "URDL"
        face = ""
        for side in sides:
            colors += self.cube["faces"][side]
        if not clockwise:
            colors = colors[::-1]
        colors = colors + colors
        if plane == 2:
            face = "B"
            colors = colors[::-1]
        elif plane == 0:
            face = "F"
        else:
            logging.debug(
                "cube2.rotate_z_axis(%s, %s):  Invalid plane %s",
                plane,
                clockwise,
                plane,
            )

        position_map = {
            "U": {1: 7, 2: 4, 3: 1, 7: 1, 8: 4, 9: 7},
            "R": {3: 1, 6: 2, 9: 3, 1: 3, 4: 2, 7: 1},
            "D": {7: 9, 8: 6, 9: 3, 1: 3, 2: 6, 3: 9},
            "L": {1: 7, 4: 8, 7: 9, 3: 9, 6: 8, 9: 7},
        }
        if not clockwise:
            position_map = {
                "U": {1: 3, 2: 6, 3: 9, 7: 9, 8: 6, 9: 3},
                "R": {3: 9, 6: 8, 9: 7, 1: 7, 4: 8, 7: 9},
                "D": {7: 1, 8: 4, 9: 7, 1: 7, 2: 4, 3: 1},
                "L": {1: 3, 4: 2, 7: 1, 3: 1, 6: 2, 9: 3},
            }
        # z axis has its own complexity, I'm not going to impose that on rotate_axis
        # self.rotate_axis(leftright,colors,positions,clockwise)

        if face in self.faces:
            self.rotate_face(face, clockwise)

        for piece in self.get_pieces(
            self.cube["faces"][face], ["edges", "corners"], True, "center"
        ):
            for square in piece:
                center = self.find_center(color=square["center"])
                if center in position_map:
                    my_map = position_map[center]
                    if square["position"] in my_map:
                        new_position = my_map[square["position"]]
                        # advance color of row squares, calculate but don't assign yet
                        idx = colors.find(square["center"])
                        idx += 1
                        if idx > len(colors):
                            idx -= len(colors)
                        new_center = colors[idx]
                        square["center"] = new_center
                        square["position"] = new_position

    def rotate(self, face, clockwise=True):
        """
        Rotate a specific face

        Args:
            face (str): face to rotate relative to F (F, B, L, R, U, D, C, M)
            clockwise (bool): True for clockwise, False for counter-clockwise (default: True)
        """
        logging.debug("cube2.rotate(%s, %s)", face, clockwise)
        if face == "C":
            self.rotate_x_axis(0, clockwise)
            self.rotate_x_axis(2, not clockwise)
            self.tilt_cube(not clockwise)
        elif face in "LCR":
            self.rotate_x_axis("LCR".find(face), clockwise)
        elif face == "M":
            self.rotate_y_axis(0, not clockwise)
            self.rotate_y_axis(2, clockwise)
            self.rotate_cube(clockwise)
        elif face in "FB":
            self.rotate_z_axis("F B".find(face), clockwise)
        else:
            self.rotate_y_axis("UMD".find(face), clockwise)

    ##########################
    # Command String functions
    ##########################

    def run_command_string(self, command):
        """
        Run a string of move commands

        Args:
            command (str): comma seperated list of moves
        """
        logging.debug("cube2.run_command_string(cube,%s)", command)
        for move in command.rstrip(",").lstrip(",").split(","):
            self.make_move(move)

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

    def get_pieces(self, colors, piece_types=None, inclusive=True, match="color"):
        """
        Find pieces that match criteria
            colors (str): Colors to include
            piece_types (list(str)): list of piece types to include (defalut: ['corners','edges'])
            inclusive (bool): Include pieces that also have other colors (default: True)
            match (str): field to match by 'color' or 'center' (default: 'color')

        Returns:
            list of pieces
        """
        if piece_types is None:
            piece_types = ["corners", "edges"]
        piece_types = self.ensure_list(piece_types)
        logging.debug("get_pieces(%s,%s,%s},%s)", colors, piece_types, inclusive, match)
        pieces = []
        for piece_type in piece_types:
            for piece in self.cube[piece_type]:
                found = False
                for square in piece:
                    if square[match] in colors:
                        found = True
                if found:
                    pieces.append(piece)
        if (
            not inclusive
        ):  # if not inclusive, we don't want pieces that have another color
            real_pieces = []
            for piece in pieces:
                keep = True
                for square in piece:
                    if square[match] not in colors:
                        keep = False
                if keep:
                    real_pieces.append(piece)
            return real_pieces
        return pieces

    def face_of_color(self, color):
        """
        Get the face that has this color center.

        Args:
            color (str): One of R, G, O, B, Y, W
        """
        for face in self.cube["faces"]:
            if self.cube["faces"][face] in color:
                return face
        return None

    ##################
    # Solver Functions
    ##################

    def solve_white_cross(self):
        """
        Solve the white cross (bottom edges).

        Return
            solved (bool)
        """
        logging.debug("cube2.solve_white_cross()")
        ######################################
        # Solve the bottom edges (white cross)
        ######################################
        self.orient_cube()
        counter = 0
        while not self.check_white_cross():
            counter += 1
            if counter > 1:
                logging.warning("cube2.solve_white_cross() too many loops")
                break
            edge_pieces = self.get_pieces("W", ["edges"])
            # print(edge_pieces)
            # sorted_edge_pieces = sorted(edge_pieces, key=lambda x: self.order.index(x[0]))
            # our order shouldn't change with this data structure,
            # so we are good to just iterate the edges
            for edge in edge_pieces:
                if not self.place_white_edge(edge):
                    break
        return self.check_white_cross()

    def check_white_cross(self):
        """
        Check the white cross.

        Return
            solved (bool)

        """
        logging.debug("cube2.check_white_cross()")
        self.orient_cube()
        pieces = self.get_pieces("W", ["edges"])
        for piece in pieces:
            for face in piece:
                if face["color"] != face["center"]:
                    return False
        return True

    def place_white_edge(self, edge):
        """
        Place and align a white edge:

        Args:
            edge (list(squares)): edge piece to place

        Returns:
            solve (bool)
        """
        logging.debug("place_white_edge(%s)", edge)
        white_square = edge[1]
        color_square = edge[0]
        if edge[0]["color"] == "W":
            white_square = edge[0]
            color_square = edge[1]

        # sentinel = 0
        while (
            white_square["color"] != white_square["center"]
            or color_square["color"] != color_square["center"]
        ):
            # sentinel += 1
            # if sentinel > 4:
            #     logging.warning("cube2.place_white_edge: breaking loop")
            #     break
            if white_square["center"] not in "WY":
                if white_square["position"] == 8:
                    self.run_command_string(self.face_of_color(white_square["center"]))
                if white_square["position"] == 2:
                    save1 = self.face_of_color(white_square["center"])
                    self.run_command_string(f"{save1}")
                    save2 = self.face_of_color(color_square["center"])
                    self.run_command_string(f"{save2},U,{save2}',{save1}'")
                elif white_square["position"] in [4]:
                    save1 = self.face_of_color(color_square["center"])
                    self.run_command_string(f"{save1}',U,{save1}")
                elif white_square["position"] in [6]:
                    save1 = self.face_of_color(color_square["center"])
                    self.run_command_string(f"{save1},U,{save1}'")
                # else:
                #     logging.debug("Position ?, how did we get here? %s}", white_square)
            if (
                white_square["center"] == "W"
                and color_square["color"] != color_square["center"]
            ):
                # facing down, but not in the right spot, send to top
                self.run_command_string(self.face_of_color(color_square["center"]))
                self.run_command_string(self.face_of_color(color_square["center"]))

            if white_square["center"] == "Y":
                # facing up
                while color_square["color"] != color_square["center"]:
                    self.run_command_string("U")
                self.run_command_string(self.face_of_color(color_square["center"]))
                self.run_command_string(self.face_of_color(color_square["center"]))
        if (
            white_square["color"] == white_square["center"]
            and color_square["color"] == color_square["center"]
        ):
            # already aligned
            return True
        return False

    def solve_white_corners(self):
        """
        Solve white (bottom) corners

        Returns:
            solved (bool)
        """
        logging.debug("solve_white_corners()")
        self.orient_cube()
        counter = 0
        # print('solve_white_corners')
        while not self.check_white_corners():
            counter += 1
            if counter > 20:
                logging.warning("solve_white_corners loop detected")
                break
            pieces = self.get_pieces("W", ["corners"])
            for piece in pieces:
                if not self.check_white_corner(piece):
                    self.place_white_corner(piece)
        return self.check_white_corners()

    def check_white_corner(self, piece):
        """
        Check position of white corner

        Return:
            correct (bool)
        """
        logging.debug("check_white_corner(%s)", piece)
        for square in piece:
            if square["color"] != square["center"]:
                return False
        return True

    def check_white_corners(self):
        """
        Check all white corners

        Return:
            correct (bool)
        """
        logging.debug("check_white_corners()")
        self.orient_cube()

        pieces = self.get_pieces("W", ["corners"])
        for piece in pieces:
            if not self.check_white_corner(piece):
                return False
        return True

    def place_white_corner(self, piece):
        """
        Place and orient a white corner

        Args:
            piece (list(squares)): piece to place

        Returns:
            correct (bool)
        """
        logging.debug("place_white_corner(%s)", piece)
        others = []
        white_square = None
        white_square, others = next(
            (square, [s for s in piece if s != square])
            for square in piece
            if square["color"] == "W"
        )
        sentinel = 0
        while not self.check_white_corner(piece):
            sentinel += 1
            if sentinel > 10:
                logging.debug("place_white_corner(%s): breaking loop", piece)
                break
            if white_square["center"] == "Y":
                for idx, other in enumerate(others):  # move to top right
                    idx2 = (idx + 1) % 2
                    self.orient_cube(others[idx2]["center"])
                    while others[idx2]["color"] != other["center"]:
                        self.run_command_string("U")
                    self.orient_cube(others[idx2]["center"])
                    if white_square["position"] == 9:
                        break
                self.run_command_string("F',U,F,R,U,U,R'")
            elif white_square["center"] == "W":
                # Safety check, this shouldn't happen because we are checking above
                # if self.check_white_corner(piece):
                #     return True

                for square in others:  # move to top right
                    self.orient_cube(square["center"])
                    if square["position"] == 9:
                        break
                self.run_command_string("R,U,R'")
            else:
                self.orient_cube(white_square["center"])
                command_strings = {
                    1: "U',F',U,F",
                    # 3:"U',F,U,F'",
                    3: "F,U,F'",
                    9: "L',U,L,",  # Just pop up, it will be in 1 next pass
                    7: "R,U',R'",  # Just pop up, it will be in 1 next pass
                }
                command_string = command_strings[white_square["position"]]
                for square in others:
                    if square["center"] in self.side_colors:
                        self.orient_cube(square["center"])
                        break
                self.run_command_string(command_string)
        return self.check_white_corner(piece)

    def solve_second_layer(self):
        """
        Solve the middle layer.

        Returns:
            solved (bool)
        """
        def orient_edge(square, square2):
            """
            sub function to orient the edge
            """
            if square["position"] == 6:
                self.orient_cube(square["center"])
            else:
                self.orient_cube(square2["center"])

        while not self.check_second_layer():
            pieces = self.get_pieces("RGOB", ["edges"], False)
            for piece in pieces:
                if "Y" in [square["center"] for square in piece]:
                    square = {}
                    for square in piece:
                        if square["center"] != "Y":
                            self.orient_cube(square["color"])
                            break
                    # self.print()
                    sentinel = 0
                    while square["color"] != square["center"]:
                        sentinel += 1
                        if sentinel > 4:
                            logging.warning("all 4 sides tried")
                            break
                        self.run_command_string("U")
                    colors = self.side_colors
                    idx = colors.find(square["color"])
                    idx_left = idx - 1
                    if idx_left < 0:
                        idx_left += len(colors)
                    left = colors[idx_left]
                    idx_right = idx + 1
                    if idx_right == len(colors):
                        idx_right = 0
                    right = colors[idx_right]
                    if left in [square2["color"] for square2 in piece]:
                        # self.print()
                        self.run_command_string("U',L',U,L,U,F,U',F'")
                    elif right in [square2["color"] for square2 in piece]:
                        # self.print()
                        self.run_command_string("U,R,U',R',U',F',U,F")
                else:
                    square, square2 = piece
                    if square["color"] != square["center"]:
                        if square["color"] != square2["center"]:
                            # piece doesn't go here
                            orient_edge(square, square2)
                            # self.print()
                            self.run_command_string("U,R,U',R',U',F',U,F")
                        else:
                            # flip it
                            orient_edge(square, square2)
                            # self.print()
                            self.run_command_string(
                                "U,R,U',R',U',F',U,F,U,U,U,R,U',R',U',F',U,F"
                            )
                    elif square2["color"] != square2["center"]:
                        # piece doesn't go here
                        orient_edge(square, square2)
                        self.run_command_string("U,R,U',R',U',F',U,F")
        return self.check_second_layer()

    def check_second_layer(self):
        """
        Check the second layer.

        Returns:
            correct (bool)
        """
        logging.debug("cube2.check_second_layer()")
        self.orient_cube()
        pieces = self.get_pieces("RGOB", ["edges"], False)
        retval = True
        for piece in pieces:
            for square in piece:
                if square["color"] != square["center"]:
                    retval = False
        return retval

    def solve_yellow_cross(self):
        """
        Place yellow edges (top).

        Return:
            solved (bool)
        """
        logging.debug("cube2.solve_yellow_cross()")
        pieces = self.get_pieces("Y", ["edges"])
        up_count = sum(
            1
            for piece in pieces
            for square in piece
            if square["color"] == "Y" and square["center"] == "Y"
        )
        sentinel = 0
        while not self.check_yellow_cross():
            sentinel += 1
            if sentinel > 10:
                logging.warning("cube2.solve_yellow_cross breaking loop")
                return False
            if up_count == 0:
                pass
            elif up_count == 2:
                square = self.get_square("U", 4)
                while square["color"] != "Y":
                    self.run_command_string("U")
                    square = self.get_square("U", 4)
                if self.get_square("U", 8)["color"] == "Y":
                    self.run_command_string("U")
                    square = self.get_square("U", 4)
            else:
                pass
            command_string = "F,R,U,R',U',F'"
            self.run_command_string(command_string)
            up_count = 0
            for piece in pieces:
                for square in piece:
                    if square["color"] == "Y" and square["center"] == "Y":
                        up_count += 1
        return self.check_yellow_cross()

    def check_yellow_cross(self):
        """
        Check the yellow edges.

        Returns:
            solved (bool)
        """
        pieces = self.get_pieces("Y", ["edges"])
        for piece in pieces:
            for square in piece:
                if square["color"] == "Y":
                    if square["center"] != "Y":
                        return False
        return True

    def solve_yellow_edges(self):
        """
        Orient the yellow edges

        Return:
            solved (bool)
        """
        logging.debug("cube2.solve_yellow_edges()")
        pieces = self.get_pieces("Y", ["edges"])
        for piece in pieces:
            for idx in [0, 1]:
                square = piece[idx]
                # other = piece[idx + 1 % 2]
                if square["color"] != "Y":
                    break
            self.orient_cube(square["color"])
            while square["color"] != square["center"]:
                self.run_command_string("U")
            while self.get_square("L", 2)["color"] != self.get_square("L", 2)["center"]:
                self.run_command_string("R,U,R',U,R,U,U,R',U")
                self.run_command_string("U'")
        return self.check_yellow_edges()

    def check_yellow_edges(self):
        """
        Check the yellow edges.

        Returns:
            correct (bool)
        """
        logging.debug("cube2.check_yellow_edges")
        pieces = self.get_pieces("Y", ["edges"])
        for piece in pieces:
            for square in piece:
                if square["color"] != square["center"]:
                    return False
        return True

    def solve_yellow_corners(self):
        """
        Place the yellow corners.

        Returns:
            solved (bool)
        """
        logging.debug("cube2.solve_yellow_corners")
        pieces = self.get_pieces("Y", ["corners"])
        correct_corners = []
        while len(correct_corners) < 4:
            correct_corners = []
            for piece in pieces:
                # match = False
                colors = []
                centers = []
                for square in piece:
                    colors.append(square["color"])
                    centers.append(square["center"])
                if sorted(colors) == sorted(centers):
                    correct_corners.append(piece)
            if len(correct_corners) != 4:
                if len(correct_corners) == 1:
                    piece = correct_corners[0]
                    for square in piece:
                        if square["center"] == "Y":
                            break
                    while square["position"] != 9:
                        self.run_command_string("X")
                elif len(correct_corners) == 0:
                    pass
                else:
                    print(self)
                    logging.warning(
                        "solve_yellow_corners: wtf? len(correct_corners) == %s",
                        len(correct_corners),
                    )

                    sys.exit(1)
                self.run_command_string("U,R,U',L',U,R',U',L")
            else:
                return True

        return False

    def orient_yellow_corners(self):
        """
        Orient yellow corners so yellow is up.

        Returns:
            solved (bool)
        """
        logging.debug("cube2.orient_yellow_corners")
        self.orient_cube()
        pieces = self.get_pieces("Y", ["corners"])
        for piece in pieces:
            for square in piece:
                if square["color"] == "Y":
                    if square["center"] != "Y":
                        while square["center"] != "R":
                            self.run_command_string("U")
                        if square["position"] == 3:
                            self.run_command_string("R',D',R,D")
                            self.run_command_string("R',D',R,D")
                            self.run_command_string("R',D',R,D")
                            self.run_command_string("R',D',R,D")
                        elif square["position"] == 1:
                            self.run_command_string("U'")
                            self.run_command_string("R',D',R,D")
                            self.run_command_string("R',D',R,D")
        square = self.get_square("F", 2)
        while square["color"] != square["center"]:
            self.run_command_string("U'")
        return self.check_yellow_corners()

    def check_yellow_corners(self):
        """
        Check the yellow corners

        Returns:
            correct (bool)
        """
        logging.debug("cube2.check_yellow_corners()")
        # are all teh yellow corners facing up?
        pieces = self.get_pieces("Y", ["corners"])
        # this first test seems redundant to teh second test
        for piece in pieces:
            for square in piece:
                if square["color"] == "Y":
                    if square["center"] != "Y":
                        return False
        for piece in pieces:
            for square in piece:
                if square["color"] != square["center"]:
                    return False
        return True

    def solve(self):
        """
        Solve The cube

        Returns:
            solved (bool)
            failed_step (str)

        """
        logging.debug("cube2.solve")
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
        Solve the cube and time each step.

        Returns:
            time_taken(int): total time taken
        """
        logging.debug("cube.clock")
        # solved = False
        # failed_step = None
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
                # failed_step = step_name
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
