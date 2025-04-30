def store_move_string(move_string, move_length):
    # Define the filename based on the move length
    filename = f"possible_{move_length}_moves.txt"

    # Open the file in append mode
    with open(filename, "a") as file:
        # Append the move string to the file followed by a newline character
        file.write(move_string + "\n")


def build_move_string(new_move, move_length, move_list=[]):
    # print(f"build_move_string({new_move},{move_length},{move_list})")
    move_list.append(new_move)
    move_string = ",".join(move_list)
    # print(f"{len(move_list)} < {move_length} = {len(move_list) < move_length}")
    if len(move_list) < move_length:
        # print(f"{move_list} is smaller than {move_length}")
        for new_move in cube_moves:
            build_move_string(new_move, move_length, move_string.split(","))
    else:
        store_move_string(move_string, move_length)


planes = "RLFBUD"

cube_moves = set()

for plane in planes:
    cube_moves.add(plane)
    cube_moves.add(f"{plane}'")

for size in range(1, 26):
    for move in cube_moves:
        build_move_string(move, size, [])
