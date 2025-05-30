"""
main cli loop
to play with the cube
"""

import logging
from cube import Cube
from solver import Solver
from visualize import print_color_cube

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main_loop():
    """
    Main loop for the command line interface.
    """
    cube = Cube(size=3, debug=True)
    solver = Solver(cube)

    while True:
        print_color_cube(str(cube))
        user_input = input("Enter a command: ").strip()
        commands = [cmd.strip().lower() for cmd in user_input.replace(",", " ").split()]
        for command in commands:
            if command in ["quit", "q"]:
                print("Exiting...")
                return
            if command in ["u", "f", "d", "l", "r", "b"]:
                cube.rotate_face(command.upper(), clockwise=True)
            elif command in ["u2", "f2", "d2", "l2", "r2", "b2"]:
                cube.rotate_face(command.upper()[:-1], clockwise=True)
                cube.rotate_face(command.upper()[:-1], clockwise=True)
            elif command in ["u'", "f'", "d'", "l'", "r'", "b'"]:
                cube.rotate_face(command.upper()[:-1], clockwise=False)
            elif command in ["x", "y", "z"]:
                cube.rotate_cube(axis=command, clockwise=True)
            elif command in ["x'", "y'", "z'"]:
                cube.rotate_cube(axis=command[:-1], clockwise=False)
            elif command in ["m", "e", "s"]:
                cube.rotate_slice(slice=command, clockwise=True)
            elif command in ["m'", "e'", "s'"]:
                cube.rotate_slice(slice=command[:-1], clockwise=False)
            elif command == "state":
                print(cube)
            elif command == "scramble":
                cube.scramble()
            elif command == "reset":
                cube.reset()
            elif command in ["p", "print"]:
                print(cube)
            elif command in ["twist", "t"]:
                cubie = cube.get_cubie("DBL")
                print(f"cubie: {cubie}")
                cubie.orientation = (cubie.orientation + 1) % len(cubie.color)
                print(f"new orientation: {cubie.orientation}")
            elif len(command) == 54:
                cube = Cube(state=command)
            elif command in ["wc", "whitecross", "white_cross"]:
                solver.cross()
            elif command == "f2l":
                solver.f2l()
            elif command == "oll":
                solver.oll()
            elif command == "pll":
                solver.pll()
            else:
                cubie = cube.get_cubie(command.upper())
                if cubie:
                    print(f"Cubie {command}: {cubie}")
                else:
                    print(f"Invalid command or cubie: {command}")
                    logging.error(f"Invalid command or cubie: {command}")


if __name__ == "__main__":
    main_loop()
