import random
import json

class Sudoku:
    def __init__(self, filename=None):
        if not filename is None:
            pass
        else:
            self.board = [[0 for _ in range(9)] for _ in range(9)]

    def __str__(self, label="Board"):
        retval = f"\n{label}:\n\n"
        for row in range(len(self.board)):
            retval += " ".join(str(num) if num != 0 else '.' for num in self.board[row][:3]) + " | " + " ".join(str(num) if num != 0 else '.' for num in self.board[row][3:6]) + " | " + " ".join(str(num) if num != 0 else '.' for num in self.board[row][6:])  + "\n"
            if row in (2,5):
                retval += '-'*21 + "\n"
        retval += "\n"
        return retval

    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.board, file)

    def load(self, filename):
        try:
            with open(filename, 'r') as file:
                self.board = json.load(file)
                print(f"Loaded {filename}")
                return True
        except:
            print(f"No {filename}")
            return False

    def find_empty_location(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return i, j  # row, col
        return None

    def is_valid(self, num, pos):
        # Check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False
        # Check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False
        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def count_solutions(self):
        find = self.find_empty_location()
        if not find:
            return 1  # No empty location, so this is a complete and valid solution
        else:
            row, col = find

        solution_count = 0
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                solution_count += self.count_solutions()
                self.board[row][col] = 0  # Reset on backtrack

        return solution_count

    def solve(self):
        print("solve()")
        find = self.find_empty_location()
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0

        return False

    def generate_sudoku(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve()

    def puzzle(self,**kwargs):
        if 'shuffle' not in kwargs or kwargs['shuffle']:
            self.generate_sudoku()
        level = 'easy'
        if 'level' in kwargs:
            level = kwargs['level']
        removes = {
            "easy": 43,
            "medium": 50,
            "hard": 60
        }
        for count in range(removes[level]):
            numbers = list(range(9))
            x = random.choice(numbers)
            y = random.choice(numbers)
            # this should probably use a method instead of manipulating board directly
            self.board[x][y]=0


if __name__ == "__main__":
    sudoku_board = Sudoku()
    sudoku_board.board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    print("Solution count:", sudoku_board.count_solutions())
