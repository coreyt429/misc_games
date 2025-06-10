import json
from cube import Cube
from solver import Solver

with open('pll_sequences.json', 'r') as f:
    pll_sequences = json.load(f)

with open('pll_sequence_data.json', 'r') as f:
    pll_seqence_data = json.load(f)


def main():
    # Create a Solver instance
    solver = Solver()
    for _ in range(1):
        solver.cube.scramble()
        # Solve the cube
        solver.solve()
        pll_state = solver._pll_get_state()

        if pll_state in pll_seqence_data:
            print(f"PLL state already processed: {pll_state}")
            solver.cube.sequence(pll_seqence_data[pll_state])
            if not solver.cube.is_solved(
                
            ):
                print("!!!!! Cube is not solved after applying the PLL sequence.")
            continue

        cube_state = str(solver.cube)
        solved = False
        for sequence_id, sequence in pll_sequences.items():
            solver.cube = Cube(state=cube_state)
            pll_state = solver._pll_get_state()
            print(f"cube state: {cube_state}, PLL state: {pll_state}, sequence_id: {sequence_id}, sequence: {sequence}")
            solver.cube.sequence(sequence)
            print(f"cube state after sequence: {str(solver.cube)}")
            if solver.cube.is_solved():
                print(f"Found PLL sequence for state {pll_state}: {sequence}")
                pll_seqence_data[pll_state] = sequence
                with open('pll_sequence_data.json', 'w') as f:
                    json.dump(pll_seqence_data, f, indent=4)
                    solved = True
                break
            for prefix in ['U', 'U2', "U'", 'Y', 'Y2', "Y'"]:
                solver.cube = Cube(state=cube_state)
                new_pll_state = solver._pll_get_state()
                print(f"cube state: {str(solver.cube)}, PLL state: {new_pll_state}, sequence_id: {sequence_id}, prefix: {prefix}, sequence: {prefix + ' ' + sequence}")
                solver.cube.sequence(prefix + ' ' + sequence)
                print(f"cube state after sequence: {str(solver.cube)}")
                if solver.cube.is_solved():
                    print(f"Found PLL sequence with prefix {prefix} for state {pll_state}: {sequence}")
                    pll_seqence_data[pll_state] = prefix + ' ' + sequence
                    with open('pll_sequence_data.json', 'w') as f:
                        json.dump(pll_seqence_data, f, indent=4)
                        solved = True
                    break
            if solved:
                break
        if not solved:
            print(f"No PLL sequence found for state {pll_state}. Cube state: {cube_state}")

if __name__ == "__main__":
    main()