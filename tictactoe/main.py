import tictactoe
import random

ttt = tictactoe.TicTacToe()


player = 'X'
won = False
while not won:
	print(ttt)
	if ttt.player == 'X':
		user_input = input(f"Player {ttt.player} choose square [0-8]: ").strip()
		if user_input in '012345678':
			ttt.play_move(int(user_input))
		else:
			print(f"Invalid input: {user_input}")
	else:
		max_score = max(ttt.probabilities)
		print(f"Highest probability is {max_score}")
		squares = [index for index, value in enumerate(ttt.probabilities) if value == max_score]
		print(f"Possible squares: {squares}")
		random_square = random.choice(squares)
		ttt.play_move(random_square)
	won, winner = ttt.is_winner()
	if winner == 'cat':
		break

print()
print(ttt)
#ttt.show()

if won:
	print(f"Congratulations {ttt.player}, you won!!!")
else:
	print(f"Cat game")
print()

