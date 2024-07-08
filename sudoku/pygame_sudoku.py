import pygame
import sys
import sudoku
import copy

# Initialize pygame
pygame.init()

# Set up the display
screen_size = 450
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Sudoku")

# Colors and settings
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0 , 0)
green = (0,255, 0)

highlight_color = (200, 200, 255)  # Light blue for highlighting
cell_size = screen_size // 9
highlight_pos = [0, 0]

# initialize sudoku object
sudoku_board = sudoku.Sudoku()
sudoku_board.puzzle(level='easy')
start_board = copy.deepcopy(sudoku_board.board)

# Fonts for numbers
font = pygame.font.Font(None, 40)  # None uses the default font, 40 is the size

# function to get filename from user
def get_filename(prompt,error=''):
    input_active = True
    user_input = []
    pygame.display.set_caption(prompt)  # Set window title to show prompt

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input.append(event.unicode)
        
        # Render the current text
        screen.fill(white)
        text_surface = font.render(''.join(user_input), True, black)
        screen.blit(text_surface, (10, screen_size // 2))
        pygame.display.flip()


    pygame.display.set_caption("Sudoku")  # Reset the window title
    return ''.join(user_input)

# Function to draw the grid and numbers
def draw_grid(sudoku_board):
    for i in range(10):  # There are 10 lines for a 9x9 grid
        width = 2 if i % 3 == 0 else 1
        pygame.draw.line(screen, black, (i * cell_size, 0), (i * cell_size, screen_size), width)
        pygame.draw.line(screen, black, (0, i * cell_size), (screen_size, i * cell_size), width)

    # check for win
    win = True
    for row in range(9):
        for col in range(9):
            number = sudoku_board.board[row][col]
            if  number == 0:
                win = False
            if not sudoku_board.is_valid(number, (row,col)):
                win = False
    
    # Draw numbers
    for row in range(9):
        for col in range(9):
            number = sudoku_board.board[row][col]
            if number != 0:
                if win:
                    text = font.render(str(number), True, green)
                elif sudoku_board.is_valid(number, (row,col)):
                    if start_board[row][col] == sudoku_board.board[row][col]:
                        text = font.render(str(number), True, black)
                    else:
                        text = font.render(str(number), True, blue)
                else:
                    text = font.render(str(number), True, red)
                text_rect = text.get_rect(center=((col * cell_size + cell_size // 2), (row * cell_size + cell_size // 2)))
                screen.blit(text, text_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and highlight_pos[0] > 0:
                highlight_pos[0] -= 1
            elif event.key == pygame.K_RIGHT and highlight_pos[0] < 8:
                highlight_pos[0] += 1
            elif event.key == pygame.K_UP and highlight_pos[1] > 0:
                highlight_pos[1] -= 1
            elif event.key == pygame.K_DOWN and highlight_pos[1] < 8:
                highlight_pos[1] += 1
            elif pygame.K_0 <= event.key <= pygame.K_9:
                num = event.key - pygame.K_0  # Get the number key that was pressed
                sudoku_board.board[highlight_pos[1]][highlight_pos[0]] = num
                print("Solution count:", sudoku_board.count_solutions())
            elif  event.key ==  pygame.K_s:
                filename = get_filename("Enter filename to save:")
                sudoku_board.save(filename)
                start_board = copy.deepcopy(sudoku_board.board)
            elif  event.key ==  pygame.K_l:
                filename = get_filename("Enter filename to load:")
                if sudoku_board.load(filename):
                    start_board = copy.deepcopy(sudoku_board.board)
                else:
                    print(f"Failed to load {filename}")
            elif  event.key ==  pygame.K_x:
                sudoku_board.solve()
            elif  event.key ==  pygame.K_n:
                sudoku_board.puzzle(level='easy')
                start_board = copy.deepcopy(sudoku_board.board)
            elif  event.key ==  pygame.K_1:
                running = False
                

    # Fill the screen with white
    screen.fill(white)

    # Draw the highlighted cell
    highlight_rect = pygame.Rect(highlight_pos[0] * cell_size, highlight_pos[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, highlight_color, highlight_rect)

    # Draw the grid and numbers on top
    draw_grid(sudoku_board)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
