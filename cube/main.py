"""
This is a simple command line interface for a Rubik's Cube solver.
It allows the user to interact with the cube, perform various
operations, and test the solver's performance.
"""

import sys
import time
import logging
import cube
import cube2

logging.basicConfig(level=logging.INFO)


def handle_debug_command(mycube, command=None):
    """
    Toggle debug mode for the cube.
    """
    if command:
        print(f"I don't know what to do with {command}")
    if mycube.cfg["debug"]:
        mycube.set_debug(False)
        logging.info("Debug disabled")
    else:
        mycube.set_debug(True)
        logging.info("Debug enabled")


def handle_rotate_command(mycube, command):
    """
    Rotate the cube based on the command.
    """
    clockwise = True
    if "'" in command:
        clockwise = False
    if "x" in command.lower():
        mycube.rotate_cube(clockwise)
    elif "t" in command.lower():
        mycube.tilt_cube(clockwise)
    else:
        mycube.rotate(command[0].upper(), clockwise)


def handle_test_command(mycube, command):
    """
    Run a series of tests on the cube.
    """
    test_count = int(command.split(" ")[1])
    successful = 0
    solved = False
    failure_steps = {}
    start_time = time.time()
    for _ in range(test_count):
        solved = False
        mycube.scramble()
        solved, failed_step = mycube.solve()
        if solved:
            successful += 1
        else:
            if failed_step in failure_steps:
                failure_steps[failed_step] += 1
            else:
                failure_steps[failed_step] = 1
            mycube.save(f"last_fail.{failed_step}.cube")
    end_time = time.time()
    total_time = end_time - start_time
    avg_time_per_test = total_time / test_count

    print(f"{successful} of {test_count} solves completed")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per test: {avg_time_per_test:.2f} seconds")
    if failure_steps:
        print("Failure steps count:")
        for step, count in failure_steps.items():
            print(f"{step}: {count}")


def handle_save_command(mycube, command):
    """
    Save the current state of the cube to a file.
    """
    mycube.save(command.split(" ", 1)[1])


def handle_load_command(mycube, command):
    """
    Load a saved state of the cube from a file.
    """
    mycube.load(command.split(" ", 1)[1])


def handle_new_command(mycube, command):
    """
    Create a new cube of the specified type.
    """
    cube_type = 1
    commands = command.split(" ")
    if len(commands) == 2:
        cube_type = int(commands[1])
    # these need to replace the mycube object that was passed in, I don't think they will like this
    if cube_type == 1:
        mycube = cube.Cube()
    elif cube_type == 2:
        mycube = cube2.Cube()
    return mycube


def print_help(**args):
    """
    Print the help message with available commands.
    """
    logging.debug("print_help(%s)", args)
    print("Available commands:")
    print("  debug - Toggle debug mode")
    print("  scramble - Scramble the cube")
    print("  u, f, d, l, r, b - Rotate the cube faces")
    print("  c - Rotate the cube clockwise")
    print("  m - Rotate the cube counter-clockwise")
    print("  x - Rotate the cube")
    print("  t - Tilt the cube")
    print("  rotate - Rotate the cube")
    print("  wc - Solve white cross")
    print("  wcn - Solve white corners")
    print("  2l - Solve second layer")
    print("  yc - Solve yellow cross")
    print("  ye - Solve yellow edges")
    print("  ycn - Solve yellow corners")
    print("  oycn - Orient yellow corners")
    print("  solve - Solve the cube")
    print("  superflip - Perform a superflip on the cube")
    print("  crosses - Perform crosses on the cube")
    print("  test <count> - Run tests on the cube")
    print("  save <filename> - Save the current state of the cube to a file")
    print("  load <filename> - Load a saved state of the cube from a file")
    print("  new <cube_type> - Create a new cube (1 or 2)")
    print("  h, help - Show this help message")
    print("  quit, q - Exit the program")


def main_loop():
    """
    Main loop for the command line interface.
    """
    mycube = cube.Cube()
    command_handlers = {
        "debug": handle_debug_command,
        "scramble": lambda mycube, command: mycube.scramble(),
        "u": handle_rotate_command,
        "f": handle_rotate_command,
        "d": handle_rotate_command,
        "l": handle_rotate_command,
        "r": handle_rotate_command,
        "b": handle_rotate_command,
        "c": handle_rotate_command,
        "m": handle_rotate_command,
        "x": handle_rotate_command,
        "t": handle_rotate_command,
        "rotate": handle_rotate_command,
        "wc": lambda mycube, command: mycube.solve_white_cross(),
        "white_cross": lambda mycube, command: mycube.solve_white_cross(),
        "wcn": lambda mycube, command: mycube.solve_white_corners(),
        "white_corners": lambda mycube, command: mycube.solve_white_corners(),
        "2l": lambda mycube, command: mycube.solve_second_layer(),
        "second_layer": lambda mycube, command: mycube.solve_second_layer(),
        "yc": lambda mycube, command: mycube.solve_yellow_cross(),
        "yellow_cross": lambda mycube, command: mycube.solve_yellow_cross(),
        "ye": lambda mycube, command: mycube.solve_yellow_edges(),
        "yellow_edges": lambda mycube, command: mycube.solve_yellow_edges(),
        "ycn": lambda mycube, command: mycube.solve_yellow_corners(),
        "yellow_corners": lambda mycube, command: mycube.solve_yellow_corners(),
        "oycn": lambda mycube, command: mycube.orient_yellow_corners(),
        "orient_yellow_corners": lambda mycube, command: mycube.orient_yellow_corners(),
        "solve": lambda mycube, command: mycube.solve(),
        "superflip": lambda mycube, command: mycube.superflip(),
        "crosses": lambda mycube, command: mycube.run_command_string(
            "U,R,U',L',U,R',U',L,U,U,R,U',L',U,R',U',L,U',T,T,",
            "U,R,U',L',U,R',U',L,U,U,R,U',L',U,R',U',L,U',T,T",
        ),
        "test": handle_test_command,
        "save": handle_save_command,
        "load": handle_load_command,
        "new": handle_new_command,
        "h": print_help,
        "help": print_help,
        "quit": lambda mycube, command: sys.exit(),
        "q": lambda mycube, command: sys.exit(),
    }

    while True:
        mycube.print()
        user_input = input("Enter a command: ").strip()
        for command in user_input.rstrip(",").split(","):
            base_command = command.split(" ")[0].lower()
            if "'" in base_command:
                base_command = base_command[0]
            handler = command_handlers.get(base_command)

            if handler:
                if base_command == "new":
                    mycube = handler(mycube, command)
                else:
                    handler(mycube, command)
            else:
                logging.warning("Unknown command: %s", command)


if __name__ == "__main__":
    main_loop()
