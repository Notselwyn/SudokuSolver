import numpy as np
import pygame
import time


def main():
    # Enter sudoku here!!!
    # The numbers are the cells in the sudoku
    first_array = [
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


    run_pygame = bool(int(input("Run pygame? (Decreases performance 45x) (1/0): ")))

    if run_pygame:
        pygame.init()  # Start the pygame sequence
        clock = pygame.time.Clock()  # Create pygame clock
        size = [600, 600]  # Screen size

        # Defining colors
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)

        # Make a pygame screen window with a size of [250, 250]
        screen = pygame.display.set_mode(size)
        grids = pygame.surface.Surface(size)
        grids.fill([255, 255, 255])

        for i in range(1, 9):
            if i % 3 == 0:
                pygame.draw.line(grids, [0, 0, 0], (int(i * size[0] // 4.5 // 2), 0), (int(i * size[0] // 4.5 // 2), size[0]), 10)
                pygame.draw.line(grids, [0, 0, 0], (0, int(i * size[0] // 4.5 // 2)), (size[0], int(i * size[0] // 4.5 // 2)), 10)
            else:
                pygame.draw.line(grids, [0, 0, 0], (int(i * size[0] // 4.5 // 2), 0), (int(i * size[0] // 4.5 // 2), size[0]), 5)
                pygame.draw.line(grids, [0, 0, 0], (0, int(i * size[0] // 4.5 // 2)), (size[0], int(i * size[0] // 4.5 // 2)), 5)

        font = pygame.font.Font('freesansbold.ttf', 40)  # Make a font
        pygame.display.set_caption('Sudo Solver: Back Track')

        def render_screen():
            for sub_row_index, sub_row in enumerate(new_array):
                for sub_num_index, sub_num in enumerate(sub_row):
                    if sub_num != 0:
                        if first_array[sub_row_index][sub_num_index] != 0:
                            text = font.render(str(first_array[sub_row_index][sub_num_index]), True, red, white)
                        else:
                            text = font.render(str(int(sub_num)), True, black, white)

                        textRect = text.get_rect()
                        textRect.center = (sub_num_index * 67 + 32, sub_row_index * 67 + 37)
                        screen.blit(text, textRect)

    # Required variables to start running
    # Some of these are not necessary, but more efficient
    first_array_flat = [x for y in first_array for x in y]
    new_array = np.nan_to_num(np.array(first_array.copy(), dtype=int))
    new_array_flat = [x for y in new_array for x in y]
    num_index = 0
    plus_one = False

    time_now = time.time()

    while num_index < 81:
        if run_pygame is True:
            screen.blit(grids, (0, 0))
            render_screen()
            pygame.display.flip()

        new_array = np.reshape(new_array_flat, (9, 9))
        threebythree_box = new_array[(num_index // 27) * 3:(num_index // 27) * 3 + 3, num_index % 9 // 3 * 3:num_index % 9 // 3 * 3 + 3].tolist()
        crosshair_cells = new_array[num_index // 9, :].tolist() + new_array[:, num_index % 9].tolist() + [x for y in threebythree_box for x in y]

        # Removing the active num from crosshairs: Horizontal, Vertical, 3x3 Box
        crosshair_cells.pop(num_index % 9)
        crosshair_cells.pop(num_index // 9 + 8)
        crosshair_cells.pop(16 + ((num_index % 9) // 9) * 3 + (num_index % 3))

        # Check if the number isn't one of the pre-defined one from the original sudoku
        if first_array_flat[num_index] == 0:
            # Check if back-track is active, if it is then do +1, if it is over 9 after +1, keep it activated
            if plus_one is True:
                new_array_flat[num_index] += 1
                if new_array_flat[num_index] > 9:
                    new_array_flat[num_index:] = first_array_flat[num_index:]
                    new_array = np.reshape(new_array_flat, (9, 9))
                    num_index -= 2
                else:
                    plus_one = False
            
            # Keep +1'ing the value, until it's valid or if it hits 10, back track gets actived
            while new_array_flat[num_index] in crosshair_cells and plus_one is False:
                new_array_flat[num_index] += 1
                if new_array_flat[num_index] > 9:
                    new_array_flat[num_index:] = first_array_flat[num_index:]
                    new_array = np.reshape(new_array_flat, (9, 9))
                    num_index -= 2
                    plus_one = True
                    break
        
        # If back track is still enabled, remove -2 from the index, so the index will go 1 down
        elif plus_one is True:
            num_index -= 2

        num_index += 1
        if num_index < 0:
            num_index = 0
            if plus_one is True:
                plus_one = False
           
        # Check if user wants to quit pygame windows
        if run_pygame is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
    
    # Please don't look at this
    print("Finished - " + str(round(time.time() - time_now, 4)) + "s")
    print("\x1b[48;2;255;255;255m")
    for array_pos, array in enumerate(new_array):
        result_str = ""
        for num_pos, num in enumerate(array):
            if num_pos % 3 == 0 and num_pos >= 3:
                result_str += " \x1b[38;2;0;0;0m|"

            if first_array[array_pos][num_pos] != 0:
                result_str += f"\x1b[38;2;255;0;0m {num}"
            else:
                result_str += f"\x1b[38;2;0;0;0m {num}"
        print(result_str)
        if (array_pos+1) % 3 == 0 and 7 >= array_pos >= 2:
            print("\x1b[38;2;0;0;0m " + "-" * 21)
    print("")


    # Initiate the final screen in pygame
    if run_pygame is True:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            pygame.display.flip()
            clock.tick(30)


if __name__ == '__main__':
    main()
