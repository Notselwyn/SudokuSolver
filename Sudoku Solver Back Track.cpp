#include <iostream>
#include <chrono>

using namespace std::chrono;
using namespace std;

int main() {
    // Enter the sudoku here!!!
    // The numbers are the cells in the sudoku
    int first_array[9][9] = {{0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0}
    };
    int first_array_flat[81];
    int new_array[9][9];
    int new_array_flat[81];
    int threebythree_box[3][3];
    int crosshair_cells[25];
    int ra[81];
    int num_index = 0;
    bool plus_one = false;
    for (int i=0; i<9; i++) {
        for (int j=0; j<9; j++) {
            first_array_flat[i*9+j] = first_array[i][j];
            new_array_flat[i*9+j] = first_array[i][j];
            ra[i*9+j] = first_array[i][j];
            new_array[i][j] = first_array[i][j];
        }
    }
    for (int low=0, high=80; low < high; low++, high--){
        swap(ra[low], ra[high]);
    }
    int end_index = 80-*find(begin(ra), end(ra), 0);
    auto start = high_resolution_clock::now();
    while (num_index < 81) {
        for (int i=0; i<81; i++) {
            new_array[i/9][i%9] = new_array_flat[i];
        }

        for (int i=0; i<3; i++) {
            for (int j=0; j<3; j++) {
                threebythree_box[i][j] = new_array[(num_index / 27) * 3 + i][num_index % 9 / 3 * 3 + j];
            }
        }

        for (int i=0; i<9; i++) {
            if (i != num_index % 9) {
                crosshair_cells[i] = new_array[num_index/9][i];
            }
            if (i != num_index / 9) {
                crosshair_cells[i+9] = new_array[i][num_index % 9];
            }
            if (i != num_index % 3 + num_index / 9 % 3 * 3) {
                crosshair_cells[i+16] = threebythree_box[i/3][i%3];
            }
        }
        if (num_index == end_index) {
            for (int i=1; i<10; i++) {
                if (find(begin(crosshair_cells), end(crosshair_cells), i) == end(crosshair_cells)) {
                    new_array[end_index/9][end_index%9] = i;
                    break;
                }
            }
            auto stop = high_resolution_clock::now();
            auto duration = duration_cast<microseconds>(stop - start);
            cout << "Finished - " << duration.count()/1000 << "ms" << endl;
            for (int i=0; i<9; i++) {
                if (i%3==0 && i!=0) {
                    cout << "-------|-------|-------" << endl;
                }
                for (int j=0; j<9; j++) {
                    if (j%3==0 && j!=0) {
                        cout << " |";
                    }
                    cout << " " << new_array[i][j];
                }
                cout << endl;
            }
            cout << endl;
        }

        if (first_array_flat[num_index] == 0) {
            if (plus_one == true) {
                new_array_flat[num_index] += 1;
                if (new_array_flat[num_index] > 9) {
                    new_array_flat[num_index] = first_array_flat[num_index];
                    for (int i=0; i<81; i++) {
                        new_array[i/9][i%9] = new_array_flat[i];
                    }
                    num_index -= 2;
                } else {
                    plus_one = false;
                }
            }

            while (find(begin(crosshair_cells), end(crosshair_cells), new_array_flat[num_index]) != end(crosshair_cells) && plus_one == false) {
                new_array_flat[num_index] += 1;
                if (new_array_flat[num_index] > 9) {
                    new_array_flat[num_index] = first_array_flat[num_index];
                    for (int i=0; i<81; i++) {
                        new_array[i/9][i%9] = new_array_flat[i];
                    }
                    num_index -= 2;
                    plus_one = true;
                }
            }
        } else if (plus_one == true) {
            num_index -= 2;
        }
        num_index += 1;
    }
    return 0;
}
