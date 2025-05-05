"""
Test cases for the Cube class.
"""

from cube import Cube, FACES
from visualize import print_color_cube

OKAY = "[\033[92m  OK  \033[0m]"
# Initial State:
states = {
    "init": (
        "W0W1W2W3W4W5W6W7W8Y0Y1Y2Y3Y4Y5Y6Y7Y8G0G1G2G3G4G5G6G7G8"
        + "B0B1B2B3B4B5B6B7B8R0R1R2R3R4R5R6R7R8O0O1O2O3O4O5O6O7O8"
    ),
    "X": (
        "R0R1R2R3R4R5R6R7R8O0O1O2O3O4O5O6O7O8G2G5G8G1G4G7G0G3G6"
        + "B6B3B0B7B4B1B8B5B2Y0Y1Y2Y3Y4Y5Y6Y7Y8W0W1W2W3W4W5W6W7W8"
    ),
    "Y": (
        "W6W3W0W7W4W1W8W5W2Y2Y5Y8Y1Y4Y7Y0Y3Y6R0R1R2R3R4R5R6R7R8"
        + "O0O1O2O3O4O5O6O7O8B0B1B2B3B4B5B6B7B8G0G1G2G3G4G5G6G7G8"
    ),
    "Z": (
        "G0G1G2G3G4G5G6G7G8B0B1B2B3B4B5B6B7B8Y0Y1Y2Y3Y4Y5Y6Y7Y8"
        + "W0W1W2W3W4W5W6W7W8R2R5R8R1R4R7R0R3R6O6O3O0O7O4O1O8O5O2"
    ),
}
if __name__ == "__main__":
    # Example usage
    CUBE_SIZE = 3  # Size of the cube
    print("Initialize Cube: ", end="")
    cube = Cube(size=CUBE_SIZE, debug=True)
    print_color_cube(str(cube))
    assert cube.size == CUBE_SIZE, f"Expected size {CUBE_SIZE}, but got {cube.size}"
    print(OKAY)
    assert str(cube) == states["init"], f"Expected initial state, but got {str(cube)}"
    for axis in ["X", "Y", "Z"]:
        cube.rotate_cube(clockwise=True, axis=axis)
        print(f"Rotate {axis} axis clockwise: ", end="")
        assert str(cube) == states[axis], f"Expected {axis} state, but got {str(cube)}"

        print(f"Rotate {axis} axis counter clockwise: ", end="")
        cube.rotate_cube(clockwise=False, axis=axis)
        assert str(cube) == states["init"], (
            f"Expected initial state after {axis}', but got {str(cube)}"
        )
        print(OKAY)
    for face in FACES:
        print(f"Rotate face {face} clockwise: ", end="")
        cube.rotate_face(face, clockwise=True)
        assert str(cube) == states["init"], (
            f"Expected {face} state', but got {str(cube)}"
        )
        print(OKAY)
        print(f"Rotate face {face} counter clockwise: ", end="")
        cube.rotate_face(face, clockwise=False)
        cube.rotate_cube(clockwise=False, axis=axis)
        assert str(cube) == states["init"], (
            f"Expected initial state after {face}', but got {str(cube)}"
        )
        print(OKAY)
