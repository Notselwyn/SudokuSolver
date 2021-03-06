import numpy as np
import datetime


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
        [0, 0, 0, 0, 8, 0, 0, 7, 0]
    ]

    # Required variables to start running
    # Some of these are not necessary, but more efficient
    first_array_flat = [x for y in first_array for x in y]
    new_array = np.nan_to_num(np.array(first_array.copy(), dtype=int))
    new_array_flat = [x for y in new_array for x in y]
    num_index = 0
    plus_one = False

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


if __name__ == '__main__':
    main()
