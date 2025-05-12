from heapq import heappush, heappop
import json
from time import time
from cube import Cube
from visualize import print_color_cube
from solver import Solver


def mask_cube(cube):
    """
    Mask the cube to show only the top face.
    """
    for cubie in cube:
        if len(cubie.color) == 1:
            continue
        if len(cubie.color) == 2 and "W" in cubie.color:
            continue
        cubie.color = tuple(["Y" for color in cubie.color])


# already_seen is a dictionary to keep track of already seen cube states
# and the number of moves to reach them, only update if the new instance
# of the state is reached in fewer moves


def run_cube_states(state_string, move_limit=2):
    """
    breadth first search function to run through all possible cube states
    """
    already_seen = {}
    heap = []
    heappush(heap, (0, state_string, "X", True, ()))
    while heap:
        moves, state_string, face, clockwise, history = heappop(heap)
        if len(heap) % 1000 == 0:
            print(
                f"heap: {len(heap)}, moves: {moves}, move_limit: {move_limit}, saved: {len(already_seen)}, state_string: {state_string}"
            )
        if state_string in already_seen and already_seen[state_string]["moves"] < moves:
            continue
        already_seen[state_string] = {"moves": moves, "history": history}
        if moves >= move_limit:
            continue
        if face == "X":
            # run each move clockwise and counter clockwise
            for move in ["U", "D", "L", "R", "F", "B"]:
                heappush(heap, (moves, state_string, move, True, history))
                heappush(heap, (moves, state_string, move, False, history))
            continue
        cube = Cube(state=state_string)
        if face in ["U", "D", "L", "R", "F", "B"]:
            # rotate the face
            cube.rotate_face(face, clockwise)
        elif face in ["M", "E", "S"]:
            # rotate the slice
            cube.rotate_slice(face, clockwise)
        else:
            print(f"How did we get here? {face}")
            continue
        # push new state to heap
        heappush(
            heap, (moves + 1, str(cube), "X", True, history + ((face, clockwise),))
        )
    return already_seen


masked_cube_string = "YWYWWWYWYYYYYYYYYYYGYYGYYYYYBYYBYYYYYRYYRYYYYYOYYOYYYY"
start_time = time()
result = run_cube_states(masked_cube_string, 20)
print(f"Result length: {len(result)}")
with open("white_cross_states.json", "w") as f:
    json.dump(result, f)
print(f"Time taken: {time() - start_time} seconds")
