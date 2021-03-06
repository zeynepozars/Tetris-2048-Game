import stddraw  # the stddraw module is used as a basic graphics library
import random  # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid  # class for modeling the game grid
from tetromino import Tetromino  # class for modeling the tetrominoes
from picture import Picture  # used representing images to display
import os  # used for file and directory operations
import numpy as np
from color import Color  # used for coloring the game menu

# Zeynep ÖZARSLAN 041802044
# Türkcan YILMAZ 041801116
# Sevag Pilibbos HERGEL 041801120


# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
    # set the dimensions of the game grid
    grid_h, grid_w = 17, 12
    # set the size of the drawing canvas
    canvas_h, canvas_w = 40 * grid_h, 40 * grid_w + 100
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.5, grid_w + 3)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino(grid_h, grid_w)
    grid.current_tetromino = current_tetromino


    # display a simple menu before opening the game
    display_game_menu(grid_h, grid_w)

    # initial score
    score = 0
    speed = 250 #initial speed

    # main game loop (keyboard interaction for moving the tetromino)
    while True:
        # check user interactions via the keyboard
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            # if the left arrow key has been pressed
            if key_typed == "left":
                # move the tetromino left by one
                current_tetromino.move(key_typed, grid)
            # if the right arrow key has been pressed
            elif key_typed == "right":
                # move the tetromino right by one
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # move the tetromino down by one
                # (causes the tetromino to fall down faster)
                current_tetromino.move(key_typed, grid)
            elif key_typed == "up":
                # rotate the tetromino 90 degree clock-wise
                current_tetromino.rotate(grid)
            elif key_typed == "space":
                # drop the tetromino
                for i in range(grid_h):
                 current_tetromino.move("down",grid)

            # clear the queue that stores all the keys pressed/typed
            stddraw.clearKeysTyped()

        # move (drop) the tetromino down by 1 at each iteration
        success = current_tetromino.move("down", grid)
        grid.connected_4()

        # place the tetromino on the game grid when it cannot go down anymore
        if not success:
            # get the tile matrix of the tetromino
            tiles_to_place = current_tetromino.tile_matrix
            # update the game grid by adding the tiles of the tetromino
            game_over = grid.update_grid(tiles_to_place)

            indv_score = 0  # starting value for a full row's score
            ind_score = 0  # starting value for a merged tiles score

            # check is_row_full for all rows
            for i in range(grid_h):
                grid.check_2048(grid.tile_matrix)
                # score from merged tiles
                ind_score = grid.update_score(grid.tile_num2)
                if grid.is_row_full(i, grid.tile_matrix):
                    # score from deleted full rows
                    indv_score = grid.update_score(grid.tile_num)
            grid.tile_num2 = np.zeros(100)  # for merged score
            score_val = ind_score + indv_score
            score += int(score_val)


            print(score)
            # end the main game loop if the game is over
            if game_over:
                break
            # increasing difficulty by increasing speed as the game process
            if score > 450:
                speed = 10
            elif score > 250:
                speed = 50
            elif score > 150:
                speed = 100
            if score > 10000:
                break
            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            current_tetromino = create_tetromino(grid_h, grid_w)
            grid.current_tetromino = current_tetromino

        # display the game grid and as well the current tetromino
        grid.display(score,speed)

    # finish the game and display game over
    finish_game(grid_h, grid_w)
    print("Game over")


# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
    # type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'L', 'J', 'S', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type, grid_height, grid_width)
    return tetromino

# Function for displaying game over
def finish_game(grid_height, grid_width):
    # colors used for the menu
    background_color = Color(28, 27, 36)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/game_over.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width + 2) / 2, grid_height - 10
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    stddraw.show(1000)

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    # colors used for the menu
    background_color = Color(28, 27, 36)
    button_color = Color(255, 255, 255)
    text_color = Color(0, 0, 0)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/menu_image.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width + 2) / 2, grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 1.5, 2
    # coordinates of the bottom left corner of the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # menu interaction loop
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
