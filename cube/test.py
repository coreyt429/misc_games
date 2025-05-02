"""
This is a test file to compare the performance of Cube 1 and Cube 2.
The test will run 1000 iterations, where in each iteration:
1. A cube is scrambled and saved to a file.
2. The cube is loaded from the file and solved.
The time taken for each operation is recorded.
The results will be printed at the end, showing how many times each cube was faster.
"""

import cube2
import cube

winners = {0: 0, 1: 0, 2: 0}
for test in range(1000):
    print("Cube 2")
    c = cube2.Cube()
    c.scramble()
    c.save("clock.cube")
    time_2 = c.clock()

    print("Cube 1")
    c = cube.Cube("clock.cube")
    # c.scramble()
    # c.save('clock1.cube')
    # c.scramble()
    time_1 = c.clock()

    if time_1 > time_2:
        winners[2] += 1
    elif time_1 == time_2:
        winners[0] += 1
    else:
        winners[1] += 1

print(winners)
