"""
Unit tests for the Cube class
"""

import unittest
import logging
from cube import Cube

# Enable debug logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# from visualize import print_color_cube

# test states to validate cube status
test_states_face_cube = {
    "init": (
        "W0W1W2W3W4W5W6W7W8"
        + "Y0Y1Y2Y3Y4Y5Y6Y7Y8"
        + "G0G1G2G3G4G5G6G7G8"
        + "B0B1B2B3B4B5B6B7B8"
        + "R0R1R2R3R4R5R6R7R8"
        + "O0O1O2O3O4O5O6O7O8"
    ),
    "X": (
        "R0R1R2R3R4R5R6R7R8"
        + "O0O1O2O3O4O5O6O7O8"
        + "G2G5G8G1G4G7G0G3G6"
        + "B6B3B0B7B4B1B8B5B2"
        + "Y0Y1Y2Y3Y4Y5Y6Y7Y8"
        + "W0W1W2W3W4W5W6W7W8"
    ),
    "Y": (
        "W6W3W0W7W4W1W8W5W2"
        + "Y2Y5Y8Y1Y4Y7Y0Y3Y6"
        + "R0R1R2R3R4R5R6R7R8"
        + "O0O1O2O3O4O5O6O7O8"
        + "B0B1B2B3B4B5B6B7B8"
        + "G0G1G2G3G4G5G6G7G8"
    ),
    "Z": (
        "G0G1G2G3G4G5G6G7G8"
        + "B0B1B2B3B4B5B6B7B8"
        + "Y0Y1Y2Y3Y4Y5Y6Y7Y8"
        + "W0W1W2W3W4W5W6W7W8"
        + "R2R5R8R1R4R7R0R3R6"
        + "O6O3O0O7O4O1O8O5O2"
    ),
    "U": (
        "W6W3W0W7W4W1W8W5W2"
        + "Y0Y1Y2Y3Y4Y5Y6Y7Y8"
        + "R0R1R2G3G4G5G6G7G8"
        + "O0O1O2B3B4B5B6B7B8"
        + "B0B1B2R3R4R5R6R7R8"
        + "G0G1G2O3O4O5O6O7O8"
    ),
    "D": (
        "W0W1W2W3W4W5W6W7W8"
        + "Y6Y3Y0Y7Y4Y1Y8Y5Y2"
        + "G0G1G2G3G4G5O6O7O8"
        + "B0B1B2B3B4B5R6R7R8"
        + "R0R1R2R3R4R5G6G7G8"
        + "O0O1O2O3O4O5B6B7B8"
    ),
    "L": (
        "O8W1W2O5W4W5O2W7W8"
        + "R0Y1Y2R3Y4Y5R6Y7Y8"
        + "G6G3G0G7G4G1G8G5G2"
        + "B0B1B2B3B4B5B6B7B8"
        + "W0R1R2W3R4R5W6R7R8"
        + "O0O1Y6O3O4Y3O6O7Y0"
    ),
    "R": (
        "W0W1R2W3W4R5W6W7R8"
        + "Y0Y1O6Y3Y4O3Y6Y7O0"
        + "G0G1G2G3G4G5G6G7G8"
        + "B6B3B0B7B4B1B8B5B2"
        + "R0R1Y2R3R4Y5R6R7Y8"
        + "W8O1O2W5O4O5W2O7O8"
    ),
    "F": (
        "W0W1W2W3W4W5G6G3G0"
        + "B0B3B6Y3Y4Y5Y6Y7Y8"
        + "Y2G1G2Y1G4G5Y0G7G8"
        + "W6B1B2W7B4B5W8B7B8"
        + "R6R3R0R7R4R1R8R5R2"
        + "O0O1O2O3O4O5O6O7O8"
    ),
    "B": (
        "B2B5B8W3W4W5W6W7W8"
        + "Y0Y1Y2Y3Y4Y5G8G5G2"
        + "G0G1W2G3G4W1G6G7W0"
        + "B0B1Y6B3B4Y7B6B7Y8"
        + "R0R1R2R3R4R5R6R7R8"
        + "O6O3O0O7O4O1O8O5O2"
    ),
    "crosses": (
        "W2Y1W0Y5W4Y3W8Y7W6"
        + "Y2W1Y0W5Y4W3Y8W7Y6"
        + "G2B7G0B5G4B3G8B1G6"
        + "B2G7B0G5B4G3B8G1B6"
        + "R0O7R2O3R4O5R6O1R8"
        + "O0R7O2R3O4R5O6R1O8"
    ),
    "repr": (
        "Cube(size=3, state='W0W1W2W3W4W5W6W7W8"
        + "Y0Y1Y2Y3Y4Y5Y6Y7Y8G0G1G2G3G4G5G6G7G8"
        + "B0B1B2B3B4B5B6B7B8R0R1R2R3R4R5R6R7R8"
        + "O0O1O2O3O4O5O6O7O8', debug=True)"
    ),
}

test_states = {
    "init": (
        "WWWWWWWWW"
        + "YYYYYYYYY"
        + "GGGGGGGGG"
        + "BBBBBBBBB"
        + "RRRRRRRRR"
        + "OOOOOOOOO"
    ),
    "X": (
        "RRRRRRRRR"
        + "OOOOOOOOO"
        + "GGGGGGGGG"
        + "BBBBBBBBB"
        + "YYYYYYYYY"
        + "WWWWWWWWW"
    ),
    "Y": (
        "WWWWWWWWW"
        + "YYYYYYYYY"
        + "RRRRRRRRR"
        + "OOOOOOOOO"
        + "BBBBBBBBB"
        + "GGGGGGGGG"
    ),
    "Z": (
        "GGGGGGGGG"
        + "BBBBBBBBB"
        + "YYYYYYYYY"
        + "WWWWWWWWW"
        + "RRRRRRRRR"
        + "OOOOOOOOO"
    ),
    "U": (
        "WWWWWWWWW"
        + "YYYYYYYYY"
        + "RRRGGGGGG"
        + "OOOBBBBBB"
        + "BBBRRRRRR"
        + "GGGOOOOOO"
    ),
    "D": (
        "WWWWWWWWW"
        + "YYYYYYYYY"
        + "GGGGGGOOO"
        + "BBBBBBRRR"
        + "RRRRRRGGG"
        + "OOOOOOBBB"
    ),
    "L": (
        "OWWOWWOWW"
        + "RYYRYYRYY"
        + "GGGGGGGGG"
        + "BBBBBBBBB"
        + "WRRWRRWRR"
        + "OOYOOYOOY"
    ),
    "R": (
        "WWRWWRWWR"
        + "YYOYYOYYO"
        + "GGGGGGGGG"
        + "BBBBBBBBB"
        + "RRYRRYRRY"
        + "WOOWOOWOO"
    ),
    "F": (
        "WWWWWWGGG"
        + "BBBYYYYYY"
        + "GGYGGYGGY"
        + "WBBWBBWBB"
        + "RRRRRRRRR"
        + "OOOOOOOOO"
    ),
    "B": (
        "BBBWWWWWW"
        + "YYYYYYGGG"
        + "WGGWGGWGG"
        + "BBYBBYBBY"
        + "RRRRRRRRR"
        + "OOOOOOOOO"
    ),
    "crosses": (
        "WYWYWYWYW"
        + "YWYWYWYWY"
        + "GBGBGBGBG"
        + "BGBGBGBGB"
        + "ROROROROR"
        + "ORORORORO"
    ),
    "repr": (
        "Cube(size=3, state='WWWWWWWWW"
        + "YYYYYYYYYGGGGGGGGG"
        + "BBBBBBBBBRRRRRRRRR"
        + "OOOOOOOOO', debug=True)"
    ),
}


class TestCube(unittest.TestCase):
    """
    Unit test cases for the Cube class.
    """

    def test_default_initialization(self):
        """
        Test the default initialization of the Cube class.
        Validates that a cube of size 3 is created and is in a solved state.
        """
        cube = Cube(debug=True)
        self.assertEqual(cube.size, 3)
        # Cube should be in solved state
        self.assertTrue(cube.is_solved())
        # Cube should be in the initial state
        self.assertEqual(str(cube), test_states["init"])

    def test_custom_initialization(self):
        """
        Test the custom initialization of the Cube class.
        Validates that a cube of specified size is created and is in a solved state.
        """
        for size in [2, 3]:
            cube = Cube(size=size, debug=True)
            # cube should be of the specified size
            self.assertEqual(cube.size, size)
            # Cube should be in solved state
            self.assertTrue(cube.is_solved())

    def test_cube_rotation(self):
        """
        Test the rotation of the cube around the X, Y, and Z axes.
        Validates that the cube rotates correctly and returns to the initial state.
        """
        cube = Cube(size=3, debug=True)
        for axis in "XYZ":
            # Rotate the cube clockwise
            cube.rotate_cube(axis=axis, clockwise=True)
            # Check if the cube is in the expected state after rotation
            self.assertEqual(str(cube), test_states[axis])
            # Rotate the cube counter-clockwise
            cube.rotate_cube(axis=axis, clockwise=False)
            # Check if the cube returns to the initial state
            self.assertEqual(str(cube), test_states["init"])

    def test_face_rotation(self):
        """
        Test the rotation of the cube faces.
        Validates that the cube faces rotate correctly and return to the initial state.
        """
        # Initialize the cube
        cube = Cube(size=3, debug=True)
        for face in "UDFBLR":
            logging.debug("Testing face rotation for %s", face)
            # Rotate the face clockwise
            cube.rotate_face(face, clockwise=True)
            logging.debug("Cube state after rotating %s clockwise: %s", face, cube)
            logging.debug("Expected state: %s", test_states[face])
            # Check if the cube is in the expected state after rotation
            self.assertEqual(str(cube), test_states[face])
            # Rotate the face counter-clockwise
            cube.rotate_face(face, clockwise=False)
            logging.debug(
                "Cube state after rotating %s counter-clockwise: %s", face, cube
            )
            logging.debug("Expected state: %s", test_states["init"])
            # Check if the cube returns to the initial state
            self.assertEqual(str(cube), test_states["init"])

    def test_scramble_and_reset(self):
        """
        Test the scramble function of the Cube class.
        Validates that the cube is scrambled and not in the initial state.
        """
        # Initialize the cube
        cube = Cube(size=3, debug=True)
        initial_state = str(cube)
        # Scramble the cube
        cube.scramble()
        # Check if the cube is not in the initial state
        self.assertNotEqual(str(cube), initial_state)
        # Reset the cube
        cube.reset()
        # Check if the cube returns to the initial state
        self.assertEqual(str(cube), initial_state)

    # def test_representation(self):
    #     """
    #     Test the string representation of the Cube class.
    #     Validates that the string representation matches the expected format.
    #     """
    #     # Initialize the cube
    #     cube = Cube(size=3, debug=True)
    #     cube.rotate_face("U", clockwise=True)
    #     cube_representation = repr(cube)
    #     cube2 = eval(cube_representation.replace('"', ""))
    #     self.assertEqual(str(cube), str(cube2))
    #     cube2.rotate_face("U", clockwise=False)
    #     self.assertTrue(cube2.is_solved())

    def test_crosses(self):
        """
        Test the crosses function of the Cube class.
        Validates that the crosses are created correctly on the cube.
        r,r,l,l,u,u,d,d,f,f,b,b

        r',r',l',l',u',u',d',d',f',f',b',b'
        """
        commands = "rrlluuddffbb"
        # Initialize the cube
        cube = Cube(size=3, debug=True)
        # Create crosses on the cube
        for command in commands:
            cube.rotate_face(command.upper(), clockwise=True)
        # Check if the crosses are created correctly
        self.assertEqual(str(cube), test_states["crosses"])
        for command in commands:
            # Rotate the face counter-clockwise
            cube.rotate_face(command.upper(), clockwise=False)
        # Check if the cube returns to the initial state
        self.assertEqual(str(cube), test_states["init"])

    # def test_load_state(self):
    #     """
    #     Test the load state function of the Cube class.
    #     Validates that the cube loads the state correctly.
    #     """
    #     # Initialize the cube
    #     cube = Cube(size=3, debug=True, state=test_states["crosses"])
    #     # Check if the crosses are created correctly
    #     self.assertEqual(str(cube), test_states["crosses"])


if __name__ == "__main__":
    unittest.main()
