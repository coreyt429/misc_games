"""
Unit tests for the solver class
"""

import unittest
import logging
from random import choice
from solver import Solver
from visualize import print_color_cube

ITERATIONS = 1000

cube_states = {
    "oriented": "XXXXWXXXXXXXXYXXXXXXXXGXXXXXXXXBXXXXXXXXRXXXXXXXXOXXXX",
    "solved": "WWWWWWWWWYYYYYYYYYGGGGGGGGGBBBBBBBBBRRRRRRRRROOOOOOOOO",
    "white_cross": "XWXWWWXWXXXXXYXXXXXGXXGXXXXXBXXBXXXXXRXXRXXXXXOXXOXXXX",
    "f2l": "WWWWWWWWWXXXXXXXXXGGGGGGXXXBBBBBBXXXRRRRRRXXXOOOOOOXXX",
    "oll": "WWWWWWWWWYYYYYYYYYGGGGGGXXXBBBBBBXXXRRRRRRXXXOOOOOOXXX"
}

# Enable debug logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def check_mask(check_string, mask_string):
    """
    Check if the characters in check_string match the mask_string.
    The mask_string can contain 'X' to ignore that position.
    """
    if not isinstance(check_string, str):
        check_string = str(check_string)
    for idx, char in enumerate(check_string):
        if char != mask_string[idx] and mask_string[idx] != "X":
            # print(f"\n{check_string}\n{mask_string}")
            return False
    return True


class TestSolver(unittest.TestCase):
    """
    Unit test cases for the Cube class.
    """

    ###################
    # Orientation tests
    ###################
    def test_orient_cube(self):
        """
        Test orientation of cube to white on top and red in front.
        Validates that the cube is oriented correctly after scrambling.
        The cube should have white on top and red in front.
        """
        solver = Solver()
        solve_iterations = ITERATIONS
        number_of_moves = 20

        for _ in range(solve_iterations):
            solver.cube.reset()
            for _ in range(number_of_moves):
                axis = choice(["x", "y", "z"])
                clockwise = choice([True, False])
                solver.cube.rotate_cube(axis=axis, clockwise=clockwise)
            solver.orient_cube()
            self.assertTrue(
                check_mask(
                    solver.cube,
                    cube_states["oriented"],
                )
            )

    ###################
    # Solver Steps
    ###################
    def test_white_cross(self):
        """
        Test solving the white cross.
        """
        solver = Solver()
        solve_iterations = ITERATIONS

        for _ in range(solve_iterations):
            solver.cube.reset()
            solver.cube.scramble()
            solver.cross()
            # Check if the cube is in a valid state
            self.assertTrue(check_mask(solver.cube, cube_states["white_cross"]))
            # check if our _check method works, not really necessary, but just to be sure
            self.assertTrue(solver._check_white_cross())  # pylint: disable=protected-access

    def test_f2l(self):
        """
        Test solving the first two layers (F2L).
        """
        solver = Solver()
        solve_iterations = ITERATIONS

        for iteration in range(solve_iterations):
            solver.cube.reset()
            solver.cube.scramble()
            scramble_state = str(solver.cube)
            solver.cross()
            solver.f2l()
            if not check_mask(solver.cube, cube_states["f2l"]):
                logging.warning(
                    "f2l failed iter(%s) for cube state: %s", iteration, scramble_state
                )
                logging.warning("Cube state after f2l: %s", str(solver.cube))
            # Check if the cube is in a valid state
            self.assertTrue(check_mask(solver.cube, cube_states["f2l"]))
            # check if our _check method works, not really necessary, but just to be sure
            self.assertTrue(solver._f2l_is_solved())  # pylint: disable=protected-access

    def test_oll(self):
        """
        Test solving the orientation of the last layer (OLL).
        """
        solver = Solver()
        solve_iterations = ITERATIONS

        for iteration in range(solve_iterations):
            solver.cube.reset()
            solver.cube.scramble()
            scramble_state = str(solver.cube)
            solver.cross()
            solver.f2l()
            solver.oll()
            solver.orient_cube()
            if not check_mask(solver.cube, cube_states["oll"]):
                logging.warning(
                    "OLL failed iter(%s) for cube state: %s", iteration, scramble_state
                )
                logging.warning("Cube state after OLL: %s", str(solver.cube))
            # Check if the cube is in a valid state
            self.assertTrue(check_mask(solver.cube, cube_states["oriented"]))
            # check if our _check method works, not really necessary, but just to be sure
            self.assertTrue(solver._oll_is_solved())


if __name__ == "__main__":
    unittest.main()
