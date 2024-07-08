import json

class TicTacToe:
    COLORS = {
        'K': '\033[30m',   # Black text
        'R': '\033[31m',   # Red text
        'Y': '\033[33m',   # Yellow text
        'G': '\033[32m',   # Green text
        'B': '\033[34m',   # Blue text
        'O': '\033[38;5;208m',  # Orange text
        'W': '\033[37m'    # White text
    }

    RESET = '\033[0m'

    def __init__(self, filename=None):
        self.WINNERS = {'      XXX': 'X','OOO      ': 'O'}
        self.player = 'X'
        self.board = ' '*9
        self.probabilities = list([-1])*9
        self.build_heuristics('X',self.board)

    def play_move(self,square):
        if self.board[square] == ' ':
            tmp_board = list(self.board)
            tmp_board[square] = self.player
            self.board = ''.join(tmp_board)
            won,winner = self.is_winner()
            # don't swap players if there is a winner
            if not won:
                if self.player == 'X':
                    self.player = 'O'
                else:
                    self.player = 'X'
            return True
        else:
            print(f"Invalid move: {square} is occupied by {self.board[square]}")
            return False
    
    def pretty(self,square):
        player = self.board[square]
        if player == 'X':
            return f"{self.COLORS['R']} {player} {self.RESET}"
        elif player == 'O':
            return f"{self.COLORS['G']} {player} {self.RESET}"
        else:
            percentage = self.probability(square)
            formatted_percentage = f"{int(percentage):3d}"[-3:]
            return formatted_percentage

    def __str__(self):
        self.probabilities = list([-1])*9
        return f"""
 {self.pretty(0)} | {self.pretty(1)} | {self.pretty(2)}
{"-"*17}
 {self.pretty(3)} | {self.pretty(4)} | {self.pretty(5)}
{"-"*17}
 {self.pretty(6)} | {self.pretty(7)} | {self.pretty(8)}

"""

    def is_winner(self,board=None):
        if board is None:
            board = self.board
        lines = [
            (0,1,2),
            (3,4,5),
            (6,7,8),
            (0,3,6),
            (1,4,7),
            (2,5,8),
            (0,4,8),
            (2,4,6)
        ]

        for line in lines:
            row = {board[i] for i in line}
            if len(row) == 1: # everything in line was the same
                if list(row)[0] != ' ': # row isn't empty
                    return True, list(row)[0] # Winner
        # no winner, but also no squares left
        if ' ' not in board: # no winner, and also no further moves
            return False, 'cat'
        return False, 'X'


    def probability(self,square):
        #print(f"probability({square}): {self.player}")
        wins = {
            "X": 0,
            "O": 0
        }
        tmp_board_list = list(self.board)
        tmp_board_list[square] = self.player
        tmp_board = ''.join(tmp_board_list)
        #print(f"board: {tmp_board}")
        for key in self.WINNERS:
            #print(f"key:   {key}")
            match = True
            for k, b  in zip(key,tmp_board):
                #print(f"if {b} != ' ' and {k} != {b}")
                if b != ' ' and k != ' ' and k != b:
                    match = False
            if match:
                wins[self.WINNERS[key]] += 1
                #print("match",key)
        if (wins['X'] + wins['O']) == 0:
            #print("let's avoid division by zero")
            return 0
        #print(wins)
        self.probabilities[square] = 100*(wins[self.player]/(wins['X'] + wins['O']))
        return self.probabilities[square]

    def build_heuristics(self,player,board):
        won, winner = self.is_winner(board)
        if won:
            self.WINNERS[board] = winner
        new_player = 'O'
        if player == 'O':
            new_player = 'X'
        for idx in range(9):
            new_board = list(board)
            if new_board[idx] == ' ':
                new_board[idx] = player
                self.build_heuristics(new_player,''.join(new_board))

