import pygame
import sys
import copy
import random

# Initialize pygame
pygame.init()

# Set up the display
screen_size = 450
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Rubik's Cube")

# Colors and settings
black = (0, 0, 0)
gray =  (169,169,169)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0 , 0)
yellow = (255,255,0)
orange = (255,165,0)
green = (0,255, 0)

highlight_color = (200, 200, 255)  # Light blue for highlighting
cell_size = screen_size // 9
highlight_pos = [0, 0]

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
        screen.fill(gray)
        text_surface = font.render(''.join(user_input), True, black)
        screen.blit(text_surface, (10, screen_size // 2))
        pygame.display.flip()


    pygame.display.set_caption("Sudoku")  # Reset the window title
    return ''.join(user_input)

# Function to draw the cube

def draw_face(face,upper_left, upper_right, lower_right, lower_left):
    square_size = int((upper_right[0] - upper_left[0])/3)
    width=2
    
    # Draw outline
    pygame.draw.line(screen, black, upper_left, upper_right, width)
    pygame.draw.line(screen, black, upper_right, lower_right, width)
    pygame.draw.line(screen, black, lower_right, lower_left, width)
    pygame.draw.line(screen, black, lower_left, upper_left, width)

    # draw inner grid
    width = 1
    x_1,y_1 = upper_left 
    x_2,y_2 = upper_right
    y_1+=square_size
    y_2+=square_size
    pygame.draw.line(screen, black, (x_1,y_1), (x_2,y_2), width)
    y_1+=square_size
    y_2+=square_size
    pygame.draw.line(screen, black, (x_1,y_1), (x_2,y_2), width)
    x_1,y_1 = upper_left 
    x_2,y_2 = lower_left
    x_1+=square_size
    x_2+=square_size
    pygame.draw.line(screen, black, (x_1,y_1), (x_2,y_2), width)
    x_1+=square_size
    x_2+=square_size
    pygame.draw.line(screen, black, (x_1,y_1), (x_2,y_2), width)

    colors = {
        "F": red,
        "R": green,
        "B": orange,
        "L": blue,
        "U": yellow,
        "D": white
    }

    # fill squares
    x_1, y_1 = upper_left
    for position in range(1,10):
        if position in [4,7]:
            y_1+=square_size
        if position in [1,4,7]:
            x_1 = upper_left[0]
        else:
            x_1+=square_size
        pygame.draw.rect(screen, colors[face], (x_1+1, y_1+1, square_size-1, square_size-1))
    

def draw_cube():
    # 12 squares wide
    # 9 squares high
    # 4 faces wide
    # 3 faces high
    padding = 5
    face_size = int(screen_size/4)-padding*2
    faces = 'L'
    middle = int(screen_size/2)
    row_2 = middle-int(face_size/2)
    row_1 = row_2 - (face_size+padding*2)
    row_3 = row_2 + (face_size+padding*2)
    face_corners = { # upper left corners
        "L": (0+padding,row_2),
        "F": (padding*3+face_size,row_2),
        "R": (2*(padding*2+face_size)+padding,row_2),
        "B": (3*(padding*2+face_size)+padding,row_2),
        "U": (padding*3+face_size,row_1),
        "D": (padding*3+face_size,row_3)

    }
    
    for face in face_corners:
        #(5, 172) (112, 172) (112, 278) (5, 278)
        upper_left = face_corners[face]
        upper_right = (upper_left[0] + face_size, upper_left[1])
        lower_right = (upper_right[0],upper_right[1]+face_size)
        lower_left = (upper_left[0],lower_right[1])
        
        draw_face(face,upper_left, upper_right, lower_right, lower_left)
        



# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # commands from cube main
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
            elif  event.key ==  pygame.K_s:
                filename = get_filename("Enter filename to save:")
                #sudoku_board.save(filename)
                #start_board = copy.deepcopy(sudoku_board.board)
            elif  event.key ==  pygame.K_l:
                filename = get_filename("Enter filename to load:")
                #if sudoku_board.load(filename):
                #    start_board = copy.deepcopy(sudoku_board.board)
                #else:
                #    print(f"Failed to load {filename}")
            elif  event.key ==  pygame.K_x:
                #sudoku_board.solve()
                pass
            elif  event.key ==  pygame.K_n:
                #sudoku_board.puzzle(level='easy')
                #start_board = copy.deepcopy(sudoku_board.board)
                pass
            elif  event.key ==  pygame.K_1:
                running = False
                

    # Fill the screen with white
    screen.fill(gray)
    
    # Draw the grid and numbers on top
    #draw_grid(sudoku_board)
    draw_cube()

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
