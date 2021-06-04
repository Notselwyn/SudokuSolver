import numpy as np
import pygame
import datetime


def main():
    # Enter sudoku here!!!
    # The numbers are the cells in the sudoku
    new_array = []
    first_array = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 0]
    ]
    first_array_flat = [x for y in first_array for x in y]
    new_array = np.nan_to_num(np.array(first_array.copy(), dtype=int))
    new_array_flat = [x for y in new_array for x in y]

    pygame.init()  # Start the pygame sequence
    clock = pygame.time.Clock()  # Create pygame clock
    size = [600, 700]  # Screen size
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

    def font_size(n):
        return pygame.font.Font('freesansbold.ttf', n)

    font = pygame.font.Font('freesansbold.ttf', 40)
    pygame.display.set_caption('Sudo Solver: Back Track')

    def render_screen(intro=False):
        for sub_row_index, sub_row in enumerate(new_array):
            for sub_num_index, sub_num in enumerate(sub_row):
                if sub_num != 0 or (intro is True and first_array[sub_row_index][sub_num_index] != 0):
                    if first_array[sub_row_index][sub_num_index] != 0:
                        text = font.render(str(first_array[sub_row_index][sub_num_index]), True, red, white)
                    else:
                        text = font.render(str(int(sub_num)), True, black, white)
                    textRect = text.get_rect()
                    textRect.center = (sub_num_index * 67 + 32, sub_row_index * 67 + 37)
                    screen.blit(text, textRect)


    # Required variables to start running
    # Some of these are not necessary, but more efficient
    num_index = 0
    fps = 200
    selected_num = 1
    plus_one = False
    ready = False
    spacing = 50
    select_num_offset = 10

    nums_to_click = []

    while ready is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEWHEEL:
                selected_num = (selected_num+event.y-1) % 9 + 1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if mouse_pos[1] > 600:
                    selected_num = range(1, 11)[max(0, (min(10, mouse_pos[0]//spacing-1)))]
                    if selected_num == 10:
                        ready = True
                    break

                elif 0 < mouse_pos[1] < 600:
                    first_array[mouse_pos[1]//(600 // 9)][mouse_pos[0]//(600 // 9)] = selected_num
                    first_array_flat = [x for y in first_array for x in y]
                    new_array = np.nan_to_num(np.array(first_array.copy(), dtype=int))
                    new_array_flat = [x for y in new_array for x in y]

            elif event.type == pygame.KEYDOWN:
                for i in range(1, 10):
                    if event.key == eval(f"pygame.K_{i}"):
                        selected_num = i
                        break

        # Updates the screen. This is necessary otherwise the screen will freeze
        for pos, button in enumerate(nums_to_click):
            screen.blit(button[0], button[1])

        screen.fill((255, 255, 255))
        screen.blit(grids, (0, 0))
        render_screen(intro=True)                   # Top left                   Mid right                  Down left
        pygame.draw.polygon(screen, (0, 210, 0), [[size[0]-90, size[1]-75], [size[0]-50, size[1]-55], [size[0]-90, size[1]-35]], 0)

        for i in range(1, 10):
            if i != selected_num:
                text = font_size(50).render(str(i), True, (100, 100, 255), white)
            else:
                text = font_size(70).render(str(i), True, (100, 100, 255), white)

            textRect = text.get_rect()
            textRect.center = (i*spacing+select_num_offset, 650)
            nums_to_click.append([text, textRect])
            screen.blit(text, textRect)

        pygame.display.flip()
        clock.tick(fps / 2)

    screen = pygame.display.set_mode((size[0], size[1]-100))
    time_now = datetime.datetime.now()

    while num_index < 81:
        new_array = np.reshape(new_array_flat, (9, 9))
        threebythree_box = new_array[(num_index // 27) * 3:(num_index // 27) * 3 + 3, num_index % 9 // 3 * 3:num_index % 9 // 3 * 3 + 3].tolist()
        crosshair_cells = new_array[num_index // 9, :].tolist() + new_array[:, num_index % 9].tolist() + [x for y in threebythree_box for x in y]
        if num_index == 80-first_array_flat[::-1].index(0):
            new_array[num_index // 9][num_index % 9] = [x for x in range(1, 10) if x not in crosshair_cells][-1]
            new_array_flat[num_index] = [x for x in range(1, 10) if x not in crosshair_cells][-1]

        # Removing the active num from crosshairs: Horizontal, Vertical, 3x3 Box
        crosshair_cells.pop(num_index % 9)
        crosshair_cells.pop(num_index // 9 + 8)
        crosshair_cells.pop(16 + num_index % 3 + num_index // 9 % 3 * 3)

        # Check if the number isn't one of the pre-defined one from the original sudoku\
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

            # Keep incrementing until theres a valid value, or back-track if value is 10
            while new_array_flat[num_index] in crosshair_cells and plus_one is False:
                new_array_flat[num_index] += 1
                if new_array_flat[num_index] > 9:
                    new_array_flat[num_index:] = first_array_flat[num_index:]
                    new_array = np.reshape(new_array_flat, (9, 9))
                    num_index -= 2
                    plus_one = True
                    break

        # If current value is a fixed value from sudoku, go back 1 cell
        elif plus_one is True:
            num_index -= 2

        num_index += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.blit(grids, (0, 0))
        render_screen()
        if int((datetime.datetime.now() - time_now).microseconds % 10) == 0:
            pygame.display.flip()

    print(f"Finished - {int((datetime.datetime.now() - time_now).total_seconds()*1000)}ms")
    for array_pos, array in enumerate(new_array):
        result_str = "\x1b[48;2;255;255;255m"
        if (array_pos+1) % 3 == 0 and 7 >= array_pos >= 2:
            result_str += "\x1b[38;2;0;0;0m\x1b[4m"
        result_str += " "
        for num_pos, num in enumerate(array):
            if num_pos % 3 == 0 and num_pos >= 3:
                result_str += "\x1b[38;2;0;0;0m| "

            if first_array[array_pos][num_pos] != 0:
                result_str += f"\x1b[38;2;255;0;0m{num}\x1b[38;2;0;0;0m "
            else:
                result_str += f"\x1b[38;2;0;0;0m{num} "
        result_str += "\x1b[0m"
        print(result_str)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
