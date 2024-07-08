"""
pygame visualization for cube2 type Rubik's cube
"""
import sys
import pygame
import cube2


# pylint: disable=no-member

# Initialize pygame
pygame.init()

# Set up the display
SCREEN_SIZE = 450
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
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

# define color map
color_map = {
    "R": red,
    "G": green,
    "O": orange,
    "B": blue,
    "Y": yellow,
    "W": white
}

# Fonts for numbers
font = pygame.font.Font(None, 40)  # None uses the default font, 40 is the size

# function to get filename from user
def get_filename(prompt):
    """
    Function to prompt a user for a filename
    """
    input_active = True
    user_input = []
    pygame.display.set_caption(prompt)  # Set window title to show prompt

    while input_active:
        for file_input_event in pygame.event.get():
            if file_input_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif file_input_event.type == pygame.KEYDOWN:
                if file_input_event.key == pygame.K_RETURN:
                    input_active = False
                elif file_input_event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input.append(file_input_event.unicode)

        # Render the current text
        screen.fill(gray)
        text_surface = font.render(''.join(user_input), True, black)
        screen.blit(text_surface, (10, SCREEN_SIZE // 2))
        pygame.display.flip()


    pygame.display.set_caption("Sudoku")  # Reset the window title
    return ''.join(user_input)

# Function to draw the cube

def draw_face(cube,face,corners):
    """
    Function to draw a face on a cube in pygame
    """
    upper_left, upper_right, lower_right, lower_left = corners

    # calculate size of a square within the face
    square_size = int((upper_right[0] - corners[0][0])/3)

    # width = 2 for outer square outline
    width=2

    # Draw outline, could we user draw.rectangle here instead?
    pygame.draw.line(screen, black, upper_left, upper_right, width)
    pygame.draw.line(screen, black, upper_right, lower_right, width)
    pygame.draw.line(screen, black, lower_right, lower_left, width)
    pygame.draw.line(screen, black, lower_left, upper_left, width)

    # draw inner grid
    # width=1 for inner grid
    width = 1
    # factor 1 and 2
    for factor in range(1,3):
        # horizontal line
        pygame.draw.line(
                screen,
                black,
                (upper_left[0],upper_left[1]+factor*square_size),
                (upper_right[0],upper_right[1]+factor*square_size),
                width
            )
        # vertical line
        pygame.draw.line(
                screen,
                black,
                (upper_left[0]+factor*square_size,upper_left[1]),
                (lower_left[0]+factor*square_size,lower_left[1]),
                width
            )

    # fill squares relative to upper_left corner
    x_1, y_1 = upper_left
    # poisitions 1-9 as defined in cube2
    for position in range(1,10):
        # new row
        if position in [4,7]:
            y_1+=square_size
        # first square in the row
        if position in [1,4,7]:
            x_1 = upper_left[0]
        # otherwise increment to next square
        else:
            x_1+=square_size
        # draw rectangle using color map and the color of the square in position on face
        rect = pygame.draw.rect(
                screen,
                color_map[cube.get_square(face,position)['color']],
                (x_1+1, y_1+1, square_size-1, square_size-1)
            )
        if cube.debug:
            text = pygame.font.Font(None, 15).render(
                    cube.get_square_label(face,position),
                    True,
                    black
                )
            screen.blit(text,text.get_rect(center = rect.center))


def draw_cube(cube):
    """
    Function to draw a rubik's cube in pygame
    """
    # padding size
    padding = 5
    # space occupied by a face and padding
    face_space = int(SCREEN_SIZE/4)
    # space occipied by a face without padding
    face_size = int(SCREEN_SIZE/4)-padding*2
    # middle of the screen
    middle = int(SCREEN_SIZE/2)
    # middle row top
    row_2 = middle-int(face_size/2)
    # top row top
    row_1 = row_2 - face_space
    # bottom row top
    row_3 = row_2 + face_space
    # upper left hand corner of each face, other corners will be calculated relative to this
    face_corners = {
        "L": (padding,row_2),
        "F": (face_space+padding,row_2),
        "R": (2*face_space+padding,row_2),
        "B": (3*face_space+padding,row_2),
        "U": (face_space+padding,row_1),
        "D": (face_space+padding,row_3)

    }

    for face,upper_left in face_corners.items():
        #calculate corners relative to upper left
        upper_right = (upper_left[0] + face_size, upper_left[1])
        lower_right = (upper_right[0],upper_right[1]+face_size)
        lower_left = (upper_left[0],lower_right[1])
        # draw the face
        draw_face(cube,face,(upper_left, upper_right, lower_right, lower_left))

# Main game loop
RUNNING = True
mycube = cube2.Cube()
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            # commands from cube main
            if event.key == pygame.K_s:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    FILENAME = get_filename("Enter filename to save:")
                    mycube.save(FILENAME)
                else:
                    mycube.scramble()
            elif event.key == pygame.K_u:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mycube.make_move("U'")
                else:
                    mycube.make_move("U")
            elif event.key == pygame.K_d:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # toggle debug mode
                    mycube.set_debug(not mycube.debug)
                elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mycube.make_move("D'")
                else:
                    mycube.make_move("D")
            elif event.key == pygame.K_r:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mycube.make_move("R'")
                else:
                    mycube.make_move("R")
            elif event.key == pygame.K_l:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mycube.make_move("L'")
                elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                    FILENAME = get_filename("Enter filename to load:")
                    mycube.load(FILENAME)
                else:
                    mycube.make_move("L")
            elif event.key == pygame.K_f:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mycube.make_move("F'")
                else:
                    mycube.make_move("F")
            elif event.key == pygame.K_b:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mycube.make_move("B'")
                else:
                    mycube.make_move("B")
            elif event.key == pygame.K_x:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    mycube.make_move("X'")
                else:
                    mycube.make_move("X")
            elif event.key == pygame.K_1:
                mycube.solve_white_cross()
            elif event.key == pygame.K_2:
                mycube.solve_white_corners()
            elif event.key == pygame.K_3:
                mycube.solve_second_layer()
            elif event.key == pygame.K_4:
                mycube.solve_yellow_cross()
            elif event.key == pygame.K_5:
                mycube.solve_yellow_edges()
            elif event.key == pygame.K_6:
                mycube.solve_yellow_corners()
            elif event.key == pygame.K_7:
                mycube.orient_yellow_corners()
            elif event.key == pygame.K_0:
                mycube.solve()
            elif  event.key ==  pygame.K_n:
                mycube = cube2.Cube()
            elif  event.key ==  pygame.K_q:
                RUNNING = False

    # Fill the screen with white
    screen.fill(gray)

    # Draw the grid and numbers on top
    #draw_grid(sudoku_board)
    draw_cube(mycube)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
